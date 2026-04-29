# Deep Research Prompts — Full Text Reference

This file contains the complete, copy-paste-ready prompts for all 13 deep research queries. Replace all `[BRAND]`, `[CATEGORY]`, `[FOUNDER]`, and `[SUBREDDITS]` placeholders before use.

---

## Gemini Deep Research Prompts

Run each via: `python3 /home/ubuntu/skills/gemini-api/scripts/deep_research.py --prompt "..." --output report_G[N].md`

### G1 — Competitive Landscape

```
Conduct a deep competitive analysis of [BRAND] in the [CATEGORY] space. Identify their top 3-5 direct competitors and 2-3 indirect/emerging competitors. For each competitor, compare: pricing architecture (entry price, average order value, premium tier), distribution channels (DTC, retail, marketplace), target demographic, and unique value proposition. Map [BRAND]'s positioning on a 2x2 matrix of relevant axes (e.g., price vs. premium perception, or innovation vs. heritage). Cite all sources with URLs.
```

### G2 — Growth Levers & Revenue Drivers

```
Analyze [BRAND]'s primary growth levers over the last 3 years. Investigate: (a) marketing channels that drove the most growth (paid social, influencer, SEO, TV, retail expansion, etc.), (b) key partnerships or collaborations, (c) product launches or line extensions that moved the needle, (d) geographic expansion, (e) any pivots in business model. Quantify growth where possible (revenue figures, store count, social following growth, app downloads). Cite business press, earnings calls, or industry reports with URLs.
```

### G3 — Financial Performance & Business Health

```
Research [BRAND]'s financial performance and business health. For public companies: cite revenue, gross margin, EBITDA, and YoY growth from SEC filings (10-K, 10-Q) and earnings transcripts. For private companies: compile estimated revenue from press reports (Forbes, Bloomberg, Business Insider, The Information), funding history (total raised, last valuation, lead investors, most recent round date), and any profitability signals. Also note: employee count and hiring/layoff trends, key executive changes in the last 2 years, and any legal/regulatory issues. Cite all sources with URLs.
```

### G4 — Origin Story & Founder Deep Dive

```
Investigate [BRAND]'s true origin story and founder background. Go beyond the official 'About' page. Research: (a) the founder(s)' career history before this brand, (b) the specific problem or insight that sparked the company, (c) early struggles, pivots, or near-death moments, (d) any controversies or lesser-known facts about the founding team, (e) the brand's cultural or subcultural roots. Look at podcast interviews, conference talks, early press coverage, LinkedIn profiles, and archived versions of the website (Wayback Machine). Cite all sources with URLs.
```

### G5 — AI Stance

```
Research [BRAND]'s public and inferable stance on the use of Generative AI and artificial intelligence broadly. Investigate ALL of the following evidence types: (a) Public statements by executives in press interviews, earnings calls, conference talks, or social media posts about AI. (b) Job postings on their careers page, LinkedIn, or job boards that mention AI, machine learning, LLMs, or generative AI — note whether these are engineering roles or marketing/creative roles. (c) Patent filings or trademark applications related to AI. (d) Partnerships with AI companies (e.g., using Jasper, Midjourney, or custom AI tools). (e) Any public controversy about AI-generated content associated with the brand. (f) Industry context — what are their competitors doing with AI? (g) Any internal policy signals (e.g., leaked memos, Glassdoor reviews mentioning AI policy). Cite every source. If no evidence exists for a category, state that explicitly.
```

### G6 — Supply Chain & Sustainability

```
Research [BRAND]'s supply chain, manufacturing approach, and sustainability practices. Where are their products made? Do they own manufacturing or outsource? What sustainability claims do they make, and are these substantiated by third-party certifications (B Corp, Fair Trade, Climate Neutral, etc.)? Have they faced any supply chain controversies, labor practice criticisms, or greenwashing accusations? Cite all sources with URLs.
```

---

## ChatGPT Deep Research Prompts

Run each via browser at `chatgpt.com/deep-research`. Submit one at a time.

### C1 — Customer Sentiment & Voice of Customer

```
Analyze [BRAND]'s customer sentiment across Reddit (search [SUBREDDITS]), Trustpilot, Amazon reviews (if applicable), Google Reviews, Better Business Bureau complaints, and niche forums or Facebook groups. Identify: (a) the top 3 systemic complaints (recurring pain points), (b) the top 3 most-praised features or attributes, (c) how customers describe the brand in their own words (capture exact phrases — these are valuable for ad copy), (d) any notable shifts in sentiment over time (e.g., 'quality used to be great but declined after they scaled'), (e) how the brand responds to negative feedback (tone, speed, resolution). Provide direct quotes where possible. Cite source URLs.
```

### C2 — Marketing Campaigns & Creative Strategy

```
Research [BRAND]'s most successful and most notable marketing campaigns over the last 3 years. For each campaign, document: (a) campaign name/theme, (b) channels used, (c) creative format (video, OOH, influencer, experiential, etc.), (d) core messaging framework (what emotional or rational lever does it pull?), (e) any reported performance metrics or awards, (f) the target audience it appeared to address. Also identify their overall brand voice and tone — is it aspirational, irreverent, clinical, warm, luxurious, accessible? Provide examples of actual copy/taglines. Cite all sources.
```

### C3 — Visual Identity & Brand Design System

```
Identify the specific typography (font families and weights), color palette (hex codes if findable), and visual design language used by [BRAND] across their website, packaging, social media, and advertising. Describe: (a) primary and secondary typefaces (check the website's CSS, Google Fonts usage, or font identification tools), (b) color palette with specific hex codes where possible, (c) photography style (studio vs. lifestyle, color grading, casting choices, backgrounds), (d) graphic design motifs (do they use illustrations, icons, patterns, textures?), (e) packaging design language, (f) how consistent their visual identity is across touchpoints. If you cannot determine exact hex codes or font names, provide your best identification and note the uncertainty.
```

### C4 — Non-Obvious Insights

```
Find 10 highly provocative, non-obvious, and surprising facts about [BRAND] that a typical external advertising agency would NOT know from a standard briefing or website review. These should be the kind of insights that make a client say 'How did you find that?' Look in these places: (a) obscure press interviews with founders or employees, (b) patent filings, (c) Glassdoor/Blind employee reviews revealing internal culture, (d) supply chain or ingredient sourcing details, (e) legal filings or regulatory actions, (f) archived versions of their website showing pivots, (g) social media deep cuts (old tweets, deleted posts, niche platform presence), (h) academic papers or case studies about the brand, (i) cultural or subcultural connections, (j) surprising customer use cases or demographics. For each fact, explain why it's surprising and cite the source URL.
```

### C5 — Video Marketing & Ad Creative Analysis

```
Analyze [BRAND]'s video marketing strategy across YouTube, TikTok, Instagram Reels, Meta (Facebook/Instagram) video ads, and connected TV (if applicable). Document: (a) their typical video ad structure (hook in first 3 seconds → problem/solution → CTA pattern), (b) whether they use consistent start cards (branded intro frames) or end cards (logo lockup, CTA, URL), (c) average video length by platform, (d) whether they use UGC-style or polished production, (e) recurring talent/creators, (f) music/sound design choices, (g) caption/subtitle style, (h) any A/B testing patterns visible in their ad library (e.g., same video with different hooks). Cite specific video URLs where possible.
```

### C6 — Social Media & Community

```
Analyze [BRAND]'s social media presence across Instagram, TikTok, X/Twitter, LinkedIn, YouTube, Pinterest, and any niche platforms. For each active platform, document: (a) follower count and estimated engagement rate, (b) posting frequency, (c) content mix (educational, promotional, UGC, behind-the-scenes, memes, etc.), (d) community management approach (do they reply to comments? What tone?), (e) any notable viral moments or social media controversies, (f) influencer/creator partnerships and their apparent tier (mega, macro, micro, nano). Identify which platform appears to be their strongest and which is underinvested.
```

### C7 — Audience & Demographics

```
Research [BRAND]'s target audience and actual customer demographics. Investigate: (a) who the brand says their target customer is (from their marketing, press interviews, investor materials), (b) who their actual customers appear to be (from review demographics, social media followers, Reddit discussions), (c) any audience segments they're trying to grow into, (d) psychographic profile (values, lifestyle, media consumption, adjacent brands they buy), (e) geographic concentration (are they stronger in certain markets?). Use SimilarWeb data, social media analytics references, press interviews, and customer review analysis. Cite sources.
```
