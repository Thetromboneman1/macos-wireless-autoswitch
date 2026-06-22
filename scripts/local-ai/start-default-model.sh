#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

"$repo_root/scripts/omlx-power-policy.sh" status >/dev/null
"$repo_root/scripts/gemma4-gguf-coding-lane.sh" start

echo "Default local AI stack is available:"
echo "  oMLX: http://127.0.0.1:18080/v1"
echo "  GGUF coding lane: http://127.0.0.1:8002/v1"
