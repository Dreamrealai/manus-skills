---
name: dreamreal
description: >
  Use when the user asks to
  generate/create/design
  any image, video, or
  audio
  - User mentions a
  specific AI model
  (Imagen, Veo, Flux,
  Seedance, etc.)
  - User wants to edit,
  assemble, or composite
  video/images
  - User wants to
  analyze, detect, or
  crop objects in images
  - User wants to run a
  creative workflow
  (product photography,
  storyboards, video
  assembly)
---

<!-- Auto-synced from DreamReal MCP update_mcp_skill v1.1.0 — 2026-04-29T03:36:37.743Z -->
<!-- To refresh: call dreamreal action=update_mcp_skill variant=both and rewrite this file -->

You have access to the DreamReal MCP server for AI image, video, and audio generation.

══════════════════════════════════════════════════
RULE 1: STAY ON THE STARTER ACTION SURFACE
══════════════════════════════════════════════════

This server does NOT expose `dreamreal_orchestrator` takeover mode unless
`enabled_actions` explicitly includes `use_orchestrator`.

For this starter/default surface:
  - Use `dreamreal` with nested `{ "action": "...", "params": { ... } }`
  - Or use the domain tools `dreamreal_create`, `dreamreal_edit`,
    `dreamreal_research`, and `dreamreal_manage`
  - Use `orchestrate: true` on generation actions when you want helper-mode
    prompt/model assistance
  - Do NOT call `dreamreal_orchestrator` or `use_orchestrator` unless the
    live `enabled_actions` list says they are available

══════════════════════════════════════════════════
RULE 2: PAYLOAD FORMAT — READ THIS CAREFULLY
══════════════════════════════════════════════════

ALL gateway tools use this shape: { "action": "<ACTION_NAME>", "params": { <PARAMS> } }
Params MUST be nested inside "params". NEVER put them at the top level.

IMPORTANT: Some actions have SUB-ACTIONS. The sub-action goes INSIDE params as "action".
This means the outer "action" is the category, and params.action is the specific operation.

══════════════════════════════════════════════════
SAFE STARTER EXAMPLES
══════════════════════════════════════════════════

--- List available models ---

Tool: dreamreal

Input: { "action": "list_models", "params": {} }

--- Generate an image (async) ---

Tool: dreamreal

Input: { "action": "generate_image", "params": { "prompt": "A sunset over mountains", "aspect_ratio": "16:9", "orchestrate": true } }

Then poll: { "action": "check_job_status", "params": { "job_id": "<JOB_ID>" } }

Optional: add "callback_url" to receive a terminal webhook instead of polling.

--- Generate MANY images in ONE call (BATCH, up to 25 — preferred for multi-image requests) ---

Tool: dreamreal

Input: { "action": "generate_image", "params": { "prompts": ["sunset over mountains", "misty forest at dawn", "neon Tokyo alley"], "aspect_ratio": "16:9" } }

Poll aggregated: { "action": "check_job_status", "params": { "batch_id": "<BATCH_ID>" } }

The server runs up to 6 in parallel with 1-5s jitter, auto-retries transient blips + content-policy blocks, and returns completed items progressively.

--- Generate a video (async) ---

Tool: dreamreal

Input: { "action": "generate_video", "params": { "prompt": "Ocean waves crashing on rocks", "duration_seconds": 8, "orchestrate": true } }

Then poll: { "action": "check_job_status", "params": { "job_id": "<JOB_ID>" } }

Optional: add "callback_url" to receive a terminal webhook instead of polling.

--- Generate audio/music ---

Tool: dreamreal

Input: { "action": "generate_audio", "params": { "prompt": "Upbeat electronic background music", "duration_seconds": 30 } }

--- Analyze an image ---

Tool: dreamreal

Input: { "action": "analyze", "params": { "action": "vision", "prompt": "Describe the composition", "image_urls": ["https://example.com/photo.jpg"] } }

--- Search assets ---

Tool: dreamreal

Input: { "action": "manage_assets", "params": { "action": "search", "query": "product hero", "limit": 20 } }

--- Upload a URL as reference ---

Tool: dreamreal

Input: { "action": "upload_media", "params": { "url": "https://example.com/ref.jpg", "purpose": "reference" } }

--- Refresh local MCP docs/skills ---

Tool: dreamreal

Input: { "action": "update_mcp_skill", "params": { "variant": "both" } }

══════════════════════════════════════════════════
RECOMMENDED: WEBHOOK CALLBACKS BEFORE POLLING
══════════════════════════════════════════════════

For long-running batches and clients that can receive inbound HTTPS, pass
callback_url (and optional callback_secret) on generate_image, generate_video,
or async generate_audio. DreamReal signs delivery with X-DR-Signature:
sha256=<hex(hmac-sha256(secret, raw request body bytes))>. Verify the raw body
before trusting the payload. Call get_setup_instructions for copy-paste Node.js
and Python HMAC verifier snippets, retry policy, and event names.

══════════════════════════════════════════════════
AVAILABLE TOOLS AND ACTIONS
══════════════════════════════════════════════════

This MCP server has a restricted action surface.

Enabled actions:
  - list_models
  - upload_media
  - generate_image
  - generate_video
  - generate_audio
  - check_job_status
  - get_setup_instructions
  - update_mcp_skill
  - get_setup_guide
  - refresh_skill
  - image_scraping
  - analyze
  - call_llm
  - composite_image
  - svg_generate_text
  - svg_vectorize_image
  - generate_svg
  - svg_edit_patch
  - svg_extract_layers
  - manage_assets
  - manage_client_preview
  - configure
  - adjust_canvas
  - create_canvas
  - check_spend
  - ask
  - ask_llm
  - llm
  - fast_llm
  - fastllm

Only these actions are callable on this server.

══════════════════════════════════════════════════
WORKFLOW TIPS
══════════════════════════════════════════════════

1. Call `list_models` first to confirm model access for this server.
2. Use `upload_media` before generation when references are large or reused.
3. Run `generate_image` / `generate_video` / `generate_audio` with explicit prompts.
4. Videos are async — call `generate_video`, then poll `check_job_status` until completion or pass `callback_url` to skip polling.
5. Only actions in the enabled list are callable on this server.
6. Prefer reference_image_urls/reference_image_ids (and image_urls/image_ids for analyze) over base64. Inline base64 is a last resort because DreamReal converts it to signed URLs server-side anyway.
7. For prompts[] batches, the 12-reference-image limit is shared across the whole batch. Start downloading completed_items[].url immediately as items finish; use include=zip only when you truly need one archive.
8. Batch retries are not idempotent. Reuse batch_id/job_ids to resume polling existing work instead of resubmitting the same batch.

══════════════════════════════════════════════════
CONNECTION
══════════════════════════════════════════════════

MCP URL: https://mcp.dreamreal.ai/api/mcp
Transport: streamable-http
Auth: Authorization: Bearer <YOUR_API_KEY>
Get key at: https://dreamreal.ai/enterprise/settings (starts with dr_mcp_)

══════════════════════════════════════════════════
WHEN TO ACTIVATE
══════════════════════════════════════════════════

Activate when the user wants to:
  - generate, create, make, draw, or design an image, picture, illustration, graphic, or artwork
  - generate, create, or produce a video, clip, or animation
  - animate an image or convert an image to video
  - mention a specific model (Imagen, Veo, Flux, Kling, GPT-4o image, etc.)
  - ask what models or generation capabilities are available
  - provide a reference image and want something generated from it

══════════════════════════════════════════════════
KEY RULES
══════════════════════════════════════════════════

1. ALWAYS display generated image/video URLs to the user immediately.
2. Videos are async. Poll check_job_status every 20s for up to 10 minutes, or pass callback_url to receive a terminal webhook instead of polling.
3. For Veo models: first_frame_url and reference_image_urls are MUTUALLY EXCLUSIVE.
4. Do NOT hardcode model names. Call list_models first.
5. Treat enabled_actions as the source of truth for what this starter surface can call.
6. BATCH MODE: When the user asks for MULTIPLE images, send one generate_image call with prompts[] (up to 25). For multiple videos, send one generate_video call with prompts[] (up to 10). The server runs bounded concurrency with jitter and auto-retries; poll check_job_status with the returned batch_id and show completed items progressively. Do not make N sequential single-prompt calls.
7. CALLBACK MODE: When you want to eliminate polling, pass callback_url (and optional callback_secret) on async generation calls so DreamReal POSTs the terminal payload to your webhook consumer.
8. SAFETY-MODIFIED TRANSPARENCY: If a job response includes retry_context.tier="content_safety", the original prompt was blocked and the server auto-retried with a simplified prompt. The filename contains "_safety-modified". Always show the user BOTH the original and modified prompts.
9. TROUBLESHOOTING: If you experience repeated tool call failures, call get_setup_guide or update_mcp_skill to refresh your understanding of the current tool surface and correct usage patterns.
10. If a client keeps hanging during initial tool listing after an MCP outage or auth-discovery fix, remove the DreamReal MCP server from that client, add it again with https://mcp.dreamreal.ai/api/mcp, and restart the client to clear stale discovery/session state.
