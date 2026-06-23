# GitHub Actions Workflow Audit

Date: 2026-06-23

Scope: `.github/workflows/*.yml` in this repository.

| Workflow | Classification | Findings | Remediation |
|---|---|---|---|
| `fork-sync.yml` | maintenance risk | Scheduled every 30 minutes and has `contents: write`; required for fork sync but powerful. Uses `actions/checkout@v4`. | Kept. Documented as privileged. Future improvement: concurrency guard and alerting. |
| `release.yml` | fixed | Used deprecated `actions/create-release@v1` and `actions/upload-release-asset@v1`. | Replaced with `softprops/action-gh-release@v2` and one upload step. Added top-level `contents: read` plus job-level release permissions. |
| `validate.yml` | healthy | Uses `actions/checkout@v4`; no secrets. Missing explicit permissions. | Added `permissions: contents: read`. |

## Standard

- Prefer maintained actions on current Node runtimes.
- Use least-privilege `permissions`.
- Avoid `pull_request_target` unless a threat model exists.
- Keep shell steps under `set -euo pipefail` when they mutate state.
- Do not pass PATs when `github.token` is sufficient.
