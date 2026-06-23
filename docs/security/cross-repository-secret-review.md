# Cross-Repository Secret Review

Date: 2026-06-23

## Scope

Secret scanning was run for repositories that received commits during this
pass. Findings were reviewed as redacted file paths only.

## Results

| Repository | Result | Notes |
| --- | --- | --- |
| `Ansible` | pass | No leaks found. |
| `odysseus-gemma-docker` | pass | No leaks found. |
| `Openclaw` | pass | No leaks found. |
| `Hermes` | pass | No leaks found. |
| `Boneman_Projects` | existing findings | 153 historical findings, concentrated in UniFi support exports and one old benchmark log. None matched changed local-AI files. |
| `Hermes/hermes-webui` | existing findings | 12 historical findings in test fixture files. None matched changed workflow files. |

## Existing-Risk File Families

Boneman_Projects redacted report file families:

- `docs/network/unifi-support-*/.../unifi-core/ipc.messageBox.log`
- `docs/network/unifi-support-*/.../unifi/teleport.json`
- `docs/network/unifi-support-*/.../unifi/logs/server.log`
- `docs/network/unifi-support-*/.../unifi/devices/**/system.cfg`
- `docs/network/unifi-analysis/system-sanitized.cfg.json`
- `mlx-native-bench/audit-results/**/logs/*.log`

Hermes WebUI redacted report file families:

- `tests/test_custom_providers_in_panel.py`
- `tests/test_issue1094_provider_bugs.py`
- timestamped `.bak` copies of those test files

## Recommendation

Handle existing findings in a separate cleanup:

1. Preserve forensic value outside Git if needed.
2. Remove or sanitize support archives and fixture backups.
3. Rotate any credentials that may have been exposed.
4. Add a documented gitleaks baseline or required scan after cleanup.
