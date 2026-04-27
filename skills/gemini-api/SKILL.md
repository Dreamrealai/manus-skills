---
name: gemini-api
description: Fast Gemini and DreamReal execution toolkit for Gemini 3.1, Veo 3.1, Lyria 3, Gemma 4, Gemini deep research, and Gemini-family fallbacks. Use when the user mentions gemini, nano banana, veo, lyria, gemma, deep research, gemini live, flash image, flash lite, gemini tts, or asks for Google model usage. Also use when image, music, or video generation may need DreamReal MCP first with Gemini fallback.
---

# Gemini API Skill

Use this skill to connect quickly to the Gemini API and to route media generation safely. Treat this skill as the default operating guide for **Gemini-family tasks**.

## Core Operating Rule

Honor the user's model choice first. If the user names a specific model, use **only that model** unless it is unavailable and the user permits a fallback. If the user does not name a model, use the **newest, strongest, and most capable helper-listed model** for the task by default.

| Situation | Required behavior |
|---|---|
| User names a Gemini model | Use that model only unless the user approves a fallback |
| User names no model | Use the highest-end default helper for the task |
| User asks for image, music, or video generation | Try DreamReal MCP first, then Gemini-native generation, then other fallbacks only if needed |
| User asks for Gemini-family model through OpenRouter | Prefer direct Gemini API access first when the task can be satisfied there |

## Quick Start

On the first Gemini invocation in a thread, run the SDK bootstrap and then use a helper script instead of writing ad hoc code.

```bash
bash /home/ubuntu/skills/gemini-api/scripts/ensure_gemini_sdk.sh
```

The fastest entry points are:

| Goal | Command |
|---|---|
| High-end Gemini chat or analysis | `python3 /home/ubuntu/skills/gemini-api/scripts/gemini_quick.py --alias gemini-3.1-pro-preview --prompt "..."` |
| Fast Gemini chat or analysis | `python3 /home/ubuntu/skills/gemini-api/scripts/gemini_quick.py --alias gemini-3.0-flash-preview --prompt "..."` |
| Cheap high-volume Gemini work | `python3 /home/ubuntu/skills/gemini-api/scripts/gemini_quick.py --alias gemini-3.1-flash-lite --prompt "..."` |
| Gemini Live setup | `python3 /home/ubuntu/skills/gemini-api/scripts/gemini_quick.py --alias gemini-3.1-flash-live --prompt "..."` |
| Image generation or editing | `python3 /home/ubuntu/skills/gemini-api/scripts/gemini_media.py --mode image --prompt "..."` |
| Video generation | `python3 /home/ubuntu/skills/gemini-api/scripts/gemini_media.py --mode video --prompt "..."` |
| Music generation | `python3 /home/ubuntu/skills/gemini-api/scripts/gemini_media.py --mode music --prompt "..."` |
| Batch processing with 5 concurrent calls | `python3 /home/ubuntu/skills/gemini-api/scripts/gemini_batch.py --tasks tasks.json` |
| Refresh the helper catalog | `python3 /home/ubuntu/skills/gemini-api/scripts/refresh_models.py --provider gemini --write-catalog --generate-wrappers` |

## Model Catalog Policy

The canonical helper registry is stored in `scripts/model_catalog.json`. Read it when you need the exact alias list or task routing behavior. The registry includes the helper aliases requested by the user, including:

| Alias family | Intended helper coverage |
|---|---|
| `gemini-3.1-pro-preview` | Flagship reasoning and complex analysis |
| `gemini-3.0-flash-preview` | Fast chat and multimodal work |
| `gemini-3.1-flash-lite` | Low-cost bulk execution |
| `gemini-3.1-flash-live` | Live interactive tasks |
| `deep-research` | Long-running autonomous research |
| `gemma-4` | Gemma-family access |
| `gemini-3.1-flash-image-preview` | Nano Banana image generation and editing |
| `gemini-2.5-pro-tts` | TTS helper |
| `veo-3.1-image-to-video`, `veo-3.1-reference-to-video`, `veo-3.1-text-to-video`, `veo-3.1-start-end-frame-preview` | Video helper routes |
| `lyria-3-clip`, `lyria-3-preview` | Music generation helpers |

If an alias is marked refresh-required in the catalog, run the refresh script before first use and update the alias target rather than guessing.

## DreamReal-First Media Rule

For **image, music, and video generation**, prefer DreamReal MCP first. Only move to Gemini-native generation when DreamReal cannot satisfy the request, the requested model is specifically Gemini, or the user explicitly asks for Gemini first.

| Media task | First choice | Second choice | Third choice |
|---|---|---|---|
| Image generation or editing | DreamReal MCP | Gemini image helper | Other approved fallback |
| Video generation | DreamReal MCP | Gemini Veo helper | Other approved fallback |
| Music generation | DreamReal MCP | Gemini Lyria helper | Other approved fallback |

When falling back, preserve the original prompt and note the provider switch in the task log or final report.

## Helper Scripts

Use the pre-written scripts instead of building one-off requests.

| Script | Purpose |
|---|---|
| `scripts/gemini_quick.py` | Fast chat, analysis, JSON extraction, and direct Gemini alias execution |
| `scripts/gemini_media.py` | DreamReal-first image, video, and music routing with Gemini fallback |
| `scripts/gemini_batch.py` | Up to 5 concurrent Gemini or mixed-helper executions |
| `scripts/refresh_models.py` | Refresh helper aliases, regenerate wrapper scripts, and report newly discovered model candidates |
| `scripts/gemini_orchestrator.py` | Legacy batch helper retained for existing flows |
| `scripts/deep_research.py` | Deep research execution |

## Batch Rule

For repeated work, use the batch helper rather than sequential loops. The default cap is **5 concurrent calls at a time**, because the user requested this explicitly.

```bash
python3 /home/ubuntu/skills/gemini-api/scripts/gemini_batch.py --tasks tasks.json --max-concurrent 5
```

A task file may mix multiple aliases. Use this when the user wants a combination of Gemini 3.1 Pro, Flash variants, image helpers, or media fallbacks in one run.

## Refresh Section

Before using newly announced models, or when the user asks for the latest model, refresh the helper registry.

```bash
python3 /home/ubuntu/skills/gemini-api/scripts/refresh_models.py --provider gemini --write-catalog --generate-wrappers
```

The refresh routine should be used when any of the following are true.

| Trigger | Action |
|---|---|
| The user asks for the newest Gemini model | Run refresh before selecting the default |
| A helper alias looks stale or fails | Run refresh and inspect the proposed replacements |
| The user asks for a just-released model | Run refresh and add or update the alias entry |

Refresh does not silently replace user-requested models. It updates the catalog suggestions, regenerates quick wrappers in `scripts/generated/`, and makes changes explicit.

## Browser Connection Guidance

If the task requires browser-connected research, verify the current model landscape with browser-based source checking before updating aliases or defaults. Save the key findings to a local note file immediately after every two browser operations so the evidence is preserved.

## Deep Research Guidance

**Browser-first, API-fallback.** Gemini Deep Research MUST use the browser extension at `gemini.google.com` as the primary method. The API script is a fallback only.

| Priority | Method | When to use |
|---|---|---|
| **1 (Primary)** | Browser: `gemini.google.com` → Tools → Deep Research | Always try first. Supports full deep research agent with search grounding. |
| **2 (Fallback)** | API: `scripts/deep_research.py` | Only when browser is unavailable, login fails, or user explicitly requests API. The Interactions API can be slow (10+ min polling) and may stall. |

### Browser Deep Research Procedure

1. Navigate to `https://gemini.google.com`.
2. Click **Tools** below the prompt box → select **Deep research**.
3. Paste the research prompt into the text area and submit.
4. Note the start timestamp. Deep research typically takes 2–10 minutes.
5. Monitor for the "Research complete" indicator. The report appears inline.
6. Copy the full report text (including citations) and save to the target output file.
7. If the report is nested or collapsed, scroll to expand all sections before copying.

### API Fallback (only if browser fails)

```bash
python3 /home/ubuntu/skills/gemini-api/scripts/deep_research.py --prompt "Research ..." --output report.md
```

The API script uses the Interactions API (`deep-research-pro-preview-12-2025` agent) with polling. Known issues: can stall at `in_progress` for extended periods. Set `--timeout 1800` for long research. If it stalls beyond 10 minutes with no progress change, kill and retry via browser.

## Validation

After editing this skill, validate it and spot-test at least one helper.

```bash
python3 /home/ubuntu/skills/skill-creator/scripts/quick_validate.py gemini-api
python3 /home/ubuntu/skills/gemini-api/scripts/gemini_quick.py --list-aliases
```

## Strict Per-Call Limits

To prevent context degradation and ensure quality, a single LLM call using any model in this skill MUST NOT exceed:
- 5 text-to-video prompts generated or evaluated
- 5 video analyses performed
- 10 image analyses performed
- 10 image-to-video prompts generated or evaluated

If a task requires more items than these limits, it MUST be broken into multiple sequential or parallel LLM calls.
