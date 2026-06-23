#!/usr/bin/env python3
"""Review current documentation for governance metadata."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any


SKIP_DIRS = {".git", ".pytest_cache", "node_modules"}


def iter_markdown(paths: list[Path]) -> list[Path]:
    files = []
    for path in paths:
        if path.is_file() and path.suffix == ".md":
            files.append(path)
        elif path.is_dir():
            for child in path.rglob("*.md"):
                if any(part in SKIP_DIRS for part in child.parts):
                    continue
                files.append(child)
    return sorted(files)


def has_review_date(text: str) -> bool:
    return any(line.startswith(("Date:", "Last reviewed:", "Reviewed:")) for line in text.splitlines()[:20])


def has_owner(text: str) -> bool:
    return any(line.startswith(("Owner:", "Service owner:", "Document owner:")) for line in text.splitlines()[:40])


def review_file(path: Path) -> list[dict[str, str]]:
    text = path.read_text(errors="replace")
    findings = []
    if not has_review_date(text):
        findings.append({"id": "missing-review-date", "severity": "warning", "path": str(path), "message": "Missing Date or Last reviewed metadata."})
    if path.parts[:2] != ("docs", "autonomous-modernization") and not has_owner(text):
        findings.append({"id": "missing-owner", "severity": "informational", "path": str(path), "message": "Missing Owner metadata."})
    return findings


def review_docs(paths: list[Path]) -> dict[str, Any]:
    findings = []
    files = iter_markdown(paths)
    for path in files:
        findings.extend(review_file(path))
    return {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ok": not any(item["severity"] == "warning" for item in findings),
        "reviewed_count": len(files),
        "finding_count": len(findings),
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, default=[Path("docs")])
    parser.add_argument("--json", type=Path, help="Write review JSON to this path.")
    args = parser.parse_args(argv)

    report = review_docs(args.paths)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
