---
name: deep-research
description: Orchestrate a three-pronged research workflow for comprehensive reports. Use when the user asks for deep research, deepdeep research, multiple research agents, or a best-of synthesis across Gemini, ChatGPT, and Manus. This skill launches Gemini and ChatGPT deep research, enforces MANDATORY 60-minute ChatGPT wait with 5-minute check-ins, preserves all raw research files with standardized names, runs internal consistency checks, and synthesizes findings with full citations. Optionally includes Claude.ai browser extension as a fourth stream.
---

# Deep Research

Run a deliberately redundant, three-pronged research workflow combining **Gemini Deep Research**, **ChatGPT Deep Research**, and **Manus independent research**. The redundancy is intentional—capture different research paths, then synthesize the strongest final answer with rigorous citation and consistency checking.

Optional **fourth stream — Claude.ai Research (Anthropic)** — can be activated on user request.

---

## 🚨 Non-Negotiable Rules

### 1. Launch Parallel Research Early
Launch Gemini and ChatGPT deep research immediately so they run in parallel with Manus research.

### 2. ChatGPT 60-Minute Wait is MANDATORY
**ChatGPT Pro Deep Research can take up to 60 minutes.** This is normal. The moment ChatGPT Deep Research is initiated:
- Start a **5-minute check-in cadence**
- Continue checking until report completes OR **60 minutes elapse**
- **DO NOT deliver final synthesis until ChatGPT is harvested**

### 3. 1-Hour Timer if ChatGPT Exceeds 60 Minutes
If ChatGPT Deep Research has not completed by the 60-minute mark:
1. Use the `schedule` tool to create a **one-time timer for 3600 seconds** (1 hour)
2. Set `repeat: false`
3. The timer MUST trigger a return to the ChatGPT thread
4. **DO NOT silently abandon the thread**
5. **DO NOT deliver final synthesis until this timer fires and ChatGPT is harvested**

### 4. Do Not Block After 20 Minutes
After 20 minutes, you may draft outlines, build interim synthesis, and prepare other deliverables. But:
- Keep 5-minute ChatGPT checks active
- Do not finalize or deliver until ChatGPT is harvested

### 5. Final ChatGPT Harvest is Mandatory
Before ANY final delivery, return to the ChatGPT thread one last time. ChatGPT Deep Research must be checked as a final step and must not be silently skipped.

### 6. Preserve All Raw Research Files
Save raw outputs from all sources (Manus, Gemini, ChatGPT, Claude if used) plus final synthesis.

### 7. Eastern Time Naming Convention
Name every saved file with Eastern Time metadata:
```
[project]_[source]_[YYYYMMDD]_[HHMM]ET.[ext]
```
Example: `butter-market_chatgpt-deep_20260427_1430ET.md`

### 8. Save ChatGPT URL Immediately
Once the `/c/<conversation_id>` thread exists, save the direct URL. Reopen that exact URL during later checks.

### 9. Start Reminder Sidecar Immediately
After tracker initialization, start the reminder sidecar so the next due check is continuously surfaced.

### 10. Redundant Model Usage is Intentional
Gemini and ChatGPT Pro may surface different sources and perspectives. Do not collapse them prematurely.

---

## 🚨 MANDATORY: Raw Research Section

Every research output file MUST include a `## Raw Research` section containing:

1. **Unedited source quotes** (copy-pasted exactly as found)
2. **Source URLs** for every quote
3. **Access timestamps** (when the source was retrieved)

**Format:**
```markdown
## Raw Research

### Source 1: [Source Name]
**URL:** https://example.com/article
**Accessed:** April 27, 2026, 2:30 PM ET

> "Exact quote from the source, copied verbatim without any editing or paraphrasing. Include full context."

### Source 2: [Source Name]
**URL:** https://example.com/report
**Accessed:** April 27, 2026, 2:45 PM ET

> "Another exact quote from this source."
```

**Why this matters:** Raw research sections provide audit trails, enable fact-checking, and prevent hallucination by preserving original source language.

---

## 🚨 MANDATORY: Parenthetical Citations

Every quantitative claim in any research output MUST have a parenthetical citation in this format:

```
(Source Name, Month YYYY)
```

**Examples:**
- The premium butter market is valued at $2.3B (Nielsen, Q4 2025)
- Irish butter imports fell 39% year-over-year (USDA Trade Data, March 2026)
- 42% of consumers bake from scratch twice monthly (Mintel, January 2026)

**Rules:**
- Use the most specific date available (Q4 2025 > 2025 > "recent")
- If exact date unknown, use "accessed April 2026"
- If source is a company report, use company name: (Kerrygold Annual Report, 2025)
- If source is a news article, use publication: (Wall Street Journal, March 2026)

**No orphan numbers:** Any percentage, dollar amount, or growth rate without a citation is a quality failure.

---

## 🚨 MANDATORY: Internal Consistency Check

Before delivering any final synthesis, run an internal consistency check:

### Step 1: Extract All Quantitative Claims
Create a table of every number mentioned across all research sources:

| Metric | Value | Source | Section |
|--------|-------|--------|---------|
| Premium butter market size | $2.3B | Nielsen | Gemini research |
| Premium butter market size | $2.0-2.35B | Mintel | ChatGPT research |
| Butterfat % (Red Barn) | 84% | Company website | Manus research |
| Butterfat % (Red Barn) | 85% | Product image | ChatGPT research |

### Step 2: Flag Contradictions
Any metric with conflicting values across sources MUST be flagged:

```markdown
## ⚠️ Internal Consistency Flags

### CONTRADICTION: Red Barn Butterfat Percentage
- Source A (Company website): 84%
- Source B (Product image): 85%
- **Resolution needed:** Verify against physical product or official spec sheet
- **Recommendation:** Use 85% (matches product packaging) and note discrepancy

### DISCREPANCY: Premium Butter Market Size
- Source A (Nielsen): $2.3B
- Source B (Mintel): $2.0-2.35B
- **Resolution:** Values are compatible (Mintel range includes Nielsen point estimate)
- **Recommendation:** Use "$2.0-2.35B (Mintel, 2025; Nielsen estimates $2.3B)"
```

### Step 3: Resolve Before Delivery
- **Hard contradictions** (e.g., 84% vs 85%): Must be resolved or explicitly flagged to user
- **Soft discrepancies** (e.g., $2.3B vs $2.0-2.35B): Note both sources, use range
- **Unresolvable conflicts:** Flag prominently in final synthesis with recommendation

---

## Research Workflow

### Phase 0: Initialization (0-5 minutes)
1. Parse user request for topic, scope, and deliverables
2. Create project folder with naming convention
3. Initialize ChatGPT check-in tracker
4. Start reminder sidecar

### Phase 1: Launch Parallel Research (5-15 minutes)
1. **Launch Gemini Deep Research** with detailed query
2. **Launch ChatGPT Deep Research** via browser extension
3. Save ChatGPT conversation URL immediately
4. **Begin Manus independent research** using web search and browsing

### Phase 2: Active Research (15-60 minutes)
1. Continue Manus research while waiting
2. Check ChatGPT every 5 minutes (log each check)
3. Harvest Gemini results when ready
4. Build interim findings document

### Phase 3: Harvest and Compile (60-90 minutes)
1. Final ChatGPT harvest (mandatory)
2. If ChatGPT not ready at 60 min, set 1-hour timer and continue
3. Compile all raw research into `## Raw Research` sections
4. Add parenthetical citations to all claims

### Phase 4: Consistency Check and Synthesis (90-120 minutes)
1. Run internal consistency check (extract metrics, flag contradictions)
2. Resolve or flag all contradictions
3. Synthesize findings across all sources
4. Produce final deliverable with citations

---

## File Naming Convention

```
[project]_[type]_[YYYYMMDD]_[HHMM]ET.[ext]
```

| File Type | Naming Example |
|-----------|----------------|
| Gemini raw research | `butter_gemini-raw_20260427_1430ET.md` |
| ChatGPT raw research | `butter_chatgpt-raw_20260427_1530ET.md` |
| Manus raw research | `butter_manus-raw_20260427_1400ET.md` |
| Final synthesis | `butter_synthesis_20260427_1600ET.md` |
| Consistency check | `butter_consistency-check_20260427_1545ET.md` |

---

## ChatGPT Check-In Log Format

Maintain a running log:

```markdown
## ChatGPT Deep Research Check-In Log

| Check # | Time (ET) | Status | Notes |
|---------|-----------|--------|-------|
| 1 | 2:05 PM | In progress | Query submitted, researching |
| 2 | 2:10 PM | In progress | Still researching |
| 3 | 2:15 PM | In progress | ~40% complete indicator |
...
| 12 | 3:00 PM | In progress | 60 min elapsed, setting 1-hour timer |
| 13 | 4:00 PM | Complete | Harvested final report |
```

---

## Deliverable Structure

Every deep research output MUST include:

```markdown
# [Topic] Deep Research Report

**Generated:** [Date, Time ET]
**Sources:** Gemini Deep Research, ChatGPT Deep Research, Manus Web Research

## Executive Summary
[Key findings with citations]

## Detailed Findings
[Organized by theme, every claim cited]

## Internal Consistency Check
[Metrics table, contradictions flagged, resolutions noted]

## Raw Research

### Gemini Deep Research Raw Output
[Unedited Gemini output with source URLs]

### ChatGPT Deep Research Raw Output
[Unedited ChatGPT output with source URLs]

### Manus Research Raw Output
[Unedited web research with source URLs]

## Sources
[Full bibliography with URLs and access dates]
```

---

## Error Recovery

### ChatGPT Never Completes
1. Wait full 60 minutes with check-ins
2. Set 1-hour timer
3. After timer fires, harvest whatever is available
4. Note in final report: "ChatGPT research incomplete after 2 hours; partial results included"

### Gemini Fails
1. Retry once
2. If still failing, proceed with ChatGPT and Manus only
3. Note in final report: "Gemini research unavailable"

### Contradictions Cannot Be Resolved
1. Present both values with sources
2. Flag prominently for user decision
3. Recommend which value to use and why

---

## Quality Checklist (Pre-Delivery)

- [ ] ChatGPT Deep Research harvested (or timer fired and partial harvested)
- [ ] Gemini Deep Research harvested
- [ ] Manus research complete
- [ ] All files saved with ET naming convention
- [ ] `## Raw Research` section included with source quotes and URLs
- [ ] Every quantitative claim has (Source, Month YYYY) citation
- [ ] Internal consistency check completed
- [ ] All contradictions flagged or resolved
- [ ] Final synthesis includes all sources
- [ ] Check-in log documented