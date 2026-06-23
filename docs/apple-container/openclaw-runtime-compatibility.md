# OpenClaw Runtime Compatibility

Date: 2026-06-23

OpenClaw remains Docker-only for its gateway service in the current dual-runtime deployment.

## Finding

The production OpenClaw Compose stack mounts:

```text
/var/run/docker.sock:/var/run/docker.sock
```

That dependency gives the gateway Docker Engine control capabilities. Apple Container is an OCI runtime for macOS but is not a Docker Engine API replacement, and this pilot must not fake or expose a broad Docker socket inside Apple Container.

## Outcome

| Component | Status | Reason |
|---|---|---|
| OpenClaw gateway | Docker-only | Docker socket dependency |
| Open WebUI | deferred | compatible candidate, but heavier service postponed due current swap pressure |
| OpenCode web | deferred | compatible candidate, but not needed for the first low-risk mirror |
| Octopoda helper | deferred | no user-facing pilot value until gateway strategy is settled |

Safe future options:

1. Disable Docker-management features if OpenClaw supports it.
2. Mirror only UI components while gateway remains Docker.
3. Build a narrow external helper with explicitly allowed operations.
4. Keep the full stack Docker-only.

Do not mount the production Docker socket into Apple Container.
