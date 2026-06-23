#!/usr/bin/env python3
"""Evaluate model promotion evidence against platform governance gates."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def ok_value(report: dict[str, Any]) -> bool:
    return bool(report.get("ok"))


def add_gate(gates: list[dict[str, Any]], findings: list[dict[str, Any]], name: str, ok: bool, finding: dict[str, Any] | None = None) -> None:
    gates.append({"name": name, "ok": ok})
    if not ok and finding:
        findings.append(finding)


def evaluate_model_promotion(
    *,
    benchmark_path: Path,
    stability_path: Path,
    health_path: Path,
    tool_call_path: Path,
    documentation_path: Path,
    max_swap_used_percent: float = 80.0,
) -> dict[str, Any]:
    benchmark = load_json(benchmark_path)
    stability = load_json(stability_path)
    health = load_json(health_path)
    tool_calling = load_json(tool_call_path)
    documentation = load_json(documentation_path)

    gates: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []

    add_gate(
        gates,
        findings,
        "benchmark",
        ok_value(benchmark),
        {"id": "benchmark-gate-failed", "severity": "warning", "message": "Benchmark governance report is not passing."},
    )
    add_gate(
        gates,
        findings,
        "stability",
        ok_value(stability),
        {"id": "stability-gate-failed", "severity": "warning", "message": "Stability evidence is not passing."},
    )
    add_gate(
        gates,
        findings,
        "health",
        ok_value(health),
        {"id": "health-gate-failed", "severity": "critical", "message": "Platform health report is not passing."},
    )

    swap = health.get("system", {}).get("swap", {})
    swap_used = swap.get("used_percent")
    swap_ok = isinstance(swap_used, (int, float)) and float(swap_used) <= max_swap_used_percent and swap.get("pressure") != "high"
    add_gate(
        gates,
        findings,
        "swap",
        swap_ok,
        {
            "id": "swap-threshold-exceeded",
            "severity": "warning",
            "message": "Swap pressure exceeds the model promotion threshold.",
            "swap_used_percent": swap_used,
            "swap_pressure": swap.get("pressure", "unknown"),
            "threshold_percent": max_swap_used_percent,
        },
    )
    add_gate(
        gates,
        findings,
        "tool_calling",
        ok_value(tool_calling),
        {"id": "tool-calling-gate-failed", "severity": "warning", "message": "Tool-calling validation is not passing."},
    )
    add_gate(
        gates,
        findings,
        "documentation",
        ok_value(documentation),
        {"id": "documentation-gate-failed", "severity": "warning", "message": "Documentation review is not passing."},
    )

    return {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ok": not findings,
        "summary": {"gate_count": len(gates), "failed_gate_count": len(findings)},
        "gates": gates,
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark-json", type=Path, required=True)
    parser.add_argument("--stability-json", type=Path, required=True)
    parser.add_argument("--health-json", type=Path, required=True)
    parser.add_argument("--tool-call-json", type=Path, required=True)
    parser.add_argument("--documentation-json", type=Path, required=True)
    parser.add_argument("--max-swap-used-percent", type=float, default=80.0)
    parser.add_argument("--json", type=Path, help="Write gate report JSON to this path.")
    args = parser.parse_args(argv)

    report = evaluate_model_promotion(
        benchmark_path=args.benchmark_json,
        stability_path=args.stability_json,
        health_path=args.health_json,
        tool_call_path=args.tool_call_json,
        documentation_path=args.documentation_json,
        max_swap_used_percent=args.max_swap_used_percent,
    )
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
