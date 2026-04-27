#!/usr/bin/env python3
"""Gemini Batch Orchestrator.

Central orchestrator for handling large batches of Gemini API requests with:
  - Up to 10 parallel API calls at a time
  - Random jitter between each call to avoid thundering herd
  - Automatic retry with exponential backoff on rate-limit (429) errors
  - Structured JSON responses for all requests
  - Smart batching: images in groups of 10, videos in groups of 5

Batching Logic:
  - Under 10 items: each item is processed as an individual parallel call.
  - 10+ images: grouped into batches of 10 per API call (array submission).
  - 10+ videos: grouped into batches of 5 per API call.

Usage:
    # Analyze a batch of images
    python gemini_orchestrator.py --mode analyze_images --files img1.jpg img2.jpg ... --prompt "Describe" --schema '{"type":"object",...}'

    # Analyze a batch of videos
    python gemini_orchestrator.py --mode analyze_videos --files v1.mp4 v2.mp4 ... --prompt "Summarize"

    # Generate multiple images
    python gemini_orchestrator.py --mode generate_images --prompts prompts.json --output-dir ./out

    # Generate TTS for multiple texts
    python gemini_orchestrator.py --mode generate_tts --prompts prompts.json --output-dir ./out
"""
import argparse
import asyncio
import json
import mimetypes
import os
import random
import sys
import time
import traceback
import wave
from pathlib import Path

from google import genai
from google.genai import types


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MAX_CONCURRENT = 10
MAX_RETRIES = 5
BASE_BACKOFF = 2.0
JITTER_MIN = 0.1
JITTER_MAX = 1.5
ENFORCED_FPS = 24
INLINE_MAX_BYTES = 20 * 1024 * 1024  # 20 MB

DEFAULT_ANALYSIS_MODEL = "gemini-3.1-pro-preview"
DEFAULT_THINKING = "high"
DEFAULT_IMAGE_MODEL = "gemini-3.1-flash-image-preview"
DEFAULT_TTS_MODEL = "gemini-2.5-flash-preview-tts"

IMAGE_BATCH_SIZE = 10
VIDEO_BATCH_SIZE = 5


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _jitter() -> float:
    return random.uniform(JITTER_MIN, JITTER_MAX)


async def _retry_with_backoff(coro_factory, task_id: str = ""):
    """Execute an async coroutine factory with exponential backoff on rate-limit errors."""
    for attempt in range(MAX_RETRIES):
        try:
            await asyncio.sleep(_jitter())
            return await coro_factory()
        except Exception as e:
            err_str = str(e).lower()
            is_rate_limit = "429" in err_str or "rate" in err_str or "resource_exhausted" in err_str
            if is_rate_limit and attempt < MAX_RETRIES - 1:
                wait = BASE_BACKOFF * (2 ** attempt) + _jitter()
                print(f"  [{task_id}] Rate limited (attempt {attempt + 1}/{MAX_RETRIES}). Retrying in {wait:.1f}s...")
                await asyncio.sleep(wait)
            else:
                print(f"  [{task_id}] Error: {e}")
                return {"error": str(e), "task_id": task_id}
    return {"error": "Max retries exceeded", "task_id": task_id}


def _load_image_part(path: str) -> types.Part:
    mime, _ = mimetypes.guess_type(path)
    mime = mime or "image/jpeg"
    with open(path, "rb") as f:
        data = f.read()
    return types.Part(inline_data=types.Blob(data=data, mime_type=mime))


def _load_video_part_inline(path: str) -> types.Part:
    with open(path, "rb") as f:
        data = f.read()
    return types.Part(
        inline_data=types.Blob(data=data, mime_type="video/mp4"),
        video_metadata=types.VideoMetadata(fps=ENFORCED_FPS),
    )


def _chunk_list(lst: list, size: int) -> list[list]:
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def _save_wav(filename: str, pcm_data: bytes, channels: int = 1, rate: int = 24000, sample_width: int = 2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_data)


# ---------------------------------------------------------------------------
# Analysis Tasks (using client.aio for true async)
# ---------------------------------------------------------------------------
async def _analyze_image_batch(
    client: genai.Client,
    image_paths: list[str],
    prompt: str,
    model: str,
    thinking_level: str,
    response_schema: dict | None,
    batch_id: str,
) -> dict:
    """Analyze a batch of images in a single API call."""
    parts = [_load_image_part(p) for p in image_paths]
    parts.append(types.Part(text=prompt))

    config_kwargs: dict = {
        "thinking_config": types.ThinkingConfig(thinking_level=thinking_level),
    }
    if response_schema:
        config_kwargs["response_mime_type"] = "application/json"
        config_kwargs["response_schema"] = response_schema

    async def _call():
        response = await client.aio.models.generate_content(
            model=model,
            contents=types.Content(parts=parts),
            config=types.GenerateContentConfig(**config_kwargs),
        )
        result = {"batch_id": batch_id, "files": image_paths}
        if response_schema:
            try:
                result["structured_output"] = json.loads(response.text)
            except json.JSONDecodeError:
                result["raw_text"] = response.text
        else:
            result["text"] = response.text
        return result

    return await _retry_with_backoff(_call, task_id=batch_id)


async def _analyze_video_batch(
    client: genai.Client,
    video_paths: list[str],
    prompt: str,
    model: str,
    thinking_level: str,
    response_schema: dict | None,
    batch_id: str,
) -> dict:
    """Analyze a batch of videos in a single API call (24fps enforced)."""
    config_kwargs: dict = {
        "thinking_config": types.ThinkingConfig(thinking_level=thinking_level),
    }
    if response_schema:
        config_kwargs["response_mime_type"] = "application/json"
        config_kwargs["response_schema"] = response_schema

    async def _call():
        # Build parts inside _call so uploads are retried on failure
        parts = []
        for vp in video_paths:
            file_size = os.path.getsize(vp)
            if file_size < INLINE_MAX_BYTES:
                parts.append(_load_video_part_inline(vp))
            else:
                uploaded = await client.aio.files.upload(file=vp)
                while uploaded.state.name == "PROCESSING":
                    await asyncio.sleep(3)
                    uploaded = await client.aio.files.get(name=uploaded.name)
                parts.append(
                    types.Part(
                        file_data=types.FileData(file_uri=uploaded.uri, mime_type="video/mp4"),
                        video_metadata=types.VideoMetadata(fps=ENFORCED_FPS),
                    )
                )
        parts.append(types.Part(text=prompt))

        response = await client.aio.models.generate_content(
            model=model,
            contents=types.Content(parts=parts),
            config=types.GenerateContentConfig(**config_kwargs),
        )
        result = {"batch_id": batch_id, "files": video_paths, "fps": ENFORCED_FPS}
        if response_schema:
            try:
                result["structured_output"] = json.loads(response.text)
            except json.JSONDecodeError:
                result["raw_text"] = response.text
        else:
            result["text"] = response.text
        return result

    return await _retry_with_backoff(_call, task_id=batch_id)


# ---------------------------------------------------------------------------
# Generation Tasks (using client.aio for true async)
# ---------------------------------------------------------------------------
async def _generate_image(
    client: genai.Client,
    prompt: str,
    model: str,
    output_path: str,
    task_id: str,
) -> dict:
    """Generate a single image."""
    async def _call():
        response = await client.aio.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                with open(output_path, "wb") as f:
                    f.write(part.inline_data.data)
                return {"task_id": task_id, "prompt": prompt, "output": output_path}
        return {"task_id": task_id, "error": "No image in response"}

    return await _retry_with_backoff(_call, task_id=task_id)


async def _generate_tts(
    client: genai.Client,
    text: str,
    model: str,
    voice: str,
    output_path: str,
    task_id: str,
) -> dict:
    """Generate a single TTS audio file."""
    async def _call():
        response = await client.aio.models.generate_content(
            model=model,
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)
                    )
                ),
            ),
        )
        audio_data = response.candidates[0].content.parts[0].inline_data.data
        _save_wav(output_path, audio_data)
        return {"task_id": task_id, "text": text[:80], "output": output_path}

    return await _retry_with_backoff(_call, task_id=task_id)


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------
async def orchestrate_analysis(
    file_paths: list[str],
    prompt: str,
    mode: str,
    model: str = DEFAULT_ANALYSIS_MODEL,
    thinking_level: str = DEFAULT_THINKING,
    response_schema: dict | None = None,
) -> list[dict]:
    """Orchestrate batch analysis of images or videos."""
    client = genai.Client()
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    is_video = mode == "analyze_videos"
    batch_size = VIDEO_BATCH_SIZE if is_video else IMAGE_BATCH_SIZE
    analyze_fn = _analyze_video_batch if is_video else _analyze_image_batch

    # Decide batching strategy
    if len(file_paths) < 10:
        # Individual parallel calls
        batches = [[fp] for fp in file_paths]
    else:
        batches = _chunk_list(file_paths, batch_size)

    async def _sem_task(batch, batch_id):
        async with semaphore:
            return await analyze_fn(client, batch, prompt, model, thinking_level, response_schema, batch_id)

    tasks = [_sem_task(batch, f"batch_{i}") for i, batch in enumerate(batches)]
    results = await asyncio.gather(*tasks)
    return list(results)


async def orchestrate_image_generation(
    prompts: list[dict],
    output_dir: str,
    model: str = DEFAULT_IMAGE_MODEL,
) -> list[dict]:
    """Orchestrate batch image generation."""
    client = genai.Client()
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    os.makedirs(output_dir, exist_ok=True)

    async def _sem_task(item, idx):
        async with semaphore:
            prompt_text = item.get("prompt", item) if isinstance(item, dict) else str(item)
            filename = item.get("filename", f"image_{idx}.png") if isinstance(item, dict) else f"image_{idx}.png"
            output_path = os.path.join(output_dir, filename)
            return await _generate_image(client, prompt_text, model, output_path, f"img_{idx}")

    tasks = [_sem_task(p, i) for i, p in enumerate(prompts)]
    results = await asyncio.gather(*tasks)
    return list(results)


async def orchestrate_tts_generation(
    prompts: list[dict],
    output_dir: str,
    model: str = DEFAULT_TTS_MODEL,
    voice: str = "Kore",
) -> list[dict]:
    """Orchestrate batch TTS generation."""
    client = genai.Client()
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    os.makedirs(output_dir, exist_ok=True)

    async def _sem_task(item, idx):
        async with semaphore:
            text = item.get("text", str(item)) if isinstance(item, dict) else str(item)
            v = item.get("voice", voice) if isinstance(item, dict) else voice
            filename = item.get("filename", f"tts_{idx}.wav") if isinstance(item, dict) else f"tts_{idx}.wav"
            output_path = os.path.join(output_dir, filename)
            return await _generate_tts(client, text, model, v, output_path, f"tts_{idx}")

    tasks = [_sem_task(p, i) for i, p in enumerate(prompts)]
    results = await asyncio.gather(*tasks)
    return list(results)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Gemini Batch Orchestrator")
    parser.add_argument("--mode", required=True, choices=["analyze_images", "analyze_videos", "generate_images", "generate_tts"], help="Operation mode")
    parser.add_argument("--files", nargs="*", help="File paths for analysis modes")
    parser.add_argument("--prompt", default=None, help="Prompt for analysis modes")
    parser.add_argument("--prompts", default=None, help="JSON file with prompts for generation modes")
    parser.add_argument("--model", default=None, help="Override default model")
    parser.add_argument("--thinking", default=DEFAULT_THINKING, choices=["minimal", "low", "medium", "high"])
    parser.add_argument("--schema", default=None, help="JSON schema string for structured output")
    parser.add_argument("--output-dir", default="./output", help="Output directory for generation modes")
    parser.add_argument("--output", default=None, help="Output JSON file for results")
    parser.add_argument("--voice", default="Kore", help="Default TTS voice")
    args = parser.parse_args()

    schema = json.loads(args.schema) if args.schema else None

    if args.mode in ("analyze_images", "analyze_videos"):
        if not args.files or not args.prompt:
            parser.error("--files and --prompt required for analysis modes")
        model = args.model or DEFAULT_ANALYSIS_MODEL
        results = asyncio.run(orchestrate_analysis(args.files, args.prompt, args.mode, model, args.thinking, schema))

    elif args.mode == "generate_images":
        if not args.prompts:
            parser.error("--prompts JSON file required for generate_images mode")
        with open(args.prompts) as f:
            prompts = json.load(f)
        model = args.model or DEFAULT_IMAGE_MODEL
        results = asyncio.run(orchestrate_image_generation(prompts, args.output_dir, model))

    elif args.mode == "generate_tts":
        if not args.prompts:
            parser.error("--prompts JSON file required for generate_tts mode")
        with open(args.prompts) as f:
            prompts = json.load(f)
        model = args.model or DEFAULT_TTS_MODEL
        results = asyncio.run(orchestrate_tts_generation(prompts, args.output_dir, model, args.voice))

    output_json = json.dumps(results, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output_json)
        print(f"Results saved to {args.output}")
    else:
        print(output_json)

    # Summary
    errors = sum(1 for r in results if isinstance(r, dict) and "error" in r)
    print(f"\n--- Summary ---")
    print(f"Total tasks: {len(results)}")
    print(f"Successful: {len(results) - errors}")
    print(f"Errors: {errors}")


if __name__ == "__main__":
    main()
