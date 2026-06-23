# Platform Drift Detection

Date: 2026-06-23

Platform drift is any change that moves the live machine away from the approved local AI, automation, validation, and secret-handling contract. Drift can be intentional during a lab window, but it must be visible and reversible.

## Commands

Endpoint-only health is the default monitoring mode because it validates the model registry without loading large models:

```bash
scripts/health/local-ai-health.py --skip-chat --json /tmp/local-ai-health.json
scripts/health/drift-detection/check-platform-drift.py \
  --health-json /tmp/local-ai-health.json \
  --json /tmp/platform-drift.json
```

Use a full chat health check only when proving generation:

```bash
scripts/health/local-ai-health.py
```

## Baseline

```text
scripts/health/drift-detection/baseline.json
```

The baseline tracks:

- expected AI port state;
- approved LaunchAgent state;
- approved GitHub Actions versions;
- required config paths;
- required validation binaries.

## Drift Classes

| Drift class | Examples | Detector |
|---|---|---|
| LaunchAgent drift | stale plist, missing program path, unexpected legacy AI startup | `check-platform-drift.py`, `local-ai-health.py` |
| GitHub Actions drift | action version downgrade or unreviewed workflow action | `check-platform-drift.py`, `actionlint` |
| AI endpoint drift | oMLX stopped, manual lab lane listening unexpectedly | `local-ai-health.py`, `check-platform-drift.py` |
| Model lane drift | four Gemma roles missing, llama.cpp/Rapid-MLX promoted without approval | `local-ai-health.py`, `/v1/models` |
| Codex skill drift | expected skill directory missing or malformed metadata | `local-ai-health.py` |
| VS Code recommendation drift | required extension recommendations missing from `.vscode/extensions.json` | `local-ai-health.py`, `jq` |
| Boneman reference drift | docs point at duplicate vaults or raw secret files | documentation review, `gitleaks` |

## Current Expected Port State

| Port | Expected | Owner |
|---:|---|---|
| 18080 | listening | oMLX production |
| 8002 | stopped unless explicitly running a llama.cpp lab | llama.cpp manual lane |
| 8010 | stopped unless explicitly running a Rapid-MLX lab | Rapid-MLX manual lane |

## Monitored Configs

| Path | Purpose |
|---|---|
| `config/local-ai-platform/routing-policy.json` | Local model routing contract |
| `config/local-ai-platform/mcp-topology.json` | MCP/client topology |
| `.vscode/extensions.json` | VS Code recommendation baseline |
| `.github/workflows/*.yml` | GitHub Actions workflow baseline |
| `scripts/health/local-ai-health.py` | Low-impact health and drift inputs |
| `scripts/health/drift-detection/baseline.json` | Drift rules |
| `docs/security/secret-inventory.md` | Boneman and secret pointer baseline |

## Remediation Workflow

1. Capture a fresh health snapshot with `--skip-chat`.
2. Run drift detection against the snapshot.
3. Classify findings as intentional lab state, approved change, stale config, or incident.
4. For stale LaunchAgents, prefer archive over deletion.
5. For endpoint/model drift, restore oMLX on `18080` and keep `8002`/`8010` manual unless a benchmark window is active.
6. For skill or extension drift, reinstall or update only the missing item, then rerun validation.
7. For Boneman drift, document item pointers only and never copy secret values into Git.

## Current Result

After archiving `com.corn.vllm-mlx`, the active AI startup set is:

- oMLX production on `18080`;
- `com.corn.omlx-power-policy`;
- no active `com.corn.vllm-mlx` plist;
- llama.cpp and Rapid-MLX stopped unless manually started.

## Cadence

- Run after any LaunchAgent, GitHub Actions, endpoint, model-routing, Codex skill, or VS Code recommendation change.
- Run monthly as part of platform maintenance.
- Treat new listeners on `8002` or `8010` as review items unless a lab session is active.
