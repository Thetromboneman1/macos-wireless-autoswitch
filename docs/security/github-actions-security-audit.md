# GitHub Actions Security Audit

Date: 2026-06-23

## Findings

| Area | Risk | Status |
|---|---|---|
| Deprecated release actions | Medium | Fixed by replacing Node-era release/upload actions. |
| Default token permissions | Medium | Reduced `validate.yml` to `contents: read`; release retains job-level `contents: write`. |
| Fork sync token | Medium | Uses `GITHUB_TOKEN` for write to fork; required for sync. |
| Scheduled workflow noise | Medium | Reduced fork sync from every 30 minutes to daily and added concurrency. |
| Third-party actions | Medium | `softprops/action-gh-release@v2` and `rhysd/actionlint@v1.7.12` are versioned and documented for review. |
| Secrets | Low | No repository secrets are referenced by current workflows. |
| Docker actions | Low | No Docker actions in this repository. |
| Artifacts | Low | Release assets are generated and uploaded in `release.yml`; no Actions artifact storage used. |
| Local endpoint assumptions | Low | New repository validation workflow avoids oMLX or model endpoint dependencies. |

## Rules

- Keep `contents: write` limited to release and fork-sync jobs.
- Do not introduce repository PATs unless `GITHUB_TOKEN` cannot perform the task.
- Pin third-party actions to major versions at minimum; consider SHA pinning for high-risk repos.
- Run `actionlint` after workflow edits.
- Keep live local AI checks local; use fixture-based tests in GitHub-hosted CI.
