# Apple Container Functional Equivalence Results

Date: 2026-06-23

| Test | Production result | Apple Container result | Status |
|---|---|---|---|
| oMLX `/health` | healthy | native only | pass production |
| oMLX `/v1/models` | four Gemma models listed | native only | pass production |
| llama.cpp `/v1/models` | GGUF coding model listed | native only | pass production |
| Rapid-MLX `/v1/models` | offline | native lab only | expected stopped |
| Apple Container CLI | installed 1.0.0 | system service running | pass bootstrap |
| Apple Container pilot ports | production untouched | all configured pilot ports free | pass guardrail |
| Apple Container mirror service startup | Docker services healthy | not started yet | pending translation |

The mirror has not yet reached workload equivalence. The current pass completes discovery, runtime bootstrap, port isolation, and rollback scaffolding.
