# Automation Monitoring

Date: 2026-06-23

## Health Command

```bash
scripts/health/local-ai-health.py
```

The monitor now reports:

- oMLX endpoint validation;
- swap usage and pressure;
- expected local AI ports;
- local AI and Docker process snapshot;
- LaunchAgent plist and executable validation.

## Watch Items

| Area | Signal | Action |
|---|---|---|
| oMLX | `lanes[].ok` false | Check `127.0.0.1:18080/health` and app state. |
| Swap | `system.swap.pressure` high | Stop lab lanes and memory-heavy apps before benchmarking. |
| LaunchAgents | `classification: broken` | Keep disabled or repair path before enabling. |
| Ports | unexpected listeners | Confirm no duplicate backend started. |

## Validation

Run after automation changes:

```bash
scripts/health/local-ai-health.py
plutil -lint ~/Library/LaunchAgents/*.plist
```
