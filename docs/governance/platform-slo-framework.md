# Platform SLO Framework

Date: 2026-06-23
Owner: SRE

## Scope

These SLOs apply to the local AI platform on this Mac. They are operating objectives, not contractual external SLAs.

## Objectives

| Area | SLO | Measurement |
|---|---|---|
| oMLX availability | Production endpoint healthy during active work windows | `scripts/health/local-ai-health.py --skip-chat` |
| Model registry | Four Gemma role models visible | authenticated `/v1/models` |
| Specialist lane control | `8002` and `8010` state matches current operating policy | drift detection |
| Health checks | Routine endpoint health completes without failures | health JSON `ok: true` |
| Drift | zero critical drift findings | drift JSON `ok: true` |
| Benchmark regression | no unreviewed TTFT or throughput warning above threshold | benchmark governance and trend analysis |
| Swap | below high pressure before promotion and long benchmarks | health JSON swap section |
| Documentation review | zero warning findings for current docs | documentation review |
| Secret handling | zero committed secret findings | gitleaks |

## SLA Language

For personal local operations, use internal service expectations:

- Restore production oMLX within one active work session after detection.
- Restore documentation and repo state from Git immediately after local file loss.
- Restore sensitive config from Boneman pointers or local source paths without copying raw secrets into Git.

## Reporting

Report monthly through:

```bash
scripts/operations/run-aiops-cycle.sh
```

Promotion and incident reviews should attach:

- health report;
- drift report;
- benchmark governance report;
- trend report when historical artifacts exist;
- documentation review;
- model promotion gate report.
