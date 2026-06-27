# Local AI Model Residency Governor

Date: 2026-06-27

Machine-readable policy: `config/local-ai-platform/residency-policy.json`.

## Decision

Keep oMLX hot as the stable OpenAI-compatible front door, but do not keep every specialist model resident at the same time.

On this 64 GB Apple Silicon Mac, Ornith 35B GGUF and Rapid-MLX are heavy on-demand lanes. Gemma GGUF is the lighter coding fallback, but it is also stopped when swap reaches the critical threshold.

## Thresholds

| Threshold | Action |
|---|---|
| Swap used percent >= 80 | Stop Ornith `8003` and Rapid-MLX `8010` if they are running. |
| Swap used percent >= 88 | Stop Gemma GGUF `8002` too. |
| Normal operation | Keep oMLX `18080` reachable and let oMLX unload idle model weights by TTL. |

macOS can keep allocated swap high after the heavy process exits. Treat a stopped listener plus falling absolute swap as the important recovery signal.

## Commands

```bash
scripts/local-ai/model-residency-governor.sh status
scripts/local-ai/model-residency-governor.sh enforce
scripts/local-ai/model-residency-governor.sh loop
```

Install or refresh the user LaunchAgent:

```bash
mkdir -p ~/Library/LaunchAgents ~/.local/state ~/.config/local-ai
install -m 0755 scripts/local-ai/model-residency-governor.sh ~/.local/bin/local-ai-model-residency-governor.sh
cp config/local-ai-platform/residency-policy.json ~/.config/local-ai/residency-policy.json
cp launchd/com.corn.local-ai-residency-governor.plist ~/Library/LaunchAgents/
launchctl bootout "gui/$(id -u)" ~/Library/LaunchAgents/com.corn.local-ai-residency-governor.plist 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" ~/Library/LaunchAgents/com.corn.local-ai-residency-governor.plist
launchctl kickstart -k "gui/$(id -u)/com.corn.local-ai-residency-governor"
```

Logs:

```bash
tail -f ~/.local/state/local-ai-model-residency-governor.log
tail -f ~/.local/state/local-ai-model-residency-governor.launchd.log
```

## Restart Specialist Lanes

Use these only for explicit benchmark or coding windows:

```bash
scripts/ornith-gguf-coding-lane.sh start
scripts/gemma4-gguf-coding-lane.sh start
scripts/local-ai/start-rapid-mlx-qwen.sh
```

The next governor pass may stop them again if swap is still above threshold.

## Self-Healing Loop Prompt

Use this prompt for a future Codex run when the local AI stack looks memory pressured:

```text
You are my senior AI platform engineer on this Mac. Fix local AI swap pressure end to end.

Loop until the stack is healthy or you can name a concrete blocker:
1. Read AGENTS.md and the local-ai, coding, documentation, and verification skills.
2. Inventory live state: git status for all workspace repos, vm.swapusage, memory_pressure, listeners on 18080/8002/8003/8010, local-ai health, and drift detection.
3. If swap is high, enforce config/local-ai-platform/residency-policy.json with scripts/local-ai/model-residency-governor.sh enforce. Keep oMLX warm on 18080. Stop Ornith 8003 and Rapid-MLX 8010 at high swap. Stop Gemma GGUF 8002 at critical swap.
4. Re-check listeners and swap. If the same unsafe state remains, repeat enforcement and capture exact evidence. Do not start heavy lanes just to make docs look happy.
5. Update machine-readable config, runbooks, and Boneman_Projects docs so they match the live state.
6. Validate with jq, shellcheck, pytest, markdownlint, local-ai health, drift detection, git diff --check, and secret scanning.
7. Commit logical changes and push every touched repo. Preserve unrelated user work; do not revert it.
8. Finish with exact listener state, swap evidence, commit hashes, pushed repos, and any remaining manual restart guidance.
```
