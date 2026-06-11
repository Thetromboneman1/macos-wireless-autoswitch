#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  scripts/omlx-power-policy.sh status
  scripts/omlx-power-policy.sh normal
  scripts/omlx-power-policy.sh conserve
  scripts/omlx-power-policy.sh battery
  scripts/omlx-power-policy.sh unload-large
  scripts/omlx-power-policy.sh unload-all
  scripts/omlx-power-policy.sh load-fast

Modes:
  normal      Apply balanced idle TTLs for daily plugged-in use.
  conserve   Apply shorter TTLs and unload the largest models immediately.
  battery    Same as conserve, intended for battery/thermal pressure.

Environment:
  OMLX_BASE       oMLX data directory. Default: ~/.omlx
  OMLX_HOST       oMLX host URL without /v1. Default: http://127.0.0.1:18080
  OMLX_RESTART    Restart oMLX after settings edits. Default: 1
USAGE
}

MODE="${1:-status}"
OMLX_BASE="${OMLX_BASE:-$HOME/.omlx}"
OMLX_HOST="${OMLX_HOST:-http://127.0.0.1:18080}"
OMLX_RESTART="${OMLX_RESTART:-1}"
SETTINGS_FILE="$OMLX_BASE/settings.json"
MODEL_SETTINGS_FILE="$OMLX_BASE/model_settings.json"

PRIMARY_MODEL="mlx-community--gemma-4-31b-it-4bit"
CODING_MODEL="mlx-community--gemma-4-26b-a4b-it-4bit"
FAST_MODEL="mlx-community--gemma-4-e4b-it-4bit"
ROUTING_MODEL="mlx-community--gemma-4-e2b-it-4bit"

require_jq() {
  if ! command -v jq >/dev/null 2>&1; then
    echo "jq is required." >&2
    exit 1
  fi
}

api_key() {
  if [ -n "${OMLX_API_KEY:-}" ]; then
    printf '%s' "$OMLX_API_KEY"
    return
  fi
  if [ -f "$SETTINGS_FILE" ]; then
    jq -r '.auth.api_key // empty' "$SETTINGS_FILE"
  fi
}

curl_omlx() {
  local path="$1"
  local key
  key="$(api_key)"
  if [ -n "$key" ]; then
    curl -fsS -H "Authorization: Bearer $key" "$OMLX_HOST$path"
  else
    curl -fsS "$OMLX_HOST$path"
  fi
}

post_omlx() {
  local path="$1"
  local key
  key="$(api_key)"
  if [ -n "$key" ]; then
    curl -fsS -X POST -H "Authorization: Bearer $key" "$OMLX_HOST$path"
  else
    curl -fsS -X POST "$OMLX_HOST$path"
  fi
}

restart_omlx() {
  if [ "$OMLX_RESTART" != "1" ]; then
    echo "Skipped oMLX restart because OMLX_RESTART=$OMLX_RESTART"
    return
  fi

  osascript -e 'tell application "oMLX" to quit' >/dev/null 2>&1 || true
  sleep 2
  open -a oMLX
  echo "Restarted oMLX so persisted TTL/pinning settings are loaded."
}

write_policy() {
  local global_idle="$1"
  local primary_ttl="$2"
  local coding_ttl="$3"
  local fast_ttl="$4"
  local routing_ttl="$5"

  if [ ! -f "$SETTINGS_FILE" ]; then
    echo "Missing $SETTINGS_FILE. Start oMLX once before applying policy." >&2
    exit 1
  fi

  mkdir -p "$OMLX_BASE"

  SETTINGS_FILE="$SETTINGS_FILE" \
  MODEL_SETTINGS_FILE="$MODEL_SETTINGS_FILE" \
  PRIMARY_MODEL="$PRIMARY_MODEL" \
  CODING_MODEL="$CODING_MODEL" \
  FAST_MODEL="$FAST_MODEL" \
  ROUTING_MODEL="$ROUTING_MODEL" \
  GLOBAL_IDLE="$global_idle" \
  PRIMARY_TTL="$primary_ttl" \
  CODING_TTL="$coding_ttl" \
  FAST_TTL="$fast_ttl" \
  ROUTING_TTL="$routing_ttl" \
  python3 - <<'PY'
import json
import os
from pathlib import Path

settings_path = Path(os.environ["SETTINGS_FILE"])
model_settings_path = Path(os.environ["MODEL_SETTINGS_FILE"])

settings = json.loads(settings_path.read_text(encoding="utf-8"))
settings.setdefault("idle_timeout", {})["idle_timeout_seconds"] = int(os.environ["GLOBAL_IDLE"])
tmp = settings_path.with_suffix(".tmp")
tmp.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
tmp.replace(settings_path)

if model_settings_path.exists():
    model_settings = json.loads(model_settings_path.read_text(encoding="utf-8"))
else:
    model_settings = {"version": 1, "settings": {}}
model_settings.setdefault("version", 1)
entries = model_settings.setdefault("settings", {})

policies = {
    os.environ["PRIMARY_MODEL"]: int(os.environ["PRIMARY_TTL"]),
    os.environ["CODING_MODEL"]: int(os.environ["CODING_TTL"]),
    os.environ["FAST_MODEL"]: int(os.environ["FAST_TTL"]),
    os.environ["ROUTING_MODEL"]: int(os.environ["ROUTING_TTL"]),
}

for model_id, ttl in policies.items():
    entry = entries.setdefault(model_id, {})
    entry["ttl_seconds"] = ttl
    entry["is_pinned"] = False

tmp = model_settings_path.with_suffix(".tmp")
tmp.write_text(json.dumps(model_settings, indent=2) + "\n", encoding="utf-8")
tmp.replace(model_settings_path)
PY
}

unload_model() {
  local model_id="$1"
  post_omlx "/v1/models/$model_id/unload" >/dev/null 2>&1 || true
}

load_model() {
  local model_id="$1"
  post_omlx "/v1/models/$model_id/load" >/dev/null
}

status() {
  echo "oMLX health:"
  curl_omlx "/health" | jq '{status, default_model, engine_pool}'
  echo
  echo "Power policy:"
  jq '{idle_timeout}' "$SETTINGS_FILE"
  if [ -f "$MODEL_SETTINGS_FILE" ]; then
    jq --arg p "$PRIMARY_MODEL" --arg c "$CODING_MODEL" --arg f "$FAST_MODEL" --arg r "$ROUTING_MODEL" '
      .settings
      | {
          primary: .[$p],
          coding: .[$c],
          fast: .[$f],
          routing: .[$r]
        }
    ' "$MODEL_SETTINGS_FILE"
  else
    echo "{}"
  fi
}

case "$MODE" in
  status)
    require_jq
    status
    ;;
  normal)
    require_jq
    write_policy 1800 1200 1800 3600 3600
    restart_omlx
    echo "Applied normal oMLX power policy."
    ;;
  conserve)
    require_jq
    write_policy 900 600 900 1200 1800
    restart_omlx
    unload_model "$PRIMARY_MODEL"
    unload_model "$CODING_MODEL"
    echo "Applied conserve oMLX power policy and unloaded large models."
    ;;
  battery)
    require_jq
    write_policy 900 600 900 1200 1800
    restart_omlx
    unload_model "$PRIMARY_MODEL"
    unload_model "$CODING_MODEL"
    echo "Applied battery oMLX power policy and unloaded large models."
    ;;
  unload-large)
    unload_model "$PRIMARY_MODEL"
    unload_model "$CODING_MODEL"
    echo "Requested unload for primary and coding models."
    ;;
  unload-all)
    unload_model "$PRIMARY_MODEL"
    unload_model "$CODING_MODEL"
    unload_model "$FAST_MODEL"
    unload_model "$ROUTING_MODEL"
    echo "Requested unload for all Gemma role models."
    ;;
  load-fast)
    load_model "$FAST_MODEL"
    load_model "$ROUTING_MODEL"
    echo "Loaded fast and routing models."
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
