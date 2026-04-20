# DeathAdder V3 HyperSpeed - Implementation Plan

## Overview
This document outlines the detailed implementation milestones and testing requirements for adding DeathAdder V3 HyperSpeed support to razer-macos.

---

## Milestone Checklist

### Milestone 1: Project Setup & Research
- [ ] Fork razer-macos repository
- [ ] Set up local macOS development environment (Xcode, USB debugging tools)
- [ ] Install USB packet sniffing tools (Wireshark + USBPcap or similar)
- [ ] Document existing razer-macos architecture
- [ ] Obtain DeathAdder V3 HyperSpeed hardware for testing

### Milestone 2: Device Recognition
- [ ] Add device entries to `devices.json` or equivalent config
  - Wired: `1532:00C4`
  - Dongle: `1532:00C5`
- [ ] Implement device detection callback
- [ ] Test hot-plug scenarios (connect/disconnect)
- [ ] Verify device appears in application UI

### Milestone 3: Protocol Reverse Engineering
- [ ] Capture USB traffic from Windows/Synapse for DPI changes
- [ ] Capture USB traffic for polling rate changes
- [ ] Capture USB traffic for button remapping
- [ ] Capture USB traffic for battery queries
- [ ] Document command structure and response formats
- [ ] Cross-reference with OpenRazer Linux driver source

### Milestone 4: Core Feature Implementation
#### 4.1 DPI Control
- [ ] Implement `setDPI(uint16_t dpi)` function
- [ ] Implement `getDPI()` function
- [ ] Support DPI range: 100-30000 (device-specific limits)
- [ ] Add DPI stages/presets if supported

#### 4.2 Polling Rate
- [ ] Implement `setPollingRate(uint16_t rate)` function
- [ ] Implement `getPollingRate()` function
- [ ] Support rates: 125Hz, 500Hz, 1000Hz, 4000Hz (HyperPolling)

#### 4.3 Battery Monitoring (Wireless Mode)
- [ ] Implement `getBatteryLevel()` function
- [ ] Implement `getChargingStatus()` function
- [ ] Add low battery notification hooks

#### 4.4 Button Mapping
- [ ] Map physical buttons to logical IDs
- [ ] Implement `setButtonAction(button, action)` function
- [ ] Support standard actions: click, DPI cycle, macro trigger

### Milestone 5: UI Integration
- [ ] Add DeathAdder V3 HyperSpeed to device selection
- [ ] Create device-specific settings panel
- [ ] Implement real-time status updates
- [ ] Add battery indicator for wireless mode

### Milestone 6: Testing & Validation
- [ ] Complete all test matrix scenarios
- [ ] Fix identified bugs
- [ ] Performance optimization
- [ ] Memory leak testing

### Milestone 7: Documentation & Release
- [ ] Update razer-macos README with supported device
- [ ] Write user guide for DeathAdder V3 HyperSpeed
- [ ] Create pull request to upstream (if applicable)
- [ ] Release standalone build

---

## Test Matrix

### Environment Compatibility
| macOS Version | Intel | Apple Silicon | Status |
|---------------|-------|---------------|--------|
| macOS 12 Monterey | ⬜ | ⬜ | Not Tested |
| macOS 13 Ventura | ⬜ | ⬜ | Not Tested |
| macOS 14 Sonoma | ⬜ | ⬜ | Not Tested |
| macOS 15 Sequoia | ⬜ | ⬜ | Not Tested |

### Connection Mode Tests
| Test Case | Wired (00C4) | Wireless (00C5) | Status |
|-----------|--------------|-----------------|--------|
| Device Detection | ⬜ | ⬜ | Not Tested |
| Hot Plug | ⬜ | ⬜ | Not Tested |
| Wake from Sleep | ⬜ | ⬜ | Not Tested |
| Reconnection | ⬜ | ⬜ | Not Tested |

### DPI Tests
| Test Case | Expected | Actual | Status |
|-----------|----------|--------|--------|
| Set minimum DPI (100) | DPI = 100 | ⬜ | Not Tested |
| Set maximum DPI (30000) | DPI = 30000 | ⬜ | Not Tested |
| Set custom DPI (1600) | DPI = 1600 | ⬜ | Not Tested |
| Read current DPI | Returns set value | ⬜ | Not Tested |
| DPI persistence after reconnect | Retains value | ⬜ | Not Tested |

### Polling Rate Tests
| Test Case | Expected | Actual | Status |
|-----------|----------|--------|--------|
| Set 125Hz | Rate = 125Hz | ⬜ | Not Tested |
| Set 500Hz | Rate = 500Hz | ⬜ | Not Tested |
| Set 1000Hz | Rate = 1000Hz | ⬜ | Not Tested |
| Set 4000Hz (HyperPolling) | Rate = 4000Hz | ⬜ | Not Tested |
| Read current polling rate | Returns set value | ⬜ | Not Tested |

### Battery Tests (Wireless Only)
| Test Case | Expected | Actual | Status |
|-----------|----------|--------|--------|
| Read battery percentage | 0-100% | ⬜ | Not Tested |
| Detect charging status | True/False | ⬜ | Not Tested |
| Low battery notification | Alert at ≤20% | ⬜ | Not Tested |

### Button Mapping Tests
| Test Case | Expected | Actual | Status |
|-----------|----------|--------|--------|
| Remap Button 4 | Custom action | ⬜ | Not Tested |
| Remap Button 5 | Custom action | ⬜ | Not Tested |
| Reset to defaults | Factory config | ⬜ | Not Tested |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Encrypted USB protocol | Medium | High | Use known OpenRazer patterns as reference |
| macOS HID permission issues | High | Medium | Document System Preferences requirements |
| Device firmware variations | Low | Medium | Test multiple firmware versions |
| razer-macos architectural limitations | Medium | Medium | Propose upstream changes or maintain fork |

---

## Resources

- [razer-macos GitHub](https://github.com/1kc/razer-macos)
- [OpenRazer GitHub](https://github.com/openrazer/openrazer)
- [OpenRazer Device Support](https://openrazer.github.io/#devices)
- [USB ID Database](https://usb-ids.gowdy.us/)

---

## Status Legend
- ⬜ Not Tested
- 🟡 In Progress
- ✅ Passed
- ❌ Failed
