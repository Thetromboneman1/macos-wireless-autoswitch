#!/bin/bash
set -euo pipefail

PLIST_LABEL="local.macos-wireless-autoswitch.fork-sync"
PLIST_SOURCE="/Users/corn/Documents/Corn_Automation/macos-wireless-autoswitch/local.macos-wireless-autoswitch.fork-sync.plist"
PLIST_TARGET="$HOME/Library/LaunchAgents/$PLIST_LABEL.plist"
UID_VALUE=$(id -u)

mkdir -p "$HOME/Library/LaunchAgents"
cp "$PLIST_SOURCE" "$PLIST_TARGET"

launchctl bootout "gui/$UID_VALUE/$PLIST_LABEL" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$UID_VALUE" "$PLIST_TARGET"
launchctl enable "gui/$UID_VALUE/$PLIST_LABEL"
launchctl kickstart -k "gui/$UID_VALUE/$PLIST_LABEL"

echo "Installed $PLIST_LABEL"
echo "Log file: /tmp/macos-wireless-autoswitch-fork-sync.log"
