# Platform Risk Register

Date: 2026-06-23
Owner: Platform Operations

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Sustained high swap pressure | High | Medium | Keep lab lanes manual, unload large models, stop nonessential Docker/apps before benchmarks | SRE |
| Model promotion from point-in-time benchmark | Medium | High | Require trend analysis, stability evidence, tool-call validation, and promotion gates | AI Platform |
| Lab lane accidentally becomes always-on | Medium | Medium | Drift detection on `8002` and `8010`; no new AI LaunchAgent without review | Platform Operations |
| Docker background services add hidden pressure | Medium | Medium | Review `docker stats`, stop unused stacks, keep inference on host oMLX | Platform Operations |
| VS Code/Codex tooling drift | Medium | Medium | Dependency report, health recommendations check, monthly review | AI Tooling |
| Documentation staleness | Medium | Medium | Documentation review automation and owner/date metadata | Documentation Owner |
| Secret leakage through backup/config docs | Low | High | Boneman pointer policy and gitleaks validation | Security |
| Model cache loss | Medium | Medium | Document model sources and treat cache restore as maintenance-window work | AI Platform |
| oMLX endpoint outage | Medium | High | DR runbook restores production oMLX before lab lanes | SRE |
| GitHub or local repo divergence | Low | Medium | Push approved phases and verify `main...origin/main` is clean | Platform Operations |
