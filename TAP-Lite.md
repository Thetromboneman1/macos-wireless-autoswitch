# TAP Lite

## Executive Summary
Automatic Wi-Fi control based on wired/VLAN link state on macOS via launchd.

## Business Purpose
Deliver reliable and maintainable functionality for the workspace AI platform and associated operations.

## Architecture Overview
- wireless.sh detection and Wi-Fi toggling
- install.sh lifecycle management
- launchd daemon plist for system monitoring

## Data Flow
~~~mermaid
flowchart TD
  A[Trigger] --> B[macos-wireless-autoswitch Service Layer]
  B --> C[State and Config]
  B --> D[Execution]
  D --> E[Observability and Validation]
~~~

## Dependencies
- Runtime and platform dependencies documented in repository README.
- Local environment and endpoint configuration in user-managed config files.

## AI Integration Strategy
No direct model inference; integrates with broader workspace automation policies.

## Security Considerations
- Principle of least privilege for background services and automation.
- Protect credentials in local env files and secret stores.
- Validate external endpoint reachability and authentication.

## Operational Considerations
- Include health checks for core commands/services.
- Keep rollback-first workflow for system and service changes.
- Prefer non-destructive cleanup unless explicitly approved.

## Risks
Incorrect interface detection may disable expected network paths; validate after OS updates.

## Roadmap
- Continue benchmark-driven tuning.
- Improve service consolidation and endpoint standardization.
- Track production-readiness metrics in catalog reports.
