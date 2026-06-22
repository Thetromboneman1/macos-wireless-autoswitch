#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TOOL_HOME="${STAR_TOOL_HOME:-$HOME/.local/share/codex-star-tools}"

check() {
  printf '\n== %s ==\n' "$1"
}

check "uv tool commands"
command -v leann
leann --help >/dev/null
command -v leann_mcp
command -v octopoda
octopoda --help >/dev/null
command -v octopoda-mcp

check "edge-lm"
"$TOOL_HOME/envs/edge-lm/bin/python" - <<'PY'
import edge_lm, importlib.metadata, sys
print("edge-lm", getattr(edge_lm, "__version__", importlib.metadata.version("edge-lm")))
print("mlx", importlib.metadata.version("mlx"))
print("python", sys.version.split()[0])
PY

check "PonyExl3"
"$TOOL_HOME/envs/ponyexl3/bin/python" - <<'PY'
import ponyexl3, importlib.metadata, sys
print("ponyexl3", getattr(ponyexl3, "__version__", importlib.metadata.version("ponyexl3")))
print("mlx", importlib.metadata.version("mlx"))
print("python", sys.version.split()[0])
PY

check "turbovec"
"$TOOL_HOME/envs/turbovec/bin/python" - <<'PY'
import importlib.metadata
import numpy as np
import turbovec

idx = turbovec.TurboQuantIndex(dim=8, bit_width=2)
vectors = np.asarray(
    [[1.0, 0, 0, 0, 0, 0, 0, 0], [0, 1.0, 0, 0, 0, 0, 0, 0]],
    dtype=np.float32,
)
queries = np.asarray([[1.0, 0, 0, 0, 0, 0, 0, 0]], dtype=np.float32)
idx.add(vectors)
scores, indexes = idx.search(queries, 1)
print("turbovec", importlib.metadata.version("turbovec"))
print("search", scores.tolist(), indexes.tolist())
PY

check "SiliconScope"
"$ROOT/tmp/star-downloads/kennss__SiliconScope/.build/debug/sscope-cli" --samples 1 >/dev/null
echo "sscope-cli sample ok"

check "headroom"
"$ROOT/tmp/star-downloads/headroomlabs-ai__headroom/target/release/headroom-proxy" --help >/dev/null
echo "headroom-proxy ok"

check "OpenHands"
docker image inspect ghcr.io/openhands/agent-server:1.29.0-python >/dev/null
echo "OpenHands agent-server image present"

check "llm-wiki"
grep -Fq '[plugins."wiki@llm-wiki"]' "$HOME/.codex/config.toml"
grep -Fq 'llm-wiki-opencode/skills/wiki-manager/SKILL.md' "$HOME/.config/opencode/opencode.json"
echo "llm-wiki config present"

check "Understand-Anything"
test -L "$HOME/.understand-anything-plugin"
test -L "$HOME/.agents/skills/understand"
test -d "$HOME/.understand-anything/repo/node_modules"
echo "Understand-Anything links and deps present"

check "OmniRoute"
test -d "$ROOT/tmp/star-downloads/diegosouzapw__OmniRoute/node_modules"
echo "OmniRoute dependencies present"

printf '\nAll star deployment checks passed.\n'
