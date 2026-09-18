#!/bin/bash

#
# macOS Wireless Auto-Switch Utility
# Automatically toggles WiFi off when a physical wired connection is detected
# and back on when disconnected. Supports Sonoma and later releases.
#
# Requirements: Root privileges, macOS 14+, Bash 3.2+
# Usage: Executed automatically by LaunchDaemon on network configuration changes
#

set -euo pipefail  # Exit on error, undefined variables, and pipe failures

# Constants
readonly SCRIPT_NAME="wireless.sh"
readonly MINIMUM_DARWIN_MAJOR=23  # macOS Sonoma
readonly TESTED_DARWIN_MAJOR=27   # macOS Golden Gate
readonly DISCOVERY_ATTEMPTS="${AUTOSWITCH_DISCOVERY_ATTEMPTS:-3}"
readonly DISCOVERY_DELAY="${AUTOSWITCH_DISCOVERY_DELAY:-2}"
readonly SETTLE_ATTEMPTS="${AUTOSWITCH_SETTLE_ATTEMPTS:-6}"
readonly SETTLE_DELAY="${AUTOSWITCH_SETTLE_DELAY:-5}"
readonly WIFI_VERIFY_ATTEMPTS="${AUTOSWITCH_WIFI_VERIFY_ATTEMPTS:-6}"
readonly WIFI_VERIFY_DELAY="${AUTOSWITCH_WIFI_VERIFY_DELAY:-2}"
readonly WIFI_RECOVERY_ATTEMPTS="${AUTOSWITCH_WIFI_RECOVERY_ATTEMPTS:-12}"
readonly WIFI_RECOVERY_DELAY="${AUTOSWITCH_WIFI_RECOVERY_DELAY:-5}"

readonly NETWORKSETUP_BIN="${NETWORKSETUP_BIN:-/usr/sbin/networksetup}"
readonly DATE_BIN="${DATE_BIN:-/bin/date}"
readonly IFCONFIG_BIN="${IFCONFIG_BIN:-/sbin/ifconfig}"
readonly LOGGER_BIN="${LOGGER_BIN:-/usr/bin/logger}"
readonly ROUTE_BIN="${ROUTE_BIN:-/sbin/route}"
readonly SLEEP_BIN="${SLEEP_BIN:-/bin/sleep}"
readonly UNAME_BIN="${UNAME_BIN:-/usr/bin/uname}"

# Global variables
IPFOUND=""
OSVERSION=""
WIREDINTERFACES=""
WIFIINTERFACES=""
LINKFOUND=""

#
# Log message to system log with script context
# Arguments: $1 - log message
#
log_message() {
    local message="$1"
    local timestamp
    timestamp=$("$DATE_BIN" -u '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || true)
    "$LOGGER_BIN" "${SCRIPT_NAME}: ${message}" 2>/dev/null || true
    echo "${timestamp:-unknown-time} ${SCRIPT_NAME}: ${message}"
}

#
# Get the current macOS version number
# Returns: OS version number (23, 24, 25, etc.)
#
get_os_version() {
    "$UNAME_BIN" -r | awk -F. '{print $1}'
}

#
# Validate the Darwin major version without breaking every future macOS update.
# Versions newer than the latest tested release continue with a warning.
# Arguments: $1 - Darwin major version
#
validate_os_version() {
    local os_version="$1"

    if [[ ! "$os_version" =~ ^[0-9]+$ ]]; then
        log_message "ERROR: Unable to determine Darwin major version: ${os_version:-empty}"
        return 1
    fi

    if (( os_version < MINIMUM_DARWIN_MAJOR )); then
        log_message "ERROR: Unsupported Darwin version $os_version; macOS Sonoma or later is required"
        return 1
    fi

    if (( os_version > TESTED_DARWIN_MAJOR )); then
        log_message "WARNING: Darwin $os_version is newer than tested Darwin $TESTED_DARWIN_MAJOR; continuing with runtime interface discovery"
    fi

    return 0
}

#
# Return enabled network-service device identifiers.
#
get_enabled_service_interfaces() {
    "$NETWORKSETUP_BIN" -listnetworkserviceorder | \
        awk '
            /^\(\*\)/ { disabled = 1; next }
            /^\([0-9]+\)/ { disabled = 0; next }
            /^\(Hardware Port:/ && !disabled {
                device = $0
                sub(/^.*Device: /, "", device)
                sub(/\).*$/, "", device)
                if (device != "") printf "%s ", device
            }
        '
}

#
# Return all network-service device identifiers, including disabled services.
# WiFi discovery uses this so it can find a powered-off radio without relying on
# a localized service or hardware-port name.
#
get_all_service_interfaces() {
    "$NETWORKSETUP_BIN" -listnetworkserviceorder | \
        awk '
            /^\(Hardware Port:/ {
                device = $0
                sub(/^.*Device: /, "", device)
                sub(/\).*$/, "", device)
                if (device != "") printf "%s ", device
            }
        '
}

#
# Return device identifiers from real hardware-port records. The parser only
# accepts a Device line immediately following a Hardware Port line, so virtual
# configuration sections are not candidates.
#
get_hardware_interfaces() {
    "$NETWORKSETUP_BIN" -listallhardwareports | \
        awk '
            /^Hardware Port: / { expect_device = 1; next }
            expect_device && /^Device: / {
                printf "%s ", $2
                expect_device = 0
                next
            }
            { expect_device = 0 }
        '
}

#
# Return the interface class reported by the current macOS network driver.
# Arguments: $1 - interface identifier
#
get_interface_type() {
    local interface="$1"
    "$IFCONFIG_BIN" -v "$interface" 2>/dev/null | \
        awk -F ': ' '/^[[:space:]]*type: / {print $2; exit}' || true
}

#
# Return enabled service devices whose live driver class is physical Ethernet.
# This does not depend on a dock vendor, service, port, interface, or VLAN name.
# Returns: Space-separated list of physical wired interface identifiers.
#
get_wired_interfaces() {
    local enabled_interfaces
    local hardware_interfaces
    local wired_interfaces=""
    local interface

    enabled_interfaces=$(get_enabled_service_interfaces)
    hardware_interfaces=$(get_hardware_interfaces)

    for interface in $enabled_interfaces; do
        [[ " $hardware_interfaces " == *" $interface "* ]] || continue
        local interface_type
        interface_type=$(get_interface_type "$interface")
        [[ "$interface_type" == *Ethernet ]] || continue

        if [[ " $wired_interfaces " != *" $interface "* ]]; then
            wired_interfaces+="$interface "
        fi
    done

    echo "${wired_interfaces% }"
}

#
# Get list of WiFi interfaces
# Returns: Space-separated list of WiFi interface names  
#
get_wifi_interfaces() {
    local service_interfaces
    local hardware_interfaces
    local wifi_interfaces=""
    local interface

    service_interfaces=$(get_all_service_interfaces)
    hardware_interfaces=$(get_hardware_interfaces)
    for interface in $service_interfaces; do
        [[ " $hardware_interfaces " == *" $interface "* ]] || continue
        if [[ "$(get_interface_type "$interface")" == "Wi-Fi" ]]; then
            wifi_interfaces+="$interface "
        fi
    done

    echo "${wifi_interfaces% }"
}

#
# Check if a network interface has a valid IP address
# Arguments: $1 - interface name
# Returns: IP address if valid, empty string otherwise
#
get_interface_status() {
    local interface="$1"

    "$IFCONFIG_BIN" "$interface" 2>/dev/null | awk '/status:/ {print $2; exit}' || true
}

#
# Check whether an interface is actively linked
# Arguments: $1 - interface name
# Returns: 0 if active, 1 otherwise
#
is_interface_active() {
    local interface="$1"

    if [[ -z "$interface" ]]; then
        return 1
    fi

    local interface_dump
    interface_dump=$("$IFCONFIG_BIN" "$interface" 2>/dev/null || true)

    if [[ -z "$interface_dump" ]]; then
        return 1
    fi

    local status
    status=$(printf '%s\n' "$interface_dump" | awk '/status:/ {print $2; exit}')

    # Prefer explicit link status when available.
    if [[ -n "$status" ]]; then
        [[ "$status" == "active" ]] || return 1
    else
        # Some physical interfaces do not expose a status line.
        printf '%s\n' "$interface_dump" | head -1 | grep -q 'RUNNING' || return 1
    fi

    return 0
}

get_interface_ip() {
    local interface="$1"
    
    if [[ -z "$interface" ]]; then
        echo ""
        return 0
    fi
    
    if ! is_interface_active "$interface"; then
        echo ""
        return 0
    fi

    # Get IP address, excluding loopback and self-assigned addresses
    local ip_result
    ip_result=$("$IFCONFIG_BIN" "$interface" 2>/dev/null | \
        grep -E 'inet [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | \
        grep -E -v '127\.0\.0\.1|169\.254\.' | \
        awk '{print $2}' | \
        head -1 2>/dev/null || true)
    
    echo "$ip_result"
}

#
# Refresh interface discovery. This is repeated while a dock is settling so a
# renamed or late-arriving physical dock interface is picked up without restart.
#
refresh_interfaces() {
    WIREDINTERFACES=$(get_wired_interfaces)
    WIFIINTERFACES=$(get_wifi_interfaces)

    log_message "Detected physical wired interfaces: ${WIREDINTERFACES:-none}"
    log_message "Detected WiFi interfaces: ${WIFIINTERFACES:-none}"
}

#
# Check if any physical wired interface has a valid IP address. If carrier is
# present but DHCP is still settling, retry a bounded number of times and
# rediscover interfaces on every pass.
# Sets global IPFOUND and LINKFOUND variables to "true" when found.
#
detect_wired_connection() {
    local attempt=1
    local discovery_attempt=1

    IPFOUND=""
    LINKFOUND=""

    log_message "Starting physical wired connection detection..."

    # Golden Gate can emit a configuration event before a dock driver finishes
    # publishing its service and interface. Briefly rediscover an entirely empty
    # candidate set. A present-but-inactive physical interface still takes the
    # immediate undock path below.
    while (( discovery_attempt <= DISCOVERY_ATTEMPTS )); do
        refresh_interfaces
        if [[ -n "$WIREDINTERFACES" ]]; then
            break
        fi

        if (( discovery_attempt < DISCOVERY_ATTEMPTS )); then
            log_message "No physical wired interface published yet; rediscovering after ${DISCOVERY_DELAY}s"
            "$SLEEP_BIN" "$DISCOVERY_DELAY"
        fi
        ((discovery_attempt += 1))
    done

    if [[ -z "$WIREDINTERFACES" ]]; then
        log_message "No enabled physical wired interfaces detected"
        return 0
    fi

    while (( attempt <= SETTLE_ATTEMPTS )); do
        refresh_interfaces
        LINKFOUND=""

        if [[ -z "$WIREDINTERFACES" ]]; then
            log_message "Physical wired interface disappeared during settle; treating as undocked"
            return 0
        fi

        log_message "Checking physical wired interfaces (attempt $attempt/$SETTLE_ATTEMPTS): $WIREDINTERFACES"

        local interface
        for interface in $WIREDINTERFACES; do
            local interface_status
            interface_status=$(get_interface_status "$interface" || true)
            log_message "Interface status for $interface: ${interface_status:-unknown}"

            if is_interface_active "$interface"; then
                LINKFOUND="true"
            fi

            local ip_address
            ip_address=$(get_interface_ip "$interface" || true)

            if [[ -n "$ip_address" ]]; then
                IPFOUND="true"
                log_message "Active physical wired connection detected on interface $interface with IP $ip_address"
                return 0
            fi

            log_message "No usable IP found on interface $interface"
        done

        if [[ -z "$LINKFOUND" ]]; then
            log_message "No active physical wired links detected"
            return 0
        fi

        if (( attempt < SETTLE_ATTEMPTS )); then
            log_message "Wired link is present but not ready; rediscovering after ${SETTLE_DELAY}s"
            "$SLEEP_BIN" "$SETTLE_DELAY"
        fi
        ((attempt += 1))
    done

    log_message "Wired link remained without a usable IP after $SETTLE_ATTEMPTS attempts"
}

#
# Toggle WiFi state based on wired connection status
# Arguments: $1 - desired state ("on" or "off")
#
toggle_wifi() {
    local desired_state="$1"
    
    if [[ -z "$WIFIINTERFACES" ]]; then
        log_message "No WiFi interfaces found - skipping WiFi toggle"
        return 0
    fi
    
    if [[ "$desired_state" != "on" && "$desired_state" != "off" ]]; then
        log_message "ERROR: Invalid WiFi state '$desired_state'. Must be 'on' or 'off'"
        return 1
    fi
    
    local interface
    local desired_label
    local failed=""
    desired_label="$(tr '[:lower:]' '[:upper:]' <<< "${desired_state:0:1}")${desired_state:1}"

    for interface in $WIFIINTERFACES; do
        local current_state
        current_state=$("$NETWORKSETUP_BIN" -getairportpower "$interface" 2>/dev/null | awk '{print tolower($NF)}' || true)

        if [[ "$current_state" == "$desired_state" ]]; then
            log_message "WiFi already $desired_label on interface $interface - no change needed"
            continue
        fi

        if ! "$NETWORKSETUP_BIN" -setairportpower "$interface" "$desired_state"; then
            log_message "ERROR: Failed to set WiFi power to $desired_state on interface $interface"
            failed="true"
            continue
        fi

        local attempt
        local verified=""
        for ((attempt = 1; attempt <= WIFI_VERIFY_ATTEMPTS; attempt += 1)); do
            current_state=$("$NETWORKSETUP_BIN" -getairportpower "$interface" 2>/dev/null | awk '{print tolower($NF)}' || true)
            if [[ "$current_state" == "$desired_state" ]]; then
                verified="true"
                break
            fi
            "$SLEEP_BIN" "$WIFI_VERIFY_DELAY"
        done

        if [[ -z "$verified" ]]; then
            log_message "ERROR: WiFi power did not reach $desired_state on interface $interface after $WIFI_VERIFY_ATTEMPTS attempts"
            failed="true"
            continue
        fi

        log_message "Successfully turned $desired_state WiFi on interface $interface"
    done

    [[ -z "$failed" ]]
}

#
# Wait for WiFi to reacquire an address and the default route after undocking.
# A periodic launchd fallback will retry if macOS association takes longer.
#
wait_for_wifi_recovery() {
    local attempt

    for ((attempt = 1; attempt <= WIFI_RECOVERY_ATTEMPTS; attempt += 1)); do
        WIFIINTERFACES=$(get_wifi_interfaces)

        local default_interface
        default_interface=$("$ROUTE_BIN" -n get default 2>/dev/null | awk '/interface:/ {print $2; exit}' || true)

        local interface
        for interface in $WIFIINTERFACES; do
            local ip_address
            ip_address=$(get_interface_ip "$interface" || true)
            if [[ -n "$ip_address" && "$default_interface" == "$interface" ]]; then
                log_message "WiFi connectivity recovered on $interface with IP $ip_address and the default route"
                return 0
            fi
        done

        if (( attempt < WIFI_RECOVERY_ATTEMPTS )); then
            log_message "Waiting for WiFi address/default route recovery (attempt $attempt/$WIFI_RECOVERY_ATTEMPTS)"
            "$SLEEP_BIN" "$WIFI_RECOVERY_DELAY"
        fi
    done

    log_message "WARNING: WiFi power is on but address/default route recovery was not observed; launchd will retry"
    return 0
}

#
# Main execution logic
#
main() {
    log_message "Starting network detection and WiFi management"
    
    # Get system information
    OSVERSION=$(get_os_version)
    log_message "Detected macOS version: $OSVERSION"
    
    validate_os_version "$OSVERSION" || return 1
    
    # Detect wired connection status
    detect_wired_connection
    
    # Manage WiFi state based on wired connection
    if [[ -n "$IPFOUND" ]]; then
        toggle_wifi "off" || return 1
        log_message "WiFi disabled due to active physical wired connection"
    else
        toggle_wifi "on" || return 1
        log_message "WiFi enabled due to no active physical wired connection"
        wait_for_wifi_recovery
    fi

    log_message "Network detection and WiFi management completed successfully"
}

# Execute main function if script is run directly
if [[ "${BASH_SOURCE[0]:-}" == "${0}" ]]; then
    main "$@"
fi
