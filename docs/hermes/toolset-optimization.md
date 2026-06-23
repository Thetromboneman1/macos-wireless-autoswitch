# Hermes Toolset Optimization

Date: 2026-06-23
Owner: Platform Operations

## Current Decision

For CLI sessions, Hermes now keeps core coding and local-ops toolsets enabled and disables high-cost or workflow-specific tools by default.

Enabled CLI toolsets after this pass:

```text
web, terminal, file, code_execution, skills, todo, memory, session_search, clarify, delegation
```

Disabled CLI toolsets after this pass:

```text
browser, vision, image_gen, tts, cronjob, messaging, computer_use
```

Evidence: `docs/autonomous-modernization/evidence/hermes-token-optimization/hermes-tools-list-after-trim.txt`.

## Profiles

| Profile | Toolsets |
|---|---|
| minimal | `terminal,file,skills,clarify` |
| coding | `terminal,file,code_execution,web,skills,memory,todo,clarify` |
| research | `web,file,skills,memory,session_search,clarify` |
| enterprise-agent | `terminal,file,web,skills,memory,todo,delegation,session_search,clarify` |
| browser-required | `web,browser,vision,file,skills,clarify` |
| administration | `terminal,file,web,skills,memory,todo,cronjob,messaging` |
| multimodal | `vision,image_gen,file,web,skills,clarify` |

Use per-invocation opt-in rather than restoring everything globally:

```bash
hermes -z "..." -t terminal,file,web,skills,memory,todo,clarify
hermes -z "..." -t web,browser,vision,file,skills,clarify
```

## Measurement Result

`hermes tools list --platform cli` shows the expected trim. However, `hermes prompt-size --json` reported the same fixed estimate before and after the trim:

| Run | Tool count | Estimated tool-schema tokens | Estimated total tokens |
|---|---:|---:|---:|
| Baseline | 29 | 11,694 | 20,130 |
| After trim | 29 | 11,694 | 20,130 |

Do not claim token savings until a request-level Hermes dump confirms fewer schemas are sent. The configuration change is still useful because it prevents accidental browser, vision, TTS, cron, messaging, and computer-use actions in ordinary CLI sessions.

## Rollback

```bash
hermes tools enable --platform cli browser vision image_gen tts cronjob messaging computer_use
```

The config backup path is recorded in `docs/autonomous-modernization/evidence/hermes-token-optimization/config-backup-dir.txt`.
