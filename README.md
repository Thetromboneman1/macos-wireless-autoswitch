# macOS Wireless Auto-Switch

Automatically disable Wi-Fi when a wired or VLAN virtual connection is active, then restore Wi-Fi when all wired/VLAN links disconnect.

## What This Repo Contains

- `wireless.sh`: core detection and Wi-Fi toggle logic.
- `com.computernetworkbasics.wifionoff.plist`: launchd daemon that watches macOS network state.
- `install.sh`: install, update, and uninstall helper.
- `docs/`: implementation and architecture notes.

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

## Project Notes

- Uses hardware-port detection for Ethernet, LAN, Thunderbolt, AX88179A, and VLAN adapters.
- Includes VLAN virtual interfaces (for example `vlan10`) when deciding whether Wi-Fi should be disabled.
- Ignores loopback and self-assigned IP ranges when deciding wired status.
- Requires admin privileges for system-level network changes.

## License

MIT. See `LICENSE`.
