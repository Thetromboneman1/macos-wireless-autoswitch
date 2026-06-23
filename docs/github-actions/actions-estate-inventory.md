# GitHub Actions Estate Inventory

Date: 2026-06-23

## Current Repository

| Workflow | File | Trigger | Permissions | Timeout | Latest known remote run | Status |
|---|---|---|---|---:|---|---|
| Validate Core Files | `.github/workflows/validate.yml` | push/PR on core files | `contents: read` | 10 min | run `18035242162`, success on 2025-09-26 | Modernized with concurrency and timeout. |
| Create Release | `.github/workflows/release.yml` | merged PR touching release inputs | top `contents: read`, job `contents: write` | 15 min | run `18035242331`, success on 2025-09-26 | Modernized with concurrency and timeout. |
| Sync Fork From Upstream | `.github/workflows/fork-sync.yml` | daily schedule, manual | `contents: write` | 10 min | no recent run returned by current query | Schedule reduced from every 30 minutes to daily. |
| Repository Validation | `.github/workflows/repository-validation.yml` | push/PR on docs/scripts/tests/config/workflows, manual | `contents: read` | 15 min | new workflow; no remote run before push | Added for maintained-docs, tests, config, and Actions validation. |

## Cross-Repository Presence

| Repository | Actions present | Notes |
|---|---|---|
| llama.cpp | yes | Upstream estate; local checkout is behind upstream. |
| Ansible | yes | `dependency-graph.yml`, `lint.yml`. |
| Boneman_Projects | no | Documentation repo with local edits; defer workflow addition until edits are reconciled. |
| Goose | no | Lightweight config repo; no action added. |
| Hermes workspace | yes | Sync workflows exist; repo is dirty and divergent. |
| OmniRoute | yes | Fork/reference checkout with CI, deploy, publish, and Dependabot. |
| hermes-agent | yes | Extensive upstream/fork CI and supply-chain workflows. |
| hermes-desktop | yes | Pages workflow only; divergent checkout. |
| hermes-webui | yes | Release, tests, upstream sync. |
| Openclaw | yes | Compose validation and auto-update; local compose edit preserved. |
| YTKillerPlus | no | Upstream app checkout; no local CI change. |
| odysseus-gemma-docker | yes | Validation workflow exists; local edits preserved. |
