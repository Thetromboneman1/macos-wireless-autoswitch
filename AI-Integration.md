# AI Integration

## Integration Scope
No direct model inference in the macOS Wi-Fi auto-switch daemon. Odysseus is installed as a separate Docker companion stack for local AI workspace workflows.

## Operational Notes
- Use OpenAI-compatible endpoint abstractions when possible.
- Keep secrets in environment/config, not in repository source.
- Validate model endpoint health before enabling automated workflows.
- Odysseus Docker/Gemma setup lives in `odysseus/` and is managed by `scripts/odysseus-docker.sh`.
- Gemma model role mapping is documented in `docs/ODYSSEUS_GEMMA_DOCKER.md`.

## Risks
Incorrect interface detection may disable expected network paths; validate after OS updates.
Odysseus automation depends on a reachable host or remote model server; Docker on macOS does not provide Metal GPU acceleration to the container.
