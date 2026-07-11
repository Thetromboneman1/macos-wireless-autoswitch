#!/bin/bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BONEMAN_ROOT="${BONEMAN_ROOT:-/Users/corn/Documents/Boneman_Projects}"
REGISTRY="$BONEMAN_ROOT/config/local-ai-platform/lab-avenues.json"
SKILL_SOURCE="$BONEMAN_ROOT/docs/skills/lab-ai-avenues"
MAX_PASSES="${MAX_PASSES:-3}"

SKILL_ROOTS=(
  "$HOME/.codex/skills"
  "$HOME/.agents/skills"
  "$HOME/.claude/skills"
  "$HOME/.config/goose/skills"
  "$HOME/.hermes/skills"
)

log() {
  printf '[lab-avenues] %s\n' "$*"
}

require_files() {
  local missing=()
  [[ -f "$REGISTRY" ]] || missing+=("$REGISTRY")
  [[ -f "$SKILL_SOURCE/SKILL.md" ]] || missing+=("$SKILL_SOURCE/SKILL.md")

  if ((${#missing[@]} > 0)); then
    printf 'Missing required lab avenue files:\n' >&2
    printf '  %s\n' "${missing[@]}" >&2
    return 1
  fi
}

wire_skill_roots() {
  local root target linked_count
  linked_count=0

  for root in "${SKILL_ROOTS[@]}"; do
    [[ -d "$root" ]] || continue
    target="$root/lab-ai-avenues"
    if [[ -L "$target" ]]; then
      ln -sfn "$SKILL_SOURCE" "$target"
    elif [[ -e "$target" ]]; then
      log "Preserving existing non-symlink $target"
      continue
    else
      ln -s "$SKILL_SOURCE" "$target"
    fi
    linked_count=$((linked_count + 1))
  done

  log "Linked lab-ai-avenues skill into $linked_count tool roots"
}

validate_registry() {
  jq -e '
    .default_policy.production_default == "oMLX" and
    .default_policy.global_env_rewrite_allowed == false and
    ([.avenues[].id] | sort) == (["9router", "ODS", "colibri", "open-knowledge", "system_prompts_leaks"] | sort) and
    ([.avenues[] | select(.id == "system_prompts_leaks") | .allowed_actions[]] | index("metadata review")) != null and
    ([.avenues[] | select(.id == "system_prompts_leaks") | .prohibited_actions[]] | index("copy raw leaked prompts into agent instructions")) != null
  ' "$REGISTRY" >/dev/null
}

validate_links() {
  local root target saw_root
  saw_root=0
  for root in "${SKILL_ROOTS[@]}"; do
    [[ -d "$root" ]] || continue
    saw_root=1
    target="$root/lab-ai-avenues"
    [[ -L "$target" ]] || {
      printf 'Missing lab-ai-avenues symlink in %s\n' "$root" >&2
      return 1
    }
    [[ "$(readlink "$target")" == "$SKILL_SOURCE" ]] || {
      printf 'Unexpected symlink target for %s: %s\n' "$target" "$(readlink "$target")" >&2
      return 1
    }
  done
  [[ "$saw_root" -eq 1 ]]
}

validate_workflows() {
  cd "$REPO_ROOT"
  if grep -R "gitleaks/gitleaks-action@v2" .github/workflows; then
    printf 'Found stale gitleaks-action@v2 reference\n' >&2
    return 1
  fi
  if grep -R "actions/checkout@v5" .github/workflows; then
    printf 'Found stale checkout@v5 reference\n' >&2
    return 1
  fi
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
    require_files
    wire_skill_roots
    validate_registry
    validate_links
    validate_workflows
    run_validation
    log "Lab avenue wiring converged on pass $pass"
    return 0
  done

  printf 'Lab avenue wiring did not converge after %s passes\n' "$MAX_PASSES" >&2
  return 1
}

main "$@"
