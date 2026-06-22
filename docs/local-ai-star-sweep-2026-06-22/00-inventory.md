# Loop 0 - Safety, Inventory, and Repo Map

## Known in 5 bullets

- Host is macOS 26.5.1 on Apple M1 Max, 10 CPU cores, 32 GPU cores, 64 GB unified memory, Metal 4.
- Docker Desktop is running, but container memory is about 8 GB; host-side Metal inference remains the right boundary.
- GitHub CLI is authenticated as `Thetromboneman1`; Hugging Face auth was not required for public model metadata.
- oMLX is live at `http://127.0.0.1:18080/v1`; GGUF llama.cpp coding lane is live at `http://127.0.0.1:8002/v1`.
- Current repo had pre-existing local-AI edits before this sweep; they were preserved and built on.

## Tool Inventory

| Tool | Status |
| --- | --- |
| Homebrew | `6.0.1` |
| Python | `3.14.3` via Homebrew |
| uv | `0.11.3` |
| Node | `v24.16.0` |
| npm | `11.13.0` |
| gh | `2.89.0`, authenticated |
| Docker | `29.5.3`, Docker Desktop, arm64 |
| oMLX | `0.4.4` CLI, app running |
| OpenCode | `1.15.4` |
| shellcheck | installed |
| gitleaks / markdownlint | not installed |

## Live Model Endpoints

| Endpoint | Evidence | Models |
| --- | --- | --- |
| `http://127.0.0.1:18080/v1` | `/health` returned healthy | `mlx-community--gemma-4-31b-it-4bit`, `mlx-community--gemma-4-26b-a4b-it-4bit`, `mlx-community--gemma-4-e4b-it-4bit`, `mlx-community--gemma-4-e2b-it-4bit` |
| `http://127.0.0.1:8002/v1` | `/v1/models` returned model metadata | `gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf` |

## Repo Inventory

| Path | Remote / branch | Status | Relevant files |
| --- | --- | --- | --- |
| `/Users/corn/Developer/ML-Models/Gemma4/repos/llama.cpp` | `ggml-org/llama.cpp`, `master` | clean | `pyproject.toml`, `requirements.txt`, `build/bin/llama-server` |
| `/Users/corn/Documents/Ansible` | `Thetromboneman1/Ansible`, `main` | clean | `.config/requirements.txt`, `.env.example`, local LLM docs |
| `/Users/corn/Documents/Boneman_Projects` | `Thetromboneman1/Boneman_Projects`, `main` | dirty before sweep | canonical local AI docs and starred-repos lab |
| `/Users/corn/Documents/Corn_Automation/Goose` | `Thetromboneman1/Goose`, `main` | clean | Goose config docs |
| `/Users/corn/Documents/Corn_Automation/macos-wireless-autoswitch` | `Thetromboneman1/macos-wireless-autoswitch`, `main` | dirty before sweep plus sweep edits | oMLX, Odysseus, GGUF lane scripts/docs |
| `/Users/corn/Documents/Hermes` | `Thetromboneman1/hermes-workspace`, `main` | behind 2, dirty before sweep | `opencode.json`, Docker, local AI runbooks |
| `/Users/corn/Documents/Hermes/OmniRoute` | `Thetromboneman1/OmniRoute`, `main` | clean | Docker, provider/model routes |
| `/Users/corn/Documents/Hermes/hermes-agent` | `Thetromboneman1/hermes-agent`, `main` | behind 1188 | `pyproject.toml`, `uv.lock`, model switch tests |
| `/Users/corn/Documents/Hermes/hermes-desktop` | `Thetromboneman1/hermes-desktop`, `main` | ahead 3 / behind 84 vs upstream | Swift desktop docs |
| `/Users/corn/Documents/Hermes/hermes-webui` | `Thetromboneman1/hermes-webui`, `local-llm-docs` | clean | `requirements.txt`, OpenCode config, model tests |
| `/Users/corn/Documents/Openclaw` | `Thetromboneman1/Openclaw`, `main` | dirty before sweep | Docker, OpenCode, local LLM docs |
| `/Users/corn/Documents/YTKillerPlus` | `iKarwan/YTKillerPlus`, `main` | clean | README |
| `/Users/corn/Documents/odysseus-gemma-docker` | `Thetromboneman1/odysseus-gemma-docker`, `main` | dirty before sweep | Odysseus env/docs/scripts |

## Safety Notes

- No model files, repos, containers, or private configs were deleted.
- OpenCode host config was backed up before editing:
  - `~/.config/opencode/opencode.json.bak-local-ai-star-sweep-2026-06-22`
  - `~/.config/opencode/opencode.jsonc.bak-local-ai-star-sweep-2026-06-22`
- Raw GitHub stars export saved to `github-stars.json`.

