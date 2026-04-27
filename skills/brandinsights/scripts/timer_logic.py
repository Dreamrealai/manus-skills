#!/usr/bin/env python3
"""
brandinsights/scripts/timer_logic.py

Manages the mandatory timers for the brandinsights skill:
  - 1-hour minimum social mining timer
  - 2-hour overall skill runtime ceiling

Usage:
  python3 timer_logic.py start --phase social_mining --tracker tracker.md
  python3 timer_logic.py check --phase social_mining --tracker tracker.md
  python3 timer_logic.py close --phase social_mining --tracker tracker.md
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

PHASES = {
    "social_mining": {"min_seconds": 3600, "label": "Social Mining (1-hour minimum)"},
    "overall": {"min_seconds": 7200, "label": "Overall Skill Runtime (2-hour ceiling)"},
    "chatgpt_deep_research": {"min_seconds": 3600, "label": "ChatGPT Deep Research (60-min ceiling)"},
}


def _load_state(tracker_path: str) -> dict:
    if os.path.exists(tracker_path):
        with open(tracker_path) as f:
            return json.load(f)
    return {}


def _save_state(tracker_path: str, state: dict) -> None:
    with open(tracker_path, "w") as f:
        json.dump(state, f, indent=2)


def _now_ts() -> float:
    return time.time()


def _fmt(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def cmd_start(phase: str, tracker_path: str) -> None:
    state = _load_state(tracker_path)
    if phase in state and state[phase].get("status") == "running":
        print(f"[timer] Phase '{phase}' already running since {_fmt(state[phase]['start_ts'])}.")
        return
    state[phase] = {
        "status": "running",
        "start_ts": _now_ts(),
        "checks": [],
    }
    _save_state(tracker_path, state)
    print(f"[timer] Started '{PHASES[phase]['label']}' at {_fmt(state[phase]['start_ts'])}.")


def cmd_check(phase: str, tracker_path: str) -> None:
    state = _load_state(tracker_path)
    if phase not in state:
        print(f"[timer] ERROR: Phase '{phase}' not started. Run 'start' first.")
        sys.exit(1)
    entry = state[phase]
    elapsed = _now_ts() - entry["start_ts"]
    min_required = PHASES[phase]["min_seconds"]
    pct = min(100, int(elapsed / min_required * 100))
    remaining = max(0, min_required - elapsed)
    entry["checks"].append({"ts": _now_ts(), "elapsed_s": elapsed})
    _save_state(tracker_path, state)
    print(
        f"[timer] '{PHASES[phase]['label']}' — "
        f"Elapsed: {elapsed/60:.1f} min | "
        f"Required: {min_required/60:.0f} min | "
        f"Progress: {pct}% | "
        f"Remaining: {remaining/60:.1f} min"
    )
    if elapsed < min_required:
        print(f"[timer] ⚠️  MINIMUM NOT MET. Continue until {remaining/60:.1f} more minutes have passed.")
    else:
        print(f"[timer] ✅ Minimum duration satisfied. You may proceed.")


def cmd_close(phase: str, tracker_path: str) -> None:
    state = _load_state(tracker_path)
    if phase not in state:
        print(f"[timer] ERROR: Phase '{phase}' not started.")
        sys.exit(1)
    entry = state[phase]
    elapsed = _now_ts() - entry["start_ts"]
    min_required = PHASES[phase]["min_seconds"]
    if elapsed < min_required:
        print(
            f"[timer] ❌ CANNOT CLOSE: Only {elapsed/60:.1f} min elapsed. "
            f"Minimum is {min_required/60:.0f} min. Continue working."
        )
        sys.exit(1)
    entry["status"] = "closed"
    entry["end_ts"] = _now_ts()
    entry["total_elapsed_s"] = elapsed
    _save_state(tracker_path, state)
    print(f"[timer] ✅ Phase '{PHASES[phase]['label']}' closed after {elapsed/60:.1f} minutes.")


def main() -> None:
    parser = argparse.ArgumentParser(description="brandinsights timer manager")
    parser.add_argument("command", choices=["start", "check", "close"])
    parser.add_argument("--phase", required=True, choices=list(PHASES.keys()))
    parser.add_argument("--tracker", required=True, help="Path to tracker JSON file")
    args = parser.parse_args()

    if args.command == "start":
        cmd_start(args.phase, args.tracker)
    elif args.command == "check":
        cmd_check(args.phase, args.tracker)
    elif args.command == "close":
        cmd_close(args.phase, args.tracker)


if __name__ == "__main__":
    main()
