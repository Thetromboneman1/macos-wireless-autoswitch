# Apple Container Client Integration

Date: 2026-06-23

## Profiles

| Profile | Runtime | Endpoint/storage rule |
|---|---|---|
| `production` | native macOS + Docker Desktop | current defaults only |
| `docker-current` | Docker Desktop | existing Compose files and ports |
| `apple-container-pilot` | Apple Container | `ac-` containers, `19000-19999`, pilot storage root |
| `native-ai` | host oMLX/llama/Rapid-MLX | no container changes |
| `hybrid-test` | Apple Container support services + host AI | pilot services consume native AI endpoints |

## Current Client Rules

- Codex default model routing stays unchanged.
- Hermes host-side configuration must continue using `127.0.0.1`.
- Docker containers keep using `host.docker.internal` where already proven.
- Apple Container services must get a separately validated host-reachability profile before using host AI endpoints.
- Goose remains a host profile unless a dedicated pilot profile is written.
- OpenCode/OpenClaw/OpenHands profiles must be explicit and must not overwrite production files.

## VS Code Tasks

The governance repo exposes manual tasks for pilot status, health, rollback, and port validation in `.vscode/tasks.json`.
