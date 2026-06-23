#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo "== Apple Container system =="
if command -v container >/dev/null 2>&1; then
  container --version || true
  container system status || true
else
  echo "container CLI is not installed"
fi

echo
echo "== Pilot port map =="
"$ROOT/scripts/apple-container/validate-port-map.sh" || true

echo
echo "== Pilot containers =="
if command -v container >/dev/null 2>&1; then
  container ls -a 2>/dev/null | awk 'NR == 1 || $1 ~ /^ac-/'
fi

echo
echo "== Production sentinels =="
for port in 18080 8002 8010 3000 4096 4097 7000 8080 8091 8100 8787 18789; do
  if lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1; then
    echo "listening: $port"
  else
    echo "stopped:   $port"
  fi
done
