# 02 - DNSCrypt Audit

Canonical audit: [../network/dnscrypt-audit.md](../network/dnscrypt-audit.md)

## Decision

Do not change DNS automatically yet. The active macOS resolver path is router DNS at `192.168.10.1`, while local dnscrypt-proxy is configured but not active. UDP DNS timed out in `dig`, TCP DNS worked, and macOS resolver APIs still resolved names.

## Next Safe Step

Use the AdGuard UI and router admin UI to identify the upstream resolver behind `192.168.10.1`, then decide whether the front door should be AdGuard, Unbound, or dnscrypt-proxy.

