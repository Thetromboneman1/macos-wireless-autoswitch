# Apple Container Current Platform Discovery

Date: 2026-06-23

This is the mandatory current-state map for the Apple Container side-by-side pilot. It is discovery evidence, not a promotion decision. Production remains Docker Desktop plus native macOS inference.

## Host

| Item | Observed value |
|---|---|
| Hardware | Apple Silicon arm64 |
| Memory | 64 GiB unified memory |
| macOS | 26.5.1 build 25F80 |
| Docker Desktop | 4.77.0, Docker Engine 29.5.3, linux/arm64 |
| Docker context | `desktop-linux` |
| Apple Container | `container` 1.0.0, commit `ee848e3` |
| Apple Container system | Started during this pilot bootstrap |
| Apple Container default network | `192.168.64.0/24` |
| Apple Container containers/images/volumes | Empty at discovery time |

Official Apple Container notes used for this pilot: Apple describes `container` as an OCI image runtime for Linux containers on Apple silicon, backed by lightweight virtual machines; the project README says macOS 26 is the supported floor and documents `container system start` as the first-start service command. The local CLI matches the current 1.0.0 release.

Sources:

- <https://github.com/apple/container>
- <https://github.com/apple/container/releases>

## Native AI Lanes

| Lane | Endpoint | State | Evidence |
|---|---:|---|---|
| oMLX production | `http://127.0.0.1:18080/v1` | Healthy | `/health` returned `status: healthy`, four Gemma models listed |
| llama.cpp coding | `http://127.0.0.1:8002/v1` | Running | `llama-server` listening on `127.0.0.1:8002`, model `gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf` |
| Rapid-MLX lab | `http://127.0.0.1:8010/v1` | Stopped | connection refused; this is expected for a manual lab lane |

Native MLX/Metal inference remains outside Apple Container unless a future benchmark proves equal or better support.

## Production Docker Workloads

| Container | Image | State | Published ports |
|---|---|---|---|
| `openclaw` | `ghcr.io/openclaw/openclaw:latest` | healthy | `18789` |
| `openclaw-opencode` | `smanx/opencode:1.15.4` | healthy | `127.0.0.1:4097` |
| `hermes-webui` | `hermes-hermes-webui` | healthy | `8787` |
| `hermes-opencode-web` | `smanx/opencode:latest` | healthy | `127.0.0.1:4096` |
| `hermes-agent` | `hermes-hermes-agent` | healthy | none |
| `odysseus-gemma-odysseus-1` | `odysseus-gemma-odysseus` | running | `127.0.0.1:7000` |
| `odysseus-gemma-searxng-1` | `searxng/searxng:2026.5.31-7159b8aed` | healthy | internal `8080` only |
| `odysseus-gemma-chromadb-1` | `chromadb/chroma:latest` | running | `127.0.0.1:8100` |
| `odysseus-gemma-ntfy-1` | `binwiederhier/ntfy` | running | `127.0.0.1:8091` |
| `ansible_controller` | `local/ansible-lab:controller` | running | `127.0.0.1:8080` |
| `open-webui` | `ghcr.io/open-webui/open-webui:v0.9.6` | healthy | `3000` |
| `openclaw-octopoda` | `python:3.12-slim` | running | none |
| `hermes-octopoda` | `python:3.12-slim` | running | none |
| `ansible_worker1` | `local/ansible-lab:worker1` | running | internal SSH |
| `ansible_worker2` | `local/ansible-lab:worker2` | running | internal SSH |

## Production Ports

The pilot must not reuse these ports: `3000`, `4096`, `4097`, `7000`, `8002`, `8010`, `8080`, `8091`, `8100`, `8787`, `18080`, `18789`, `20128`, `53530`.

Apple Container pilot ports are reserved in `19000-19999`, documented in `config/apple-container/port-map.json`, and validated by `scripts/apple-container/validate-port-map.sh`.

## LaunchAgents And Daemons

| Path | Role |
|---|---|
| `/Users/corn/Library/LaunchAgents/com.corn.omlx-power-policy.plist` | oMLX power policy |
| `/Users/corn/Library/LaunchAgents/com.corn.omlx.plist.disabled` | disabled legacy oMLX start path |
| `/Users/corn/Library/LaunchAgents/homebrew.mxcl.dnscrypt-proxy.plist` | LocalDNSCrypt service |
| `/Library/LaunchDaemons/com.docker.socket.plist` | Docker socket helper |
| `/Library/LaunchDaemons/com.docker.vmnetd.plist` | Docker networking helper |

No Apple Container pilot LaunchAgent was created in this pass. Early pilot startup remains manual.

## Open Blockers

- Apple Container can run OCI images but does not provide Docker Engine API compatibility. Workloads requiring `/var/run/docker.sock` are blocked or Docker-only until redesigned.
- Compose stacks must be translated explicitly; no native Compose compatibility is assumed.
- Apple Container mirror workloads have not been promoted or started. The current completed milestone is discovery plus guardrails.
