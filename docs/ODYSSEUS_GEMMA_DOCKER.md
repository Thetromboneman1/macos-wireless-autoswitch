# Odysseus Docker + Gemma Setup

This repo includes a companion Odysseus Docker stack for local AI workspace workflows. It keeps Odysseus separate from the macOS Wi-Fi auto-switch daemon and stores Odysseus runtime data under `odysseus/data/`.

## What Is Installed

- Odysseus web UI, built from `pewdiepie-archdaemon/odysseus`.
- ChromaDB for memory/vector storage.
- SearXNG for internal web search.
- ntfy for local notifications.
- A Gemma endpoint map seeded into Odysseus.

The stack defaults to upstream Odysseus `main`, the stable curated branch. Change `ODYSSEUS_GIT_REF` in `odysseus/.env` to pin a specific commit or use another branch.

## Start

```bash
scripts/odysseus-docker.sh install
```

Open:

```text
http://127.0.0.1:7000
```

On first boot, Odysseus prints the temporary admin password in the container logs:

```bash
docker compose --env-file odysseus/.env -p odysseus-gemma -f odysseus/docker-compose.yml logs odysseus | grep 'Temporary password'
```

Change the password in Odysseus after login.

## Gemma Model Wiring

The configurator creates these Odysseus model endpoints:

| Role | Endpoint ID | Default model ID | Intended use |
| --- | --- | --- | --- |
| Primary | `gemma-primary` | `mlx-community--gemma-4-31b-it-4bit` | Primary chat/reasoning |
| Coding | `gemma-coding` | `mlx-community--gemma-4-26b-a4b-it-4bit` | Coding/edit/apply |
| Fast | `gemma-fast` | `mlx-community--gemma-4-e4b-it-4bit` | Fast chat/edit/apply/autocomplete |
| Small | `gemma-small` | `mlx-community--gemma-4-e2b-it-4bit` | Small/routing tasks |

Odysseus settings are seeded as:

| Odysseus setting | Gemma role |
| --- | --- |
| Default chat model | Primary |
| Deep research model | Primary |
| Utility model | Small |
| Background task model | Small |
| Default fallback chain | Coding, then Fast, then Small |
| Utility fallback chain | Fast |

Odysseus does not currently expose separate first-class settings for every "coding/edit/apply/autocomplete" sub-role. Those models are still pinned and selectable in the model picker, and the role map is persisted at `odysseus/data/gemma-role-map.json`.

## Model Server Requirement

Docker on macOS cannot use Metal GPU acceleration for model serving. This setup therefore expects Gemma to be served outside the Odysseus container through an OpenAI-compatible API.

Default oMLX endpoint:

```text
http://host.docker.internal:18080/v1
```

The helper auto-detects the local oMLX API key from `~/.omlx/settings.json` when `ODYSSEUS_GEMMA_API_KEY` is blank. The key is passed into Odysseus during configuration and is not committed to Git.

The host oMLX runtime should use TTL-based unloading so all four Gemma role models are not permanently resident. Apply the balanced policy with:

```bash
scripts/omlx-power-policy.sh normal
```

Use `scripts/omlx-power-policy.sh battery` when unplugged or under thermal pressure. See `docs/OMLX_POWER_POLICY.md` for the exact TTLs and manual unload/load commands.

If all four models are served from one API, edit:

```bash
ODYSSEUS_GEMMA_BASE_URL=http://host.docker.internal:18080/v1
```

If the models are served on different ports, set per-role URLs:

```bash
ODYSSEUS_GEMMA_PRIMARY_BASE_URL=http://host.docker.internal:8001/v1
ODYSSEUS_GEMMA_CODING_BASE_URL=http://host.docker.internal:8002/v1
ODYSSEUS_GEMMA_FAST_BASE_URL=http://host.docker.internal:8003/v1
ODYSSEUS_GEMMA_SMALL_BASE_URL=http://host.docker.internal:8004/v1
```

If your serving runtime exposes different model names, update the model IDs in `odysseus/.env`, then rerun:

```bash
scripts/odysseus-docker.sh configure
```

## Common Commands

```bash
# Start existing stack
scripts/odysseus-docker.sh up

# Reapply Gemma endpoint/default settings after editing odysseus/.env
scripts/odysseus-docker.sh configure

# Show container status
scripts/odysseus-docker.sh ps

# Tail Odysseus logs
scripts/odysseus-docker.sh logs

# Stop the stack
scripts/odysseus-docker.sh down
```

## Validation

Check containers:

```bash
scripts/odysseus-docker.sh ps
```

Check the seeded Gemma role map:

```bash
cat odysseus/data/gemma-role-map.json
```

From inside Odysseus, each endpoint should be visible in Admin or the model picker. If an endpoint appears but chat fails, verify the host model server answers from the container:

```bash
docker compose --env-file odysseus/.env -p odysseus-gemma -f odysseus/docker-compose.yml exec odysseus \
  python - <<'PY'
import httpx
print(httpx.get("http://host.docker.internal:18080/health", timeout=5).text[:1000])
PY
```

If that request fails, start or rebind your host model server before debugging Odysseus.
