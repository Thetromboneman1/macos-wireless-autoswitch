# Hermes MLX Runbook

Date: 2026-06-22

## Health

```bash
curl -fsS http://127.0.0.1:18080/health
curl -fsS -H "Authorization: Bearer ${OMLX_API_KEY:-mlx-local}" http://127.0.0.1:18080/v1/models
scripts/local-ai/validate-hermes-mlx.py --name omlx-gemma26
```

## Start Optional Lanes

```bash
scripts/gemma4-gguf-coding-lane.sh start
scripts/local-ai/start-rapid-mlx-qwen.sh
```

Run Rapid-MLX in its own terminal or tmux session. It binds to `127.0.0.1:8010` and forces `RAPID_MLX_TELEMETRY=0`.

## Validate Rapid-MLX

```bash
scripts/local-ai/validate-hermes-mlx.py \
  --name rapid-mlx-qwen36 \
  --base-url http://127.0.0.1:8010/v1 \
  --model qwen3.6-35b-4bit \
  --api-key '' \
  --out docs/autonomous-modernization/hermes-mlx-validation-rapid-mlx.json
```

## Benchmark

```bash
scripts/local-ai/benchmark-engine-bakeoff.py
```

The benchmark is intentionally an operational smoke bake-off, not a long soak test.

## Rollback

```bash
scripts/local-ai/rollback-hermes-mlx.sh
```

## Hermes Host Defaults

```bash
hermes config set model.provider custom
hermes config set model.api_mode chat_completions
hermes config set model.base_url http://127.0.0.1:18080/v1
hermes config set model.default mlx-community--gemma-4-26b-a4b-it-4bit
```

Keep any real API keys in `Boneman` or the existing local runtime settings. Do not commit secret values.
