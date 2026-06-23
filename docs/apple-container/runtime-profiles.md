# Runtime Profiles

Date: 2026-06-23

Runtime profiles live under `config/runtime-profiles/`.

| Profile | Purpose |
|---|---|
| `production` | current Docker Desktop plus native oMLX defaults |
| `docker-current` | explicit Docker Desktop service profile |
| `apple-container-pilot` | enabled Apple Container mirror services |
| `side-by-side` | comparison profile exposing Docker and Apple Container endpoints |
| `native-ai` | native macOS AI endpoints only |
| `rollback-safe` | production-only fallback with pilot disabled |

All profiles use `1Password: Boneman` as the sensitive-value source. The profile files contain endpoint and service references only, not secret values.

Current side-by-side service:

| Service | Docker endpoint | Apple Container endpoint |
|---|---|---|
| ntfy | `http://127.0.0.1:8091/v1/health` | `http://127.0.0.1:19091/v1/health` |
