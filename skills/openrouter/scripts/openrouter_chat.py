#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path

import time

import requests

CATALOG_PATH = Path(__file__).with_name("model_catalog.json")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


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
                "reasoning": meta.get("reasoning"),
                "refresh_required": meta.get("refresh_required", False),
            }
        )
    print(json.dumps(rows, indent=2, ensure_ascii=False))


def resolve_alias(alias: str) -> tuple[str, dict]:
    catalog = load_catalog()
    meta = catalog["models"].get(alias)
    if meta:
        return meta["api_model"], meta
    if "/" in alias:
        return alias, {"provider": "openrouter", "api_model": alias, "reasoning": "medium", "refresh_required": False}
    raise SystemExit(f"Unknown alias: {alias}. Run --list-aliases first.")


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        return args.prompt
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8")
    if args.stdin:
        return sys.stdin.read()
    raise SystemExit("Provide --prompt, --prompt-file, or --stdin.")


def build_messages(system_text: str | None, prompt: str) -> list[dict]:
    messages = []
    if system_text:
        messages.append({"role": "system", "content": system_text})
    messages.append({"role": "user", "content": prompt})
    return messages


def normalize_reasoning(reasoning: str | None, meta: dict) -> str | None:
    if reasoning:
        return reasoning
    return meta.get("reasoning")


def call_gemini(meta: dict, prompt: str, system_text: str | None, reasoning: str | None, json_mode: bool, temperature: float) -> dict:
    from google import genai
    from google.genai import types

    client = genai.Client()
    contents = prompt if not system_text else f"System instructions:\n{system_text}\n\nUser request:\n{prompt}"
    kwargs = {"temperature": temperature}
    if reasoning and reasoning != "off":
        kwargs["thinking_config"] = types.ThinkingConfig(thinking_level=reasoning)
    if json_mode:
        kwargs["response_mime_type"] = "application/json"
    response = client.models.generate_content(
        model=meta.get("gemini_api_model") or meta["api_model"],
        contents=contents,
        config=types.GenerateContentConfig(**kwargs),
    )
    return {
        "provider": "gemini",
        "api_model": meta.get("gemini_api_model") or meta["api_model"],
        "text": getattr(response, "text", "") or "",
    }


def call_openrouter(model: str, messages: list[dict], reasoning: str | None, temperature: float, max_tokens: int | None, json_mode: bool) -> dict:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY is not set.")

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    if reasoning and reasoning != "off":
        payload["reasoning"] = {"effort": reasoning}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://manus.im",
        "X-Title": "Manus OpenRouter Skill",
    }
    last_error = None
    for attempt in range(1, 4):
        try:
            response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=300)
            response.raise_for_status()
            data = response.json()
            text = data["choices"][0]["message"]["content"]
            return {"provider": "openrouter", "api_model": model, "text": text, "raw": data}
        except requests.RequestException as exc:
            last_error = exc
            if attempt == 3:
                raise
            time.sleep(attempt * 2)
    raise last_error



def main() -> None:
    parser = argparse.ArgumentParser(description="Catalog-driven OpenRouter helper with Gemini-first routing for Gemini-family aliases.")
    parser.add_argument("--alias", default="opus-4.7", help="Catalog alias or full OpenRouter model ID.")
    parser.add_argument("--provider", choices=["auto", "openrouter", "gemini"], default="auto")
    parser.add_argument("--prompt", help="Prompt text.")
    parser.add_argument("--prompt-file", help="Path to a prompt file.")
    parser.add_argument("--stdin", action="store_true", help="Read the prompt from stdin.")
    parser.add_argument("--system", help="Optional system instructions.")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int)
    parser.add_argument("--reasoning", choices=["off", "minimal", "low", "medium", "high", "xhigh"])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output", help="Write the text response to a file.")
    parser.add_argument("--meta-output", help="Write the metadata JSON to a file.")
    parser.add_argument("--list-aliases", action="store_true")
    args = parser.parse_args()

    if args.list_aliases:
        list_aliases()
        return

    model, meta = resolve_alias(args.alias)
    prompt = read_prompt(args)
    reasoning = normalize_reasoning(args.reasoning, meta)

    if args.provider == "gemini" or (args.provider == "auto" and meta.get("provider") == "gemini_first"):
        result = call_gemini(meta, prompt, args.system, reasoning, args.json, args.temperature)
    else:
        result = call_openrouter(model, build_messages(args.system, prompt), reasoning, args.temperature, args.max_tokens, args.json)

    text = result.get("text", "")
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)

    if args.meta_output:
        payload = {
            "alias": args.alias,
            "requested_provider": args.provider,
            "resolved_provider": result.get("provider"),
            "api_model": result.get("api_model"),
            "refresh_required": meta.get("refresh_required", False),
            "reasoning": reasoning,
        }
        Path(args.meta_output).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
