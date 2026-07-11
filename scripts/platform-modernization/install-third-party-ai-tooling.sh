#!/bin/bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AUDIT_ROOT="${AUDIT_ROOT:-/Users/corn/Documents/Boneman_Projects/local-ai-platform/third-party-tool-audit}"
SOURCE_ROOT="$AUDIT_ROOT/sources"
MANIFEST="$AUDIT_ROOT/manifest.json"
MAX_PASSES="${MAX_PASSES:-3}"

REPOS=(
  "mukul975/Anthropic-Cybersecurity-Skills"
  "asgeirtj/system_prompts_leaks"
  "decolua/9router"
  "Osmantic/ODS"
  "itsfatduck/optimizerDuck"
  "inkeep/open-knowledge"
  "JustVugg/colibri"
  "tirth8205/code-review-graph"
)

SKILL_ROOTS=(
  "$HOME/.codex/skills"
  "$HOME/.agents/skills"
  "$HOME/.claude/skills"
  "$HOME/.config/goose/skills"
  "$HOME/.hermes/skills"
)

log() {
  printf '[third-party-ai-tooling] %s\n' "$*"
}

require_tools() {
  local missing=()
  local tool
  for tool in git python3 jq; do
    if ! command -v "$tool" >/dev/null 2>&1; then
      missing+=("$tool")
    fi
  done

  if ((${#missing[@]} > 0)); then
    printf 'Missing required tools: %s\n' "${missing[*]}" >&2
    return 1
  fi
}

clone_or_refresh_repos() {
  mkdir -p "$SOURCE_ROOT"

  local repo dir url branch
  for repo in "${REPOS[@]}"; do
    dir="$SOURCE_ROOT/${repo#*/}"
    url="https://github.com/$repo.git"
    if [[ -d "$dir/.git" ]]; then
      log "Refreshing $repo"
      git -C "$dir" fetch --depth=1 origin
      branch="$(git -C "$dir" remote show origin | sed -n 's/.*HEAD branch: //p')"
      branch="${branch:-main}"
      git -C "$dir" checkout -q "$branch" || true
      git -C "$dir" reset --hard -q "origin/$branch"
    else
      log "Cloning $repo"
      git clone --depth=1 "$url" "$dir"
    fi
  done
}

install_cybersecurity_skills() {
  local src="$SOURCE_ROOT/Anthropic-Cybersecurity-Skills/skills"
  if [[ ! -d "$src" ]]; then
    printf 'Missing cybersecurity skills source: %s\n' "$src" >&2
    return 1
  fi

  local root skill name target installed_count
  installed_count=0
  for root in "${SKILL_ROOTS[@]}"; do
    [[ -d "$root" ]] || continue
    for skill in "$src"/*; do
      [[ -d "$skill" && -f "$skill/SKILL.md" ]] || continue
      name="cybersecurity-$(basename "$skill")"
      target="$root/$name"
      if [[ -L "$target" ]]; then
        ln -sfn "$skill" "$target"
      elif [[ -e "$target" ]]; then
        log "Preserving existing non-symlink skill $target"
        continue
      else
        ln -s "$skill" "$target"
      fi
      installed_count=$((installed_count + 1))
    done
  done

  log "Installed or refreshed $installed_count cybersecurity skill links"
}

verify_code_review_graph() {
  local status="unavailable"
  if command -v code-review-graph >/dev/null 2>&1; then
    status="$(code-review-graph --version 2>/dev/null || printf installed)"
  elif command -v uvx >/dev/null 2>&1; then
    status="$(uvx --from code-review-graph code-review-graph --version 2>/dev/null || printf 'uvx available')"
  fi
  printf '%s\n' "$status" > "$AUDIT_ROOT/code-review-graph.status"
  log "code-review-graph status: $status"
}

write_manifest() {
  mkdir -p "$AUDIT_ROOT"
  python3 - "$SOURCE_ROOT" "$MANIFEST" "$AUDIT_ROOT/code-review-graph.status" <<'PY'
import json
import subprocess
import sys
from pathlib import Path

source_root = Path(sys.argv[1])
manifest_path = Path(sys.argv[2])
crg_status_path = Path(sys.argv[3])

decisions = {
    "Anthropic-Cybersecurity-Skills": ("installed", "Apache-2.0 structured cybersecurity skills installed into local skill roots with cybersecurity- prefixes."),
    "system_prompts_leaks": ("audit-only", "Leaked system-prompt corpus; not copied into prompts, skills, or configs."),
    "9router": ("lab-candidate", "Gateway can conflict with oMLX-first OPENAI_BASE_URL routing; clone only."),
    "ODS": ("lab-candidate", "Local AI platform stack overlaps Boneman_Projects runtime ownership; clone only."),
    "optimizerDuck": ("audit-only", "Windows-only optimization app; no macOS installation."),
    "open-knowledge": ("lab-candidate", "Knowledge editor/wiki candidate; no replacement of existing llm-wiki setup."),
    "colibri": ("lab-candidate", "Experimental large-model inference engine; requires benchmark before runtime wiring."),
    "code-review-graph": ("verified-candidate", "MCP/code graph candidate kept alongside active codebase-memory-mcp."),
}

repos = []
for path in sorted(p for p in source_root.iterdir() if (p / ".git").is_dir()):
    sha = subprocess.check_output(["git", "-C", str(path), "rev-parse", "--short", "HEAD"], text=True).strip()
    date = subprocess.check_output(["git", "-C", str(path), "log", "-1", "--format=%cs"], text=True).strip()
    remote = subprocess.check_output(["git", "-C", str(path), "remote", "get-url", "origin"], text=True).strip()
    status, rationale = decisions.get(path.name, ("review-required", "No decision recorded."))
    repos.append({
        "name": path.name,
        "remote": remote,
        "sha": sha,
        "commit_date": date,
        "status": status,
        "rationale": rationale,
    })

manifest = {
    "generated_at": subprocess.check_output(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], text=True).strip(),
    "audit_root": str(source_root.parent),
    "code_review_graph_status": crg_status_path.read_text().strip() if crg_status_path.exists() else "not checked",
    "local_ai_policy": {
        "default": "oMLX",
        "openai_base_url": "http://127.0.0.1:18080/v1",
        "gguf_coding_lane": "http://127.0.0.1:8002/v1",
        "rapid_mlx_lab_lane": "http://127.0.0.1:8010/v1",
        "ollama_default": False,
    },
    "repositories": repos,
}
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
PY
}

validate_manifest() {
  jq -e '
    (.repositories | length) == 8 and
    ([.repositories[] | select(.status == "installed") | .name] | index("Anthropic-Cybersecurity-Skills")) != null and
    ([.repositories[] | select(.name == "system_prompts_leaks" and .status == "audit-only")] | length) == 1 and
    .local_ai_policy.ollama_default == false
  ' "$MANIFEST" >/dev/null
}

run_validation() {
  cd "$REPO_ROOT"
  if command -v actionlint >/dev/null 2>&1; then
    actionlint .github/workflows/*.yml
  fi
  if command -v shellcheck >/dev/null 2>&1; then
    shellcheck install.sh wireless.sh scripts/**/*.sh
  fi
  if command -v markdownlint >/dev/null 2>&1; then
    markdownlint README.md docs/**/*.md
  fi
}

main() {
  local pass
  for pass in $(seq 1 "$MAX_PASSES"); do
    log "Pass $pass of $MAX_PASSES"
    require_tools
    clone_or_refresh_repos
    install_cybersecurity_skills
    verify_code_review_graph
    write_manifest
    validate_manifest
    run_validation
    log "Self-healing loop converged on pass $pass"
    return 0
  done

  printf 'Self-healing loop did not converge after %s passes\n' "$MAX_PASSES" >&2
  return 1
}

main "$@"
