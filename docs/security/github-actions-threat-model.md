# GitHub Actions Threat Model

Date: 2026-06-23

## Assets

- Repository contents and release artifacts.
- `GITHUB_TOKEN` permissions.
- Local AI documentation that references, but does not contain, secrets.
- 1Password `Boneman` item names and retrieval guidance.

## Trust Boundaries

- Pull request code is untrusted.
- GitHub-hosted runners cannot access local oMLX endpoints.
- Docker consumer URLs and host loopback URLs are documentation/config boundaries, not CI service dependencies.

## Threats And Controls

| Threat | Control |
|---|---|
| Overbroad token permissions | Top-level `contents: read`; write permission only in release and fork-sync jobs that need it. |
| Workflow spam or race conditions | Concurrency groups and reduced fork-sync schedule. |
| Secret exposure | No secret values in docs or workflows; use GitHub Secrets/Environments and 1Password `Boneman` pointers. |
| Third-party action drift | Versioned actions and documented review cadence. |
| Local endpoint assumptions | CI validates fixtures/docs/scripts only; live oMLX validation remains local. |
