# Cross-Repository Consolidation

Date: 2026-06-23

## Decisions

| Function | Current locations | Decision |
|---|---|---|
| Local AI health checks | `macos-wireless-autoswitch/scripts/health`, related docs in Boneman_Projects | Keep this repo as the executable health-check home; Boneman_Projects remains canonical architecture narrative. |
| Drift detection | `macos-wireless-autoswitch/scripts/health/drift-detection` | Keep repo-local; it depends on this repo's local platform docs and fixtures. |
| Benchmark scripts | `scripts/local-ai`, `llama.cpp` upstream tooling | Keep split; upstream engine benchmarks should not be centralized into governance scripts. |
| Docker consumer wiring | Openclaw, odysseus-gemma-docker, Hermes docs | Keep repo-local config; synchronize endpoint policy through docs. |
| GitHub Actions validation | This repo, Ansible, Hermes forks, Odysseus | Add this repo's repository-validation workflow; evaluate reusable workflows later after dirty repos are reconciled. |
| Secret handling | Boneman vault docs across repos | Use `Boneman` only; document item names and retrieval methods, never secret values. |

The consolidation principle is to centralize policy and evidence, not every script. Local repo independence is retained where it improves recovery or avoids local-service assumptions in CI.
