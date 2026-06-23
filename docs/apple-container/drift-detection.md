# Apple Container Drift Detection

Date: 2026-06-23

Apple Container drift checks compare:

- `config/apple-container/port-map.json`
- pilot scripts in `scripts/apple-container/`
- Docker Compose source stacks
- documented service names, ports, and storage roots
- `.env.apple-container.example` files once created
- health endpoints and rollback rules

Severity model:

| Severity | Meaning |
|---|---|
| Critical | production port/data collision, secret leak, unsafe mount, default profile replacement |
| Warning | undocumented port, missing health check, version drift, unvalidated profile |
| Informational | new candidate service, doc-only inventory change |

Current implementation starts with port-map validation and health-script reporting. Full Compose-vs-pilot drift comparison is pending the translation pass.
