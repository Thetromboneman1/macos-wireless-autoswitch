# Repository Reorganization Plan

Updated: 2026-06-24

This plan narrows macos-wireless-autoswitch back to wireless automation while preserving platform content in the correct destination repositories.

## Atomic Batches

1. Repository-governance documents to Boneman_Projects.
2. Apple Container platform tooling and config to Boneman_Projects.
3. Local AI health, drift, and runtime-profile configuration to Boneman_Projects.
4. Docker/Odysseus assets to odysseus-gemma-docker.
5. Hermes-specific docs and tests to the relevant Hermes repository.
6. Historical modernization reports to `docs/archive/2026/` in the canonical governance repo.
7. Wireless repo README, docs, tests, LaunchAgents, and CI narrowing after destination validation.

## Commit Order

For each batch: add destination copy, validate destination, commit and push destination, update source references, remove source copy, validate source, commit and push source, then record both commits in the provenance register.
