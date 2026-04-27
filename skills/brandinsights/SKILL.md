---
name: brandinsights
description: >-
  A robust, agentic insights orchestrator for CPG, B2B, or any brand/industry/product launch. Mines consumer insights, brand history, competitive benchmarks, and social trends using 10+ deep research calls, 5 Opus 4.7 planning calls, 5 Gemini 3.1 Pro breadth calls, 3 GPT-5.5 Thinking deduplication calls (alias: gpt-5.5-high), and 2 GPT-5.5 Pro Extended Thinking validation calls (alias: gpt-5.5-pro, reasoning=xhigh). Enforces MANDATORY 1-hour ChatGPT Deep Research wait loop, internal consistency checks before deck generation, and dual audits (Opus formatting + ChatGPT fact-check) after deck generation. Produces four deliverables: raw research markdown, de-duplicated insights markdown, Excel source sheet with hallucination risk column, and a 20-30 page PowerPoint deck.
---

# Brand Insights

A highly structured, multi-model orchestrator that generates deep consumer insights, competitive benchmarks, and social trends for any brand. Combines redundant research architecture with rigorous consistency checking, mandatory wait loops, and dual-audit deck validation.

**Designed runtime: up to 2 hours.** Do not rush.

---

## 🚨 Non-Negotiable Rules

### 1. Model Call Quotas (HARD MINIMUMS)
You MUST execute at least:
- **10 Deep Research Calls** (split across Gemini, ChatGPT, and Claude)
- **5 Opus 4.7 Calls** (brand identity, competitor mapping, prompt generation)
- **5 Gemini 3.1 Pro Calls** (social platform summarization)
- **3 GPT-5.5 Thinking Calls** (deduplication) — alias: `gpt-5.5-high`, reasoning=high
- **2 GPT-5.5 Pro Extended Thinking Calls** (validation and deck outlining) — alias: `gpt-5.5-pro`, reasoning=xhigh

### 2. ChatGPT Deep Research is MANDATORY
ChatGPT Deep Research via browser extension is **required, not optional**. You MUST:
- Launch ChatGPT Deep Research in Phase 1
- Follow the 5-minute check-in cadence
- Wait up to **60 minutes** for completion
- If not complete at 60 minutes, set a **1-hour timer** using `schedule` tool
- **DO NOT proceed to final deliverables until ChatGPT is harvested**

### 3. Social Mining Timer (60 Minutes)
You MUST spend minimum **60 minutes** actively mining social media. Use `scripts/timer_logic.py` to enforce. Do NOT proceed to Phase 2 until timer confirms 60 minutes elapsed.

### 4. Recency Protocol (Current Date Reference)
Every quantitative claim MUST carry a `(Source, Month YYYY)` inline citation. Flag any data older than 6 months as STALE and explicitly caveat it. Prioritize most recent earnings calls and data.

### 5. Overall Runtime: 2 Hours
This skill is designed for up to **2 hours**. ChatGPT Deep Research can take an hour. Let it run while completing social mining. Do not prematurely collapse research streams.

### 6. Deduplication is Mandatory
The 10+ deep research calls produce massive overlapping data. You MUST use the 3 GPT-5.5 Thinking calls (`gpt-5.5-high`, reasoning=high) to de-duplicate before producing `insights.md`.

### 7. Raw Research Section Required
Every research file MUST include a `## Raw Research` section with:
- Unedited source quotes (copy-pasted exactly)
- Source URLs
- Access timestamps

### 8. Parenthetical Citations Everywhere
Every quantitative claim in `insights.md` MUST have a citation: `(Source Name, Month YYYY)`

### 9. Internal Consistency Check Before Deck
Before generating the PowerPoint deck, you MUST run an internal consistency check on all product specs, prices, and market data.

### 10. Dual Audit After Deck Generation
After deck is generated, you MUST run:
- **Opus 4.7 PDF Formatting Audit** (per slide-production skill)
- **GPT-5.5 Pro Fact-Check Audit** (alias: `gpt-5.5-pro`, reasoning=xhigh, per slide-production skill)
- Fix all MAJOR_ISSUES, BLANK_BROKEN, LIKELY_HALLUCINATED, and CONTRADICTED items

### 11. Four Deliverables Required
You MUST produce all four:
1. `research.md` (raw research with source quotes)
2. `insights.md` (de-duplicated insights with citations)
3. `sources.xlsx` (with Hallucination Risk column)
4. PowerPoint deck (PPTX + PDF, 20-30 pages)

### 12. Brand-Native Formatting
The PowerPoint deck MUST use the brand's own colors, fonts, and visual identity when available.

---

## 🚨 MANDATORY: Raw Research Section Format

Every research output file MUST include:

```markdown
## Raw Research

### Source 1: [Source Name]
**URL:** https://example.com/article
**Accessed:** [Date, Time ET]
**Research Stream:** [Gemini/ChatGPT/Manus/Claude]

> "Exact quote from the source, copied verbatim without any editing or paraphrasing."

### Source 2: [Source Name]
**URL:** https://example.com/report
**Accessed:** [Date, Time ET]
**Research Stream:** [Gemini/ChatGPT/Manus/Claude]

> "Another exact quote from this source."
```

---

## 🚨 MANDATORY: Internal Consistency Check (Pre-Deck)

Before generating the PowerPoint deck, extract and verify all key metrics:

### Step 1: Create Product Spec Table

| Spec | Value | Source | Research File |
|------|-------|--------|---------------|
| Butterfat % | 85% | Product image | chatgpt_research.md |
| Butterfat % | 84% | Company website | manus_research.md |
| Price (8oz) | $4.29-4.99 | Retailer scan | gemini_research.md |
| Price (8oz) | $4.49 | Company website | manus_research.md |

### Step 2: Create Market Data Table

| Metric | Value | Source | Research File |
|--------|-------|--------|---------------|
| Total butter market | $5.9B | Nielsen | gemini_research.md |
| Premium segment | $2.0-2.35B | Mintel | chatgpt_research.md |
| Premium segment | $2.3B | Nielsen | manus_research.md |
| Premium CAGR | 10% | Nielsen | gemini_research.md |
| Premium CAGR | 8-14% | Mintel | chatgpt_research.md |

### Step 3: Flag and Resolve Contradictions

```markdown
## ⚠️ Pre-Deck Consistency Flags

### CRITICAL: Butterfat Percentage Contradiction
- Product image shows: 85%
- Company website states: 84%
- **Resolution:** Use 85% (matches physical product packaging)
- **Action:** Update all deck references to 85%

### MINOR: Price Range Variation
- Retailer scan: $4.29-4.99
- Company website: $4.49
- **Resolution:** Use range $4.29-4.99 (captures market variation)
- **Action:** Cite as "typically $4.29-4.99 at retail"

### ACCEPTABLE: Market Size Estimates
- Mintel: $2.0-2.35B
- Nielsen: $2.3B
- **Resolution:** Values are compatible
- **Action:** Use "$2.0-2.35B (Mintel, 2025)" in deck
```

### Step 4: Lock Values for Deck
Create a "Locked Values" reference that the deck MUST use consistently:

```markdown
## Locked Values for Deck Generation

| Metric | Locked Value | Citation |
|--------|--------------|----------|
| Butterfat % | 85% | (Product packaging, April 2026) |
| Retail price | $4.29-4.99/8oz | (Retailer scan, April 2026) |
| Premium market size | $2.0-2.35B | (Mintel, Q1 2026) |
| Premium CAGR | 8-14% | (Mintel, Q1 2026) |
| Total butter market | $5.9B | (Nielsen, Q4 2025) |
```

**The deck generator MUST reference this locked values table and use ONLY these figures.**

---

## 🚨 MANDATORY: Excel Source Sheet with Hallucination Risk

The `sources.xlsx` file MUST include these columns:

| Column | Description |
|--------|-------------|
| Claim | The specific claim or data point |
| Value | The number or statement |
| Source Name | Publication/organization name |
| Source URL | Direct link to source |
| Source Date | Publication date |
| Access Date | When you accessed it |
| Research Stream | Gemini/ChatGPT/Manus/Claude |
| Verification Status | Verified/Unverified/Contradicted |
| **Hallucination Risk** | Low/Medium/High/Critical |
| Notes | Any caveats or context |

### Hallucination Risk Scoring

| Risk Level | Criteria |
|------------|----------|
| **Low** | Direct quote from primary source with URL; independently verified |
| **Medium** | Secondary source; plausible but not independently verified |
| **High** | No URL available; single source only; unusual claim |
| **Critical** | Contradicts other sources; sounds like fabrication; government quote without official source |

**Examples of Critical Risk:**
- "HHS calls seed oils 'poison'" → No official HHS statement found
- "KitchenAid Color of the Year 2025" → Cannot verify announcement
- Any specific quote attributed to a government official without official source

---

## Workflow Phases

### Phase 0: Brand Identity Mapping (0-15 minutes)
**Model calls:** 2 Opus 4.7

1. Parse user request for brand name, category, and objectives
2. Use Opus 4.7 to map brand identity:
   - Brand history and heritage
   - Product portfolio
   - Current positioning
   - Known competitors
3. Use Opus 4.7 to generate research prompts for each stream
4. Create project folder with naming convention

### Phase 1: Parallel Deep Research (15-75 minutes)
**Model calls:** 10 Deep Research, 5 Gemini 3.1 Pro

#### 1.1 Launch Deep Research Streams
1. **Launch ChatGPT Deep Research** (MANDATORY via browser extension)
   - Save conversation URL immediately
   - Start 5-minute check-in cadence
2. **Launch Gemini Deep Research** with brand-specific queries
3. **Launch Claude Deep Research** if fourth stream requested
4. **Begin Manus independent research**

#### 1.2 Social Mining (60 minutes MANDATORY)
Start timer. Mine these platforms:
- TikTok (search brand name, category, competitors)
- Instagram (brand hashtags, competitor hashtags)
- Reddit (relevant subreddits, brand mentions)
- Twitter/X (brand mentions, category conversations)
- YouTube (product reviews, category content)

Use 5 Gemini 3.1 Pro calls to summarize findings per platform.

#### 1.3 ChatGPT Check-In Cadence
Every 5 minutes, check ChatGPT thread status. Log each check:

```markdown
## ChatGPT Check-In Log
| Check # | Time | Status | Notes |
|---------|------|--------|-------|
| 1 | 2:05 PM | In progress | Researching |
| 2 | 2:10 PM | In progress | ~30% complete |
...
```

If not complete at 60 minutes: set 1-hour timer, continue other work, but DO NOT finalize deliverables.

### Phase 2: Deduplication and Synthesis (75-100 minutes)
**Model calls:** 3 GPT-5.5 Thinking (`gpt-5.5-high`), 2 Opus 4.7

1. Harvest all research streams (ChatGPT MUST be harvested)
2. Compile raw research into `research.md` with `## Raw Research` sections
3. Use 3 GPT-5.5 Thinking calls (`gpt-5.5-high`, reasoning=high) to deduplicate:
   - Call 1: Dedupe market data and sizing
   - Call 2: Dedupe competitive intelligence
   - Call 3: Dedupe consumer insights and trends
4. Use 2 Opus 4.7 calls to structure insights
5. Run internal consistency check (see section above)
6. Produce `insights.md` with parenthetical citations
7. Produce `sources.xlsx` with Hallucination Risk column

### Phase 3: Deck Generation and Validation (100-120 minutes)
**Model calls:** 2 GPT-5.5 Pro (`gpt-5.5-pro`, reasoning=xhigh), 1 Opus 4.7

1. Use GPT-5.5 Pro (`gpt-5.5-pro`, reasoning=xhigh) to outline deck structure
2. Reference "Locked Values" table for all metrics
3. Generate 20-30 slide deck in Manus native slides canvas
4. Apply brand colors and visual identity
5. Ensure every slide meets visual standards (per slide-production skill)
6. Export PPTX and PDF

### Phase 4: Dual Audit and Fix Cycle (Post-Generation)

#### Audit 1: Opus 4.7 PDF Formatting Audit
Per slide-production skill:
1. Run Opus 4.7 audit on PDF
2. Fix all MAJOR_ISSUES and BLANK_BROKEN slides
3. Re-export PDF

#### Audit 2: ChatGPT 5.5 Fact-Check Audit
Per slide-production skill:
1. Run ChatGPT 5.5 Thinking audit on PDF
2. Fix all LIKELY_HALLUCINATED and CONTRADICTED claims
3. Verify all claims match "Locked Values" table
4. Re-export final PDF and PPTX

### Phase 5: Final Delivery

1. Save all four deliverables to Google Drive:
   - `research.md`
   - `insights.md`
   - `sources.xlsx`
   - `[Brand]_Insights_Deck.pptx`
   - `[Brand]_Insights_Deck.pdf`
2. Include audit summaries in delivery message
3. Flag any unresolved issues or caveats

---

## File Naming Convention

```
brandinsights_[brand-name]_[YYYYMMDD]_[HHMM]ET/
├── research.md
├── insights.md
├── sources.xlsx
├── consistency_check.md
├── [Brand]_Insights_Deck.pptx
├── [Brand]_Insights_Deck.pdf
├── audits/
│   ├── opus_formatting_audit.md
│   └── chatgpt_factcheck_audit.md
└── raw/
    ├── gemini_raw_[timestamp].md
    ├── chatgpt_raw_[timestamp].md
    ├── manus_raw_[timestamp].md
    └── social_mining_[timestamp].md
```

---

## Quality Checklist (Pre-Delivery)

### Research Quality
- [ ] ChatGPT Deep Research harvested (waited up to 60 min + timer if needed)
- [ ] Gemini Deep Research harvested
- [ ] Manus research complete
- [ ] Social mining completed (60 min minimum)
- [ ] All raw research files have `## Raw Research` sections
- [ ] All quantitative claims have (Source, Month YYYY) citations

### Consistency Quality
- [ ] Internal consistency check completed
- [ ] All contradictions flagged and resolved
- [ ] "Locked Values" table created
- [ ] Deck uses only locked values

### Deck Quality
- [ ] 20-30 slides generated
- [ ] Brand colors applied
- [ ] Opus 4.7 formatting audit completed
- [ ] All MAJOR_ISSUES fixed
- [ ] ChatGPT 5.5 fact-check audit completed
- [ ] All LIKELY_HALLUCINATED claims removed/fixed
- [ ] All CONTRADICTED claims resolved

### Deliverables
- [ ] research.md saved
- [ ] insights.md saved
- [ ] sources.xlsx saved (with Hallucination Risk column)
- [ ] PPTX exported and saved
- [ ] PDF exported and saved
- [ ] All files in Google Drive

---

## Error Recovery

### ChatGPT Never Completes
1. Wait 60 minutes with check-ins
2. Set 1-hour timer
3. After timer, harvest whatever is available
4. Note in deliverables: "ChatGPT research incomplete; partial results included"
5. Increase Hallucination Risk scores for claims from other sources only

### Consistency Check Finds Critical Contradictions
1. Do not proceed to deck generation
2. Flag contradictions to user
3. Request clarification on correct values
4. Update "Locked Values" table with user-confirmed values
5. Then proceed to deck generation

### Audit Finds Hallucinations in Deck
1. Trace claim back to source in `sources.xlsx`
2. If source is valid, fix citation in deck
3. If source is fabricated, remove claim entirely
4. Update Hallucination Risk to "Critical" in sources.xlsx
5. Re-run fact-check audit after fixes

---

## Prompt Templates

### ChatGPT Deep Research Launch Prompt
```
I need comprehensive research on [BRAND NAME] in the [CATEGORY] market.

Please research:
1. Brand history, founding story, and heritage
2. Current product portfolio and key SKUs
3. Pricing and distribution channels
4. Competitive landscape (key competitors, positioning)
5. Consumer perception and reviews
6. Recent news, earnings, and market developments
7. Social media presence and sentiment
8. Market size and growth trends for the category

Focus on data from the past 12 months. Cite all sources with URLs.
```

### Opus 4.7 Brand Identity Prompt
```
Analyze this brand for a comprehensive insights deck:

Brand: [NAME]
Category: [CATEGORY]
Known products: [LIST]

Map:
1. Brand positioning (premium/value/mainstream)
2. Key differentiators
3. Target consumer profile
4. Competitive set (3-5 key competitors)
5. Brand voice and personality

Output a structured brand identity brief.
```

### Consistency Check Prompt
```
Review these research findings for internal consistency.

Extract every quantitative claim and create a comparison table.
Flag any contradictions between sources.
Recommend which value to use and why.

Research files:
[PASTE RELEVANT SECTIONS]
```