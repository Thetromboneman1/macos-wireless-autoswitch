# Apple Container Pilot Workloads

Date: 2026-06-23

## Enabled Workloads

| Workload | Docker production | Apple Container pilot | Status |
|---|---|---|---|
| ntfy | `odysseus-gemma-ntfy-1` on `127.0.0.1:8091` | `ac-ntfy` on `127.0.0.1:19091` | dual-runtime validated |

## ac-ntfy

| Field | Value |
|---|---|
| Why selected | Small ARM64 HTTP service, no Docker socket, no privileged mode, no production database |
| Production image | `binwiederhier/ntfy` |
| Apple Container image | `docker.io/binwiederhier/ntfy:latest` |
| Image digest | `sha256:f8a9b104313b87cc24ae4f775f39e6328205b57dff6ede3eaf098a91e5d79f59` |
| Architecture | `linux/arm64` |
| Production port | `127.0.0.1:8091 -> 80/tcp` |
| Pilot port | `127.0.0.1:19091 -> 80/tcp` |
| Production storage | Docker volume `odysseus-gemma_ntfy-cache` |
| Pilot storage | `~/.local/share/apple-container-pilot/volumes/ac-ntfy/cache` |
| Secrets required | none for current health and local test path |
| Health check | `/v1/health` |
| Functional test | `scripts/apple-container/compare-all.sh` |
| Rollback | `scripts/apple-container/rollback-all.sh` |

## Deferred Workloads

ChromaDB, Open WebUI, Hermes WebUI, OpenCode, Ansible, and OmniRoute remain candidates. They were not started in this pass because live swap was already above 80 percent and the request requires production stability ahead of breadth.
