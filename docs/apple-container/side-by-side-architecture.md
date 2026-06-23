# Apple Container Side-By-Side Architecture

Date: 2026-06-23

```mermaid
flowchart LR
  subgraph Native["Native macOS production AI"]
    OMLX["oMLX 127.0.0.1:18080/v1"]
    LLAMA["llama.cpp 127.0.0.1:8002/v1"]
    RAPID["Rapid-MLX 127.0.0.1:8010/v1 manual"]
  end

  subgraph Docker["Docker Desktop production"]
    HERMES["Hermes containers"]
    OPENCLAW["OpenClaw containers"]
    ODYSSEUS["Odysseus containers"]
    ANSIBLE["Ansible lab"]
  end

  subgraph Pilot["Apple Container pilot"]
    ACH["ac-hermes-* 19081/19096"]
    ACO["ac-openclaw-* 19082/19083/19097"]
    ACD["ac-odysseus-* 19070/19091/19100"]
    ACA["ac-ansible-controller 19088"]
    ACR["ac-omniroute 19128"]
  end

  HERMES --> OMLX
  OPENCLAW --> OMLX
  OPENCLAW --> LLAMA
  ODYSSEUS --> OMLX
  ANSIBLE --> OMLX

  ACH -. test profile .-> OMLX
  ACO -. test profile .-> OMLX
  ACO -. coding .-> LLAMA
  ACD -. test profile .-> OMLX
  ACA -. test profile .-> OMLX
  ACR -. route candidate .-> OMLX

  Pilot -. isolated storage .-> STORE["~/.local/share/apple-container-pilot"]
```

The pilot is a separate test lane. It must not bind production ports, write production volumes, replace host oMLX, or alter default Codex/Hermes/OpenCode/Goose profiles.
