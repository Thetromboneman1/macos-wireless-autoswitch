# Executive Summary

Review date: 2026-06-24.

The ten candidate repositories were verified against current GitHub metadata and shallow-cloned into `/tmp/codex-ai-repo-review-2026-06-24` for static inspection. The local host is an Apple Silicon Mac running macOS 26.5.1 with oMLX healthy at `http://127.0.0.1:18080`, the GGUF coding lane available at `http://127.0.0.1:8002`, and the Rapid-MLX lab lane not running during validation.

## What Changed

- Added this dated review package under `docs/ai-trending-repos/2026-06-24/`.
- Added pinned upstream inventory at `config/ai-trending-repos/upstream-versions-2026-06-24.json`.
- Added validation evidence at `config/ai-trending-repos/validation-results-2026-06-24.json`.
- Added an execution checklist at `docs/superpowers/plans/2026-06-24-ai-repository-review.md`.

No candidate was globally installed into Codex, OpenCode, Hermes, Goose, MCP configs, launch agents, Docker, or Apple containers during this pass.

## Decisions

| Candidate | Decision | Reason |
|---|---|---|
| NVIDIA SkillSpector | ADOPT_LIMITED | Useful as an isolated pre-install skill scanner; static mode worked and caught a synthetic malicious skill. |
| Agent-Reach | ADOPT_LIMITED | Public/no-credential channels can be used cautiously; cookie/session channels require separate approval. |
| Headroom | PILOT | Potential value for log/tool-output compression, but local source build exceeded the bounded validation window. |
| Addy Osmani Agent Skills | PILOT | Useful skill source, but only after SkillSpector plus manual review; no bulk install. |
| Codebase Memory MCP | PILOT | Promising local code graph MCP, but installer writes agent configs and indexes code; needs allowlisted pilot. |
| PaddleOCR | PILOT | Useful OCR gap exists locally, but dependencies/model storage need a contained proof of concept. |
| AgentsView | PILOT | Good fit for local transcript analytics, but indexes sensitive agent history and telemetry must be disabled. |
| OpenMontage | DEFER | Large AGPL media/agent surface with many skills/tools; requires isolated creative pilot. |
| Flue | DEFER | Interesting TypeScript agent harness, but local `pnpm` is absent and sandbox claims need deeper review. |
| LMCache | REJECT_INCOMPATIBLE | Current production stack is oMLX/MLX plus llama.cpp on Apple Silicon; LMCache is primarily vLLM/Linux/GPU oriented. |

## Readiness

Environment status: **READY WITH LIMITATIONS**.

The review artifacts are ready to use as the gate for follow-up pilots. The environment should not be considered to have adopted the full candidate set until each pilot has isolated install automation, measured local value, rollback, and fresh security validation.
