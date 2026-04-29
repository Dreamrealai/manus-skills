---
name: deepdeep-research
description: >-
  OVERKILL maximally-redundant deep research skill that orchestrates Opus 4.7 planning, parallel Gemini Deep Research + ChatGPT Deep Research + Claude Research (via Claude.ai browser extension, user-triggerable) + independent Manus social/web reconnaissance (YouTube, LinkedIn, Twitter/X, Reddit, Weibo, Xiaohongshu, Douyin/TikTok, forums, news), then aggregates everything through Opus 4.7 (via OpenRouter) into one validated, bookmarked PDF. ChatGPT Pro Deep Research can take up to 60 minutes; auto-timer fallback fires 1 hour later if not complete. Trigger on: deepdeep, deepdeep research, deep deep research, overkill research, maximum research, redundant research, multi-agent research, flagship research, comprehensive deep dive, belt and suspenders research, paranoid research, triple-check research, everything research. Use when the user wants the most exhaustive, cross-verified, multi-source research report possible, cost and time be damned.
---

# deepdeep-research — The Overkill Research Skill

> "If it's worth researching, it's worth researching **four times in parallel, synthesized, validated, and archived**."

This skill is intentionally redundant. The redundancy is the feature. Do not "optimize" it by skipping streams. Every stream catches something the others miss.

## 🚨 Non-Negotiable Rules

0. **Enforced Call Quotas:** You MUST execute at least 10 deep research calls (Claude, Gemini, GPT), 5 Opus 4.7 calls, 5 Gemini 3.1 Pro calls, and 3 ChatGPT 5.4 thinking calls.
0. **Deepthink Enforcement:** You MUST force the use of Gemini Deepthink and Opus 4.7 for all synthesis and validation.
0. **Timer Logic:** Both this skill and the `brandinsights` skill are prepared for runtimes of up to 2 hours. **ChatGPT Pro Deep Research can take up to 60 minutes — this is normal and expected, not a failure.** Build in explicit timer logic and do not prematurely collapse the streams. If ChatGPT has not completed by the 60-minute ceiling, set an automatic 1-hour auto-timer fallback (see Auto-Timer Fallback section) and continue with available materials.

1. **NEVER skip the Opus 4.7 planning phase.** All downstream prompts derive from it.
2. **NEVER run research streams sequentially when they can run in parallel.** Launch Gemini, ChatGPT, Claude, and Manus social recon within the same 5-minute window.
3. **ALWAYS use Opus 4.7 for final synthesis and validation.** Opus 4.7 (via OpenRouter) is the sole synthesizer and integrator. It selects the best-of-all findings, resolves conflicts, and produces the definitive report. No other model may perform aggregation or validation.
4. **NEVER use the API for Gemini, ChatGPT, or Claude.** Always use the **Manus Chrome Browser Extension** at gemini.google.com, chatgpt.com, and claude.ai.
5. **NEVER accept a report without citations.** If a stream returns no sources, re-prompt it for citations before saving.
6. **NEVER exceed 60 minutes waiting on ChatGPT Deep Research.** Hard ceiling. Harvest whatever exists, close the tracker as `timed_out`, and activate the auto-timer fallback.
7. **NEVER collapse the four streams into one file before the aggregation phase.** Each raw report is preserved verbatim.
8. **NEVER delete raw reports after synthesis.** They are archived permanently.
9. **NEVER skip the validation pass.** A report that hasn't been error-checked is not a deepdeep report.
10. **NEVER produce a final PDF without bookmarks and a clickable table of contents.**
11. **ALWAYS save a tracker log** (`tracker.md`) updated at every check-in with timestamps.
12. **ALWAYS flag conflicting findings** between sources explicitly in the synthesis.
12a. **ALWAYS resolve conflicts via live web search before synthesis — anchored to today's date.** When research streams disagree on factual claims (version numbers, release dates, licensing, pricing, feature availability, API status), the agent MUST perform live web search (using search tools or browser navigation to the authoritative source — e.g., GitHub releases page, npm registry, official docs) to determine the ground truth **as of today's date** (use `date +%Y-%m-%d` to get the current date and include it in every verification entry). Do NOT let Opus 4.7 or any LLM arbitrate factual disputes from memory alone — LLMs hallucinate version numbers constantly. The web-verified answer is the canonical answer. Document every verification in `synthesis/conflict_resolution_log.md` with: the conflicting claims, which streams made them, the verification URL visited, the verified answer, and the date checked. This rule applies to Opus 4.7's own claims as well — if Opus 4.7 asserts a version number during synthesis that was not web-verified, the agent MUST pause and verify it before including it in the final report.
13. **ALWAYS attribute claims** to their originating stream (Gemini / ChatGPT / Claude / Manus-Social).
14. **ALWAYS revisit and harvest streams that finish late.** If a stream finishes while you are working on other tasks, you MUST return to it, harvest the final output, and run the explicit `close` command on the tracker to clear the delivery gate. Do not silently move on.
15. **ALWAYS enforce the Recency Protocol (April 2026).** Every quantitative claim MUST carry a `[Source, Month YYYY]` inline citation. Flag any data point older than October 2025 as STALE and explicitly caveat it. Prioritize Q1 2026 earnings calls and recent data.
16. **ALWAYS use Agentic Scraping.** Do not rely solely on public search. You MUST use the Manus Chrome Extension or API tools to scrape quantified signals (e.g., Amazon reviews, Trustpilot/G2 scores, Meta Ads Library ad counts, Reddit sentiment, SimilarWeb traffic).
17. **ALWAYS produce a validation delta document** showing what the validation pass changed and why.
18. **ALWAYS archive everything to Google Drive** — raw reports, synthesis, PDF, delta, tracker, planning memo.
19. **ALWAYS include Chinese-language social sources** (Weibo, Xiaohongshu, Douyin) unless the topic is explicitly inapplicable (in which case, document the exclusion).
20. **ALWAYS ask for citations at every stage** — planning, research, synthesis, and validation.
21. **If any stream fails, log the failure in `tracker.md` and continue.** Do not abort the whole skill because one stream died.
22. **NEVER allow the final report to be under 10 pages.** If the aggregated output is under 10 pages, it is not a deepdeep report — re-prompt immediately.
23. **NEVER allow any model to over-condense.** Summarizing away detail is a failure mode. Depth, breadth, and specificity must be preserved at every stage.
24. **The target length is 20 pages. The hard floor is 10 pages. The hard ceiling is 30 pages.** Reports outside this band must be expanded or trimmed before PDF generation.
25. **The final PDF must open with a 1-2 page Executive Summary followed by a 1 page Table of Contents / Bookmarks page.** These are mandatory structural elements, not optional.

## Workflow Overview

```text
[User Topic]
     │
     ▼
Phase 0: Opus 4.7 Planning (OpenRouter)
     │  → 3+ sub-topic prompts, 1 meta-question, strategy memo, target sources
     ▼
Phase 1: Preflight Setup (folders, naming, tracker)
     │
     ▼
Phase 2: PARALLEL LAUNCH
     ├── 2a: Gemini Deep Research (Targeted)  ──┐
     ├── 2b: ChatGPT Deep Research (Targeted) ──┤
     ├── 2c: Claude Research                  ──┤  (all simultaneously)
     ├── 2d: Manus Social Recon               ──┤
     ├── 2e: Gemini Deep Research (Broad)     ──┤
     └── 2f: ChatGPT Agent-Mode (Broad)       ──┘
     │
     ▼
Phase 3: Monitoring Loop (5/10-min check-ins)
     │  → If ChatGPT not done at 60 min: auto-timer fallback fires 1 hr later
     ▼
Phase 4: Harvest All Reports
     │
     ▼
Phase 5: Aggregation via Opus 4.7 (OpenRouter)
     │  → de-dupe, synthesize, select best-of-all, attribute, flag conflicts
     ▼
Phase 6: PDF Generation (with bookmarks + TOC)
     │
     ▼
Phase 7: Validation Pass via Opus 4.7 (OpenRouter)
     │  → fact-check, hallucination hunt, validation delta
     ▼
Phase 8: Archive to Google Drive
     │
     ▼
[Final Deliverable Bundle]
```

## Phase 0 — Opus 4.7 Planning (OpenRouter)

**Goal:** Decompose the user's topic into a rigorous research plan before a single browser tab opens.

**Tool:** Opus 4.7 via OpenRouter (`python3 /home/ubuntu/skills/openrouter/scripts/openrouter_chat.py --alias opus-4.7`).

**Inputs:** User topic, any user-provided constraints (recency, geography, depth, etc.).

**Prompt scaffold to send Opus 4.7:**

```text
You are the planning architect for an overkill redundant research operation.
Topic: <USER_TOPIC>
Constraints: <USER_CONSTRAINTS or "none">

Produce a JSON document with:
1. "sub_prompts": an array of AT LEAST 3 self-contained deep-research prompts
   covering distinct sub-angles of the topic. Each must be brief, open-ended, and 
   no more than 2-3 sentences long.
   **Crucial Formatting Rule:** Lead with the core topic and context, and instruct
   the models to discover the latest insights, key trends, players, and best tools.
   Leave room for expansive interpretation so the research models can follow the data
   across all sources. Each prompt must request citations and explicitly demand
   recency anchored to 2026 and maximum breadth.
2. "meta_question": ONE broad synthesis theme or question that ties all sub-prompts
   together. Must demand cross-domain reasoning and allow for nuanced, unexpected findings.
3. "strategy_memo": a 300-600 word memo explaining WHY these prompts were
   chosen, what gaps they cover, and what risks/blind spots remain.
4. "target_sources": a list of specific source types or named sources to
   prioritize (academic journals, named experts, specific subreddits,
   specific Weibo/Xiaohongshu tags, YouTube channels, etc.).
5. "success_criteria": bullet list of what a successful final report
   must contain.

**Important Philosophy:** Avoid overly rigid interrogative framing. Do not box the research models in with strict yes/no or narrow questions. Instead, frame the prompt around the topic, provide examples of what to look for, and instruct the models to discover and synthesize the most critical insights organically.

Return ONLY valid JSON.
```

**Outputs saved to `planning/`:**
- `planning/opus_plan.json`
- `planning/strategy_memo.md` (human-readable extraction)
- `planning/sub_prompts.md`
- `planning/meta_question.md`

**Rule:** If Opus returns fewer than 3 sub-prompts, re-prompt. Do not proceed with fewer.

**JSON truncation guard:** Opus 4.7 may truncate if `--max-tokens` is too low. The planning prompt generates verbose sub-prompts (~150-300 words each), so always use `--max-tokens 4000` or higher for the planning call. If the returned JSON is invalid or incomplete, re-run with a higher token limit before proceeding. Validate the JSON is parseable before saving:

```bash
python3 -c "import json, sys; data=json.load(open('planning/opus_plan.json')); print('Keys:', list(data.keys())); print('sub_prompts:', len(data['sub_prompts']))"
```

**Extract human-readable files from the JSON immediately after validation:**

```bash
python3 -c "
import json
with open('planning/opus_plan.json') as f:
    data = json.load(f)
with open('planning/sub_prompts.md', 'w') as f:
    for i, p in enumerate(data['sub_prompts'], 1):
        f.write(f'## Sub-Prompt {i}\n\n{p}\n\n')
with open('planning/meta_question.md', 'w') as f:
    f.write(f'# Meta-Question\n\n{data[\"meta_question\"]}\n')
with open('planning/strategy_memo.md', 'w') as f:
    f.write(f'# Strategy Memo\n\n{data[\"strategy_memo\"]}\n')
print('Extracted planning files OK')
"
```

## Phase 1 — Preflight Setup

**Goal:** Establish deterministic folder structure and naming conventions BEFORE launching any stream.

**Folder structure (created under `./deepdeep_<slug>_<YYYYMMDD_HHMM>/`):**

```text
deepdeep_<slug>_<timestamp>/
├── planning/
│   ├── opus_plan.json
│   ├── strategy_memo.md
│   ├── sub_prompts.md
│   └── meta_question.md
├── raw/
│   ├── gemini_deepresearch_<slug>.md
│   ├── chatgpt_deepresearch_<slug>.md
│   ├── claude_research_<slug>.md
│   └── manus_social_<slug>.md
├── social_subreports/
│   ├── youtube.md
│   ├── linkedin.md
│   ├── twitter_x.md
│   ├── reddit.md
│   ├── weibo.md
│   ├── xiaohongshu.md
│   ├── douyin_tiktok.md
│   ├── forums_news.md
│   └── screenshots/
├── synthesis/
│   ├── aggregated_report.md
│   ├── aggregated_report.pdf
│   └── conflicts_ledger.md
├── validation/
│   ├── validation_delta.md
│   └── aggregated_report_validated.pdf
├── tracker.md
└── MANIFEST.md
```

**Naming convention:** `<stream>_<slug>_<YYYYMMDD>.md`. The slug is a kebab-case compression of the topic (≤40 chars).

**Initialize `tracker.md`** with columns: `timestamp | phase | stream | status | notes`.

## Phase 2 — Launch ALL Research Streams Simultaneously

> Do not wait for any stream to finish before starting the next. All four streams launch within the same 5-minute window.

### 2a — Gemini Deep Research (Targeted)

- **Tool:** Manus Chrome Browser Extension → `gemini.google.com` → enable "Deep Research" mode.
- **Input:** Paste ALL sub-prompts from `planning/sub_prompts.md` as a combined prompt, explicitly asking for:
  - Citations with URLs
  - Distinct sections per sub-prompt
  - Tables where comparative
  - Flagged uncertainties
- **Action:** Click "Start research" and note the start timestamp in `tracker.md`.

### 2e — Gemini Deep Research (Broad)

- **Tool:** Manus Chrome Browser Extension → `gemini.google.com` → enable "Deep Research" mode (in a new tab/thread).
- **Input:** "Provide the latest insights on <USER_TOPIC>. What are the key trends, players, and best tools? Be expansive in all sources, ensure recency anchored to 2026, and capture maximum breadth."
- **Action:** Click "Start research" and note the start timestamp in `tracker.md`.

### 2b — ChatGPT Deep Research (Targeted) + Tracker

- **Tool:** Manus Chrome Browser Extension → `chatgpt.com` → select "Deep Research" (or equivalent) mode on GPT-5.4 Pro.
- **Input:** ALL sub-prompts **PLUS the meta-question** (this stream is the only one that gets the meta-question during initial research).
- **Explicitly request:**
  - Inline citations
  - A dedicated "cross-cutting synthesis" section answering the meta-question
  - Structured headers
- Answer ChatGPT's clarifying questions quickly and minimally (prefer "proceed with best judgment, cover all angles").
- **Immediately save the direct conversation URL** once the `/c/<conversation_id>` thread exists. Store it in `tracker.md` under the ChatGPT row. This URL is required for all subsequent check-ins and harvest. If the URL is lost, recover it from the ChatGPT sidebar by finding the most recent matching conversation.
- Log the start timestamp.

### 2f — ChatGPT Agent-Mode Thinking (Broad)

- **Tool:** Manus Chrome Browser Extension → `chatgpt.com` → select "Agent Mode" (allows browsing, looking at sites directly).
- **Input:** "Provide the latest insights on <USER_TOPIC>. What are the key trends, players, and best tools? Be expansive in all sources, ensure recency anchored to 2026, and capture maximum breadth."
- **Action:** Allow Agent Mode to browse sites directly. Save the conversation URL and note the start timestamp in `tracker.md`.

> **Timing note:** ChatGPT Pro Deep Research routinely takes **30–60 minutes** to complete. This is expected behavior, not a failure. The 60-minute mark is a **hard ceiling** — not a typical completion time. Do not treat a long-running session as stalled unless it exceeds 60 minutes without any visible progress. Plan the rest of the workflow accordingly and keep the monitoring loop active throughout.

- **Hard ceiling: 60 minutes.** If not complete by then, close the tracker as `timed_out` and activate the auto-timer fallback (see below).

### 2c — Claude Research (Anthropic via Claude.ai Browser Extension)

- **Tool:** Manus Chrome Browser Extension → `claude.ai` → enable **Research** mode (if available on the account).
- **Trigger:** This stream is active by default in deepdeep-research. The user may also explicitly request it in the `deep-research` skill for maximum coverage.
- **Input:** Sub-prompts from `planning/sub_prompts.md`.
- **Request:** Citations, structured sections, explicit confidence levels on claims.
- **Save the direct conversation URL immediately** once the thread exists. Store it in `tracker.md` under the Claude row.
- **Fallback:** If Claude Research mode is unavailable or the account lacks access, use Claude in standard chat mode with the prompt: "Please conduct thorough research on the following and provide citations for every claim." Note the fallback in `tracker.md`.
- **Hard ceiling: 45 minutes.** If not complete, harvest partial output and mark degraded.

### 2d — Manus Social / Web Research (independent, concurrent)

Manus independently browses — **do not delegate this to any LLM tool**. This stream is the ground-truth human-like reconnaissance layer.

**Required coverage (one sub-report per platform, in `social_subreports/`):**

| Platform | What to gather |
|---|---|
| **YouTube** | Top 5-10 relevant videos: title, channel, URL, view count, upload date, transcript summary, key claims, notable comments |
| **LinkedIn** | Expert posts, company updates, named practitioners, relevant articles |
| **Twitter/X** | Threads from subject-matter experts, trending takes, dissenting views, linked sources |
| **Reddit** | Top threads across relevant subreddits; highly-upvoted comments; contrarian views |
| **Weibo (微博)** | Chinese public discourse, trending hashtags, verified-account posts |
| **Xiaohongshu (小红书)** | Consumer/lifestyle/practitioner perspective from mainland China |
| **Douyin / TikTok** | Short-form video trends, creator claims, engagement signals |
| **Forums & News** | Hacker News, specialist forums, major news outlets, trade press |

**Rules for this stream:**
- Capture URLs for every claim.
- Take screenshots for non-text-archival content (save under `social_subreports/screenshots/`).
- Translate Chinese-language content to English but preserve original quotes.
- Produce `raw/manus_social_<slug>.md` as a unified report citing all sub-reports.

## Phase 3 — Monitoring Loop

Run concurrent monitoring. Update `tracker.md` at every check-in.

| Stream | Check cadence | Hard ceiling | Action on ceiling |
|---|---|---|---|
| ChatGPT Deep Research | Every 5 min | 60 min | Harvest partial; close tracker as `timed_out`; activate auto-timer fallback |
| Gemini Deep Research | Every 5-10 min | 45 min | Harvest partial; note in tracker |
| Claude Research | Every 10 min | 45 min | Harvest partial; note in tracker |
| Manus Social | Continuous | Until Phase 4 trigger | Keep gathering until all platforms covered |

**Check-in procedure (each stream):**
1. Open the browser tab via extension.
2. Check completion status.
3. If complete → harvest in Phase 4. **Crucial:** If you observe a stream is complete but you are busy with another stream, you MUST return to it later to harvest.
   - **ChatGPT Extraction Trick**: For ChatGPT Deep Research, reopen the exact thread URL, scroll to bottom, and click into the central report area to expand the nested report view (canvas) before extracting. If it remains nested, ask ChatGPT 5.4 Thinking to "Please give the response back to me without nesting it or changing the content."
4. If in progress → log progress, return to loop.
5. If stalled/errored → attempt one refresh; on second failure, mark degraded in tracker and continue.
6. **Delivery Gate:** You cannot proceed to Phase 5 until the tracker script explicitly confirms the final completion gate is cleared via the `close` command.

**Proceed to Phase 4 only when:** all three LLM streams have either completed, hit their ceiling, or are marked degraded; AND the Manus social stream has covered all required platforms.

## Auto-Timer Fallback (ChatGPT Exceeds 60 Minutes)

If ChatGPT Deep Research has **not completed by the 60-minute ceiling**:

1. Perform one final explicit check of the ChatGPT thread.
2. Close the tracker with `--final-status timed_out` and note the timeout in `tracker.md`.
3. **Immediately set an automatic 1-hour timer** using the `schedule` tool:

```text
Use the schedule tool with type "interval", interval 3600, repeat false.
Prompt: "Return to the saved ChatGPT Deep Research thread URL stored in tracker.md and check whether the report has completed. If complete, harvest the full report, save it with a standardized ChatGPT filename in the raw/ folder, integrate the findings into the existing synthesis/aggregated_report.md, and regenerate the validated PDF. If still running, note the status in tracker.md and set another 1-hour check if warranted."
```

4. Continue with Phase 5 aggregation using Gemini + Claude + Manus materials in the meantime.
5. When the timer fires, reopen the saved `/c/<conversation_id>` URL, harvest whatever is available, and integrate it into the final report before the definitive delivery.

This ensures ChatGPT findings are never permanently lost due to a long-running session, even if the session significantly exceeds the 60-minute ceiling.

## Phase 4 — Harvest All Reports

For each completed stream:

1. Copy full output (including citations) from the browser. (For ChatGPT Deep Research, remember to use the extraction trick: reopen exact URL, scroll to bottom, click central report area to expand canvas, or fall back to asking GPT 5.4 Thinking to print flat).
2. Save to `raw/<stream>_<slug>_<YYYYMMDD>.md` using the standardized filename.
3. Prepend a YAML header to each raw file:

```yaml
---
stream: gemini | chatgpt | claude | manus-social
started_at: <ISO timestamp>
ended_at: <ISO timestamp>
status: complete | partial | degraded
prompts_used: [sub-prompt-1, sub-prompt-2, ...]
meta_question_included: true | false
citation_count: <int>
---
```

4. Verify citations are present. If missing from an LLM stream, re-prompt that stream once for "add citations inline to the report above." Save the re-prompted version.
5. Update `tracker.md` with final harvest timestamp and citation count.
6. Produce `MANIFEST.md` listing every file with size, line count, and status.

## Output Length & Structure Standard

Every final report produced by this skill must conform to the following page and structure standard. This applies to both the aggregated report (Phase 5) and the validated report (Phase 7).

| Attribute | Requirement |
|---|---|
| **Hard floor** | 10 pages minimum |
| **Target** | 20 pages |
| **Hard ceiling** | 30 pages |
| **Page 1-2** | Executive Summary (1-2 pages) — key findings, consensus conclusions, top conflicts, confidence rating |
| **Page 3** | Table of Contents / Bookmarks page — all `##` and `###` headings listed with page numbers |
| **Pages 4+** | Body — full organized content with `##` section headers and `###` sub-headers |
| **Final pages** | Full Bibliography (deduplicated URLs) + Open Questions & Gaps |

**Anti-condensation rules:**
- Do not summarize when you can quote or paraphrase with full detail.
- Do not merge distinct findings from different streams into a single sentence.
- Do not drop a finding just because another stream said something similar — attribute both.
- Do not truncate citations, source lists, or bibliography entries.
- If a section feels thin, expand it with additional context, background, or source detail rather than leaving it short.

**Page count check procedure (mandatory before PDF generation):**
1. Count approximate pages: divide total word count by 400 (standard ~400 words/page).
2. If under 10 pages (< ~4,000 words): re-prompt Opus 4.7 with the expansion directive below.
3. If over 30 pages (> ~12,000 words): re-prompt Opus 4.7 with the trim directive below.
4. If within 10-30 pages: proceed to PDF generation.

**Expansion directive (use when under 10 pages):**
```text
This report is too short. The target is 20 pages (approximately 8,000 words).
For every section that is under 3 paragraphs, expand it with:
- Additional context and background
- More granular detail from the source material
- Specific data points, quotes, or examples
- Additional attribution of which streams support each claim
Do NOT add filler. Expand with substance. Do not summarize — elaborate.
```

**Trim directive (use when over 30 pages):**
```text
This report exceeds 30 pages. Trim to approximately 20-25 pages by:
- Removing exact duplicate sentences (same claim, same wording)
- Condensing the bibliography to remove dead or duplicate URLs only
- Shortening transition prose between sections
Do NOT remove unique findings, citations, or any content from a single-source section.
```

## Phase 4b — Conflict Resolution via Live Web Search (MANDATORY)

**Goal:** Before Opus 4.7 synthesizes, the agent MUST identify and resolve every factual conflict between research streams using live web search. This prevents LLM hallucination from contaminating the final report. **All verifications must be anchored to today's date** — run `date +%Y-%m-%d` at the start of this phase and include the date in every log entry. Opus 4.7 is the synthesizer, but it is NOT the fact-checker — the web is the fact-checker.

**Procedure:**
1. Compare all harvested raw reports and identify every factual disagreement: version numbers, release dates, licensing terms, pricing, feature claims, API availability, GitHub stars, maintenance status.
2. For EACH conflict, perform a live web search or navigate directly to the authoritative source:
   - **Version numbers**: Check the GitHub releases page or npm registry (`https://github.com/<org>/<repo>/releases` or `https://www.npmjs.com/package/<pkg>`)
   - **Licensing**: Check the LICENSE file in the repo or the package.json
   - **Pricing**: Check the official pricing page
   - **Feature claims**: Check the official documentation or changelog
   - **Stars/maintenance**: Check the GitHub repo directly
3. Save all verifications to `synthesis/conflict_resolution_log.md` in this format:

```markdown
## Conflict: <component name>
- **Stream A claim** (<stream>): <claim>
- **Stream B claim** (<stream>): <claim>
- **Verification URL**: <url visited>
- **Verified answer**: <ground truth as of today>
- **Date checked**: <YYYY-MM-DD>
- **Winner**: <which stream was correct>
```

4. Feed the `conflict_resolution_log.md` to Opus 4.7 along with the raw reports so it uses verified facts, not LLM guesses.
5. **Post-synthesis spot-check**: After Opus 4.7 produces the aggregated report, the agent MUST scan the output for any NEW factual claims (version numbers, dates, pricing) that Opus introduced which were NOT in the conflict resolution log. If found, web-verify those too before finalizing. Opus 4.7 is brilliant at synthesis but still hallucinates specifics.

**Hard rule:** The agent MUST NOT proceed to Phase 5 aggregation until all identified conflicts have been web-verified. If a conflict cannot be verified (source is down, paywalled, etc.), document it as `UNVERIFIED` with the reason and flag it in the final report. Every entry in the conflict resolution log MUST include the verification date (today's date via `date +%Y-%m-%d`).

## Phase 5 — Aggregation via Opus 4.7

**Tool:** Opus 4.7 via OpenRouter API (`python3 /home/ubuntu/skills/openrouter/scripts/openrouter_chat.py --alias opus-4.7`). Opus 4.7 is the sole synthesizer — it selects the best insights from all streams, resolves version conflicts using the web-verified conflict resolution log, and produces the definitive best-of-all report.

**Procedure:**
1. Upload (or paste in chunks if needed) all four raw reports + the Opus planning memo + the meta-question + `synthesis/conflict_resolution_log.md`.
2. Issue the following aggregation directive:

```text
You are the aggregator for an overkill redundant research project. You have:
- planning/strategy_memo.md
- planning/meta_question.md
- raw/gemini_deepresearch_targeted_<slug>.md
- raw/gemini_deepresearch_broad_<slug>.md
- raw/chatgpt_deepresearch_targeted_<slug>.md
- raw/chatgpt_agent_broad_<slug>.md
- raw/claude_research_<slug>.md
- raw/manus_social_<slug>.md (plus per-platform sub-reports)

Produce ONE very long, organized synthesis report structured as follows:

SECTION 1 — Executive Summary (1-2 pages)
Summarize the most important findings across all streams. Include: top
consensus conclusions, the most significant conflicts, the answer to the
meta-question in brief, and an overall confidence rating. This section
should stand alone as a briefing document.

SECTION 2 — Table of Contents (1 page)
List every ## and ### heading with anchor links. This is a navigation
page, not a summary.

SECTION 3+ — Body (organized by topic, not by stream)
Use ## for major topic sections and ### for sub-topics. For every
substantive claim, include an inline attribution tag: [Gemini], [ChatGPT],
[Claude], [Manus-Social], or [Multiple]. Preserve inline citations (URLs)
from the raw reports throughout.

Required body sections (add more as the topic demands):
- Background & Context
- Key Findings by Sub-Topic (one ## per sub-prompt from the plan)
- Consensus Findings (claims supported by ≥3 streams)
- Single-Source Findings (claims from only 1 stream — flag as lower confidence)
- Conflicts & Disagreements (every point where sources disagreed, with
  attribution on both sides — do not merge or paper over disagreements)
- Answer to the Meta-Question (synthesizing across all streams)
- Social & Community Signals (from Manus social recon)
- Open Questions & Gaps
- Full Bibliography (all cited URLs, deduplicated)

LENGTH REQUIREMENT: The report MUST be approximately 20 pages
(~8,000 words). The hard floor is 10 pages (~4,000 words). The hard
ceiling is 30 pages (~12,000 words). Do not summarize — elaborate.
Do not merge distinct findings — attribute each separately. Do not
drop any finding that is unique to one stream. Thoroughness is the
primary success criterion. If you find yourself writing a section in
fewer than 3 paragraphs, expand it.
```

3. Save the result as `synthesis/aggregated_report.md`.
4. Extract the conflicts section also to `synthesis/conflicts_ledger.md` for quick reference.

**Length check (mandatory):** After saving `synthesis/aggregated_report.md`, count the word count (`wc -w synthesis/aggregated_report.md`). Apply the page count check procedure from the Output Length & Structure Standard section above before proceeding to Phase 6. Do not skip this check.

## Phase 6 — PDF Generation with Bookmarks

**Tool:** Pre-installed utility `manus-md-to-pdf` or similar markdown-to-pdf converter.

**Requirements:**
- Clickable Table of Contents at the start.
- PDF bookmarks mirroring every `#` and `##` heading.
- Page numbers.
- Citations preserved as hyperlinks.

**Command (reference):**
```bash
manus-md-to-pdf synthesis/aggregated_report.md synthesis/aggregated_report.pdf
```

**Verify:** Open the PDF, confirm the bookmark panel populates and links navigate correctly. If bookmarks are missing, regenerate before proceeding.

## Phase 7 — Validation Pass via Opus 4.7

**Tool:** Opus 4.7 via OpenRouter API (`python3 /home/ubuntu/skills/openrouter/scripts/openrouter_chat.py --alias opus-4.7`). Opus 4.7 performs the validation pass as the authoritative fact-checker.

**Procedure:**
1. Upload `synthesis/aggregated_report.pdf`.
2. Issue the validation directive (ensure web search is enabled for fact-checking):

```text
You are the validator for an overkill research project. Review the attached
PDF for:

1. Factual errors (check against your training knowledge and the inline citations).
2. Hallucinations (claims with no citation or with fabricated-looking URLs).
3. Unsupported claims (inference presented as fact).
4. Logical inconsistencies (claims that contradict each other within the doc).
5. Citation integrity (do cited URLs plausibly exist and match the claim?).
6. Attribution errors (claim tagged to wrong stream).

For EACH issue found, produce a row in a validation table:
  | location | issue type | original text | recommended fix | severity |

Then produce a "corrected" version of the report with all fixes applied.
Clearly mark every changed passage with [VALIDATED] or [CORRECTED].

CRITICAL LENGTH RULE: When correcting errors, do NOT shorten the report.
Fix factual issues in place. Do not remove sections, collapse paragraphs,
or summarize content that was previously expanded. The corrected version
must remain within the 10-30 page band (target 20 pages). If corrections
require removing a passage, replace it with corrected content of similar
length — do not leave a gap.

Also produce a "validation_delta.md" summarizing:
- Number of issues found by category
- List of most material corrections
- Overall confidence rating (low / medium / high) with justification
- Word count of corrected report vs. original (must remain in 10-30 page band)
```

3. Save:
   - Corrected markdown → regenerate PDF → `validation/aggregated_report_validated.pdf`
   - `validation/validation_delta.md`
4. Regenerate bookmarks on the validated PDF using the same Phase 6 procedure.

**Rule:** If the validator finds >10 material errors, loop once more through validation on the corrected version. Cap at 2 validation passes.

## Phase 8 — Final Archive to Google Drive

**Tool:** `gws` CLI tool.

**Procedure:**
1. Create a Drive folder: `deepdeep-research / <slug> / <YYYYMMDD_HHMM>`.
2. Upload the **entire** local directory tree, preserving structure.
3. Produce and upload a final `MANIFEST.md` including:
   - Topic, slug, timestamp
   - Links to every file
   - Stream statuses
   - Citation counts per stream
   - Validation summary
   - Known gaps
4. Return the Drive folder URL to the user along with direct links to:
   - `synthesis/aggregated_report.md`
   - `validation/aggregated_report_validated.pdf`
   - `validation/validation_delta.md`
   - `tracker.md`

## Failure & Recovery Rules

| Failure | Recovery |
|---|---|
| Opus 4.7 (OpenRouter) unreachable | Retry 3× with backoff; if still failing, fall back to Claude Sonnet via OpenRouter for planning and annotate `strategy_memo.md` with the fallback |
| Gemini Deep Research stalls >45 min | Harvest partial, mark degraded, continue |
| ChatGPT Deep Research stalls >60 min | Hard stop. Harvest partial. Close tracker as `timed_out`. Activate auto-timer fallback (1-hour check). Continue with remaining streams. |
| Claude Research stalls >45 min | Harvest partial, mark degraded, continue |
| Browser extension disconnects | Reconnect, refresh tab, resume check-in cadence; log the gap |
| One social platform inaccessible (login wall, geo-block) | Document in `manus_social_<slug>.md` under "Coverage Gaps"; do not abort |
| Aggregation step produces thin output (<10 pages) | Re-prompt Opus 4.7 with the expansion directive from the Output Length & Structure Standard section |
| Aggregation step produces bloated output (>30 pages) | Re-prompt Opus 4.7 with the trim directive from the Output Length & Structure Standard section |
| Validation pass shrinks the report below 10 pages | Re-prompt validator: "Fix errors in place — do not remove content. Replace corrected passages with corrected content of equal length." |
| PDF generation fails | Fall back to standard markdown-to-pdf; if still failing, produce HTML + print-to-PDF |
| Validation finds >10 material errors | Run second validation pass on corrected doc (max 2 passes total) |
| Google Drive upload fails | Retry 3×; fall back to local zip archive + notify user |
| Any single stream totally fails | Continue with remaining streams; note in tracker and MANIFEST; final report must explicitly disclose the missing stream |

**Cardinal rule:** One failed stream does NOT abort the skill. The redundancy exists precisely to survive partial failures.

## ✅ Deliverable Checklist

Before declaring the skill complete, confirm **every** item:

- [ ] `planning/opus_plan.json` generated
- [ ] `planning/strategy_memo.md` generated
- [ ] `planning/sub_prompts.md` generated
- [ ] `planning/meta_question.md` generated
- [ ] Folder structure created
- [ ] `tracker.md` initialized
- [ ] Gemini Deep Research launched
- [ ] ChatGPT Deep Research launched (direct conversation URL saved immediately)
- [ ] Claude Research launched via Claude.ai browser extension (or fallback noted)
- [ ] Manus Social Recon started across all platforms
- [ ] Check-ins performed on cadence and logged
- [ ] If ChatGPT exceeded 60 min: tracker closed as `timed_out` AND auto-timer fallback set for 1-hour follow-up
- [ ] All reports harvested with YAML headers
- [ ] `synthesis/conflict_resolution_log.md` generated with web-verified resolutions for all inter-stream conflicts
- [ ] `synthesis/aggregated_report.md` generated via Opus 4.7 (using verified conflict resolutions)
- [ ] `synthesis/conflicts_ledger.md` extracted
- [ ] Page count check performed (word count ÷ 400 = estimated pages; must be 10-30)
- [ ] Executive Summary present (1-2 pages)
- [ ] Table of Contents / Bookmarks page present (1 page)
- [ ] All required body sections present with ## headers
- [ ] PDF generated with bookmarks
- [ ] Validation pass performed via Opus 4.7
- [ ] `validation/validation_delta.md` generated
- [ ] `validation/aggregated_report_validated.pdf` generated
- [ ] Final page count confirmed within 10-30 page band
- [ ] Full package uploaded to Google Drive
- [ ] Deliverables sent to user

## Enforcement Hooks & Completion Gates

The following enforcement mechanisms are **mandatory** and prevent the skill from declaring completion prematurely. These are not suggestions — they are hard gates.

### Gate 1: Tracker State Machine

A `tracker.md` file MUST be initialized at Phase 1 and updated at every check-in. The tracker records:
- Stream launch timestamps and URLs
- Check-in timestamps with observed status
- Harvest timestamps
- Timer fallback activation timestamps
- Final closure status per stream

**Hard rule:** The skill CANNOT proceed to Phase 5 (Aggregation) until every stream is either `harvested`, `timed_out`, or `failed` in the tracker. No stream may remain in `running` or `unknown` status when aggregation begins.

### Gate 2: Timer Enforcement

When ChatGPT Deep Research exceeds 60 minutes:
1. The tracker MUST be updated with status `timed_out`
2. A 1-hour auto-timer fallback MUST be set using the `schedule` tool
3. The timer prompt MUST include the ChatGPT conversation URL and instructions to harvest, integrate, and update Google Drive
4. **Verification:** Before declaring the skill complete, check whether the auto-timer has fired. If it has not yet fired, the skill MUST either wait for it or explicitly document that the ChatGPT stream will be integrated asynchronously.

### Gate 3: Pre-Delivery Checklist Validation

Before sending final deliverables to the user, the agent MUST programmatically verify every item in the Deliverable Checklist section above. This is not a mental check — it requires:
1. Verifying each file exists on disk (`ls -la` each expected file)
2. Verifying word count of `synthesis/aggregated_report.md` is within the 10-30 page band
3. Verifying the tracker shows all streams are closed (not `running`)
4. Verifying Google Drive upload succeeded (file IDs returned)

If any gate fails, the skill MUST NOT deliver results. Instead, it must fix the failing gate and re-check.

### Gate 4: Late-Arriving Stream Integration

If a stream completes after the initial synthesis (e.g., ChatGPT finishes during or after the auto-timer), the agent MUST:
1. Harvest the late stream's full output
2. Run a supplementary Opus 4.7 synthesis call to integrate the new findings
3. Produce an addendum document or update the main report
4. Upload the updated materials to Google Drive
5. Notify the user of the integration

This gate ensures no research stream's findings are permanently lost due to timing.

## Strict Per-Call Limits

To prevent context degradation and ensure quality, a single LLM call MUST NOT exceed:
- 5 text-to-video prompts generated or evaluated
- 5 video analyses performed
- 10 image analyses performed
- 10 image-to-video prompts generated or evaluated

If a task requires more items than these limits, it MUST be broken into multiple sequential or parallel LLM calls.
