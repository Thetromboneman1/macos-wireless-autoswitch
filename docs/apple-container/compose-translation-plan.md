# Apple Container Compose Translation Plan

Date: 2026-06-23

Apple Container is not treated as a Docker Compose replacement. Each Compose stack must be translated into reviewed `container run` or `container create/start` commands.

## Translation Checklist

For each Compose file:

1. Parse services, images, builds, entrypoints, commands, env, env files, ports, volumes, networks, dependencies, health checks, restart policies, profiles, and secrets.
2. Reject or defer services that require Docker socket access, privileged device access, unsupported host networking, or unsafe production mounts.
3. Assign `ac-` names from `config/apple-container/port-map.json`.
4. Bind only to `127.0.0.1`.
5. Map writable data only under `~/.local/share/apple-container-pilot`.
6. Preserve startup order with explicit health waits.
7. Stop in reverse dependency order.
8. Save logs under the pilot log root.

## Stack Priority

| Priority | Stack | Reason |
|---:|---|---|
| 1 | ntfy | small, low-risk HTTP service |
| 2 | ChromaDB | persistence exercise with isolated volume |
| 3 | OpenCode Web | single service plus host AI endpoint profile |
| 4 | Hermes WebUI | service UI with existing local image |
| 5 | Ansible controller | local lab, port remap required |
| 6 | Odysseus full stack | multi-service dependency validation |
| 7 | Open WebUI | larger persistent UI service |
| 8 | OmniRoute | build required |
| blocked | OpenClaw gateway | Docker socket dependency |

Generated commands belong in `scripts/apple-container/start.sh` only after each service has passed a one-service smoke test.
