# AdGuard + Local DNSCrypt Setup

## Final Architecture

```text
Apps/Browsers
  -> AdGuard for Mac DNS Protection
  -> LocalDNSCrypt 127.0.0.1:53530
  -> dnscrypt-proxy
  -> selected encrypted upstream resolvers
  -> Internet
```

## Current Working State

- AdGuard screenshot-observed provider: `LocalDNSCrypt`.
- AdGuard target: `127.0.0.1:53530`.
- dnscrypt-proxy version: `2.1.16`.
- dnscrypt-proxy config: `/opt/homebrew/etc/dnscrypt-proxy.toml`.
- listener: `listen_addresses = ['127.0.0.1:53530']`.
- launchd label: `homebrew.mxcl.dnscrypt-proxy`.
- service plist: `~/Library/LaunchAgents/homebrew.mxcl.dnscrypt-proxy.plist`.

## Commands

```bash
brew services list | grep -i dnscrypt
lsof -nP -iUDP:53530 -iTCP:53530
dig @127.0.0.1 -p 53530 example.com
dig +tcp @127.0.0.1 -p 53530 example.com
dig @127.0.0.1 -p 53530 dnssec-failed.org
scripts/network/dnscrypt-healthcheck.sh
```

## Install Or Repair

```bash
brew install dnscrypt-proxy
cp -av /opt/homebrew/etc/dnscrypt-proxy.toml "backups/dnscrypt-$(date +%Y%m%d-%H%M%S)/"
sed -i '' "s|^listen_addresses = .*|listen_addresses = ['127.0.0.1:53530']|" /opt/homebrew/etc/dnscrypt-proxy.toml
brew services restart dnscrypt-proxy
dig @127.0.0.1 -p 53530 example.com
```

## Self-Healing

Use the repo healthcheck:

```bash
scripts/network/dnscrypt-healthcheck.sh
tail -f ~/Library/Logs/dnscrypt-healthcheck.log
```

It checks the `53530` listener, runs a DNS query, restarts `dnscrypt-proxy` with Homebrew if needed, retests, logs the result, and exits non-zero if still unhealthy.

No separate healthcheck LaunchAgent is enabled by this repo. The dnscrypt-proxy Homebrew service already runs from `~/Library/LaunchAgents/homebrew.mxcl.dnscrypt-proxy.plist`.

## Rollback

```bash
brew services stop dnscrypt-proxy
cp backups/dnscrypt-YYYYMMDD-HHMMSS/dnscrypt-proxy.toml /opt/homebrew/etc/dnscrypt-proxy.toml
brew services restart dnscrypt-proxy
```

If AdGuard DNS fails, switch AdGuard DNS Protection back to a known-good provider or temporarily disable DNS Protection from the AdGuard UI.

