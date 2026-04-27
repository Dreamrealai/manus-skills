---
name: openrouter
description: Fast OpenRouter frontier-model toolkit with Gemini-aware routing, Opus 4.7, Sonnet 4.6, GPT 5.5, GPT 5.5 Pro, GPT 5.4, GLM 5.1, Grok 4.20, Kimi, DeepSeek, Qwen, MiniMax, and refreshable helper wrappers. Use when the user mentions opus, sonnet, claude, openrouter, GPT 5.5, GPT 5.5 Pro, ChatGPT 5.5, ChatGPT 5.5 Pro, GPT 5.4, ChatGPT 5.4 Pro, Grok, GLM, Kimi, DeepSeek, Qwen, MiniMax, or asks for a frontier chat model through OpenRouter.
---

# OpenRouter Skill

Use this skill for fast access to frontier text models through OpenRouter. Treat the user's stated model choice as binding unless the user explicitly asks for a fallback.

## Core Operating Rule

If the user names a model, use **only that model** unless the user explicitly asks for a fallback. If the user does not name a model, default to **Opus 4.7** unless the task clearly calls for a specialized helper such as **GPT 5.5 Pro** for maximum reasoning depth/fact-checking/audits, **GPT 5.5** for high-quality reasoning tasks, or **Sonnet 4.6** for speed.

| Situation | Required behavior |
|---|---|
| User names Opus 4.7, Opus 4.6, Sonnet 4.6, GPT 5.5, GPT 5.5 Pro, GPT 5.4, Kimi, GLM, Grok, or another model | Use that model only |
| User names a Gemini-family model through OpenRouter | Prefer direct Gemini API access first when the task can be completed there |
| User names no model | Default to Opus 4.7 unless a specialized helper is more appropriate for the task category |
| A requested alias is provisional or stale | Run refresh first, then update the alias explicitly |

## Quick Start

The fastest entry points are:

| Goal | Command |
|---|
| Default flagship chat | `python3 /home/ubuntu/skills/openrouter/scripts/openrouter_chat.py --alias opus-4.7 --prompt "..."` |
| GPT-5.5 standard (high reasoning) | `python3 /home/ubuntu/skills/openrouter/scripts/openrouter_chat.py --alias gpt-5.5 --reasoning high --prompt "..."` |
| GPT-5.5 extra-high reasoning | `python3 /home/ubuntu/skills/openrouter/scripts/openrouter_chat.py --alias gpt-5.5-xhigh --prompt "..."` |
| GPT-5.5 Pro (fact-check / audit) | `python3 /home/ubuntu/skills/openrouter/scripts/openrouter_chat.py --alias gpt-5.5-pro --prompt "..."` |
| Legacy Anthropic fallback | `python3 /home/ubuntu/skills/openrouter/scripts/openrouter_chat.py --alias opus-4.6 --prompt "..."` |
| Fast professional work | `python3 /home/ubuntu/skills/openrouter/scripts/openrouter_chat.py --alias sonnet-4.6 --prompt "..."` |
| Mixed-model comparison | `python3 /home/ubuntu/skills/openrouter/scripts/openrouter_batch.py --tasks tasks.json` |
| Refresh aliases and wrappers | `python3 /home/ubuntu/skills/openrouter/scripts/refresh_models.py --write-catalog --generate-wrappers` |
| Media requests from this skill | Defer to the Gemini skill's DreamReal-first media helper before any direct OpenRouter media fallback |

## Gemini-First Rule

OpenRouter may expose Gemini-family models, but if the user asks for a Gemini-family model and the task can be satisfied through the Gemini API directly, prefer the Gemini skill first. Use OpenRouter Gemini aliases only as a fallback path or when the user specifically asks for OpenRouter.

| Request type | Preferred route |
|---|---|
| Gemini family requested, no OpenRouter requirement | Gemini API first |
| Gemini family requested through OpenRouter explicitly | OpenRouter allowed |
| Gemini family fallback needed after direct Gemini issue | Use the OpenRouter Gemini alias |

## DreamReal-First Media Delegation

For **image, video, and music generation requested while using this skill**, do not improvise a direct OpenRouter media route first. Defer to the Gemini skill's DreamReal-first helper policy, then allow Gemini-family fallback, and only use other routes if the user explicitly asks.

| Media request | Required route |
|---|---|
| Image generation or editing | DreamReal MCP first through the Gemini media helper |
| Video generation | DreamReal MCP first through the Gemini media helper |
| Music generation | DreamReal MCP first through the Gemini media helper |

## Model Catalog

The canonical registry lives in `scripts/model_catalog.json`. It includes helper aliases for:

| Alias group | Coverage |
|---|---|
| `opus-4.7`, `opus-4.6`, `sonnet-4.6` | Anthropic flagship helpers |
| `gpt-5.5-pro` | GPT-5.5 Pro — best for fact-checking, audits, deep reasoning ($30/$180 per 1M tokens, xhigh reasoning) |
| `gpt-5.5`, `gpt-5.5-high`, `gpt-5.5-xhigh` | GPT-5.5 standard with configurable reasoning effort ($5/$30 per 1M tokens) |
| `gpt-5.4-pro`, `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.4-nano` | OpenAI GPT-5.4 legacy helpers |
| `kimi-k2.5`, `glm-5.1`, `grok-4.20` | User-requested non-Anthropic frontier helpers |
| `mystery-latest` | The most recent notable model candidate captured during refresh |
| `deepseek-v3.2`, `minimax-m2.7`, `qwen3.6-plus` | Additional state-of-the-art helpers |
| `gemini-3.1-pro-preview`, `gemini-3.0-flash-preview`, `gemini-3.1-flash-lite`, `gemini-3.1-flash-live`, `gemma-4` | Gemini-family OpenRouter fallbacks |

If an alias is marked refresh-required, do not guess. Run the refresh script and inspect the report.

## Helper Scripts

Use the pre-written scripts instead of ad hoc API calls.

| Script | Purpose |
|---|---|
| `scripts/openrouter_chat.py` | Fast single-model execution with alias routing and Gemini-aware provider selection |
| `scripts/openrouter_batch.py` | Up to 5 concurrent tasks with mixed models |
| `scripts/refresh_models.py` | Refresh the model catalog from current sources and regenerate helper wrappers |
| `scripts/generated/*.sh` | Auto-generated one-command wrappers for key aliases |

## Reasoning Modes

When the user requests reasoning, preserve that instruction. If the user does not specify a reasoning mode, use the helper default for the chosen alias.

| Alias | Default reasoning policy | Notes |
|---|
| `gpt-5.5-pro` | xhigh | Best for audits and fact-checking. Passes `reasoning={"effort": "xhigh"}` |
| `gpt-5.5-xhigh` | xhigh | GPT-5.5 standard with xhigh effort |
| `gpt-5.5`, `gpt-5.5-high` | high | GPT-5.5 standard with high effort |
| `gpt-5.4-pro` | high | Legacy GPT-5.4 Pro |
| `gpt-5.4` | medium | Legacy GPT-5.4 |
| `opus-4.7` | medium | Anthropic flagship |
| `opus-4.6` | medium | Anthropic legacy |
| `sonnet-4.6` | low | Fast Anthropic |
| `deepseek-v3.2` | high | DeepSeek |

### Reasoning Effort Levels (OpenAI/GPT-5.x series)

Passed via `extra_body={"reasoning": {"effort": "<level>"}}` or `--reasoning <level>` flag:

| Level | Token allocation | Use case |
|---|
| `xhigh` | ~95% of max_tokens for reasoning | Audits, fact-checking, complex multi-step problems |
| `high` | ~80% of max_tokens for reasoning | Deep analysis, research synthesis |
| `medium` | ~50% of max_tokens for reasoning | Standard tasks |
| `low` | ~20% of max_tokens for reasoning | Fast responses |
| `minimal` | ~10% of max_tokens for reasoning | Near-instant, simple tasks |
| `none` / `off` | No reasoning | Pure generation, no chain-of-thought |

## Batch Rule

Use the batch helper when the task involves multiple prompts, multiple models, or parallel audits. The default cap is **5 concurrent calls at a time**.

```bash
python3 /home/ubuntu/skills/openrouter/scripts/openrouter_batch.py --tasks tasks.json --max-concurrent 5
```

A task file may mix models such as Opus 4.7, Opus 4.6, GPT 5.4 Pro, Sonnet 4.6, GLM 5.1, DeepSeek V3.2, or Gemini-family fallbacks.

## Refresh Section

Refresh the registry before using a newly released model or when the user asks for the newest default.

```bash
python3 /home/ubuntu/skills/openrouter/scripts/refresh_models.py --write-catalog --generate-wrappers
```

The refresh routine should:

| Trigger | Action |
|---|---|
| User asks for the latest frontier model | Refresh before selecting a default |
| User asks for a just-released or mystery model | Refresh and inspect the report |
| An alias fails or looks stale | Refresh and regenerate wrappers |

The refresh routine updates the catalog and regenerates quick wrapper scripts in `scripts/generated/` so connection remains fast.

## Browser Connection Guidance

When the user asks for the newest model or model verification, confirm the current catalog through browser-based source checking or direct provider endpoints before changing defaults.

## Validation

After editing this skill, validate it and spot-test the helper inventory.

```bash
python3 /home/ubuntu/skills/skill-creator/scripts/quick_validate.py openrouter
python3 /home/ubuntu/skills/openrouter/scripts/openrouter_chat.py --list-aliases
```

## Strict Per-Call Limits

To prevent context degradation and ensure quality, a single LLM call using any model in this skill MUST NOT exceed:
- 5 text-to-video prompts generated or evaluated
- 5 video analyses performed
- 10 image analyses performed
- 10 image-to-video prompts generated or evaluated

If a task requires more items than these limits, it MUST be broken into multiple sequential or parallel LLM calls.
