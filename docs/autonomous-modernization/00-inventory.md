# 00 - Inventory

## Facts

- Host: macOS 26.5.1, Apple M1 Max, 64 GB unified memory, Metal 4.
- Docker Desktop is running on arm64 with about 8 GB container memory.
- oMLX is live at `http://127.0.0.1:18080/v1`.
- llama.cpp GGUF coding lane is live at `http://127.0.0.1:8002/v1`.
- GitHub CLI is authenticated and exported 45 starred repos.
- AdGuard and WireGuard are running; DNSCrypt config exists but is not active in macOS resolver path.

## Evidence

- `scutil --dns` showed `192.168.10.1` on `vlan0`.
- `curl /health` on oMLX returned healthy.
- llama.cpp `/v1/models` returned `gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf`.
- `docs/autonomous-modernization/github-stars.json` contains the raw star export.
- `docs/autonomous-modernization/github-stars-ranked.json` contains the ranked star summary.

## Unknowns

- Router-side DNS implementation behind `192.168.10.1`.
- Exact AdGuard DNS filtering mode from the GUI.
- Whether DNS UDP timeout is transient or policy-driven.

