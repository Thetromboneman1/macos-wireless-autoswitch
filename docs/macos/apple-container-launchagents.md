# Apple Container LaunchAgents

Date: 2026-06-23

No Apple Container pilot LaunchAgent was created.

## Policy

Early pilot operation is manual and on demand. A LaunchAgent may be added only after:

1. the mirrored services pass smoke tests,
2. rollback is tested,
3. logs are isolated,
4. restart behavior is bounded,
5. the LaunchAgent is disabled by default or explicitly approved.

Reserved labels:

- `com.corn.apple-container-pilot`
- `com.corn.apple-container-health`
- `com.corn.apple-container-drift`

Each future LaunchAgent must use absolute paths, separate logs under `~/.local/share/apple-container-pilot/logs`, and must not start at login until the pilot is promoted.
