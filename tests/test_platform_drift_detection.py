from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_drift_module():
    path = ROOT / "scripts" / "health" / "drift-detection" / "check-platform-drift.py"
    spec = importlib.util.spec_from_file_location("platform_drift", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_detects_unexpected_listener_on_manual_lane():
    drift = load_drift_module()
    baseline = {
        "ports": {
            "18080": {"expected": "listening"},
            "8002": {"expected": "stopped"},
        }
    }
    observed = {
        "ports": [
            {"port": 18080, "listening": True},
            {"port": 8002, "listening": True},
        ]
    }

    findings = drift.compare_ports(baseline, observed)

    assert findings == [
        {
            "id": "port-8002-state",
            "severity": "medium",
            "message": "Port 8002 expected stopped but is listening.",
        }
    ]


def test_detects_launchagent_missing_program(tmp_path):
    drift = load_drift_module()
    plist = tmp_path / "local.test.agent.plist"
    plist.write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>local.test.agent</string>
<key>ProgramArguments</key><array><string>/missing/program.sh</string></array>
</dict></plist>
"""
    )
    baseline = {"launchagents": {"local.test.agent": {"expected": "healthy"}}}

    findings = drift.compare_launchagents(baseline, tmp_path)

    assert findings[0]["id"] == "launchagent-local.test.agent-program"
    assert findings[0]["severity"] == "high"
    assert "missing program" in findings[0]["message"]


def test_detects_unapproved_workflow_action_version(tmp_path):
    drift = load_drift_module()
    workflow_dir = tmp_path / ".github" / "workflows"
    workflow_dir.mkdir(parents=True)
    (workflow_dir / "release.yml").write_text(
        """name: Release
on: push
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: softprops/action-gh-release@v2
"""
    )
    baseline = {
        "workflow_actions": {
            "actions/checkout": "v4",
            "softprops/action-gh-release": "v2",
        }
    }

    findings = drift.compare_workflows(baseline, workflow_dir)

    assert findings == [
        {
            "id": "workflow-action-actions/checkout",
            "severity": "medium",
            "message": "actions/checkout expected v4 but found v3 in release.yml.",
        }
    ]
