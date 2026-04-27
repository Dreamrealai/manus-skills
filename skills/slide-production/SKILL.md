---
name: slide-production
description: Create, revise, export, and reconstruct presentation slides and decks. Use whenever the user says slides, slide deck, deck, powerpoint, PowerPoint, presentation, pitch deck, keynote, PPT, or PPTX, or asks to make, edit, fix, export, recreate, or review a deck. Treat these requests as slide-production work by default. Always create the final deck in Manus native slides canvas first, then export both PPTX and PDF, run mandatory dual audits (Opus 4.7 formatting + image enrichment → fix → GPT-5.5-pro fact-check + image/chart suggestions → fix), and save final deliverables to Google Drive. Both auditors receive the raw research context to suggest specific images and charts for Manus to execute.
---

# Slide Production

Use this skill for all presentation work. The mandatory workflow is:

**Build in Manus canvas** → **Export PDF** → **Opus 4.7 audit (formatting + image gaps + research-informed suggestions)** → **Manus fixes all MAJOR/BLANK issues + adds images/charts** → **Re-export PDF** → **GPT-5.5-pro audit (fact-check + hallucination + image/chart log)** → **Manus applies all factual fixes + additional enrichments** → **Final export PPTX + PDF** → **Save to Google Drive**

---

## Workflow Decision Table

| Situation | Required workflow |
|---|---|
| New presentation request | Build → dual audit → fix cycle → Drive |
| Edits to existing deck | Revise → dual audit → fix cycle → Drive |
| Uploaded deck reconstruction | Reconstruct in canvas → dual audit → fix cycle → Drive |
| Export/handoff only | Ensure in canvas → export → dual audit → fix cycle → Drive |

---

## Non-Negotiable Global Rules

### Trigger Rules
Any user mention of **slides**, **deck**, or **powerpoint** triggers this skill. Default to slide-production behavior unless the user is unmistakably asking for a definition or non-deliverable explanation.

### Working Surface
The final working deck MUST live in **Manus native slides canvas**. Do not treat standalone PPTX, browser-only HTML, or PDF as the primary working surface.

### Export Requirements
Every completed deck MUST be exported in **two formats**: **PPTX** and **PDF**. Both are mandatory. The PDF is the required review format for audits.

### Google Drive
Every completed deck MUST be saved to **Google Drive**. Read `gws-best-practices` before the first Google Workspace operation. Use user-specified folder, existing project folder, or `Manus_Work-in-progress_Donotshare` as fallback.

### Editable Text
All slide text MUST remain **editable**. Never flatten text into images.

### Punctuation
Default to **no terminal periods** in slide copy (titles, headers, bullets, labels, callouts). Use periods only for prose paragraphs, explicit user request, or formal citations.

### No Negative Offsets
Never use negative margins, negative top offsets, or container-level hacks to hide overflow. Redesign the composition instead.

---

## 🚨 MANDATORY VISUAL STANDARDS (Enforced in Every Audit)

### Font Size Minimums
| Element | Minimum Size |
|---|---|
| Slide titles | 28px |
| Section headers | 22px |
| Body text / bullets | 16px |
| Chart labels / legends | 12px |
| Footnotes / source lines | 10px |

### Visual Density Rules
- **Maximum 60% text coverage** per slide (excluding titles)
- **Minimum 1 visual element per slide**: chart, image, icon, diagram, or illustration
- **No text-wall slides**: Any slide exceeding 60% text MUST be split or visualized
- **Data slides MUST have a Chart.js or D3.js chart** — never a data slide with only text bullets

### Margin Standards
- **40px margins** on all four sides (top, bottom, left, right)
- Consistent across all slides in the deck
- Content must not touch slide edges

### Brand Color Enforcement
- Every slide MUST use at least one brand color (from user-provided palette or extracted from logo)
- Title bars, accent elements, or icons must carry brand identity
- No plain white backgrounds without brand accent elements

### Slide-Type Visual Requirements

| Slide Type | Required Visual Elements |
|---|---|
| Data / Market slides | Chart (bar, line, pie, bubble) with 12px+ labels + source line |
| Persona / Consumer slides | Human imagery (photo, illustration, or avatar) |
| Framework / Strategy slides | Diagram (2x2 matrix, flowchart, pyramid, or process flow) |
| Competitive slides | Positioning matrix OR comparison table with brand logos |
| Timeline / History slides | Visual timeline with dates and milestones |
| Title / Cover slides | Hero image, brand logo, or brand photography |
| Executive Summary | 2-3 key metrics with icons; pull-quote or highlight box |
| Quote / Insight slides | Large pull-quote with speaker attribution + supporting image |
| Section Dividers | Full-bleed brand image or bold typographic treatment |

### Image Enrichment Rules
- **Minimum 40% of slides** must include a photographic or illustrative image (not just charts or icons)
- Brand product photography MUST appear on at least 3 slides in any brand deck
- Lifestyle/contextual imagery (people using the product, relevant environments) MUST appear on consumer insight slides
- Competitive slides should include competitor brand logos or product imagery where available
- Images must be **high-resolution, watermark-free**, and **object-fit: contain** in their containers
- **Never use placeholder or stock imagery that contradicts brand identity**

---

## 🚨 MANDATORY DUAL AUDIT SYSTEM WITH RESEARCH CONTEXT

After every deck is generated, you MUST run two sequential audits. **Both auditors receive the raw research document** (aggregated_research.md, master_research_raw.md, or equivalent) so they can suggest specific images, charts, and data visualizations that Manus should then execute.

> **NON-NEGOTIABLE:** Do NOT deliver the deck to the user until BOTH audit rounds are complete and all MAJOR_ISSUES, BLANK_BROKEN, LIKELY_HALLUCINATED, and CONTRADICTED items are fixed.

---

### Audit 1: Opus 4.7 Formatting + Image Enrichment Audit

**Trigger:** Immediately after first PDF export.

**Preparation — Provide Research Context:**
Before running the Opus audit, prepare a `research_context_summary.md` file containing:
1. The top 20 key facts/statistics from the research (with sources)
2. The list of available brand images (file paths)
3. The list of available competitor images or logos
4. Any charts or data tables from the research that could be visualized

Pass this file alongside the PDF to Opus so it can suggest specific, executable improvements.

**Method:**
```bash
# Upload PDF to S3 for Opus vision access
PDF_URL=$(manus-upload-file /path/to/deck_v1.pdf | grep -o 'https://[^ ]*')

# Run Opus audit with research context
python3 /home/ubuntu/skills/openrouter/scripts/openrouter_chat.py \
  --alias opus \
  --prompt-file /path/to/opus_audit_prompt.txt \
  --output /path/to/opus_formatting_audit.md
```

**Opus Audit Prompt Template:**
```
You are a senior presentation designer and McKinsey deck quality reviewer. You are auditing a presentation PDF AND have access to the raw research document below.

RESEARCH CONTEXT:
[Insert research_context_summary.md content here — top facts, available images, data tables]

AVAILABLE BRAND IMAGES:
[List file paths of available images]

TASK: Audit this presentation slide by slide for formatting, visual design, and image enrichment opportunities.

For EVERY slide, evaluate and output a JSON object:
{
  "slide_number": int,
  "slide_title": string,
  "status": "PASS" | "MINOR_ISSUES" | "MAJOR_ISSUES" | "BLANK_BROKEN",
  "grade": "A" | "B" | "C" | "D" | "F",
  "formatting_issues": [list of specific issues],
  "visual_issues": [list of specific issues — missing charts, no images, text-wall],
  "font_violations": [list of elements below minimum size],
  "margin_violations": [list of margin issues],
  "brand_color_issues": [list of brand color problems],
  "image_opportunity": {
    "recommended": true/false,
    "type": "product_photo" | "lifestyle_photo" | "chart" | "diagram" | "competitor_logo" | "icon_set",
    "specific_suggestion": "Exact description of what image/chart to add and where",
    "data_to_visualize": "If chart: exact data points from research to use",
    "search_query": "If photo needed: exact search query to find the right image",
    "available_local_image": "If a local image from the available list fits, specify the path"
  },
  "priority_fix": "Single most important fix for this slide"
}

After the JSON array, provide:
- OVERALL_GRADE: A/B/C/D/F
- SYSTEMIC_ISSUES: Patterns on 3+ slides
- IMAGE_ENRICHMENT_PLAN: Ordered list of the top 10 image/chart additions that would most improve the deck
- ROOT_CAUSES: What caused the most common failures
```

**Required Output:** Save to `opus_formatting_audit.md`. Must include:
- Full JSON audit array
- Summary table (Slide | Title | Status | Grade | Priority Fix)
- IMAGE_ENRICHMENT_PLAN with specific, executable suggestions

---

### Audit 1 Fix Cycle — Manus Executes All Fixes

After receiving Opus audit, Manus MUST:

**Step A — Fix Structural Issues (Mandatory):**
1. Rebuild ALL slides marked `BLANK_BROKEN`
2. Fix ALL slides marked `MAJOR_ISSUES` (address every formatting_issue and visual_issue)
3. Fix ALL slides graded D or F
4. Enforce font minimums: body ≥ 16px, titles ≥ 28px, chart labels ≥ 12px
5. Fix all margin violations (40px on all sides)
6. Apply brand colors to any slides missing them

**Step B — Execute Image Enrichment Plan (Mandatory):**
For each item in Opus's IMAGE_ENRICHMENT_PLAN:
1. **If chart suggested:** Build the chart in Chart.js or D3.js using the exact data points specified. Add source line.
2. **If local image available:** Use the specified file path in the slide HTML with `object-fit: contain`.
3. **If search needed:** Run `search` tool with the exact query Opus provided. Download the best result. Embed in slide.
4. **If diagram suggested:** Build the diagram in HTML/CSS using brand colors.
5. Document each image/chart added in `image_enrichment_log.md`.

**Step C — Re-export:**
Re-export as `deck_v2.pdf` after all fixes.

---

### Audit 2: GPT-5.5-Pro Fact-Check + Image/Chart Suggestion Audit

**Trigger:** After Opus audit fixes are complete and v2 PDF is exported.

**Preparation — Provide Research Context:**
Pass the same `research_context_summary.md` plus the full `aggregated_research.md` (or equivalent) to GPT-5.5-pro so it can:
1. Cross-reference claims against the source research
2. Identify data points in the research that are NOT yet visualized in the deck
3. Suggest additional charts or images that would strengthen specific slides

**Method:**
```bash
python3 /home/ubuntu/skills/openrouter/scripts/openrouter_chat.py \
  --alias gpt-5.5-pro \
  --reasoning xhigh \
  --prompt-file /path/to/gpt55_factcheck_prompt.txt \
  --output /path/to/gpt55_factcheck_audit.md
```
**Fallback:** If `gpt-5.5-pro` fails, use `gpt-5.5-xhigh`. If that fails, use Gemini 3.1 Pro.

**GPT-5.5-Pro Audit Prompt Template:**
```
You are a senior fact-checker and data visualization strategist auditing a presentation deck. You have access to the raw research document that was used to build this deck.

RAW RESEARCH:
[Insert full aggregated_research.md content here]

AVAILABLE BRAND IMAGES:
[List file paths of available images]

TASK: Audit this deck for (1) factual accuracy and hallucinations, and (2) missed data visualization opportunities.

For EVERY slide with factual claims, output a JSON object:
{
  "slide_number": int,
  "slide_title": string,
  "factual_status": "VERIFIED" | "PLAUSIBLE" | "UNVERIFIED" | "LIKELY_HALLUCINATED" | "CONTRADICTED",
  "confidence_score": 0-100,
  "suspicious_claims": [list of claims needing verification],
  "hallucination_flags": [list of likely fabricated claims with explanation],
  "missing_citations": [list of claims needing (Source, Year) format],
  "internal_contradictions": [list of claims contradicting other slides],
  "research_data_unused": [list of data points from the research NOT yet in the deck that would strengthen this slide],
  "additional_image_opportunity": {
    "recommended": true/false,
    "specific_suggestion": "Exact description of image/chart to add",
    "data_source": "Which part of the research to use",
    "chart_type": "bar/line/pie/scatter/table/none",
    "search_query": "If photo: exact search query"
  },
  "recommended_fix": "Specific action to resolve all issues on this slide"
}

After the JSON array, provide:
- OVERALL_CONFIDENCE: 0-100
- VERIFIED_FACTS: Top 10 claims confirmed accurate
- HALLUCINATION_REPORT: Detailed explanation of any likely hallucinations
- CITATION_GAPS: Consolidated list of all missing citations
- UNUSED_RESEARCH_OPPORTUNITIES: Top 5 data points from the research not yet in the deck
- ADDITIONAL_IMAGE_LOG: Ordered list of additional images/charts to add (beyond what Opus already suggested)
```

**Required Output:** Save to `gpt55_factcheck_audit.md`. Must include:
- Full JSON audit array
- Summary table (Slide | Title | Factual Status | Confidence | Key Issue)
- ADDITIONAL_IMAGE_LOG with specific, executable suggestions

---

### Audit 2 Fix Cycle — Manus Executes All Fixes

After receiving GPT-5.5-pro audit, Manus MUST:

**Step A — Fix Factual Issues (Mandatory):**
1. Remove or correct ALL claims marked `LIKELY_HALLUCINATED`
2. Resolve ALL `CONTRADICTED` claims (determine correct value, fix ALL instances across deck)
3. Add `(Source, Year)` citations to ALL items in missing_citations
4. Tag retained unverifiable claims as `[Unverified]`

**Step B — Execute Additional Image/Chart Log (Mandatory):**
For each item in GPT-5.5-pro's ADDITIONAL_IMAGE_LOG:
1. **If chart:** Build in Chart.js/D3.js using the specified research data. Add source line.
2. **If photo:** Search with the exact query. Download best result. Embed in slide.
3. **If unused research data:** Add a new data callout, stat box, or chart to the relevant slide.
4. Append all additions to `image_enrichment_log.md`.

**Step C — Final Export:**
1. Export final PPTX: `{Project}_Final.pptx`
2. Export final PDF: `{Project}_Final.pdf`
3. Save both to Google Drive
4. Include audit summary in delivery message

---

## Image Enrichment Log Format

Maintain `image_enrichment_log.md` throughout both fix cycles:

```markdown
# Image Enrichment Log

## Round 1 (Opus 4.7 Suggestions)
| Slide | Type | Action Taken | Source/Path |
|-------|------|--------------|-------------|
| 3 | Chart | Added bar chart: US butter market growth 2020-2025 | Circana 2025 data from research |
| 7 | Product photo | Added Red Barn 85% butterfat product image | /path/to/product_main.png |
| 12 | Lifestyle photo | Added farm/pastoral image | Downloaded from search: "golden hour farm pastoral" |

## Round 2 (GPT-5.5-Pro Suggestions)
| Slide | Type | Action Taken | Source/Path |
|-------|------|--------------|-------------|
| 5 | Chart | Added Kerrygold vs Vital Farms market share pie chart | Ornua 2025 Annual Report |
| 18 | Competitor logos | Added Kerrygold, Vital Farms, Land O'Lakes logos | Downloaded from brand sites |
```

---

## Citation Standards for Slides

### Quantitative Claims
Every number, percentage, or market figure MUST have a parenthetical citation:
```
Premium butter market growing at 10% CAGR (Nielsen, Q4 2025)
```

### Source Line Format
Bottom of data slides should include:
```
Sources: Nielsen Retail Data Q4 2025; Mintel Butter Report Jan 2026
```

### Recency Requirements
- Flag any data older than 6 months as potentially stale
- Prefer Q1 2026 or Q4 2025 data for current decks
- If using older data, explicitly note: "(2024 data; 2025 update pending)"

---

## Slide Creation Workflow

### Phase 1: Planning
1. Confirm topic, audience, and purpose
2. Request or extract brand colors and logo
3. Outline slide structure (recommend 1 slide per key point)
4. Identify which slides need charts, images, or diagrams
5. **Prepare research_context_summary.md** with top facts, available images, and data tables

### Phase 2: Building
1. Create all slides in Manus native slides canvas
2. Apply visual standards (fonts, margins, density)
3. Ensure every slide has required visual elements per type
4. Add citations to all quantitative claims
5. Embed brand product images on at least 3 slides

### Phase 3: Export
1. Export PPTX
2. Export PDF (v1)

### Phase 4: Dual Audit + Fix Cycle
1. **Prepare research_context_summary.md** (if not already done)
2. Run Opus 4.7 formatting + image enrichment audit (with research context)
3. Fix all MAJOR_ISSUES and BLANK_BROKEN slides
4. Execute Opus IMAGE_ENRICHMENT_PLAN (add all suggested charts/images)
5. Re-export PDF (v2)
6. Run GPT-5.5-pro fact-check + additional image audit (with research context)
7. Fix all LIKELY_HALLUCINATED and CONTRADICTED claims
8. Execute GPT-5.5 ADDITIONAL_IMAGE_LOG (add remaining charts/images)
9. Re-export final PPTX and PDF

### Phase 5: Delivery
1. Save final PPTX and PDF to Google Drive
2. Share audit summary + image enrichment log with user
3. Note any unresolved issues or caveats

---

## Revision Workflow

When user requests edits to an existing deck:
1. Apply requested changes in Manus native slides canvas
2. Re-export PPTX and PDF
3. Run dual audit system (Opus formatting + GPT-5.5-pro fact-check), both with research context
4. Complete fix cycles including image enrichment
5. Save to Google Drive

---

## Reconstruction Workflow

When user uploads a PPTX or PDF to recreate:
1. Analyze uploaded file for structure, content, and styling
2. Recreate in Manus native slides canvas with improvements
3. Apply visual standards
4. Export PPTX and PDF
5. Run dual audit system with research context
6. Complete fix cycles including image enrichment
7. Save to Google Drive

---

## Quality Checklist (Pre-Delivery)

Before marking any deck complete, verify:

- [ ] All slides in Manus native canvas
- [ ] PPTX exported
- [ ] PDF exported (v1)
- [ ] `research_context_summary.md` prepared with top facts + available images
- [ ] Opus 4.7 audit completed (with research context passed)
- [ ] All BLANK_BROKEN slides rebuilt
- [ ] All MAJOR_ISSUES slides fixed
- [ ] Opus IMAGE_ENRICHMENT_PLAN fully executed (all suggested charts/images added)
- [ ] PDF re-exported (v2)
- [ ] GPT-5.5-pro audit completed (with full research context passed)
- [ ] All LIKELY_HALLUCINATED claims removed or corrected
- [ ] All CONTRADICTED claims resolved across all instances
- [ ] All missing citations added in (Source, Year) format
- [ ] GPT-5.5 ADDITIONAL_IMAGE_LOG fully executed
- [ ] `image_enrichment_log.md` complete with all additions documented
- [ ] Body text ≥ 16px throughout
- [ ] Titles ≥ 28px throughout
- [ ] Every slide has ≥ 1 visual element
- [ ] ≥ 40% of slides have photographic/illustrative images
- [ ] Brand product images on ≥ 3 slides
- [ ] Text density ≤ 60% on all slides
- [ ] Margins consistent at 40px
- [ ] Brand colors present on every slide
- [ ] All quantitative claims have (Source, Year) citations
- [ ] Final PPTX and PDF saved to Google Drive

---

## Error Recovery

### If Opus audit fails to run:
1. Retry with PDF URL via `manus-upload-file`
2. If still failing, manually review PDF against visual standards checklist
3. Document that automated audit was unavailable

### If GPT-5.5-pro audit fails to run:
1. Retry with `gpt-5.5-xhigh` alias
2. If that fails, use Gemini 3.1 Pro as emergency fallback
3. If all fail, manually review all quantitative claims for citations
4. Flag deck as "Fact-check audit incomplete" in delivery

### If fix cycle creates new issues:
1. Re-run relevant audit after fixes
2. Iterate until no MAJOR_ISSUES or LIKELY_HALLUCINATED remain
3. Maximum 3 fix cycles before escalating to user

### If image search returns no suitable results:
1. Try 2 alternative search queries
2. Use a brand-appropriate abstract or texture image as fallback
3. Build a data visualization instead if the slide has data
4. Never leave a slide with zero visual elements

---

## Manus Skill Update Procedure

When updating this skill or any other skill globally, follow this two-step process:

### Step 1: Update files on disk and push to GitHub
```bash
# 1. Edit the skill file(s)
# 2. Copy to the cloned manus-skills repo
cp /home/ubuntu/skills/<skill-name>/SKILL.md /home/ubuntu/manus-skills/skills/<skill-name>/SKILL.md
# 3. Commit and push
cd /home/ubuntu/manus-skills && git add -A && git commit -m "Update <skill-name>" && git push
```

### Step 2: Reload in Manus Settings via Browser (MANDATORY)
After pushing to GitHub, reload the skill in Manus settings:
1. Navigate to `https://manus.im/app#settings/skills` in the browser
2. Find the skill in the list (hover to reveal the **"..."** three-dot menu)
3. Click **"..."** → **"Replace"** to update in place, OR click **"Delete"** then **"+ Add Skill"** → **"Import from GitHub"**
4. Verify the skill appears with the updated description

**If the "..." menu does not appear:** Hover directly over the skill card — the menu appears on hover only.
