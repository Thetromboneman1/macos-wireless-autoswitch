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
| Hermes oMLX provider | Host local model endpoint | `~/.hermes/config.yaml` points at `http://127.0.0.1:18080/v1`; API key remains a local placeholder or `Boneman` pointer. | User | No secret value committed. |
| Hermes cloud providers | Optional fallback or escalation | Future provider keys must be stored in `Boneman` and documented by item name only. | User | No paid provider added in the 2026-06-23 cost pass. |
| Rapid-MLX lab lane | Qwen3.6 Hermes candidate endpoint | No API key by default on `127.0.0.1:8010`; keep LAN exposure disabled. | User | Telemetry forced off by launcher. |
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
| Codex GitHub skills | PR review, CI triage, commit/push/PR workflow | Existing `gh` authenticated session. | User | No GitHub token value is stored in repo; use `gh auth status` for validation. |
| VS Code Kubernetes Tools | Kubernetes authoring and diagnostics | Local kubeconfig/keychain or future `Boneman` item for cluster credentials. | User | Extension installed; no cluster secret added. |
| VS Code Terraform | Terraform authoring and optional Terraform Cloud integration | Future `Boneman` item `Terraform Cloud - API Token` if cloud features are enabled. | User | Editor support installed; no cloud token added. |
| VS Code PowerShell | Windows and PowerShell administration | Future `Boneman` item for remoting credentials if used. | User | Extension installed; no remote credentials added. |
| Sentry Codex skill/plugin | Issue triage and production diagnostics | Future `Boneman` item `Sentry - API Token` if enabled for a project. | User | Deferred/manual approval required. |
| Notion Codex skills | Knowledge capture and workspace automation | Future `Boneman` item `Notion - Integration Token` if installed. | User | Deferred/manual approval required. |

## Secret Surfaces Found

- `scripts/local-ai/healthcheck.sh`, `benchmark-smoke.sh`, and `benchmark-engine-bakeoff.py` use local authorization headers or env vars.
- `scripts/odysseus-docker.sh` reads oMLX auth from `~/.omlx/settings.json` when no env var is set, then passes it to a local Docker configuration flow.
- `scripts/omlx-power-policy.sh` reads `OMLX_API_KEY` or `~/.omlx/settings.json`.
- `scripts/star-tools/start-omniroute-local.sh` exposes `REQUIRE_API_KEY` and `ALLOW_API_KEY_REVEAL` flags; keep `ALLOW_API_KEY_REVEAL=false`.
- `scripts/star-tools/start-octopoda-local.sh` sets `OCTOPODA_API_KEY` to a local placeholder unless provided.
- `.vscode/settings.json` and VS Code user settings contain non-secret local endpoint hints only.
- `~/.agents/skills/*/SKILL.md` contains workflow pointers and no credential values.

## Validation Commands

```bash
op vault get Boneman --format json >/dev/null
op vault get "Boneman Projects" --format json
git diff | grep -Ei 'secret|token|password|apikey|api_key|private_key|BEGIN RSA|BEGIN OPENSSH' || true
```

Review matches manually. Secret-policy docs and placeholder examples are acceptable; real values are not.
