#!/usr/bin/env bash
set -euo pipefail

omlx_auth="${OMLX_API_KEY:-mlx-local}"
omlx_base="${OMLX_BASE_URL:-http://127.0.0.1:18080}"
gguf_base="${GGUF_CODING_BASE_URL:-http://127.0.0.1:8002}"

echo "oMLX health:"
curl -fsS -H "Authorization: Bearer $omlx_auth" "$omlx_base/health" | jq .

echo "oMLX models:"
curl -fsS -H "Authorization: Bearer $omlx_auth" "$omlx_base/v1/models" | jq -r '.data[].id'

echo "GGUF coding models:"
curl -fsS "$gguf_base/v1/models" | jq -r '.data[].id'
