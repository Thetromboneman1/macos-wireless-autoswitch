# Hermes Cost Token Governance

Date: 2026-06-23
Owner: Platform Operations

## Weekly Audit

Run:

```bash
scripts/operations/run-aiops-cycle.sh
```

Review:

- actual default model and provider;
- fixed prompt overhead;
- tool-schema overhead;
- cache-hit percentage;
- input/output token split;
- fallback events;
- background job costs;
- local-versus-cloud percentage;
- browser/vision/computer-use activation;
- memory growth;
- compression settings.

## Promotion Gate

Do not promote a new Hermes default model or provider unless it beats the current oMLX lane on:

- tool-call success;
- multi-turn reliability;
- latency and throughput;
- memory/swap impact;
- privacy;
- cost;
- rollback simplicity.

Community reports are useful hypotheses, not promotion evidence.
