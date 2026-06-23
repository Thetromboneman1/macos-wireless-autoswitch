# Local Repository Inventory

Date: 2026-06-23

Scope: `~/Documents`, `~/Projects`, `~/Developer`, and known Corn/Boneman local AI workspaces. Remote refs were refreshed with `git fetch --all --prune`; no working trees were reset, cleaned, or stashed.

## Inventory

| Repository | Local path | Remote | Branch | Upstream | Ahead/behind | Dirty | Actions | Disposition |
|---|---|---|---|---|---:|---|---|---|
| llama.cpp | `/Users/corn/Developer/ML-Models/Gemma4/repos/llama.cpp` | `https://github.com/ggml-org/llama.cpp` | `master` | `origin/master` | `0/161` | clean | yes, upstream estate | Experimental engine source; update only in a measured benchmark window. |
| Ansible | `/Users/corn/Documents/Ansible` | `https://github.com/Thetromboneman1/Ansible.git` | `main` | `origin/main` | `0/0` | clean | yes | Active supporting automation; healthy. |
| Boneman_Projects | `/Users/corn/Documents/Boneman_Projects` | `https://github.com/Thetromboneman1/Boneman_Projects.git` | `main` | `origin/main` | `0/0` | modified docs | no | Canonical local AI docs; preserve existing user/local edits. |
| Goose | `/Users/corn/Documents/Corn_Automation/Goose` | `https://github.com/Thetromboneman1/Goose.git` | `main` | `origin/main` | `0/0` | clean | no | Active local config; healthy. |
| macos-wireless-autoswitch | `/Users/corn/Documents/Corn_Automation/macos-wireless-autoswitch` | `https://github.com/Thetromboneman1/macos-wireless-autoswitch.git` | `main` | `origin/main` | `0/0` | modified by this pass | yes | Active governance and platform automation repo. |
| Hermes workspace | `/Users/corn/Documents/Hermes` | `https://github.com/Thetromboneman1/hermes-workspace.git` | `main` | `upstream/main` | `1/2` | modified config/docs/gitlink | yes | Manual reconciliation required; do not auto-merge over local AI wiring. |
| OmniRoute | `/Users/corn/Documents/Hermes/OmniRoute` | `https://github.com/Thetromboneman1/OmniRoute.git` | `main` | `origin/main` | `0/0` | clean | yes | Dormant fork/reference checkout. |
| hermes-agent | `/Users/corn/Documents/Hermes/hermes-agent` | `https://github.com/Thetromboneman1/hermes-agent.git` | `main` | `origin/main` | `0/1302` | clean | yes | Fork/private mirror; upstream refresh is a separate decision. |
| hermes-desktop | `/Users/corn/Documents/Hermes/hermes-desktop` | `https://github.com/Thetromboneman1/hermes-desktop.git` | `main` | `upstream/main` | `3/84` | clean | yes | Divergent legacy/reference checkout; manual decision required. |
| hermes-webui | `/Users/corn/Documents/Hermes/hermes-webui` | `https://github.com/nesquena/hermes-webui.git` | `local-llm-docs` | `fork/local-llm-docs` | `0/0` | clean | yes | Local docs branch; healthy. |
| Openclaw | `/Users/corn/Documents/Openclaw` | `https://github.com/Thetromboneman1/Openclaw.git` | `main` | `origin/main` | `0/0` | modified compose | yes | Active local stack; preserve existing compose edit. |
| YTKillerPlus | `/Users/corn/Documents/YTKillerPlus` | `https://github.com/iKarwan/YTKillerPlus.git` | `main` | `origin/main` | `0/8` | clean | no | Upstream app checkout; update manually when needed. |
| odysseus-gemma-docker | `/Users/corn/Documents/odysseus-gemma-docker` | `https://github.com/Thetromboneman1/odysseus-gemma-docker.git` | `main` | `origin/main` | `0/0` | modified docs/env/script | yes | Active Docker consumer; preserve existing local AI edits. |

## Notes

- Archived or divergent upstream checkouts were inventoried but not rewritten.
- Existing dirty files outside this repo were treated as unrelated local work unless already documented as part of the local AI stack.
- Secret values were not read or recorded.
