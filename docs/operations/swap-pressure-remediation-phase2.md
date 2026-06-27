# Swap Pressure Remediation Phase 2

Date: 2026-06-23

## Current State

Phase-two checks found swap still high but active pressure lower than the raw swap number implies:

| Signal | Value |
|---|---:|
| Swap total | 8192 MB |
| Swap used before cleanup | 6563 MB |
| Swap used after cleanup | 6475 MB |
| Post-cleanup swap classification | high |
| oMLX model memory before unload | 16.4 GB |
| oMLX model memory after unload-large | 0 GB |
| Active AI listeners after cleanup | `18080` only |
| One-hour absolute swap delta | -448 MB |

The `memory_pressure` command reported high free headroom while swap remained allocated. That means the system had historical swap usage from long-running workloads, not an active memory emergency at the time of the phase-two pass.

During the one-hour endpoint-only soak, macOS reduced allocated swap from 8192 MB to 7168 MB and used swap from 6475 MB to 6027 MB. The used percentage remained high only because the total swap denominator shrank.

## Root Cause

The largest current contributors were:

| Consumer | Approximate RSS | Classification |
|---|---:|---|
| Docker/macOS virtualization VM | 4.5 GB | standing container platform |
| oMLX server before unload | 15.2 GB | model residency |
| oMLX server after unload | 2.4 GB | service runtime |
| Sideloadly daemon/app | 2.0 GB combined | background desktop service |
| Pandora/WebKit/VS Code helpers | 1 GB+ each for top processes | user desktop workload |

Rapid-MLX and llama.cpp were not listening during the cleanup. They were not the root cause of current swap.

## Remediation Actions

- Archived the obsolete `com.corn.vllm-mlx` LaunchAgent out of active startup.
- Added low-impact health mode with `scripts/health/local-ai-health.py --skip-chat`.
- Unloaded the large oMLX primary/coding models after benchmark validation.
- Kept Rapid-MLX and llama.cpp manual-only.
- Added drift detection so manual lanes do not quietly become startup lanes.

## Recommended State

| Service | Desired state |
|---|---|
| oMLX app/server | running, models unloaded when idle |
| Gemma 26B-A4B | loaded on demand, not pinned |
| Gemma 31B | loaded only for explicit reasoning runs |
| llama.cpp | manual lab lane on `8002` |
| Rapid-MLX | manual experimental lane on `8010` |
| Docker consumers | allowed, reviewed during monthly maintenance |

## Follow-Up

Swap may not fully return to zero without closing large desktop apps, stopping Docker Desktop, or logging out/rebooting. Do those only when they will not interrupt active work.

## 2026-06-27 Ornith Residency Update

Installing and validating Ornith 35B GGUF proved the local lane is useful, but running Ornith, Gemma GGUF, and oMLX together can push swap back into critical territory.

The current remediation is automated through:

```bash
scripts/local-ai/model-residency-governor.sh enforce
```

Policy:

- oMLX `18080` stays warm as the required production front door.
- Ornith `8003` and Rapid-MLX `8010` are stopped when swap used percent is at or above 80.
- Gemma GGUF `8002` is also stopped when swap used percent is at or above 88.
- The LaunchAgent `com.corn.local-ai-residency-governor` runs the same loop every five minutes.

The self-healing prompt and launchd install commands live in `docs/operations/model-residency-governor.md`.
