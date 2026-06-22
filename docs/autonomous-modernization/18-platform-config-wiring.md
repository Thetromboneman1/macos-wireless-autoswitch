# Platform Config Wiring

Date: 2026-06-22

## Summary

This pass wired user-level agent and editor configs to the shared local-AI
platform policy created in the previous integration pass.

Backups:

```text
~/.local/share/codex-star-tools/backups/20260622-161103-platform-configs/
```

## Updated Configs

| Surface | Change |
|---|---|
| Codex | Added `local_ai_platform` pointers to routing policy, MCP topology, runbook, and `Boneman`. |
| Codex plugin | Installed and enabled `wiki@llm-wiki` with `codex plugin add wiki@llm-wiki`. |
| OpenCode | Added platform docs to the instruction list and allowed the platform config/docs directories. |
| Goose | Added `GOOSE_LOCAL_AI_PLATFORM` with routing, MCP, runbook, and vault pointers. |
| Hermes | Added `local_ai_platform` with routing, MCP, runbook, model-routing, and vault pointers. |
| Hermes WebUI | Set default model to the local Gemma 31B reasoning lane and added platform pointers. |
| Hermes WebUI MVP | Set default model to the local Gemma 31B reasoning lane and added platform pointers. |
| VS Code user settings | Added `localAiPlatform.*` pointers for routing, MCP, runbook, and vault. |
| Hermes workspace VS Code | Switched Python package manager from pip to uv and added platform pointers. |
| OpenClaw workspace VS Code | Switched Python package manager from pip to uv and added platform pointers. |

## 1Password

The duplicate `Boneman Projects` vault was checked twice and had zero items.
It was then deleted with the 1Password CLI. The canonical vault remains:

```text
Boneman
```

## Plugin Materialization

`codex plugin list` showed `wiki@llm-wiki` as available but not installed.
Running `codex plugin add wiki@llm-wiki` installed version `0.12.0` and
left it enabled.

## Safety Boundaries

- Cloud provider fallback was not removed.
- OmniRoute, headroom, Octopoda, and OpenHands are still not autostarted.
- No secret values were read or written.
- Config backups were created before user-level edits.

## Validation

Validation for this pass:

```bash
codex plugin list
op vault get Boneman --format json
jq empty ~/.config/opencode/opencode.json
jq empty ~/Library/Application\ Support/Code/User/settings.json
python3 - <<'PY'
import tomllib, pathlib
tomllib.loads(pathlib.Path("~/.codex/config.toml").expanduser().read_text())
PY
LOCAL_AI_BENCH_ENGINES=omlx-mlx \
  LOCAL_AI_BENCH_OUTPUT=docs/autonomous-modernization/benchmark-results-omlx-extended.json \
  python3 scripts/local-ai/benchmark-engine-bakeoff.py
LOCAL_AI_BENCH_ENGINES=llama-cpp-gguf \
  LOCAL_AI_BENCH_OUTPUT=docs/autonomous-modernization/benchmark-results-llama-cpp-extended.json \
  python3 scripts/local-ai/benchmark-engine-bakeoff.py
```

The combined all-engine benchmark can exceed an interactive tool runtime window,
so per-engine runs are the preferred operational method.
