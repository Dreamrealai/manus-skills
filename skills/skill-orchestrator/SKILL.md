---
name: skill-orchestrator
description: Master coordination layer for Manus skills. Use before planning any non-trivial task, any task that may involve multiple domains, or any request to combine, integrate, select, route, chain, or coordinate skills. Chooses primary and supporting skills, enforces read-before-plan behavior, resolves overlap, and builds cross-skill workflows for reports, dashboards, emails, apps, research, media, skill creation, automation, and external-service tasks.
---

# Skill Orchestrator

Use this skill as the first-pass routing and coordination layer for user requests that may benefit from one or more installed skills. The goal is **not** to load every skill every time. The goal is to identify the correct primary skill, add only necessary supporting skills, and make those skills work together in the right order.

## Core Rule

Before creating a task plan for any non-trivial request, perform a quick skill triage:

1. Identify the user’s requested outcome, domain, output format, destination, and constraints.
2. Select **one primary skill** that owns the main workflow.
3. Select **up to two supporting skills** for style, output format, platform integration, governance, or packaging.
4. Read the selected skill files before planning or execution.
5. If no installed skill fits, proceed normally and note no skill was required.

Do not read every skill by default. Reading all skills wastes context and can create conflicting instructions. Prefer the most specific domain skill over a general formatting or style skill.

## Selection Priority

When multiple skills appear relevant, resolve overlap in this order:

| Priority | Skill Type | Rule |
|---:|---|---|
| 1 | Safety, publishing, sending, applying, or live-service operation | Follow the skill and platform confirmation requirements before taking action. |
| 2 | Domain-specific workflow | Use the skill that owns the subject matter, such as recon reporting, construction documentation, manuscript review, vendor monitoring, or job applications. |
| 3 | Output format | Add skills for dashboards, spreadsheets, reports, slide decks, email, or motion graphics when that format is requested. |
| 4 | Style, brand, or language | Add brand, executive, email, or humanization skills after the core workflow is chosen. |
| 5 | Tools and infrastructure | Add persistent-computing, GitHub solution search, Google Workspace, Manus API, or external-service skills only when the task requires that environment or integration. |

If skill instructions conflict, follow the most specific domain skill first, then the output-format skill, then style/brand guidance. Never use a supporting skill to override a primary skill’s safety rules.

## Routing Map

| User Intent | Primary Skill | Supporting Skills to Consider |
|---|---|---|
| Draft, refine, or send an email | email-ops for real mailbox work; email-drafter or email-writer for drafting | executive-secretary for leadership tone; gws-best-practices for Google Workspace files |
| Prepare executive memo, agenda, minutes, action tracker, board material, or bilingual corporate communication | executive-secretary or executive-management-reporting-assistant | reporting; excel-generator; manus-brand-guideline |
| Create a report, dashboard, analytics view, chart, visualization, scheduled report, or spreadsheet | reporting-dashboards, dashboard-builder, dashboard, or excel-generator | reporting; agency-data-consolidation-agent; Test Reporting & Dashboards; manus-brand-guideline |
| Produce cybersecurity reconnaissance findings, CVSS scoring, MITRE mapping, or handoff package | reporting | reporting-dashboards or dashboard-builder only if visualization is requested |
| Build or update a website, app, admin dashboard, or dashboard screen | dashboard or dashboard-create-screen when relevant | github-gem-seeker; manus-brand-guideline; persistent-computing if persistent runtime is needed |
| Create, update, publish, promote, or find skills | skill-creator-v2 for creation or update; internet-skill-finder for discovery; promote-skill for promotion | github-gem-seeker; manus-brand-guideline |
| Review or manage manuscripts | manuscript-writing-review for prose review; manuscript-as-code for reproducible manuscript pipeline | reporting; excel-generator |
| Prepare construction documentation or construction administration artifacts | construction-documentation | executive-secretary; reporting; excel-generator |
| Build vendor privacy monitoring, governance, reassessment, renewal, KPI, or dashboard workflows | vendor-monitoring-program | executive-management-reporting-assistant; reporting-dashboards; excel-generator |
| Automate LinkedIn or Dice job applications | linkedin-easy-apply or dice-easy-apply | email-writer; persistent-computing for recurring automation |
| Generate music, motion graphics, animated diagrams, or media assets | music-prompter for music; motion-graphics for animated video | manus-brand-guideline; reporting for scripts or explanatory structure |
| Use Google Drive, Docs, Sheets, or Slides from the command line | gws-best-practices | excel-generator; executive-secretary; reporting-dashboards |
| Delegate or orchestrate Manus API / external Manus agents | manus, Manus AI Agent Integration, or manus-api | persistent-computing when building bots or long-running automations |
| Post or interact on Clawk, manage Things tasks, or use platform-specific connectors | clawk or things-mac | executive-secretary or email-writer for wording |
| Evaluate an important decision or review a plan automatically | council for high-stakes tradeoffs; autoplan for full plan review gauntlet | executive-management-reporting-assistant; reporting |
| Humanize Malaysian Bahasa Melayu or detect Indonesian intrusion | manusiawi | email-writer or manuscript-writing-review only if the genre requires it |

## Workflow Patterns

### Single-Skill Workflow

Use when the task has one clear owner. Read that skill, follow it, and produce the requested output. Example: for “humanize this BM text,” use `manusiawi` without adding unrelated writing skills unless the user asks for an email, manuscript, or executive memo.

### Primary Plus Format Workflow

Use when the domain and deliverable format differ. Read the domain skill first, then the format skill. Example: for “turn vendor monitoring KPIs into a board dashboard,” read `vendor-monitoring-program` first, then `reporting-dashboards` or `excel-generator`, then apply executive summary standards if needed.

### Primary Plus Style Workflow

Use when the workflow is clear but the audience or tone matters. Read the primary skill first, then the style skill. Example: for “write a board-ready incident update,” use the incident or reporting skill first, then `executive-secretary` or `executive-management-reporting-assistant` for leadership tone.

### Multi-Stage Production Workflow

Use when the final artifact requires sequential stages. A common pattern is: domain analysis → data or evidence organization → output format → style/brand polish → delivery. Example: a sales dashboard may combine `agency-data-consolidation-agent`, `excel-generator`, `reporting-dashboards`, and `manus-brand-guideline`, but read only the skills needed for the actual deliverables.

### Skill Lifecycle Workflow

For any request to create, update, improve, package, publish, or promote a skill, read `skill-creator-v2` first and follow its workflow. Use `internet-skill-finder` only when discovering external skills. Use `promote-skill` only when the user asks to distribute a skill across marketplaces or public channels.

## Mandatory Pre-Reads

Some skills must be read before specific actions:

| Condition | Required Skill |
|---|---|
| Creating or editing skills | skill-creator-v2 |
| Generating music or entering music generation workflow | music-prompter |
| Persistent services, bots, Docker, fixed IP, background jobs, heavy compute, or reusable environments | persistent-computing |
| Google Workspace CLI operations | gws-best-practices |
| Manus-branded visual artifacts | manus-brand-guideline |
| Real mailbox triage, sending, or proof of sent mail | email-ops |
| LinkedIn Easy Apply automation | linkedin-easy-apply |
| Dice Easy Apply automation | dice-easy-apply |
| Recon reports, findings, CVSS scoring, MITRE mapping, or evidence handoff | reporting |

## Confirmation and Safety

Before actions that send, post, publish, submit, apply, delete, pay, or modify live external data, ask the user for confirmation unless the relevant skill already defines a stricter procedure. Do not guess credentials, personal information, recipients, job-application answers, or account-specific settings. When a task depends on an external service that is not enabled, inspect available connectors or ask a concise clarification question.

## Improvement Loop

If a selected skill causes repeated retries, ambiguity, missing steps, or an avoidable workaround, finish the user’s task if possible and then suggest a concrete skill improvement. Phrase the improvement as an actionable edit, such as “Add a fallback for missing dashboard data” or “Clarify when to use CVSS 3.1 dual reporting.”

## Output Expectations

At delivery, briefly state which skills were coordinated and why. If the task produced files, attach the final artifacts and the most important supporting files. Keep the user-facing explanation concise unless the user asked for detailed reasoning.
