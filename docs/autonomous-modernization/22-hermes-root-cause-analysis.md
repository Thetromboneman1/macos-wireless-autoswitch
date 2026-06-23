# 22 - Hermes Root Cause Analysis

Date: 2026-06-23

## Executive Summary

Resolved. Hermes CLI one-shot requests were failing with:

```text
API call failed after 3 retries: Connection error.
```

The root cause was host/container endpoint drift in host-side Hermes config. Direct oMLX validation succeeded on `127.0.0.1:18080`, but Hermes fallback and named custom-provider paths still pointed to Docker-only `host.docker.internal` URLs. On this macOS host, `host.docker.internal` did not resolve, so Hermes retried failed requests until it reported a generic connection error.

## Evidence

Live oMLX validation passed:

- `GET http://127.0.0.1:18080/health` returned healthy engine-pool state.
- Authenticated `GET http://127.0.0.1:18080/v1/models` returned the four Gemma role models.
- Direct OpenAI Python SDK chat completion against `http://127.0.0.1:18080/v1` returned `OK`.
- `scripts/local-ai/validate-hermes-mlx.py` passed `models`, `chat_completion`, and `tool_call`.

Hermes request dumps showed the failing path:

```text
POST http://host.docker.internal:18080/v1/chat/completions
model: mlx-community--gemma-4-e2b-it-4bit
reason: max_retries_exhausted
```

Host DNS check showed:

```text
host.docker.internal -> nodename nor servname provided, or not known
```

## Affected Paths

The stale values were in host-side Hermes files:

- `~/.hermes/config.yaml`
- `~/.hermes/.env`

The Docker endpoint remains valid for Docker consumers such as Odysseus. The fix applies only to host-side Hermes execution.

## Remediation

Updated host-side Hermes config:

- oMLX/Gemma endpoints: `http://127.0.0.1:18080/v1`
- GGUF coding lane: `http://127.0.0.1:8002/v1`
- Named custom providers: host loopback instead of `host.docker.internal`
- Fallback providers: host loopback instead of `host.docker.internal`

## Verification

After remediation:

```text
hermes -z 'Reply with exactly OK.' --provider custom --model mlx-community--gemma-4-26b-a4b-it-4bit
OK.

hermes -z 'Reply with exactly OK.' --provider custom:local-mlx-routing --model mlx-community--gemma-4-e2b-it-4bit
OK.
```

Endpoint validator:

```text
docs/autonomous-modernization/hermes-mlx-validation-omlx.json
ok: true
```

## Operating Rule

Use `127.0.0.1` for host tools. Use `host.docker.internal` only inside Docker containers.
