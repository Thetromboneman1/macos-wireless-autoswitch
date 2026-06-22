#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TOOL_HOME="${STAR_TOOL_HOME:-$HOME/.local/share/codex-star-tools}"
OMLX_BASE="${OMLX_BASE_URL:-http://127.0.0.1:18080}"
GGUF_BASE="${GGUF_BASE_URL:-http://127.0.0.1:8002}"

section() {
  printf '\n== %s ==\n' "$1"
}

ok() {
  printf 'ok  %s\n' "$1"
}

warn() {
  printf 'warn  %s\n' "$1"
}

have() {
  if command -v "$1" >/dev/null 2>&1; then
    ok "$1: $(command -v "$1")"
  else
    warn "$1: not found"
  fi
}

endpoint() {
  local name="$1"
  local url="$2"
  if curl -fsS --max-time 2 "$url" >/dev/null 2>&1; then
    ok "$name: $url"
  else
    warn "$name: $url unavailable"
  fi
}

path_status() {
  local kind="$1"
  local path="$2"
  local label="$3"
  if [ "$kind" = "file" ] && [ -x "$path" ]; then
    ok "$label"
  elif [ "$kind" = "dir" ] && [ -d "$path" ]; then
    ok "$label"
  else
    warn "$label missing"
  fi
}

doc_status() {
  local doc="$1"
  if [ -f "$ROOT/$doc" ]; then
    ok "$doc"
  else
    warn "$doc missing"
  fi
}

section "Commands"
for cmd in codex opencode goose hermes openclaw uv docker mlx_lm leann leann_mcp octopoda octopoda-mcp op gh; do
  have "$cmd"
done

section "Installed star tools"
path_status file "$TOOL_HOME/envs/edge-lm/bin/python" "edge-lm env"
path_status file "$TOOL_HOME/envs/ponyexl3/bin/python" "PonyExl3 env"
path_status file "$TOOL_HOME/envs/turbovec/bin/python" "turbovec env"
path_status file "$ROOT/tmp/star-downloads/kennss__SiliconScope/.build/debug/sscope-cli" "SiliconScope CLI"
path_status file "$ROOT/tmp/star-downloads/headroomlabs-ai__headroom/target/release/headroom-proxy" "headroom proxy"
path_status dir "$ROOT/tmp/star-downloads/diegosouzapw__OmniRoute/node_modules" "OmniRoute deps"
path_status dir "$HOME/.understand-anything/repo/node_modules" "Understand-Anything deps"

section "Model endpoints"
endpoint "oMLX health" "$OMLX_BASE/health"
endpoint "llama.cpp health" "$GGUF_BASE/health"

section "Docker images"
if docker image inspect ghcr.io/openhands/agent-server:1.29.0-python >/dev/null 2>&1; then
  ok "OpenHands agent-server image"
else
  warn "OpenHands agent-server image missing"
fi

section "1Password vaults"
if command -v op >/dev/null 2>&1; then
  if op vault get Boneman --format json >/dev/null 2>&1; then
    ok "Boneman vault available"
  else
    warn "Boneman vault unavailable"
  fi
  if op vault get "Boneman Projects" --format json >/dev/null 2>&1; then
    count="$(op item list --vault "Boneman Projects" --format json 2>/dev/null | jq 'length' 2>/dev/null || printf '?')"
    warn "Boneman Projects duplicate vault exists; item count: $count"
  fi
else
  warn "op CLI unavailable"
fi

section "Docs"
for doc in \
  docs/autonomous-modernization/16-unified-ai-platform-architecture.md \
  docs/autonomous-modernization/17-ai-platform-integration-report.md \
  docs/security/secret-inventory.md \
  docs/architecture/mcp-topology.md \
  docs/architecture/model-routing.md \
  docs/architecture/knowledge-layer.md \
  docs/operations/platform-runbook.md; do
  doc_status "$doc"
done
