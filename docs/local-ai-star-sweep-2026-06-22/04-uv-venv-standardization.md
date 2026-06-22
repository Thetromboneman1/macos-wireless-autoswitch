# Loop 3 - uv + venv Standardization

## Evidence

`uv 0.11.3` is installed. Python-related repos found:

| Repo | Python config | Decision |
| --- | --- | --- |
| `llama.cpp` | `pyproject.toml`, `requirements.txt` | Leave unchanged; upstream project conventions. |
| `Ansible` | `.config/requirements.txt` | Leave unchanged; likely Ansible venv workflow, no repo edits in this pass. |
| `Hermes/hermes-agent` | `pyproject.toml`, `uv.lock`, setup files | Already uv-compatible; do not migrate while repo is 1188 commits behind. |
| `Hermes/hermes-webui` | `requirements.txt` | Document-only; branch-specific app, no safe migration without running full tests. |

## Decision

No cross-repo uv migration was performed. The safe improvement is to keep new local scripts shell-based and avoid forcing Python packaging changes into dirty or divergent repos.

## Recommended Future Work

- For `hermes-webui`, add `pyproject.toml` only after its branch and test matrix are reconciled.
- For `Ansible`, keep the current dedicated venv unless converting the playbook tooling to `uv tool` is explicitly requested.

