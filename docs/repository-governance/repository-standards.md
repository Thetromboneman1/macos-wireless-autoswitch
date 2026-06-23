# Repository Standards

Date: 2026-06-23

## Baseline

| Standard | Active repos | Fork/reference repos | Notes |
|---|---|---|---|
| README | Required | Recommended | Should identify runtime boundaries and validation commands. |
| AGENTS.md | Recommended | Optional | Required when local AI, secrets, or non-obvious validation rules apply. |
| `.gitignore` | Required | Required | Must exclude caches, secrets, local runtime state, and generated reports. |
| Markdownlint config | Required for docs-heavy repos | Optional | Use explicit exclusions for historical or third-party docs. |
| GitHub Actions validation | Recommended | Not applicable unless maintained | Must avoid local-only endpoints. |
| Secret documentation | Required when secrets exist | Optional | Use 1Password `Boneman` item names only. |
| Security policy | Recommended | Optional | At minimum, document secret and Actions handling. |
| Tests | Required for executable automation | Optional | Fixture-based tests preferred for local AI checks. |

## Non-Goals

- Do not force CI into archived or upstream mirror checkouts.
- Do not add secrets or model downloads to GitHub-hosted CI.
- Do not rewrite third-party reference snapshots for local style.
