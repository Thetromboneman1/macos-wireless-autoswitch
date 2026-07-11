# GitHub Actions Workflow Audit

Date: 2026-07-11

Scope: `.github/workflows/*.yml` in this repository.

| Workflow | Classification | Findings | Remediation |
|---|---|---|---|
| `fork-sync.yml` | privileged maintenance | Scheduled every 30 minutes and has `contents: write`; required for fork sync but powerful. Uses `actions/checkout@v4`. | Reduced to daily schedule, added concurrency, retained job timeout. |
| `release.yml` | fixed | Used deprecated `actions/create-release@v1` and `actions/upload-release-asset@v1`. | Replaced with `softprops/action-gh-release@v2`; added least privilege, timeout, and concurrency. |
| `validate.yml` | healthy | Uses `actions/checkout@v4`; no secrets. Missing explicit permissions. | Added `permissions: contents: read`, timeout, and concurrency. |
| `repository-validation.yml` | added | No workflow covered docs/scripts/tests/config/workflows together. | Added local-equivalent validation without local endpoint dependency. |
| `workflow-health-audit.yml` | added | Scheduled/manual workflow health audit was missing for workflow docs, prompts, and platform-modernization scripts. | Added weekly and manual audit with actionlint, yamllint, shellcheck, markdownlint, and gitleaks. |

## July 2026 Update

- Added `workflow-health-audit.yml` so GitHub Actions health can be checked independently of ordinary repository validation.
- Expanded `repository-validation.yml` path filters to cover GitHub prompt/chatmode assets and new self-healing prompt artifacts.
- Hardened JSON validation so missing optional config directories do not fail the job through unmatched shell globs.
- Added gitleaks coverage to repository validation and workflow health audit.

## Standard

- Prefer maintained actions on current Node runtimes.
- Use least-privilege `permissions`.
- Avoid `pull_request_target` unless a threat model exists.
- Keep shell steps under `set -euo pipefail` when they mutate state.
- Do not pass PATs when `github.token` is sufficient.
