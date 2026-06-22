# 10 - DNSCrypt Fix and Ranked Stars Implementation

## Baseline

- Timestamp: 2026-06-22T15:55:26Z
- Repo path: `/Users/corn/Documents/Corn_Automation/macos-wireless-autoswitch`
- Branch: `main`
- Git state at start: ahead of `origin/main` by 2 local commits.
- Existing local commits:
  - `f31e2eb infra: implement GitHub stars, DNSCrypt optimization, local AI modernization`
  - `c40678c local-ai: implement Codex star sweep and model-serving updates`
- Screenshot-observed AdGuard target: `LocalDNSCrypt` at `127.0.0.1:53530`.

## Existing Findings

- Prior audit saw macOS resolver path as `vlan0 -> 192.168.10.1`.
- Prior audit saw `/opt/homebrew/etc/dnscrypt-proxy.toml` configured for `127.0.0.1:53`.
- New validation found nothing listening on `127.0.0.1:53530` or `127.0.0.1:53`.
- New validation found the dnscrypt-proxy config existed, but the Homebrew `dnscrypt-proxy` package was not installed.

## DNSCrypt Root Cause

AdGuard was configured correctly for the intended local provider, but the local provider was absent:

```text
AdGuard LocalDNSCrypt -> 127.0.0.1:53530 -> no listener
```

The stale config file on `127.0.0.1:53` made the earlier audit look like a port mismatch, but the deeper issue was missing dnscrypt-proxy installation/service state.

## DNSCrypt Implementation

### Evidence

- `command -v dnscrypt-proxy` returned nothing before install.
- `/opt/homebrew/opt/dnscrypt-proxy/sbin/dnscrypt-proxy` did not exist before install.
- `brew services info dnscrypt-proxy` reported `Running: false`, `Loaded: false`, `Schedulable: false`.

### Decision

Install dnscrypt-proxy and align its listener to AdGuard's screenshot-observed target: `127.0.0.1:53530`.

### Change

- Backed up config to `backups/dnscrypt-20260622-105231/dnscrypt-proxy.toml`.
- Installed `dnscrypt-proxy 2.1.16` with Homebrew.
- Updated `/opt/homebrew/etc/dnscrypt-proxy.toml`:

```toml
listen_addresses = ['127.0.0.1:53530']
```

- Started user service:

```text
~/Library/LaunchAgents/homebrew.mxcl.dnscrypt-proxy.plist
```

- Added `scripts/network/dnscrypt-healthcheck.sh`.

### Validation

| Check | Result |
| --- | --- |
| UDP listener | `dnscrypt-proxy` listening on `127.0.0.1:53530` |
| TCP listener | `dnscrypt-proxy` listening on `127.0.0.1:53530` |
| `dig @127.0.0.1 -p 53530 example.com` | `NOERROR`, 57 ms |
| `dig +tcp @127.0.0.1 -p 53530 example.com` | `NOERROR`, 92 ms |
| `dig @127.0.0.1 -p 53530 sigok.verteiltesysteme.net` | `NOERROR` |
| `dig @127.0.0.1 -p 53530 dnssec-failed.org` | `SERVFAIL` |
| `scripts/network/dnscrypt-healthcheck.sh` | logged `ok` |

## Ranked GitHub Stars Implementation

Source: `docs/autonomous-modernization/github-stars-ranked.json`.

Implemented in this pass:

| Repo / tool | Bucket | Action | Validation | Rollback |
| --- | --- | --- | --- | --- |
| `dnscrypt-proxy` from DNS objective | Required by AdGuard integration | Installed and configured local listener | `dig` and healthcheck passed | `brew services stop dnscrypt-proxy`; restore backup config |
| `aaif-goose/goose` | Must Implement | Documented as already part of local stack; no new install | Existing repo/config inventoried | No change to rollback |
| `Thetromboneman1/Openclaw` | Must Implement | Documented as separate dirty repo; no overwrite | `git status` reviewed | No change to rollback |
| `Thetromboneman1/hermes-*`, `NousResearch/hermes-agent` | Must Implement | Documented as separate dirty/behind repos; no overwrite | `git status` reviewed | No change to rollback |
| `google-gemma/gemma-skills` | Must Implement | Kept as document/evaluate item | No install performed | No change to rollback |
| `nvk/llm-wiki` | Must Implement | Kept as document/evaluate item | No install performed | No change to rollback |

Skipped or deferred:

| Repo / tool | Bucket | Reason |
| --- | --- | --- |
| `SiliconScope` | Must Implement | Useful telemetry GUI, but installing a GUI app is not necessary to fix DNSCrypt and needs a separate UI/runtime trial. |
| `Understand-Anything` | Must Implement | High-value code graph tool; requires choosing a target repo and indexing scope. |
| `gbrain`, `ECC`, `osaurus`, `OpenHands`, `npcsh` | Must/High | Overlap existing Codex/OpenCode/Hermes agent stack; install would add parallel frameworks without a narrow trial. |
| `coreai-model-zoo` | Must | Prior compatibility note says current production stack should stay oMLX/GGUF until macOS/Xcode Core AI runtime support is ready. |
| `headroom`, `LEANN`, `turbovec`, `Octopoda-OS` | High | Promising infra candidates, but require separate data/indexing/proxy decisions. |
| `PonyExl3`, `edge-lm`, `ApodexAI/AgentHarness` | High | Model/eval research; no selected serving target today. |
| `apple/container` | High | Interesting Mac container runtime, but not needed for DNSCrypt and does not replace host-side Metal model serving. |

## Local Repo Sweep

| Repo | Status | Decision |
| --- | --- | --- |
| `Boneman_Projects` | dirty local AI docs | Do not overwrite or commit from this repo. |
| `Hermes` | dirty and behind upstream by 2 | Separate reconciliation needed. |
| `Openclaw` | dirty Docker compose | Separate focused audit needed. |
| `odysseus-gemma-docker` | dirty local AI docs/scripts | Separate commit in that repo if desired. |

## Rollback

```bash
brew services stop dnscrypt-proxy
cp backups/dnscrypt-20260622-105231/dnscrypt-proxy.toml /opt/homebrew/etc/dnscrypt-proxy.toml
brew services restart dnscrypt-proxy
```

If AdGuard DNS fails, disable DNS Protection or switch away from `LocalDNSCrypt` in the AdGuard UI until the local listener is restored.

