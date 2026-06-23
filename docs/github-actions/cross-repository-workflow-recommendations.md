# Cross-Repository Workflow Recommendations

Date: 2026-06-23

## Recommended Next Changes

1. Add `workflow_dispatch` to validation workflows that are safe to run
   manually and have no publish, branch rewrite, PR creation, or notification
   side effects.
2. Add lightweight `push` validation to `Hermes` for docs, compose, JSON, and
   workflow syntax. Keep the weekly build/publish workflow separate.
3. Add a validation workflow to `Boneman_Projects` for local-AI docs and secret
   scanning after historical support archives are remediated or excluded with a
   documented baseline.
4. Introduce a shared workflow style config so `yamllint` rules match how
   GitHub workflow YAML is actually maintained.
5. Review third-party actions independently before major bumps or SHA rewrites.

## Repository-Specific Notes

| Repository | Recommendation |
| --- | --- |
| `Boneman_Projects` | Clean or quarantine historical UniFi support exports before enabling required gitleaks. |
| `Hermes` | Split validation from weekly publish/sync jobs so push checks are safe and quick. |
| `Hermes/hermes-webui` | Add a safe branch validation workflow for `local-llm-docs`. |
| `Openclaw` | Keep compose validation on push; run image auto-bump by schedule or explicit maintenance window. |
| `odysseus-gemma-docker` | Current validation is sufficient for the Docker/Gemma contract. |
| `Ansible` | Current lint and dependency graph workflows are sufficient after Node runtime migration. |

## Safety Boundary

Do not automatically fast-forward or rebase clean but divergent upstream
checkouts (`llama.cpp`, `hermes-agent`, `hermes-desktop`, `YTKillerPlus`)
without a repo-specific migration plan.
