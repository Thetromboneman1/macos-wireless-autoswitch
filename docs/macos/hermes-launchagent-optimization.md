# Hermes LaunchAgent Optimization

Date: 2026-06-23
Owner: Platform Operations

## Current Finding

No new Hermes LaunchAgent was added. The approved AI LaunchAgent remains `com.corn.omlx-power-policy`, which preserves oMLX availability without making llama.cpp or Rapid-MLX always-on.

## Requirements For Any Future Hermes LaunchAgent

- absolute executable paths;
- explicit working directory;
- log path under a documented directory;
- bounded retries or non-overlap guard;
- no hidden always-on lab lane;
- no port conflict with `18080`, `8002`, or `8010`;
- `--skip-chat` for routine health checks unless a chat probe is explicitly required.

## Evidence

LaunchAgent health is captured in:

- `docs/autonomous-modernization/evidence/hermes-token-optimization/local-ai-health-chat-baseline.json`
- `docs/autonomous-modernization/evidence/hermes-token-optimization/local-ai-health-chat-after-trim.json`
