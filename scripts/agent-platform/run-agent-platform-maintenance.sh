#!/usr/bin/env bash
set -euo pipefail

base="$HOME/Library/Application Support/BonemanAgentPlatform"
export PATH="$base/bin:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
mcporter_config="${BONEMAN_MCPORTER_CONFIG:-/Users/corn/Documents/Corn_Automation/macos-wireless-autoswitch/config/mcporter.json}"
log_dir="$base/logs"
report_dir="$base/generated/reports"
mkdir -p "$log_dir" "$report_dir"

stamp="$(date -u +%Y%m%dT%H%M%SZ)"
log="$log_dir/maintenance-$stamp.log"

run_limited() {
  local seconds="$1"
  shift
  python3 - "$seconds" "$@" <<'PY'
import subprocess
import sys

seconds = int(sys.argv[1])
cmd = sys.argv[2:]
try:
    completed = subprocess.run(cmd, timeout=seconds, check=False)
    raise SystemExit(completed.returncode)
except subprocess.TimeoutExpired:
    print(f"timeout after {seconds}s: {' '.join(cmd)}", file=sys.stderr)
    raise SystemExit(124)
PY
}

{
  echo "started_at=$stamp"
  run_limited 60 boneman-agent-platform doctor >/dev/null || true
  agent-reach doctor --json > "$report_dir/agent-reach-doctor-maintenance.json"
  run_limited 45 agent-reach check-update || true
  run_limited 45 mcporter --config "$mcporter_config" list || true
  run_limited 15 designmd spec >/dev/null || true
  find "$log_dir" -name 'maintenance-*.log' -mtime +45 -delete
  echo "completed_at=$(date -u +%Y%m%dT%H%M%SZ)"
} >>"$log" 2>&1
