---
name: ultrathink
description: "Orchestrate an ensemble of models to intentionally solve a problem using redundant agents, validation checkpoints, and expansion checkpoints. Use when the user asks for ultrathink, ensemble models, redundant agents, or multi-model validation. Uses Opus 4.7 via OpenRouter for planning/validation, plus Gemini 3.1 Pro (API), ChatGPT 5.5 Thinking Extended (browser extension), Gemini Deep Think (browser extension), and Gemini Deep Research (browser extension). Enforces strict per-call limits: 1 LLM call maxes at 5 text-to-video prompts, 5 video analyses, 10 image analyses, or 10 image-to-video prompts."
---

# Ultrathink Skill

Use this skill to run an **intentional ensemble of frontier models** to solve complex problems. It relies on planned redundancy, validation checkpoints, and expansion checkpoints to ensure the highest quality outcome.

## Core Workflow Rules

1. **Initial Planning (Opus 4.7)**: Use Opus 4.7 via OpenRouter to create the master plan, including specific model assignments, a checkpoint schedule, and a **Constraint Ledger** (a list of all hard constraints extracted from the user's prompt).
2. **Required Tool Ensemble**: The workflow MUST use all of the following tools at least once:
   - **Gemini 3.1 Pro** (via `gemini-api` skill)
   - **ChatGPT 5.5 Thinking Extended** (via browser extension)
   - **Gemini Deep Think** (via browser extension)
   - **Gemini Deep Research** (via browser extension - browser first, API fallback)
   - **ChatGPT Deep Research** (via browser extension ONLY - use GPT thinking mode)
   - **Claude.ai Research** (via browser extension ONLY)
   - **Opus 4.7** (via `openrouter` skill) — MUST be used at least 3 times (Planning, Validation, and one other phase).
3. **Liberal Research Integration**: The main planner should decide to use research, and if the user explicitly says deep research or implies it, ALWAYS invoke at least 3 deep research agents (Gemini, ChatGPT, Claude.ai). Overlapping prompts are fine across the three providers.
4. **Timer Logic for Long Research**: ChatGPT and Claude.ai deep research can take up to an hour. A timer MUST be set at the beginning if they are invoked. If not complete within a reasonable timeframe, set a 90-minute timer from start to check back.
5. **Research Reconciliation**: After deep research, Opus 4.7 MUST explicitly produce a "points of agreement / points of conflict / unresolved questions" memo to synthesize parallel research outputs before expansion. Opus 4.7 is the sole synthesizer and integrator — it selects the best-of-all findings and produces the definitive output.
6. **Mandatory Web-Search Conflict Resolution (anchored to today's date)**: When parallel research streams or model outputs disagree on factual claims (version numbers, release dates, licensing, pricing, feature availability, API status, GitHub stars), the agent MUST perform live web search — using search tools or browser navigation to the authoritative source (e.g., GitHub releases page, npm registry, official docs, pricing pages) — to determine the ground truth **as of today's date** (run `date +%Y-%m-%d` and include the date in every verification). Do NOT let any LLM (including Opus 4.7) arbitrate factual disputes from memory alone — LLMs hallucinate version numbers constantly. The web-verified answer is the canonical answer. Save all verifications to a `conflict_resolution_log.md` file with: the conflicting claims, which models/streams made them, the verification URL visited, the verified answer, and the date checked. This log MUST be fed to Opus 4.7 before it synthesizes. After Opus 4.7 produces output, the agent MUST spot-check any NEW factual claims Opus introduced that were not in the conflict resolution log — if found, web-verify those too before finalizing.
7. **Validation Checkpoints**: At critical junctures, pause generation and use Opus 4.7 to validate the intermediate findings. Validation MUST be multi-dimensional:
   - Factual accuracy (cross-referenced against web-verified conflict resolution log)
   - Constraint compliance (checking against the Constraint Ledger)
   - Format correctness
   - Completeness
   *If any dimension fails, trigger the Rollback Procedure (retry the failed phase up to 2 times before escalating to the user).*
8. **Final Fact-Check Pass**: After synthesis, MUST perform a final fact-check pass using live web search to flag errors and hallucinations. Any version number, release date, or pricing claim in the final output that was not web-verified during conflict resolution MUST be verified now.
9. **Expansion Checkpoints**: After validation, use an ensemble model to expand the verified findings into the final required formats.
10. **Strict Per-Call Limits**: To prevent context degradation and ensure quality, a single LLM call MUST NOT exceed:
   - 5 text-to-video prompts generated or evaluated
   - 5 video analyses performed
   - 10 image analyses performed
   - 10 image-to-video prompts generated or evaluated

If a task requires more items than these limits, it MUST be broken into multiple sequential or parallel LLM calls.

## Checkpoint Architecture

| Phase | Primary Agent | Purpose | Required Input | Required Output |
|---|---|---|---|---|
| **Planning** | Opus 4.7 | Break the problem down and assign the ensemble models. | User prompt | Task decomposition, model assignments, Constraint Ledger |
| **Deep Research** | Gemini Deep Research + ChatGPT Deep Research + Claude.ai | Parallel fact-gathering and synthesis. | Task decomposition | Parallel research dumps |
| **Web-Search Conflict Resolution** | Manus (search tools + browser) | Verify every factual disagreement via authoritative web sources, anchored to today's date. | Parallel research dumps | `conflict_resolution_log.md` with web-verified ground truth |
| **Reconciliation** | Opus 4.7 | Synthesize research using web-verified facts. Opus 4.7 is the sole synthesizer. | Parallel research dumps + conflict_resolution_log.md | Agreement/conflict memo with verified facts |
| **Expansion** | Gemini Deep Think + Gemini 3.1 Pro | Generate drafts, scripts, code, or prompts based on the research. | Agreement/conflict memo | Draft deliverables |
| **Validation** | Opus 4.7 | Verify the expansion against facts and constraints. | Draft deliverables, Constraint Ledger, conflict_resolution_log.md | Pass/fail verdict with required revisions |
| **Final Polish** | Opus 4.7 | Final formatting and delivery preparation. | Validated deliverables | Final formatted output |
| **Final Fact-Check** | Manus (web search) + Opus 4.7 | Spot-check any new factual claims Opus introduced; web-verify unverified specifics. | Final formatted output + conflict_resolution_log.md | Fact-checked and validated final output |

## Tool Access Priority

Prioritize the **Manus Chrome Extension** for accessing browser-based tools (ChatGPT 5.5 Thinking Extended, Gemini Deep Think, Gemini Deep Research, ChatGPT Deep Research, Claude.ai). If the extension fails, use the OpenRouter API for ChatGPT 5.5 Thinking Extended and the Gemini API for Gemini Deep Research as fallback options. ChatGPT Deep Research and Claude.ai are browser-only.

## ChatGPT Deep Research Extraction Trick

ChatGPT Deep Research may appear missing unless the exact thread is reopened. The extraction flow must support one primary method and up to two fallbacks:

**Primary Method: Expand the Central Report Area**
1. Reopen the saved direct thread URL (`https://chatgpt.com/c/<conversation_id>`).
2. If the page looks blank or only shows the composer, keep the sidebar visible and confirm the conversation title.
3. Use the visible **Scroll to bottom** control.
4. Click into the **central report area** itself to expand or surface the nested report view (canvas).
5. Wait until the report body is visibly rendered, then use the copy affordance or manual extraction.

**Fallback Method 1: Use Visible Controls**
Look for the visible **expand**, **open**, or **download** button on the report card.

**Fallback Method 2: Ask ChatGPT to Reprint Flat**
If the report remains nested, switch to **GPT 5.4 Thinking** in the same thread and send this recovery instruction verbatim:
> Please give the response back to me without nesting it or changing the content.

## Integration with Other Skills

This skill orchestrates other skills. When calling them, ensure you pass the per-call limits explicitly:
- Call `gemini-api` for Gemini 3.1 Pro.
- Call `openrouter` for Opus 4.7.
- Call `image-video-generation-studio` or `video-generator` for media tasks, strictly enforcing the 5-video / 10-image limits per prompt batch.

## File Storage and Persistence

After creating this plan, save all intermediate steps (especially the Constraint Ledger and Reconciliation memo) and the final deliverable to Google Drive if it involves multiple files or long text. This ensures state persistence and allows for recovery if the run is interrupted.
