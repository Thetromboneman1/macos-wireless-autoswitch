# Security Review

## Summary

No candidate received blanket install approval. The safe outcome of this pass is a documented review package plus limited, isolated gates for follow-up pilots.

## Supply Chain Findings

| Candidate | Key Security Notes | Decision Impact |
|---|---|---|
| Headroom | Python/Rust project with proxy, MCP, telemetry, optional ML, OCR, memory, and OpenTelemetry surfaces. Source build was non-trivial. | Pilot only; use pinned release and local-only config. |
| Agent-Reach | Optional dependencies include Playwright and `browser-cookie3`; README and doctor describe cookie/session-backed channels. | Public channels only unless separately approved. |
| Addy Osmani Agent Skills | Skills are instructions that can change agent behavior. SkillSpector produced caution-level findings on defensive content, proving scanner output needs manual review. | No bulk install. |
| SkillSpector | Static scan is useful and local; LLM modes require provider credentials. | Adopt limited static mode first. |
| Codebase Memory MCP | Installer can auto-detect and write agent configs, hooks, skills, and instructions. Indexes code into SQLite under `~/.cache/codebase-memory-mcp/`; can optionally commit `.codebase-memory/graph.db.zst`. | Pilot with explicit allowlist and `.codebase-memory/` ignored unless intentionally shared. |
| OpenMontage | Large AGPL project with many skills, tools, media pipelines, and generation/provider surfaces. | Defer broad access. |
| PaddleOCR | Optional AI Studio token path exists for MCP server; dependencies and model caches need containment. | Pilot without external document uploads or private files. |
| AgentsView | Indexes local agent transcripts that may contain secrets. Docs mention localhost default, redaction, auth controls, and telemetry opt-out. | Pilot only with read-only mounts and telemetry disabled. |
| LMCache | Linux/GPU/vLLM-oriented acceleration path; local Mac install would add risk without benefit. | Reject local install. |
| Flue | Sandbox is central to value, but local TypeScript tooling was unavailable and runtime isolation was not validated. | Defer. |

## Scanner Evidence

SkillSpector static mode was run through `uvx --from /tmp/codex-ai-repo-review-2026-06-24/SkillSpector`.

Results:

- Synthetic suspicious skill: `HIGH`, score 61, recommendation `DO_NOT_INSTALL`; detected credential-path access, instruction override, and browser-cookie theft pattern.
- `agent-skills/skills/browser-testing-with-devtools`: `MEDIUM`, score 38, recommendation `CAUTION`; findings were caused by defensive discussion of cookies and prompt injection.

Conclusion: SkillSpector is useful as a mandatory gate, but clean or noisy scanner output must be paired with manual review.

## Secret Handling

- Correct vault: `Boneman`.
- No new secret values were needed.
- No candidate credentials, cookies, browser exports, provider keys, API tokens, or private documents were added to Git.
- Any future secret-dependent pilot must store only safe references such as `op://Boneman/<item>/<field>` in documentation.

## Network And Service Boundaries

Future pilots must default to loopback only. AgentsView and Codebase Memory MCP both have local web/UI surfaces that must not be exposed to LAN, VPN, Tailscale, or reverse proxy without separate approval.
