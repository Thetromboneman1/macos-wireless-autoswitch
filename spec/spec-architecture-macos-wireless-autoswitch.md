---
title: Architecture Specification - macOS Wireless Auto-Switch Utility
version: 1.2
date_created: 2025-09-14
last_updated: 2026-09-18
owner: System Architecture Team
tags: [architecture, macos, networking, launchd, system-utility, automation]
---

# Introduction

This specification defines the architecture, requirements, and implementation guidelines for the macOS Wireless Auto-Switch utility - a system service that automatically manages WiFi connectivity based on dynamically discovered physical wired adapter status. The utility ignores tagged VLAN and other virtual adapters.

## 1. Purpose & Scope

### Purpose
Define the complete architecture and requirements for a macOS system utility that automatically toggles WiFi connectivity based on active physical wired network connections without depending on a dock name, service name, vendor, interface number, or VLAN tag.

### Scope
- **In Scope**: Network interface detection, WiFi state management, system service integration, installation/management tooling, macOS compatibility (Sonoma 14.x, Sequoia 15.x, Tahoe 16.x)
- **Out of Scope**: GUI applications, network configuration management beyond WiFi toggle, third-party network managers, cross-platform support
- **Target Audience**: System administrators, developers maintaining macOS network automation tools, DevOps engineers
- **Assumptions**: Administrator privileges available, standard macOS networking stack, bash shell environment

## 2. Definitions

- **LaunchDaemon**: macOS system service that runs with root privileges and starts automatically at boot
- **NetworkSetup**: macOS command-line utility for network configuration management
- **Hardware Port**: Physical network interface identifier in macOS network configuration
- **Airport Power**: macOS WiFi radio state (on/off) controlled via networksetup command
- **System Configuration**: macOS framework for network and system state monitoring located at `/Library/Preferences/SystemConfiguration`
- **Self-Assigned Address**: IPv4 address in 169.254.x.x range assigned when DHCP fails
- **Physical Wired Interface**: An enabled macOS network-service device present in a real hardware-port record whose live driver class ends in `Ethernet` and has active carrier plus a usable IP address

## 3. Requirements, Constraints & Guidelines

### Functional Requirements
- **REQ-001**: System shall detect active physical wired network services with valid IP addresses
- **REQ-002**: System shall automatically disable WiFi when a physical wired connection is active
- **REQ-003**: System shall automatically enable WiFi when no physical wired connection is active
- **REQ-004**: System shall discover dock adapters through hardware-record membership and live driver class without hardcoded service, port, vendor, interface, or VLAN names
- **REQ-005**: System shall ignore loopback (127.0.0.1) and self-assigned (169.254.x.x) IP addresses
- **REQ-006**: System shall respond to network configuration changes in real-time
- **REQ-007**: System shall provide comprehensive installation and management tooling
- **REQ-008**: System shall briefly retry an empty candidate set to catch a dock driver published after the launchd event

### Performance Requirements
- **PERF-001**: Immediate link-state detection shall complete promptly; driver publication may use a bounded 4-second grace and active carrier awaiting DHCP may use a bounded 30-second settle window
- **PERF-002**: WiFi toggle operations shall complete within 10 seconds
- **PERF-003**: Periodic reconciliation shall remain bounded and idempotent

### Security Requirements
- **SEC-001**: System shall require administrator privileges for installation and execution
- **SEC-002**: System shall use absolute paths for all system commands
- **SEC-003**: System shall validate input parameters and exit with appropriate error codes
- **SEC-004**: Scripts shall be owned by root with appropriate execution permissions

### Compatibility Requirements
- **COMP-001**: System shall support macOS Sonoma (Darwin 23) and later, including Golden Gate (Darwin 27), while warning and continuing on newer Darwin majors
- **COMP-002**: System shall remain compatible with the macOS system Bash 3.2 runtime
- **COMP-003**: System shall integrate with standard macOS networking utilities

### Operational Constraints
- **CON-001**: System must run with root privileges for network configuration access
- **CON-002**: System files must be installed in standard macOS system directories
- **CON-003**: System shall not interfere with user manual network configuration
- **CON-004**: System shall provide logging integration with macOS system logs

### Development Guidelines
- **GUD-001**: Use explicit error handling with appropriate exit codes
- **GUD-002**: Implement comprehensive logging for debugging and monitoring
- **GUD-003**: Follow macOS system service best practices for LaunchDaemon configuration
- **GUD-004**: Maintain backward compatibility within supported macOS versions

### Architecture Patterns
- **PAT-001**: Use network-change monitoring for fast response plus periodic reconciliation for missed or race-prone events
- **PAT-002**: Implement idempotent operations for safe repeated execution
- **PAT-003**: Separate concerns between detection logic and configuration management
- **PAT-004**: Use declarative configuration for LaunchDaemon properties

## 4. Interfaces & Data Contracts

### Command Line Interface
```bash
# Installation script interface
./install.sh [i|up|ui]
# i  = install system components
# up = update existing installation  
# ui = uninstall system components
```

### System Integration Points
| Component | Interface | Purpose |
|-----------|-----------|---------|
| networksetup | `/usr/sbin/networksetup -listnetworkserviceorder` | Enumerate network interfaces |
| networksetup | `/usr/sbin/networksetup -listallhardwareports` | Get WiFi interface identifiers |
| networksetup | `/usr/sbin/networksetup -setairportpower <interface> <on\|off>` | Control WiFi state |
| ifconfig | `ifconfig <interface>` | Query interface IP configuration |
| logger | `logger <message>` | System log integration |
| launchctl | `launchctl load/unload <plist>` | Service lifecycle management |

### File System Layout
```
/Library/Scripts/NetBasics/
├── wireless.sh                    # Core detection and toggle logic
└── install.sh                     # Installation management script

/Library/LaunchDaemons/
└── com.computernetworkbasics.wifionoff.plist  # Service configuration

/var/log/system.log                 # System logging destination
```

### LaunchDaemon Configuration Schema
```xml
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.computernetworkbasics.wifionoff</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Library/Scripts/NetBasics/wireless.sh</string>
    </array>
    <key>WatchPaths</key>
    <array>
        <string>/Library/Preferences/SystemConfiguration</string>
    </array>
</dict>
</plist>
```

## 5. Acceptance Criteria

### Network Detection
- **AC-001**: Given multiple renamed network interfaces, When an enabled physical wired device has active carrier and a valid IP address, Then system shall detect the wired connection without a name mapping
- **AC-002**: Given a physical wired interface with self-assigned IP (169.254.x.x), When evaluating connection status, Then system shall treat it as inactive
- **AC-003**: Given tagged, bridge, WiFi, disabled, and physical wired services, Then only enabled devices whose driver class ends in `Ethernet` shall be wired candidates

### WiFi State Management  
- **AC-004**: Given an active physical wired connection, When WiFi is currently enabled, Then system shall disable WiFi and log action
- **AC-005**: Given no active physical wired connection, When WiFi is currently disabled, Then system shall enable WiFi and log action
- **AC-006**: Given WiFi state change command fails, When executing networksetup command, Then system shall exit with error code 1

### System Integration
- **AC-007**: Given network configuration changes, When SystemConfiguration directory is modified, Then LaunchDaemon shall trigger script execution within 5 seconds
- **AC-008**: Given repeated triggers, When the requested WiFi state is already correct, Then system shall perform no state write
- **AC-009**: Given system startup, When LaunchDaemon loads, Then service shall start automatically without user intervention

### Installation Process
- **AC-010**: Given installation command executed, When install script runs with 'i' parameter, Then all system files shall be copied and permissions set correctly
- **AC-011**: Given uninstall command executed, When install script runs with 'ui' parameter, Then all system files shall be removed and service stopped
- **AC-012**: Given update command executed, When install script runs with 'up' parameter, Then existing files shall be replaced and service restarted

## 6. Test Automation Strategy

### Test Levels
- **Unit Testing**: Shell script function validation using bash test framework
- **Integration Testing**: Network interface detection with mocked system commands
- **System Testing**: End-to-end validation on target macOS versions
- **Compatibility Testing**: Cross-version validation on Sonoma and later releases

### Testing Frameworks
- **Shell Testing**: Bash Automated Testing System (BATS) for script validation
- **Mock Testing**: Custom mocking for networksetup and ifconfig commands
- **System Testing**: GitHub Actions with macOS runners for automated validation
- **Manual Testing**: Physical hardware validation with multiple adapter types

### Test Data Management
- **Network Mocking**: Predefined interface configurations for consistent testing
- **IP Address Scenarios**: Valid, invalid, self-assigned, and loopback address sets
- **Hardware Simulation**: Mock data with renamed physical devices, disabled services, WiFi, bridges, and tagged virtual devices

### CI/CD Integration
- **Automated Testing**: GitHub Actions workflow with macOS matrix builds
- **Syntax Validation**: ShellCheck integration for static analysis
- **Security Scanning**: Automated vulnerability assessment for shell scripts
- **Documentation Validation**: Automated README and specification consistency checks

### Coverage Requirements
- **Script Coverage**: 100% line coverage for core wireless.sh logic
- **Scenario Coverage**: All supported hardware adapter types and IP configurations
- **Error Handling**: All error conditions and exit codes validated
- **Integration Points**: All system command interactions tested with mocks

### Performance Testing
- **Response Time**: Network change detection and WiFi toggle performance measurement
- **Resource Usage**: Memory and CPU utilization monitoring during operation
- **Stress Testing**: Rapid network state changes and concurrent execution scenarios

## 7. Rationale & Context

### Architecture Decisions

#### LaunchDaemon vs LaunchAgent
**Decision**: Use LaunchDaemon for system-level network monitoring
**Rationale**: Requires root privileges for networksetup commands and must operate regardless of user login status

#### File System Monitoring and Reconciliation
**Decision**: Monitor `/Library/Preferences/SystemConfiguration` for fast response and reconcile every 60 seconds
**Rationale**: macOS documents `WatchPaths` as race-prone; bounded periodic reconciliation recovers missed dock and wake events

#### Shell Script vs Compiled Binary
**Decision**: Implement core logic in Bash shell script
**Rationale**: Simplifies maintenance, leverages existing macOS command-line tools, and provides transparency for security auditing

#### Hardware Port Detection Strategy
**Decision**: Use `networksetup -listnetworkserviceorder` with hardware port filtering
**Rationale**: Provides reliable identification of physical interfaces across different macOS versions and hardware configurations

### Design Trade-offs

#### Performance vs Reliability
- **Trade-off**: 10-second sleep delay after execution
- **Rationale**: Prevents LaunchDaemon restart loops at cost of slight delay in rapid network changes

#### Physical Hardware vs Virtual Configuration
- **Trade-off**: Only enabled services backed by the physical hardware-port inventory qualify as dock Ethernet
- **Rationale**: Live driver classification survives service, port, and interface renames while excluding unreliable virtual adapters

#### Security vs Usability
- **Trade-off**: Requires sudo privileges for installation
- **Rationale**: System-level network control necessitates administrative access

## 8. Dependencies & External Integrations

### macOS System Dependencies
- **SYS-001**: macOS networksetup utility - Network interface configuration and control
- **SYS-002**: macOS ifconfig utility - Network interface status and IP address query
- **SYS-003**: macOS launchctl utility - Service lifecycle management
- **SYS-004**: macOS logger utility - System log integration
- **SYS-005**: Bash shell environment - Script execution runtime

### System Framework Dependencies
- **FWK-001**: SystemConfiguration framework - Network state change monitoring
- **FWK-002**: Airport/WiFi framework - Wireless interface control via networksetup
- **FWK-003**: LaunchDaemon framework - System service execution environment

### Hardware Dependencies
- **HW-001**: Network interfaces - Any enabled physical wired device exposed by the active dock driver
- **HW-002**: WiFi capability - Wireless network interface for state management
- **HW-003**: Administrator access - User account with sudo privileges

### File System Dependencies
- **FS-001**: System directories - Write access to `/Library/Scripts/` and `/Library/LaunchDaemons/`
- **FS-002**: Configuration monitoring - Read access to `/Library/Preferences/SystemConfiguration`
- **FS-003**: System logging - Write access to system log facilities

### Network Dependencies
- **NET-001**: DHCP services - For valid IP address assignment to the physical wired interface
- **NET-002**: Network infrastructure - Physical dock network connectivity

### Version Dependencies
- **VER-001**: macOS Sonoma 14.x+ - Minimum supported operating system version
- **VER-002**: Bash 3.2+ - Compatible with the macOS system shell

## 9. Examples & Edge Cases

### Basic Network Detection Logic
```bash
# Discover enabled service devices, then classify each with ifconfig -v.
ENABLED_INTERFACES=$(networksetup -listnetworkserviceorder | \
    awk '/^\([0-9]+\)/ { disabled=0; next }
         /^\(\*\)/ { disabled=1; next }
         /^\(Hardware Port:/ && !disabled {
             device=$0; sub(/^.*Device: /,"",device); sub(/\).*$/,"",device)
             printf "%s ", device
         }')

for INTERFACE in $ENABLED_INTERFACES; do
    INTERFACE_TYPE=$(ifconfig -v "$INTERFACE" | \
        awk -F ': ' '/^[[:space:]]*type: / {print $2; exit}')
    [[ "$INTERFACE_TYPE" == *Ethernet ]] || continue
    IPCHECK=$(ifconfig "$INTERFACE" | \
        grep -E 'inet [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | \
        grep -E -v '127.0.0.1|169.254.' | \
        awk '{print $2}')
    if [ "$IPCHECK" ]; then
        IPFOUND=true
        break
    fi
done
```

### WiFi State Management
```bash
# Reuse the structural service + hardware-record + driver-class discovery.
source ./wireless.sh
WIFIINTERFACES=$(get_wifi_interfaces)

# Toggle WiFi based on physical wired connection status
if [[ -n "${IPFOUND:-}" ]]; then
    networksetup -setairportpower "$WIFIINTERFACES" off || exit 1
    logger "wireless.sh: turning off wireless card ($WIFIINTERFACES)"
else
    networksetup -setairportpower "$WIFIINTERFACES" on || exit 1
    logger "wireless.sh: turning on wireless card ($WIFIINTERFACES)"
fi
```

### Edge Cases

#### Multiple Wired Interfaces
- **Scenario**: System has multiple physical network devices and virtual tagged or bridge services
- **Behavior**: Detection ignores virtual devices and finds the first enabled physical interface with active carrier and a valid IP
- **Handling**: Loop through all interfaces, set IPFOUND=true on first valid IP

#### Rapid Network Changes
- **Scenario**: User frequently connects/disconnects a physical dock adapter
- **Behavior**: Each change triggers LaunchDaemon execution
- **Handling**: 10-second sleep prevents rapid cycling and system instability

#### No WiFi Interface
- **Scenario**: System has no wireless capability (desktop Mac Pro)
- **Behavior**: Script continues execution but WiFi commands fail silently
- **Handling**: Check for WiFi interface existence before state changes

#### Invalid IP Assignments
- **Scenario**: Physical wired interface gets self-assigned IP (169.254.x.x)
- **Behavior**: System treats it as no valid wired connection
- **Handling**: Explicit exclusion of 169.254.x.x range in IP detection

#### Permission Failures
- **Scenario**: Script runs without sufficient privileges
- **Behavior**: networksetup commands fail with permission errors
- **Handling**: Exit with error code 1 to signal LaunchDaemon failure

## 10. Validation Criteria

### Functional Validation
- **VAL-001**: Script identifies renamed enabled physical dock interfaces by live driver class and rejects tagged, bridge, WiFi, and disabled services
- **VAL-002**: WiFi toggle operations complete successfully across all supported macOS versions
- **VAL-003**: IP address filtering excludes loopback and self-assigned addresses correctly
- **VAL-004**: LaunchDaemon responds to network configuration changes within specified timeframes

### Performance Validation
- **VAL-005**: Network detection completes within 5-second requirement under normal conditions
- **VAL-006**: System operates without memory leaks during extended operation periods
- **VAL-007**: CPU utilization remains minimal during monitoring and execution cycles

### Integration Validation
- **VAL-008**: Installation script successfully deploys all components with correct permissions
- **VAL-009**: System logging integration captures all significant events and errors
- **VAL-010**: Uninstallation completely removes all system components without residue

### Security Validation
- **VAL-011**: All system commands use absolute paths to prevent PATH injection attacks
- **VAL-012**: Script validation detects and prevents execution of malformed commands
- **VAL-013**: File permissions prevent unauthorized modification of system components

### Compatibility Validation
- **VAL-014**: Solution operates correctly across Sonoma, Sequoia, and Tahoe macOS versions
- **VAL-015**: Hardware compatibility verified with various adapter types and configurations
- **VAL-016**: Script handles differences in command output formats across macOS versions

## 11. Related Specifications / Further Reading

- [CI/CD Workflow Specification - macOS Utility Validation](spec-process-cicd-macos-utility-validation.md)
- [Apple Developer Documentation - LaunchDaemon and LaunchAgent](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html)
- [macOS Network Configuration Guide](https://support.apple.com/guide/mac-help/mchlp2439/mac)
- [Bash Scripting Best Practices for System Administration](https://google.github.io/styleguide/shellguide.html)
- [macOS Security and Privacy Guidelines](https://support.apple.com/guide/security/welcome/web)
