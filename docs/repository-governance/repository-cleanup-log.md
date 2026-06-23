# Repository Cleanup Log

Date: 2026-06-23

## Decisions

| Artifact | Classification | Action | Evidence |
|---|---|---|---|
| `/.DS_Store` | macOS generated metadata | Removed from version control | `.gitignore` already ignores `.DS_Store`. |
| `docs/.DS_Store` | macOS generated metadata | Left untracked and ignored | Not committed. |
| `.pytest_cache/` | generated test cache | Left ignored | Not required for recovery. |
| `scripts/**/__pycache__/`, `tests/**/__pycache__/` | generated Python caches | Left ignored | Rebuilt by tests. |
| `backups/hermes-cost-token-optimization-20260623T155950Z/` | local rollback backup | Left ignored | Only local recovery copy; not committed. |
| `docs/operations/reports/*.json` | generated AIOps reports | Left ignored | `docs/operations/reports/.gitignore` is tracked. |
| `odysseus/data/`, `odysseus/.env` | local runtime and secrets-adjacent state | Left ignored | Must not be committed. |

No model files were deleted.
