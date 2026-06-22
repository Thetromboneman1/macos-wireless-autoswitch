#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo "oMLX chat smoke:"
curl -fsS http://127.0.0.1:18080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer ${OMLX_API_KEY:-mlx-local}" \
  -d '{"model":"mlx-community--gemma-4-e4b-it-4bit","messages":[{"role":"user","content":"Reply with exactly: OK"}],"max_tokens":8,"temperature":0}' \
  | jq -r '.choices[0].message.content'

echo "GGUF coding lane smoke:"
"$repo_root/scripts/gemma4-gguf-coding-lane.sh" bench
