# Dependency Update Strategy

Date: 2026-06-23

## Policy

- Use explicit action versions in workflows.
- Prefer official GitHub actions for checkout and language setup.
- Third-party actions require a reason in the Actions audit and periodic review.
- Do not enable unattended auto-merge for CI, Docker, model, or security tooling updates.

## Current Decisions

| Dependency class | Cadence | Automation |
|---|---|---|
| GitHub Actions | Monthly review | Manual for now; Dependabot later if noise is acceptable. |
| Python test tools | On demand | Installed in CI from PyPI; no lockfile in this repo. |
| Shell and system tools | On demand | Installed from Ubuntu apt or Homebrew locally. |
| Local AI models | Manual | Never update from GitHub Actions. |

Rollback is `git revert` for workflow changes and rerun the previous green local validation command set.
