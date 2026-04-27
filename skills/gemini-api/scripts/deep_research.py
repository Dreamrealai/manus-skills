#!/usr/bin/env python3
"""Gemini Deep Research Script.

Performs autonomous multi-step research using the Gemini Deep Research Agent
via the Interactions API. Supports polling and streaming modes, multimodal
inputs (images, PDFs, audio, video), follow-up questions, and optional
File Search integration.

The agent is powered by Gemini 3.1 Pro and uses google_search + url_context
by default. Research tasks run in the background and can take several minutes.

Agent: deep-research-pro-preview-12-2025

Usage:
    # Basic research (polling mode)
    python deep_research.py --prompt "Research the history of quantum computing"

    # Streaming with thinking summaries
    python deep_research.py --prompt "Compare EV battery technologies" --stream

    # With local file input (uploaded via Files API)
    python deep_research.py --prompt "Identify and research this architecture" --files photo.jpg

    # With image URL
    python deep_research.py --prompt "Research the species in this image" --image-urls "https://example.com/photo.jpg"

    # With File Search (your own data)
    python deep_research.py --prompt "Summarize our Q4 report" --file-search-store "fileSearchStores/my-store"

    # Follow-up on a previous interaction (runs new research with context)
    python deep_research.py --prompt "Elaborate on the second point" --follow-up INTERACTION_ID

    # Quick follow-up chat (no new research, synchronous)
    python deep_research.py --prompt "Summarize in 3 bullets" --follow-up INTERACTION_ID --quick

    # Custom output file
    python deep_research.py --prompt "Research topic" --output report.md

    # Set custom poll interval and timeout
    python deep_research.py --prompt "Research topic" --poll-interval 15 --timeout 3600
"""
import argparse
import json
import mimetypes
import os
import sys
import time

from google import genai


DEFAULT_AGENT = "deep-research-pro-preview-12-2025"
DEFAULT_FOLLOW_UP_MODEL = "gemini-3.1-pro-preview"
DEFAULT_POLL_INTERVAL = 10  # seconds
DEFAULT_TIMEOUT = 3600  # 60 minutes max


def upload_file(client: genai.Client, path: str) -> str:
    """Upload a local file via the Files API and return its URI."""
    mime, _ = mimetypes.guess_type(path)
    mime = mime or "application/octet-stream"
    print(f"  Uploading {path} ({mime})...", file=sys.stderr)
    uploaded = client.files.upload(file=path, config={"mime_type": mime})
    print(f"  Uploaded as {uploaded.uri}", file=sys.stderr)
    return uploaded.uri


def build_multimodal_input(client: genai.Client, prompt: str,
                           file_paths: list[str] | None = None,
                           image_urls: list[str] | None = None) -> list | str:
    """Build a multimodal input list. Local files are uploaded via the Files API
    to obtain URIs (preferred by the Interactions API over base64)."""
    if not file_paths and not image_urls:
        return prompt

    parts = [{"type": "text", "text": prompt}]

    if file_paths:
        for path in file_paths:
            uri = upload_file(client, path)
            mime, _ = mimetypes.guess_type(path)
            mime = mime or "application/octet-stream"
            if mime.startswith("image"):
                parts.append({"type": "image", "uri": uri})
            elif mime.startswith("video"):
                parts.append({"type": "video", "uri": uri})
            elif mime.startswith("audio"):
                parts.append({"type": "audio", "uri": uri})
            else:
                # PDFs and other documents
                parts.append({"type": "file", "uri": uri})

    if image_urls:
        for url in image_urls:
            parts.append({"type": "image", "uri": url})

    return parts


def build_tools(file_search_store: str | None = None) -> list | None:
    """Build the tools list if File Search is requested."""
    if not file_search_store:
        return None
    return [
        {
            "type": "file_search",
            "file_search_store_names": [file_search_store],
        }
    ]


def run_polling(client: genai.Client, create_kwargs: dict,
                poll_interval: int, timeout: int) -> dict:
    """Run deep research in polling mode and return the result."""
    interaction = client.interactions.create(**create_kwargs)
    interaction_id = interaction.id
    print(f"Research started: {interaction_id}", file=sys.stderr)

    elapsed = 0
    while elapsed < timeout:
        interaction = client.interactions.get(interaction_id)
        status = interaction.status

        if status == "completed":
            print(f"Research completed in ~{elapsed}s", file=sys.stderr)
            report_text = interaction.outputs[-1].text if interaction.outputs else ""
            return {
                "status": "completed",
                "interaction_id": interaction_id,
                "report": report_text,
            }
        elif status == "failed":
            error_msg = getattr(interaction, "error", "Unknown error")
            return {
                "status": "failed",
                "interaction_id": interaction_id,
                "error": str(error_msg),
            }

        print(f"  Status: {status} ({elapsed}s elapsed)...", file=sys.stderr)
        time.sleep(poll_interval)
        elapsed += poll_interval

    return {
        "status": "timeout",
        "interaction_id": interaction_id,
        "error": f"Research did not complete within {timeout}s. You can resume polling with the interaction_id.",
    }


def run_streaming(client: genai.Client, create_kwargs: dict,
                  timeout: int) -> dict:
    """Run deep research in streaming mode with thinking summaries."""
    create_kwargs["stream"] = True
    create_kwargs["agent_config"] = {
        "type": "deep-research",
        "thinking_summaries": "auto",
    }

    interaction_id = None
    last_event_id = None
    report = ""
    is_complete = False

    def process_stream(event_stream):
        nonlocal interaction_id, last_event_id, report, is_complete
        for event in event_stream:
            if event.event_type == "interaction.start":
                interaction_id = event.interaction.id
                print(f"Interaction started: {interaction_id}", file=sys.stderr)

            if event.event_id:
                last_event_id = event.event_id

            if event.event_type == "content.delta":
                if event.delta.type == "text":
                    report += event.delta.text
                elif event.delta.type == "thought_summary":
                    print(f"  [Thought] {event.delta.content.text}", file=sys.stderr)

            if event.event_type in ("interaction.complete", "error"):
                is_complete = True
                if event.event_type == "error":
                    print(f"  [Error] Stream error encountered", file=sys.stderr)

    # Initial stream attempt
    try:
        print("Starting research (streaming)...", file=sys.stderr)
        initial_stream = client.interactions.create(**create_kwargs)
        process_stream(initial_stream)
    except Exception as e:
        print(f"  Connection dropped: {e}", file=sys.stderr)

    # Reconnection loop
    max_retries = 10
    retries = 0
    while not is_complete and interaction_id and retries < max_retries:
        print(f"  Reconnecting from event {last_event_id}...", file=sys.stderr)
        time.sleep(2)
        retries += 1
        try:
            get_kwargs = {"id": interaction_id, "stream": True}
            if last_event_id:
                get_kwargs["last_event_id"] = last_event_id
            resume_stream = client.interactions.get(**get_kwargs)
            process_stream(resume_stream)
        except Exception as e:
            print(f"  Reconnection failed ({e}), retrying...", file=sys.stderr)

    if is_complete:
        return {
            "status": "completed",
            "interaction_id": interaction_id,
            "report": report,
        }
    else:
        return {
            "status": "incomplete",
            "interaction_id": interaction_id,
            "report": report,
            "error": "Stream ended without completion. Partial report returned.",
        }


def run_quick_follow_up(client: genai.Client, prompt: str,
                        previous_interaction_id: str, model: str) -> dict:
    """Send a quick synchronous follow-up (no new research) to a completed interaction."""
    interaction = client.interactions.create(
        input=prompt,
        model=model,
        previous_interaction_id=previous_interaction_id,
    )
    return {
        "status": "completed",
        "interaction_id": interaction.id,
        "previous_interaction_id": previous_interaction_id,
        "report": interaction.outputs[-1].text if interaction.outputs else "",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Gemini Deep Research Agent — autonomous multi-step research via the Interactions API"
    )
    parser.add_argument("--prompt", required=True, help="The research prompt or follow-up question")
    parser.add_argument("--agent", default=DEFAULT_AGENT, help=f"Agent ID (default: {DEFAULT_AGENT})")
    parser.add_argument("--stream", action="store_true", help="Use streaming mode with thinking summaries")
    parser.add_argument("--files", nargs="*", help="Local file paths (images, PDFs, audio, video) — uploaded via Files API")
    parser.add_argument("--image-urls", nargs="*", help="Image URLs for multimodal input")
    parser.add_argument("--file-search-store", default=None, help="File Search store name (e.g. fileSearchStores/my-store)")
    parser.add_argument("--follow-up", default=None, metavar="INTERACTION_ID",
                        help="Continue research from a completed interaction (runs new deep research with context)")
    parser.add_argument("--quick", action="store_true",
                        help="With --follow-up: send a quick synchronous chat instead of new research")
    parser.add_argument("--follow-up-model", default=DEFAULT_FOLLOW_UP_MODEL,
                        help=f"Model for quick follow-ups (default: {DEFAULT_FOLLOW_UP_MODEL})")
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL,
                        help=f"Seconds between polls (default: {DEFAULT_POLL_INTERVAL})")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help=f"Max seconds to wait (default: {DEFAULT_TIMEOUT})")
    parser.add_argument("--output", default=None, help="Output file path (.md for report, .json for full result)")
    args = parser.parse_args()

    client = genai.Client()

    # Quick follow-up mode (synchronous, no new research)
    if args.follow_up and args.quick:
        print(f"Sending quick follow-up to interaction {args.follow_up}...", file=sys.stderr)
        result = run_quick_follow_up(client, args.prompt, args.follow_up, args.follow_up_model)
    else:
        # Build inputs
        input_data = build_multimodal_input(client, args.prompt, args.files, args.image_urls)
        tools = build_tools(args.file_search_store)

        # Build shared create kwargs
        create_kwargs = {
            "input": input_data,
            "agent": args.agent,
            "background": True,
        }
        if tools:
            create_kwargs["tools"] = tools
        if args.follow_up:
            create_kwargs["previous_interaction_id"] = args.follow_up
            print(f"Continuing research from interaction {args.follow_up}...", file=sys.stderr)

        # Run research
        if args.stream:
            result = run_streaming(client, create_kwargs, args.timeout)
        else:
            result = run_polling(client, create_kwargs, args.poll_interval, args.timeout)

    # Output
    if args.output:
        if args.output.endswith(".json"):
            with open(args.output, "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Full result saved to {args.output}", file=sys.stderr)
        else:
            with open(args.output, "w") as f:
                f.write(result.get("report", ""))
            print(f"Report saved to {args.output}", file=sys.stderr)
    else:
        # Print report to stdout, metadata to stderr
        print(json.dumps({"status": result["status"], "interaction_id": result.get("interaction_id")},
                         indent=2), file=sys.stderr)
        print(result.get("report", ""))


if __name__ == "__main__":
    main()
