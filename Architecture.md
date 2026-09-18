# Architecture

## Purpose
Automatic Wi-Fi control based on dynamically discovered physical wired link
state on macOS via launchd. Virtual VLAN and bridge adapters are excluded.

## Core Components
- wireless.sh detection and Wi-Fi toggling
- install.sh lifecycle management
- launchd daemon plist for system monitoring

## Data Flow
~~~mermaid
flowchart LR
  Input[User or Automation Trigger] --> Logic[macos-wireless-autoswitch Logic]
  Logic --> State[Local Config or Runtime State]
  Logic --> Output[System Action or API Result]
  State --> Output
~~~
