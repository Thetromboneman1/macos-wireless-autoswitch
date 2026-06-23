# Apple Container Storage Isolation

Date: 2026-06-23

## Root

Pilot storage root:

```text
~/.local/share/apple-container-pilot/
```

Expected layout:

```text
~/.local/share/apple-container-pilot/
├── data/
├── volumes/
├── logs/
├── state/
├── backups/
├── env/
└── benchmarks/
```

## Rules

- Never mount Docker production volumes read-write into Apple Container.
- Never mount `~/.omlx`, `~/.config/goose`, or raw credential files into pilot containers.
- Use 1Password vault `Boneman` for secret references; docs may name item names and retrieval methods, not values.
- Copy only sanitized fixtures or read-only snapshots into `data/`.
- Preserve logs and evidence during rollback.

## Per-Service Draft Roots

Per-service roots are declared in `config/apple-container/port-map.json` under each service's `storage` key. Those roots are placeholders until the Compose translation pass maps exact volume targets.

## Active Pilot Storage

| Service | Path | Purpose |
|---|---|---|
| `ac-ntfy` | `~/.local/share/apple-container-pilot/volumes/ac-ntfy/cache` | test-only ntfy cache mounted at `/var/cache/ntfy` |

The start script rejects pilot roots outside `~/.local/share/apple-container-pilot*` and creates `data`, `volumes`, `logs`, `state`, `env`, `backups`, `benchmarks`, and `evidence` before starting enabled services.
