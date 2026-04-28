---
name: slide-production
description: Create, revise, export, and reconstruct presentation slides and decks. Use whenever the user says slides, slide deck, deck, powerpoint, PowerPoint, presentation, pitch deck, keynote, PPT, or PPTX, or asks to make, edit, fix, export, recreate, or review a deck. Primary slide production LLM is Opus 4.7 via OpenRouter (alias: opus-4.7). CRITICAL: Always upload all images to Google Drive as public URLs BEFORE building slides — Manus frequently drops local image paths when using OpenRouter API. Enforces strict density/layout/color rules, mandatory dual audit cycle (Opus 4.7 formatting → fix → GPT-5.5-pro fact-check → fix), and Google Drive delivery.
---

# Slide Production

Use this skill for all presentation work. The mandatory workflow is:

**Upload images to Google Drive (public URLs)** → **Build in Manus canvas** → **Export PDF** → **Opus 4.7 audit (formatting + image gaps + research-informed suggestions)** → **Manus fixes all MAJOR/BLANK issues** → **Re-export PDF** → **GPT-5.5-pro audit (fact-check + hallucination + image/chart log)** → **Manus applies all factual fixes** → **Final export PPTX + PDF** → **Save to Google Drive**

---

## 🚨 PRIMARY SLIDE PRODUCTION LLM: OPUS 4.7

**All slide HTML generation MUST use Opus 4.7 via OpenRouter** (alias: `opus-4.7`).

- Use `openrouter_chat.py --alias opus-4.7` for any programmatic slide generation
- Sonnet 4.6 (alias: `sonnet-4.6`) is the fallback if Opus is unavailable or times out
- **Never use GPT models for slide HTML generation** — they produce inconsistent HTML/CSS
- When using Manus native `slide_edit` tool, the tool itself handles LLM routing; no alias needed

---

## 🚨 CRITICAL: IMAGE PRESERVATION VIA GOOGLE DRIVE PUBLIC URLS

**This is the #1 failure mode in slide production.** When Opus 4.7 (or any OpenRouter model) generates slide HTML, it frequently drops or ignores local file paths for images. The result is slides with missing images or broken `<img>` tags.

### Mandatory Image Upload Workflow (BEFORE building any slides)

**Step 1: Collect all images**
```bash
# List all available brand/product images
ls /path/to/brand_assets/
ls /home/ubuntu/upload/search_images/
```

**Step 2: Upload ALL images to Google Drive and get public URLs**
```bash
# Upload each image using gws or manus-upload-file
manus-upload-file /path/to/image1.png  # Returns CDN URL
manus-upload-file /path/to/image2.jpg  # Returns CDN URL

# OR use gws to upload to a dedicated Images folder in the project Drive folder
gws drive files create --params '{"name": "product_main.png", "parents": ["FOLDER_ID"]}'
```

**Step 3: Build an image URL manifest**
Create `image_manifest.json` BEFORE building any slides:
```json
{
  "product_main": "https://files.manuscdn.com/...",
  "product_barn": "https://files.manuscdn.com/...",
  "kv_hero": "https://files.manuscdn.com/...",
  "competitor_kerrygold": "https://files.manuscdn.com/...",
  "farm_lifestyle": "https://files.manuscdn.com/..."
}
```

**Step 4: Reference ONLY public URLs in slide HTML**
```html
<!-- CORRECT — always use public URL -->
<img src="https://files.manuscdn.com/abc123.png" style="width: 300px; height: 200px; object-fit: contain;" />

<!-- WRONG — local paths get dropped by OpenRouter -->
<img src="/home/ubuntu/brand_assets/product_main.png" />
```

### When Using Manus Native `slide_edit` Tool
When using the Manus `slide_edit` tool (not OpenRouter API), local absolute paths ARE supported:
```html
<img src="/home/ubuntu/brandinsights_red-barn_20260427_1231/brand_assets/kv_rb_v11.png" style="width: 400px; height: 280px; object-fit: contain;" />
```
But still prefer public URLs for portability and to avoid path loss during export.

### Image Preservation Checklist
Before finalizing any slide:
- [ ] Every `<img>` tag uses a public CDN URL or verified absolute local path
- [ ] No `<img>` tags with relative paths (`./`, `../`)
- [ ] No `<img>` tags with placeholder `src` values
- [ ] All images have explicit `width` and `height` in pixels (not percentages)
- [ ] All images use `object-fit: contain` or `object-fit: cover` as appropriate

---

## 🚨 MANDATORY VISUAL QUALITY STANDARDS

These standards are enforced in EVERY audit. Violations are MAJOR_ISSUES.

### 1. Density & Word Count Rules
| Slide Type | Max Words (excl. title) | Max Bullet Points |
|---|---|---|
| Data / Market slide | 80 words | 5 bullets |
| Strategy / Framework | 100 words | 6 bullets |
| Persona / Consumer | 60 words | 4 bullets |
| Executive Summary | 120 words | 8 bullets |
| Section Divider | 20 words | 0 bullets |
| Cover / Title | 15 words | 0 bullets |

**Text-wall rule:** Any slide exceeding these limits MUST be split into two slides or converted to a visual (chart, diagram, table).

### 2. Font Size Minimums
| Element | Minimum Size |
|---|---|
| Slide titles | 28px |
| Section headers / H2 | 22px |
| Body text / bullets | 16px |
| Chart labels / axis text | 12px |
| Source / footnote lines | 10px |

**Never use 11px, 12px, or 13px for body text.** This is the most common failure mode.

### 3. Layout & Spacing Rules
- **40px minimum margins** on all four sides — content must NOT touch slide edges
- **Consistent margin across ALL slides** — never mix 20px and 40px margins in the same deck
- **No large empty white areas** — if a slide has >30% empty space on one side, redistribute content or add a visual
- **No blue dashed borders** (`border: 1px dashed #007bff`) — this is a website UI pattern, not a slide pattern
- **No card shadows** (`box-shadow`) on content containers
- **No rounded corners** (`border-radius`) on primary content containers
- **Full-width layouts** — use the entire 1280px width; never leave half the slide blank

### 4. Color Rules
- **Brand colors only** — use the provided brand palette exclusively; no random blues, greens, or greys
- **Background consistency** — all content slides MUST share the same background color/treatment
- **Accent color discipline** — use accent colors (gold, etc.) for 1-2 elements per slide maximum; never as body text color
- **Contrast requirement** — body text must have ≥ 4.5:1 contrast ratio against background
- **No white-on-white** — never place white text on a white or near-white background
- **No light grey text on white** — minimum body text color: `#333333` on white backgrounds

### 5. Visual Element Requirements
| Slide Type | Required Visual |
|---|---|
| Data / Market | Chart (Chart.js or D3.js) with source line |
| Persona / Consumer | Human photo or illustrated avatar |
| Framework / Strategy | Diagram (2×2, funnel, pyramid, process flow) |
| Competitive | Positioning matrix OR comparison table |
| Timeline | Visual timeline with dates |
| Cover | Full-bleed hero image or brand photography |
| Executive Summary | 2-3 stat callouts with icons |
| Section Divider | Full-bleed brand image or bold typographic treatment |
| Quote / Insight | Large pull-quote with attribution |

**Minimum image rule:** ≥ 40% of slides must include a photographic or illustrative image (not just icons or charts). Brand product photography must appear on ≥ 3 slides in any brand deck.

### 6. Layout Variety Rule
- **No two consecutive slides** may use the same layout structure
- Alternate between: full-width text+chart, split left/right, 3-column grid, hero image with overlay text, stat callout grid
- Section dividers and cover slides are exempt from this rule

### 7. Chart Quality Rules
- All charts use **Chart.js v3** (not v2 — no `horizontalBar` type)
- Wrap every `<canvas>` in a parent div with explicit pixel height: `<div style="height: 300px;"><canvas></canvas></div>`
- Every chart MUST have a **source line** below it: `Source: [Source Name], [Month YYYY]`
- Chart colors MUST use the brand palette (not Chart.js defaults)
- No radar charts — they are visually poor

---

## 🚨 MANDATORY DUAL AUDIT SYSTEM

After every deck is generated, run two sequential audits. **Both auditors receive the raw research document** so they can suggest specific images, charts, and data visualizations.

> **NON-NEGOTIABLE:** Do NOT deliver the deck until BOTH audit rounds are complete and ALL MAJOR_ISSUES, BLANK_BROKEN, LIKELY_HALLUCINATED, and CONTRADICTED items are fixed.

---

### Audit 1: Opus 4.7 Formatting + Image Enrichment Audit

**Trigger:** Immediately after first PDF export.

**Preparation:**
1. Upload PDF via `manus-upload-file` to get a public URL
2. Prepare `research_context_summary.md` with top 20 facts, available image URLs, and data tables
3. Pass both to Opus

**Method:**
```bash
PDF_URL=$(manus-upload-file /path/to/deck_v1.pdf | grep -o 'https://[^ ]*')

python3 /home/ubuntu/skills/openrouter/scripts/openrouter_chat.py \
  --alias opus-4.7 \
  --prompt "You are auditing a presentation. PDF URL: $PDF_URL. Research context: [paste research_context_summary.md]. For EVERY slide, provide: slide number, title, grade (A/B/C/D/F), status (PASS/MINOR_ISSUES/MAJOR_ISSUES/BLANK_BROKEN), list of formatting issues, list of visual issues, and a specific image/chart recommendation. After all slides, provide SYSTEMIC_ISSUES and IMAGE_ENRICHMENT_PLAN." \
  --output /path/to/opus_audit.md
```

**Required Output:** `opus_formatting_audit.md` with:
- Per-slide table: Slide | Title | Grade | Status | Top Issue
- IMAGE_ENRICHMENT_PLAN: ordered list of top 10 image/chart additions
- SYSTEMIC_ISSUES: patterns across 3+ slides

**Fix Cycle After Opus Audit:**
1. Rebuild ALL `BLANK_BROKEN` slides
2. Fix ALL `MAJOR_ISSUES` slides (address every formatting and visual issue)
3. Fix ALL slides graded D or F
4. Enforce font minimums, margin rules, density limits
5. Execute IMAGE_ENRICHMENT_PLAN: add all suggested charts/images
6. Re-export as `deck_v2.pdf`

---

### Audit 2: GPT-5.5-Pro Fact-Check + Additional Image Audit

**Trigger:** After Opus fixes and v2 PDF exported.

**Method:**
```bash
PDF_URL_V2=$(manus-upload-file /path/to/deck_v2.pdf | grep -o 'https://[^ ]*')

python3 /home/ubuntu/skills/openrouter/scripts/openrouter_chat.py \
  --alias gpt-5.5-pro \
  --reasoning xhigh \
  --prompt "Fact-check this presentation PDF ($PDF_URL_V2) against this research: [paste full research]. For every slide: factual_status (VERIFIED/PLAUSIBLE/UNVERIFIED/LIKELY_HALLUCINATED/CONTRADICTED), suspicious claims, missing citations, and additional image/chart opportunities not yet in the deck." \
  --output /path/to/gpt55_audit.md
```

**Fallback:** If `gpt-5.5-pro` fails → use `gpt-5.5-xhigh` → if that fails → use Gemini 3.1 Pro.

**Fix Cycle After GPT-5.5 Audit:**
1. Remove/correct ALL `LIKELY_HALLUCINATED` claims
2. Resolve ALL `CONTRADICTED` claims across entire deck
3. Add `(Source, Year)` citations to all flagged items
4. Execute ADDITIONAL_IMAGE_LOG: add remaining charts/images
5. Export final PPTX and PDF

---

## 🚨 MANDATORY LAYOUT VARIATION SYSTEM

Every deck MUST use at least 6 of these 8 named layout patterns. **No two consecutive slides may use the same pattern.** The pattern name must be noted in a comment at the top of each slide's HTML.

### Pattern 1: HERO-STAT — Giant Number Callout
```
Full-width background | 1-3 giant numbers (80-120px) centered | 1 sentence headline above | 2-line supporting context below
Example use: Market size, growth rate, key metric
Max words: 25 total
```

### Pattern 2: SPLIT-IMAGE — 50/50 Photo + Text
```
Left 50%: full-bleed photography (object-fit: cover, height: 720px)
Right 50%: white/cream background | Title 32px | 3-4 bullets at 16px | 40px padding
Max words on text side: 60
```

### Pattern 3: CHART-DOMINANT — Data Visualization
```
Title bar at top (60px tall) | Chart takes 65% of slide height | Source line at bottom
Right sidebar (25% width): 2-3 insight callouts in gold accent boxes
Max words outside chart: 40
```

### Pattern 4: THREE-COLUMN GRID — Comparison/Framework
```
3 equal columns with icon/number at top of each | Column title 20px bold | 2-3 lines body text 16px
No borders between columns — use background color alternation or spacing
Max words per column: 30
```

### Pattern 5: FULL-BLEED-OVERLAY — Section Divider / Impact Slide
```
Full-bleed photography or brand color | Semi-transparent dark overlay (rgba 0,0,0,0.5)
Centered text: 1 headline 48-64px white | 1 subline 24px white
Max words: 15
```

### Pattern 6: INSIGHT-QUOTE — Pull Quote
```
Large quotation mark graphic | Quote text 28-36px centered | Attribution 16px below
Left accent bar in brand color | Clean white background
Max words: 35
```

### Pattern 7: TABLE-MATRIX — Competitive/Comparison
```
Title at top | Full-width table with alternating row colors | Max 6 rows, 5 columns
Header row in brand primary color | Body text 14px minimum in table cells
No more than 8 words per cell
```

### Pattern 8: TIMELINE-PROCESS — Sequential Flow
```
Horizontal timeline bar spanning full width | 4-6 nodes with icons
Above/below alternating labels | Year/date prominent at 20px | Description 14px
Brand accent color for timeline bar
```

---

## 🚨 DENSITY RULES — WHAT "TOO DENSE" MEANS

These are the most common failures. Each is a MAJOR_ISSUE in the audit.

### ❌ WRONG — Text Wall (DO NOT DO THIS)
```
Slide title: "Consumer Purchase Drivers"
• Consumers increasingly seek premium, artisanal products with transparent sourcing and authentic brand stories
• Price sensitivity varies by income bracket with HHI >$100K showing 3.2x higher premium butter purchase intent  
• Health and wellness positioning drives purchase for 67% of premium butter buyers who cite grass-fed and high-fat content
• Social media influence, particularly TikTok "ButterTok" content, drives trial among 18-34 demographic
• Retail channel preference shifting toward specialty and natural grocery with Whole Foods and Sprouts outperforming
• Gifting occasion represents 18% of premium butter purchases with seasonal spikes in Q4
```
**Problem:** 6 bullets, 120+ words, no visual, no hierarchy, no breathing room.

### ✅ CORRECT — Focused Insight Slide
```
Slide title: "3 Reasons Shoppers Trade Up to Premium Butter"
[Large icon] HEALTH — "85% butterfat, grass-fed, no additives" (18px)
[Large icon] TASTE — "Richer flavor, higher smoke point" (18px)  
[Large icon] STORY — "Farmer-sourced, American-made" (18px)
[Bottom bar] Source: Mintel Premium Butter Report, Jan 2026
```
**Result:** 3 points, 30 words, clear visual hierarchy, instant comprehension.

### Hard Density Limits (ENFORCED IN AUDIT)
- **Maximum 5 bullet points per slide** — if you have 6+, split into two slides
- **Maximum 15 words per bullet** — if longer, it's a paragraph, not a bullet
- **Maximum 120 words total per content slide** (title excluded)
- **Minimum 35% of slide area must be non-text** (image, chart, whitespace, icon)
- **No paragraph blocks** — if text is more than 2 lines without a break, it's a paragraph and must be redesigned

---

## 🚨 COLOR SYSTEM — RED BARN BRAND (AND GENERAL RULES)

### For Red Barn Creamery Specifically
```
Background (content slides): #FAFAF5 (warm off-white/cream)
Background (cover + section dividers): #8B1A1A (barn red)
Primary text: #1A1A1A (near-black — NOT pure black)
Secondary text: #4A4A4A (dark grey)
Accent 1: #D4A017 (butter gold — for callouts, highlights, icons)
Accent 2: #8B1A1A (barn red — for headers, borders, chart bars)
Never use: pure white (#FFFFFF) as background — too sterile
Never use: #D4A017 gold as body text — only for accent elements
Never use: red text on red background
```

### General Contrast Rules (ALL DECKS)
- White/cream background + dark text (#1A1A1A): ✓ Always safe
- Dark background + white text: ✓ Safe if background is ≥ 60% dark
- Gold accent on dark background: ✓ Use sparingly (1-2 elements per slide)
- **NEVER:** Light grey text (#999) on white background — fails WCAG AA
- **NEVER:** Yellow/gold text on white background — fails contrast
- **NEVER:** Red text on dark red background — invisible
- **NEVER:** Multiple accent colors on the same slide — pick one per slide

---

## Workflow Decision Table

| Situation | Required workflow |
|---|---|
| New presentation | Image upload → Build → Dual audit → Fix → Drive |
| Edits to existing deck | Revise → Dual audit → Fix → Drive |
| Uploaded deck reconstruction | Reconstruct → Dual audit → Fix → Drive |
| Export/handoff only | Ensure in canvas → Export → Dual audit → Fix → Drive |

---

## Slide Creation Workflow

### Phase 0: Image Upload (MANDATORY FIRST STEP)
1. Collect all brand images, product photos, competitor logos
2. Upload ALL to Google Drive or via `manus-upload-file`
3. Build `image_manifest.json` with public URLs
4. Never reference local paths in slide HTML when using OpenRouter API

### Phase 1: Planning
1. Confirm topic, audience, and purpose
2. Extract brand colors, fonts, and logo
3. Outline slide structure (1 slide per key point)
4. Identify which slides need charts, images, or diagrams
5. Prepare `research_context_summary.md`

### Phase 2: Building (Using Manus `slide_edit` Tool)
1. Create all slides in Manus native canvas using `slide_edit`
2. Apply visual standards: fonts, margins, density, color
3. Ensure every slide has required visual elements per type
4. Add citations to all quantitative claims
5. Embed brand product images on ≥ 3 slides
6. Verify image URLs are public CDN links (not local paths)

### Phase 3: Export
1. Export PPTX
2. Export PDF (v1)

### Phase 4: Dual Audit + Fix Cycle
1. Run Opus 4.7 formatting + image enrichment audit
2. Fix all MAJOR_ISSUES and BLANK_BROKEN slides
3. Execute Opus IMAGE_ENRICHMENT_PLAN
4. Re-export PDF (v2)
5. Run GPT-5.5-pro fact-check + additional image audit
6. Fix all LIKELY_HALLUCINATED and CONTRADICTED claims
7. Execute GPT-5.5 ADDITIONAL_IMAGE_LOG
8. Re-export final PPTX and PDF

### Phase 5: Delivery
1. Save final PPTX and PDF to Google Drive
2. Share audit summary + image enrichment log with user

---

## Quality Checklist (Pre-Delivery)

- [ ] All images uploaded to Google Drive / CDN before slide building
- [ ] `image_manifest.json` created with public URLs
- [ ] All `<img>` tags use public CDN URLs or verified absolute local paths
- [ ] No local relative paths in any `<img>` tag
- [ ] Body text ≥ 16px throughout (zero exceptions)
- [ ] Titles ≥ 28px throughout
- [ ] No slide exceeds word count limits for its type
- [ ] Margins consistent at 40px on all slides
- [ ] No large empty white areas (>30% unused space on one side)
- [ ] No blue dashed borders or card shadows
- [ ] Brand colors present on every slide
- [ ] Every slide has ≥ 1 visual element (chart, image, icon, diagram)
- [ ] ≥ 40% of slides have photographic/illustrative images
- [ ] Brand product images on ≥ 3 slides
- [ ] All quantitative claims have (Source, Year) citations
- [ ] Opus 4.7 audit completed
- [ ] All BLANK_BROKEN slides rebuilt
- [ ] All MAJOR_ISSUES slides fixed
- [ ] Opus IMAGE_ENRICHMENT_PLAN fully executed
- [ ] GPT-5.5-pro audit completed
- [ ] All LIKELY_HALLUCINATED claims removed
- [ ] All CONTRADICTED claims resolved
- [ ] GPT-5.5 ADDITIONAL_IMAGE_LOG fully executed
- [ ] Final PPTX and PDF saved to Google Drive

---

## Citation Standards

Every quantitative claim MUST have a parenthetical citation:
```
Premium butter market growing at 10% CAGR (Circana, Q4 2025)
```

Data slide source line (bottom of slide):
```
Sources: Circana Retail Data Q4 2025; Mintel Butter Report Jan 2026
```

Flag data older than 6 months: `(2024 data; 2025 update pending)`

---

## Error Recovery

### If images are missing after slide build:
1. Check `image_manifest.json` — are all URLs public CDN links?
2. Re-upload any local images via `manus-upload-file`
3. Update all `<img src="">` tags with the new public URLs
4. **Never accept a slide with a broken or missing image**

### If Opus audit fails:
1. Retry with PDF URL via `manus-upload-file`
2. If still failing, manually review against visual standards checklist

### If GPT-5.5-pro audit fails:
1. Retry with `gpt-5.5-xhigh`
2. If that fails, use Gemini 3.1 Pro as fallback
3. Flag deck as "Fact-check audit incomplete" in delivery

### If fix cycle creates new issues:
1. Re-run relevant audit after fixes
2. Iterate until no MAJOR_ISSUES or LIKELY_HALLUCINATED remain
3. Maximum 3 fix cycles before escalating to user

---

## Manus Skill Update Procedure

### Step 1: Update files on disk and push to GitHub
```bash
cp /home/ubuntu/skills/<skill-name>/SKILL.md /home/ubuntu/manus-skills/skills/<skill-name>/SKILL.md
cd /home/ubuntu/manus-skills && git add -A && git commit -m "Update <skill-name>" && git push
```

### Step 2: Reload in Manus Settings via Browser (MANDATORY)
1. Navigate to `https://manus.im/app#settings/skills`
2. Find the skill (hover to reveal **"..."** three-dot menu)
3. Click **"..."** → **"Replace"** to update in place
4. Verify the updated description appears

**If "..." menu does not appear:** Hover directly over the skill card — the menu appears on hover only.
