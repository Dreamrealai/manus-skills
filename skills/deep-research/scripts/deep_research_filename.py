#!/usr/bin/env python3
"""Generate standardized filenames for deep-research raw outputs.

Pattern:
    YYMMDD_Project_Topic_Source_HHMM.ext

Rules:
- Timezone is always America/New_York.
- Source is normalized to a human-readable canonical form.
- Combined Project + Topic segment is capped at 38 characters to keep
  filenames compact and roughly aligned with the requested example length.
- If project is unknown, only Topic is used.
- If an output directory is supplied and a collision is detected, seconds are
  appended after HHMM to preserve uniqueness.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
MAX_COMBINED_LENGTH = 38
SOURCE_MAP = {
    "manus": "Manus",
    "gemini": "Gemini",
    "chatgpt": "ChatGPT",
    "chatgptdeepresearch": "ChatGPT",
    "gpt": "ChatGPT",
    "final": "Final",
    "tracker": "Tracker",
    "reminder": "Reminder",
}


def normalize_words(text: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", text)
    if not words:
        return "Research"
    return "".join(word[:1].upper() + word[1:] for word in words)


def normalize_source(source: str) -> str:
    key = re.sub(r"[^A-Za-z0-9]+", "", source).lower()
    return SOURCE_MAP.get(key, normalize_words(source))


def trim_project_topic(project: str, topic: str) -> tuple[str, str, bool]:
    project_clean = normalize_words(project) if project else ""
    topic_clean = normalize_words(topic)
    truncated = False

    if not project_clean:
        trimmed_topic = topic_clean[:MAX_COMBINED_LENGTH] or "Research"
        truncated = trimmed_topic != topic_clean
        return "", trimmed_topic, truncated

    joined = f"{project_clean}_{topic_clean}"
    if len(joined) <= MAX_COMBINED_LENGTH:
        return project_clean, topic_clean, truncated

    project_limit = min(len(project_clean), 14)
    remaining = max(12, MAX_COMBINED_LENGTH - project_limit - 1)
    trimmed_project = project_clean[:project_limit]
    trimmed_topic = topic_clean[:remaining]
    truncated = trimmed_project != project_clean or trimmed_topic != topic_clean
    return trimmed_project, trimmed_topic, truncated


def build_filename(project: str, topic: str, source: str, ext: str, output_dir: str = "") -> tuple[str, bool, bool]:
    now = datetime.now(ET)
    date_part = now.strftime("%y%m%d")
    time_part = now.strftime("%H%M")
    seconds_part = now.strftime("%S")
    project_part, topic_part, truncated = trim_project_topic(project, topic)
    source_part = normalize_source(source)
    ext = ext.lstrip(".") or "md"

    if project_part:
        base_name = f"{date_part}_{project_part}_{topic_part}_{source_part}_{time_part}"
    else:
        base_name = f"{date_part}_{topic_part}_{source_part}_{time_part}"

    filename = f"{base_name}.{ext}"
    collision_avoided = False
    if output_dir:
        output_path = Path(output_dir)
        if (output_path / filename).exists():
            filename = f"{base_name}{seconds_part}.{ext}"
            collision_avoided = True

    return filename, truncated, collision_avoided


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a standardized deep-research filename using Eastern time and compact human-readable segments."
    )
    parser.add_argument("--topic", required=True, help="Short topic description")
    parser.add_argument("--project", default="", help="Project or client name if known")
    parser.add_argument("--source", required=True, help="Origin source such as Manus, Gemini, ChatGPT, Final, Tracker, or Reminder")
    parser.add_argument("--ext", default="md", help="File extension without dot (default: md)")
    parser.add_argument("--output-dir", default="", help="Optional output directory used for same-minute collision detection")
    args = parser.parse_args()

    filename, truncated, collision_avoided = build_filename(
        args.project,
        args.topic,
        args.source,
        args.ext,
        args.output_dir,
    )
    if truncated:
        print("Note: project/topic label was truncated to keep the filename compact.", file=sys.stderr)
    if collision_avoided:
        print("Note: same-minute collision detected; appended seconds for uniqueness.", file=sys.stderr)
    print(filename)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
