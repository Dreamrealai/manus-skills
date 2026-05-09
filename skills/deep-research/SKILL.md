---
name: deep-research
description: Orchestrate a three-pronged research workflow for comprehensive reports. Use when the user asks for deep research, deepdeep research, multiple research agents, or a best-of synthesis across Gemini, ChatGPT, and Manus. This skill launches Gemini and ChatGPT deep research, enforces 5-minute ChatGPT check-ins for up to 60 minutes, preserves all raw research files with standardized names, synthesizes Manus findings in parallel, and archives the full research package. Optionally includes Claude.ai browser extension as a fourth Anthropic research stream when the user requests it.
---

# Deep Research

Run a deliberately redundant, three-pronged research workflow that combines **Gemini Deep Research**, **ChatGPT Deep Research**, and **Manus independent research**. Treat the redundancy as intentional. The goal is not to streamline it away, but to capture different research paths and then synthesize the strongest final answer.

An optional **fourth stream — Claude.ai Research (Anthropic)** — can be activated when the user explicitly requests it or when maximum coverage is needed. See the Optional Claude Stream section below.

## Non-Negotiable Rules

1. **Launch Gemini and ChatGPT deep research early** so they can run in parallel with Manus research.
2. **ChatGPT Pro Deep Research can take up to 60 minutes to complete.** This is normal and expected — do not treat a long-running ChatGPT session as a failure. The moment ChatGPT Deep Research is initiated, start a 5-minute check-in cadence and keep it going until the report is completed or **60 minutes** have elapsed.
3. **If ChatGPT Deep Research has not completed by the 60-minute ceiling, set an automatic timer to check back exactly 1 hour later.** Use the `schedule` tool to create a one-time interval task (3600 seconds, `repeat: false`) that prompts a return to the ChatGPT thread to harvest whatever is available. Do not silently abandon the thread — the timer ensures a final harvest attempt even if the session runs long.
4. **After 20 minutes, do not block the workflow waiting on ChatGPT.** It is acceptable to draft outlines, build interim synthesis, and prepare other reports first, but keep the 5-minute ChatGPT checks active.
5. **Before any final delivery, return to the ChatGPT thread one last time.** ChatGPT Deep Research must be checked as a final step and must not be silently skipped.
6. **Always preserve the raw files from all three origins** — Manus, Gemini, and ChatGPT — plus the final synthesis.
7. **Name every saved file with Eastern Time metadata** using the standardized format in the naming section below.
8. **Save the direct ChatGPT conversation URL immediately** once the `/c/<conversation_id>` thread exists. Reopen that exact URL during later checks and harvest.
9. **Start the reminder sidecar immediately after tracker initialization** so the next due check is continuously surfaced while other work continues.
10. **Gemini and ChatGPT Pro may be used redundantly when needed.** If one path is incomplete, delayed, or weak on a subtopic, keep the other active rather than collapsing to a single-provider workflow.
11. **Use Manus in a complementary way, not as a duplicate of the other two systems.** Manus is especially useful for wide research asks, logged-in browser work, social media scraping, primary-source collection, and cross-checking edge cases the other systems may miss.
12. **If the user asks for careful validation, every substantive claim in the final report must be citation-backed wherever possible.** Use ChatGPT 5.5 Thinking Extended via API with web search allowed on the final report as a dedicated validation pass to look for errors, hallucinations, and source mismatches one by one.
13. **Incorrect or unsupported areas must not be silently left in place.** Fix incorrect areas, and clearly flag any areas that could not be validated.

## Bundled Helpers

Use the bundled scripts to reduce missed steps and keep filenames consistent.

| Helper | Purpose | Typical Use |
|---|---|---|
| `scripts/deep_research_tracker.py` | Track mandatory 5-minute ChatGPT check-ins, the 20-minute non-blocking threshold, and the 60-minute ceiling | Start immediately after launching ChatGPT Deep Research |
| `scripts/deep_research_reminder.py` | Watch the tracker and emit reminder messages until the explicit close step clears the gate | Start in a separate shell session right after tracker initialization |
| `scripts/deep_research_filename.py` | Generate compact, human-readable filenames using Eastern date and military time | Run before saving each raw report, tracker file, reminder log, or final synthesis |
| `references/browser_automation.md` | Browser selectors, UI recovery notes, and extraction fallbacks for Gemini and ChatGPT Deep Research | Read when launching or harvesting reports |

## Core Workflow

1. **Create a project folder and standardized file paths**.
2. **Launch Gemini Deep Research** via the browser extension (or fall back to the Gemini API script if the extension fails).
3. **Launch ChatGPT Deep Research and immediately start the tracker and reminder sidecar**.
4. *(Optional)* **Launch Claude.ai Research** if the user requested it or maximum coverage is needed.
5. **Conduct Manus independent research while checking ChatGPT every 5 minutes**.
6. **Check Gemini on the same cadence and harvest it as soon as it is ready**.
7. **If ChatGPT is still running after 20 minutes, continue drafting without it, but keep monitoring**.
8. **If ChatGPT has not completed by 60 minutes, set the 1-hour auto-timer fallback** (see Auto-Timer Fallback section below) and proceed with available materials.
9. **Return to ChatGPT as the final pre-delivery step, harvest it, and integrate the findings**.
10. **If the user requested careful validation, run a final ChatGPT 5.5 Thinking Extended API (with web search) validation pass on the report and citations**.
11. **Archive the entire research package, including raw files, tracker logs, reminder logs, and validation notes**.

## Phase 1: Preflight Setup

Choose a short **project** label if one is obvious from the task. If not, use only a short topic description.

Create a short date-prefixed project folder. For example:

```text
260312_Lysol_DeepResearch
```

Then create standardized filenames before saving any output.

### Standard Naming Pattern

```text
YYMMDD_Project_Topic_Source_HHMM.ext
```

Example:

```text
260312_Lysol_CleaningDetergentEffectiveness_Manus_0217.md
```

### Naming Rules

| Component | Rule |
|---|---|
| `YYMMDD` | Eastern date only |
| `Project` | Optional; omit if unknown |
| `Topic` | Short human-readable topic label |
| `Source` | Use `Manus`, `Gemini`, `ChatGPT`, `Claude`, `Final`, `Tracker`, `Reminder`, or `Validation` |
| `HHMM` | Eastern military time, zero-padded |
| Length limit | Combined `Project + Topic` segment should stay compact, capped at roughly the example length (38 characters) |
| Collision handling | If an output directory is provided and a same-minute collision exists, the helper appends seconds automatically |

If the project is unknown, generate filenames with only the topic, source, and time.

### Recommended Setup Commands

```bash
PROJECT_DIR="/home/ubuntu/deep_research_runs/260312_Lysol_DeepResearch"
mkdir -p "$PROJECT_DIR"

TRACKER_JSON="$PROJECT_DIR/$(python /home/ubuntu/skills/deep-research/scripts/deep_research_filename.py \
  --project "Lysol" \
  --topic "Cleaning detergent effectiveness" \
  --source "Tracker" \
  --ext json \
  --output-dir "$PROJECT_DIR")"

REMINDER_LOG="$PROJECT_DIR/$(python /home/ubuntu/skills/deep-research/scripts/deep_research_filename.py \
  --project "Lysol" \
  --topic "Cleaning detergent effectiveness" \
  --source "Reminder" \
  --ext log \
  --output-dir "$PROJECT_DIR")"
```

## Phase 2: Launch Gemini Deep Research

For detailed UI selectors, read `references/browser_automation.md`.

1. Use the **Manus Chrome Browser Extension** to access Gemini. Navigate to `https://gemini.google.com/app`.
2. Enable **Tools → Deep Research**.
3. Submit the EXACT SAME research prompt used for ChatGPT, **prefacing it with a mandatory enumeration step if the topic involves software, platforms, or tools:**
   > "Before diving into deep analysis, please first comprehensively list and categorize every relevant tool, platform, or software updated or released through 2026 related to this topic. Once the exhaustive landscape is mapped, proceed with the deep research."
4. Confirm the research plan.
5. Leave the Gemini tab running in the background.

### Gemini API Fallback

If the browser extension fails, times out, or cannot access Gemini Deep Research via the web UI, you MUST fall back to the Gemini API using the `gemini-api` skill's dedicated research script:

```bash
# Run Gemini Deep Research via API
python3 /home/ubuntu/skills/gemini-api/scripts/deep_research.py --prompt "Your full research prompt here" --output "$PROJECT_DIR/Gemini_API_Fallback_Report.md"
```

### Gemini Monitoring

Check Gemini on the same 5-minute cadence as ChatGPT. If Gemini completes first, harvest it immediately and save the raw report with a standardized `Gemini` filename. If Gemini is still not complete after roughly 30 minutes, note that in the working notes and continue; **Gemini does not replace the mandatory final ChatGPT check**.

## Phase 3: Launch ChatGPT Deep Research and Start Monitoring

1. Navigate to `https://chatgpt.com/deep-research`.
2. Submit the same research prompt, **including the mandatory tool enumeration preface if applicable** (see Gemini step).
3. Confirm the plan.
4. **As soon as the direct conversation thread exists, save the `/c/<conversation_id>` URL.**
5. Immediately initialize the tracker.
6. Immediately start the reminder sidecar in a separate shell session.

> **Timing note:** ChatGPT Pro Deep Research routinely takes **30–60 minutes** to complete. This is expected behavior, not a failure. The 60-minute mark is a hard ceiling — not a typical completion time. Plan the rest of the workflow accordingly and keep the monitoring loop active throughout.

### Tracker Setup

```bash
python /home/ubuntu/skills/deep-research/scripts/deep_research_tracker.py init \
  --state-file "$TRACKER_JSON" \
  --project "Lysol" \
  --topic "Cleaning detergent effectiveness" \
  --source "ChatGPT" \
  --thread-url "https://chatgpt.com/c/REPLACE_WITH_CONVERSATION_ID"
```

### Reminder Sidecar Setup

```bash
python /home/ubuntu/skills/deep-research/scripts/deep_research_reminder.py \
  --state-file "$TRACKER_JSON" \
  --log-file "$REMINDER_LOG"
```

### Mandatory Monitoring Policy

| Elapsed time | Required action |
|---|---|
| 0-20 minutes | Check ChatGPT every 5 minutes while doing Manus research |
| 20-60 minutes | Continue checking every 5 minutes, but begin drafting Gemini + Manus synthesis if needed |
| 60 minutes | Perform a final explicit ChatGPT check, then close the tracker as `completed`, `timed_out`, or `failed` |
| Beyond 60 minutes | If still not complete, the auto-timer fallback (see below) will trigger a check 1 hour later |

### Active Reminder Protocol

The tracker records the cadence, but the reminder sidecar is what continuously surfaces the next due check while other work is in progress.

1. Start the reminder sidecar immediately after `init`.
2. After every `check`, read the next-due time from the tracker output.
3. Treat the next due time as the highest-priority interrupt until the tracker is explicitly closed.
4. Do not stop the reminder sidecar until the final ChatGPT closure step is complete.

### Example Periodic Check

```bash
python /home/ubuntu/skills/deep-research/scripts/deep_research_tracker.py check \
  --state-file "$TRACKER_JSON" \
  --observed-status running \
  --note "Still processing at 25-minute check"
```

**Do not stop the 5-minute cadence just because you started writing the report.** The draft can begin after 20 minutes, but the ChatGPT monitoring loop must continue.

## Auto-Timer Fallback (ChatGPT Exceeds 60 Minutes)

If ChatGPT Deep Research has **not completed by the 60-minute ceiling**, do not silently abandon the thread. Instead:

1. Close the tracker with `--final-status timed_out` and note the timeout.
2. **Immediately set an automatic 1-hour timer** using the `schedule` tool:

```text
Use the schedule tool with type "interval", interval 3600, repeat false.
Prompt: "Return to the saved ChatGPT Deep Research thread URL and check whether the report has completed. If complete, harvest the full report, save it with a standardized ChatGPT filename, and integrate the findings into the existing synthesis. If still running, note the status and set another 1-hour check if warranted."
```

3. Continue with the synthesis using Gemini + Manus materials in the meantime.
4. When the timer fires, reopen the saved `/c/<conversation_id>` URL, harvest whatever is available, and integrate it into the final report before delivery.

This ensures ChatGPT findings are never permanently lost due to a long-running session.

## Optional Claude Stream (Anthropic Research via Claude.ai)

When the user **explicitly requests maximum coverage**, mentions Claude, or asks for a fourth research stream, activate the Claude.ai Research stream alongside the other three.

**Tool:** Manus Chrome Browser Extension → `claude.ai` → enable **Research** mode (if available on the account).

**Procedure:**
1. Navigate to `https://claude.ai`.
2. Enable Research mode if available; otherwise use standard Claude chat with the instruction: "Please conduct thorough research on the following and provide citations for every claim."
3. Submit the same research prompt used for Gemini and ChatGPT.
4. Save the direct conversation URL immediately.
5. Monitor on the same 5-10 minute cadence as Gemini (hard ceiling: 45 minutes).
6. Harvest the full report and save it with a standardized `Claude` filename.
7. Integrate Claude findings into the synthesis alongside Gemini, ChatGPT, and Manus outputs.

**Fallback:** If Claude Research mode is unavailable or the account lacks access, use Claude in standard chat mode and note the fallback in the working log.

**Attribution:** In the final synthesis, tag Claude-sourced claims as `[Claude]` to distinguish them from `[Gemini]`, `[ChatGPT]`, and `[Manus]`.

## Phase 4: Manus Independent Research

While Gemini and ChatGPT run, conduct Manus's own research in a deliberately complementary way rather than merely repeating the same queries. Manus is especially useful for **wide research asks**, **logged-in browsing**, **social media scrapes**, **primary-source collection**, and **cross-checking nuanced or fast-moving claims**.

| Source Type | Focus |
|---|---|
| X / Twitter | Sentiment, breaking commentary, expert reactions |
| Reddit | Candid user feedback, community nuance, practitioner anecdotes |
| LinkedIn | Professional commentary, executive or operator insight |
| YouTube / Podcasts | Interviews, panels, explainers, expert analysis |
| Primary documents | Press releases, earnings calls, official studies, regulator or company publications |

### Research Principles

Write working notes continuously rather than waiting until the end. Preserve source URLs and short evidence snippets as you go. Push beyond standard search results and look for what the other two systems may miss. For wide or social-source-heavy asks, let Manus carry more of that burden while Gemini and ChatGPT supply parallel deep-research coverage. Save Manus notes using the standardized filename helper with source `Manus` and `--output-dir "$PROJECT_DIR"`.

## Phase 5: Harvest Gemini and ChatGPT

### 5.1 Gemini Harvest

When Gemini is complete, copy the full report and save it with a standardized `Gemini` filename.

### 5.2 ChatGPT Harvest — Final Check Is Mandatory

ChatGPT Deep Research may appear missing unless the exact thread is reopened. Use the verified recovery path below. The extraction flow must support **one primary method and up to two fallbacks** so the report is not skipped simply because it is nested or partially collapsed.

#### Primary Method: Expand the Central Report Area

1. Reopen the saved direct thread URL in the form `https://chatgpt.com/c/<conversation_id>`.
2. If the page looks blank or only shows the composer, **do not assume failure**.
3. Keep the sidebar visible and confirm the conversation title.
4. Use the visible **Scroll to bottom** control.
5. Click into the **central report area** itself to expand or surface the nested report view (canvas).
6. Wait until the report body is visibly rendered, then use the copy affordance or manual extraction.
7. Save the raw ChatGPT report with a standardized `ChatGPT` filename.

#### Fallback Method 1: Use the Visible Expand or Download Controls

If the central report-area click does not surface the full report, use the visible controls on the report card itself.

1. Look for the visible **expand**, **open**, or **download** button on the report card.
2. Use whichever control surfaces the full report.
3. If a download/export path works, save the export and preserve it alongside the raw copied text.
4. Extract only after the full report is visibly loaded.

#### Fallback Method 2: Ask ChatGPT to Reprint the Exact Response Flat

If the report remains nested, partially hidden, or uncopyable, switch to **GPT 5.4 Thinking** in the same thread and send this recovery instruction verbatim:

> Please give the response back to me without nesting it or changing the content.

Then wait for ChatGPT to restate the report in a flatter format and save that output as the harvested ChatGPT report. Note in the working log that the flattening fallback was used.

If the report finishes late, return to the draft synthesis and integrate the ChatGPT findings before final delivery.

### 5.3 If the ChatGPT Thread URL Was Not Saved

If the direct thread URL was never captured, recover it before proceeding.

1. Navigate to `https://chatgpt.com/`.
2. Inspect the sidebar for the most recent conversation matching the research prompt.
3. Open that conversation and immediately save the direct `/c/<conversation_id>` URL.
4. Resume normal monitoring and harvest steps.

### 5.4 Closing the Tracker

After the final ChatGPT check, explicitly close the tracker. This prevents silent skipping.

```bash
python /home/ubuntu/skills/deep-research/scripts/deep_research_tracker.py close \
  --state-file "$TRACKER_JSON" \
  --final-status completed \
  --note "Harvested final ChatGPT Deep Research report"
```

If the report never completes by the 60-minute final check, close with `--final-status timed_out` and note that the workflow performed the mandatory last check. Then activate the auto-timer fallback described above.

## Phase 6: Synthesis

You should now have at least these materials:

1. A raw Gemini report.
2. A raw ChatGPT report or a timed-out tracker showing the mandatory final check.
3. Raw Manus research notes.
4. *(If activated)* A raw Claude report.
5. A tracker JSON documenting the monitoring cadence.
6. A reminder log showing that the check cadence remained active.

### Synthesis Rules

| Rule | Requirement |
|---|---|
| Redundancy | Preserve all research streams as distinct attributed inputs; do not collapse them into a single-source workflow |
| Attribution | Make clear which insights came from Gemini, ChatGPT, Claude (if used), Manus, or external sources |
| Interim drafting | Acceptable after 20 minutes if ChatGPT is still running |
| Final delivery | Must happen only after the final ChatGPT return/check and explicit tracker closure |
| Validation trigger | If the user asked for careful validation, run the additional validation pass before delivery |

If you created an interim draft before ChatGPT finished, revise the synthesis after harvesting ChatGPT so the final report reflects all available findings.

Save the consolidated report with source `Final`.

### Careful-Validation Mode

If the user asks to validate findings carefully, treat validation as a separate mandatory stage rather than a casual reread.

1. Ensure **every substantive claim is citation-backed wherever the evidence is available**.
2. Run **ChatGPT 5.5 Thinking Extended via API with web search** on the final report specifically to look for errors, hallucinations, source mismatches, and overstatements.
3. Check cited sources one by one rather than trusting summary-level agreement.
4. Fix incorrect areas before delivery.
5. If a claim cannot be validated cleanly, flag it clearly to the user instead of presenting it as established fact.
6. Save the validation notes with source `Validation` if they are substantial enough to be useful later.

## Phase 7: Archive the Full Research Package

Archive **all raw and final materials**, not just the polished report.

### Minimum Required Files

| File Type | Required |
|---|---|
| Raw Gemini report | Yes |
| Raw ChatGPT report or explicit timeout record | Yes |
| Raw Manus notes | Yes |
| Raw Claude report (if stream was activated) | Yes |
| Final synthesized report | Yes |
| ChatGPT tracker JSON / status log | Yes |
| Reminder log | Yes |
| Validation notes, if validation mode was requested | Yes |

Use Google Drive for long-running research tasks. Prefer `gws` for Drive operations; use `rclone` only as fallback for bulk copy or sync.

Because the tracker JSON and reminder log were created inside the project folder with standardized names, they should already be included in the archive package.

## Failure and Recovery Rules

1. If ChatGPT appears blank, reopen the exact `/c/<conversation_id>` URL before assuming failure.
2. If the page is loaded but the report is not visible, jump to the bottom before extracting.
3. If the primary extraction method fails, try the visible expand/download controls before falling back to the flattening prompt.
4. If ChatGPT is not finished after 20 minutes, continue drafting other outputs but keep the 5-minute checks alive.
5. If ChatGPT is still unfinished at 60 minutes, perform one last explicit check, close the tracker as `timed_out`, activate the auto-timer fallback, and document the timeout.
6. If the direct ChatGPT thread URL was not saved, recover it from the most recent matching sidebar conversation and save it immediately.
7. Do not send a final user-facing deliverable until the final ChatGPT check, tracker closure, and any requested validation pass have been completed.
8. If the Claude stream was activated and stalls beyond 45 minutes, harvest partial output, mark it degraded, and continue without it.

## Deliverable Checklist

Before completing the task, confirm all of the following:

- Gemini Deep Research was launched.
- ChatGPT Deep Research was launched.
- The direct ChatGPT thread URL was preserved or explicitly recovered.
- The tracker was initialized immediately after ChatGPT launch.
- The reminder sidecar was started and kept active until tracker closure.
- ChatGPT was checked every 5 minutes until completion or 60 minutes elapsed.
- If ChatGPT exceeded 20 minutes, the workflow still continued without abandoning the monitoring loop.
- If ChatGPT exceeded 60 minutes, the auto-timer fallback was set for a 1-hour follow-up check.
- The final ChatGPT check happened before delivery (or the auto-timer fallback was activated).
- At least one primary extraction method and, when necessary, the defined fallbacks were used instead of skipping the report.
- The tracker was explicitly closed.
- All raw files were saved with standardized filenames.
- If the Claude stream was activated, the Claude report was harvested and attributed in the synthesis.
- Manus research was used in a complementary way, especially for wide or social-source-heavy asks.
- If careful validation was requested, the final report was citation-checked and reviewed with ChatGPT 5.5 Thinking Extended via API with web search.
- The final synthesized report was saved and archived with the raw materials.

If any box is not checked, the workflow is not complete.

## Strict Per-Call Limits

To prevent context degradation and ensure quality, a single LLM call generating or evaluating research prompts MUST NOT exceed:
- 5 text-to-video prompts generated or evaluated
- 5 video analyses performed
- 10 image analyses performed
- 10 image-to-video prompts generated or evaluated

If a task requires more items than these limits, it MUST be broken into multiple sequential or parallel LLM calls.
