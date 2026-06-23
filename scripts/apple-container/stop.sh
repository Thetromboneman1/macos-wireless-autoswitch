#!/usr/bin/env bash
set -euo pipefail

if ! command -v container >/dev/null 2>&1; then
  echo "container CLI is not installed; nothing to stop."
  exit 0
fi

if ! container system status >/dev/null 2>&1; then
  echo "Apple Container system service is stopped; nothing to stop."
  exit 0
fi

pilot_count=0
while IFS= read -r name; do
  pilot_count=$((pilot_count + 1))
  echo "Stopping pilot container: $name"
  container stop "$name" >/dev/null 2>&1 || true
done < <(container ls -a 2>/dev/null | awk 'NR > 1 && $1 ~ /^ac-/ {print $1}')

if [[ "$pilot_count" -eq 0 ]]; then
  echo "No ac- pilot containers found."
fi
