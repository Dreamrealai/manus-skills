#!/usr/bin/env bash
set -euo pipefail
python3 "/home/ubuntu/skills/gemini-api/scripts/gemini_media.py" --mode "music" --alias "lyria-3-clip" "$@"
