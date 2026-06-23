# Repository Inventory

Date: 2026-06-23

## Local Repositories

| Repository | Branch | Dirty files | Workflows | Last commit | Remote |
|---|---|---:|---:|---|---|
| `Ansible` | `main` | 0 | 2 | 2026-06-08 | `Thetromboneman1/Ansible` |
| `Boneman_Projects` | `main` | 7 | 0 | 2026-06-11 | `Thetromboneman1/Boneman_Projects` |
| `Corn_Automation/Goose` | `main` | 0 | 0 | 2026-06-08 | `Thetromboneman1/Goose` |
| `macos-wireless-autoswitch` | `main` | active changes | 3 | 2026-06-23 | `Thetromboneman1/macos-wireless-autoswitch` |
| `Hermes` | `main` | 9 | 3 | 2026-06-22 | local workspace root |
| `Hermes/OmniRoute` | `main` | 0 | 7 | 2026-06-04 | `Thetromboneman1/OmniRoute` |
| `Hermes/hermes-agent` | `main` | 0 | 11 | 2026-06-11 | `Thetromboneman1/hermes-agent` |
| `Hermes/hermes-desktop` | `main` | 0 | 1 | 2026-06-04 | `Thetromboneman1/hermes-desktop` |
| `Hermes/hermes-webui` | `local-llm-docs` | 0 | 3 | 2026-06-07 | `nesquena/hermes-webui` |
| `Openclaw` | `main` | 1 | 2 | 2026-06-22 | `Thetromboneman1/Openclaw` |
| `YTKillerPlus` | `main` | 0 | 0 | 2026-06-09 | `iKarwan/YTKillerPlus` |
| `odysseus-gemma-docker` | `main` | 4 | 1 | 2026-06-11 | `Thetromboneman1/odysseus-gemma-docker` |

Dirty files outside this repository were not modified in this pass.

## GitHub Repositories

| Repository | Active | Fork | Default branch | Actions focus |
|---|---:|---:|---|---|
| `macos-wireless-autoswitch` | yes | yes | `main` | current remediation target |
| `hermes-agent` | yes | yes | `main` | separate CI surface |
| `hermes-agent-private` | yes | no | `main` | private staging |
| `Openclaw` | yes | no | `main` | separate CI surface |
| `hermes-workspace` | yes | no | `main` | workspace metadata |
| `odysseus-gemma-docker` | yes | no | `main` | Docker companion |
| `Boneman_Projects` | yes | no | `main` | canonical local platform docs |
| `Goose` | yes | no | `main` | local tool config |
| `Ansible` | yes | no | `main` | automation |
| `hermes-webui` | yes | no | `master` | web UI |
| `hermes-desktop` | yes | yes | `main` | divergent legacy/reference checkout |
| `OmniRoute` | yes | yes | `main` | routing lab |
| `stremio-docker-setup` | yes | no | `main` | unrelated Docker service |

## Risk Levels

- High: repositories with workflows plus dirty local state should be audited before automated pushes.
- Medium: forks with upstream divergence need explicit merge decisions.
- Low: repositories with no Actions and clean local state.
