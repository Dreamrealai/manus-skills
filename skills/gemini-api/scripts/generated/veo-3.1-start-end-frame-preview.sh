#!/usr/bin/env bash
set -euo pipefail
python3 "/home/ubuntu/skills/gemini-api/scripts/gemini_media.py" --mode "video" --alias "veo-3.1-start-end-frame-preview" "$@"
