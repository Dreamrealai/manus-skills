#!/usr/bin/env python3
"""Gemini Video Analysis Script.

Analyzes videos using Gemini 3.1 Pro with MANDATORY 24fps frame extraction.
Supports local files (inline < 20MB, File API for larger), YouTube URLs, and structured JSON output.

Usage:
    python video_analysis.py --prompt "Describe this video" --video video.mp4 [--schema SCHEMA_JSON]
    python video_analysis.py --prompt "Summarize" --youtube "https://youtube.com/watch?v=..."
"""
import argparse
import json
import os
import sys
import time

from google import genai
from google.genai import types


DEFAULT_MODEL = "gemini-3.1-pro-preview"
DEFAULT_THINKING = "high"
ENFORCED_FPS = 24
INLINE_MAX_BYTES = 20 * 1024 * 1024  # 20 MB


def analyze_video_inline(
    client: genai.Client,
    video_path: str,
    prompt: str,
    model: str,
    thinking_level: str,
    response_schema: dict | None,
) -> dict:
    """Analyze a video file < 20MB using inline data with 24fps."""
    with open(video_path, "rb") as f:
        video_bytes = f.read()

    parts = [
        types.Part(
            inline_data=types.Blob(data=video_bytes, mime_type="video/mp4"),
            video_metadata=types.VideoMetadata(fps=ENFORCED_FPS),
        ),
        types.Part(text=prompt),
    ]

    config_kwargs: dict = {
        "thinking_config": types.ThinkingConfig(thinking_level=thinking_level),
    }
    if response_schema:
        config_kwargs["response_mime_type"] = "application/json"
        config_kwargs["response_schema"] = response_schema

    response = client.models.generate_content(
        model=model,
        contents=types.Content(parts=parts),
        config=types.GenerateContentConfig(**config_kwargs),
    )
    return _parse_response(response, response_schema)


def analyze_video_file_api(
    client: genai.Client,
    video_path: str,
    prompt: str,
    model: str,
    thinking_level: str,
    response_schema: dict | None,
) -> dict:
    """Analyze a video file >= 20MB using the File API with 24fps."""
    print(f"Uploading {video_path} via File API...")
    uploaded = client.files.upload(file=video_path)

    # Wait for processing
    while uploaded.state.name == "PROCESSING":
        print("  Waiting for file processing...")
        time.sleep(5)
        uploaded = client.files.get(name=uploaded.name)

    if uploaded.state.name != "ACTIVE":
        raise RuntimeError(f"File upload failed with state: {uploaded.state.name}")

    parts = [
        types.Part(
            file_data=types.FileData(file_uri=uploaded.uri, mime_type="video/mp4"),
            video_metadata=types.VideoMetadata(fps=ENFORCED_FPS),
        ),
        types.Part(text=prompt),
    ]

    config_kwargs: dict = {
        "thinking_config": types.ThinkingConfig(thinking_level=thinking_level),
    }
    if response_schema:
        config_kwargs["response_mime_type"] = "application/json"
        config_kwargs["response_schema"] = response_schema

    response = client.models.generate_content(
        model=model,
        contents=types.Content(parts=parts),
        config=types.GenerateContentConfig(**config_kwargs),
    )
    return _parse_response(response, response_schema)


def analyze_youtube(
    client: genai.Client,
    youtube_url: str,
    prompt: str,
    model: str,
    thinking_level: str,
    response_schema: dict | None,
) -> dict:
    """Analyze a YouTube video by URL with 24fps."""
    parts = [
        types.Part(
            file_data=types.FileData(file_uri=youtube_url, mime_type="video/mp4"),
            video_metadata=types.VideoMetadata(fps=ENFORCED_FPS),
        ),
        types.Part(text=prompt),
    ]

    config_kwargs: dict = {
        "thinking_config": types.ThinkingConfig(thinking_level=thinking_level),
    }
    if response_schema:
        config_kwargs["response_mime_type"] = "application/json"
        config_kwargs["response_schema"] = response_schema

    response = client.models.generate_content(
        model=model,
        contents=types.Content(parts=parts),
        config=types.GenerateContentConfig(**config_kwargs),
    )
    return _parse_response(response, response_schema)


def _parse_response(response, response_schema: dict | None) -> dict:
    """Parse a Gemini response into a result dict."""
    result: dict = {}
    if response_schema:
        try:
            result["structured_output"] = json.loads(response.text)
        except json.JSONDecodeError:
            result["raw_text"] = response.text
    else:
        result["text"] = response.text
    result["fps"] = ENFORCED_FPS
    return result


def main():
    parser = argparse.ArgumentParser(description="Gemini Video Analysis (24fps enforced)")
    parser.add_argument("--prompt", required=True, help="Analysis prompt")
    parser.add_argument("--video", default=None, help="Local video file path")
    parser.add_argument("--youtube", default=None, help="YouTube URL")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model ID (default: {DEFAULT_MODEL})")
    parser.add_argument("--thinking", default=DEFAULT_THINKING, choices=["minimal", "low", "medium", "high"])
    parser.add_argument("--schema", default=None, help="JSON schema string for structured output")
    parser.add_argument("--output", default=None, help="Output JSON file path")
    args = parser.parse_args()

    if not args.video and not args.youtube:
        parser.error("Provide either --video or --youtube")

    client = genai.Client()
    schema = json.loads(args.schema) if args.schema else None

    if args.youtube:
        result = analyze_youtube(client, args.youtube, args.prompt, args.model, args.thinking, schema)
    else:
        file_size = os.path.getsize(args.video)
        if file_size < INLINE_MAX_BYTES:
            result = analyze_video_inline(client, args.video, args.prompt, args.model, args.thinking, schema)
        else:
            result = analyze_video_file_api(client, args.video, args.prompt, args.model, args.thinking, schema)

    output_json = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output_json)
        print(f"Result saved to {args.output}")
    else:
        print(output_json)


if __name__ == "__main__":
    main()
