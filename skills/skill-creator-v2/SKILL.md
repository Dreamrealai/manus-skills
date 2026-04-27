---
name: skill-creator-v2
description: Guide for creating or updating skills that extend Manus via specialized knowledge, workflows, or tool integrations. Includes browser extension integration for skill publishing. For any modification or improvement request, MUST first read this skill and follow its update workflow instead of editing files directly.
license: Complete terms in LICENSE.txt
---

# Skill Creator

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend Manus's capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks—they transform Manus from a general-purpose agent into a specialized agent equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else Manus needs: system prompt, conversation history, other Skills' metadata, and the actual user request.

**Default assumption: Manus is already very smart.** Only add context Manus doesn't already have. Challenge each piece of information: "Does Manus really need this explanation?" and "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

**High freedom (text-based instructions)**: Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.

**Medium freedom (pseudocode or scripts with parameters)**: Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.

**Low freedom (specific scripts, few parameters)**: Use when operations are fragile and error-prone, consistency is critical, or a specific sequence must be followed.

Think of Manus as exploring a path: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── templates/        - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md (required)

Every SKILL.md consists of:

- **Frontmatter** (YAML): Contains `name` and `description` fields. These are the only fields that Manus reads to determine when the skill gets used, thus it is very important to be clear and comprehensive in describing what the skill is, and when it should be used.
- **Body** (Markdown): Instructions and guidance for using the skill. Only loaded AFTER the skill triggers (if at all).

#### Bundled Resources (optional)

- **`scripts/`** - Executable code for repetitive or deterministic tasks (e.g., `rotate_pdf.py`). Token efficient, can run without loading into context.
- **`references/`** - Documentation loaded as needed (schemas, API docs, policies). Keeps SKILL.md lean. For large files (>10k words), include grep patterns in SKILL.md.
- **`templates/`** - Output assets not loaded into context (logos, fonts, boilerplate code).

**Avoid duplication**: Information lives in SKILL.md OR references, not both.

**Do NOT include**: README.md, CHANGELOG.md, or other auxiliary documentation. Skills are for AI agents, not users.

### Progressive Disclosure

Three-level loading system:
1. **Metadata** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<500 lines)
3. **Bundled resources** - As needed

Keep SKILL.md under 500 lines. When splitting content to references, clearly describe when to read them.

**Key principle:** Keep core workflow in SKILL.md; move variant-specific details to reference files.

Example structure for multi-domain skills:

```
bigquery-skill/
├── SKILL.md (overview + navigation)
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```

Manus only loads the relevant reference file when needed.

## Skill Creation Process

Skill creation involves these steps:

1. Activate Browser Extension: Immediately ask the user to approve browser extension usage.
2. Understand the skill with concrete examples
3. Plan reusable skill contents (scripts, references, templates)
4. Initialize the skill (run init_skill.py)
5. Edit the skill (implement resources and write SKILL.md)
6. Publish the skill: ALL skill changes (new skills, updates, improvements) MUST be pushed to the canonical `manus-skills` GitHub repository, followed by a deprecation/disable step for any older versions via the Manus browser.
7. Iterate based on real usage

Follow these steps in order, skipping only if there is a clear reason why they are not applicable.

### Step 1: Activate Browser Extension

Immediately upon triggering this skill, before doing any other work, ask the user to approve browser extension usage. Wait for their approval. This is required because publishing the skill in Step 6 relies on the browser extension.

### Step 2: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood.

Gather concrete examples of how the skill will be used. Ask questions like:
- "What functionality should this skill support?"
- "Can you give examples of how it would be used?"

Avoid asking too many questions at once. Conclude when you have a clear sense of the functionality.

### Step 3: Planning the Reusable Skill Contents

For each example, identify reusable resources:

| Resource Type | When to Use                     | Example                               |
| ------------- | ------------------------------- | ------------------------------------- |
| `scripts/`    | Code rewritten repeatedly       | `rotate_pdf.py` for PDF rotation      |
| `templates/`  | Same boilerplate each time      | HTML/React starter for webapp builder |
| `references/` | Documentation needed repeatedly | Database schemas for BigQuery skill   |

### Step 4: Initializing the Skill

At this point, it is time to actually create the skill.

Skip this step only if the skill being developed already exists, and iteration or packaging is needed. In this case, continue to the next step.

When creating a new skill from scratch, always run the `init_skill.py` script. The script conveniently generates a new template skill directory that automatically includes everything a skill requires, making the skill creation process much more efficient and reliable.

Usage:

```bash
python /home/ubuntu/skills/skill-creator/scripts/init_skill.py <skill-name>
```

The script:

- Creates the skill directory at `/home/ubuntu/skills/<skill-name>/`
- Generates a SKILL.md template with proper frontmatter and TODO placeholders
- Creates example resource directories: `scripts/`, `references/`, and `templates/`
- Adds example files in each directory that can be customized or deleted

After initialization, customize or remove the generated SKILL.md and example files as needed.

### Step 5: Edit the Skill

When editing the (newly-generated or existing) skill, remember that the skill is being created for another instance of Manus to use. Include information that would be beneficial and non-obvious to Manus. Consider what procedural knowledge, domain-specific details, or reusable assets would help another Manus instance execute these tasks more effectively.

#### Learn Proven Design Patterns

Consult these helpful guides based on your skill's needs:

- **Multi-step processes**: See `/home/ubuntu/skills/skill-creator/references/workflows.md` for sequential workflows and conditional logic
- **Output formats or quality standards**: See `/home/ubuntu/skills/skill-creator/references/output-patterns.md` for template and example patterns
- **Progressive Disclosure Patterns**: See `/home/ubuntu/skills/skill-creator/references/progressive-disclosure-patterns.md` for splitting content across files.

These files contain established best practices for effective skill design.

#### Start with Reusable Skill Contents

Begin with the `scripts/`, `references/`, and `templates/` files identified in Step 2. This may require user input (e.g., brand assets for `templates/`, documentation for `references/`).

Test added scripts by running them to ensure they work correctly. For many similar scripts, test a representative sample.

Delete any unused example files from initialization.

#### Update SKILL.md

**Writing Guidelines:** Always use imperative/infinitive form.

##### Frontmatter

Write the YAML frontmatter with `name` and `description`:

- `name`: The skill name
- `description`: Primary trigger mechanism. Must include what the skill does AND when to use it (body only loads after triggering).
  - Example: "Document creation and editing with tracked changes. Use for: creating .docx files, modifying content, working with tracked changes."

##### Body

Write instructions for using the skill and its bundled resources.

### Step 6: Publishing the Skill

Once development of the skill is complete, validate it first:

```bash
python /home/ubuntu/skills/skill-creator-v2/scripts/quick_validate.py <skill-name>
```

If validation fails, fix the errors and run validation again.

Once validated, you MUST publish the skill to the user's account. **ALL skill changes, updates, and new skills MUST go through the canonical GitHub repository workflow going forward.**

**The Canonical GitHub Workflow (Mandatory)**
1. Push the skill directory to the user's canonical `manus-skills` GitHub repository at `https://github.com/Dreamrealai/manus-skills/tree/main/skills/<skill-name>`.
2. Use the `browser_navigate` tool to open `https://manus.im/app#settings/skills`.
3. **For new skills:** Click `+ Add` -> `Import from GitHub` and paste the repository subdirectory URL.
4. **For updates to existing skills:** You MUST first click the `...` menu on the existing skill in the Settings panel and select `Delete` to remove the outdated version, then use `+ Add` -> `Import from GitHub` to pull the fresh version from the canonical repo. (Note: The `Replace` option in the UI is for `.skill` file uploads, not GitHub syncs).

**Deprecating Old Versions (Mandatory Step)**
If you are creating a "v2" or replacing an entirely different skill:
1. Use the `browser_navigate` tool to open `https://manus.im/app#settings/skills`.
2. Locate the old/expired skill in the list.
3. Click its toggle switch to turn it off (grey/disabled), or click the `...` menu and select `Delete` to remove it entirely if requested.
4. This ensures the agent does not trigger conflicting or outdated instructions.

*(Optional Fallback)* **The Browser Extension Click-to-Add Workflow (For Contextual Saving)**
1. Ensure the browser extension was activated in Step 1.
2. Use the `browser_navigate` tool to open the `manus.im` page.
3. Locate the originating thread where the skill was requested.
4. Click the "Move to project" or "Add to Project" button in the UI to save the thread contextually.

After publishing, you can also use the `message` tool to send the SKILL.md file as an attachment as a fallback:

```
/home/ubuntu/skills/{skill-name}/SKILL.md
```

### Step 7: Iterate

After testing the skill, users may request improvements. Often this happens right after using the skill, with fresh context of how the skill performed.

**Iteration workflow:**

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again

**Proactive improvement rule:** When executing ANY skill, if the workflow encounters errors, unexpected behavior, excessive retries (more than 2 attempts at the same step), or workarounds, MUST proactively suggest specific improvements to that skill's SKILL.md or bundled resources before completing the task. Frame suggestions as actionable edits (e.g., "Add a fallback for X in step Y" or "Update the script to handle Z"). Ask the user: "I noticed [issue] while running [skill-name]. Would you like me to update the skill to handle this better?" Do not silently work around skill deficiencies—surface them so skills continuously improve.

## Strict Per-Call Limits

To prevent context degradation and ensure quality, a single LLM call MUST NOT exceed:
- 5 text-to-video prompts generated or evaluated
- 5 video analyses performed
- 10 image analyses performed
- 10 image-to-video prompts generated or evaluated

If a task requires more items than these limits, it MUST be broken into multiple sequential or parallel LLM calls.
