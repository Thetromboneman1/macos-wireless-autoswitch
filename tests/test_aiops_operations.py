from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    path = ROOT / "scripts" / "operations" / name
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, data: dict) -> Path:
    path.write_text(json.dumps(data, indent=2) + "\n")
    return path


def test_platform_report_combines_health_and_drift(tmp_path):
    report = load_script("generate-platform-report.py")
    health_path = write_json(
        tmp_path / "health.json",
        {
            "ok": True,
            "system": {"swap": {"pressure": "normal", "used_percent": 12.3}},
            "lanes": [
                {"name": "omlx-production", "ok": True},
                {"name": "rapid-mlx", "ok": True, "state": "stopped"},
            ],
            "launchagents": [{"label": "com.corn.omlx-power-policy", "ok": True}],
            "codex_skills": {"ok": True},
            "vscode_recommendations": {"ok": True},
        },
    )
    drift_path = write_json(tmp_path / "drift.json", {"ok": True, "finding_count": 0, "findings": []})
    doc_path = write_json(tmp_path / "documentation.json", {"ok": True, "reviewed_count": 3, "finding_count": 0, "findings": []})

    result = report.build_report(health_path, drift_path, documentation_path=doc_path)

    assert result["ok"] is True
    assert result["sections"]["health"]["ok"] is True
    assert result["sections"]["drift"]["finding_count"] == 0
    assert result["sections"]["documentation"]["reviewed_count"] == 3
    assert result["sections"]["lanes"]["running"] == ["omlx-production"]
    assert result["sections"]["lanes"]["manual_stopped"] == ["rapid-mlx"]


def test_benchmark_governance_flags_ttft_regression(tmp_path):
    bench = load_script("benchmark-governance.py")
    baseline = {
        "engines": [
            {
                "engine": "omlx-mlx",
                "runs": [{"workload": "coding_patch", "ttft_s": 0.05, "output_tok_s_wall": 50.0}],
            }
        ]
    }
    current = {
        "engines": [
            {
                "engine": "omlx-mlx",
                "runs": [{"workload": "coding_patch", "ttft_s": 0.09, "output_tok_s_wall": 42.0}],
            }
        ]
    }

    result = bench.compare_benchmarks(baseline, current, ttft_regression_pct=25, throughput_regression_pct=10)

    assert result["ok"] is False
    assert {finding["metric"] for finding in result["findings"]} == {"ttft_s", "output_tok_s_wall"}
    assert result["summary"]["comparison_count"] == 1


def test_documentation_review_finds_missing_review_date(tmp_path):
    review = load_script("documentation-review.py")
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "good.md").write_text("# Good\n\nDate: 2026-06-23\n\nOwner: Platform\n")
    (docs / "bad.md").write_text("# Bad\n\nOwner: Platform\n")

    result = review.review_docs([docs])

    assert result["ok"] is False
    assert result["finding_count"] == 1
    assert result["findings"][0]["path"].endswith("bad.md")
    assert result["findings"][0]["id"] == "missing-review-date"


def test_dependency_report_extracts_workflow_actions(tmp_path):
    deps = load_script("dependency-report.py")
    workflow = tmp_path / ".github" / "workflows" / "release.yml"
    workflow.parent.mkdir(parents=True)
    workflow.write_text("steps:\n  - uses: actions/checkout@v4\n")

    result = deps.build_dependency_report(root=tmp_path, include_live=False)

    assert result["ok"] is True
    assert result["sections"]["github_actions"] == [{"action": "actions/checkout", "version": "v4", "path": str(workflow)}]
    assert "python" in result["sections"]
