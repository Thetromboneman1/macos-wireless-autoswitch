#!/usr/bin/env bash
set -euo pipefail

export OCTOPODA_API_KEY="${OCTOPODA_API_KEY:-local}"
port="${OCTOPODA_PORT:-7842}"
api_port="${OCTOPODA_API_PORT:-7843}"

exec octopoda --port "$port" --api-port "$api_port" --no-browser "$@"
