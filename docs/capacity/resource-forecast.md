# Resource Forecast

Date: 2026-06-23
Owner: Platform Operations

## Basis

This forecast uses the live 2026-06-23 capacity snapshot plus the existing operational model: one oMLX production lane, manual lab lanes, generated reports ignored by Git, and benchmark artifacts retained only when they support decisions.

## Forecast

| Horizon | Memory | Storage | Models | Benchmarks | Documentation | Dependencies |
|---|---|---|---|---|---|---|
| 3 months | Stable if one production lane remains active and lab lanes are scheduled | Low growth; docs and JSON reports remain small | No new always-on model servers | Monthly production artifacts plus occasional lab artifacts | 10-25 additional docs or updates | Extension/Homebrew drift expected but manageable |
| 6 months | Swap pressure remains the main recurring constraint | VS Code/user data likely dominates local growth | One or two candidates may require controlled trials | Trend set becomes useful for seasonality and regression detection | Governance docs need quarterly review | Review action versions, Codex skills, Docker images |
| 12 months | 64 GB remains enough for disciplined single-user operation; weak if multiple large lanes become always-on | Model caches and editor data can become material | Retire unused lab models or move them to archived cache | Benchmark history should be summarized, not hoarded | Docs need ownership enforcement to avoid stale sprawl | Dependency report should be part of monthly AIOps review |

## Storage Growth Controls

- Keep generated `docs/operations/reports/*.json` ignored unless a specific report is evidence for a decision.
- Keep benchmark artifacts under `docs/benchmarks/` only when they provide baseline, trend, promotion, or incident evidence.
- Archive model candidates that are not benchmarked within two quarterly cycles.
- Keep local backups outside Git and document pointers rather than copying secrets or runtime config values.

## Memory Forecast

The practical memory budget is governed by concurrency, not raw model count. The platform can carry the four Gemma role models as registered/selectable oMLX models, but should not keep all large roles resident through manual pinning. If Docker, LM Studio, VS Code, and multiple model lanes run together, swap will remain high and promotion windows should be blocked.

## Forecast Triggers

Reforecast when any of these happen:

- a new always-on model service is proposed;
- Docker memory limits or container count materially increase;
- swap remains above 80 percent after closing known background contributors;
- benchmark artifacts exceed the point where trend summaries are easier to review than raw files;
- VS Code or Codex integration adds persistent background services.
