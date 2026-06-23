# Cross-Repository Finalization

Date: 2026-06-23

This finalization pass completed the requested cross-repository reconciliation
after the primary repository modernization had already passed.

## Completed Commits

| Repository | Commit | Purpose |
| --- | --- | --- |
| `Ansible` | `82e764cdb2a8` | Move first-party workflow actions to Node 24-compatible majors. |
| `odysseus-gemma-docker` | `e588a461d7c0` | Validate GGUF coding lane defaults and update workflow runtime. |
| `Openclaw` | `c47ca66758a7` | Align docs/config/workflows with oMLX plus GGUF coding lane. |
| `Boneman_Projects` | `36e1db6fca56` | Record measured GGUF coding lane selection in local-AI docs. |
| `Hermes/hermes-webui` | `b6bfaa42699f` | Update workflow action runtimes and shell style. |
| `Hermes` | `069e241a32b5` | Align Hermes compose/docs/OpenCode and gitlinks with local model lanes. |

## Runtime Contract

- Production endpoint: `http://127.0.0.1:18080/v1`
- Production engine: oMLX/MLX
- Coding endpoint: `http://127.0.0.1:8002/v1`
- Coding engine: llama.cpp GGUF/MTP lane
- Docker endpoint pattern: `host.docker.internal`
- Ollama remains compatibility-only.

## Final Local-AI Validation

```text
oMLX /v1/models: mlx-community--gemma-4-31b-it-4bit,
mlx-community--gemma-4-26b-a4b-it-4bit,
mlx-community--gemma-4-e4b-it-4bit,
mlx-community--gemma-4-e2b-it-4bit

oMLX chat: OK

llama.cpp /v1/models: gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf
llama.cpp chat: OK
```

The coding lane required a larger completion budget than the quick oMLX probe
because the Gemma GGUF template emits `reasoning_content` before final visible
content.

## Deferred

- Do not auto-update divergent upstream/reference checkouts.
- Do not enable required gitleaks in `Boneman_Projects` or
  `Hermes/hermes-webui` until existing historical findings are remediated.
- Do not manually dispatch workflows that publish containers, send
  notifications, rewrite branches, or create pull requests outside a maintenance
  window.
