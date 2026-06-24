# Placement Decisions

This repository is a coordination and documentation hub for the local AI and macOS automation stack. It is not the right home for vendored copies of unrelated upstream tools. The durable artifact here is the review record and the operational decision matrix.

## Candidate Placement

| Candidate | Placement Decision |
|---|---|
| Headroom | Keep documentation here. Pilot in an AI platform/tooling repository after a pinned wheel or release artifact can be tested against representative local logs and tool outputs. |
| Agent-Reach | Keep existing skill installation constrained to public/no-cookie flows. Do not copy browser cookies or session exports into any repo. |
| Addy Osmani Agent Skills | Use as an upstream skill source only. Candidate skills must be scanned and manually reviewed before import into `~/.codex/skills` or `~/.agents/skills`. |
| NVIDIA SkillSpector | Use as a pre-install gate by pinned `uvx --from` command or future package pin. Document policy here; do not vendor scanner source. |
| Codebase Memory MCP | Pilot outside this repo because it writes MCP/agent configs and indexes repository content. Use allowlisted repo paths only. |
| OpenMontage | Defer to an isolated creative-tools workspace. Its AGPL license, media dependencies, and large skill surface do not belong in this coordination repo. |
| PaddleOCR | Pilot in a document/OCR preprocessing workspace. Keep model caches and generated OCR outputs out of Git. |
| AgentsView | Pilot as a local-only analytics service with transcript roots mounted read-only and telemetry disabled. Do not expose beyond `127.0.0.1`. |
| LMCache | Do not install locally. Reconsider only for a Linux/vLLM/NVIDIA server lane. |
| Flue | Defer until TypeScript tooling and sandbox claims are validated in a separate agent-framework research workspace. |

## Repository Hygiene Notes

Pre-existing untracked files in this checkout and staged files in `Boneman_Projects` appear to be part of a separate governance/container migration. This review did not move, stage, or modify those files.
