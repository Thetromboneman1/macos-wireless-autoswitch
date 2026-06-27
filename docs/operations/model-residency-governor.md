# Local AI Model Residency Governor

Date: 2026-06-27

Machine-readable policy: `config/local-ai-platform/residency-policy.json`.

## Decision

Keep oMLX hot as the stable OpenAI-compatible front door, but do not keep every specialist model resident at the same time.

On this 64 GB Apple Silicon Mac, Ornith 35B GGUF and Rapid-MLX are heavy on-demand lanes. Gemma GGUF is the lighter coding fallback, but it is also stopped when swap reaches the critical threshold.

The tool-facing ports stay warm through lightweight gateways:

| Tool-facing port | Backend port | Lane |
|---|---:|---|
| `8002` | `18002` | Gemma GGUF fallback |
| `8003` | `18003` | Ornith 35B GGUF |
| `8010` | `18010` | Rapid-MLX Qwen3.6 |

Requests to `/v1/models`, `/v1/chat/completions`, and other OpenAI-compatible paths start the backend if it is cold. Requests to `/__lane_status` report gateway/backend state without waking the model.

## Thresholds

| Threshold | Action |
|---|---|
| Swap used percent >= 80 | Stop Ornith backend `18003` and Rapid-MLX backend `18010` if they are running. |
| Swap used percent >= 88 | Stop Gemma GGUF backend `18002` too. |
| Normal operation | Keep oMLX `18080` reachable and let oMLX unload idle model weights by TTL. |

macOS can keep allocated swap high after the heavy process exits. Treat a stopped backend plus falling absolute swap as the important recovery signal.

## Commands

```bash
scripts/local-ai/model-residency-governor.sh status
scripts/local-ai/model-residency-governor.sh enforce
scripts/local-ai/model-residency-governor.sh loop
scripts/local-ai/install-on-demand-gateways.sh
```

Install or refresh the user LaunchAgent:

```bash
scripts/local-ai/install-on-demand-gateways.sh
```

Logs:

```bash
tail -f ~/.local/state/local-ai-model-residency-governor.log
tail -f ~/.local/state/local-ai-model-residency-governor.launchd.log
tail -f ~/.local/state/local-ai-ornith-gateway.log
```

## Wake Specialist Lanes

Call the existing tool-facing endpoint. The gateway starts the backend automatically:

```bash
curl http://127.0.0.1:8003/__lane_status
curl http://127.0.0.1:8003/v1/models
```

The first command is no-wake status. The second command wakes Ornith if it is cold. The next governor pass may stop the backend again if swap is still above threshold.

## Self-Healing Loop Prompt

Use this prompt for a future Codex run when the local AI stack looks memory pressured:

```text
You are my senior AI platform engineer on this Mac. Make the local AI model lanes on-demand with automatic startup from my toolset.

Loop until the stack is healthy or you can name a concrete blocker:
1. Read AGENTS.md and the local-ai, coding, documentation, and verification skills.
2. Inventory live state: git status for all workspace repos, vm.swapusage, memory_pressure, public listeners on 18080/8002/8003/8010, backend listeners on 18002/18003/18010, local-ai health, and drift detection.
3. Ensure config/local-ai-platform/residency-policy.json declares public gateway ports and private backend ports for Gemma GGUF, Ornith, and Rapid-MLX.
4. Ensure scripts/local-ai/on-demand-lane-gateway.py starts a cold backend before proxying OpenAI-compatible requests, and that /__lane_status never wakes a model.
5. Ensure scripts/local-ai/model-residency-governor.sh stops only backend ports under swap pressure, leaving public gateways warm.
6. Install or refresh scripts/local-ai/install-on-demand-gateways.sh so the gateway, copied lane managers, policy copy, and LaunchAgents are in launchd-safe locations.
7. Verify tool-facing calls wake the requested model lane, then enforce spin-down and confirm the public gateway remains listening while the backend stops.
8. Update machine-readable config, runbooks, and Boneman_Projects docs so they match live behavior.
9. Validate with jq, plutil, shellcheck, pytest, markdownlint, local-ai health, drift detection, git diff --check, and secret scanning.
10. Commit logical changes and push every touched repo. Preserve unrelated user work; do not revert it.
11. Finish with exact public gateway state, backend model state, swap evidence, commit hashes, pushed repos, and any remaining manual guidance.
```
