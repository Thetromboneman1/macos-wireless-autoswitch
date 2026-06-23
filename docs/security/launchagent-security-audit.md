# LaunchAgent Security Audit

Date: 2026-06-23

## Findings

| Finding | Risk | Action |
|---|---|---|
| Legacy `com.corn.vllm-mlx` references missing script | Medium | Keep disabled; archive plist after manual confirmation. |
| Frequent `com.boneman.magic-mouse-scroll-reverser` interval | Low | Keep if needed, but review whether 5s polling is still necessary. |
| Third-party Razer and Sideloadly agents consume background memory | Low | Documented as swap contributors; do not remove automatically. |
| oMLX power policy is active and valid | Low | Keep as approved startup policy. |

## Rules

- Validate plists with `plutil -lint`.
- Validate executable paths before enabling an agent.
- Prefer logs under a predictable application support or logs directory.
- Do not auto-enable experimental AI servers at login.
