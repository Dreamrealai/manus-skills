---
name: creative-supercharger
description: Comprehensive multi-agent workflow to produce a 6-part brand intelligence package for any brand. Deliverables include a Brand Growth Strategy Deck, Brand Guidelines & Typography folder, "5 Things We Wouldn't Expect an Agency to Know", Product Images & End Cards, Example Ads Spreadsheet with downloads, and an AI Stance Report. Uses 12+ deep research prompts across Gemini, ChatGPT, and Manus independent research. Use when the user asks for a "brand setup", "creative supercharger", "brand intelligence report", "brand pack", or "deep research brand pack" for any brand.
---

# Creative Supercharger: Brand Intelligence Workflow

Orchestrates a multi-agent deep research process to generate a comprehensive 6-part brand setup package for any brand. Combines Gemini Deep Research, ChatGPT Deep Research, and Manus independent web/social research. Total time: 45-75 minutes.

## Pre-Flight: Brand Intake & Classification

Before launching research, establish a **Brand Context Profile**.

### Required Inputs

| Variable | Description | Example |
|---|---|---|
| `BRAND_NAME` | Exact legal name + DBA/trade names | Ten Thousand |
| `BRAND_URL` | Website URL (if exists) | tenthousand.cc |
| `BRAND_CATEGORY` | Industry/vertical | Men's training apparel |
| `FOUNDER_NAME` | Founder(s) name(s) | Keith Nowak |
| `KEY_COMPETITORS` | Known competitors | Lululemon, Vuori, Rhone |
| `RELEVANT_SUBREDDITS` | Niche communities | r/crossfit, r/Activewear |
| `ENGAGEMENT_CONTEXT` | Why we're researching | Potential agency engagement |

### Brand Archetype Classification

Classify the brand before executing — it changes how every phase runs:

| Archetype | Signals | Workflow Adjustments |
|---|---|---|
| **Pre-Launch / Stealth** | No live website, no ad history | Skip Deliverables 5 and most of 2. Focus on founder backgrounds, patent filings, competitive whitespace. Deck becomes market opportunity analysis. |
| **Early-Stage DTC** | <3 years, VC-funded, limited ads | Lean on social listening, founder interviews, Meta Ad Library. Substitute funding data for financials. |
| **Established DTC** | 3+ years, active ad spend | Full workflow applies. |
| **Enterprise / Public** | SEC filings, 1000+ employees | Scope to a specific business unit. Use 10-K/10-Q as primary financial sources. |
| **B2B / SaaS** | Enterprise sales, no consumer ads | Shift ads to LinkedIn/webinars. Sentiment from G2, Capterra, HackerNews. |
| **Local / SMB** | Regional, minimal digital footprint | Scale down to 8 prompts. Deck becomes competitive landscape + opportunity. |

---

## The 6 Deliverables

1. **Brand Growth Strategy Deck** — 20-30 slide presentation (competitive research, growth levers, performance, campaign ideas). Every claim sourced. Presentable to a CMO without edits.
2. **Brand Guidelines & Typography** — Folder with logos (SVG/PNG), color palette (HEX/RGB), typography specs, photography style notes, and a `Brand_Guidelines_Summary.md`.
3. **5 Non-Obvious Insights** — "5 Things We Wouldn't Expect an Agency to Know." Provocative, insider-level facts. Quality bar: if a typical account manager could find it in 5 minutes of Googling, it is NOT non-obvious enough.
4. **Product Images & References** — 5-10 key product images, video start/end card screenshots, `References_Index.md`. Minimum 1080px resolution.
5. **Example Ads Database** — `Example_Ads.xlsx` (15-25 ads cataloged) + downloaded video files. Primarily video, but also other channels. Includes a Summary tab with patterns analysis.
6. **AI Stance Report** — 1-3 page Markdown report on the brand's public/inferable stance on AI. If no stance found, report that as a finding.

---

## Phase 1: Launch Parallel Deep Research (12+ Prompts)

Launch at least 12 prompts across Gemini and ChatGPT. Redundancy is intentional for cross-validation. Instruct models to **cite all sources with URLs** and **prioritize precision over speculation**.

### Gemini Deep Research (Run via `gemini-api` skill `scripts/deep_research.py`)

**G1 — Competitive Landscape:**
> "Conduct a deep competitive analysis of [BRAND] in the [CATEGORY] space. Identify top 3-5 direct competitors and 2-3 indirect/emerging competitors. Compare: pricing architecture, distribution channels, target demographic, unique value proposition. Map positioning on a 2x2 matrix. Cite all sources."

**G2 — Growth Levers & Revenue Drivers:**
> "Analyze [BRAND]'s primary growth levers over the last 3 years: (a) marketing channels driving growth, (b) key partnerships/collaborations, (c) product launches that moved the needle, (d) geographic expansion, (e) business model pivots. Quantify where possible. Cite business press or industry reports."

**G3 — Financial Performance & Business Health:**
> "Research [BRAND]'s financial performance. Public companies: cite revenue, margins, YoY growth from SEC filings. Private companies: compile estimated revenue from press, funding history (total raised, valuation, investors, last round date), profitability signals. Note employee count, hiring/layoff trends, executive changes, legal issues. Cite all sources with URLs."

**G4 — Origin Story & Founder Deep Dive:**
> "Investigate [BRAND]'s true origin story beyond the official 'About' page: (a) founder career history before this brand, (b) specific problem that sparked the company, (c) early struggles or pivots, (d) controversies about the founding team, (e) cultural/subcultural roots. Check podcast interviews, conference talks, early press, LinkedIn, Wayback Machine. Cite all sources."

**G5 — AI Stance:**
> "Research [BRAND]'s stance on Generative AI: (a) executive statements in press/earnings calls/social media, (b) job postings mentioning AI/ML/LLMs, (c) patent filings related to AI, (d) partnerships with AI companies, (e) public controversy about AI content, (f) competitor AI adoption context, (g) internal signals from Glassdoor/Blind. Cite every source. If no evidence exists for a category, state explicitly."

**G6 — Supply Chain & Sustainability:**
> "Research [BRAND]'s supply chain, manufacturing, and sustainability: Where are products made? Own manufacturing or outsource? Sustainability claims substantiated by certifications (B Corp, Fair Trade, Climate Neutral)? Supply chain controversies, labor criticisms, greenwashing accusations? Cite all sources."

### ChatGPT Deep Research (Run via browser at `chatgpt.com/deep-research`)

**C1 — Customer Sentiment & Voice of Customer:**
> "Analyze [BRAND]'s customer sentiment across Reddit, Trustpilot, Amazon reviews, BBB, and forums. Identify: (a) top 3 systemic complaints, (b) top 3 most-praised features, (c) how customers describe the brand in their own words (capture exact phrases), (d) sentiment shifts over time, (e) how the brand responds to negative feedback. Direct quotes where possible. Cite URLs."

**C2 — Marketing Campaigns & Creative Strategy:**
> "Research [BRAND]'s most notable marketing campaigns (last 3 years). For each: campaign name/theme, channels, format, core messaging framework, reported metrics/awards, target audience. Identify overall brand voice and tone. Provide examples of actual copy/taglines. Cite all sources."

**C3 — Visual Identity & Brand Design System:**
> "Identify [BRAND]'s typography (font families/weights), color palette (hex codes), and visual design language across website, packaging, social, and advertising. Describe: typefaces, color palette, photography style, graphic motifs, packaging design, cross-touchpoint consistency. Cite sources."

**C4 — Non-Obvious Insights:**
> "Find 10 highly provocative, non-obvious facts about [BRAND] that an external agency would NOT know. Look in: (a) obscure press interviews, (b) patent filings, (c) Glassdoor/Blind reviews, (d) supply chain details, (e) legal filings, (f) archived website versions, (g) old social media posts, (h) academic papers, (i) cultural connections, (j) surprising customer demographics. For each, explain why it's surprising and cite the source URL."

**C5 — Video Marketing & Ad Creative Analysis:**
> "Analyze [BRAND]'s video marketing across YouTube, TikTok, Instagram Reels, Meta video ads, and CTV. Document: (a) typical video ad structure (hook → problem/solution → CTA), (b) start/end card consistency, (c) average length by platform, (d) UGC vs. polished production, (e) recurring creators, (f) music/sound choices, (g) caption style, (h) A/B testing patterns. Cite specific video URLs."

**C6 — Social Media & Community:**
> "Analyze [BRAND]'s social media across Instagram, TikTok, X, LinkedIn, YouTube, Pinterest. For each: follower count, engagement rate, posting frequency, content mix, community management approach, viral moments, influencer partnerships (tier). Identify strongest platform and most underinvested."

**C7 — Audience & Demographics:**
> "Research [BRAND]'s target vs. actual customer demographics: (a) stated target customer, (b) actual customers from reviews/social/Reddit, (c) growth segments, (d) psychographic profile, (e) geographic concentration. Use SimilarWeb data, social analytics, press interviews. Cite sources."

### Prompt Adaptation Rules

- **Pre-Launch**: Replace competitor analysis with market whitespace. Replace financials with founder track record and funding landscape.
- **B2B/SaaS**: In C1, replace Reddit/Trustpilot with G2/Capterra/HackerNews. In C5, replace video ads with webinar/demo analysis.
- **Enterprise/Public**: Add prompt analyzing most recent earnings call transcript.
- **Local/SMB**: Reduce to 8 prompts. Focus on local SEO, Google Business Profile, local competitors.

---

## Phase 2: Manus Independent Asset Collection

Execute in parallel with Phase 1. Do NOT wait for deep research.

### 2A. Brand Guidelines (Deliverable 2)

1. **Logo Extraction**: Extract SVG/PNG from website source (`<img>`, `<svg>`, CSS `background-image`). Check `/press`, `/media`, `/brand` pages for press kits. Also check social profiles and app store listings. Save to `Brand_Guidelines/Logos/`.
2. **Color Palette**: Use `curl [URL] | grep -oP '#[0-9a-fA-F]{6}'` to extract hex codes. Fetch CSS stylesheets for custom properties (`--color-primary`). Filter to 4-8 most prominent colors. Document in `Brand_Guidelines/Color_Palette.md` with HEX, RGB, descriptive name.
3. **Typography**: Check CSS `font-family`, Google Fonts `<link>` tags, Adobe Fonts kit IDs. Document font names, weights, usage (headlines/body/CTAs), licensing status in `Brand_Guidelines/Typography.md`.
4. **Summary**: Create `Brand_Guidelines/Brand_Guidelines_Summary.md` consolidating all findings.

### 2B. Product Images (Deliverable 4)

1. Download 5-10 hero product images from website. Inspect `srcset` for highest resolution. Modify URL params (`?w=`, `?quality=`) for full res.
2. Check Instagram, Amazon, press pages, Google Image search (large filter).
3. For start/end cards: Visit YouTube channel and Meta Ad Library. Screenshot first and last frames of 3-5 recent video ads.
4. Save to `Product_Images/` with descriptive filenames. Create `References_Index.md`.

### 2C. Example Ads Database (Deliverable 5)

**Spreadsheet Schema** — columns for each ad entry:

| Column | Description |
|---|---|
| `Ad_ID` | Sequential number |
| `Brand` | Brand name (mark competitors clearly) |
| `Platform` | Meta / TikTok / YouTube / Google / LinkedIn |
| `Format` | Video / Carousel / Single Image / Collection |
| `Status` | Active / Inactive |
| `First_Seen_Date` | When ad started running |
| `Ad_Copy_Headline` | Headline text |
| `Ad_Copy_Body` | Primary text (first 100 chars) |
| `CTA_Button` | Call-to-action text |
| `Core_Message` | 1-sentence summary of ad's angle |
| `Hook_Type` | Question / Bold Claim / UGC / Product Demo / Problem-Agitate |
| `Production_Style` | UGC / Polished Studio / Motion Graphics / Mixed |
| `Landing_Page_URL` | Destination URL |
| `Thumbnail_Saved` | Yes/No |
| `Video_Downloaded` | Yes/No |
| `Notes` | Additional observations |

**Collection Sources (in priority order):**

1. **Meta Ad Library** (`facebook.com/ads/library/`): Search brand, filter US, catalog up to 30 ads. Download videos via `yt-dlp` or extract video URLs from source.
2. **TikTok Creative Center** (`ads.tiktok.com/business/creativecenter/`): Search brand, catalog and download.
3. **YouTube**: Brand channel + search `[BRAND] ad`. Download 3-5 videos: `yt-dlp -f 'bestvideo[height<=1080]+bestaudio' -o 'Example_Ads/Videos/yt_%(id)s.%(ext)s' [URL]`
4. **Google Ads Transparency** (`adstransparency.google.com/`): Search verified advertiser name.
5. **LinkedIn Ad Library** (B2B only): Brand company page + `linkedin.com/ad-library/`.
6. **Supplementary**: AdAge/Adweek/The Drum coverage, Vimeo (production companies), `moat.com`.
7. **Competitor Ads**: If brand has <15 ads, repeat steps 1-3 for top 2-3 competitors. Mark as `[COMPETITOR] (Competitor)` in Brand column.

**Finalize**: Create `Example_Ads/Example_Ads.xlsx` with a **Summary tab** containing: total ads (brand vs. competitor), breakdown by platform/format, top 3 messaging themes, top 3 creative styles, notable patterns.

---

## Phase 3: Harvest & Synthesize

**Prerequisite**: All 12+ deep research prompts must have returned. Re-run failures once, then proceed with available data.

### 3A. Cross-Validation

1. Collect all reports into a working directory.
2. Identify **corroborated facts** (high-confidence), **contradictions** (resolve by source authority: SEC filing > press > blog), and **gaps** (supplement with Manus browser searches).

### 3B. 5 Non-Obvious Insights (Deliverable 3)

**The 10→5 Funnel:**

1. **Collect candidates**: Pull every surprising fact from ALL reports + Phase 2 findings. Aim for 15-20 candidates.
2. **Score each on 4 dimensions** (1-5 scale):

| Dimension | 1 (Low) | 5 (High) |
|---|---|---|
| **Surprise Factor** | Common knowledge, on their Wikipedia page | Genuinely unexpected, contradicts conventional wisdom |
| **Strategic Relevance** | Interesting trivia, no creative implication | Directly informs a campaign angle or positioning |
| **Credibility** | Single unverified source, speculation | Multiple sources, official documents, direct quotes |
| **Conversation Value** | Client would shrug | Client would lean forward and say "How did you find that?" |

3. **Rank by total score**, select top 10.
4. **Diversity filter**: Final 5 must span at least 3 categories: Founder/Origin, Customer/Audience, Product/Supply Chain, Financial/Business Model, Cultural/Competitive, Controversy/Risk.
5. **Classify risk level**: Opportunity / Context / High Risk / Critical Risk / Strategic Opportunity.
6. **Format** in `Non_Obvious_Insights.md`:

```
# 5 Things We Wouldn't Expect an Agency to Know About [BRAND]

## 1. [Provocative Headline]
[2-3 sentence explanation]

**Why This Matters**: [Strategic/creative implication]
**Risk Level**: [Classification]
**Source**: [URL or citation]
```

### 3C. AI Stance Report (Deliverable 6)

**Evidence Assembly** — compile from Prompt G5 + supplement with targeted research:

1. **Executive Statements**: Search `[BRAND CEO/CTO] artificial intelligence` in Google News, YouTube, podcast transcripts.
2. **Job Postings**: Check careers page, LinkedIn Jobs, Indeed for AI/ML/LLM mentions. Note if engineering or marketing roles.
3. **Patent Filings**: Search USPTO and Google Patents for `[BRAND] + artificial intelligence`.
4. **Partnerships**: Look for press releases about AI vendor partnerships (Jasper, Adobe Firefly, Salesforce Einstein, etc.).
5. **Controversy**: Search `[BRAND] AI generated controversy` for any backlash incidents.
6. **Competitor Context**: What are their top 3 competitors doing with AI? This frames the brand's position.
7. **Internal Signals**: Check Glassdoor/Blind for mentions of AI tools or policy. Check LinkedIn for AI-related hires.

**Confidence Rating**: Rate overall AI stance confidence as High (multiple direct statements), Medium (indirect signals), or Low (no evidence found).

**Format** in `AI_Stance_Report.md`:
- Executive Summary (2-3 sentences)
- Evidence by Type (organized by the 7 categories above)
- Confidence Assessment
- Strategic Implications (how this affects the agency relationship)

---

## Phase 4: Deck Creation (Deliverable 1)

Using consolidated research, generate the Brand Growth Strategy Deck.

### Deck Structure (20-30 slides)

| Section | Slides | Content |
|---|---|---|
| SEC.01: Brand Identity | 4-5 | Cover, Executive Summary (6 key stats), Brand Origin Story, Brand Pillars |
| SEC.02: Product & Innovation | 2-3 | Product Architecture grid, Fabric/Technology/IP details |
| SEC.03: Market & Competition | 2-3 | Market Opportunity (size + growth), Competitive Landscape (price comparison chart) |
| SEC.04: Digital & Distribution | 2-3 | Digital Footprint (traffic, social stats), Distribution Strategy |
| SEC.05: Marketing & Growth | 3-4 | Marketing Strategy, Growth Levers, Customer Sentiment, "5 Things" highlight |
| SEC.06: Strategic Opportunities | 5-6 | 3-5 Campaign Ideas (each: concept + 3 tactic cards) |
| SEC.07: Closing | 2 | Key Metrics Summary, Sources & Methodology |

### Slide Generation

1. Initialize: `slide_initialize` with `generate_mode: "image"`, dark aesthetic (background #0A0A0A, gold accent, white text, monospace section codes).
2. Generate each slide with `image_slide_generate`. Include 1-2 previous slide images as reference for visual continuity.
3. **Quality control**: After generation, review each slide for text hallucination (AI image generators sometimes misspell words). Regenerate any slide with garbled text.
4. Present with `slide_present`.

---

## Phase 5: Organization & Delivery

### Folder Structure

```
[BRAND_NAME]_Creative_Supercharger/
├── 1_Brand_Growth_Strategy_Deck/
│   └── (presentation files)
├── 2_Brand_Guidelines/
│   ├── Logos/
│   ├── Color_Palette.md
│   ├── Typography.md
│   └── Brand_Guidelines_Summary.md
├── 3_Non_Obvious_Insights.md
├── 4_Product_Images_and_Cards/
│   └── References_Index.md
├── 5_Example_Ads/
│   ├── Example_Ads.xlsx
│   ├── Screenshots/
│   └── Videos/
└── 6_AI_Stance_Report.md
```

### Delivery Steps

1. Zip the master folder: `zip -r [BRAND]_Creative_Supercharger.zip [BRAND]_Creative_Supercharger/`
2. Upload to Google Drive using `gws` CLI or `rclone`. Create a subfolder in the designated project folder.
3. Grant access to `david@dreamreal.ai` if creating new folders.
4. Deliver the Google Drive link, the presentation URL (from `slide_present`), and the ZIP file to the user.

---

## Quick-Start Prompt

Copy-paste this to kick off a Creative Supercharger for any brand:

> "Run the Creative Supercharger for [BRAND NAME] ([WEBSITE URL]). They are a [CATEGORY] brand. Key competitors include [COMPETITOR 1, 2, 3]. This is for [CONTEXT, e.g., a potential agency pitch]. Generate all 6 deliverables and save to Google Drive."
