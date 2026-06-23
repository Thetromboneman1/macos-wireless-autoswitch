#!/usr/bin/env python3
"""Analyze benchmark artifacts for local AI performance trends."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def pct_change(old: float, new: float, *, higher_is_better: bool) -> float:
    if old == 0:
        return 0.0
    if higher_is_better:
        return round(((old - new) / old) * 100, 2)
    return round(((new - old) / old) * 100, 2)


def iter_runs(path: Path, artifact: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    created_at = artifact.get("created_at") or path.stem
    for engine in artifact.get("engines", []):
        engine_name = str(engine.get("engine", "unknown"))
        for group in ("runs", "context_scaling"):
            for run in engine.get(group, []):
                workload = run.get("workload")
                if workload:
                    rows.append({"path": str(path), "created_at": created_at, "engine": engine_name, "workload": str(workload), "data": run})
        for run in engine.get("concurrency", []):
            concurrency = run.get("concurrency")
            if concurrency is not None:
                rows.append({"path": str(path), "created_at": created_at, "engine": engine_name, "workload": f"concurrency_{concurrency}", "data": run})
    return rows


def analyze_trends(
    paths: list[Path],
    *,
    ttft_degradation_pct: float = 35.0,
    throughput_degradation_pct: float = 20.0,
    swap_degradation_pct: float = 20.0,
    reliability_degradation_pct: float = 5.0,
) -> dict[str, Any]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for path in paths:
        for row in iter_runs(path, load_json(path)):
            grouped.setdefault((row["engine"], row["workload"]), []).append(row)

    findings = []
    series = []
    for (engine, workload), rows in sorted(grouped.items()):
        rows = sorted(rows, key=lambda item: (str(item["created_at"]), item["path"]))
        if len(rows) < 2:
            continue
        first = rows[0]["data"]
        last = rows[-1]["data"]
        summary = {"engine": engine, "workload": workload, "points": len(rows), "first_path": rows[0]["path"], "last_path": rows[-1]["path"]}
        for metric, threshold, higher_is_better, finding_id in (
            ("ttft_s", ttft_degradation_pct, False, "ttft-degradation"),
            ("output_tok_s_wall", throughput_degradation_pct, True, "throughput-degradation"),
            ("aggregate_output_tok_s_wall", throughput_degradation_pct, True, "throughput-degradation"),
            ("swap_used_percent", swap_degradation_pct, False, "swap-degradation"),
            ("reliability", reliability_degradation_pct, True, "reliability-degradation"),
        ):
            old = first.get(metric)
            new = last.get(metric)
            if not isinstance(old, (int, float)) or not isinstance(new, (int, float)):
                continue
            change = pct_change(float(old), float(new), higher_is_better=higher_is_better)
            summary[f"{metric}_change_pct"] = change
            if change > threshold:
                findings.append(
                    {
                        "id": finding_id,
                        "severity": "warning",
                        "engine": engine,
                        "workload": workload,
                        "metric": metric,
                        "baseline": old,
                        "current": new,
                        "change_pct": change,
                        "threshold_pct": threshold,
                    }
                )
        series.append(summary)

    return {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ok": not findings,
        "summary": {"artifact_count": len(paths), "series_count": len(series), "finding_count": len(findings)},
        "series": series,
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("benchmarks", nargs="+", type=Path)
    parser.add_argument("--json", type=Path, help="Write trend report JSON to this path.")
    parser.add_argument("--ttft-degradation-pct", type=float, default=35.0)
    parser.add_argument("--throughput-degradation-pct", type=float, default=20.0)
    parser.add_argument("--swap-degradation-pct", type=float, default=20.0)
    parser.add_argument("--reliability-degradation-pct", type=float, default=5.0)
    args = parser.parse_args(argv)

    report = analyze_trends(
        args.benchmarks,
        ttft_degradation_pct=args.ttft_degradation_pct,
        throughput_degradation_pct=args.throughput_degradation_pct,
        swap_degradation_pct=args.swap_degradation_pct,
        reliability_degradation_pct=args.reliability_degradation_pct,
    )
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
