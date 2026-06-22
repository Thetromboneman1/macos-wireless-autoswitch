#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

"$repo_root/scripts/gemma4-gguf-coding-lane.sh" stop

echo "Stopped the optional GGUF coding lane."
echo "oMLX is app-managed; quit oMLX manually or with: osascript -e 'tell application \"oMLX\" to quit'"
