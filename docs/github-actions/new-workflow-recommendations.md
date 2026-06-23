# New Workflow Recommendations

Date: 2026-06-23

| Workflow | Decision | Reason |
|---|---|---|
| Repository Validation for this repo | Implemented | Matches local validation without requiring oMLX, model downloads, or secrets. |
| Gitleaks in every push | Recommended later | Local scan passes; remote workflow can be added after deciding whether to use the GitHub Action or a pinned binary install. |
| Dependabot for this repo | Deferred | Most dependencies are tools installed at runtime; avoid noisy PRs until workflow dependency policy is finalized. |
| Broken-link checker | Recommended later | Useful once historical/reference docs are excluded or clearly scoped. |
| Monthly audit issue | Deferred | Could create notification noise; use manual `workflow_dispatch` first. |
| Local AI endpoint CI | Rejected | GitHub-hosted runners cannot reach the Mac's oMLX endpoint. |
