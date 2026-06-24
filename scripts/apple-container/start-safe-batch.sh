#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
THRESHOLDS="$ROOT/config/apple-container/resource-thresholds.json"
EVIDENCE_ROOT="${APPLE_CONTAINER_EVIDENCE_ROOT:-$HOME/.local/share/apple-container-pilot/evidence}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
EVIDENCE_DIR="$EVIDENCE_ROOT/safe-batch-$STAMP"

mkdir -p "$EVIDENCE_DIR"

record() {
  local name="$1"
  shift
  {
    echo "$ $*"
    "$@"
  } >"$EVIDENCE_DIR/$name" 2>&1 || true
}

memory_pressure_text="$(memory_pressure 2>/dev/null || true)"
pressure_raw="$(printf '%s\n' "$memory_pressure_text" | awk -F': ' '/System-wide memory free percentage|System-wide memory pressure/ {print tolower($NF); exit}')"
case "$pressure_raw" in
  *%)
    pressure_number="${pressure_raw%%%}"
    pressure_state="$(awk -v value="$pressure_number" 'BEGIN {
      if (value >= 20) print "normal";
      else if (value >= 10) print "warn";
      else print "critical";
    }')"
    ;;
  normal|warn|warning|critical)
    pressure_state="${pressure_raw/warning/warn}"
    ;;
  *)
    pressure_state="normal"
    ;;
esac
free_pages="$(vm_stat | awk '/Pages free/ {gsub("\\.","",$3); print $3; exit}')"
free_pages="${free_pages:-0}"

record memory-pressure.txt memory_pressure
record vm-stat.txt vm_stat
record docker-stats.txt docker stats --no-stream
record apple-container-list.txt container ls --all
record apple-container-stats.txt container stats --no-stream

if ! jq -e --arg state "$pressure_state" '.limits.memory_pressure_allowed | index($state)' "$THRESHOLDS" >/dev/null; then
  echo "Refusing Apple Container batch: memory pressure state '$pressure_state' is outside configured allowance." >&2
  exit 2
fi

minimum_free_pages="$(jq -r '.limits.minimum_free_pages' "$THRESHOLDS")"
if [ "$free_pages" -lt "$minimum_free_pages" ]; then
  echo "Refusing Apple Container batch: free pages $free_pages below threshold $minimum_free_pages." >&2
  exit 2
fi

before_swap="$(sysctl -n vm.swapusage 2>/dev/null | awk '{for (i=1;i<=NF;i++) if ($i=="used") {print $(i+2); exit}}' | tr -d 'M')"
before_swap="${before_swap:-0}"
printf '%s\n' "$before_swap" >"$EVIDENCE_DIR/swap-before-mb.txt"

"$ROOT/scripts/apple-container/start-all.sh"

sleep "$(jq -r '.limits.post_start_observation_seconds' "$THRESHOLDS")"
record post-memory-pressure.txt memory_pressure
record post-vm-stat.txt vm_stat
record post-docker-stats.txt docker stats --no-stream
record post-apple-container-stats.txt container stats --no-stream

after_swap="$(sysctl -n vm.swapusage 2>/dev/null | awk '{for (i=1;i<=NF;i++) if ($i=="used") {print $(i+2); exit}}' | tr -d 'M')"
after_swap="${after_swap:-0}"
printf '%s\n' "$after_swap" >"$EVIDENCE_DIR/swap-after-mb.txt"

max_growth="$(jq -r '.limits.maximum_swap_growth_mb_per_batch' "$THRESHOLDS")"
growth="$(awk -v after="$after_swap" -v before="$before_swap" 'BEGIN { printf "%.0f", after - before }')"
if [ "$growth" -gt "$max_growth" ]; then
  echo "Swap grew by ${growth}MB, above ${max_growth}MB; stopping newly started enabled mirrors." >&2
  "$ROOT/scripts/apple-container/stop-all.sh" || true
  exit 3
fi

"$ROOT/scripts/apple-container/health-all.sh"
echo "Apple Container safe batch evidence: $EVIDENCE_DIR"
