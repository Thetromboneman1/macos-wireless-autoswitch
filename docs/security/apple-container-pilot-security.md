# Apple Container Pilot Security

Date: 2026-06-23

## Controls

- Bind pilot services to `127.0.0.1`.
- Use `ac-` names for every pilot container.
- Use only `19000-19999` pilot ports.
- Keep secrets in 1Password vault `Boneman`.
- Do not commit `.env` files, token prefixes, cookies, private keys, or raw credential files.
- Do not mount production Docker volumes or credential directories read-write.
- Preserve Docker Desktop production services during the pilot.

## Current Security Findings

| Item | Status |
|---|---|
| Apple Container system | installed and running |
| Pilot ports | mapped; `19091` is occupied only by enabled `ac-ntfy` |
| OpenClaw gateway | blocked because it mounts `/var/run/docker.sock` in production Compose |
| Pilot secrets | no real secrets committed; `ac-ntfy` uses no sensitive value for current local health path |
| LaunchAgents | none created |

## Required Before Workload Start

For each image: record source, tag, digest when practical, architecture, exposed ports, user, mounts, health check, and logs. Prefer localhost bindings and least writable storage.

`ac-ntfy` image source is `docker.io/binwiederhier/ntfy:latest`, manifest digest `sha256:f8a9b104313b87cc24ae4f775f39e6328205b57dff6ede3eaf098a91e5d79f59`, platform `linux/arm64`, localhost-only pilot binding, isolated cache mount, and no Docker socket.
