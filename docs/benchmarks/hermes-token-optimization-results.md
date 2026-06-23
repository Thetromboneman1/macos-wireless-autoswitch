# Hermes Token Optimization Results

Date: 2026-06-23
Owner: Platform Operations

## Implemented Changes

- Disabled default CLI access to browser, vision, image generation, TTS, cron, messaging, and computer-use toolsets.
- Added Hermes token/cost reporting to the AIOps cycle.
- Preserved local oMLX as the production default.
- Left llama.cpp and Rapid-MLX as manual lanes.

## Before And After

| Metric | Before | After |
|---|---:|---:|
| CLI disabled high-cost toolsets | 0 | 7 |
| `prompt-size` tool count | 29 | 29 |
| Estimated tool-schema tokens | 11,694 | 11,694 |
| Estimated fixed prompt tokens | 20,130 | 20,130 |
| oMLX tiny chat status | pass | pass |
| Hermes one-shot status | not captured | pass |

## Interpretation

The supported Hermes tool toggle changed runtime availability, but the installed `prompt-size` command did not show a reduced schema budget. Therefore, this pass does not claim a 40-50% token reduction.

The measurable win is governance and safety: expensive workflow tools no longer appear as enabled CLI defaults, and recurring AIOps reports now include Hermes fixed-overhead and usage aggregation.

## Evidence

- `docs/autonomous-modernization/evidence/hermes-token-optimization/hermes-tools-list-after-trim.txt`
- `docs/autonomous-modernization/evidence/hermes-token-optimization/hermes-cost-baseline.json`
- `docs/autonomous-modernization/evidence/hermes-token-optimization/hermes-cost-after-trim.json`
- `docs/autonomous-modernization/evidence/hermes-token-optimization/hermes-oneshot-after-trim.txt`
