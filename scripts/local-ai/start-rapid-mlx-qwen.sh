#!/usr/bin/env bash
set -euo pipefail

MODEL_ALIAS="${RAPID_MLX_MODEL_ALIAS:-qwen3.6-35b-4bit}"
HOST="${RAPID_MLX_HOST:-127.0.0.1}"
PORT="${RAPID_MLX_PORT:-8010}"
SERVED_MODEL_NAME="${RAPID_MLX_SERVED_MODEL_NAME:-qwen3.6-35b-4bit}"

if ! command -v rapid-mlx >/dev/null 2>&1; then
  echo "rapid-mlx is not installed. Run: uv tool install rapid-mlx@latest" >&2
  exit 1
fi

if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Port $PORT is already in use. Stop that service or set RAPID_MLX_PORT." >&2
  exit 1
fi

RAPID_MLX_TELEMETRY=0 exec rapid-mlx serve "$MODEL_ALIAS" \
  --host "$HOST" \
  --port "$PORT" \
  --served-model-name "$SERVED_MODEL_NAME" \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder_xml \
  --reasoning-parser qwen3 \
  --kv-cache-quantization \
  --kv-cache-quantization-bits 8 \
  --no-spec-decode \
  --default-temperature 0.6 \
  --default-top-p 0.95 \
  --default-top-k 20
