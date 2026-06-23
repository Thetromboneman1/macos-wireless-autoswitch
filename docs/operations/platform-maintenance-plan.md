# Platform Maintenance Plan

Date: 2026-06-23

## Cadence

| Work | Cadence | Command or Artifact |
|---|---|---|
| Daily health check | Daily before heavy work | `scripts/health/local-ai-health.py` |
| Endpoint validation | Weekly or after config changes | `scripts/local-ai/validate-hermes-mlx.py` |
| Benchmark refresh | Monthly or after model/backend changes | `scripts/local-ai/benchmark-engine-bakeoff.py` |
| Model catalog review | Monthly | `docs/benchmarks/production-model-catalog.md` |
| Backend review | Quarterly | oMLX, llama.cpp, Rapid-MLX versions and changelogs |
| Secret inventory review | Monthly | `docs/security/secret-inventory.md` and Boneman |
| Documentation review | Monthly | `docs/README.md` |
| Long-duration soak | Before lane promotion | `docs/benchmarks/long-duration-stability.md` |

## Backup Strategy

- Keep raw secrets out of Git.
- Store secret pointers in docs and values in Boneman or local runtime settings.
- Before major host config changes, copy affected user config files to a timestamped directory under `~/.local/share/codex-star-tools/backups/`.

## Rollback Strategy

Default rollback is direct oMLX:

```text
base_url: http://127.0.0.1:18080/v1
model: mlx-community--gemma-4-26b-a4b-it-4bit
```

Stop optional lab lanes first:

```bash
scripts/local-ai/rollback-hermes-mlx.sh
```

## Lane Promotion Process

1. Add or update the lane in `config/local-ai-platform/routing-policy.json`.
2. Validate endpoint models, chat, and tool calling.
3. Run smoke benchmark and 1h soak.
4. Run 4h soak for production candidates.
5. Update `docs/benchmarks/production-model-catalog.md`.
6. Update runbook and rollback instructions.
7. Commit docs/config/scripts together after validation.
