# Dual-Runtime Operational Deployment

Date: 2026-06-23

## Outcome

Docker Desktop and Apple Container now run side by side for the first selected workload, `ntfy`.

Production remains Docker Desktop. Apple Container is a pilot/secondary runtime with `ac-` service names, isolated `19000-19999` ports, isolated storage, and explicit runtime profiles.

## Versions

| Runtime | Version |
|---|---|
| Docker Desktop | 4.77.0 |
| Docker Engine | 29.5.3 |
| Docker Compose | v5.1.4 |
| Apple Container | 1.0.0, commit `ee848e3` |

## Mirrored Workload

| Workload | Docker Desktop | Apple Container | Result |
|---|---|---|---|
| ntfy | `odysseus-gemma-ntfy-1`, `127.0.0.1:8091` | `ac-ntfy`, `127.0.0.1:19091` | dual-runtime validated |

The Apple Container image is `docker.io/binwiederhier/ntfy:latest`, `linux/arm64`, digest `sha256:f8a9b104313b87cc24ae4f775f39e6328205b57dff6ede3eaf098a91e5d79f59`.

## Validation Evidence

| Check | Result |
|---|---|
| Port map | valid |
| Docker ntfy health | pass |
| Apple Container ntfy health | pass |
| Side-by-side comparison | pass |
| Restart | pass |
| Self-heal after pilot stop | pass |
| Production oMLX | healthy |
| Production Docker services | left running |

Health comparison:

| Runtime | Endpoint | Seconds |
|---|---|---:|
| Docker Desktop | `http://127.0.0.1:8091/v1/health` | 0.004340 |
| Apple Container | `http://127.0.0.1:19091/v1/health` | 0.005419 |

## Runtime Profiles

Profiles were added under `config/runtime-profiles/`:

- `production`
- `docker-current`
- `apple-container-pilot`
- `side-by-side`
- `native-ai`
- `rollback-safe`

## Deferred Or Blocked

| Workload | Status | Reason |
|---|---|---|
| OpenClaw gateway | Docker-only | requires `/var/run/docker.sock` |
| Open WebUI | deferred | heavier service; live swap was already high |
| ChromaDB | deferred | persistent vector store; test data and longer validation needed |
| Hermes WebUI / OpenCode | deferred | compatible candidates, not first low-risk target |
| OmniRoute | deferred | build required |
| native oMLX / llama.cpp / Rapid-MLX | native macOS | Metal/MLX inference stays host-native |

## Security

- No real `.env` files were committed.
- No secrets were committed.
- Sensitive values remain sourced from 1Password vault `Boneman`.
- Pilot service binds to `127.0.0.1`.
- Pilot storage is under `~/.local/share/apple-container-pilot/`.
- No Docker socket is mounted into Apple Container.

## Recommendation

Keep Docker Desktop as production and continue the Apple Container pilot one service at a time. The next safest candidates are simple UI/helper services after swap pressure is reduced; defer databases and Docker-socket-dependent services until their storage and runtime boundaries are fully modeled.
