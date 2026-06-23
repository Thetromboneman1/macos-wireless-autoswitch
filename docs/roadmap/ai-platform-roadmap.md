# AI Platform Roadmap

Date: 2026-06-23
Owner: Platform Operations

## Prioritization

| Item | Class | Effort | Impact | Risk | Dependencies |
|---|---|---:|---:|---|---|
| Run monthly AIOps cycle and review report | Quick win | Low | High | Low | current scripts |
| Add local-link validation to documentation review | Quick win | Low | Medium | Low | documentation-review script |
| Add benchmark comparison thresholds to CI/manual task | Quick win | Low | High | Medium | benchmark artifacts |
| Create optional LaunchAgent for AIOps cycle | Medium-term | Medium | Medium | Medium | stable report retention policy |
| Add dependency age/staleness enrichment | Medium-term | Medium | Medium | Low | Homebrew/VS Code version feeds |
| Add model lifecycle dashboard artifact | Medium-term | Medium | High | Low | model lifecycle docs |
| Automate Boneman pointer audit | Strategic | High | High | Medium | 1Password CLI authorization |
| Add cross-repo operations report | Strategic | High | High | Medium | canonical Boneman architecture repo |

## Roadmap Rules

- Do not autostart lab lanes as part of roadmap experiments.
- Do not add secret-bearing external integrations without Boneman item pointers.
- Benchmark before changing production inference defaults.
- Keep small, reviewable commits.
