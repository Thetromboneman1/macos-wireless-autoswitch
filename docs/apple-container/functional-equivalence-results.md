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
| ntfy health | `http://127.0.0.1:8091/v1/health` returned healthy | `http://127.0.0.1:19091/v1/health` returned healthy | pass |
| ntfy restart | Docker production remained running | `scripts/apple-container/restart-all.sh` restarted `ac-ntfy` and health passed | pass |
| ntfy self-heal | Docker production remained healthy | stopped `ac-ntfy`; `scripts/apple-container/self-heal.sh` restarted it and reported healthy | pass |
| Apple Container mirror service startup | Docker services healthy | `ac-ntfy` running | pass for selected workload |

The mirror has reached equivalence for the selected low-risk `ntfy` workload. Heavier candidates remain deferred while swap pressure is high.
