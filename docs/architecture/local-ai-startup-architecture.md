# Local AI Startup Architecture

Date: 2026-06-23

```mermaid
flowchart TD
  Login[User Login] --> PowerPolicy[com.corn.omlx-power-policy]
  PowerPolicy --> OMLX[oMLX app and omlx-server]
  OMLX --> Prod[Gemma 4 26B-A4B production lane]
  Manual[Manual Specialist Start] --> Llama[llama.cpp on 8002]
  RapidStart[tmux rapid-mlx-qwen] --> Rapid[Rapid-MLX on 8010]
  Docker[Docker Consumers] --> HostAlias[host.docker.internal to host oMLX]
  HostTools[Host Tools: Hermes, OpenCode, Codex] --> Loopback[127.0.0.1 endpoints]
```

## Startup Rules

- oMLX power policy may start at login.
- llama.cpp remains a manual specialist lane.
- Rapid-MLX is currently expected to stay running in `tmux` session `rapid-mlx-qwen` as an available specialist lane; stop it only for documented memory pressure or rollback.
- `com.corn.vllm-mlx` is archived and no longer part of active startup.
- Host tools use `127.0.0.1`.
- Docker consumers use `host.docker.internal`.

## Current Ports

| Port | Lane | Current state |
|---:|---|---|
| 18080 | oMLX production | listening |
| 8002 | llama.cpp GGUF specialist | listening |
| 8010 | Rapid-MLX Qwen3.6 specialist | listening |

For the current startup policy, use [startup-orchestration-v2.md](startup-orchestration-v2.md).
