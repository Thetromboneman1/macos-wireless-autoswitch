# Benchmark Trend Analysis

Date: 2026-06-23
Owner: AI Platform

## Purpose

Benchmark governance compares two artifacts. Trend analysis compares historical artifacts to detect changes across time for TTFT, throughput, concurrency, swap pressure, and reliability.

## Script

```bash
scripts/operations/benchmark-trend-analysis.py \
  docs/autonomous-modernization/benchmark-results-omlx-extended.json \
  docs/benchmarks/post-cleanup-benchmark-results.json \
  --json /tmp/benchmark-trends.json
```

## Metrics

| Metric | Direction | Default Alert |
|---|---|---|
| `ttft_s` | lower is better | 35 percent degradation |
| `output_tok_s_wall` | higher is better | 20 percent degradation |
| `aggregate_output_tok_s_wall` | higher is better | 20 percent degradation |
| `swap_used_percent` | lower is better | 20 percent degradation |
| `reliability` | higher is better | 5 percent degradation |

## Current Historical Finding

The 2026-06-23 historical comparison between `docs/autonomous-modernization/benchmark-results-omlx-extended.json` and `docs/benchmarks/post-cleanup-benchmark-results.json` found one warning:

| Engine | Workload | Metric | Change |
|---|---|---|---|
| `omlx-mlx` | `coding_patch` | `ttft_s` | 45.68 percent degradation |

Other compared oMLX workloads either improved or stayed within threshold. Treat this as a watch item, not a production outage.

## Operating Rules

- Do not promote a model from one good point-in-time benchmark.
- Review at least two comparable artifacts for production promotion.
- If only one artifact exists, label the model experimental or candidate.
- Run trend analysis before changing default routing, startup policy, or lifecycle state.
