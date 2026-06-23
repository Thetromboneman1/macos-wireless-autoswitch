#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

"$ROOT/scripts/apple-container/validate-port-map.sh"

if ! command -v container >/dev/null 2>&1; then
  echo "container CLI is not installed" >&2
  exit 1
fi

if ! container system status >/dev/null 2>&1; then
  echo "Apple Container system service is not running. Start it with: container system start" >&2
  exit 1
fi

echo "Apple Container pilot start is gated."
echo "No mirrored workload will be started until its Compose translation, storage isolation, and health check are committed."
