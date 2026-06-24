#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MAX_ITERATIONS="${MAX_ITERATIONS:-1}"
iteration=0

while [ "$iteration" -lt "$MAX_ITERATIONS" ]; do
  iteration=$((iteration + 1))
  echo "modernization iteration $iteration of $MAX_ITERATIONS"

  "$ROOT/scripts/repository-governance/generate-repository-governance.py"
  git diff --check

  if [ "${RUN_APPLE_CONTAINER_SAFE_BATCH:-false}" = "true" ]; then
    "$ROOT/scripts/apple-container/start-safe-batch.sh"
  fi

  if [ "${RUN_VALIDATION:-false}" = "true" ]; then
    uvx pytest tests/test_repository_governance.py tests/test_apple_container_pilot.py
  fi
done
