#!/usr/bin/env bash
set -euo pipefail

plan_file="${1:-docs/autonomous-modernization/github-stars-implementation-plan.json}"

if [ ! -f "$plan_file" ]; then
  echo "Missing plan file: $plan_file" >&2
  exit 1
fi

jq -r '
  .items[]
  | select(.classification != "Skip")
  | "## " + .full_name + "\n"
    + "classification: " + .classification + "\n"
    + "reason: " + .reason + "\n"
    + "risk: " + .risk + "\n"
    + "onepassword: " + .onepassword + "\n"
' "$plan_file"
