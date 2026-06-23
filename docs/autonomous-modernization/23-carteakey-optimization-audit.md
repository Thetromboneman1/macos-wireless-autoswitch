# 23 - Carteakey Optimization Audit

Date: 2026-06-23

Source: [Carteakey Local LLM Inference Optimization](https://carteakey.dev/blog/local-inference/local-llm-optimization/)

## Scope

The Carteakey guide is primarily a CUDA/Linux and llama.cpp tuning guide. This platform is an Apple Silicon local AI stack with oMLX/MLX as the production lane, llama.cpp/Metal as the reliability lane, and Rapid-MLX as an experimental lane. Items below are classified for this machine, not copied blindly from CUDA assumptions.

## Audit Matrix

| Optimization | Status | Apple Silicon Adaptation |
|---|---|---|
| Measure TTFT, prompt processing, token generation, memory, and long-session drift | Partially implemented | Existing benchmark captures TTFT, wall tok/s, RSS deltas, context scaling, and 2-way concurrency. Long-duration scripts are now documented as required soak tests. |
| Prefer explicit backend selection over generic desktop wrappers | Implemented | Production lane is direct oMLX/MLX. llama.cpp and Rapid-MLX are separate lanes. Ollama is not the default. |
| Compare Apple Silicon MLX with llama.cpp Metal | Implemented | Existing bake-off compares oMLX/MLX and llama.cpp GGUF/Metal-compatible serving. |
| Context sizing and KV-cache pressure awareness | Partially implemented | Benchmarks include moderate context and RSS delta. Next step is 1h/4h/overnight drift capture. |
| Keep single-user homelab parallelism conservative | Implemented | Production oMLX uses TTL unload behavior. Rapid-MLX concurrency is lab-only. |
| Flash attention | Backend dependent | Applicable where exposed by MLX/Rapid-MLX/llama.cpp launchers. Not force-enabled globally. |
| KV cache quantization | Backend dependent | CUDA flags from the guide do not directly apply to oMLX. llama.cpp experiments should record KV type when supported by the active build. |
| MTP/speculative decoding | Not production applicable | MTP remains disabled for the Apple Silicon GGUF lane because prior validation found it unsuitable here. |
| Layer placement, `--fit`, `-ngl`, `-ot` | Lab applicable | Relevant to llama.cpp/Metal experiments. Not applicable to oMLX production config. |
| `--no-mmap` and `--mlock` | Lab applicable | Consider only for llama.cpp long-session tests; monitor memory pressure and swap first. |
| CPU P-core pinning / `taskset` | Not applicable | Linux hybrid-CPU advice does not map cleanly to macOS Apple Silicon. |
| Linux power-profile tuning / headless mode | Not applicable | Replaced by macOS LaunchAgent power policy and TTL unload behavior. |
| CUDA graph / cuBLAS / CUDA env vars | Not applicable | CUDA-only. |
| Vision/mmproj tuning | Lab applicable | Keep in llama.cpp reliability lane; do not promote until memory headroom is measured. |
| Security notes for local endpoints | Implemented | Secret docs point to Boneman and runtime settings, not committed values. |

## Production Decisions

- Keep oMLX/MLX as the production front door.
- Keep llama.cpp as a reliability and diagnostic lane with explicit launch scripts.
- Keep Rapid-MLX Qwen3.6 as experimental high-throughput lane.
- Do not enable MTP in production on this Mac.
- Treat memory pressure and swap as promotion blockers.

## Implementation Follow-Up

- Use `scripts/health/local-ai-health.py` before and after benchmark runs.
- Run long-duration tests before promoting Rapid-MLX or any llama.cpp KV-cache profile.
- Record every benchmark with endpoint, model, backend, context size, concurrency, RSS delta, and swap delta.
