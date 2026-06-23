# Model Governance Automation

Date: 2026-06-23
Owner: AI Platform

## Script

Promotion gate evaluator:

```bash
scripts/operations/model-governance/evaluate-promotion.py \
  --benchmark-json /tmp/benchmark-governance.json \
  --stability-json /tmp/stability.json \
  --health-json /tmp/local-ai-health.json \
  --tool-call-json /tmp/tool-call-validation.json \
  --documentation-json /tmp/documentation-review.json \
  --json /tmp/model-promotion-gates.json
```

## Gates

| Gate | Required Evidence |
|---|---|
| Benchmark | `ok: true` from benchmark governance |
| Stability | `ok: true` from soak or stability report |
| Health | `ok: true` from platform health |
| Swap | swap pressure below high and used percent within threshold |
| Tool calling | `ok: true` for agent/tool workloads |
| Documentation | `ok: true` from documentation review |

## Default Thresholds

- Maximum swap used for promotion: 80 percent.
- Production promotion should target below 75 percent swap used before test start.
- Any critical health failure blocks promotion.
- Any missing required evidence blocks promotion.

## Output Contract

The script emits:

- `ok`
- `summary.gate_count`
- `summary.failed_gate_count`
- `gates[]`
- `findings[]`

Use nonzero exit status as a hard stop for promotion.
