# Apple Container Repository Migration Inventory

Date: 2026-06-23

## Repository Summary

| Repository | Branch | Remote | State | Container assets | Pilot classification |
|---|---|---|---|---|---|
| `/Users/corn/Documents/Corn_Automation/macos-wireless-autoswitch` | `main` | `origin/main` | clean | `odysseus/docker-compose.yml`, health/scripts/docs | primary governance repo |
| `/Users/corn/Documents/odysseus-gemma-docker` | `main` | `origin/main` | clean | `odysseus/docker-compose.yml` | compatible with changes |
| `/Users/corn/Documents/Openclaw` | `main` | `origin/main` | clean | `docker-compose.yml` | partial; gateway blocked by Docker socket |
| `/Users/corn/Documents/Ansible` | `main` | `origin/main` | clean | `compose.yaml`, `compose.dev.yaml` | compatible with changes |
| `/Users/corn/Documents/Boneman_Projects` | `main` | `origin/main` | clean | `local-ai-platform/starred-repos-lab/docker-compose.yml` | candidate after data review |
| `/Users/corn/Documents/Hermes` | `main` | `upstream/main` | clean | `docker-compose.yaml`, nested stacks | compatible with changes |
| `/Users/corn/Documents/Hermes/hermes-agent` | detached `HEAD` | `origin`, `private` | clean | `Dockerfile`, `docker-compose.yml` | candidate; branch state needs separate handling |
| `/Users/corn/Documents/Hermes/hermes-webui` | `local-llm-docs` | `fork/local-llm-docs` | clean | `Dockerfile`, `docker-compose.yml` | candidate |
| `/Users/corn/Documents/Hermes/hermes-desktop` | `main` | `upstream/main` | ahead 3, behind 84 | none found | keep out of pilot commits |
| `/Users/corn/Documents/Hermes/OmniRoute` | `main` | `origin/main` | clean | `Dockerfile`, `docker-compose.yml` | candidate build required |
| `/Users/corn/Documents/Corn_Automation/Goose` | `main` | `origin/main` | clean | none | client profile only |
| `/Users/corn/Documents/YTKillerPlus` | `main` | `origin/main` | behind 8 | none | not needed for pilot |

## Compose And Runtime Findings

| Stack | Services | Current production dependencies | Apple Container concern |
|---|---|---|---|
| OpenClaw | OpenClaw, Open WebUI, OpenCode, Octopoda | oMLX via `host.docker.internal`, llama.cpp via `host.docker.internal`, Docker socket mount | OpenClaw gateway mounts `/var/run/docker.sock`; classify that service as blocked until redesigned |
| Hermes | Hermes agent, web UI, OpenCode, Octopoda | host oMLX and local Docker network | translate service order and health checks manually |
| Odysseus | Odysseus, ChromaDB, ntfy, searxng | host oMLX via Docker host bridge | verify Apple Container host reachability before mirroring |
| Ansible | controller, workers | code-server on `8080`, host oMLX | likely compatible, but SSH worker topology must be re-created explicitly |
| OmniRoute | Next/Electron/API stack | local dev port `20128` | build/runtime commands need a focused pass |

## Required Follow-Up

1. Parse every Compose stack into service, network, volume, health, and secret rows.
2. Create per-repo `.env.apple-container.example` files only after the target commands are known.
3. Keep commits repository-specific; do not bundle nested repo edits into the governance repo commit.
4. Do not touch `Hermes/hermes-desktop` until its upstream divergence is reconciled.
