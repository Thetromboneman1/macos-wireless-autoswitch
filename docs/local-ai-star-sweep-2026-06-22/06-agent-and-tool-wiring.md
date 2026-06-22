# Loop 5 - Codex/OpenCode/IDE/Agent Wiring

## Evidence

- Global OpenCode config had `gguf-coding` registered but used `http://host.docker.internal:8002/v1`, which is Docker-facing rather than ideal for host OpenCode.
- OpenCode model listing includes `gguf-coding/gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf` and all four oMLX models.
- VS Code settings are mostly unrelated, with GitLens AI still using VS Code/Copilot models.
- Repo OpenCode configs in Hermes/Openclaw/hermes-webui already document oMLX providers; no direct edits were made there.

## Change

- Backed up `~/.config/opencode/opencode.json`.
- Changed global host OpenCode GGUF base URL to `http://127.0.0.1:8002/v1`.
- Left cloud providers and Copilot fallbacks intact.

## Validation

- `jq . ~/.config/opencode/opencode.json` succeeded.
- `opencode models` still lists the GGUF coding model and oMLX models.

## Rollback

```bash
cp ~/.config/opencode/opencode.json.bak-local-ai-star-sweep-2026-06-22 ~/.config/opencode/opencode.json
```

