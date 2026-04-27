#!/usr/bin/env python3
"""Track long-running deep-research jobs with mandatory check-ins.

Designed for the deep-research skill so another Manus instance can:
1. Start a tracker as soon as ChatGPT Deep Research is launched.
2. Check status every 5 minutes until completion or 60 minutes elapsed.
3. Allow non-blocking report drafting after 20 minutes while preserving
   mandatory 5-minute monitoring.
4. Force an explicit final closure step so ChatGPT is not silently skipped.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
CHECK_INTERVAL_MINUTES = 5
NON_BLOCKING_AFTER_MINUTES = 20
MAX_RUNTIME_MINUTES = 60
TERMINAL_PENDING_STATUSES = {"completed_pending_close", "failed_pending_close"}


@dataclass
class TrackerSummary:
    elapsed_minutes: int
    next_due_minutes: int
    recommended_action: str
    phase_guidance: str


def now_et() -> datetime:
    return datetime.now(ET)


def fmt_ts(dt: datetime) -> str:
    return dt.astimezone(ET).strftime("%Y-%m-%d %H:%M:%S %Z")


def load_state(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp_path, path)


def compute_next_due(start_time_et: datetime, elapsed_minutes: int, status: str, finished: bool) -> datetime | None:
    if finished or status in TERMINAL_PENDING_STATUSES or elapsed_minutes >= MAX_RUNTIME_MINUTES:
        return None
    due_minutes = ((elapsed_minutes // CHECK_INTERVAL_MINUTES) + 1) * CHECK_INTERVAL_MINUTES
    return start_time_et + timedelta(minutes=due_minutes)


def compute_summary(start_time_et: datetime, finished: bool, status: str) -> TrackerSummary:
    elapsed_seconds = max(0, int((now_et() - start_time_et).total_seconds()))
    elapsed_minutes = elapsed_seconds // 60
    next_due_minutes = ((elapsed_minutes // CHECK_INTERVAL_MINUTES) + 1) * CHECK_INTERVAL_MINUTES

    if finished:
        return TrackerSummary(
            elapsed_minutes=elapsed_minutes,
            next_due_minutes=elapsed_minutes,
            recommended_action="complete",
            phase_guidance="Tracker is already closed. Proceed with the archived outcome recorded in the state file.",
        )

    if status in TERMINAL_PENDING_STATUSES:
        return TrackerSummary(
            elapsed_minutes=elapsed_minutes,
            next_due_minutes=elapsed_minutes,
            recommended_action="close_after_final_check",
            phase_guidance=(
                "The report has already been observed in a terminal state. Perform the final harvest/check now and "
                "run the explicit close step before delivery."
            ),
        )

    if elapsed_minutes < NON_BLOCKING_AFTER_MINUTES:
        return TrackerSummary(
            elapsed_minutes=elapsed_minutes,
            next_due_minutes=next_due_minutes,
            recommended_action="keep_monitoring",
            phase_guidance=(
                "Continue independent research, but return every 5 minutes. "
                "Do not let ChatGPT Deep Research go unchecked."
            ),
        )

    if elapsed_minutes < MAX_RUNTIME_MINUTES:
        final_due = start_time_et + timedelta(minutes=MAX_RUNTIME_MINUTES)
        return TrackerSummary(
            elapsed_minutes=elapsed_minutes,
            next_due_minutes=next_due_minutes,
            recommended_action="build_reports_while_monitoring",
            phase_guidance=(
                "It is acceptable to draft Gemini + Manus synthesis first, but keep checking ChatGPT every 5 minutes. "
                f"The hard stop for the mandatory final check is {fmt_ts(final_due)}."
            ),
        )

    return TrackerSummary(
        elapsed_minutes=elapsed_minutes,
        next_due_minutes=elapsed_minutes,
        recommended_action="final_timeout_check_required",
        phase_guidance=(
            "60 minutes have elapsed. Perform one final ChatGPT thread check before closing the tracker. "
            "Do not deliver a final report until this final check has been completed and recorded."
        ),
    )


def update_due_fields(state: dict, start_time_et: datetime) -> None:
    elapsed_seconds = max(0, int((now_et() - start_time_et).total_seconds()))
    elapsed_minutes = elapsed_seconds // 60
    next_due = compute_next_due(start_time_et, elapsed_minutes, state.get("status", "running"), bool(state.get("finished")))
    if next_due is None:
        state["next_check_due_at_et"] = None
        state["next_check_due_at_et_iso"] = None
    else:
        state["next_check_due_at_et"] = fmt_ts(next_due)
        state["next_check_due_at_et_iso"] = next_due.isoformat()



def cmd_init(args: argparse.Namespace) -> int:
    state_path = Path(args.state_file)
    started = now_et()
    state = {
        "project": args.project or "",
        "topic": args.topic,
        "source": args.source,
        "started_at_et": fmt_ts(started),
        "started_at_et_iso": started.isoformat(),
        "thread_url": args.thread_url or "",
        "status": "running",
        "finished": False,
        "final_check_required": True,
        "check_interval_minutes": CHECK_INTERVAL_MINUTES,
        "non_blocking_after_minutes": NON_BLOCKING_AFTER_MINUTES,
        "max_runtime_minutes": MAX_RUNTIME_MINUTES,
        "checks": [
            {
                "time_et": fmt_ts(started),
                "event": "tracker_initialized",
                "note": args.note or "",
            }
        ],
    }
    update_due_fields(state, started)
    save_state(state_path, state)
    print(f"Tracker initialized: {state_path}")
    print(f"Started: {state['started_at_et']}")
    if state.get("next_check_due_at_et"):
        print(f"Next check due: {state['next_check_due_at_et']}")
    if state["thread_url"]:
        print(f"Saved thread URL: {state['thread_url']}")
    print("Reminder protocol: schedule the next 5-minute check immediately, then begin independent research.")
    return 0



def cmd_check(args: argparse.Namespace) -> int:
    state_path = Path(args.state_file)
    state = load_state(state_path)
    started = datetime.fromisoformat(state["started_at_et_iso"])
    previous_status = state.get("status", "running")

    if previous_status in TERMINAL_PENDING_STATUSES and args.observed_status == "running":
        effective_status = previous_status
        note_prefix = "Terminal pending status preserved; ignored later running observation."
    elif args.observed_status == "completed":
        effective_status = "completed_pending_close"
        note_prefix = "Observed completed; explicit close step is now required."
    elif args.observed_status == "failed":
        effective_status = "failed_pending_close"
        note_prefix = "Observed failed; explicit close step is now required."
    else:
        effective_status = "running"
        note_prefix = ""

    state["status"] = effective_status
    update_due_fields(state, started)
    summary = compute_summary(started, bool(state.get("finished")), state["status"])

    check_time = now_et()
    note = args.note or ""
    if note_prefix:
        note = f"{note_prefix} {note}".strip()
    entry = {
        "time_et": fmt_ts(check_time),
        "event": "status_check",
        "observed_status": args.observed_status,
        "effective_status": state["status"],
        "elapsed_minutes": summary.elapsed_minutes,
        "recommended_action": summary.recommended_action,
        "note": note,
    }
    state.setdefault("checks", []).append(entry)
    save_state(state_path, state)

    print(f"Elapsed minutes: {summary.elapsed_minutes}")
    print(f"Observed status: {args.observed_status}")
    print(f"Tracker status: {state['status']}")
    print(f"Recommended action: {summary.recommended_action}")
    print(summary.phase_guidance)
    if state.get("next_check_due_at_et"):
        print(f"Next check target: {state['next_check_due_at_et']}")
    else:
        print("No further periodic check is scheduled inside the tracker. Complete the explicit close step when appropriate.")
    if state.get("thread_url"):
        print(f"Thread URL: {state['thread_url']}")
    if args.observed_status == "completed":
        print("NOTE: Report observed as completed. Run 'close --final-status completed' after harvest to clear the delivery gate.")
    elif args.observed_status == "failed":
        print("NOTE: Report observed as failed. Run 'close --final-status failed' after the final check to clear the delivery gate.")
    if state.get("final_check_required"):
        print("Final ChatGPT check is still REQUIRED before delivery.")
    return 0



def cmd_close(args: argparse.Namespace) -> int:
    state_path = Path(args.state_file)
    state = load_state(state_path)
    closed = now_et()
    state["finished"] = True
    state["status"] = args.final_status
    state["closed_at_et"] = fmt_ts(closed)
    state["closed_at_et_iso"] = closed.isoformat()
    state["final_check_required"] = False
    state["next_check_due_at_et"] = None
    state["next_check_due_at_et_iso"] = None
    state.setdefault("checks", []).append(
        {
            "time_et": fmt_ts(closed),
            "event": "tracker_closed",
            "final_status": args.final_status,
            "note": args.note or "",
        }
    )
    save_state(state_path, state)
    print(f"Tracker closed: {state_path}")
    print(f"Final status: {args.final_status}")
    print("Final ChatGPT completion gate cleared.")
    return 0



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Track mandatory 5-minute deep-research status checks until completion or 60 minutes elapsed."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a new tracker state file")
    init_parser.add_argument("--state-file", required=True, help="Path to the JSON tracker state file")
    init_parser.add_argument("--project", default="", help="Project name if known")
    init_parser.add_argument("--topic", required=True, help="Short topic description")
    init_parser.add_argument("--source", default="ChatGPT", help="Origin source label")
    init_parser.add_argument("--thread-url", default="", help="Saved direct conversation URL")
    init_parser.add_argument("--note", default="", help="Optional setup note")
    init_parser.set_defaults(func=cmd_init)

    check_parser = subparsers.add_parser("check", help="Record a periodic status check")
    check_parser.add_argument("--state-file", required=True, help="Path to the JSON tracker state file")
    check_parser.add_argument(
        "--observed-status",
        default="unknown",
        choices=["unknown", "running", "completed", "failed"],
        help="Observed UI status during this check",
    )
    check_parser.add_argument("--note", default="", help="Optional observation note")
    check_parser.set_defaults(func=cmd_check)

    close_parser = subparsers.add_parser("close", help="Explicitly close the tracker after the final check")
    close_parser.add_argument("--state-file", required=True, help="Path to the JSON tracker state file")
    close_parser.add_argument(
        "--final-status",
        required=True,
        choices=["completed", "timed_out", "failed"],
        help="Final outcome after the mandatory last ChatGPT check",
    )
    close_parser.add_argument("--note", default="", help="Optional closing note")
    close_parser.set_defaults(func=cmd_close)

    return parser



def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
