#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

tmux kill-session -t rapid-mlx-qwen 2>/dev/null || true
pkill -f 'rapid-mlx serve qwen3.6-35b-4bit' 2>/dev/null || true
"$repo_root/scripts/gemma4-gguf-coding-lane.sh" stop

cat <<'ROLLBACK'
Rolled back optional Hermes/MLX lab lanes.

Default endpoint:
  base_url: http://127.0.0.1:18080/v1
  model: mlx-community--gemma-4-26b-a4b-it-4bit
  provider: custom local Mac endpoint
  API key source: Boneman pointer or ~/.omlx/settings.json at runtime

oMLX is app-managed. If it is not healthy, restart it with:
  osascript -e 'tell application "oMLX" to quit'
  open -a oMLX
ROLLBACK
