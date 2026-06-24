# Benchmark Results

This pass used bounded smoke tests and static validation. It did not run full performance benchmarks for all candidates because several require toolchain installation, model downloads, credentials, or services with broader access.

## Measured Checks

| Target | Command Class | Result |
|---|---|---|
| SkillSpector | `uvx --from <clone> skillspector --help` | Passed; CLI exposed `scan`, `mcp`, and `baseline`. |
| SkillSpector synthetic malicious sample | Static scan, no LLM | Passed; `HIGH`, score 61, `DO_NOT_INSTALL`. |
| Addy Osmani browser-testing skill | Static scan, no LLM | Warning; `MEDIUM`, score 38, `CAUTION`, with defensive-content false positives. |
| Agent-Reach | `uvx --from <clone> agent-reach --help` | Passed; CLI installed in isolated uvx environment. |
| Agent-Reach doctor | Public capability check | Warning; 5/13 channels available, with session-dependent channels blocked by approval boundary. |
| oMLX health | `curl http://127.0.0.1:18080/health` | Passed; healthy. |
| GGUF lane models | `curl http://127.0.0.1:8002/v1/models` | Passed; Gemma 26B GGUF model listed. |

## Blocked Or Deferred Benchmarks

| Target | Blocker |
|---|---|
| Headroom | Source CLI build exceeded bounded validation window; retry with pinned release/wheel before benchmarking compression. |
| AgentsView | Go not installed; service test deferred. |
| Flue | `pnpm` not installed; sandbox test deferred. |
| PaddleOCR | OCR tool/model path not installed; pilot should use nonsensitive fixtures. |
| Codebase Memory MCP | Installer writes agent configs and indexes code; pilot needs allowlist and rollback first. |
| LMCache | Rejected for local Mac stack; benchmark only on compatible Linux/vLLM/GPU server. |
| OpenMontage | Deferred due broad media/tool/skill surface and AGPL review needs. |

## Headroom Benchmark Plan

Use representative local workloads only:

- `scripts/health/local-ai-health.py` output.
- A synthetic build/test log with stack traces.
- A nonsensitive excerpt of repository analysis output.

For each sample, record input token estimate, compressed token estimate, percentage reduction, latency, preserved facts, lost facts, and recommended integration mode. Do not repeat upstream compression claims as local measured results until reproduced.
