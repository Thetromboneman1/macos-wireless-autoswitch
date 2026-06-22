# Secret Inventory

Date: 2026-06-22

## Policy

All local AI, star-tool, DNS, provider, and agent secrets belong in 1Password vault `Boneman`. Documentation may name item titles and retrieval methods, but must not include secret values, token prefixes, cookies, private keys, or raw credential files.

## 1Password Vault Audit

| Vault | State | Action |
|---|---|---|
| `Boneman` | Present and contains local AI/service items. | Canonical target for all new platform secrets. |
| `Boneman Projects` | Empty duplicate, removed on 2026-06-22. | No longer available; do not recreate. |
| `BonemanP Projects` | Not observed. | No action. |
| `Bonema Project Vault` | Not observed. | No action. |

## Inventory

| Service | Purpose | Retrieval method | Owner | Notes |
|---|---|---|---|---|
| oMLX | Local OpenAI-compatible model API | Runtime reads `OMLX_API_KEY` or `~/.omlx/settings.json`; long-term pointer should be in `Boneman` item `Sensitive Items: Goose/oMLX Local AI`. | User | Secret value not copied into repo. |
| OpenCode oMLX provider | Local model provider | Current config uses local placeholder key for localhost provider. | User | No cloud credential in repo config. |
| OpenCode GGUF provider | llama.cpp provider | Current config uses local placeholder key. | User | No cloud credential in repo config. |
| OpenClaw gateway | Local gateway auth | `Boneman` item `OpenClaw Gateway Token (localhost:18789)`. | User | Existing vault item observed by title only. |
| Hermes env | Hermes local environment | `Boneman` items `Environment Details: .hermes/.env` and `Secrets Backup: ~/.hermes/.env`. | User | Values not read. |
| OpenClaw env | OpenClaw local environment | `Boneman` items `Environment Details: Documents/Openclaw/.env` and `Secrets Backup: Openclaw/.env`. | User | Values not read. |
| Octopoda | Local dashboard/MCP auth | `OCTOPODA_API_KEY` env or future `Boneman` item `Octopoda - Local AI`. | User | Start script defaults to local placeholder; avoid exposing remotely. |
| OmniRoute | Provider routing/OAuth/API keys | Future `Boneman` item `OmniRoute - Provider Credentials`. | User | Installed but stopped; do not enable provider routes before threat model. |
| headroom | Compression/proxy and possible Copilot/GitHub tokens | Future `Boneman` item `headroom - Proxy Credentials`; prefer keychain/provider tools when possible. | User | Installed but stopped; token proxy boundary is sensitive. |
| OpenHands | Agent server and workspace access | Future `Boneman` item `OpenHands - Local Config` if external providers are enabled. | User | Docker image installed; no provider secrets configured here. |
| LEANN | Embedding/LLM providers for RAG | `OPENAI_BASE_URL` plus `OPENAI_API_KEY` from `Boneman` when cloud/local auth is required. | User | Local-only indexing can avoid cloud secrets. |
| llm-wiki | Knowledge-base plugin | No secret required for local markdown corpus. | User | Codex plugin materialization may use Codex plugin state, not repo secrets. |
| Hugging Face | Model downloads and gated models | `hf` token or `Boneman` item `Hugging Face - API Token`. | User | Required only for gated model terms/downloads. |
| GitHub CLI | Star export and repo operations | Existing `gh` auth/session. | User | Do not print token. |
| Docker | Pulling/running local containers | Docker Desktop credentials/keychain, if any. | User | Do not store registry tokens in repo. |

## Secret Surfaces Found

- `scripts/local-ai/healthcheck.sh`, `benchmark-smoke.sh`, and `benchmark-engine-bakeoff.py` use local authorization headers or env vars.
- `scripts/odysseus-docker.sh` reads oMLX auth from `~/.omlx/settings.json` when no env var is set, then passes it to a local Docker configuration flow.
- `scripts/omlx-power-policy.sh` reads `OMLX_API_KEY` or `~/.omlx/settings.json`.
- `scripts/star-tools/start-omniroute-local.sh` exposes `REQUIRE_API_KEY` and `ALLOW_API_KEY_REVEAL` flags; keep `ALLOW_API_KEY_REVEAL=false`.
- `scripts/star-tools/start-octopoda-local.sh` sets `OCTOPODA_API_KEY` to a local placeholder unless provided.

## Validation Commands

```bash
op vault get Boneman --format json >/dev/null
op vault get "Boneman Projects" --format json
git diff | grep -Ei 'secret|token|password|apikey|api_key|private_key|BEGIN RSA|BEGIN OPENSSH' || true
```

Review matches manually. Secret-policy docs and placeholder examples are acceptable; real values are not.
