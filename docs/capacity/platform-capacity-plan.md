# Platform Capacity Plan

Date: 2026-06-23
Owner: Platform Operations

## Current State

The local AI platform is operational on an Apple Silicon Mac with 64 GB unified memory. The production inference endpoint is oMLX on `127.0.0.1:18080`; llama.cpp on `8002` and Rapid-MLX on `8010` remain manual lab lanes.

Live capacity snapshot from 2026-06-23:

| Signal | Observed |
|---|---|
| macOS | `26.5.1` |
| Unified memory | 64 GB |
| Swap | 7168 MB total, 6011 MB used, 83.9 percent used |
| Swap pressure | high |
| Production port | `18080` listening |
| Lab ports | `8002` stopped, `8010` stopped |
| oMLX model registry | four Gemma role models visible |
| Docker container memory limit | 7.75 GiB per Docker stats view |
| Largest Docker container observed | `open-webui`, about 708 MiB |
| VS Code extension footprint | about 2.0 GB on disk |
| VS Code user data footprint | about 851 MB on disk |
| Docs footprint | about 2.0 MB |
| Benchmark footprint | about 40 KB |

## Component Assessment

| Component | Capacity Impact | Current Finding | Operating Rule |
|---|---|---|---|
| RAM and unified memory | Shared by oMLX, GUI apps, Docker, editor tooling, and model loads | The machine has enough total memory, but historical swap remains high | Treat high swap as a scheduling constraint for benchmarks and promotions |
| Swap | Degrades long benchmarks and promotion confidence | High at 83.9 percent during this pass | Do not promote models above 80 percent swap used |
| Model residency | Large Gemma roles can reload on demand | TTL/unload policy reduces idle residency | Keep 31B and large coding roles selectable, not permanently pinned |
| Endpoint concurrency | oMLX is production; lab lanes are manual | Only oMLX was listening during assessment | Keep one production lane active by default |
| LaunchAgents | Can create hidden startup pressure | `com.corn.omlx-power-policy` is healthy; legacy vLLM is archived | No new AI LaunchAgent without capacity review |
| Docker | Active companion and agent services add background pressure | Containers were modest individually but persistent collectively | Stop nonessential Docker stacks before long benchmark windows |
| VS Code | Extension/user data footprint is large on disk and can create background processes | Editor integration is useful but should not become a hidden runtime dependency | Keep recommendations curated and avoid auto-opening extra workspaces |
| Codex | Consumes local tools, skills, and repo checks | Skills are installed and health-checked | Validate skills through health checks, not manual reinstall loops |
| Hermes | Host tools must use loopback endpoint | Host endpoint policy already documented | Keep Hermes on `127.0.0.1`; Docker consumers use `host.docker.internal` |

## Bottlenecks

1. Sustained swap pressure is the primary bottleneck.
2. Concurrent model loading plus Docker plus editor processes is the most likely pressure amplifier.
3. Rapid-MLX remains lab-only because its prior performance upside came with startup memory-pressure risk.
4. Benchmark trend evidence shows one coding-patch TTFT regression that should be watched before treating current oMLX behavior as a new baseline.

## Growth Limits

| Resource | Soft Limit | Hard Stop |
|---|---|---|
| Swap used | 75 percent for normal operation | 80 percent for model promotion gates |
| Production endpoints | one always-on inference front door | any unapproved listener on `8002` or `8010` |
| Lab lanes | one lab lane at a time | Rapid-MLX and llama.cpp running during unrelated work |
| Docker | companion stacks only when needed | starting extra model-serving containers on macOS |
| Benchmarks | monthly production, quarterly lab windows | long benchmarks while swap is high unless studying pressure |

## Projected State

The platform can support continued single-user local AI operations with oMLX as the default front door. It should not grow by adding more always-on local model servers. Future growth should come from better scheduling, TTL unloading, artifact trend analysis, and explicit maintenance windows rather than background capacity expansion.

## Recommended Operating Envelope

- Keep oMLX on `18080` as the only default production endpoint.
- Keep llama.cpp and Rapid-MLX stopped unless a named benchmark, fallback, or validation window is active.
- Run endpoint-only health checks during routine monitoring.
- Run full chat/tool-call checks only for validation, promotion, or incident recovery.
- Start promotion or long benchmark work only when swap is below 75 percent, or explicitly record high swap as the experiment variable.
- Close or stop nonessential Docker, LM Studio, and heavy editor sessions before long model tests.
