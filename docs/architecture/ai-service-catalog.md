# AI Service Catalog

Date: 2026-06-23

| Service | Owner | Purpose | Startup | Health Check | Dependencies | Status |
|---|---|---|---|---|---|---|
| oMLX | User | Production OpenAI-compatible Gemma runtime | App plus `com.corn.omlx-power-policy` | `scripts/health/local-ai-health.py --skip-chat` | `~/.omlx/settings.json`, Metal/MLX | running |
| Gemma 4 26B-A4B | User | Coding/default production model | on demand through oMLX | `/v1/models`, optional chat probe | oMLX | active, unloaded when idle |
| Gemma 4 31B | User | Reasoning role | on demand through oMLX | `/v1/models` | oMLX | active, manual load |
| Gemma 4 E4B | User | Fast agent role | on demand through oMLX | `/v1/models` | oMLX | active, manual/on-demand |
| Gemma 4 E2B | User | Routing/utility role | on demand through oMLX | `/v1/models` | oMLX | active, manual/on-demand |
| llama.cpp GGUF | User | Specialist coding/reliability lane | manual script | port `8002`, `/v1/models` when started | local GGUF model, Metal build | dormant |
| Rapid-MLX Qwen3.6 | User | Experimental high-throughput/tool-call lane | manual script | port `8010`, validation script when started | Rapid-MLX env | dormant experimental |
| Hermes | User | Host and container agent consumers | host config plus Docker services | Hermes one-shot validation, container health | oMLX endpoint, Docker | running consumer |
| OpenHands | User | Agent platform trial | manual Docker start | image/container checks | Docker, workspace mount | installed, manual |
| Octopoda | User | MCP/dashboard experiment | manual start scripts and Docker sidecars | `scripts/star-tools/validate-star-deployments.sh` | Docker or uv tool install | installed, limited use |
| LEANN | User | Local semantic/RAG indexing | manual CLI/MCP | `leann --help`, MCP command | uv tool env | installed, dormant |
| OmniRoute | User | Routing lab | manual local start | dependency presence, guarded script | Node deps, provider secrets if enabled | installed, stopped |
| edge-lm | User | MLX research package | manual isolated env | import check | uv env | installed, dormant |
| PonyExl3 | User | MLX/model research | manual isolated env | import check | uv env | installed, dormant |
| turbovec | User | Vector/search experiment | manual isolated env | import/search smoke | uv env | installed, dormant |
| LLM Wiki | User | Codex/OpenCode knowledge layer | plugin/config, not a daemon | config/plugin presence | `~/wiki`, Codex/OpenCode config | active knowledge tool |

## Lifecycle Rules

- Only oMLX should be available by default.
- Large models should be unloaded when idle.
- Docker consumers use `host.docker.internal`; host tools use `127.0.0.1`.
- Experimental tools stay manual until they have a narrow owner, health check, and rollback path.
