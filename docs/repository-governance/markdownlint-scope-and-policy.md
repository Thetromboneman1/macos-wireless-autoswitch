# Markdownlint Scope And Policy

Date: 2026-06-23

## Canonical Tooling

Local and CI markdown validation use `markdownlint` with `.markdownlint.json` and `.markdownlintignore`.

```bash
markdownlint README.md docs/**/*.md
```

## Maintained Scope

Maintained documentation includes `README.md` and current docs under `docs/architecture`, `docs/benchmarks`, `docs/capacity`, `docs/disaster-recovery`, `docs/github-actions`, `docs/governance`, `docs/hermes`, `docs/macos`, `docs/network`, `docs/operations`, `docs/repository-governance`, `docs/security`, and `docs/skills`.

## Exclusions

| Path | Reason |
|---|---|
| `docs/autonomous-modernization/**` | Dated implementation evidence; preserve historical meaning. |
| `docs/local-ai-star-sweep-2026-06-22/**` | Dated sweep notes with captured external snippets and run output. |
| `docs/reference/**` | Downloaded third-party README snapshots; do not rewrite for local style. |
| `docs/IMPLEMENTATION_PLAN.md` | Legacy third-party implementation plan retained as history. |

No meaningful lint rule is globally disabled except line length and MD060, matching existing local style.
