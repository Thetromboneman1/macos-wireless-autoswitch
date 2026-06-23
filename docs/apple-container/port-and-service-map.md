# Apple Container Port And Service Map

Date: 2026-06-23

The authoritative pilot map is `config/apple-container/port-map.json`.

## Policy

| Rule | Value |
|---|---|
| Pilot prefix | `ac-` |
| Pilot bind address | `127.0.0.1` |
| Pilot port range | `19000-19999` |
| Production ports | never reused |
| Validation | `scripts/apple-container/validate-port-map.sh` |

## Current Pilot Assignments

| Service | Production | Apple Container pilot | Status |
|---|---:|---:|---|
| Hermes WebUI | `8787` | `19081` | candidate |
| Hermes OpenCode Web | `4096` | `19096` | candidate |
| OpenClaw gateway | `18789` | `19082` | blocked by Docker socket dependency |
| Open WebUI | `3000` | `19083` | candidate |
| OpenClaw OpenCode | `4097` | `19097` | candidate |
| Odysseus | `7000` | `19070` | candidate |
| ChromaDB | `8100` | `19100` | candidate |
| ntfy | `8091` | `19091` | dual-runtime validated |
| Ansible controller | `8080` | `19088` | candidate |
| OmniRoute | `20128` | `19128` | candidate build required |
| MCP gateway | none selected | `19085` | placeholder |

Run:

```bash
scripts/apple-container/validate-port-map.sh
```

The validator fails when a pilot port is occupied, outside the reserved range, duplicated, bound to anything other than localhost, or reused from the production list.
