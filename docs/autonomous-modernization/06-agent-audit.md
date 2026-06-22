# 06 - Agent Audit

## Current Agent Stack

| Tool | State | Decision |
| --- | --- | --- |
| Codex CLI / app | Present, cloud-backed | Do not force local-only; keep cloud fallback. |
| OpenCode | Present, sees oMLX and GGUF providers | Keep oMLX small model and GGUF coding lane available. |
| VS Code | Present, GitLens AI uses VS Code/Copilot model | Do not alter without explicit IDE workflow request. |
| Hermes | Present, dirty workspace with local AI edits | Do not commit unrelated Hermes changes from this repo. |
| OpenClaw | Present, dirty Docker compose | Audit separately before modifying. |
| MCP configs | Present in VS Code and Codex app caches | No secret-bearing config edits. |

## Change From This Pass

No new agent framework was installed. The prior OpenCode host URL fix remains the key local wiring change.

## Recommended Workflow

- Default fast/small agent work: oMLX E4B.
- Default coding lane when explicitly selected: llama.cpp GGUF 26B A4B.
- Reasoning: oMLX 31B.
- Keep cloud providers available for tasks needing stronger reasoning or external tool support.

