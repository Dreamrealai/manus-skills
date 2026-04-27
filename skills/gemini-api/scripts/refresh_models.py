#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import re
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
CATALOG_PATH = SCRIPT_DIR / "model_catalog.json"
WRAPPER_DIR = SCRIPT_DIR / "generated"
SOURCES = {
    "google_models_doc": "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models",
    "google_monthly_ai": "https://cloud.google.com/blog/products/ai-machine-learning/what-google-cloud-announced-in-ai-this-month",
    "recent_releases": "https://pricepertoken.com/news/model-releases",
}
PATTERNS = {
    "gemini-3.1-pro-preview": r"Gemini\s*3\.1\s*Pro",
    "gemini-3.0-flash-preview": r"Gemini\s*3(?:\.0)?\s*Flash",
    "gemini-3.1-flash-lite": r"Gemini\s*3\.1\s*Flash[- ]Lite",
    "gemini-3.1-flash-live": r"Gemini\s*3\.1\s*Flash\s*Live",
    "deep-research": r"deep\s*research",
    "gemma-4": r"Gemma\s*4",
    "gemini-3.1-flash-image-preview": r"Gemini\s*3\.1\s*Flash\s*Image",
    "gemini-2.5-pro-tts": r"Gemini\s*2\.5\s*Pro.*TTS|text[- ]to[- ]speech",
    "veo-3.1-image-to-video": r"Veo\s*3\.1",
    "veo-3.1-reference-to-video": r"Veo\s*3\.1",
    "veo-3.1-text-to-video": r"Veo\s*3\.1",
    "veo-3.1-start-end-frame-preview": r"Veo\s*3\.1|start[- ]frame|end[- ]frame",
    "lyria-3-clip": r"Lyria\s*3",
    "lyria-3-preview": r"Lyria\s*3",
}


def fetch_text(url: str) -> str:
    response = requests.get(url, timeout=60, headers={"User-Agent": "Manus Skill Refresh"})
    response.raise_for_status()
    return response.text


def generate_wrappers(catalog: dict) -> list[str]:
    WRAPPER_DIR.mkdir(parents=True, exist_ok=True)
    created = []
    for alias, meta in sorted(catalog["models"].items()):
        script_path = WRAPPER_DIR / f"{alias}.sh"
        if any(task in meta.get("task_types", []) for task in ["image", "video", "music", "audio", "tts"]):
            if "tts" in meta.get("task_types", []):
                body = (
                    "#!/usr/bin/env bash\n"
                    "set -euo pipefail\n"
                    f'python3 "{SCRIPT_DIR / "gemini_quick.py"}" --alias "{alias}" "$@"\n'
                )
            else:
                mode = "image"
                if "video" in meta.get("task_types", []):
                    mode = "video"
                elif "music" in meta.get("task_types", []) or "audio" in meta.get("task_types", []):
                    mode = "music"
                body = (
                    "#!/usr/bin/env bash\n"
                    "set -euo pipefail\n"
                    f'python3 "{SCRIPT_DIR / "gemini_media.py"}" --mode "{mode}" --alias "{alias}" "$@"\n'
                )
        else:
            body = (
                "#!/usr/bin/env bash\n"
                "set -euo pipefail\n"
                f'python3 "{SCRIPT_DIR / "gemini_quick.py"}" --alias "{alias}" "$@"\n'
            )
        script_path.write_text(body, encoding="utf-8")
        script_path.chmod(0o755)
        created.append(str(script_path))
    return created


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh the Gemini helper registry using current public sources.")
    parser.add_argument("--provider", default="gemini")
    parser.add_argument("--write-catalog", action="store_true")
    parser.add_argument("--generate-wrappers", action="store_true")
    parser.add_argument("--report", help="Optional JSON report path.")
    args = parser.parse_args()

    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    report = {
        "provider": args.provider,
        "refreshed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
        "sources": {},
        "matches": {},
        "recommendations": [],
        "wrappers": [],
    }

    combined_text = []
    for name, url in SOURCES.items():
        try:
            text = fetch_text(url)
            report["sources"][name] = {"url": url, "status": "ok", "length": len(text)}
            combined_text.append(text)
        except Exception as exc:
            report["sources"][name] = {"url": url, "status": "error", "error": str(exc)}

    merged = "\n".join(combined_text)
    for alias, pattern in PATTERNS.items():
        report["matches"][alias] = bool(re.search(pattern, merged, flags=re.IGNORECASE))
        if alias in catalog["models"] and not report["matches"][alias]:
            report["recommendations"].append(f"Verify alias '{alias}' before production use; source match was not found in the refresh scan.")

    catalog["last_refreshed_utc"] = report["refreshed_at_utc"]
    catalog["last_refresh_report"] = report
    if args.write_catalog:
        CATALOG_PATH.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.generate_wrappers:
        report["wrappers"] = generate_wrappers(catalog)

    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.report:
        Path(args.report).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
