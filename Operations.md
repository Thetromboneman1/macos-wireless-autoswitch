# Operations

## Start

./install.sh i

## Validate

```bash
sudo launchctl print system/com.computernetworkbasics.wifionoff
/bin/bash -c 'source /Library/Scripts/NetBasics/wireless.sh; for wifi_device in $(get_wifi_interfaces); do /usr/sbin/networksetup -getairportpower "$wifi_device"; done'
route -n get default
tail -50 /var/log/wireless-autoswitch.log
```

When docked, the physical wired interface should own the default route and Wi-Fi
should be off. When undocked, Wi-Fi should turn on, reacquire an address, and own
the default route. The daemon runs at load, on SystemConfiguration changes, and
every 60 seconds as a recovery fallback.

## Golden Gate Recovery

macOS Golden Gate reports Darwin major version 27. Older releases of this
project used an exact Darwin 23–25 allowlist, so every launchd run exited before
checking the dock. Update the installation with:

```bash
./install.sh up
```

Current versions require Sonoma or later and warn, but continue, on a future
Darwin major version. Interface compatibility is decided by hardware-port
membership, live driver type, enabled-service state, link, address, and route
state instead of a brittle version or adapter-name list. A short publication
grace catches drivers that appear just after the launchd event; a separate
bounded window handles DHCP. Tagged VLAN and bridge virtual interfaces are
intentionally excluded.

## DNS Safety

The automation never calls a DNS configuration command. Existing DHCP DNS,
custom DNS, AdGuard, Control D, and dnscrypt-proxy settings are outside its
write scope and should be verified before and after any live transition test.

## Maintenance

- Keep dependencies and scripts up to date.
- Re-run validation after configuration changes.
- Keep rollback references current before destructive changes.

## Platform Boundary

Local AI platform operations now live in `/Users/corn/Documents/Boneman_Projects`.
Do not add model-serving, model-residency, agent-platform, or Apple Container
pilot automation back to this repository.
