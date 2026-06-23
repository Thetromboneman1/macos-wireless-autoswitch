# GitHub Actions Operations Runbook

Date: 2026-06-23

## Review

```bash
gh run list --limit 20
gh run view <run-id> --log-failed
find .github/workflows -maxdepth 1 -type f -name '*.yml' -print0 | xargs -0 actionlint
yamllint .github/workflows/*.yml .yamllint
```

## Failure Triage

1. Check whether the failure is workflow syntax, dependency install, test failure, or permission related.
2. Reproduce locally when possible with `uvx pytest`, `shellcheck`, `markdownlint`, `jq`, `yamllint`, and `actionlint`.
3. Fix the root cause before rerunning the workflow.
4. If a secret is missing, document the GitHub secret name, purpose, scope, and matching 1Password `Boneman` item. Do not print the value.

## Remote Verification After Push

```bash
gh run list --branch main --limit 10
gh run watch <run-id>
```

Record run URLs in the final report or dated evidence docs when workflow changes are material.
