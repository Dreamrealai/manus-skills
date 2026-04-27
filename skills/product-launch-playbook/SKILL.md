---
name: product-launch-playbook
description: Dynamic orchestrator for building consulting-grade (McKinsey/BCG/Bain style) product launch decks. Takes any brand or product as input, dynamically generates bespoke deep research prompts from a modular topic library, executes a redundant 3-pronged research workflow (running ALL prompts through both Gemini Deep Research and ChatGPT Deep Research, plus Manus independent research), aggregates findings with citations, and outputs a structured presentation deck natively styled in the brand's own color palette and typography. Enforces MANDATORY 1-hour ChatGPT Deep Research wait with 5-minute check-ins and dual audit cycle (Opus 4.7 formatting + GPT-5.5-pro fact-check) after deck generation. Use when the user asks to create a product launch playbook, brand launch deck, go-to-market presentation, or launch strategy deck.
---

# Product Launch Playbook

A comprehensive, dynamic workflow that generates a consulting-grade (MBB-style) product launch presentation for **any** brand, product, or category. Every execution is bespoke — prompts, research focus, channel strategy, and deck styling adapt entirely to the input.

## Prerequisites

Before starting, confirm you have:
- The **brand name** and **product name** (or product concept).
- The **product category** (e.g., CPG Beverage, B2B SaaS, Luxury Fashion, Consumer Electronics, QSR, Automotive, Fintech, Pharma OTC, DTC Beauty, Entertainment/Media).
- Any **specific goals, audiences, or constraints** the user has stated.
- Access to: `openrouter` skill (Claude Opus 4), `gemini-api` skill, ChatGPT web browser, Manus search/browser tools, Manus `slides` generation tool, and `gws`/`rclone` for Drive upload.

---

## Phase 1: Category Classification & Dynamic Prompt Generation

### Step 1.1 — Classify the Product Category

Determine which category archetype applies. This drives conditional logic throughout the workflow:

| Category Archetype | Examples | Key Channel Implications |
|---|---|---|
| **CPG / FMCG** | Beverages, snacks, household | Retail media (Amazon, Walmart Connect, Instacart), in-store activation, shopper marketing |
| **Consumer Electronics** | Phones, wearables, smart home | Retail media, creator/unboxing content, review seeding, Best Buy/Amazon |
| **B2B SaaS / Enterprise** | Software platforms, dev tools | LinkedIn, ABM, content marketing, analyst relations, partner channels |
| **Luxury / Premium** | Fashion, watches, spirits | Experiential, editorial, influencer seeding (not paid posts), CRM, clienteling |
| **DTC / Digitally Native** | Beauty, wellness, apparel | Paid social, creator economy, community building, subscription/loyalty |
| **QSR / Food Service** | Restaurant chains, delivery | LTO strategy, app/loyalty, local media, delivery platform partnerships |
| **Automotive** | Vehicles, EV, mobility | Dealer network, experiential, OOH, configurator/digital experience |
| **Pharma / Health OTC** | OTC drugs, supplements | HCP marketing, regulatory considerations, DTC awareness, retail pharmacy |
| **Fintech / Financial** | Cards, apps, neobanks | Trust/credibility, referral loops, compliance, partnerships |
| **Entertainment / Media** | Films, games, streaming | Fandom activation, social-first, PR/earned, platform exclusives |

Save classification to `category_profile.md` with the archetype, relevant channels, and any channels explicitly **excluded** (e.g., no retail media for B2B SaaS).

### Step 1.2 — Dynamically Assemble 3 Bespoke Research Prompts

Use the **Modular Topic Library** below. Select 3–4 topics per prompt based on category relevance. **Never reuse the same combination twice.** Each prompt must be tailored to the specific brand, product, category, and competitive context.

#### Modular Topic Library (10 Topics)

1. **Market Sizing & Growth Dynamics** — TAM/SAM/SOM, category growth rate, macro tailwinds/headwinds, regulatory factors.
2. **Consumer/Buyer Insights & Need-States** — Target audience demographics, psychographics, Jobs-to-Be-Done, purchase triggers, unmet needs.
3. **Competitive Dynamics & How to Win** — Top 3-5 direct competitors: how they position, how they market (channels, messaging, creative approach, spend levels), their launch playbooks, what's working for them, where they're vulnerable, and a specific strategy for how to win against each.
4. **Brand Perception & Cultural Context** — Brand equity, sentiment analysis, cultural relevance, heritage/authenticity signals, brand stretch risk.
5. **Channel & Distribution Strategy** — Relevant go-to-market channels (retail, DTC, marketplace, wholesale, partnerships), channel economics.
6. **Digital & Paid Media Landscape** — Platform-specific opportunities (Meta, TikTok, Google, LinkedIn, CTV, programmatic), CPM/CPA benchmarks, emerging formats.
7. **Earned Media, PR & Word-of-Mouth** — Influencer/creator ecosystem, editorial landscape, WOM drivers, virality mechanics, community dynamics.
8. **Retail Media & Shopper Marketing** — *(Only for CPG, Consumer Electronics, DTC with retail presence)* — Amazon Ads, Walmart Connect, Instacart, Criteo, in-store activation, trade spend.
9. **Pricing, Promotion & Commercial Strategy** — Price sensitivity, promotional mechanics, bundling, subscription models, LTV/CAC dynamics.
10. **Measurement, KPIs & Benchmarks** — Category-specific KPIs, attribution models, benchmark conversion rates, leading/lagging indicators.

#### Step 1.3 — Call Opus to Generate the Prompts

Call Claude Opus 4 via `openrouter` with the following system prompt:

```
SYSTEM PROMPT FOR OPUS — DYNAMIC PROMPT GENERATOR
===================================================
You are a senior strategy consultant at McKinsey, BCG, or Bain. You are generating 3 deep research prompts for an AI research assistant that will investigate a specific product launch.

INPUTS:
- Brand: {brand_name}
- Product: {product_name}
- Category Archetype: {category_archetype}
- User Goals/Constraints: {user_goals}
- Excluded Channels: {excluded_channels}
- Included Modular Topics: {selected_topics_per_prompt}

INSTRUCTIONS:
1. Generate exactly 3 deep research prompts, each 200-400 words long.
2. Each prompt must combine 3-4 topics from the Modular Topic Library in a unique, non-overlapping way. Distribute all 10 topics across the 3 prompts (some topics may appear in more than one prompt if they intersect, but the ANGLE must differ).
3. Each prompt must be specifically about {brand_name} and {product_name} — reference real competitors, real market dynamics, and real channels by name.
4. Do NOT include topics from the Excluded Channels list.
5. Prompt 1 should emphasize quantitative data: market sizing, growth rates, pricing benchmarks, financial data.
6. Prompt 2 should emphasize strategic analysis: deep competitive dynamics (how top competitors market, their channel mix, messaging, creative approach, estimated spend, what's working for them, where they're vulnerable), brand strategy, go-to-market frameworks, and a specific how-to-win strategy.
7. Prompt 3 should emphasize real-time signals: social media sentiment, creator/influencer landscape, trending conversations, community reactions, earned media coverage.
8. Every prompt must end with: "Provide all findings with specific citations including source name, author where available, and date."
9. Write each prompt as a direct instruction to a research assistant. Be specific — name competitors, platforms, retailers, and data sources to investigate.
10. CRITICAL EXCLUSION: Do NOT include any content about supply chain, logistics, manufacturing, warehousing, fulfillment, or inventory management. Focus exclusively on marketing, brand strategy, and go-to-market communications.

OUTPUT FORMAT:
## Prompt 1: [Descriptive Title]
[prompt text]

## Prompt 2: [Descriptive Title]
[prompt text]

## Prompt 3: [Descriptive Title]
[prompt text]
```

Save output to `research_prompts.md`.

---

## Phase 2: Brand Style & Identity Extraction

Before building the deck, you MUST extract the brand's visual identity. This will guide the native slides generation.

### Step 2.1 — Research Brand Guidelines
1. Use browser tools to search for `"{brand_name}" brand guidelines filetype:pdf` and `"{brand_name}" visual identity`.
2. Visit the brand's official website. Inspect:
   - Primary and secondary colors (identify hex codes)
   - Typography (font families used in headings and body text). **If the brand/typography doesn't exist or can't be found, that's not an issue — just pick one that you feel is appropriate for the category.**
   - Logo usage patterns
   - Visual style (e.g., photography-heavy, minimalist, bold graphic, editorial)
3. Search for `"{brand_name}" brand colors hex` or check brand resource sites (e.g., BrandColors.net, Brandfetch).

### Step 2.2 — Create Brand Style Profile
Save to `brand_style.md`:

```
# Brand Style Profile: {brand_name}

## Colors
- Primary: #{hex} (name)
- Secondary: #{hex} (name)
- Accent: #{hex} (name)
- Background: #{hex}
- Text Primary: #{hex}
- Text Secondary: #{hex}

## Typography
- Heading Font: {font_family} (fallback: {safe_fallback})
- Body Font: {font_family} (fallback: {safe_fallback})

## Visual Style Guidelines for Slides
- {Description of visual style, e.g., "Clean minimalist with bold accent colors, heavy use of white space, lifestyle photography"}
- {Specific instructions for Manus slides generation, e.g., "Use Primary Blue for all slide titles, Accent Orange for data callouts"}
```

---

## Phase 3: Redundant Deep Research Execution

Execute the research prompts redundantly to ensure maximum coverage and fact-checking. Total research phase target: **30–45 minutes**.

### Execution Strategy
Run Phases 3A, 3B, and 3C in PARALLEL where possible:
- Submit all 3 Gemini API calls first (they run asynchronously).
- While Gemini processes, open ChatGPT in the browser and submit Prompt 1.
- While ChatGPT researches, begin Manus independent research (3C).
- Periodically check Gemini and ChatGPT for completed results.
- Target: All research complete within 30-45 minutes of starting Phase 3.

### 3A — Gemini Deep Research (All 3 Prompts)
1. Submit Prompt 1, Prompt 2, and Prompt 3 to Gemini via the `gemini-api` skill using the deep research / grounding mode.
2. Wait for completion.
3. Save the full responses with citations to `gemini_report_1.md`, `gemini_report_2.md`, and `gemini_report_3.md`.

### 3B — ChatGPT Deep Research (All 3 Prompts)

> **MANDATORY: 1-Hour Wait with 5-Minute Check-ins**
> ChatGPT Pro Deep Research can take up to 60 minutes per prompt. This is normal and expected.
> - The moment each ChatGPT Deep Research session is submitted, **start a 5-minute check-in cadence** using the `schedule` tool.
> - Check the browser tab every 5 minutes for completion.
> - **DO NOT proceed to Phase 4 until ALL ChatGPT reports are harvested** OR 60 minutes have elapsed.
> - **If ChatGPT has not completed within 60 minutes:** Set a 1-hour timer (`schedule` tool, `interval` type, 3600 seconds, `repeat=false`) with the prompt: "Check ChatGPT browser tab for completed Deep Research reports on {brand_name} and harvest any available results into chatgpt_report_*.md files." Then proceed to Phase 4 with whatever is available, noting the gap.

1. Open `https://chatgpt.com` in the browser.
2. Navigate to a new conversation, select the **Deep Research** mode/model.
3. Submit Prompt 1, Prompt 2, and Prompt 3 (in separate deep research sessions if necessary).
4. **Start the 5-minute check-in cadence immediately** after each submission.
5. Wait for all research reports to complete (up to 60 minutes). Monitor browser tabs at each check-in.
6. Once complete, copy the full outputs and save to `chatgpt_report_1.md`, `chatgpt_report_2.md`, and `chatgpt_report_3.md`.
7. **Fallback if ChatGPT Deep Research is unavailable:** Use ChatGPT standard mode with web browsing enabled. Note reduced depth in the aggregated research file.

### 3C — Manus Independent Research
Execute the prompts yourself using Manus search and browser tools to fill any gaps or focus on real-time signals. Follow this protocol:

1. **Search broadly first**: Run 5–8 search queries covering the prompt's topic areas.
2. **Go deep on primary sources**: Visit at minimum 10–15 unique URLs. Prioritize:
   - Brand's own website, press releases, investor materials
   - Social media (TikTok, Instagram, X/Twitter, Reddit, LinkedIn) for real-time sentiment
   - Industry publications (e.g., Ad Age, Marketing Week, TechCrunch, Business of Fashion)
   - Data providers (Statista, eMarketer, Nielsen, Sensor Tower, SimilarWeb)
   - Creator/influencer content and comment sections
3. **Capture verbatim quotes and data points** with full source URLs.
4. Save to `manus_research.md` with inline citations `[Source Name, Date](URL)`.

---

## Phase 4: Aggregation, Synthesis & Fact-Checking

### Step 4.1 — Harvest Reports
Collect all 6 deep research reports (`gemini_report_*.md`, `chatgpt_report_*.md`) and `manus_research.md`.

### Step 4.2 — Aggregate
Create `aggregated_research.md` structured by the following sections (map findings to whichever sections are relevant):

1. Market Overview & Sizing
2. Consumer/Buyer Insights
3. Competitive Landscape
4. Brand Perception & Cultural Context
5. Channel & Distribution Opportunities
6. Media & Communications Landscape
7. Pricing & Commercial Dynamics
8. Measurement Benchmarks
9. Risks & Watchouts
10. Key Data Points & Statistics (consolidated table)

### Step 4.3 — De-duplicate & Validate (via Gemini 3.1 Pro)
Use Gemini 3.1 Pro via the `gemini-api` skill as the primary validator and judge of the work to aggregate findings:
1. Pass all raw reports to Gemini 3.1 Pro with instructions to de-duplicate and resolve conflicts.
2. Ask Gemini to ensure every claim has at least one citation, removing unsourced claims or marking as `[Unverified]`.
3. Have Gemini highlight the **10 most compelling insights** that should anchor the deck narrative.

---

## Phase 5: Consulting-Grade Deck Structuring

Use Claude Opus 4 via `openrouter` to synthesize the aggregated research into a 20-30 slide MBB-style (McKinsey/BCG/Bain) presentation outline. The outline MUST follow the Pyramid Principle (Answer first, then supporting data) and use Action Titles (every slide title is a conclusion).

```
You are a Principal at McKinsey & Company creating a product launch strategy deck.

INPUT: The aggregated research document below contains all findings for {brand_name}'s launch of {product_name}.

TASK: Create a detailed 20-30 slide outline following the Pyramid Principle. Every slide title MUST be an Action Title (a complete sentence that states the slide's conclusion). Structure the narrative as a SCQA (Situation-Complication-Question-Answer) arc.

CATEGORY: {category_archetype}
EXCLUDED TOPICS: {excluded_channels}. Do NOT include slides or content about these.
CRITICAL EXCLUSION: The deck must contain ZERO content about supply chain, logistics, manufacturing, or fulfillment. If the research contains such findings, exclude them entirely.

SLIDE STRUCTURE (Expand these sections to create 20-30 total slides):
1. Cover Slide
2-3. Executive Summary (SCQA framework)
4-6. Market Landscape (Size, growth, tailwinds, trends)
7-9. Consumer Insights (Audience profile, need-states, purchase journey)
10-12. Competitive Dynamics (Top competitors, how they market, positioning map, vulnerabilities, how-to-win strategy)
13-15. Product Overview & Value Prop (Features, benefits, differentiators)
16-17. Brand Positioning (Positioning statement, personality, tone)
18-20. Go-to-Market Strategy (Channel mix, category-specific channels)
21-23. Communications & Media Plan (Creative strategy, WOM/earned)
24-25. Launch Timeline (Pre-launch, Burst, Sustain phases)
26-27. Investment Framework (Budget allocation, expected ROI)
28-29. KPIs & Measurement (Targets, leading/lagging indicators)
30. Risks & Contingencies (Top risks and mitigation)
31+. Appendix (Source list, detailed data tables)

TOTAL: Target 25 slides. Minimum 20, maximum 30. Consolidate sections where content is thin.

For each slide, provide:
- Action Title (conclusion sentence)
- 3-5 bullet points of key content
- 1-2 data points to feature (with source)
- Suggested visual element (chart type, framework, or diagram)
- Speaker Notes (2-3 sentences of narrative context that the presenter would say aloud)

OUTPUT the outline in structured Markdown.
```

Save to `deck_outline.md`.

---

## Phase 6: PowerPoint Deck Creation

Build a polished PowerPoint presentation applying the brand guidelines from Phase 2.

### Step 6.1 — Prepare Slide Content
Format `deck_outline.md` into the slide content structure. Ensure every slide has its Action Title, bullet points, and data callouts clearly laid out.

### Step 6.2 — Generate the Deck
1. Enter slides mode and generate all 20-30 slides based on the consulting-grade outline.
2. Apply the brand's exact hex codes for backgrounds, titles, and accents from `brand_style.md`.
3. Apply the brand's typography for headings and body text.
4. Use `html` mode for data-heavy/editable decks, or `image` mode if the user requests a visually stunning/artistic presentation.

### Step 6.3 — Validate & Export
- Confirm all 20-30 slides rendered correctly.
- Verify brand colors and fonts are applied accurately.
- Check that no slide has overflowing text.
- Export as `{Brand}_{Product}_Launch_Playbook.pptx` (or PDF if requested).

---


---

## Phase 7: Mandatory Dual Audit & Fix Cycle

Once the initial deck is generated, you MUST run it through a **mandatory two-round audit and fix cycle** before delivery. Both rounds are non-negotiable. Each round produces a slide-by-slide evaluation table, followed by Manus fixing all flagged issues.

> **NON-NEGOTIABLE RULE:** Do NOT deliver the deck to the user until BOTH audit rounds are complete and all MAJOR issues are fixed.

---

### Audit Round 1: Opus 4.7 Formatting & Visual Quality Audit

**Purpose:** Catch formatting failures, visual design issues, blank slides, text overflow, font size violations, and missing visual elements.

#### Step 7.1 — Export PDF for Audit
1. Export the current deck as PDF: `{Brand}_{Product}_Launch_Playbook_v1.pdf`
2. Upload the PDF to S3 using `manus-upload-file` to get a public URL.

#### Step 7.2 — Run Opus 4.7 Formatting Audit
Call Claude Opus 4.7 via `openrouter` (alias: `opus`) with the PDF URL and this system prompt:

```
You are a senior presentation designer and McKinsey deck quality reviewer. Audit this product launch presentation PDF slide by slide for formatting, visual design, and composition issues.

For EACH slide, evaluate:
1. BLANK/BROKEN: Is the slide blank, mostly empty, or broken?
2. FONT SIZE: Is body text below 16px? Titles below 24px?
3. TEXT DENSITY: Is the slide a text wall (>60% text coverage with no visual relief)?
4. IMAGES/VISUALS: Does the slide have at least one visual element (chart, image, icon, diagram)? Data slides MUST have a chart.
5. MARGINS: Are margins consistent? Is content too close to edges (<3% margin)?
6. BRAND COLORS: Are the brand's hex colors applied correctly to titles, accents, and backgrounds?
7. WHITESPACE: Is there sufficient breathing room? Is the page well-utilized without overcrowding?
8. ALIGNMENT: Are elements aligned to a consistent grid?

Output a Markdown table with columns: Slide # | Title | Status | Issues | Priority | Recommended Fix
Status values: PASS | MINOR_ISSUES | MAJOR_ISSUES | BLANK_BROKEN
Priority values: CRITICAL | HIGH | MEDIUM | LOW

After the table, provide:
- OVERALL_GRADE: A/B/C/D/F
- SYSTEMIC_ISSUES: List any patterns appearing on 3+ slides
- ROOT_CAUSES: What caused the most common failures?
```

#### Step 7.3 — Fix All Flagged Issues
After receiving Opus's audit table:
1. Save the audit table to `opus_formatting_audit_v1.md`.
2. **Mandatory fixes:** Address ALL slides with `BLANK_BROKEN` or `MAJOR_ISSUES` status.
3. **Strongly recommended:** Address all `HIGH` priority items.
4. Use `slide_edit` to fix each flagged slide. Ensure:
   - Minimum 16px body text, 24px titles
   - At least one visual element per data/insight slide
   - Consistent margins (≥3% on all sides)
   - Brand colors correctly applied
   - No blank slides
5. Re-export as `{Brand}_{Product}_Launch_Playbook_v2.pdf`.

---

### Audit Round 2: GPT-5.5-Pro Fact-Check & Hallucination Audit

**Purpose:** Catch factual errors, hallucinated statistics, missing citations, internal contradictions, and unsourced claims.

#### Step 7.4 — Run GPT-5.5-Pro Fact-Check Audit
Call GPT-5.5-Pro via `openrouter` (alias: `gpt-5.5-pro`, reasoning=xhigh) with the v2 PDF URL and this system prompt:

```
You are a senior fact-checker and research analyst auditing a product launch strategy deck for factual accuracy, citation quality, and hallucination risk.

For EACH slide, evaluate:
1. FACTUAL_STATUS: Are all statistics, market figures, and claims verifiable?
2. SUSPICIOUS_CLAIMS: Flag any statistics that seem implausible, exaggerated, or inconsistent with known industry data.
3. HALLUCINATION_FLAGS: Identify claims that are likely fabricated (e.g., precise statistics without sources, quotes attributed to unnamed sources, overly specific predictions).
4. MISSING_CITATIONS: List any data points that need a source citation.
5. INTERNAL_CONTRADICTIONS: Flag any claim that contradicts another claim elsewhere in the deck.
6. FORMATTING_NOTES: Light pass only — note any obvious issues (e.g., blank slide, illegible text).

Output a Markdown table with columns: Slide # | Title | Factual Status | Suspicious Claims | Hallucination Risk | Missing Citations | Recommended Fix
Factual Status values: VERIFIED | PLAUSIBLE | UNVERIFIED | LIKELY_HALLUCINATED
Hallucination Risk values: LOW | MEDIUM | HIGH | CRITICAL

After the table, provide:
- VERIFIED_FACTS: List of claims you can confirm as accurate
- HALLUCINATION_REPORT: Detailed explanation of any likely hallucinations
- CITATION_GAPS: Consolidated list of all missing citations
- OVERALL_CONFIDENCE: 0-100 score for deck factual reliability
```

#### Step 7.5 — Fix All Fact-Check Issues
After receiving GPT-5.5-Pro's audit:
1. Save the audit table to `gpt55_factcheck_audit_v2.md`.
2. **Mandatory fixes:** Remove or correct ALL `LIKELY_HALLUCINATED` claims.
3. **Mandatory fixes:** Add `[Source Needed]` tags to all `MISSING_CITATIONS` items, or remove the unsourced claim.
4. **Mandatory fixes:** Resolve all `INTERNAL_CONTRADICTIONS`.
5. Fix each flagged slide using `slide_edit`.
6. Re-export as `{Brand}_{Product}_Launch_Playbook_Final.pdf` and `{Brand}_{Product}_Launch_Playbook_Final.pptx`.

---

### Audit Summary Table
After both rounds, create `audit_summary.md` with:
- Round 1 (Opus) overall grade and top 5 issues fixed
- Round 2 (GPT-5.5-Pro) confidence score and top 5 facts verified/corrected
- Total slides fixed across both rounds

---

## Phase 8: Packaging & Delivery

### Step 8.1 — Create Deliverable Package
Bundle the final exported deck and all raw research reports (`gemini_report_*.md`, `chatgpt_report_*.md`, `manus_research.md`, `aggregated_research.md`, `deck_outline.md`, `brand_style.md`) into a ZIP archive named `{Brand}_{Product}_Launch_Package.zip`.

### Step 8.2 — Upload to Google Drive
Use `gws` or `rclone` to upload the ZIP to the user's Google Drive `Work in Progress` folder.

### Step 8.3 — Present to User
Provide the user with:
1. The final presentation file directly in chat.
2. A summary of the 5 most important strategic insights from the research.
3. A note on any data gaps, unverified claims, or areas that would benefit from proprietary data.
4. The Google Drive link to the full package.

---

## Conditional Logic Reference

Apply these rules throughout all phases:

| Condition | Action |
|---|---|
| Category is CPG/FMCG or Consumer Electronics | Include retail media (Topic 8) in prompts and deck |
| Category is B2B SaaS/Enterprise | Exclude retail media; include ABM, analyst relations, partner channels |
| Category is Luxury/Premium | Exclude performance marketing heavy tactics; emphasize experiential, editorial, CRM |
| Category is DTC with no retail presence | Exclude retail media; focus on paid social, community, creator economy |
| Category is Pharma/Health | Include regulatory considerations; flag any claims needing medical/legal review |
| Category is Automotive | Include dealer/network strategy; emphasize experiential and configurator |
| User specifies a budget | Include specific $ allocations in the Investment Framework slides (26-27); otherwise use % ranges |
| User specifies a launch date | Anchor the Launch Timeline slides (24-25) to that date; otherwise use relative T-minus phasing |

---

## Error Handling

- **Gemini API timeout/failure**: Re-submit once. If it fails again, redistribute the prompt's topics into Manus research and note the gap.
- **ChatGPT Deep Research unavailable**: Use ChatGPT standard mode with web browsing enabled as fallback. Note reduced depth.
- **Brand style unresearchable** (e.g., stealth startup): Use a clean, professional default palette (navy #1B2A4A, white #FFFFFF, accent blue #2D7DD2) with Inter/Helvetica fonts. Ask user to confirm or provide brand assets.
- **Insufficient research data**: Flag specific gaps to the user. Do NOT fabricate data. Use `[Data Needed]` placeholders in the deck and note them in delivery.

---

## Quality Checklist (Before Delivery)

- [ ] All 20-30 slides present and populated
- [ ] Every slide title is an Action Title (complete conclusion sentence)
- [ ] Executive Summary follows SCQA structure
- [ ] No generic/filler content — everything is specific to this brand and product
- [ ] Brand colors (hex) correctly applied to slide backgrounds, titles, and accents
- [ ] Brand typography applied
- [ ] All data points have citations (parenthetical format: `(Source Name, Year)`)
- [ ] Channel recommendations are category-appropriate (no excluded channels present)
- [ ] No supply chain content anywhere in the deck
- [ ] **ChatGPT Deep Research 1-hour wait completed** — all 3 ChatGPT reports harvested (or timer fallback set)
- [ ] **Opus 4.7 formatting audit completed** — audit table saved to `opus_formatting_audit_v1.md`
- [ ] **All BLANK_BROKEN and MAJOR_ISSUES slides fixed** after Opus audit
- [ ] **GPT-5.5-Pro fact-check audit completed** — audit table saved to `gpt55_factcheck_audit_v2.md`
- [ ] **All LIKELY_HALLUCINATED claims removed or corrected** after GPT-5.5-Pro audit
- [ ] **Audit summary saved** to `audit_summary.md`
- [ ] ZIP package contains all files including redundant research reports and audit tables
- [ ] File uploaded to Google Drive successfully
