# Stability Validation Phase 2

Date: 2026-06-23

## Short Sample

Artifact:

```text
docs/benchmarks/stability-phase2-sample.json
```

The short low-impact sample ran four endpoint-only health checks over about one minute:

| Signal | Result |
|---|---|
| Samples | 4 |
| oMLX endpoint | healthy |
| Active AI listeners | `18080` only |
| Broken LaunchAgents | none |
| Swap delta | 0.0 percentage points |
| Chat probe | skipped to avoid reloading large models |

## One-Hour Soak

Artifacts:

```text
docs/benchmarks/stability-phase2-hour-samples.jsonl
docs/benchmarks/stability-phase2-hour-summary.json
```

The one-hour soak sampled endpoint health every five minutes with `--skip-chat`.

| Signal | Result |
|---|---|
| Start | 2026-06-23T13:30:51Z |
| End | 2026-06-23T14:31:03Z |
| Samples | 13 |
| All health checks OK | true |
| Expected AI ports only | true |
| Broken LaunchAgents | false |
| Swap used delta | -448.06 MB |
| Swap total delta | -1024 MB |
| Swap used percent delta | +5.1 points |

The percent rose because macOS reduced the allocated swap total from 8192 MB to 7168 MB during the soak. Absolute used swap decreased.

## Interpretation

Use full chat validation when proving generation works. Use endpoint-only stability checks when the goal is long-duration idle stability and memory conservation.
