# Post-Skills Cleanup and Drift Reconciliation

Date: 2026-06-23

## Baseline

Previous completed commit:

```text
e08f889117eb61e5f95911361b43bb1ec7809d22 Add Codex and VS Code skills integration
```

This pass reviewed the remaining dirty working tree, completed the valid platform drift, LaunchAgent, and health-monitoring work, and validated Codex/VS Code skill activation state.

## Dirty File Classification

| Path | Classification | Action |
|---|---|---|
| `docs/architecture/local-ai-startup-architecture.md` | LaunchAgent documentation | Kept and linked to V2 startup policy. |
| `docs/architecture/ai-service-catalog.md` | Platform drift documentation | Added as current service inventory. |
| `docs/architecture/startup-orchestration-v2.md` | LaunchAgent/platform documentation | Added as current startup policy. |
| `docs/autonomous-modernization/26-post-skills-cleanup-and-drift-reconciliation.md` | Final report | Added in this pass. |
| `docs/benchmarks/post-cleanup-benchmark-results.json` | Generated benchmark artifact | Kept as evidence for post-cleanup oMLX validation. |
| `docs/benchmarks/post-cleanup-validation.md` | Generated benchmark documentation | Kept and tied to benchmark artifact. |
| `docs/benchmarks/stability-phase2-sample.json` | Generated health sample | Kept as short low-impact stability evidence. |
| `docs/benchmarks/stability-phase2-hour-samples.jsonl` | Generated partial soak artifact | Kept as partial sample evidence; not treated as a completed one-hour soak. |
| `docs/benchmarks/stability-validation-phase2.md` | Stability documentation | Updated to describe the current partial sample honestly. |
| `docs/governance/documentation-governance.md` | Documentation governance | Kept as current-doc routing policy. |
| `docs/macos/launchagent-inventory.md` | LaunchAgent documentation | Kept and reconciled with archived `com.corn.vllm-mlx`. |
| `docs/macos/launchagent-legacy-cleanup.md` | LaunchAgent documentation | Kept as archive/rollback record. |
| `docs/operations/automation-monitoring.md` | Health monitoring documentation | Kept and updated for `--skip-chat` and drift detection. |
| `docs/operations/platform-drift-detection.md` | Platform drift documentation | Expanded to enterprise standard. |
| `docs/operations/platform-maintenance-v2.md` | Platform drift documentation | Kept as maintenance cadence. |
| `docs/operations/swap-pressure-analysis.md` | Health monitoring documentation | Kept and linked to phase-two remediation. |
| `docs/operations/swap-pressure-remediation-phase2.md` | Health monitoring documentation | Kept as memory-pressure decision record. |
| `docs/security/launchagent-security-audit.md` | LaunchAgent/security documentation | Kept and marked legacy LaunchAgent finding resolved. |
| `docs/skills/codex-skill-activation.md` | Codex skills validation | Added in this pass. |
| `docs/skills/vscode-extension-validation.md` | VS Code validation | Added in this pass. |
| `scripts/health/local-ai-health.py` | Health monitoring | Reconciled and extended. |
| `scripts/health/drift-detection/baseline.json` | Platform drift detection | Kept as drift baseline. |
| `scripts/health/drift-detection/check-platform-drift.py` | Platform drift detection | Kept as drift detector. |
| `tests/test_local_ai_scripts.py` | Health monitoring tests | Extended for `--skip-chat`, optional lanes, Codex skills, and VS Code recommendations. |
| `tests/test_platform_drift_detection.py` | Platform drift tests | Kept as detector coverage. |

No unrelated user work remained outside the approved cleanup scope after classification.

## Actions Taken

- Completed Codex skill activation validation documentation.
- Completed VS Code extension validation documentation.
- Expanded platform drift documentation for LaunchAgents, GitHub Actions, AI endpoints, model lanes, Codex skills, VS Code recommendations, and Boneman references.
- Reconciled `scripts/health/local-ai-health.py` so it now reports:
  - oMLX production health;
  - manual llama.cpp lane health when port `8002` is listening;
  - manual Rapid-MLX lane health when port `8010` is listening;
  - swap and memory pressure;
  - port listeners;
  - key processes;
  - LaunchAgent health and missing program paths;
  - Codex skill directory and metadata health;
  - VS Code extension recommendation health.
- Preserved the oMLX-first architecture and kept llama.cpp/Rapid-MLX manual.
- Did not reinstall already installed skills or extensions.

## Codex Skill Activation Status

Expected skills exist under `~/.codex/skills` and pass metadata validation through `scripts/health/local-ai-health.py`.

Manual note: restart Codex if an already-open Codex UI/session does not display newly installed skills.

## VS Code Validation Status

The VS Code app CLI reports the expected extensions installed:

- `charliermarsh.ruff@2026.54.0`
- `davidanson.vscode-markdownlint@0.61.2`
- `hashicorp.terraform@2.39.3`
- `ms-kubernetes-tools.vscode-kubernetes-tools@1.4.0`
- `ms-vscode.powershell@2025.4.0`
- `tamasfe.even-better-toml@0.21.2`

Workspace JSON files validate with `jq`.

## LaunchAgent Legacy Decision

`com.corn.vllm-mlx` is archived, not deleted.

Reasoning:

- it was disabled;
- it pointed at a missing legacy path;
- oMLX is the approved production lane;
- llama.cpp and Rapid-MLX are manual lanes;
- archive gives a rollback path without leaving a broken active plist.

Archive path:

```text
~/Library/LaunchAgents/Archive/com.corn.vllm-mlx.plist.20260623-082607.archived
```

## Health Script Reconciliation

The health script now distinguishes:

- required production lane failure;
- optional manual lane stopped state;
- optional manual lane running but unhealthy state.

It also surfaces Codex skill and VS Code recommendation drift in the same JSON snapshot used by drift detection.

## Validation Results

Validation run for this pass:

```text
uvx pytest
shellcheck install.sh wireless.sh scripts/**/*.sh
markdownlint targeted docs
jq JSON validation
taplo TOML validation
yamllint .github/workflows/*.yml
actionlint
plutil -lint LaunchAgent plists
gitleaks detect --no-banner --redact --source .
gitleaks protect --staged --no-banner --redact
git diff --check
scripts/health/local-ai-health.py --skip-chat
oMLX /health and authenticated /v1/models
```

## Commit and Push Status

Cleanup implementation commit:

```text
300f25c Harden skill activation and platform drift documentation
```

Push target:

```text
origin/main
```

Push result: succeeded.

## Remaining Manual Actions

- Restart Codex manually if old sessions do not show newly installed skills.
- Treat `docs/benchmarks/stability-phase2-hour-samples.jsonl` as partial soak evidence unless a future run completes the intended hour window.
- Re-run a dedicated llama.cpp/Rapid-MLX benchmark window before changing their manual-lane status.
