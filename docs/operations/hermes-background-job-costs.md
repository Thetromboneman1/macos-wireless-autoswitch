# Hermes Background Job Costs

Date: 2026-06-23
Owner: Platform Operations

## Current State

No new Hermes cron, gateway, heartbeat, research, or maintenance job was created in this pass.

Hermes cron tooling supports per-job `enabled_toolsets`. Use that instead of broad defaults for recurring work.

## Job Review Checklist

For each recurring job, document:

- schedule and required frequency;
- model and provider;
- enabled toolsets;
- expected input/output tokens;
- whether it can run local-only;
- off-peak schedule;
- non-overlap guard;
- retry limit;
- log path and retention.

Routine endpoint checks should prefer `scripts/health/local-ai-health.py --skip-chat` unless a chat completion is the point of the test.
