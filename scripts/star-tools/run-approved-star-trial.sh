#!/usr/bin/env bash
set -euo pipefail

plan_file="${PLAN_FILE:-docs/autonomous-modernization/github-stars-approved-execution.json}"
trial_root="${STAR_TRIAL_ROOT:-tmp/star-downloads}"

usage() {
  cat <<'USAGE'
Usage: scripts/star-tools/run-approved-star-trial.sh <owner/repo>

Creates or updates a shallow local checkout for an approved GitHub-star trial
under tmp/star-downloads/. It does not install services, start daemons, pull
models, write secrets, or alter the default Codex/OpenCode/Hermes/DNS stack.
USAGE
}

repo="${1:-}"
if [ -z "$repo" ] || [ "$repo" = "-h" ] || [ "$repo" = "--help" ]; then
  usage
  exit 0
fi

if [ ! -f "$plan_file" ]; then
  echo "Missing plan file: $plan_file" >&2
  exit 1
fi

bucket="$(jq -r --arg repo "$repo" '.items[] | select(.full_name == $repo) | .execution_bucket // empty' "$plan_file")"
if [ -z "$bucket" ]; then
  echo "Repo is not in approved execution plan: $repo" >&2
  exit 2
fi

case "$bucket" in
  "Create Trial Harness"|"Download Needed Files"|"Document Only"|"Configure Existing Tool") ;;
  *)
    echo "Repo is not approved for a local trial. Bucket: $bucket" >&2
    exit 3
    ;;
esac

mkdir -p "$trial_root"
target="$trial_root/${repo//\//__}"
url="https://github.com/$repo.git"

if [ -d "$target/.git" ]; then
  git -C "$target" fetch --depth 1 origin
  git -C "$target" reset --hard FETCH_HEAD
else
  git clone --depth 1 "$url" "$target"
fi

echo "Trial checkout ready: $target"
echo "Bucket: $bucket"
echo "Review README and install docs before running anything inside the checkout."
