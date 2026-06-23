# Dependency Governance

Date: 2026-06-23
Owner: Platform Operations

## Scope

Dependency governance covers Python packages, Homebrew packages, VS Code extensions, Codex skills, MCP tools, GitHub Actions, and Docker images.

## Automated Report

```bash
scripts/operations/dependency-report.py --json /tmp/dependency-report.json
```

The report inventories:

- Python manifest files;
- Homebrew leaves;
- VS Code extensions;
- Codex skills;
- GitHub Actions and pinned versions;
- Docker images from compose files;
- MCP topology files.

## Cadence

| Dependency class | Review cadence | Validation |
|---|---|---|
| Python tooling | Monthly | `uvx pytest` |
| Homebrew tools | Monthly | version capture plus relevant CLI smoke |
| VS Code extensions | Monthly | `code --list-extensions --show-versions` |
| Codex skills | Monthly | health script metadata check |
| MCP tools | Quarterly | topology review and transport smoke |
| GitHub Actions | Monthly | `actionlint`, drift baseline |
| Docker images | Quarterly | compose config and image inspection |

## Rollback Requirements

- Keep previous benchmark and health artifacts before changing AI dependencies.
- Do not update multiple model engines in the same maintenance commit.
- For VS Code or Codex tooling, document exact versions/skills changed.
- For secrets-bearing integrations, update Boneman pointers without committing values.
