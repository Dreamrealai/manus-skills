#!/usr/bin/env python3
"""Gemini Video Generation Script (Veo 3.1).

Generates videos using Veo 3.1 with support for text-to-video, image-to-video,
and reference-to-video modes.

Usage:
    python video_generation.py --prompt "A sunset over the ocean" --output sunset.mp4
    python video_generation.py --prompt "A cat walking" --image cat.jpg --output cat_walk.mp4
    python video_generation.py --prompt "Fashion show" --references ref1.jpg ref2.jpg --output fashion.mp4
"""
import argparse
import json
import os
import sys
import time

from google import genai
from google.genai import types


DEFAULT_MODEL = "veo-3.1-generate-preview"
POLL_INTERVAL = 10


def _poll_operation(client: genai.Client, operation) -> object:
    """Poll an operation until it completes."""
    while not operation.done:
        print("Waiting for video generation...")
        time.sleep(POLL_INTERVAL)
        operation = client.operations.get(name=operation.name)
    return operation


def _download_and_save(client: genai.Client, operation, output_path: str):
    """Download the generated video from a completed operation and save to disk."""
    video = operation.response.generated_videos[0]
    video_bytes = client.files.download(name=video.video.name)
    with open(output_path, "wb") as f:
        f.write(video_bytes)


def generate_text_to_video(
    client: genai.Client,
    prompt: str,
    model: str,
    output_path: str,
    aspect_ratio: str = "16:9",
    resolution: str | None = None,
) -> dict:
    """Generate a video from a text prompt."""
    config_kwargs = {}
    if aspect_ratio:
        config_kwargs["aspect_ratio"] = aspect_ratio
    if resolution:
        config_kwargs["resolution"] = resolution

    config = types.GenerateVideosConfig(**config_kwargs) if config_kwargs else None

    operation = client.models.generate_videos(
        model=model,
        prompt=prompt,
        config=config,
    )

    operation = _poll_operation(client, operation)
    _download_and_save(client, operation, output_path)
    return {"mode": "text-to-video", "model": model, "output": output_path}


def generate_image_to_video(
    client: genai.Client,
    prompt: str,
    image_path: str,
    model: str,
    output_path: str,
    aspect_ratio: str = "16:9",
) -> dict:
    """Generate a video from an image (first frame) and text prompt."""
    # Upload the image via File API
    uploaded_image = client.files.upload(file=image_path)
    while uploaded_image.state.name == "PROCESSING":
        time.sleep(3)
        uploaded_image = client.files.get(name=uploaded_image.name)

    operation = client.models.generate_videos(
        model=model,
        prompt=prompt,
        image=uploaded_image,
        config=types.GenerateVideosConfig(aspect_ratio=aspect_ratio),
    )

    operation = _poll_operation(client, operation)
    _download_and_save(client, operation, output_path)
    return {"mode": "image-to-video", "model": model, "output": output_path}


def generate_reference_to_video(
    client: genai.Client,
    prompt: str,
    reference_paths: list[str],
    model: str,
    output_path: str,
    aspect_ratio: str = "16:9",
) -> dict:
    """Generate a video using reference images (up to 3) to guide content."""
    reference_images = []
    for ref_path in reference_paths[:3]:
        uploaded = client.files.upload(file=ref_path)
        while uploaded.state.name == "PROCESSING":
            time.sleep(3)
            uploaded = client.files.get(name=uploaded.name)
        ref = types.VideoGenerationReferenceImage(
            image=uploaded,
            reference_type="asset",
        )
        reference_images.append(ref)

    operation = client.models.generate_videos(
        model=model,
        prompt=prompt,
        reference_images=reference_images,
        config=types.GenerateVideosConfig(aspect_ratio=aspect_ratio),
    )

    operation = _poll_operation(client, operation)
    _download_and_save(client, operation, output_path)
    return {"mode": "reference-to-video", "model": model, "output": output_path, "num_references": len(reference_paths)}


def main():
    parser = argparse.ArgumentParser(description="Gemini Video Generation (Veo 3.1)")
    parser.add_argument("--prompt", required=True, help="Video generation prompt")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model ID (default: {DEFAULT_MODEL})")
    parser.add_argument("--output", default="generated_video.mp4", help="Output file path")
    parser.add_argument("--image", default=None, help="Input image for image-to-video mode")
    parser.add_argument("--references", nargs="*", help="Reference image paths (up to 3) for reference-to-video mode")
    parser.add_argument("--aspect-ratio", default="16:9", choices=["16:9", "9:16"], help="Aspect ratio")
    parser.add_argument("--resolution", default=None, choices=["720p", "1080p", "4k"], help="Output resolution")
    args = parser.parse_args()

    client = genai.Client()

    if args.references:
        result = generate_reference_to_video(client, args.prompt, args.references, args.model, args.output, args.aspect_ratio)
    elif args.image:
        result = generate_image_to_video(client, args.prompt, args.image, args.model, args.output, args.aspect_ratio)
    else:
        result = generate_text_to_video(client, args.prompt, args.model, args.output, args.aspect_ratio, args.resolution)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
