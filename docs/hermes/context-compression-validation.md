# Hermes Context Compression Validation

Date: 2026-06-23
Owner: Platform Operations

## Current Config

Installed Hermes config already matches the conservative community recommendation:

```yaml
compression:
  enabled: true
  threshold: 0.5
  target_ratio: 0.2
  protect_last_n: 20
  summary_model: mlx-community--gemma-4-e4b-it-4bit
```

## Decision

Keep the current compression settings. Do not lower the threshold below `0.30` without long-session evidence that coding accuracy, tool loops, and requirement retention still pass.

## Required Future Test

Before changing compression:

1. Run current settings on a long Hermes session.
2. Test default 50% threshold.
3. Test one profile between 30% and 50%.
4. Confirm no lost user requirements, malformed summaries, or summary recursion.
5. Confirm the summary model can handle the effective input context it receives.

No more aggressive compression was enabled in this pass.
