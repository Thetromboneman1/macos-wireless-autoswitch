# Apple Container Workload Compatibility Matrix

Date: 2026-06-23

| Workload | Classification | Reason | Next action |
|---|---|---|---|
| oMLX / MLX-LM | Must remain native macOS | Metal/MLX acceleration and current production endpoint are host-native | keep on `127.0.0.1:18080` |
| llama.cpp coding lane | Must remain native macOS | Metal GGUF lane already measured on host | keep on `127.0.0.1:8002` |
| Rapid-MLX | Must remain native macOS lab | experimental MLX lane | keep manual on `127.0.0.1:8010` |
| Hermes WebUI | Compatible with changes | OCI image exists; needs explicit ports/env/storage | translate first |
| Hermes agent | Compatible with changes | local image exists; no published port | validate env and host reachability |
| Hermes OpenCode Web | Compatible with changes | OCI image exists; needs auth and endpoint profile | translate first |
| OpenClaw gateway | Blocked | production Compose mounts `/var/run/docker.sock` | redesign or keep Docker |
| Open WebUI | Compatible with changes | OCI image exists; data volume must be isolated | translate first |
| OpenClaw OpenCode | Compatible with changes | OCI image exists; needs separate profile | translate first |
| Odysseus | Compatible with changes | local image exists; depends on ChromaDB/ntfy/searxng | translate full dependency order |
| ChromaDB | Compatible with changes | OCI image exists; persistence must be isolated | test persistence |
| ntfy | Compatible with changes | OCI image exists; simple port/storage model | smoke test |
| searxng | Partially compatible | image exists; network and config need review | translate after Odysseus |
| Ansible controller/workers | Compatible with changes | local images exist; multi-container SSH topology | translate network/worker dependencies |
| OmniRoute | Candidate build required | Dockerfile exists; current app is dev-oriented | build explicit pilot image |
| Docker socket consumers | Must remain Docker or be redesigned | Apple Container is not a Docker Engine API replacement | document blockers |
