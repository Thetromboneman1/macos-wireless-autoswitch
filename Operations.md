# Operations

## Start
./install.sh i

## Validate
sudo launchctl list | grep com.computernetworkbasics.wifionoff

## Maintenance
- Keep dependencies and scripts up to date.
- Re-run validation after configuration changes.
- Keep rollback references current before destructive changes.

## Odysseus Companion Stack

```bash
# install/start Odysseus and seed Gemma endpoints
scripts/odysseus-docker.sh install

# status/logs
scripts/odysseus-docker.sh ps
scripts/odysseus-docker.sh logs

# stop
scripts/odysseus-docker.sh down
```

See `docs/ODYSSEUS_GEMMA_DOCKER.md` for Gemma endpoint mapping and model-server requirements.
