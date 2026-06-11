# AI Integration

## Integration Scope
No direct model inference in the macOS Wi-Fi auto-switch daemon. Odysseus is installed as a separate Docker companion stack for local AI workspace workflows.

## Operational Notes
- Use OpenAI-compatible endpoint abstractions when possible.
- Keep secrets in environment/config, not in repository source.
- Validate model endpoint health before enabling automated workflows.
- Odysseus Docker/Gemma setup lives in `odysseus/` and is managed by `scripts/odysseus-docker.sh`.
- Gemma model role mapping is documented in `docs/ODYSSEUS_GEMMA_DOCKER.md`.
- Host-side oMLX memory and battery behavior is managed by `scripts/omlx-power-policy.sh` and documented in `docs/OMLX_POWER_POLICY.md`.

## Risks
Incorrect interface detection may disable expected network paths; validate after OS updates.
Odysseus automation depends on a reachable host or remote model server; Docker on macOS does not provide Metal GPU acceleration to the container.
Pinned oMLX models ignore idle TTLs. Keep large Gemma models unpinned unless there is a deliberate need to keep them resident.
