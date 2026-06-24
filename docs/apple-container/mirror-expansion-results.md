# Mirror Expansion Results

Updated: 2026-06-24

| Workload | Docker state | Apple Container state | Disposition |
|---|---|---|---|
| ntfy | running on 127.0.0.1:8091 | running on 127.0.0.1:19091 | keep mirror running |
| OpenClaw gateway | running, Docker socket dependent | not mirrored | Docker-only until runtime-neutral socket replacement exists |
| ChromaDB | running | not started | defer behind resource gate |
| Open WebUI | running | not started | defer behind resource gate |
| Hermes UI | running | not started | defer behind resource gate |
