#!/usr/bin/env python3
"""Detect drift from the approved local AI platform baseline."""

from __future__ import annotations

import argparse
import json
import plistlib
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_BASELINE = Path(__file__).with_name("baseline.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def finding(id_: str, severity: str, message: str) -> dict[str, str]:
    return {"id": id_, "severity": severity, "message": message}


def observed_ports_from_lsof(ports: list[int]) -> list[dict[str, Any]]:
    rows = []
    for port in ports:
        try:
            out = subprocess.check_output(
                ["lsof", "-nP", f"-iTCP:{port}", "-sTCP:LISTEN"],
                text=True,
                stderr=subprocess.DEVNULL,
            )
            listeners = [line for line in out.splitlines()[1:] if line.strip()]
        except subprocess.CalledProcessError:
            listeners = []
        rows.append({"port": port, "listening": bool(listeners), "listeners": listeners[:5]})
    return rows


def compare_ports(baseline: dict[str, Any], observed: dict[str, Any]) -> list[dict[str, str]]:
    observed_by_port = {str(row["port"]): bool(row.get("listening")) for row in observed.get("ports", [])}
    findings = []
    for port, rule in baseline.get("ports", {}).items():
        expected = rule.get("expected")
        listening = observed_by_port.get(str(port), False)
        if expected == "listening" and not listening:
            findings.append(finding(f"port-{port}-state", "high", f"Port {port} expected listening but is stopped."))
        if expected == "stopped" and listening:
            findings.append(finding(f"port-{port}-state", "medium", f"Port {port} expected stopped but is listening."))
    return findings


def load_plist(path: Path) -> dict[str, Any]:
    try:
        data = plistlib.loads(path.read_bytes())
    except Exception:
        out = subprocess.check_output(["plutil", "-convert", "json", "-o", "-", str(path)], text=True)
        data = json.loads(out)
    if not isinstance(data, dict):
        raise ValueError(f"{path} plist root is not a dictionary")
    return data


def plist_program(data: dict[str, Any]) -> str:
    args = data.get("ProgramArguments")
    if isinstance(args, list) and args:
        return str(args[0])
    program = data.get("Program")
    return str(program) if program else ""


def compare_launchagents(baseline: dict[str, Any], launchagent_dir: Path | None = None) -> list[dict[str, str]]:
    directory = launchagent_dir or (Path.home() / "Library" / "LaunchAgents")
    plists = {}
    for path in directory.glob("*.plist"):
        try:
            data = load_plist(path)
        except Exception as exc:
            plists[path.stem] = {"path": path, "error": str(exc)}
            continue
        label = str(data.get("Label") or path.stem)
        plists[label] = {"path": path, "data": data}

    findings = []
    for label, rule in baseline.get("launchagents", {}).items():
        expected = rule.get("expected")
        item = plists.get(label)
        if expected == "absent" and item:
            findings.append(finding(f"launchagent-{label}-present", "medium", f"{label} should be absent but exists at {item['path']}."))
            continue
        if expected != "healthy":
            continue
        if not item:
            findings.append(finding(f"launchagent-{label}-missing", "high", f"{label} expected healthy but plist is missing."))
            continue
        if item.get("error"):
            findings.append(finding(f"launchagent-{label}-plist", "high", f"{label} plist cannot be parsed: {item['error']}"))
            continue
        program = plist_program(item["data"])
        if not program or not Path(program).exists():
            findings.append(finding(f"launchagent-{label}-program", "high", f"{label} has missing program path: {program or '<none>'}."))
    return findings


def workflow_uses(path: Path) -> list[tuple[str, str]]:
    uses = []
    for line in path.read_text().splitlines():
        match = re.search(r"uses:\s*([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)@([A-Za-z0-9_.-]+)", line)
        if match:
            uses.append((match.group(1), match.group(2)))
    return uses


def compare_workflows(baseline: dict[str, Any], workflow_dir: Path | None = None) -> list[dict[str, str]]:
    directory = workflow_dir or (ROOT / ".github" / "workflows")
    approved = baseline.get("workflow_actions", {})
    findings = []
    for path in sorted(directory.glob("*.yml")) + sorted(directory.glob("*.yaml")):
        for action, version in workflow_uses(path):
            expected = approved.get(action)
            if expected and version != expected:
                findings.append(
                    finding(
                        f"workflow-action-{action}",
                        "medium",
                        f"{action} expected {expected} but found {version} in {path.name}.",
                    )
                )
    return findings


def compare_config_paths(baseline: dict[str, Any], root: Path = ROOT) -> list[dict[str, str]]:
    findings = []
    for rel_path, kind in baseline.get("config_paths", {}).items():
        path = root / rel_path
        if kind == "file" and not path.is_file():
            findings.append(finding(f"config-{rel_path}", "medium", f"Expected config file is missing: {rel_path}."))
        elif kind == "directory" and not path.is_dir():
            findings.append(finding(f"config-{rel_path}", "medium", f"Expected config directory is missing: {rel_path}."))
    return findings


def compare_binaries(baseline: dict[str, Any]) -> list[dict[str, str]]:
    findings = []
    for name, state in baseline.get("binaries", {}).items():
        if state == "required" and not shutil.which(name):
            findings.append(finding(f"binary-{name}", "medium", f"Required validation binary is missing from PATH: {name}."))
    return findings


def collect_observed(baseline: dict[str, Any], health_json: Path | None) -> dict[str, Any]:
    if health_json:
        return load_json(health_json)
    ports = [int(port) for port in baseline.get("ports", {})]
    return {"ports": observed_ports_from_lsof(ports)}


def build_report(baseline: dict[str, Any], observed: dict[str, Any]) -> dict[str, Any]:
    findings = []
    findings.extend(compare_ports(baseline, observed))
    findings.extend(compare_launchagents(baseline))
    findings.extend(compare_workflows(baseline))
    findings.extend(compare_config_paths(baseline))
    findings.extend(compare_binaries(baseline))
    return {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ok": not findings,
        "finding_count": len(findings),
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    parser.add_argument("--health-json", type=Path, help="Use an existing local-ai-health JSON snapshot.")
    parser.add_argument("--json", type=Path, help="Write the drift report to this path.")
    args = parser.parse_args(argv)

    baseline = load_json(args.baseline)
    observed = collect_observed(baseline, args.health_json)
    report = build_report(baseline, observed)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
