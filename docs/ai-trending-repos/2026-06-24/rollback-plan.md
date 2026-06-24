# Rollback Plan

## Current Review Package

This pass only added documentation and JSON inventories.

Rollback:

```bash
git rm -r docs/ai-trending-repos/2026-06-24
git rm docs/superpowers/plans/2026-06-24-ai-repository-review.md
git rm config/ai-trending-repos/upstream-versions-2026-06-24.json
git rm config/ai-trending-repos/validation-results-2026-06-24.json
git commit -m "revert: remove 2026-06-24 AI repository review"
```

## Future Pilots

| Tool | Rollback |
|---|---|
| SkillSpector | Remove pinned wrapper or tool config. Delete uv cache only if needed. |
| Agent-Reach | Use `agent-reach uninstall` only after reviewing what it will remove. Preserve tokens/cookies unless explicitly approved for deletion. |
| Addy Osmani skills | Remove only the selected imported skill directory. Keep scan report for audit. |
| Codebase Memory MCP | Run `codebase-memory-mcp uninstall`, remove MCP entries manually if needed, and delete only allowlisted cache under `~/.cache/codebase-memory-mcp/`. |
| AgentsView | Stop local service/container, remove local volume/database after confirming no needed audit data, remove any launch-at-login entry. |
| PaddleOCR | Remove isolated uv environment, model cache, and generated OCR outputs. Keep nonsensitive fixture docs if useful. |
| Headroom | Remove local proxy/MCP config and any cache/database files created by the pilot. Restore prior agent endpoint config. |
| Flue | Remove isolated TypeScript workspace and any sandbox runtime config. |
| OpenMontage | Remove isolated creative pilot workspace and generated media assets. |
| LMCache | No local rollback needed because it was not installed. |

Do not delete generated indexes, transcripts, model caches, or media outputs if they may contain sensitive work product until they have been reviewed.
