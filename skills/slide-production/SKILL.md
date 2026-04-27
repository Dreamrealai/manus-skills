---
name: slide-production
description: Create, revise, export, and reconstruct presentation slides and decks. Use whenever the user says slides, slide deck, deck, powerpoint, PowerPoint, presentation, pitch deck, keynote, PPT, or PPTX, or asks to make, edit, fix, export, recreate, or review a deck. Treat these requests as slide-production work by default. Always create the final deck in Manus native slides canvas first, then export both PPTX and PDF, review the PDF, run mandatory dual audits (Opus 4.7 formatting + ChatGPT 5.5 fact-check), fix all critical issues, and save the deliverables to Google Drive.
---

# Slide Production

Use this skill for all presentation work. The mandatory workflow is: **native Manus slides canvas first** → **export both PPTX and PDF** → **Opus 4.7 PDF formatting audit** → **fix all MAJOR_ISSUES and BLANK_BROKEN slides** → **ChatGPT 5.5 Thinking fact-check audit** → **fix all LIKELY_HALLUCINATED and CONTRADICTED claims** → **re-export if fixes were made** → **save final deliverables to Google Drive**.

---

## Workflow Decision Table

| Situation | Required workflow |
|---|---|
| New presentation request | Follow creation workflow → dual audit → fix cycle |
| Edits to existing deck | Follow revision workflow → dual audit → fix cycle |
| Uploaded deck reconstruction | Follow reconstruction workflow → represent in Manus canvas → dual audit → fix cycle |
| Export/handoff only | Ensure deck is in Manus canvas → export → dual audit → fix cycle → save to Drive |

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
| Data / Market slides | Chart (bar, line, pie, bubble) with 12px+ labels |
| Persona / Consumer slides | Human imagery (photo, illustration, or avatar) |
| Framework / Strategy slides | Diagram (2x2 matrix, flowchart, pyramid, or process) |
| Competitive slides | Positioning matrix OR comparison table with logos |
| Timeline / History slides | Visual timeline with dates and milestones |
| Title slides | Hero image, brand logo, or brand imagery |
| Executive Summary | 2-3 key metrics with icons; pull-quote or highlight box |

---

## 🚨 MANDATORY DUAL AUDIT SYSTEM

After every deck is generated (new, revised, or reconstructed), you MUST run two sequential audits before delivery.

### Audit 1: Opus 4.7 PDF Formatting Audit

**Trigger:** Immediately after PDF export is complete.

**Method:**
1. Upload the PDF to the conversation or use the PDF URL
2. Call Claude Opus 4.7 (claude-opus-4-5-20250514) with the following prompt structure:

```
You are a senior presentation designer auditing this PDF deck for formatting, visual design, and slide composition issues.

For EVERY slide, produce a JSON object with these fields:
- slide_number (integer)
- slide_title (string)
- status: one of [PASS, MINOR_ISSUES, MAJOR_ISSUES, BLANK_BROKEN]
- formatting_issues: array of specific issues (font sizes, spacing, alignment, margins)
- visual_issues: array of specific issues (missing charts, no images, text-wall, no brand colors)
- content_issues: array of specific issues (missing data, unclear hierarchy, no citations)
- blank_or_broken: boolean
- priority_fix: single most important fix for this slide
- overall_grade: A/B/C/D/F

Apply these standards:
- Body text minimum 16px, titles minimum 28px, chart labels minimum 12px
- Maximum 60% text density per slide
- Every slide needs at least 1 visual element
- 40px margins on all sides
- Data slides MUST have charts
- Persona slides MUST have images
- Framework slides MUST have diagrams

Output a JSON array of all slide audits, then a summary table.
```

**Required Output Format:**
```
## Opus 4.7 Formatting Audit Results

| Slide | Title | Status | Grade | Priority Fix |
|-------|-------|--------|-------|--------------|
| 1 | Title Slide | MINOR_ISSUES | C | Add hero image |
| 2 | Executive Summary | MAJOR_ISSUES | D | Increase body text to 16px, add metrics with icons |
...

### Critical Issues Requiring Immediate Fix:
- Slide 2: [specific issue]
- Slide 5: [specific issue]
```

### Audit 1 Fix Cycle

**Mandatory:** After Opus audit, you MUST fix:
1. ALL slides marked **BLANK_BROKEN** (rebuild entirely)
2. ALL slides marked **MAJOR_ISSUES** (address every formatting_issue and visual_issue)
3. Any slide graded **D or F**

**Fix Process:**
1. Return to Manus native slides canvas
2. Apply fixes slide-by-slide
3. Re-export PDF after fixes
4. Document fixes made in a brief changelog

### Audit 2: ChatGPT 5.5 Thinking Fact-Check Audit

**Trigger:** After Opus audit fixes are complete and PDF is re-exported.

**Method:**
1. Use OpenRouter to call ChatGPT 5.5 Thinking (or ChatGPT-4o with extended thinking)
2. Provide the PDF URL or upload
3. Use this prompt structure:

```
You are a senior fact-checker auditing this presentation deck for factual accuracy, hallucinations, and citation quality. Focus on CONTENT accuracy, not formatting.

For EVERY slide with factual claims, produce a JSON object with:
- slide_number (integer)
- slide_title (string)
- factual_status: one of [VERIFIED, UNVERIFIED, LIKELY_HALLUCINATED, CONTRADICTED]
- suspicious_claims: array of specific claims that need verification
- missing_citations: array of claims lacking (Source, Year) citations
- hallucination_flags: array of claims that appear fabricated or misattributed
- internal_contradictions: array of claims that contradict other slides in this deck
- confidence_score: 0-100
- recommended_fix: specific action to resolve issues

Flag these as HIGH RISK:
- Government agency quotes (verify exact wording)
- Specific percentages without sources
- Future predictions stated as fact
- Brand/product claims that contradict visible imagery
- Market sizes or growth rates without citations

Output a JSON array of all slide audits, then a summary of hallucination risks.
```

**Required Output Format:**
```
## ChatGPT 5.5 Fact-Check Audit Results

| Slide | Title | Factual Status | Confidence | Key Issue |
|-------|-------|----------------|------------|-----------|
| 3 | Opportunity | CONTRADICTED | 40 | Butterfat % contradicts product image |
| 5 | Market Trends | LIKELY_HALLUCINATED | 20 | "HHS calls them poison" unverified |
...

### Hallucination Flags (Must Fix Before Delivery):
- Slide 3: Butterfat stated as 84% but image shows 85%
- Slide 5: HHS quote appears fabricated
...

### Missing Citations (Must Add):
- Slide 4: Premium segment size needs source
- Slide 6: Import data needs source
```

### Audit 2 Fix Cycle

**Mandatory:** After ChatGPT fact-check audit, you MUST:
1. **Remove or correct** ALL claims marked **LIKELY_HALLUCINATED**
2. **Resolve** ALL claims marked **CONTRADICTED** (determine correct value, fix all instances)
3. **Add citations** for ALL claims marked in missing_citations
4. **Flag as "Unverified"** any claim that cannot be sourced but is retained

**Fix Process:**
1. Return to Manus native slides canvas
2. Correct factual errors, add citations, remove hallucinations
3. Re-export PDF after fixes
4. Document all factual corrections in changelog

### Final Export (Post-Audit)

After both audit fix cycles are complete:
1. Export final PPTX
2. Export final PDF
3. Save both to Google Drive
4. Include audit summary in delivery message to user

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

### Phase 2: Building
1. Create all slides in Manus native slides canvas
2. Apply visual standards (fonts, margins, density)
3. Ensure every slide has required visual elements per type
4. Add citations to all quantitative claims

### Phase 3: Export
1. Export PPTX
2. Export PDF

### Phase 4: Dual Audit
1. Run Opus 4.7 formatting audit on PDF
2. Fix all MAJOR_ISSUES and BLANK_BROKEN slides
3. Re-export PDF
4. Run ChatGPT 5.5 fact-check audit on PDF
5. Fix all LIKELY_HALLUCINATED and CONTRADICTED claims
6. Re-export final PDF and PPTX

### Phase 5: Delivery
1. Save final PPTX and PDF to Google Drive
2. Share audit summary with user
3. Note any unresolved issues or caveats

---

## Revision Workflow

When user requests edits to an existing deck:
1. Apply requested changes in Manus native slides canvas
2. Re-export PPTX and PDF
3. Run dual audit system (Opus formatting + ChatGPT fact-check)
4. Complete fix cycles
5. Save to Google Drive

---

## Reconstruction Workflow

When user uploads a PPTX or PDF to recreate:
1. Analyze uploaded file for structure, content, and styling
2. Recreate in Manus native slides canvas with improvements
3. Apply visual standards
4. Export PPTX and PDF
5. Run dual audit system
6. Complete fix cycles
7. Save to Google Drive

---

## Quality Checklist (Pre-Delivery)

Before marking any deck complete, verify:

- [ ] All slides in Manus native canvas
- [ ] PPTX exported
- [ ] PDF exported
- [ ] Opus 4.7 audit completed
- [ ] All MAJOR_ISSUES fixed
- [ ] ChatGPT 5.5 audit completed
- [ ] All LIKELY_HALLUCINATED claims removed/fixed
- [ ] All CONTRADICTED claims resolved
- [ ] Body text ≥ 16px throughout
- [ ] Titles ≥ 28px throughout
- [ ] Every slide has ≥ 1 visual element
- [ ] Text density ≤ 60% on all slides
- [ ] Margins consistent at 40px
- [ ] Brand colors present on every slide
- [ ] All quantitative claims have (Source, Year) citations
- [ ] Files saved to Google Drive

---

## Audit Prompt Templates

### Opus 4.7 Formatting Audit Prompt
See full prompt in Audit 1 section above. Save as reference: `opus_formatting_audit_prompt.md`

### ChatGPT 5.5 Fact-Check Audit Prompt
See full prompt in Audit 2 section above. Save as reference: `chatgpt_factcheck_audit_prompt.md`

---

## Error Recovery

### If Opus audit fails to run:
1. Retry with PDF URL
2. If still failing, manually review PDF against visual standards checklist
3. Document that automated audit was unavailable

### If ChatGPT audit fails to run:
1. Retry via OpenRouter
2. If still failing, manually review all quantitative claims for citations
3. Flag deck as "Fact-check audit incomplete" in delivery

### If fix cycle creates new issues:
1. Re-run relevant audit after fixes
2. Iterate until no MAJOR_ISSUES or LIKELY_HALLUCINATED remain
3. Maximum 3 fix cycles before escalating to user