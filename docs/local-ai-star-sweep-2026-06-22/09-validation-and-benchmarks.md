# Loop 8 - Validation and Benchmarks

## Commands Run

| Check | Result |
| --- | --- |
| `scripts/local-ai/healthcheck.sh` | Passed after executable bit was set |
| `scripts/local-ai/benchmark-smoke.sh` | Passed |
| `jq . ~/.config/opencode/opencode.json` | Passed |
| `opencode models` | Listed GGUF and oMLX models |
| oMLX `/v1/models` | Returned four Gemma MLX models |
| GGUF `/v1/models` | Returned `gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf` |

## Benchmark Evidence

| Metric | Result |
| --- | --- |
| oMLX chat smoke | Returned exactly `OK` |
| GGUF completion tokens | 128 |
| GGUF curl seconds | `1.998155` |
| GGUF output tok/s | `64.06` |
| Recent server log prompt eval | about `155.93 tok/s` on a 32-token cached prompt |
| Recent server log generation | about `71.81 tok/s` on a 128-token run |
| GGUF process RSS | about 2.7 GiB resident, with model memory largely Metal/mmap-backed |

## Known Failure Mode

The first `scripts/local-ai/healthcheck.sh` call was launched before `chmod +x` completed in a parallel batch and returned permission denied. Re-running after chmod passed.

