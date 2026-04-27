#!/usr/bin/env python3
import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
QUICK = SCRIPT_DIR / "gemini_quick.py"
MEDIA = SCRIPT_DIR / "gemini_media.py"


def run_task(task: dict) -> dict:
    task_type = task.get("type", "quick")
    if task_type == "quick":
        command = [
            "python3",
            str(QUICK),
            "--alias",
            task.get("alias", "gemini-3.1-pro-preview"),
            "--prompt",
            task["prompt"],
            "--thinking",
            task.get("thinking", "high"),
        ]
        if task.get("system"):
            command += ["--system", task["system"]]
        if task.get("json"):
            command.append("--json")
    elif task_type == "media":
        command = [
            "python3",
            str(MEDIA),
            "--mode",
            task["mode"],
            "--prompt",
            task["prompt"],
            "--provider",
            task.get("provider", "auto"),
        ]
        if task.get("alias"):
            command += ["--alias", task["alias"]]
        if task.get("count"):
            command += ["--count", str(task["count"])]
        if task.get("aspect_ratio"):
            command += ["--aspect-ratio", task["aspect_ratio"]]
        if task.get("duration_seconds"):
            command += ["--duration-seconds", str(task["duration_seconds"])]
        if task.get("image_url"):
            command += ["--image-url", task["image_url"]]
        if task.get("first_frame_url"):
            command += ["--first-frame-url", task["first_frame_url"]]
        if task.get("last_frame_url"):
            command += ["--last-frame-url", task["last_frame_url"]]
        if task.get("reference_image_urls"):
            command += ["--reference-image-urls", *task["reference_image_urls"]]
        if task.get("orchestrate"):
            command.append("--orchestrate")
        if task.get("poll"):
            command.append("--poll")
    else:
        raise ValueError(f"Unsupported task type: {task_type}")

    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    return {
        "task": task,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Gemini tasks in batches with capped concurrency.")
    parser.add_argument("--tasks", required=True, help="Path to a JSON array of task objects.")
    parser.add_argument("--max-concurrent", type=int, default=5, help="Concurrent task cap.")
    parser.add_argument("--output", help="Optional JSON output path.")
    args = parser.parse_args()

    tasks = json.loads(Path(args.tasks).read_text(encoding="utf-8"))
    results = []
    with ThreadPoolExecutor(max_workers=args.max_concurrent) as pool:
        futures = {pool.submit(run_task, task): task for task in tasks}
        for future in as_completed(futures):
            results.append(future.result())

    text = json.dumps(results, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
