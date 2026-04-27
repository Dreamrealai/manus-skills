#!/usr/bin/env python3
"""Gemini Image Generation Script.

Generates images using Gemini native image models (Nano Banana) or Imagen 4.
Default model: gemini-3.1-flash-image-preview (Nano Banana 2).

Usage:
    python image_generation.py --prompt "A cat on the moon" [--model MODEL] [--output output.png]
    python image_generation.py --prompt "A logo" --model imagen-4.0-generate-001 --output logo.png
"""
import argparse
import json
import os
import sys

from google import genai
from google.genai import types


DEFAULT_MODEL = "gemini-3.1-flash-image-preview"
IMAGEN_MODELS = [
    "imagen-4.0-generate-001",
    "imagen-4.0-ultra-generate-001",
    "imagen-4.0-fast-generate-001",
]


def generate_with_gemini_native(
    client: genai.Client,
    prompt: str,
    model: str,
    output_path: str,
) -> dict:
    """Generate an image using Gemini native image models (Nano Banana family)."""
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        ),
    )

    result = {"model": model, "prompt": prompt}
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            img_data = part.inline_data.data
            if not output_path.endswith(".png"):
                output_path = output_path.rsplit(".", 1)[0] + ".png" if "." in output_path else output_path + ".png"
            with open(output_path, "wb") as f:
                f.write(img_data)
            result["output_path"] = output_path
            result["size_bytes"] = len(img_data)
            break
    return result


def generate_with_imagen(
    client: genai.Client,
    prompt: str,
    model: str,
    output_path: str,
    num_images: int = 1,
) -> dict:
    """Generate images using Imagen 4 models."""
    response = client.models.generate_images(
        model=model,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=num_images,
        ),
    )

    result = {"model": model, "prompt": prompt, "images": []}
    for i, image in enumerate(response.generated_images):
        path = output_path
        if num_images > 1:
            base, ext = os.path.splitext(output_path)
            path = f"{base}_{i}{ext}"
        # Write raw image bytes directly to file
        with open(path, "wb") as f:
            f.write(image.image.image_bytes)
        result["images"].append({"path": path})
    return result


def main():
    parser = argparse.ArgumentParser(description="Gemini Image Generation")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model ID (default: {DEFAULT_MODEL})")
    parser.add_argument("--output", default="generated_image.png", help="Output file path")
    parser.add_argument("--num-images", type=int, default=1, help="Number of images (Imagen only)")
    args = parser.parse_args()

    client = genai.Client()

    if args.model in IMAGEN_MODELS:
        result = generate_with_imagen(client, args.prompt, args.model, args.output, args.num_images)
    else:
        result = generate_with_gemini_native(client, args.prompt, args.model, args.output)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
