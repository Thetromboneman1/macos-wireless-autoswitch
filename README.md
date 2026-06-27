# macOS Wireless Auto-Switch

Automatically disable Wi-Fi when a wired or VLAN virtual connection is active, then restore Wi-Fi when all wired/VLAN links disconnect.

## What This Repo Contains

- `wireless.sh`: core detection and Wi-Fi toggle logic.
- `com.computernetworkbasics.wifionoff.plist`: launchd daemon that watches macOS network state.
- `install.sh`: install, update, and uninstall helper.
- `docs/`: wireless automation notes plus small compatibility redirects for platform content now owned by Boneman_Projects.

## Supported Platforms

- macOS Sonoma (14.x)
- macOS Sequoia (15.x)
- macOS Tahoe (16.x)

## Quick Start

```bash
git clone https://github.com/locus313/macos-wireless-autoswitch.git
cd macos-wireless-autoswitch
./install.sh i
```

## Daily Commands

```bash
# install
./install.sh i

# update
./install.sh up

# uninstall
./install.sh ui

# menu mode
./install.sh
```

## Validate Installation

```bash
sudo launchctl list | grep com.computernetworkbasics.wifionoff
sudo /Library/Scripts/NetBasics/wireless.sh
networksetup -getairportpower Wi-Fi
```

## Troubleshooting

```bash
# restart daemon
sudo launchctl unload /Library/LaunchDaemons/com.computernetworkbasics.wifionoff.plist
sudo launchctl load /Library/LaunchDaemons/com.computernetworkbasics.wifionoff.plist

# list hardware ports
networksetup -listallhardwareports
```

## Fork Sync CI (Maintainers)

The fork sync workflow (`.github/workflows/fork-sync.yml`) runs every 30 minutes and is safe to trigger manually from the Actions tab.

- Checkout auth is not persisted globally.
- Push auth is scoped to `origin` only.
- Upstream fetch runs anonymously with retries to reduce intermittent credential prompt failures.
- Transient runner/network issues are tolerated so the next schedule can self-heal.

## Project Notes

- Uses hardware-port detection for Ethernet, LAN, Thunderbolt, AX88179A, and VLAN adapters.
- Includes VLAN virtual interfaces (for example `vlan10`) when deciding whether Wi-Fi should be disabled.
- Ignores loopback and self-assigned IP ranges when deciding wired status.
- Requires admin privileges for system-level network changes.
- AdGuard LocalDNSCrypt is documented in `docs/network/adguard-dnscrypt-setup.md`.
- Local AI, model residency, platform governance, agent-platform, Apple Container pilot, and AI tooling docs are canonical in `/Users/corn/Documents/Boneman_Projects` and `https://github.com/Thetromboneman1/Boneman_Projects`.

## License

MIT. See `LICENSE`.
