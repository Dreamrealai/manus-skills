#!/usr/bin/env bash
set -euo pipefail
python3 "/home/ubuntu/skills/gemini-api/scripts/gemini_media.py" --mode "image" --alias "gemini-3.1-flash-image-preview" "$@"
