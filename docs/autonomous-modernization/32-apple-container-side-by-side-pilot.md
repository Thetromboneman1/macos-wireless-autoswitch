# Apple Container Side-By-Side Pilot Report

Date: 2026-06-23

## Outcome So Far

The pilot completed the first safe milestone:

- audited the local host, production Docker services, native AI lanes, LaunchAgents, repositories, skills, and Apple Container runtime;
- bootstrapped Apple Container 1.0.0 with its recommended kernel;
- created the `ac-` naming and `19000-19999` port plan;
- added validation, status, health, and rollback scripts;
- documented workload compatibility and migration blockers.

No production service was replaced. No Apple Container workload was promoted.

## Evidence Highlights

- oMLX production: healthy at `127.0.0.1:18080`.
- llama.cpp coding lane: listening at `127.0.0.1:8002`.
- Rapid-MLX lab lane: stopped at `127.0.0.1:8010`.
- Docker Desktop: production workloads running for OpenClaw, Hermes, Odysseus, Open WebUI, and Ansible.
- Apple Container: CLI and system service running; no pilot containers yet.

## Recommendation

Use a hybrid pilot. Keep native AI and Docker Desktop as production. Start Apple Container with low-risk support services first: `ntfy`, `ChromaDB`, then single-service UI/tool endpoints. Defer or reject services that require Docker socket access unless their architecture is changed.
