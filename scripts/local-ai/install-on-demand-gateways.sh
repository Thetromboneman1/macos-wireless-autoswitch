#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BIN_DIR="$HOME/.local/bin"
CONFIG_DIR="$HOME/.config/local-ai"
STATE_DIR="$HOME/.local/state"
LAUNCH_DIR="$HOME/Library/LaunchAgents"

install_one_plist() {
  local plist="$1"
  mkdir -p "$LAUNCH_DIR"
  cp "$ROOT/launchd/$plist" "$LAUNCH_DIR/$plist"
  launchctl bootout "gui/$(id -u)" "$LAUNCH_DIR/$plist" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$LAUNCH_DIR/$plist"
}

mkdir -p "$BIN_DIR" "$CONFIG_DIR" "$STATE_DIR"

install -m 0755 "$ROOT/scripts/local-ai/on-demand-lane-gateway.py" "$BIN_DIR/local-ai-on-demand-lane-gateway.py"
install -m 0755 "$ROOT/scripts/local-ai/model-residency-governor.sh" "$BIN_DIR/local-ai-model-residency-governor.sh"
install -m 0755 "$ROOT/scripts/gemma4-gguf-coding-lane.sh" "$BIN_DIR/local-ai-gemma4-gguf-coding-lane.sh"
install -m 0755 "$ROOT/scripts/ornith-gguf-coding-lane.sh" "$BIN_DIR/local-ai-ornith-gguf-coding-lane.sh"
install -m 0755 "$ROOT/scripts/local-ai/start-rapid-mlx-qwen.sh" "$BIN_DIR/local-ai-start-rapid-mlx-qwen.sh"
cp "$ROOT/config/local-ai-platform/residency-policy.json" "$CONFIG_DIR/residency-policy.json"

plutil -lint \
  "$ROOT/launchd/com.corn.local-ai-gemma-gguf-gateway.plist" \
  "$ROOT/launchd/com.corn.local-ai-ornith-gateway.plist" \
  "$ROOT/launchd/com.corn.local-ai-rapid-mlx-gateway.plist" \
  "$ROOT/launchd/com.corn.local-ai-residency-governor.plist"

install_one_plist "com.corn.local-ai-gemma-gguf-gateway.plist"
install_one_plist "com.corn.local-ai-ornith-gateway.plist"
install_one_plist "com.corn.local-ai-rapid-mlx-gateway.plist"
install_one_plist "com.corn.local-ai-residency-governor.plist"

launchctl kickstart -k "gui/$(id -u)/com.corn.local-ai-gemma-gguf-gateway"
launchctl kickstart -k "gui/$(id -u)/com.corn.local-ai-ornith-gateway"
launchctl kickstart -k "gui/$(id -u)/com.corn.local-ai-rapid-mlx-gateway"
launchctl kickstart -k "gui/$(id -u)/com.corn.local-ai-residency-governor"

echo "Installed local AI on-demand gateways and residency governor."
