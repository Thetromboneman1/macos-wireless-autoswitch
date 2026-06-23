# LaunchAgent Inventory

Date: 2026-06-23

| Label | Purpose | Trigger | Status | Notes |
|---|---|---|---|---|
| `com.boneman.betterdisplay.internal.enforcer` | BetterDisplay internal display enforcement | RunAtLoad, 180s | healthy | Script exists. |
| `com.boneman.betterdisplay.internal.healthcheck` | BetterDisplay health check | RunAtLoad, 900s | healthy | Script exists. |
| `com.boneman.citrix-auto-self-heal` | Citrix self-heal | RunAtLoad, 180s | healthy | Script exists. |
| `com.boneman.ea-auto-close` | EA launcher cleanup | RunAtLoad, 90s | healthy | Script exists. |
| `com.boneman.gfn-bf6-enforcer` | Game/GeForce Now enforcement | RunAtLoad, 60s | healthy | Script exists. |
| `com.boneman.launcher-auto-maintenance` | Game launcher maintenance | RunAtLoad, 21600s | healthy | Script exists. |
| `com.boneman.magic-mouse-scroll-reverser` | Mouse scroll setting enforcement | RunAtLoad, 5s | healthy but noisy | Very frequent interval. |
| `com.boneman.steam-auto-updater` | Steam game updates | RunAtLoad, 14400s | healthy | Script exists. |
| `com.corn.omlx-power-policy` | oMLX power policy | RunAtLoad, KeepAlive | healthy | Approved AI LaunchAgent. |
| `com.razer.gms` | Razer service | RunAtLoad | third-party | High background footprint family. |
| `homebrew.mxcl.dnscrypt-proxy` | DNSCrypt listener | RunAtLoad | healthy | Required for AdGuard LocalDNSCrypt. |
| `io.sideloadly.daemon` | Sideloadly daemon | RunAtLoad | third-party | Largest observed RSS among listed agents. |
| `local.vscode.open-workspace` | VS Code workspace opener | RunAtLoad | healthy | Opens workspace at login. |

## Health Findings

- `com.corn.vllm-mlx` was disabled, pointed to a missing script under `Boneman_Projects/mlx-native-bench`, and has now been archived out of active LaunchAgents.
- `com.corn.omlx-power-policy` is the current approved AI platform LaunchAgent and should remain enabled.
- High swap pressure is not caused by loaded Rapid-MLX or llama.cpp lanes in the captured state; only oMLX was listening on `18080`.

See [launchagent-legacy-cleanup.md](launchagent-legacy-cleanup.md) for the archive path and rollback notes.
