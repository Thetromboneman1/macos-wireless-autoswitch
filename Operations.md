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

## oMLX Power Policy

```bash
# show loaded models and persisted TTL/pinning settings
scripts/omlx-power-policy.sh status

# normal plugged-in policy
scripts/omlx-power-policy.sh normal

# battery/thermal pressure policy
scripts/omlx-power-policy.sh battery

# apply the correct policy for the current power source once
scripts/omlx-power-watch.sh --once
```

See `docs/OMLX_POWER_POLICY.md` for the Gemma role TTLs and manual unload/load commands.
