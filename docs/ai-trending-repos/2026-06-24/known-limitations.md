# Known Limitations

- The review did not independently verify "top trending this week" ranking beyond current GitHub repository activity, stars, releases, and recent pushes.
- Headroom was not benchmarked because source build exceeded the bounded validation window.
- oMLX `/v1/models` was not queried with an authenticated key in this pass; unauthenticated access returned HTTP 401.
- Rapid-MLX at `127.0.0.1:8010` was not running during validation.
- Go and pnpm were not installed, blocking AgentsView and Flue test execution.
- PaddleOCR OCR quality was not tested because OCR/model tooling was not installed and no nonsensitive fixture set existed yet.
- Codebase Memory MCP was not installed because the installer can modify agent/MCP config and index code. That needs an allowlisted pilot with rollback.
- Agent-Reach was not authorized to import browser cookies, Reddit sessions, Twitter/X sessions, Xiaohongshu sessions, or other account material.
- OpenMontage was not run because broad media pipelines and many skills/tools need an isolated security review first.
