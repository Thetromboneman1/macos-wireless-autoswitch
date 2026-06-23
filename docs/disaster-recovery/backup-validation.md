# Backup Validation

Date: 2026-06-23
Owner: Platform Operations

## Inventory

| Asset | Backup Source | Current Risk |
|---|---|---|
| Repository | GitHub `origin/main` | Low if pushed after each phase |
| Documentation | Git-tracked Markdown | Low; generated report JSON intentionally ignored |
| Health and drift baseline | Git-tracked scripts and baseline JSON | Low |
| LaunchAgents | User LaunchAgent files plus docs inventory | Medium; local plist state can drift outside Git |
| oMLX settings | local config and Boneman pointer policy | Medium; secret values are intentionally not in Git |
| Model caches | local model caches and upstream sources | Medium; large files are not repo-managed |
| Codex config and skills | local Codex home and skill docs | Medium; host-local state must be revalidated |
| VS Code config/extensions | local Code user data and extension store | Medium; 2.0 GB extension footprint is not repo-backed |
| Docker consumers | compose repos and local Docker state | Medium; running container state is not a backup |
| Boneman vault | 1Password | High dependency if vault access is unavailable |

## Validation Procedure

1. Confirm `git status --short --branch` is clean and synced after each phase.
2. Confirm generated reports remain ignored unless intentionally promoted as evidence.
3. Confirm `gitleaks detect --no-banner --redact --source .` is clean.
4. Confirm `docs/security/onepassword-secrets.md` and `docs/security/secret-inventory.md` point to secret locations without values.
5. Confirm LaunchAgent inventory matches `~/Library/LaunchAgents`.
6. Confirm oMLX endpoint can be rebuilt from documented app/config pointers and Boneman secret pointers.

## Not Backed Up By This Repo

- Raw oMLX API key.
- Raw Goose/Hermes secret files.
- Full model cache contents.
- Docker volumes and container runtime state.
- VS Code extension binaries and user data.

Document pointers and recovery workflows here; keep sensitive or heavy runtime state outside Git.
