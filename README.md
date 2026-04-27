# manus-skills

**David Chen's personal Manus agent skills library.**

Skills are modular, reusable capability packs that extend what Manus can do — each one is a directory containing a `SKILL.md` instruction file plus optional scripts, references, and templates.

---

## How to Import a Skill into Manus

1. Go to **Manus → Profile → Settings → Skills**
2. Click **+ Add → Import from GitHub**
3. Paste the URL for the specific skill subfolder (see table below)
4. Click **Import** — the skill is immediately available globally across all your tasks

> **Note:** Manus imports from the root of a GitHub repo. To import a single skill from this multi-skill repo, point to the skill's subdirectory URL.

---

## Skills in This Library

| Skill | Description | Import URL |
|---|---|---|
| **skill-creator-v2** | Enhanced skill creator with auto browser-extension activation and post-save project-linking flow | `https://github.com/Dreamrealai/manus-skills/tree/main/skills/skill-creator-v2` |

---

## Naming Convention

Each skill lives at `skills/{skill-name}/` and must contain:

```
skills/
  {skill-name}/
    SKILL.md          ← Required: instructions Manus reads at runtime
    LICENSE.txt       ← Optional but recommended
    references/       ← Optional: supporting docs, workflows, examples
    scripts/          ← Optional: helper Python/shell scripts
```

---

## Adding a New Skill

1. Create a new directory under `skills/`
2. Add a `SKILL.md` following the [skill-creator-v2](skills/skill-creator-v2/SKILL.md) template
3. Commit and push
4. Import into Manus via the GitHub import flow above

---

## Repository

- **Org:** [Dreamrealai](https://github.com/Dreamrealai)
- **Repo:** [manus-skills](https://github.com/Dreamrealai/manus-skills)
- **Visibility:** Public (required for Manus GitHub import)
