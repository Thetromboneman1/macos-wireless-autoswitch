#!/usr/bin/env python3
"""Generate a compact AIOps platform report from health and drift JSON."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def summarize_lanes(lanes: list[dict[str, Any]]) -> dict[str, list[str]]:
    running = []
    manual_stopped = []
    failed = []
    for lane in lanes:
        name = str(lane.get("name", "unknown"))
        if not lane.get("ok"):
            failed.append(name)
        elif lane.get("state") == "stopped":
            manual_stopped.append(name)
        else:
            running.append(name)
    return {"running": running, "manual_stopped": manual_stopped, "failed": failed}


def build_report(
    health_path: Path,
    drift_path: Path,
    dependency_path: Path | None = None,
    documentation_path: Path | None = None,
) -> dict[str, Any]:
    health = load_json(health_path)
    drift = load_json(drift_path)
    dependency = load_json(dependency_path) if dependency_path else {"ok": None, "finding_count": None, "findings": []}
    documentation = load_json(documentation_path) if documentation_path else {"ok": None, "finding_count": None, "findings": []}
    sections = {
        "health": {
            "ok": bool(health.get("ok")),
            "swap_pressure": health.get("system", {}).get("swap", {}).get("pressure", "unknown"),
            "swap_used_percent": health.get("system", {}).get("swap", {}).get("used_percent"),
            "codex_skills_ok": health.get("codex_skills", {}).get("ok"),
            "vscode_recommendations_ok": health.get("vscode_recommendations", {}).get("ok"),
        },
        "lanes": summarize_lanes(health.get("lanes", [])),
        "launchagents": {
            "count": len(health.get("launchagents", [])),
            "broken": [item.get("label") for item in health.get("launchagents", []) if not item.get("ok")],
        },
        "drift": {
            "ok": bool(drift.get("ok")),
            "finding_count": int(drift.get("finding_count", 0)),
            "findings": drift.get("findings", []),
        },
        "dependencies": {
            "ok": dependency.get("ok"),
            "finding_count": dependency.get("finding_count"),
            "findings": dependency.get("findings", []),
        },
        "documentation": {
            "ok": documentation.get("ok"),
            "reviewed_count": documentation.get("reviewed_count"),
            "finding_count": documentation.get("finding_count"),
            "findings": documentation.get("findings", []),
        },
    }
    optional_dependency_ok = dependency.get("ok") is not False
    optional_documentation_ok = documentation.get("ok") is not False
    return {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ok": (
            sections["health"]["ok"]
            and sections["drift"]["ok"]
            and optional_dependency_ok
            and optional_documentation_ok
            and not sections["lanes"]["failed"]
        ),
        "sections": sections,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--health-json", type=Path, required=True)
    parser.add_argument("--drift-json", type=Path, required=True)
    parser.add_argument("--dependency-json", type=Path)
    parser.add_argument("--documentation-json", type=Path)
    parser.add_argument("--json", type=Path, help="Write report JSON to this path.")
    args = parser.parse_args(argv)

    report = build_report(args.health_json, args.drift_json, args.dependency_json, args.documentation_json)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
