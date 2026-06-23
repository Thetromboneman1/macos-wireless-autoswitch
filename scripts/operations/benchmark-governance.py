#!/usr/bin/env python3
"""Compare local AI benchmark artifacts and flag regressions."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def indexed_runs(artifact: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    rows = {}
    for engine in artifact.get("engines", []):
        engine_name = str(engine.get("engine", "unknown"))
        for group in ("runs", "context_scaling"):
            for run in engine.get(group, []):
                if run.get("workload"):
                    rows[(engine_name, str(run["workload"]))] = run
        for item in engine.get("concurrency", []):
            rows[(engine_name, f"concurrency_{item.get('concurrency')}")] = item
    return rows


def regression_pct(old: float, new: float, *, higher_is_better: bool) -> float:
    if old == 0:
        return 0.0
    if higher_is_better:
        return round(((old - new) / old) * 100, 2)
    return round(((new - old) / old) * 100, 2)


def compare_benchmarks(
    baseline: dict[str, Any],
    current: dict[str, Any],
    *,
    ttft_regression_pct: float = 35.0,
    throughput_regression_pct: float = 20.0,
) -> dict[str, Any]:
    baseline_runs = indexed_runs(baseline)
    current_runs = indexed_runs(current)
    findings = []
    comparison_count = 0
    for key, before in sorted(baseline_runs.items()):
        after = current_runs.get(key)
        if not after:
            findings.append({"id": "missing-workload", "severity": "warning", "engine": key[0], "workload": key[1]})
            continue
        comparison_count += 1
        for metric, threshold, higher_is_better in (
            ("ttft_s", ttft_regression_pct, False),
            ("output_tok_s_wall", throughput_regression_pct, True),
            ("aggregate_output_tok_s_wall", throughput_regression_pct, True),
        ):
            old = before.get(metric)
            new = after.get(metric)
            if not isinstance(old, (int, float)) or not isinstance(new, (int, float)):
                continue
            change = regression_pct(float(old), float(new), higher_is_better=higher_is_better)
            if change > threshold:
                findings.append(
                    {
                        "id": "benchmark-regression",
                        "severity": "warning",
                        "engine": key[0],
                        "workload": key[1],
                        "metric": metric,
                        "baseline": old,
                        "current": new,
                        "regression_pct": change,
                        "threshold_pct": threshold,
                    }
                )
    return {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ok": not findings,
        "summary": {"comparison_count": comparison_count, "finding_count": len(findings)},
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--current", type=Path, required=True)
    parser.add_argument("--json", type=Path, help="Write comparison JSON to this path.")
    parser.add_argument("--ttft-regression-pct", type=float, default=35.0)
    parser.add_argument("--throughput-regression-pct", type=float, default=20.0)
    args = parser.parse_args(argv)

    report = compare_benchmarks(
        load_json(args.baseline),
        load_json(args.current),
        ttft_regression_pct=args.ttft_regression_pct,
        throughput_regression_pct=args.throughput_regression_pct,
    )
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
