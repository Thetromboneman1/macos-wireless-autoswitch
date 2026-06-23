# GitHub Actions Security Audit

Date: 2026-06-23

## Findings

| Area | Risk | Status |
|---|---|---|
| Deprecated release actions | Medium | Fixed by replacing Node-era release/upload actions. |
| Default token permissions | Medium | Reduced `validate.yml` to `contents: read`; release retains job-level `contents: write`. |
| Fork sync token | Medium | Uses `GITHUB_TOKEN` for write to fork; required for sync. |
| Third-party actions | Medium | `softprops/action-gh-release@v2` introduced for maintained release support. Review on version bumps. |
| Secrets | Low | No repository secrets are referenced by current workflows. |
| Docker actions | Low | No Docker actions in this repository. |
| Artifacts | Low | Release assets are generated and uploaded in `release.yml`; no Actions artifact storage used. |

## Rules

- Keep `contents: write` limited to release and fork-sync jobs.
- Do not introduce repository PATs unless `GITHUB_TOKEN` cannot perform the task.
- Pin third-party actions to major versions at minimum; consider SHA pinning for high-risk repos.
- Run `actionlint` after workflow edits.
