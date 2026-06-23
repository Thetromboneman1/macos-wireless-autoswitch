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

## Retention

- Keep dated benchmark summaries in `docs/benchmarks/`.
- Keep routine generated reports under `docs/operations/reports/` only when they add evidence for a decision.
- Use `/tmp` for disposable validation output.
