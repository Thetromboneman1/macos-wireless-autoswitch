# Environment Inventory

Captured on 2026-06-24.

## Host

- Hardware: Apple Silicon MacBook Pro, Apple M1 Max, 64 GB memory.
- OS: macOS 26.5.1 build 25F80.
- Architecture: `arm64`.

## Toolchains

| Tool | Observed State |
|---|---|
| Homebrew | 6.0.3 |
| Python | 3.14.3 |
| uv | 0.11.3 |
| Node.js | v26.3.1 |
| npm | 11.16.0 |
| Rust | rustc 1.94.1 |
| Go | Not installed |
| pnpm | Not installed |
| GitHub CLI | gh 2.89.0, authenticated |
| 1Password CLI | op 2.34.0 |

## Local AI Runtime

| Endpoint | Role | Validation |
|---|---|---|
| `http://127.0.0.1:18080/v1` | oMLX production OpenAI-compatible endpoint | `/health` returned healthy; unauthenticated `/v1/models` returned HTTP 401 |
| `http://127.0.0.1:8002/v1` | llama.cpp GGUF coding lane | `/v1/models` listed `gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf` |
| `http://127.0.0.1:8010/v1` | Rapid-MLX lab lane | Not running during this review |

The Gemma role contract remains unchanged: 31B reasoning, 26B A4B coding, E4B fast agent, and E2B routing/utility.

## Containers

Docker containers observed included OpenClaw, Hermes, Odysseus, ChromaDB, Open WebUI, SearXNG, ntfy, and Ansible lab services. Some web containers publish on all interfaces, but this review did not change any container network exposure.

Apple container CLI reported one running container:

| ID | Image | State | IP | Resources |
|---|---|---|---|---|
| `ac-ntfy` | `docker.io/binwiederhier/ntfy:latest` | running | `192.168.64.4/24` | 4 CPUs, 1024 MB |

## Repositories

Nearby Git repositories were found under `~/Documents`, including `Boneman_Projects`, `Goose`, `Hermes`, `Openclaw`, `odysseus-gemma-docker`, and this repository. This checkout had pre-existing untracked governance/container files before this review. `Boneman_Projects` had a related staged governance/platform batch. Those pre-existing files were not modified by this review.

## Agent And MCP Configs

Observed local config or instruction files included Codex, Goose, OpenCode, Hermes, LM Studio MCP, and repository-level `AGENTS.md` files. This review did not modify agent configs or MCP server entries.
