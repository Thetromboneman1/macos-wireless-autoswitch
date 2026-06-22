# 05 - uv Standardization

## Facts

- `uv 0.11.3` is installed.
- `Hermes/hermes-agent` already has `pyproject.toml` and `uv.lock`.
- `llama.cpp` has upstream Python packaging files and should not be locally rewritten.
- `Hermes/hermes-webui` and `Ansible` have requirements-based workflows.

## Decision

No automatic uv migration was performed. The safe path is:

- Keep `hermes-agent` on uv.
- Do not rewrite upstream `llama.cpp`.
- Convert `hermes-webui` only after branch sync and test matrix review.
- Convert Ansible tooling only if the venv path in VS Code settings is updated together.

