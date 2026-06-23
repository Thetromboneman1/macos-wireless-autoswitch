#!/usr/bin/env bash
set -euo pipefail

PILOT_ROOT="${APPLE_CONTAINER_PILOT_ROOT:-$HOME/.local/share/apple-container-pilot}"

case "$PILOT_ROOT" in
  "$HOME"/.local/share/apple-container-pilot*) ;;
  *)
    echo "Refusing to reset unexpected pilot root: $PILOT_ROOT" >&2
    exit 2
    ;;
esac

mkdir -p "$PILOT_ROOT/backups"
if [[ -d "$PILOT_ROOT/data" || -d "$PILOT_ROOT/volumes" || -d "$PILOT_ROOT/state" ]]; then
  stamp="$(date -u +%Y%m%dT%H%M%SZ)"
  archive="$PILOT_ROOT/backups/test-data-$stamp.tar.gz"
  tar -czf "$archive" -C "$PILOT_ROOT" data volumes state 2>/dev/null || true
  echo "Backed up existing pilot test data to $archive"
fi

rm -rf "$PILOT_ROOT/data" "$PILOT_ROOT/volumes" "$PILOT_ROOT/state"
mkdir -p "$PILOT_ROOT/data" "$PILOT_ROOT/volumes" "$PILOT_ROOT/state" "$PILOT_ROOT/logs" "$PILOT_ROOT/env" "$PILOT_ROOT/benchmarks"
echo "Reset Apple Container pilot test data under $PILOT_ROOT"
