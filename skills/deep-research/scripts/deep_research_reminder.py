#!/usr/bin/env python3
"""Emit reminder messages for mandatory ChatGPT deep-research check-ins.

This sidecar is intended to run in a separate shell session while the main
workflow continues. It watches the tracker JSON and prints a reminder whenever
an Eastern-time check is due, stopping once the tracker is explicitly closed.
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")


def now_et() -> datetime:
    return datetime.now(ET)


def fmt_ts(dt: datetime) -> str:
    return dt.astimezone(ET).strftime("%Y-%m-%d %H:%M:%S %Z")


def load_state(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def emit(message: str, log_file: Path | None) -> None:
    line = f"[{fmt_ts(now_et())}] {message}"
    print(line, flush=True)
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Watch a deep-research tracker JSON file and emit reminders when the next 5-minute ChatGPT check is due."
    )
    parser.add_argument("--state-file", required=True, help="Path to the JSON tracker state file")
    parser.add_argument("--poll-seconds", type=int, default=30, help="Polling interval in seconds (default: 30)")
    parser.add_argument("--log-file", default="", help="Optional log file for reminder messages")
    args = parser.parse_args()

    state_path = Path(args.state_file)
    log_path = Path(args.log_file) if args.log_file else None
    last_due_iso = None
    last_emitted_key = None

    emit(f"Reminder watcher started for {state_path}", log_path)

    while True:
        if not state_path.exists():
            emit("Tracker file not found yet; waiting.", log_path)
            time.sleep(args.poll_seconds)
            continue

        state = load_state(state_path)
        if not state.get("final_check_required", True) or state.get("finished"):
            emit(f"Tracker closed with status '{state.get('status', 'unknown')}'. Reminder watcher exiting.", log_path)
            return 0

        due_iso = state.get("next_check_due_at_et_iso")
        due_text = state.get("next_check_due_at_et")
        thread_url = state.get("thread_url", "")
        status = state.get("status", "running")

        if due_iso:
            due_dt = datetime.fromisoformat(due_iso)
            due_key = f"{due_iso}|{status}"
            if due_iso != last_due_iso:
                emit(f"Next ChatGPT check due at {due_text}. Current tracker status: {status}.", log_path)
                last_due_iso = due_iso
                last_emitted_key = None
            if now_et() >= due_dt and last_emitted_key != due_key:
                message = (
                    f"CHECK NOW: ChatGPT Deep Research is due for review. Tracker status: {status}. "
                    f"Thread: {thread_url or '[missing thread URL]'}"
                )
                emit(message, log_path)
                last_emitted_key = due_key
        else:
            emit("No next due time is currently scheduled; a final close step may be required.", log_path)
            if status in {"completed_pending_close", "failed_pending_close"}:
                emit("Run the explicit close command after the final harvest/check to clear the delivery gate.", log_path)
                return 0

        time.sleep(args.poll_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
