#!/usr/bin/env python3
"""Gemini Chat & Analysis Script.

Performs text/document analysis using Gemini 3.1 Pro with structured JSON output.
Supports text prompts, image analysis, and document analysis.

Usage:
    python chat_analysis.py --prompt "Your question" [--images img1.jpg img2.jpg] [--model MODEL] [--thinking LEVEL] [--schema SCHEMA_JSON]
"""
import argparse
import base64
import json
import mimetypes
import os
import sys

from google import genai
from google.genai import types


DEFAULT_MODEL = "gemini-3.1-pro-preview"
DEFAULT_THINKING = "high"


def build_schema(schema_json: str | None) -> dict | None:
    """Parse a JSON schema string into a dict for structured output."""
    if not schema_json:
        return None
    return json.loads(schema_json)


def load_image_part(path: str) -> types.Part:
    """Load an image file as an inline Part."""
    mime, _ = mimetypes.guess_type(path)
    mime = mime or "image/jpeg"
    with open(path, "rb") as f:
        data = f.read()
    return types.Part(inline_data=types.Blob(data=data, mime_type=mime))


def run_analysis(
    prompt: str,
    image_paths: list[str] | None = None,
    model: str = DEFAULT_MODEL,
    thinking_level: str = DEFAULT_THINKING,
    response_schema: dict | None = None,
) -> dict:
    """Execute a single analysis request and return the result."""
    client = genai.Client()

    parts: list[types.Part] = []
    if image_paths:
        for p in image_paths:
            parts.append(load_image_part(p))
    parts.append(types.Part(text=prompt))

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

    result = {"model": model, "thinking_level": thinking_level}
    if response_schema:
        try:
            result["structured_output"] = json.loads(response.text)
        except json.JSONDecodeError:
            result["raw_text"] = response.text
    else:
        result["text"] = response.text
    return result


def main():
    parser = argparse.ArgumentParser(description="Gemini Chat & Analysis")
    parser.add_argument("--prompt", required=True, help="The analysis prompt")
    parser.add_argument("--images", nargs="*", help="Image file paths to analyze")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model ID (default: {DEFAULT_MODEL})")
    parser.add_argument("--thinking", default=DEFAULT_THINKING, choices=["minimal", "low", "medium", "high"], help="Thinking level")
    parser.add_argument("--schema", default=None, help="JSON schema string for structured output")
    parser.add_argument("--output", default=None, help="Output JSON file path")
    args = parser.parse_args()

    schema = build_schema(args.schema)
    result = run_analysis(
        prompt=args.prompt,
        image_paths=args.images,
        model=args.model,
        thinking_level=args.thinking,
        response_schema=schema,
    )

    output_json = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output_json)
        print(f"Result saved to {args.output}")
    else:
        print(output_json)


if __name__ == "__main__":
    main()
