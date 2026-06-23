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
    cost_path = write_json(
        tmp_path / "hermes-cost.json",
        {
            "ok": True,
            "sections": {
                "usage": {"input_tokens": 150, "output_tokens": 30, "cache_hit_percent": 26.7},
                "fixed_prompt_overhead": {"platforms": {"cli": {"estimated_total_tokens": 1795}}},
                "runtime_toolsets": {"tools-cli": {"enabled_count": 10, "disabled_count": 15}},
            },
        },
    )

    result = report.build_report(health_path, drift_path, documentation_path=doc_path, hermes_cost_path=cost_path)

    assert result["ok"] is True
    assert result["sections"]["health"]["ok"] is True
    assert result["sections"]["drift"]["finding_count"] == 0
    assert result["sections"]["documentation"]["reviewed_count"] == 3
    assert result["sections"]["lanes"]["running"] == ["omlx-production"]
    assert result["sections"]["lanes"]["manual_stopped"] == ["rapid-mlx"]
    assert result["sections"]["hermes_cost"]["usage"]["input_tokens"] == 150
    assert result["sections"]["hermes_cost"]["fixed_prompt_overhead"]["cli_estimated_total_tokens"] == 1795
    assert result["sections"]["hermes_cost"]["runtime_toolsets"]["tools-cli"]["enabled_count"] == 10


def test_hermes_cost_report_summarizes_prompt_overhead(tmp_path):
    costs = load_script("hermes-cost-report.py")
    prompt_path = write_json(
        tmp_path / "prompt-size.json",
        {
            "platform": "cli",
            "model": "local-model",
            "system_prompt": {"chars": 2000, "bytes": 2100},
            "skills_index": {"chars": 1000, "bytes": 1000},
            "memory": {"chars": 100, "bytes": 100},
            "user_profile": {"chars": 80, "bytes": 80},
            "tools": {"count": 10, "json_bytes": 4000},
        },
    )

    result = costs.build_cost_report(prompt_size_paths=[prompt_path])

    assert result["ok"] is True
    fixed = result["sections"]["fixed_prompt_overhead"]
    assert fixed["platforms"]["cli"]["tool_count"] == 10
    assert fixed["platforms"]["cli"]["reported_tool_count"] == 10
    assert fixed["platforms"]["cli"]["measurement_scope"] == "hermes_prompt_size_reported_static_overhead"
    assert fixed["platforms"]["cli"]["cost_claim_status"] == "reported_not_observed_usage"
    assert fixed["platforms"]["cli"]["estimated_total_tokens"] == 1795
    assert fixed["platforms"]["cli"]["reported_total_tokens"] == 1795
    assert fixed["platforms"]["cli"]["estimated_tool_schema_tokens"] == 1000
    assert fixed["platforms"]["cli"]["reported_tool_schema_tokens"] == 1000


def test_hermes_cost_report_records_runtime_toolsets(tmp_path):
    costs = load_script("hermes-cost-report.py")
    tools_path = tmp_path / "tools-cli.txt"
    tools_path.write_text(
        "\n".join(
            [
                "Built-in toolsets (cli):",
                "  ✓ enabled  web  Web Search & Scraping",
                "  ✗ disabled  browser  Browser Automation",
                "  ✓ enabled  terminal  Terminal & Processes",
                "",
                "MCP servers:",
                "  octopoda  all tools enabled",
            ]
        )
        + "\n"
    )

    result = costs.build_cost_report(tools_list_paths=[tools_path])

    runtime = result["sections"]["runtime_toolsets"]["tools-cli"]
    assert runtime["enabled"] == ["web", "terminal"]
    assert runtime["disabled"] == ["browser"]
    assert runtime["enabled_count"] == 2
    assert runtime["disabled_count"] == 1
    assert runtime["mcp_servers"] == ["octopoda"]


def test_hermes_cost_report_aggregates_usage_records(tmp_path):
    costs = load_script("hermes-cost-report.py")
    usage_path = tmp_path / "session.jsonl"
    usage_path.write_text(
        "\n".join(
            [
                json.dumps({"usage": {"prompt_tokens": 100, "completion_tokens": 20, "prompt_tokens_details": {"cached_tokens": 40}}}),
                json.dumps({"response": {"usage": {"input_tokens": 50, "output_tokens": 10}}}),
            ]
        )
        + "\n"
    )

    result = costs.build_cost_report(session_paths=[usage_path])

    usage = result["sections"]["usage"]
    assert usage["record_count"] == 2
    assert usage["input_tokens"] == 150
    assert usage["output_tokens"] == 30
    assert usage["cached_input_tokens"] == 40
    assert usage["cache_hit_percent"] == 26.7


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


def test_model_promotion_gate_rejects_high_swap(tmp_path):
    gates = load_script("model-governance/evaluate-promotion.py")
    benchmark_path = write_json(tmp_path / "benchmark.json", {"ok": True, "summary": {"finding_count": 0}})
    stability_path = write_json(tmp_path / "stability.json", {"ok": True, "failure_count": 0})
    health_path = write_json(
        tmp_path / "health.json",
        {
            "ok": True,
            "system": {"swap": {"pressure": "high", "used_percent": 84.0}},
            "lanes": [{"name": "omlx-production", "ok": True}],
        },
    )
    tool_path = write_json(tmp_path / "tool.json", {"ok": True})
    docs_path = write_json(tmp_path / "documentation.json", {"ok": True, "finding_count": 0})

    result = gates.evaluate_model_promotion(
        benchmark_path=benchmark_path,
        stability_path=stability_path,
        health_path=health_path,
        tool_call_path=tool_path,
        documentation_path=docs_path,
        max_swap_used_percent=75.0,
    )

    assert result["ok"] is False
    assert result["summary"]["gate_count"] == 6
    assert result["summary"]["failed_gate_count"] == 1
    assert result["findings"][0]["id"] == "swap-threshold-exceeded"


def test_model_promotion_gate_accepts_complete_evidence(tmp_path):
    gates = load_script("model-governance/evaluate-promotion.py")
    benchmark_path = write_json(tmp_path / "benchmark.json", {"ok": True, "summary": {"finding_count": 0}})
    stability_path = write_json(tmp_path / "stability.json", {"ok": True, "failure_count": 0})
    health_path = write_json(
        tmp_path / "health.json",
        {
            "ok": True,
            "system": {"swap": {"pressure": "elevated", "used_percent": 42.0}},
            "lanes": [{"name": "omlx-production", "ok": True}],
        },
    )
    tool_path = write_json(tmp_path / "tool.json", {"ok": True})
    docs_path = write_json(tmp_path / "documentation.json", {"ok": True, "finding_count": 0})

    result = gates.evaluate_model_promotion(
        benchmark_path=benchmark_path,
        stability_path=stability_path,
        health_path=health_path,
        tool_call_path=tool_path,
        documentation_path=docs_path,
    )

    assert result["ok"] is True
    assert result["findings"] == []
    assert {gate["name"] for gate in result["gates"]} == {
        "benchmark",
        "stability",
        "health",
        "swap",
        "tool_calling",
        "documentation",
    }


def test_benchmark_trend_analysis_flags_ttft_degradation(tmp_path):
    trends = load_script("benchmark-trend-analysis.py")
    first = write_json(
        tmp_path / "bench-1.json",
        {
            "created_at": "2026-06-01T00:00:00Z",
            "engines": [
                {
                    "engine": "omlx-mlx",
                    "runs": [{"workload": "coding_patch", "ttft_s": 0.05, "output_tok_s_wall": 50.0, "reliability": 1.0}],
                }
            ],
        },
    )
    second = write_json(
        tmp_path / "bench-2.json",
        {
            "created_at": "2026-06-23T00:00:00Z",
            "engines": [
                {
                    "engine": "omlx-mlx",
                    "runs": [{"workload": "coding_patch", "ttft_s": 0.09, "output_tok_s_wall": 49.0, "reliability": 1.0}],
                }
            ],
        },
    )

    result = trends.analyze_trends([first, second], ttft_degradation_pct=50.0)

    assert result["ok"] is False
    assert result["summary"]["series_count"] == 1
    assert result["findings"][0]["id"] == "ttft-degradation"
    assert result["series"][0]["engine"] == "omlx-mlx"
    assert result["series"][0]["workload"] == "coding_patch"
