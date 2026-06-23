# Model Lifecycle Management

Date: 2026-06-23
Owner: AI Platform

## Lifecycle States

| State | Meaning | Promotion requirement |
|---|---|---|
| Production | Default supported lane | Health, benchmark, docs, rollback path |
| Candidate | Potential future production lane | Two benchmark windows and tool-call validation |
| Experimental | Lab-only investigation | Manual start, isolated docs, no autostart |
| Deprecated | Superseded or stale | Archive docs/config and remove from startup |

## Model Inventory

| Model | Lane | State | Purpose | Last benchmark evidence | Maintenance status |
|---|---|---|---|---|---|
| `mlx-community--gemma-4-26b-a4b-it-4bit` | oMLX `18080` | Production | Default coding and agent workflow | `docs/benchmarks/post-cleanup-benchmark-results.json` | Keep |
| `mlx-community--gemma-4-31b-it-4bit` | oMLX `18080` | Production role | Reasoning and architecture work | `/v1/models` role validation | Keep, load on demand |
| `mlx-community--gemma-4-e4b-it-4bit` | oMLX `18080` | Production role | Fast agent and summary work | `/v1/models` role validation | Keep, load on demand |
| `mlx-community--gemma-4-e2b-it-4bit` | oMLX `18080` | Production role | Routing and utility work | `/v1/models` role validation | Keep, load on demand |
| `gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf` | llama.cpp `8002` | Candidate/reliability | GGUF portability and coding lane | prior benchmark docs | Manual only |
| `qwen3.6-35b-4bit` | Rapid-MLX `8010` | Experimental | High-throughput/tool-call lab | prior Rapid-MLX benchmark docs | Manual only |

## Lifecycle Workflow

1. Register model purpose and lane.
2. Validate endpoint visibility with `/v1/models`.
3. Run benchmark governance.
4. Run tool-call validation when the model is intended for agent workflows.
5. Document memory/swap impact.
6. Decide state: production, candidate, experimental, or deprecated.
7. Update routing policy and operations docs together.

## Retirement Workflow

- Remove from default routing.
- Keep rollback notes if the model served production traffic.
- Archive stale LaunchAgents rather than deleting them immediately.
- Keep Boneman pointers if a credential or file location remains relevant.
