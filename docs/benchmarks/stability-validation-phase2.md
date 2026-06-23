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

## Partial Soak

Artifacts:

```text
docs/benchmarks/stability-phase2-hour-samples.jsonl
```

The current soak artifact contains three five-minute samples. Treat it as partial evidence, not a completed one-hour soak. A future full soak should sample endpoint health every five minutes with `--skip-chat`, then write a summary that validates service stability, expected ports, LaunchAgent health, and swap trend without warming the large model.

## Interpretation

Use full chat validation when proving generation works. Use endpoint-only stability checks when the goal is long-duration idle stability and memory conservation.
