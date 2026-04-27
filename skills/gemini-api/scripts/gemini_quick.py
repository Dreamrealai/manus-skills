#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

from google import genai
from google.genai import types

CATALOG_PATH = Path(__file__).with_name("model_catalog.json")


def load_catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def list_aliases() -> None:
    catalog = load_catalog()
    rows = []
    for alias, meta in sorted(catalog["models"].items()):
        rows.append(
            {
                "alias": alias,
                "api_model": meta.get("api_model"),
                "provider": meta.get("provider"),
                "tasks": ",".join(meta.get("task_types", [])),
                "refresh_required": meta.get("refresh_required", False),
            }
        )
    print(json.dumps(rows, indent=2, ensure_ascii=False))


def resolve_alias(alias: str) -> tuple[str, dict]:
    catalog = load_catalog()
    models = catalog["models"]
    if alias in models:
        meta = models[alias]
        return meta["api_model"], meta
    raise SystemExit(f"Unknown Gemini alias: {alias}. Run --list-aliases first.")


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        return args.prompt
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8")
    if args.stdin:
        return sys.stdin.read()
    raise SystemExit("Provide --prompt, --prompt-file, or --stdin.")


def build_contents(system_text: str | None, user_prompt: str) -> str:
    if not system_text:
        return user_prompt
    return f"System instructions:\n{system_text}\n\nUser request:\n{user_prompt}"


def make_config(args: argparse.Namespace) -> types.GenerateContentConfig:
    kwargs = {}
    if args.temperature is not None:
        kwargs["temperature"] = args.temperature
    if args.max_output_tokens is not None:
        kwargs["max_output_tokens"] = args.max_output_tokens
    if args.thinking:
        kwargs["thinking_config"] = types.ThinkingConfig(thinking_level=args.thinking)
    if args.json:
        kwargs["response_mime_type"] = "application/json"
    return types.GenerateContentConfig(**kwargs)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fast Gemini helper for chat, analysis, and structured output.")
    parser.add_argument("--alias", default="gemini-3.1-pro-preview", help="Catalog alias to use.")
    parser.add_argument("--prompt", help="Prompt text.")
    parser.add_argument("--prompt-file", help="Path to a prompt file.")
    parser.add_argument("--stdin", action="store_true", help="Read the prompt from stdin.")
    parser.add_argument("--system", help="Optional system instructions.")
    parser.add_argument("--temperature", type=float, default=0.2, help="Sampling temperature.")
    parser.add_argument("--max-output-tokens", type=int, help="Optional output token cap.")
    parser.add_argument("--thinking", choices=["minimal", "low", "medium", "high"], default="high")
    parser.add_argument("--json", action="store_true", help="Request JSON-shaped output.")
    parser.add_argument("--output", help="Write the response text to a file.")
    parser.add_argument("--meta-output", help="Write response metadata JSON to a file.")
    parser.add_argument("--list-aliases", action="store_true", help="List the catalog aliases and exit.")
    args = parser.parse_args()

    if args.list_aliases:
        list_aliases()
        return

    model_name, meta = resolve_alias(args.alias)
    prompt = read_prompt(args)
    contents = build_contents(args.system, prompt)
    client = genai.Client()
    response = client.models.generate_content(
        model=model_name,
        contents=contents,
        config=make_config(args),
    )
    text = getattr(response, "text", None) or ""
    result = {
        "alias": args.alias,
        "api_model": model_name,
        "provider": meta.get("provider"),
        "refresh_required": meta.get("refresh_required", False),
        "text": text,
    }

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)

    if args.meta_output:
        Path(args.meta_output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
