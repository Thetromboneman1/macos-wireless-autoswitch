# Platform Reporting

Date: 2026-06-23
Owner: Platform Operations

## Purpose

Platform reporting converts health, drift, dependency, benchmark, documentation, LaunchAgent, and GitHub Actions signals into reviewable artifacts.

## Automated Report

Run the AIOps cycle:

```bash
scripts/operations/run-aiops-cycle.sh
```

Core report generator:

```bash
scripts/operations/generate-platform-report.py \
  --health-json /tmp/local-ai-health.json \
  --drift-json /tmp/platform-drift.json \
  --dependency-json /tmp/dependency-report.json \
  --documentation-json /tmp/documentation-review.json \
  --hermes-cost-json /tmp/hermes-cost.json \
  --json /tmp/platform-report.json
```

## Report Sections

| Section | Source |
|---|---|
| Platform health | `scripts/health/local-ai-health.py` |
| Benchmark status | `scripts/operations/benchmark-governance.py` |
| Model inventory | `docs/operations/model-lifecycle-management.md` |
| Drift findings | `scripts/health/drift-detection/check-platform-drift.py` |
| Dependency status | `scripts/operations/dependency-report.py` |
| LaunchAgent health | health script launchagent section |
| GitHub Actions health | `actionlint`, drift baseline, dependency report |
| Hermes token and cost status | `scripts/operations/hermes-cost-report.py` |

## Hermes Cost Report

The AIOps cycle captures `hermes prompt-size --json`, writes `hermes-cost-<timestamp>.json`, and folds the result into the platform report under `sections.hermes_cost`.

The report is count-only. It must not include prompt text, secret values, token prefixes, cookies, private keys, or raw credential files.

## Retention

- Keep dated benchmark summaries in `docs/benchmarks/`.
- Keep routine generated reports under `docs/operations/reports/` only when they add evidence for a decision.
- Use `/tmp` for disposable validation output.
