# DNSCrypt Audit - 2026-06-22

## 2026-06-22 AdGuard Correction

The AdGuard screenshot showed DNS Protection enabled with provider `LocalDNSCrypt` at `127.0.0.1:53530`. The earlier audit had only seen `/opt/homebrew/etc/dnscrypt-proxy.toml` with `listen_addresses = ['127.0.0.1:53']` and had not confirmed an active dnscrypt-proxy process.

Root cause:

- dnscrypt-proxy config existed, but the Homebrew `dnscrypt-proxy` package was not installed.
- Nothing was listening on `127.0.0.1:53530` or `127.0.0.1:53`.
- AdGuard was pointed at a local DNSCrypt endpoint that did not exist yet.

Fix applied:

- Backed up `/opt/homebrew/etc/dnscrypt-proxy.toml` to `backups/dnscrypt-20260622-105231/`.
- Installed `dnscrypt-proxy 2.1.16`.
- Changed `listen_addresses` to `['127.0.0.1:53530']` to match AdGuard.
- Started the user Homebrew service `homebrew.mxcl.dnscrypt-proxy`.
- Added `scripts/network/dnscrypt-healthcheck.sh`.

Validated path:

```text
Apps/Browsers
  -> AdGuard for Mac DNS Protection
  -> LocalDNSCrypt 127.0.0.1:53530
  -> dnscrypt-proxy
  -> encrypted upstream resolvers
  -> Internet
```

Validation evidence:

- `lsof` showed `dnscrypt-proxy` listening on UDP and TCP `127.0.0.1:53530`.
- `dig @127.0.0.1 -p 53530 example.com` returned `NOERROR`.
- `dig +tcp @127.0.0.1 -p 53530 example.com` returned `NOERROR`.
- `dig @127.0.0.1 -p 53530 dnssec-failed.org` returned `SERVFAIL`.
- `dig @127.0.0.1 -p 53530 sigok.verteiltesysteme.net` returned `NOERROR`.

See [adguard-dnscrypt-setup.md](adguard-dnscrypt-setup.md) for operating commands and rollback.

## Current State

Facts:

- macOS resolver path currently points to `192.168.10.1` on `vlan0`.
- `/etc/resolv.conf` also lists `nameserver 192.168.10.1`, but macOS warns that `scutil --dns` is authoritative.
- AdGuard for Mac and WireGuard are running.
- `/opt/homebrew/etc/dnscrypt-proxy.toml` exists and is now configured to listen on `127.0.0.1:53530` for AdGuard.
- At initial audit time, `dnscrypt-proxy`, Unbound, NextDNS, and dnsmasq were not observed as active local resolver processes. After the correction, `dnscrypt-proxy` is active on `127.0.0.1:53530`.
- `dig` over UDP to system DNS and `@192.168.10.1` timed out during this audit; `dig +tcp` to `192.168.10.1` succeeded in about 1 ms.
- `dscacheutil` and `curl` resolved and reached `example.com`, so macOS/browser resolution still worked.

Assumptions:

- The router or AdGuard network extension may be mediating DNS behavior.
- The DNSCrypt config is a dormant candidate, not the active path.
- IPv6 is present only as local/utun routes in the observed route table, not as a normal external DNS path.

Unknowns:

- Whether `192.168.10.1` forwards to AdGuard Home, Unbound, DNSCrypt, ISP DNS, or another upstream.
- Whether UDP timeout is intentional firewall policy, router behavior, AdGuard filtering behavior, or transient network state.
- Whether Private Relay is enabled in the UI.

## Actual DNS Path Discovered

Observed path:

```text
macOS client
  -> vlan0 resolver 192.168.10.1
  -> router/upstream path unknown
  -> Internet
```

Not observed as active:

```text
macOS client -> local dnscrypt-proxy 127.0.0.1:53 -> upstream resolver
macOS client -> local Unbound -> dnscrypt-proxy -> upstream resolver
```

## Findings

| Area | Finding | Risk |
| --- | --- | --- |
| DNSCrypt | Config existed but the package/service was missing; fixed by installing and starting dnscrypt-proxy on `53530`. | AdGuard DNS Protection would fail if dnscrypt-proxy stops. |
| Local listener | Final listener is `127.0.0.1:53530`, matching AdGuard. | Port drift between AdGuard and dnscrypt-proxy would break filtered DNS. |
| UDP DNS | `dig` UDP queries timed out, while TCP DNS to router worked. | Some tools may experience delay/fallback behavior. |
| Cache | dnscrypt-proxy config has cache enabled, size `4096`, min TTL `2400`, max TTL `86400`. | Fine if active, irrelevant while inactive; high min TTL can keep stale answers longer. |
| Privacy filters | `require_nolog=true`, `require_nofilter=true`, `require_dnssec=false`, IPv6 upstreams disabled. | Privacy-focused, but DNSSEC is not required by dnscrypt-proxy. |
| Bootstrap | Bootstrap resolvers are `9.9.9.11:53` and `8.8.8.8:53`. | Plain bootstrap is normal for discovery but should be documented. |
| AdGuard | AdGuard app and network extension are running. | DNS filtering may be app-mediated and should not be bypassed accidentally. |

## Source Guidance

- DNSCrypt authenticates client-to-resolver DNS traffic and can be deployed by configuring clients to use a local proxy such as `127.0.0.1`; DNSCrypt also notes it is not a VPN and does not hide all hostname metadata.
- DNSCrypt documentation recommends combining DNSCrypt with a local caching resolver such as Unbound for performance and availability, with each component listening on distinct addresses or ports.
- Unbound documentation describes DNSSEC trust anchors and `qname-minimisation: yes` as part of a basic privacy-aware resolver configuration.
- RFC 9156 defines QNAME minimisation as a DNS privacy technique.
- AdGuard for Mac supports DNS filtering and native Apple Silicon builds, but the app/network-extension path should be audited from the app UI before replacing it.

## Recommended Changes

Do not change DNS automatically in this pass. The safe target architecture is:

```text
macOS network DNS
  -> 127.0.0.1:53
  -> local cache/filter layer, either AdGuard DNS filtering or Unbound
  -> dnscrypt-proxy on alternate local port
  -> privacy-focused DNSCrypt/DoH upstreams
```

Recommended implementation sequence:

1. Confirm AdGuard DNS filtering state and whether it should remain the front filter.
2. Decide one front door: AdGuard DNS filtering, Unbound, or dnscrypt-proxy standalone.
3. If using Unbound + DNSCrypt, run Unbound on `127.0.0.1:53` and dnscrypt-proxy on a non-privileged alternate local port, then forward Unbound to dnscrypt-proxy.
4. Require DNSSEC in exactly one layer, not blindly in both.
5. Lower dnscrypt-proxy `cache_min_ttl` from `2400` if stale records become a problem, especially for dev services.
6. Validate UDP and TCP DNS separately before changing macOS DNS.
7. Only after validation, set the active macOS service DNS to `127.0.0.1`.

## Implementation

No DNS implementation change was made because the active path does not currently use local DNSCrypt and the local resolver was not confirmed healthy.

## Validation Commands

```bash
scutil --dns
dig +time=2 +tries=1 example.com
dig +tcp +time=3 +tries=1 example.com
dig +time=2 +tries=1 @127.0.0.1 example.com
brew services list | rg -i 'dnscrypt|unbound|nextdns|dnsmasq'
ps -axo pid,command | rg -i 'dnscrypt|unbound|adguard|nextdns|dnsmasq'
```

## Rollback

If a future DNS change breaks resolution:

```bash
networksetup -setdnsservers "Home10" Empty
networksetup -setdnsservers "Wi-Fi" Empty
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

Then restore the previous resolver path to `192.168.10.1` if DHCP does not repopulate it.
