# GitHub Actions Secrets

Date: 2026-06-23

## Current State

This repository does not require custom GitHub Actions secrets for normal validation, fork sync, or release creation.

| Secret | Required | Notes |
|---|---:|---|
| `GITHUB_TOKEN` | yes | Provided by GitHub Actions. Used by release and fork-sync. |
| PAT | no | Do not add unless a future workflow needs cross-repository access. |
| oMLX/Hermes keys | no | Local-only; never put local runtime keys into GitHub Actions. |

## Boneman Policy

If a future workflow needs a secret:

1. Store the source value in Boneman.
2. Create or rotate the GitHub secret from Boneman manually or through an approved one-time script.
3. Document only the secret name, owner, rotation cadence, and retrieval path.
4. Do not commit secret values, token prefixes, or exported `.env` files.
