# Repository Health Audit

Date: 2026-06-23

## Summary

| Class | Repositories |
|---|---|
| Healthy | Ansible, Goose, OmniRoute, hermes-webui |
| Healthy with minor cleanup | macos-wireless-autoswitch |
| Requires manual reconciliation | Hermes workspace, hermes-desktop |
| Preserve local edits | Boneman_Projects, Openclaw, odysseus-gemma-docker |
| Upstream update candidate | llama.cpp, hermes-agent, YTKillerPlus |

## Findings

- `macos-wireless-autoswitch` had a tracked `.DS_Store`; it was removed and remains covered by `.gitignore`.
- `docs/operations/reports/` contains ignored generated AIOps JSON. The directory keeps only its `.gitignore` under version control.
- Python caches, `.pytest_cache`, local backups, and Odysseus runtime state are ignored and not committed.
- `Boneman_Projects`, `Hermes`, `Openclaw`, and `odysseus-gemma-docker` contain pre-existing local edits. They were preserved.
- `llama.cpp`, `hermes-agent`, `hermes-desktop`, and `YTKillerPlus` are behind upstream or divergent. Updating them may affect local benchmark or reference behavior and should be handled separately.

## Validation

This pass validated the active governance repo with shell, workflow, config, markdown, tests, and secret scanning. Other repositories were inventoried and classified but not modified.
