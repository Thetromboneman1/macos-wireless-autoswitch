# Restore Testing

Date: 2026-06-23
Owner: SRE

## Non-Destructive Validation

This pass performed non-destructive restore validation from the live checkout and documented recovery sources. No production service was stopped.

## Checks

| Area | Validation | Result |
|---|---|---|
| Repository restoration | `origin/main` is the recovery source and repo status is checked before/after commits | validated by sync checks |
| Documentation restoration | all current docs are Git-tracked Markdown except ignored generated reports | validated by docs index and Git status |
| Configuration restoration | oMLX, LaunchAgent, Codex, VS Code, and Docker paths are documented as pointers | validated through docs review |
| Health restoration | endpoint-only health validates oMLX and lane state | validated in this phase |
| Drift restoration | drift detector validates ports, LaunchAgents, configs, and workflow baseline | validated in this phase |

## Restore Test Commands

```bash
git status --short --branch
scripts/health/local-ai-health.py --skip-chat --json /tmp/local-ai-health-restore.json
scripts/health/drift-detection/check-platform-drift.py --health-json /tmp/local-ai-health-restore.json --json /tmp/platform-drift-restore.json
scripts/operations/documentation-review.py docs/operations docs/governance docs/architecture docs/macos docs/security docs/skills docs/executive docs/roadmap docs/capacity docs/disaster-recovery --json /tmp/documentation-restore.json
```

## Findings

- Repository and documentation restore are low risk when changes are pushed.
- Runtime secret restore depends on Boneman and local secure stores.
- Full model-cache restore is not proven by this repo; promotion and DR plans should assume re-download or local cache recovery may take a maintenance window.
- Generated AIOps reports are disposable unless explicitly retained as decision evidence.
