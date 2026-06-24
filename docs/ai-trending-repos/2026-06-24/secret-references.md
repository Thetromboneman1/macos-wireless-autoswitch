# Secret References

Correct vault: `Boneman`.

No new secret values were required or created for this review.

## Future Secret References

| Tool | Secret Purpose | 1Password Item | Field | Safe Reference | Rotation Guidance | Consumer Path |
|---|---|---|---|---|---|---|
| SkillSpector | Optional LLM provider key for semantic scan | Not created | Not created | `op://Boneman/<item>/<field>` | Rotate according to provider policy before enabling LLM scan mode | Shell environment for one-shot scan only |
| Agent-Reach | Optional platform tokens/cookies | Not approved | Not approved | Do not store browser cookies without explicit approval | Revoke platform session if exposed | Agent-Reach local config only |
| PaddleOCR MCP | Optional AI Studio token | Not created | Not created | `op://Boneman/<item>/<field>` | Rotate after pilot or provider guidance | MCP environment variable only |
| AgentsView | Optional local bearer token | Not created | Not created | `op://Boneman/<item>/<field>` | Rotate if UI exposure changes | Local-only service config |
| Codebase Memory MCP | None expected for local mode | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |

## Rules

- Never commit secret values, token prefixes, cookies, private keys, raw credential files, or browser exports.
- Use placeholders or `op://Boneman/...` references only.
- If 1Password is locked during a future pilot, complete nonsecret work and mark secret-dependent validation blocked.
