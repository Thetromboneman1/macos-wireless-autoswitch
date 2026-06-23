# LaunchAgent Legacy Cleanup

Date: 2026-06-23

## Decision

`com.corn.vllm-mlx` is obsolete and has been archived.

Evidence:

- It was disabled in `launchctl print-disabled`.
- Its `ProgramArguments` path pointed to a missing `Boneman_Projects/mlx-native-bench/.../start-vllm-mlx.sh` script.
- The active production lane is oMLX on `127.0.0.1:18080`.
- llama.cpp and Rapid-MLX are explicit manual lab lanes.

## Action Taken

The active plist was moved from:

```text
~/Library/LaunchAgents/com.corn.vllm-mlx.plist
```

to:

```text
~/Library/LaunchAgents/Archive/com.corn.vllm-mlx.plist.20260623-082607.archived
```

No enabled service was stopped. The current active LaunchAgent set has no broken plist executable paths.

## Current AI LaunchAgent Policy

| Label | State | Decision |
|---|---|---|
| `com.corn.omlx-power-policy` | active | Keep. Applies oMLX TTL/unload policy. |
| `com.corn.vllm-mlx` | archived | Removed from active startup. |
| `com.corn.omlx` | disabled file | Leave untouched unless a future oMLX migration needs it. |

## Rollback

If the legacy vLLM/MLX path is intentionally restored later:

```bash
cp ~/Library/LaunchAgents/Archive/com.corn.vllm-mlx.plist.20260623-082607.archived \
  ~/Library/LaunchAgents/com.corn.vllm-mlx.plist
plutil -lint ~/Library/LaunchAgents/com.corn.vllm-mlx.plist
```

Do not enable it until the referenced program path exists and memory pressure is measured.
