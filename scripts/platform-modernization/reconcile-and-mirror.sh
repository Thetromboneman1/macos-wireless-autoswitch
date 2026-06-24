#!/usr/bin/env bash
set -euo pipefail

BONEMAN_PROJECTS_ROOT="${BONEMAN_PROJECTS_ROOT:-$HOME/Documents/Boneman_Projects}"
CANONICAL="$BONEMAN_PROJECTS_ROOT/scripts/platform-modernization/reconcile-and-mirror.sh"

if [ ! -x "$CANONICAL" ]; then
  echo "Canonical platform modernization controller not found: $CANONICAL" >&2
  echo "Set BONEMAN_PROJECTS_ROOT to the Boneman_Projects checkout." >&2
  exit 2
fi

exec "$CANONICAL" "$@"
