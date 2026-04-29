# Deep Research Playbook: "5 Things We Wouldn't Expect an Agency to Know About Us"

## Purpose

This template describes how to conduct deep research on any brand before producing a formatted insider-knowledge PDF. The goal is to uncover non-obvious, insider-level facts that go beyond what a standard brand audit, competitive review, or media scan would surface — the kind of findings that make a brand's team pause and say, "How did they know that?"

Fill in the variables below, then follow the workflow.

---

## Variables

Fill these in before starting research:

| Variable | Value |
|---|---|
| `{{BRAND_NAME}}` | _(e.g., Ten Thousand)_ |
| `{{BRAND_URL}}` | _(e.g., tenthousand.cc)_ |
| `{{BRAND_CATEGORY}}` | _(e.g., men's training apparel)_ |
| `{{FOUNDER_NAME}}` | _(e.g., Keith Nowak)_ |
| `{{ENGAGEMENT_CONTEXT}}` | _(e.g., potential agency engagement)_ |
| `{{RELEVANT_SUBREDDITS}}` | _(e.g., r/crossfit, r/Activewear, r/malefashionadvice)_ |
| `{{KEY_COMPETITORS}}` | _(e.g., Lululemon, Vuori, Rhone)_ |
| `{{RESEARCH_DATE}}` | _(today's date)_ |

---

## Research Architecture

Use the **DeepDeep Research** workflow (three-pronged approach):

1. **Gemini Deep Research** — long-form synthesis from web sources
2. **ChatGPT Deep Research** — parallel long-form synthesis for cross-validation
3. **Manus Independent Research** — social media, SEC filings, niche databases, real-time sources

All three run in parallel (~30 minutes). The final report is a "best of 3" consolidation.

---

## Deep Research Master Prompt

Use this prompt for both Gemini and ChatGPT Deep Research. Replace all `{{variables}}` before submitting.

```
I'm conducting due diligence on {{BRAND_NAME}}, the {{BRAND_CATEGORY}} brand
({{BRAND_URL}}), for a {{ENGAGEMENT_CONTEXT}}. I need you to go beyond the
standard brand narrative and uncover non-obvious facts that would surprise even
their internal team.

Research the following five areas in depth:

1. FOUNDER / LEADERSHIP BACKGROUND: {{FOUNDER_NAME}}'s full biography before
   {{BRAND_NAME}} — not just the polished LinkedIn version. Look for prior careers,
   personal blogs, university records, athletic or creative backgrounds, personal
   websites, niche professional profiles, and podcast appearances. Find connections
   between their personal history and the brand's positioning that aren't part of
   the official narrative.

2. TRUE ORIGIN STORY: The brand's actual launch timeline vs. the story they tell
   today. Look at early business journal coverage, trade press, SEC filings,
   crowdfunding campaigns, early retail partnerships, and any co-founders or
   beneficial owners who are not publicly acknowledged. Was the original business
   model different from what exists today?

3. CUSTOMER EXPERIENCE REALITY: The full timeline of customer complaints — not
   just recent ones. Search Reddit ({{RELEVANT_SUBREDDITS}}), Trustpilot, Better
   Business Bureau, and consumer forums. Determine whether any service issues are
   recent scaling problems or long-standing structural patterns. Look for evidence
   of complaint suppression, review manipulation, or account blocking.

4. CURRENT BUSINESS HEALTH: Any signals of financial strength or distress — layoffs,
   hiring surges, unpaid partnerships, website changes, shifts in promotional
   frequency, web traffic trends (SimilarWeb), and employee sentiment on LinkedIn
   or Glassdoor. Look at Reddit threads, news coverage, and industry reports for
   insider perspectives.

5. WHAT ACTUALLY WORKS IN THEIR MARKETING: Identify their most successful marketing
   moments — not just paid ads, but owned events, community activations, brand
   collaborations, and grassroots efforts. Compare the cultural impact and apparent
   ROI of these activations vs. their standard paid media spend. Look at event
   listings, athlete/influencer posts, case studies, and partnership announcements.

For each finding, cite the specific source with date and URL where possible.
Distinguish between verified facts and unconfirmed claims.
```

---

## Manus Independent Research Plan

While Gemini and ChatGPT run (~30 min), conduct manual research across these sources:

### Priority 1: Reddit & Forums (15 min)

| Source | Search Terms | What to Look For |
|---|---|---|
| {{RELEVANT_SUBREDDITS}} | "{{BRAND_NAME}}" | Complaint threads, praise threads, insider accounts |
| r/Entrepreneur, r/smallbusiness | "{{BRAND_NAME}}" OR "{{FOUNDER_NAME}}" | Business model discussions, insider perspectives |
| Trustpilot | {{BRAND_URL}} | Rating trend over time, recurring complaint themes |
| Better Business Bureau | "{{BRAND_NAME}}" | Rating, complaint count, registered address vs. stated HQ |

### Priority 2: Corporate Filings & Business Data (5 min)

| Source | What to Search |
|---|---|
| SEC EDGAR | "{{BRAND_NAME}}" or known legal entity name — crowdfunding filings, beneficial owners |
| Crunchbase / Tracxn / PitchBook | Funding rounds, investors, ownership changes |
| SimilarWeb | {{BRAND_URL}} traffic trend (6-month view), traffic sources |
| LinkedIn | "{{BRAND_NAME}}" — recent employee departures, hiring activity, headcount changes |

### Priority 3: Social Media Sentiment (5 min)

| Platform | Search Strategy |
|---|---|
| Instagram | @{{BRAND_HANDLE}} — comment sentiment, engagement trends, recent campaign posts |
| Twitter/X | "{{BRAND_NAME}}" since:{{6_MONTHS_AGO}} — real-time sentiment, complaints, praise |
| LinkedIn | {{FOUNDER_NAME}} posts, employee posts, brand page activity |
| YouTube | "{{BRAND_NAME}} review" — unsponsored reviews, complaint videos |

### Priority 4: Competitive & Market Context (5 min)

| Source | What to Search |
|---|---|
| Google News | "{{BRAND_NAME}}" — recent press coverage, funding announcements, controversies |
| Archive.org Wayback Machine | {{BRAND_URL}} — compare current site to 6-12 months ago for removed pages, messaging changes |
| {{KEY_COMPETITORS}} websites | Pricing, positioning, and messaging to identify differentiation gaps |

---

## How to Structure Findings for the PDF

After research is complete, select the 5 strongest non-obvious findings and organize them using this framework.

### Finding Selection Criteria

A strong finding should meet at least 3 of these 5 criteria:

1. **Non-obvious** — not discoverable through a basic Google search or the brand's own website
2. **Sourced** — backed by at least one primary source (filing, article, data point)
3. **Cross-referenced** — corroborated by a second independent source
4. **Consequential** — materially affects how an agency should approach the brand
5. **Surprising** — would genuinely make the brand's team react

### Risk Level Classification

Each finding gets a risk level:

| Risk Level | Definition | When to Use |
|---|---|---|
| **Opportunity** | Positive non-obvious fact that strengthens the brand story | Founder authenticity, hidden strengths, untold advantages |
| **Context** | Neutral but important historical nuance that reframes the narrative | Origin story differs from marketing, pivots, quiet changes |
| **High Risk** | Ongoing operational problem that affects agency positioning | Systemic service failures, quality issues, talent churn |
| **Critical Risk** | Existential threat that could derail an engagement | Financial distress, legal issues, leadership instability |
| **Strategic Opportunity** | Actionable insight for a differentiated agency pitch | Underexploited channels, community models, untapped audiences |

### Quality Checklist

For each of the 5 findings, verify before writing:

- [ ] Primary source identified with date and URL
- [ ] At least 2 independent sources corroborate the claim
- [ ] Counterpoint considered — is there an innocent explanation?
- [ ] Risk level classification is justified by the evidence
- [ ] The finding would genuinely surprise the brand's leadership

---

## Output Files

| File | Purpose |
|---|---|
| `gemini_report.md` | Raw Gemini Deep Research output |
| `chatgpt_report.md` | Raw ChatGPT Deep Research output |
| `manus_research_notes.md` | Independent research notes with URLs |
| `content.json` | Structured content ready for the PDF formatter |
| `{{BRAND_NAME}}_Report.pdf` | Final branded 2-page PDF |

---

## Execution Checklist

1. [ ] Fill in all `{{variables}}` in this playbook
2. [ ] Launch Gemini Deep Research with the master prompt
3. [ ] Launch ChatGPT Deep Research with the master prompt
4. [ ] Conduct Manus independent research (Reddit, filings, social media, web traffic)
5. [ ] Harvest Gemini report after ~30 min
6. [ ] Harvest ChatGPT report after ~30 min
7. [ ] Consolidate "best of 3" findings — select the 5 strongest
8. [ ] Classify each finding with a risk level
9. [ ] Run quality checklist on each finding
10. [ ] Build `content.json` from findings
11. [ ] Generate PDF with the PDF formatter skill
12. [ ] Upload all files to Google Drive
