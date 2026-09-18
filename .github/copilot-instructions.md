# Copilot Instructions for macOS Wireless Auto-Switch

## Project Overview
This is a simple macOS utility that automatically toggles WiFi off when a wired Ethernet connection is detected, and back on when disconnected. The system uses a LaunchDaemon to monitor network configuration changes.

## Architecture Components

### Core Files
- `wireless.sh` - Main logic script that detects wired connections and toggles WiFi
- `com.computernetworkbasics.wifionoff.plist` - LaunchDaemon configuration that watches `/Library/Preferences/SystemConfiguration` for network changes
- `install.sh` - Installation/management script with interactive menu system

### Key Patterns

#### Network Detection Logic (`wireless.sh`)
- Parses enabled devices from `networksetup -listnetworkserviceorder`, intersects
  them with real hardware-port records, and classifies them with `ifconfig -v`
- Accepts live driver types ending in `Ethernet`; never hardcode a dock, service,
  vendor, interface number, port label, or VLAN tag
- Tagged VLAN, bridge, WiFi, disabled, and other virtual services are not dock Ethernet
- Uses `ifconfig` + `grep` to find valid IP addresses (excludes 127.0.0.1 and 169.254.x.x)
- OS version detection uses the Darwin major from `uname -r`; Sonoma and later
  are accepted, with warning-and-continue behavior for newer untested releases

#### Installation Structure
- Scripts install to `/Library/Scripts/NetBasics/`
- LaunchDaemon plist goes to `/Library/LaunchDaemons/`
- Requires root permissions for system-level network control

### Development Workflows

#### Testing Network Detection
```bash
# Use the same dynamic discovery functions as production
source ./wireless.sh
get_wired_interfaces
get_wifi_interfaces
```

#### Installation Commands
- Install: `./install.sh i`
- Update: `./install.sh up` 
- Uninstall: `./install.sh ui`

### macOS-Specific Considerations
- Uses `networksetup -setairportpower` for WiFi control (requires admin privileges)
- LaunchDaemon watches SystemConfiguration for network state changes
- Idempotent writes, bounded settle/recovery checks, and 60-second periodic
  reconciliation prevent loops and recover missed dock or wake events
- Logging via `logger` command integrates with system logs

### Error Handling Patterns
- Exit codes used for LaunchDaemon error detection (`|| exit 1`)
- Conditional logic ensures WiFi interfaces exist before control attempts
- Sudo detection and privilege escalation in install script

### Compatibility Notes
- Keep compatibility with the macOS system Bash 3.2 runtime
- Driver-class discovery must remain independent of adapter and interface names
- Runtime compatibility checks must not become a future OS-update kill switch

When modifying this codebase, always test network detection logic thoroughly and ensure LaunchDaemon integration works correctly with system network events.
