# Swap Pressure Analysis

Date: 2026-06-23

## Current State

Captured state:

- Swap total: 8192 MB.
- Swap used: about 6620 MB.
- Swap pressure classification: high.
- oMLX production port `18080` was listening.
- llama.cpp `8002` and Rapid-MLX `8010` were not listening.
- oMLX server RSS was about 2.2 GB.
- Sideloadly, Docker Desktop, Razer helpers, LM Studio, and BetterDisplay were visible background contributors.

## Root Cause

The high swap state is not from active Rapid-MLX or llama.cpp lab lanes in this snapshot. It appears to be accumulated system pressure from long-running desktop services, Docker Desktop, third-party LaunchAgents, and the oMLX production server.

## Safe Remediation

- Keep Rapid-MLX and llama.cpp manual-only.
- Keep `com.corn.vllm-mlx` archived; it is obsolete and outside the approved lanes.
- Before long benchmarks, close or stop Docker Desktop, LM Studio, Sideloadly, and Razer tooling when not needed.
- Reboot or log out after long high-memory sessions if swap remains high after closing apps.

No stable AI lane was stopped in this pass.

Phase-two remediation is tracked in [swap-pressure-remediation-phase2.md](swap-pressure-remediation-phase2.md).
