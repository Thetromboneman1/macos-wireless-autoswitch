# Codex Skill Activation Validation

Date: 2026-06-23

## Scope

Validate that the Codex skills installed in commit `e08f889117eb61e5f95911361b43bb1ec7809d22` are present and have usable front matter.

Expected skills:

- `gh-address-comments`
- `gh-fix-ci`
- `migrate-to-codex`
- `openai-docs`
- `playwright`
- `playwright-interactive`
- `security-best-practices`
- `security-ownership-map`
- `security-threat-model`
- `yeet`

## Validation Method

Commands:

```bash
find ~/.codex/skills -maxdepth 2 -type f -name SKILL.md | sort
scripts/health/local-ai-health.py --skip-chat --json /tmp/local-ai-health.json
jq '.codex_skills' /tmp/local-ai-health.json
```

The health script checks:

- each expected skill directory exists;
- each `SKILL.md` exists;
- front matter contains `name` matching the directory;
- front matter contains `description`.

## Result

All expected skill files are present on disk and pass metadata validation.

## Activation Notes

Codex skill discovery happens at session startup. The current session can read and use the installed skills from disk, but a manual Codex app/session restart is the safest way to refresh the UI-discovered skill list everywhere.

Safe activation action:

```text
Restart Codex after this pass if the newly installed skills do not appear in an existing session.
```

No destructive Codex reload command was run.
