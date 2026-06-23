#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT_DIR="${AIOPS_OUTPUT_DIR:-$ROOT/docs/operations/reports}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"

mkdir -p "$OUT_DIR"

health_json="$OUT_DIR/health-$STAMP.json"
drift_json="$OUT_DIR/drift-$STAMP.json"
dependency_json="$OUT_DIR/dependencies-$STAMP.json"
doc_json="$OUT_DIR/documentation-$STAMP.json"
prompt_size_json="$OUT_DIR/hermes-prompt-size-$STAMP.json"
hermes_cost_json="$OUT_DIR/hermes-cost-$STAMP.json"
platform_json="$OUT_DIR/platform-report-$STAMP.json"

cd "$ROOT"

scripts/health/local-ai-health.py --skip-chat --json "$health_json" >/dev/null
scripts/health/drift-detection/check-platform-drift.py --health-json "$health_json" --json "$drift_json" >/dev/null
scripts/operations/dependency-report.py --json "$dependency_json" >/dev/null
doc_status=0
scripts/operations/documentation-review.py docs/operations docs/governance docs/architecture docs/macos docs/security docs/skills docs/executive docs/roadmap docs/capacity docs/disaster-recovery --json "$doc_json" >/dev/null || doc_status=$?
hermes prompt-size --json > "$prompt_size_json"
scripts/operations/hermes-cost-report.py \
  --prompt-size-json "$prompt_size_json" \
  --health-json "$health_json" \
  --json "$hermes_cost_json" >/dev/null
scripts/operations/generate-platform-report.py \
  --health-json "$health_json" \
  --drift-json "$drift_json" \
  --dependency-json "$dependency_json" \
  --documentation-json "$doc_json" \
  --hermes-cost-json "$hermes_cost_json" \
  --json "$platform_json" >/dev/null

if [[ -n "${AIOPS_BENCH_BASELINE:-}" && -n "${AIOPS_BENCH_CURRENT:-}" ]]; then
  scripts/operations/benchmark-governance.py \
    --baseline "$AIOPS_BENCH_BASELINE" \
    --current "$AIOPS_BENCH_CURRENT" \
    --json "$OUT_DIR/benchmark-comparison-$STAMP.json" >/dev/null
fi

printf '%s\n' "$platform_json"
exit "$doc_status"
