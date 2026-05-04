# Skill Orchestration Reference Map

This reference expands the routing logic in `SKILL.md`. Load it only when a user request is broad, ambiguous, or likely to involve several skills.

| Task Family | Primary Skills | Supporting Skills | Coordination Pattern |
|---|---|---|---|
| Executive communication and management reporting | executive-secretary; executive-management-reporting-assistant | email-writer; reporting; manus-brand-guideline; excel-generator | Start with executive audience, choose language, structure decision-ready content, apply report or brand formatting, then produce email, memo, table, deck content, or dashboard concept. |
| Email drafting and mailbox operations | email-ops; email-drafter; email-writer | executive-secretary; gws-best-practices | Use mailbox workflow when interacting with real mail surfaces; use drafting skills for tone and structure; use executive skills for leadership context. |
| Reports, dashboards, analytics, and spreadsheets | reporting-dashboards; dashboard-builder; dashboard; excel-generator | reporting; agency-data-consolidation-agent; Test Reporting & Dashboards; manus-brand-guideline | Determine whether the output is a written report, spreadsheet, static dashboard screen, operational dashboard, ServiceNow report, test dashboard, or sales data consolidation. Combine data analysis, visual formatting, and reporting standards. |
| Cybersecurity reconnaissance reporting | reporting | dashboard-builder; reporting-dashboards | Use reporting for recon structure, findings, CVSS v4.0, MITRE mapping, evidence handling, and handoff checklists. Use dashboards only if the user asks for visualization or monitoring. |
| Web, app, dashboard, and persistent systems | dashboard-create-screen; dashboard; persistent-computing | github-gem-seeker; manus-brand-guideline; reporting-dashboards | For websites/apps, initialize the appropriate project first. Use persistent-computing when the task needs bots, Docker, fixed IP, background jobs, or reusable environments. |
| Manus skills lifecycle | skill-creator-v2; skill-creator; promote-skill; internet-skill-finder | github-gem-seeker; manus-brand-guideline | For creating or updating skills, read skill-creator-v2 first, follow validation and publishing workflow, and use promote-skill only for marketplace distribution. |
| Research manuscripts and academic writing | manuscript-writing-review; manuscript-as-code | reporting; excel-generator; gws-best-practices | Use writing review for prose quality; use manuscript-as-code for reproducible repo/build pipelines; use reporting only when summarizing findings. |
| Construction and vendor governance | construction-documentation; vendor-monitoring-program | executive-secretary; reporting; excel-generator | Use domain skill as primary; use reporting and executive skills for governance summaries, trackers, and leadership-ready outputs. |
| Job applications and career automation | linkedin-easy-apply; dice-easy-apply | email-writer; persistent-computing | Apply conservative guardrails, verify resume assets, and use persistent-computing only for recurring/background automation not suited to normal sandbox execution. |
| Media and creative production | music-prompter; motion-graphics | manus-brand-guideline; reporting | Read music-prompter before music generation. Use motion-graphics for animated videos and visual explainers; apply brand guidance when relevant. |
| External services, APIs, and platform integrations | manus; Manus AI Agent Integration; manus-api; gws-best-practices; things-mac; clawk | email-ops; persistent-computing | Use the service-specific skill only when the user’s requested destination or platform matches that service. Do not guess accounts or publish/post without confirmation. |
| Decision support and planning review | council; autoplan | executive-management-reporting-assistant; reporting | Use council for genuine decisions with stakes and tradeoffs. Use autoplan when the user asks for full CEO/design/engineering review automation. |
| Language refinement | manusiawi; email-writer; manuscript-writing-review | executive-secretary | Use manusiawi for Malaysian Bahasa Melayu humanization and Indonesian-intrusion detection; use email/manuscript skills for their specific genres. |

## Cross-Skill Rules

Choose one primary skill and no more than two supporting skills unless the user explicitly requests a broad pipeline. Read the primary skill first. Read supporting skills only when their procedures are necessary. If instructions conflict, prioritize the most specific domain skill, then output-format skill, then style/brand skill.

Always apply confirmation rules before using skills that post externally, send email, submit job applications, modify live services, publish content, or delete data.
