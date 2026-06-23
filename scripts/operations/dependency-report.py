#!/usr/bin/env python3
"""Generate a dependency governance inventory for the local AI platform repo."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from pathlib import Path
from typing import Any


def run_lines(command: list[str]) -> list[str]:
    try:
        out = subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def workflow_actions(root: Path) -> list[dict[str, str]]:
    rows = []
    workflow_dir = root / ".github" / "workflows"
    for path in sorted(workflow_dir.glob("*.yml")) + sorted(workflow_dir.glob("*.yaml")):
        for line in path.read_text().splitlines():
            match = re.search(r"uses:\s*([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)@([A-Za-z0-9_.-]+)", line)
            if match:
                rows.append({"action": match.group(1), "version": match.group(2), "path": str(path)})
    return rows


def docker_images(root: Path) -> list[dict[str, str]]:
    rows = []
    for path in sorted(root.glob("**/docker-compose.yml")):
        for line in path.read_text().splitlines():
            stripped = line.strip()
            if stripped.startswith("image:"):
                rows.append({"image": stripped.split(":", 1)[1].strip(), "path": str(path)})
    return rows


def codex_skills() -> list[str]:
    skills_root = Path.home() / ".codex" / "skills"
    return sorted(path.parent.name for path in skills_root.glob("*/SKILL.md"))


def vscode_extensions() -> list[str]:
    code = "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
    return run_lines([code, "--list-extensions", "--show-versions"])


def build_dependency_report(root: Path = Path("."), *, include_live: bool = True) -> dict[str, Any]:
    sections: dict[str, Any] = {
        "python": {
            "manifest_files": [str(path) for path in sorted(root.glob("**/requirements*.txt")) + sorted(root.glob("**/pyproject.toml"))],
            "test_runner": "uvx pytest",
        },
        "homebrew": run_lines(["brew", "leaves"]) if include_live else [],
        "vscode_extensions": vscode_extensions() if include_live else [],
        "codex_skills": codex_skills() if include_live else [],
        "github_actions": workflow_actions(root),
        "docker_images": docker_images(root),
        "mcp_tools": [str(path) for path in sorted((root / "config" / "local-ai-platform").glob("*.json"))],
    }
    return {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ok": True,
        "sections": sections,
        "finding_count": 0,
        "findings": [],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--no-live", action="store_true", help="Skip live Homebrew/VS Code/Codex inventory.")
    parser.add_argument("--json", type=Path, help="Write report JSON to this path.")
    args = parser.parse_args(argv)

    report = build_dependency_report(args.root, include_live=not args.no_live)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
