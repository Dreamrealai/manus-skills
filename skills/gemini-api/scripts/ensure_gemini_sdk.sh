#!/usr/bin/env bash
set -euo pipefail

if python3.11 - <<'PY' >/dev/null 2>&1
from google import genai
print(genai.__name__)
PY
then
  echo "Gemini SDK already available"
else
  echo "Installing Gemini SDK (google-genai)..."
  sudo uv pip install --system -U google-genai
  python3.11 - <<'PY' >/dev/null
from google import genai
print(genai.__name__)
PY
  echo "Gemini SDK installed successfully"
fi
