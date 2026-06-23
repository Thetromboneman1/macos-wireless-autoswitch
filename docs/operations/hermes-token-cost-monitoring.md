# Hermes Token Cost Monitoring

Date: 2026-06-23
Owner: Platform Operations

## Added Tooling

`scripts/operations/hermes-cost-report.py` builds a secret-safe token/cost observability report from:

- `hermes prompt-size --json`;
- Hermes/session JSON or JSONL usage records;
- local AI health JSON.

The AIOps cycle now emits:

- `hermes-prompt-size-<timestamp>.json`;
- `hermes-cost-<timestamp>.json`;
- platform report with a `hermes_cost` section.

## Usage

```bash
scripts/operations/hermes-cost-report.py \
  --prompt-size-json docs/autonomous-modernization/evidence/hermes-token-optimization/prompt-size-cli-baseline.json \
  --health-json docs/autonomous-modernization/evidence/hermes-token-optimization/local-ai-health-chat-baseline.json \
  --json /tmp/hermes-cost.json
```

## Privacy

The report aggregates counts and model/lane names. It does not log prompt text, secret values, token prefixes, cookies, private keys, or raw credential files.
