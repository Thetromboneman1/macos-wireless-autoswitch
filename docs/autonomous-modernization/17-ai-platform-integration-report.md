# AI Platform Integration Report

Date: 2026-06-22

## Summary

This pass converted the installed starred tools into a coherent local-AI platform definition. It did not autostart high-risk services. Instead, it added shared routing policy, MCP topology, knowledge-layer topology, a platform runbook, a secret inventory, and a status script.

## Implemented

| Area | Change | Validation |
|---|---|---|
| Vault policy | Corrected all new platform docs to use 1Password `Boneman`. | `op vault list` shows `Boneman`; `Boneman Projects` is empty. |
| Routing | Added `config/local-ai-platform/routing-policy.json` and [model-routing.md](../architecture/model-routing.md). | JSON validates with `jq`. |
| MCP | Added `config/local-ai-platform/mcp-topology.json` and [mcp-topology.md](../architecture/mcp-topology.md). | JSON validates with `jq`. |
| Knowledge | Added [knowledge-layer.md](../architecture/knowledge-layer.md). | LEANN, turbovec, llm-wiki, and Understand-Anything deployments are validated by existing script. |
| Operations | Added [platform-runbook.md](../operations/platform-runbook.md). | Status script checks commands, endpoint health, Docker image, vaults, and docs. |
| Secrets | Added [secret-inventory.md](../security/secret-inventory.md). | Inventory records retrieval methods only; no values. |
| App configs | Wired Codex, OpenCode, Goose, Hermes, VS Code, and workspace settings to the shared policy files. | JSON/YAML/TOML parse checks and app-specific CLI checks. |
| 1Password cleanup | Deleted empty duplicate `Boneman Projects` vault after confirming item count was zero. | `op vault get "Boneman Projects"` returns not found. |

## Tool Integration Status

| Tool | Role | Integration status |
|---|---|---|
| Codex | Primary autonomous engineering surface | llm-wiki marketplace config present; cloud fallback kept. |
| OpenCode | Local coding shell | oMLX/GGUF providers and llm-wiki instruction path present. |
| Goose | Local agent client | Installed; should follow shared routing profile before further edits. |
| Hermes | Agent/workbench | Installed; do not overwrite existing dirty workspace state from this repo. |
| OpenClaw | Agent/workbench | Installed; treat gateway tokens as `Boneman` secrets. |
| OpenHands | High-agency sandbox | Docker image present; launch script available; stopped by default. |
| Octopoda | Agent memory/audit | CLI/MCP installed; dashboard start script available; stopped by default. |
| LEANN | Private RAG and MCP | CLI/MCP installed; index creation is explicit. |
| llm-wiki | Local AI knowledge base | Codex/OpenCode wiring present; first Codex materialization may require interactive `/plugins`. |
| Understand-Anything | Repo graph and skills | Skills symlinked into `~/.agents/skills`; dashboard start script available. |
| OmniRoute | Routing lab | Dependencies installed; stopped by default until secret/routing threat model is complete. |
| headroom | Compression/proxy lab | Binary built; stopped by default until proxy boundary review. |
| edge-lm/PonyExl3 | Apple Silicon model experiments | Isolated uv envs installed; model downloads require terms/model selection. |
| SiliconScope | Apple Silicon observability | CLI built and usable for benchmark observation. |

## Operational Posture

- Default local requests should go directly to oMLX unless a specific GGUF/llama.cpp test is being run.
- OmniRoute and headroom are lab tools until provider key, logging, and request-retention behavior is reviewed.
- OpenHands is available for sandboxed work, not host-wide unattended operation.
- Octopoda is useful for memory/audit experiments but should be scoped per run.

## 2026-06-22 Follow-Up Actions

- `wiki@llm-wiki` was installed and enabled with `codex plugin add wiki@llm-wiki`.
- The duplicate empty `Boneman Projects` vault was deleted.
- Goose and Hermes user configs now reference the shared platform policy.
- VS Code user, Hermes workspace, and OpenClaw workspace settings now reference the shared platform policy.
- Extended per-engine MLX and llama.cpp benchmark passes were run and merged into [07-benchmarks.md](07-benchmarks.md).
