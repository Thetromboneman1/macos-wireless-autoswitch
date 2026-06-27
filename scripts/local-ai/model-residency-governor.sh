#!/usr/bin/env bash
set -euo pipefail

ROOT="${LOCAL_AI_PLATFORM_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
POLICY="${LOCAL_AI_RESIDENCY_POLICY:-$ROOT/config/local-ai-platform/residency-policy.json}"
LOG_FILE="${LOCAL_AI_RESIDENCY_LOG:-$HOME/.local/state/local-ai-model-residency-governor.log}"
HIGH_SWAP="${LOCAL_AI_HIGH_SWAP_PERCENT:-}"
CRITICAL_SWAP="${LOCAL_AI_CRITICAL_SWAP_PERCENT:-}"
LOOP_INTERVAL="${LOCAL_AI_RESIDENCY_INTERVAL:-}"
DRY_RUN="${LOCAL_AI_RESIDENCY_DRY_RUN:-0}"

usage() {
  cat <<'USAGE'
Usage: scripts/local-ai/model-residency-governor.sh <command>

Commands:
  status      Print swap pressure, listener state, and policy thresholds
  enforce     Stop optional heavy lanes when swap crosses policy thresholds
  loop        Run enforce forever, sleeping between checks

Environment overrides:
  LOCAL_AI_RESIDENCY_POLICY       Policy JSON path
  LOCAL_AI_HIGH_SWAP_PERCENT      Default: policy thresholds.high_swap_used_percent
  LOCAL_AI_CRITICAL_SWAP_PERCENT  Default: policy thresholds.critical_swap_used_percent
  LOCAL_AI_RESIDENCY_INTERVAL     Default: policy thresholds.loop_interval_seconds
  LOCAL_AI_RESIDENCY_DRY_RUN=1    Print actions without stopping lanes
USAGE
}

log() {
  mkdir -p "$(dirname "$LOG_FILE")"
  printf '%s %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$*" | tee -a "$LOG_FILE"
}

json_value() {
  jq -r "$1" "$POLICY"
}

load_policy() {
  if [ ! -f "$POLICY" ]; then
    echo "Missing residency policy: $POLICY" >&2
    exit 1
  fi
  HIGH_SWAP="${HIGH_SWAP:-$(json_value '.thresholds.high_swap_used_percent')}"
  CRITICAL_SWAP="${CRITICAL_SWAP:-$(json_value '.thresholds.critical_swap_used_percent')}"
  LOOP_INTERVAL="${LOOP_INTERVAL:-$(json_value '.thresholds.loop_interval_seconds')}"
}

swap_used_percent() {
  sysctl -n vm.swapusage |
    awk '
      {
        total=0; used=0
        for (i=1; i<=NF; i++) {
          if ($i == "total") { total=$(i+2) }
          if ($i == "used") { used=$(i+2) }
        }
        gsub(/M/, "", total)
        gsub(/M/, "", used)
        if (total > 0) {
          printf "%.1f\n", (used / total) * 100
        } else {
          print "0.0"
        }
      }'
}

port_listening() {
  local port="$1"
  lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1
}

listener_pids() {
  local port="$1"
  lsof -nP -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null || true
}

stop_by_port() {
  local name="$1"
  local port="$2"
  local pids
  pids="$(listener_pids "$port")"
  if [ -z "$pids" ]; then
    log "$name already stopped"
    return 0
  fi
  if [ "$DRY_RUN" = "1" ]; then
    log "dry-run stop $name pids: $pids"
    return 0
  fi
  log "stopping $name pids: $pids"
  # shellcheck disable=SC2086
  kill $pids 2>/dev/null || true
}

stop_by_manager() {
  local name="$1"
  local manager="$2"
  local port="$3"
  if [ "$DRY_RUN" = "1" ]; then
    log "dry-run stop $name with $manager stop"
    return 0
  fi
  if [ ! -x "$ROOT/$manager" ]; then
    log "manager unavailable for $name: $ROOT/$manager; falling back to port $port"
    stop_by_port "$name" "$port"
    return 0
  fi
  log "stopping $name with $manager stop"
  "$ROOT/$manager" stop
}

stop_rapid_mlx() {
  local pids
  pids="$(listener_pids 8010)"
  if [ -z "$pids" ]; then
    log "rapid-mlx-qwen36 already stopped"
    return 0
  fi
  if [ "$DRY_RUN" = "1" ]; then
    log "dry-run stop rapid-mlx-qwen36 pids: $pids"
    return 0
  fi
  log "stopping rapid-mlx-qwen36 pids: $pids"
  # shellcheck disable=SC2086
  kill $pids 2>/dev/null || true
}

warm_omlx_front_door() {
  curl -fsS --max-time 3 "http://127.0.0.1:18080/health" >/dev/null 2>&1 || true
}

status() {
  load_policy
  local used
  used="$(swap_used_percent)"
  printf 'policy=%s\n' "$POLICY"
  printf 'swap_used_percent=%s\n' "$used"
  printf 'high_swap_threshold=%s\n' "$HIGH_SWAP"
  printf 'critical_swap_threshold=%s\n' "$CRITICAL_SWAP"
  for port in 18080 8002 8003 8010; do
    if port_listening "$port"; then
      printf 'port_%s=running\n' "$port"
    else
      printf 'port_%s=stopped\n' "$port"
    fi
  done
}

enforce() {
  load_policy
  warm_omlx_front_door
  local used
  used="$(swap_used_percent)"
  log "swap_used_percent=$used high=$HIGH_SWAP critical=$CRITICAL_SWAP"

  if awk -v used="$used" -v high="$HIGH_SWAP" 'BEGIN { exit !(used >= high) }'; then
    if port_listening 8003; then
      stop_by_manager "ornith-35b-gguf" "scripts/ornith-gguf-coding-lane.sh" "8003"
    else
      log "ornith-35b-gguf already stopped"
    fi
    if port_listening 8010; then
      stop_rapid_mlx
    else
      log "rapid-mlx-qwen36 already stopped"
    fi
  fi

  if awk -v used="$used" -v critical="$CRITICAL_SWAP" 'BEGIN { exit !(used >= critical) }'; then
    if port_listening 8002; then
      stop_by_manager "gemma-gguf-coding-fallback" "scripts/gemma4-gguf-coding-lane.sh" "8002"
    else
      log "gemma-gguf-coding-fallback already stopped"
    fi
  fi
}

loop() {
  load_policy
  log "starting local AI model residency loop interval=${LOOP_INTERVAL}s"
  while true; do
    enforce
    sleep "$LOOP_INTERVAL"
  done
}

cmd="${1:-}"
case "$cmd" in
  status) status ;;
  enforce) enforce ;;
  loop) loop ;;
  -h|--help|help|"") usage ;;
  *) echo "Unknown command: $cmd" >&2; usage; exit 2 ;;
esac
