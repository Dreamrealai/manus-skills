#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types

CATALOG_PATH = Path(__file__).with_name("model_catalog.json")


def load_catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def resolve_alias(alias: str) -> tuple[str, dict]:
    catalog = load_catalog()
    meta = catalog["models"].get(alias)
    if not meta:
        raise SystemExit(f"Unknown alias: {alias}")
    return meta["api_model"], meta


def dreamreal_call(payload: dict) -> dict:
    command = [
        "manus-mcp-cli",
        "tool",
        "call",
        "dreamreal",
        "--server",
        "dreamreal",
        "--input",
        json.dumps(payload),
    ]
    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "DreamReal call failed")
    stdout = proc.stdout.strip()
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {"raw": stdout}


def poll_job(job_id: str, interval_seconds: int, max_wait_seconds: int) -> dict:
    deadline = time.time() + max_wait_seconds
    while time.time() < deadline:
        status = dreamreal_call({"action": "check_job_status", "job_id": job_id, "include": "summary"})
        state = status.get("status") or status.get("job", {}).get("status") or status.get("state")
        if state in {"completed", "failed", "cancelled", "error"}:
            return status
        time.sleep(interval_seconds)
    return {"status": "timeout", "job_id": job_id}


def gemini_image_fallback(prompt: str, alias: str, output_path: str | None) -> dict:
    model_name, meta = resolve_alias(alias)
    client = genai.Client()
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
    )
    saved_files = []
    for idx, part in enumerate(response.candidates[0].content.parts):
        if getattr(part, "inline_data", None):
            path = output_path or f"image_{idx}.png"
            if idx and output_path:
                suffix = Path(output_path).suffix or ".png"
                stem = str(Path(output_path).with_suffix(""))
                path = f"{stem}_{idx}{suffix}"
            Path(path).write_bytes(part.inline_data.data)
            saved_files.append(path)
    return {
        "provider": "gemini",
        "alias": alias,
        "api_model": model_name,
        "files": saved_files,
        "notes": meta.get("notes"),
    }


def gemini_video_fallback(args: argparse.Namespace, alias: str) -> dict:
    model_name, meta = resolve_alias(alias)
    client = genai.Client()
    config_kwargs = {
        "numberOfVideos": args.count,
        "durationSeconds": args.duration_seconds,
        "aspectRatio": args.aspect_ratio,
        "generateAudio": True,
    }
    config_kwargs = {key: value for key, value in config_kwargs.items() if value not in (None, "")}
    prompt = args.prompt
    reference_notes = []
    if args.image_url:
        reference_notes.append(f"image_url={args.image_url}")
    if args.first_frame_url:
        reference_notes.append(f"first_frame_url={args.first_frame_url}")
    if args.last_frame_url:
        reference_notes.append(f"last_frame_url={args.last_frame_url}")
    if args.reference_image_urls:
        reference_notes.append("reference_image_urls=" + ", ".join(args.reference_image_urls))
    if reference_notes:
        prompt = prompt + "\n\nReference context preserved from the original request: " + " | ".join(reference_notes)
    operation = client.models.generate_videos(
        model=model_name,
        source=types.GenerateVideosSource(prompt=prompt),
        config=types.GenerateVideosConfig(**config_kwargs),
    )
    deadline = time.time() + args.max_wait
    while not operation.done and time.time() < deadline:
        time.sleep(max(10, args.poll_interval))
        operation = client.operations.get(operation)
    if not operation.done:
        return {
            "provider": "gemini",
            "alias": alias,
            "api_model": model_name,
            "status": "timeout",
            "message": "Gemini Veo fallback did not finish before max wait elapsed.",
        }
    result = operation.result
    generated = []
    for item in getattr(result, "generated_videos", []) or []:
        video = getattr(item, "video", None)
        generated.append(
            {
                "uri": getattr(video, "uri", None),
                "mime_type": getattr(video, "mime_type", None),
            }
        )
    return {
        "provider": "gemini",
        "alias": alias,
        "api_model": model_name,
        "videos": generated,
        "notes": meta.get("notes"),
        "fallback_mode": "veo_direct",
        "reference_handling": "Text-preserved fallback. DreamReal remains the preferred route for rich reference-controlled video workflows.",
    }


def build_dreamreal_payload(args: argparse.Namespace, alias: str | None) -> dict:
    action = {"image": "generate_image", "video": "generate_video", "music": "generate_audio"}[args.mode]
    payload = {"action": action, "prompt": args.prompt, "orchestrate": args.orchestrate}
    if args.count:
        payload["count"] = args.count
    if args.aspect_ratio:
        payload["aspect_ratio"] = args.aspect_ratio
    if args.duration_seconds:
        payload["duration_seconds"] = args.duration_seconds
    if args.image_url:
        payload["image_url"] = args.image_url
    if args.first_frame_url:
        payload["first_frame_url"] = args.first_frame_url
    if args.last_frame_url:
        payload["last_frame_url"] = args.last_frame_url
    if args.reference_image_urls:
        payload["reference_image_urls"] = args.reference_image_urls
    if alias:
        model_name, _ = resolve_alias(alias)
        payload["model"] = model_name
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="DreamReal-first helper for Gemini media tasks.")
    parser.add_argument("--mode", required=True, choices=["image", "video", "music"])
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--provider", choices=["auto", "dreamreal", "gemini"], default="auto")
    parser.add_argument("--alias", help="Optional alias override from model_catalog.json")
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--aspect-ratio")
    parser.add_argument("--duration-seconds", type=int)
    parser.add_argument("--image-url")
    parser.add_argument("--first-frame-url")
    parser.add_argument("--last-frame-url")
    parser.add_argument("--reference-image-urls", nargs="*")
    parser.add_argument("--orchestrate", action="store_true")
    parser.add_argument("--poll", action="store_true")
    parser.add_argument("--poll-interval", type=int, default=20)
    parser.add_argument("--max-wait", type=int, default=900)
    parser.add_argument("--output")
    parser.add_argument("--json-output")
    args = parser.parse_args()

    catalog = load_catalog()
    default_alias = {
        "image": catalog["defaults"]["image"],
        "video": catalog["defaults"]["video"],
        "music": catalog["defaults"]["music"],
    }[args.mode]
    alias = args.alias or default_alias

    result = None
    if args.provider in {"auto", "dreamreal"}:
        try:
            result = dreamreal_call(build_dreamreal_payload(args, alias))
            job_id = result.get("job_id")
            if job_id and args.poll:
                result = {
                    "submitted": result,
                    "final": poll_job(job_id, args.poll_interval if args.mode != "image" else max(10, args.poll_interval), args.max_wait),
                }
        except Exception as exc:
            if args.provider == "dreamreal":
                raise
            result = {"provider": "dreamreal", "error": str(exc), "fallback_attempted": False}

    if args.provider == "gemini" or (args.provider == "auto" and (not result or result.get("error"))):
        if args.mode == "image":
            result = gemini_image_fallback(args.prompt, alias, args.output)
        elif args.mode == "video":
            result = gemini_video_fallback(args, alias)
        else:
            result = {
                "provider": "gemini",
                "alias": alias,
                "status": "manual_fallback_required",
                "message": "DreamReal-first execution failed or was skipped. Gemini music fallback remains manual until a stable direct Lyria path is verified in the installed SDK.",
            }

    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.json_output:
        Path(args.json_output).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
