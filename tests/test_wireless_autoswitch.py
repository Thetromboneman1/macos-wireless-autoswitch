from __future__ import annotations

import os
import plistlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "wireless.sh"


def run_bash(body: str, *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    command = f'source "{SCRIPT}"\n{body}'
    merged_env = os.environ.copy()
    merged_env.update(
        {
            "AUTOSWITCH_DISCOVERY_ATTEMPTS": "3",
            "AUTOSWITCH_DISCOVERY_DELAY": "0",
            "AUTOSWITCH_SETTLE_ATTEMPTS": "3",
            "AUTOSWITCH_SETTLE_DELAY": "0",
            "AUTOSWITCH_WIFI_VERIFY_ATTEMPTS": "2",
            "AUTOSWITCH_WIFI_VERIFY_DELAY": "0",
            "AUTOSWITCH_WIFI_RECOVERY_ATTEMPTS": "2",
            "AUTOSWITCH_WIFI_RECOVERY_DELAY": "0",
            "LOGGER_BIN": "/usr/bin/true",
            "SLEEP_BIN": "/usr/bin/true",
        }
    )
    if env:
        merged_env.update(env)
    return subprocess.run(
        ["/bin/bash", "-c", command],
        cwd=ROOT,
        env=merged_env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_golden_gate_and_future_versions_continue_but_legacy_fails() -> None:
    current = run_bash('validate_os_version 27; echo "status=$?"')
    future = run_bash('validate_os_version 28; echo "status=$?"')
    legacy = run_bash('validate_os_version 22; echo "status=$?"')

    assert current.returncode == 0
    assert "status=0" in current.stdout
    assert "newer than tested" in future.stdout
    assert "status=0" in future.stdout
    assert legacy.returncode == 1
    assert "macOS Sonoma or later is required" in legacy.stdout


def test_delayed_physical_interface_rename_is_rediscovered() -> None:
    result = run_bash(
        r'''
        refresh_count=0
        refresh_interfaces() {
            ((refresh_count += 1))
            if (( refresh_count == 1 )); then
                WIREDINTERFACES="wired_old"
            else
                WIREDINTERFACES="wired_new"
            fi
            WIFIINTERFACES="wifi_primary"
        }
        get_interface_status() { echo active; }
        is_interface_active() { return 0; }
        get_interface_ip() {
            if [[ "$1" == "wired_new" && "$refresh_count" -ge 2 ]]; then
                echo 192.0.2.10
            fi
        }
        detect_wired_connection
        echo "ipfound=$IPFOUND interfaces=$WIREDINTERFACES refreshes=$refresh_count"
        '''
    )

    assert result.returncode == 0, result.stderr
    assert "ipfound=true" in result.stdout
    assert "interfaces=wired_new" in result.stdout
    assert "refreshes=2" in result.stdout


def test_late_driver_publication_is_rediscovered() -> None:
    result = run_bash(
        r'''
        refresh_count=0
        refresh_interfaces() {
            ((refresh_count += 1))
            if (( refresh_count == 1 )); then
                WIREDINTERFACES=""
            else
                WIREDINTERFACES="wired_late"
            fi
            WIFIINTERFACES="wifi_primary"
        }
        get_interface_status() { echo active; }
        is_interface_active() { return 0; }
        get_interface_ip() { [[ "$1" == "wired_late" ]] && echo 192.0.2.30; }
        detect_wired_connection
        echo "ipfound=$IPFOUND interfaces=$WIREDINTERFACES refreshes=$refresh_count"
        ''',
    )

    assert result.returncode == 0, result.stderr
    assert "ipfound=true" in result.stdout
    assert "interfaces=wired_late" in result.stdout
    assert "refreshes=3" in result.stdout


def test_undock_without_active_carrier_does_not_wait() -> None:
    result = run_bash(
        r'''
        refresh_count=0
        refresh_interfaces() { ((refresh_count += 1)); WIREDINTERFACES="wired_primary"; WIFIINTERFACES="wifi_primary"; }
        get_interface_status() { echo inactive; }
        is_interface_active() { return 1; }
        get_interface_ip() { return 0; }
        detect_wired_connection
        echo "ipfound=${IPFOUND:-false} refreshes=$refresh_count"
        '''
    )

    assert result.returncode == 0, result.stderr
    assert "ipfound=false" in result.stdout
    assert "refreshes=2" in result.stdout


def test_wifi_toggle_is_idempotent_and_handles_each_interface(tmp_path: Path) -> None:
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    (state_dir / "wifi_primary").write_text("off")
    (state_dir / "wifi_secondary").write_text("on")
    command_log = tmp_path / "commands.log"
    mock_networksetup = tmp_path / "networksetup"
    mock_networksetup.write_text(
        """#!/bin/bash
set -euo pipefail
case "$1" in
  -getairportpower)
    state=$(cat "$STATE_DIR/$2")
    label=$(printf '%s' "$state" | awk '{print toupper(substr($0,1,1)) substr($0,2)}')
    printf 'Wi-Fi Power (%s): %s\\n' "$2" "$label"
    ;;
  -setairportpower)
    printf '%s %s\\n' "$2" "$3" >> "$COMMAND_LOG"
    printf '%s' "$3" > "$STATE_DIR/$2"
    ;;
  *) exit 2 ;;
esac
"""
    )
    mock_networksetup.chmod(0o755)

    result = run_bash(
        'WIFIINTERFACES="wifi_primary wifi_secondary"\ntoggle_wifi off',
        env={
            "NETWORKSETUP_BIN": str(mock_networksetup),
            "STATE_DIR": str(state_dir),
            "COMMAND_LOG": str(command_log),
        },
    )

    assert result.returncode == 0, result.stderr
    assert "WiFi already Off on interface wifi_primary" in result.stdout
    assert command_log.read_text().splitlines() == ["wifi_secondary off"]
    assert (state_dir / "wifi_secondary").read_text() == "off"


def test_wifi_recovery_accepts_address_and_default_route(tmp_path: Path) -> None:
    route = tmp_path / "route"
    route.write_text("#!/bin/bash\nprintf '   interface: wifi_primary\\n'\n")
    route.chmod(0o755)

    result = run_bash(
        r'''
        get_wifi_interfaces() { echo wifi_primary; }
        get_interface_ip() { echo 192.0.2.20; }
        wait_for_wifi_recovery
        ''',
        env={"ROUTE_BIN": str(route)},
    )

    assert result.returncode == 0, result.stderr
    assert "WiFi connectivity recovered on wifi_primary" in result.stdout


def test_wired_discovery_uses_enabled_physical_services_only(tmp_path: Path) -> None:
    mock_networksetup = tmp_path / "networksetup"
    mock_networksetup.write_text(
        """#!/bin/bash
case "$1" in
  -listallhardwareports)
    cat <<'EOF'
Hardware Port: Dock Network
Device: wired_dynamic

Hardware Port: Wi-Fi
Device: wifi_dynamic

Hardware Port: Thunderbolt Bridge
Device: bridge_dynamic

Virtual Configurations
======================
Device: virtual_tagged
EOF
    ;;
  -listnetworkserviceorder)
    cat <<'EOF'
(1) Any Dock Name
(Hardware Port: Dock Network, Device: wired_dynamic)
(2) Wi-Fi
(Hardware Port: Wi-Fi, Device: wifi_dynamic)
(3) Thunderbolt Bridge
(Hardware Port: Thunderbolt Bridge, Device: bridge_dynamic)
(4) Tagged Virtual Service
(Hardware Port: VLAN, Device: virtual_tagged)
(*) Disabled Physical Service
(Hardware Port: Other Dock, Device: wired_disabled)
EOF
    ;;
  *) exit 2 ;;
esac
"""
    )
    mock_networksetup.chmod(0o755)
    mock_ifconfig = tmp_path / "ifconfig"
    mock_ifconfig.write_text(
        """#!/bin/bash
if [[ "$1" != "-v" ]]; then exit 2; fi
case "$2" in
  wired_dynamic) printf '    type: USB Ethernet\n' ;;
  wifi_dynamic) printf '    type: Wi-Fi\n' ;;
  bridge_dynamic) printf '    type: Bridge\n' ;;
  virtual_tagged) printf '    type: VLAN\n' ;;
  wired_disabled) printf '    type: USB Ethernet\n' ;;
esac
"""
    )
    mock_ifconfig.chmod(0o755)

    result = run_bash(
        'printf "wired=%s wifi=%s\\n" "$(get_wired_interfaces)" "$(get_wifi_interfaces)"',
        env={
            "NETWORKSETUP_BIN": str(mock_networksetup),
            "IFCONFIG_BIN": str(mock_ifconfig),
        },
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "wired=wired_dynamic wifi=wifi_dynamic"


def test_networksetup_failure_is_reported(tmp_path: Path) -> None:
    mock_networksetup = tmp_path / "networksetup"
    mock_networksetup.write_text(
        """#!/bin/bash
if [[ "$1" == "-getairportpower" ]]; then
  printf 'Wi-Fi Power (%s): On\n' "$2"
  exit 0
fi
exit 1
"""
    )
    mock_networksetup.chmod(0o755)

    result = run_bash(
        'WIFIINTERFACES="wifi_primary"\nif toggle_wifi off; then echo unexpected; else echo failed; fi',
        env={"NETWORKSETUP_BIN": str(mock_networksetup)},
    )

    assert result.returncode == 0, result.stderr
    assert "Failed to set WiFi power to off" in result.stdout
    assert result.stdout.rstrip().endswith("failed")


def test_launchd_has_startup_and_periodic_reconciliation() -> None:
    plist = ROOT / "com.computernetworkbasics.wifionoff.plist"
    with plist.open("rb") as handle:
        launchd = plistlib.load(handle)

    assert launchd["RunAtLoad"] is True
    assert launchd["StartInterval"] == 60
    assert launchd["KeepAlive"] is False
    assert launchd["WatchPaths"] == ["/Library/Preferences/SystemConfiguration"]
