from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_validator_module():
    path = ROOT / "scripts" / "local-ai" / "validate-hermes-mlx.py"
    spec = importlib.util.spec_from_file_location("validate_hermes_mlx", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_health_module():
    path = ROOT / "scripts" / "health" / "local-ai-health.py"
    spec = importlib.util.spec_from_file_location("local_ai_health", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_gguf_coding_lane_does_not_enable_mtp_on_apple_silicon():
    script = (ROOT / "scripts" / "gemma4-gguf-coding-lane.sh").read_text()

    assert "--spec-type draft-mtp" not in script
    assert "--model-draft" not in script
    assert "no-MTP" in script


def test_tool_call_payload_uses_openai_tool_schema():
    validator = load_validator_module()

    payload = validator.tool_call_payload("local-model")

    assert payload["model"] == "local-model"
    assert payload["tool_choice"]["type"] == "function"
    assert payload["tool_choice"]["function"]["name"] == "record_validation"
    tool = payload["tools"][0]["function"]
    assert tool["parameters"]["required"] == ["status"]
    assert tool["parameters"]["properties"]["status"]["enum"] == ["ok"]


def test_authorization_header_masks_secret_value():
    validator = load_validator_module()

    headers = validator.headers_for_api_key("real-secret")
    display = validator.safe_headers_for_report(headers)

    assert headers["Authorization"] == "Bearer real-secret"
    assert display["Authorization"] == "Bearer <redacted>"


def test_chat_check_handles_null_content_without_exception(monkeypatch):
    validator = load_validator_module()

    def fake_post_json(url, payload, headers, timeout):
        return 0.1, {"choices": [{"message": {"content": None}}], "usage": {}}

    monkeypatch.setattr(validator, "post_json", fake_post_json)

    result = validator.check_chat("http://example.test/v1", {}, "local-model", 1)

    assert result.ok is False
    assert result.detail["content"] is None


def test_rapid_mlx_helper_is_local_telemetry_off_lab_lane():
    script = (ROOT / "scripts" / "local-ai" / "start-rapid-mlx-qwen.sh").read_text()

    assert "RAPID_MLX_TELEMETRY=0" in script
    assert "qwen3.6-35b-4bit" in script
    assert 'HOST="${RAPID_MLX_HOST:-127.0.0.1}"' in script
    assert 'PORT="${RAPID_MLX_PORT:-8010}"' in script
    assert '--host "$HOST"' in script
    assert '--port "$PORT"' in script


def test_benchmark_bakeoff_includes_rapid_mlx_candidate():
    script = (ROOT / "scripts" / "local-ai" / "benchmark-engine-bakeoff.py").read_text()

    assert '"name": "rapid-mlx-qwen36"' in script
    assert '"base_url": "http://127.0.0.1:8010/v1"' in script


def test_rollback_script_returns_to_omlx_default():
    script = (ROOT / "scripts" / "local-ai" / "rollback-hermes-mlx.sh").read_text()

    assert "rapid-mlx-qwen" in script
    assert "gemma4-gguf-coding-lane.sh\" stop" in script
    assert "http://127.0.0.1:18080/v1" in script
    assert "mlx-community--gemma-4-26b-a4b-it-4bit" in script


def test_health_checker_reads_omlx_settings_without_printing_key():
    script = (ROOT / "scripts" / "health" / "local-ai-health.py").read_text()

    assert "/ \"settings.json\"" in script
    assert "Authorization" in script
    assert "api_key" in script
    assert "print(api_key)" not in script


def test_health_checker_parses_swap_usage():
    health = load_health_module()

    parsed = health.parse_swapusage("total = 8192.00M  used = 6627.12M  free = 1564.88M  (encrypted)")

    assert parsed["total_mb"] == 8192.0
    assert parsed["used_mb"] == 6627.12
    assert parsed["free_mb"] == 1564.88
    assert parsed["used_percent"] == 80.9
    assert parsed["pressure"] == "high"


def test_health_checker_skip_chat_avoids_completion_probe(monkeypatch):
    health = load_health_module()
    calls = []

    def fake_request_json(url, **kwargs):
        calls.append((url, kwargs.get("method", "GET")))
        return {"data": [{"id": "local-model"}]}

    monkeypatch.setattr(health, "request_json", fake_request_json)

    result = health.check_endpoint("local", "http://example.test/v1", "local-model", "", skip_chat=True)

    assert result["ok"] is True
    assert result["model_found"] is True
    assert result["chat_skipped"] is True
    assert calls == [("http://example.test/v1/models", "GET")]


def test_health_checker_marks_optional_lane_stopped_as_ok():
    health = load_health_module()

    ports = [{"port": 8010, "listening": False, "listeners": []}]
    result = health.check_optional_lane(
        "rapid-mlx",
        "http://127.0.0.1:8010/v1",
        "qwen3.6-35b-4bit",
        "",
        8010,
        ports,
    )

    assert result["ok"] is True
    assert result["state"] == "stopped"
    assert result["expected"] == "manual"


def test_health_checker_checks_optional_lane_when_port_is_listening(monkeypatch):
    health = load_health_module()
    calls = []

    def fake_request_json(url, **kwargs):
        calls.append(url)
        return {"data": [{"id": "qwen3.6-35b-4bit"}]}

    monkeypatch.setattr(health, "request_json", fake_request_json)

    ports = [{"port": 8010, "listening": True, "listeners": ["rapid-mlx"]}]
    result = health.check_optional_lane(
        "rapid-mlx",
        "http://127.0.0.1:8010/v1",
        "qwen3.6-35b-4bit",
        "",
        8010,
        ports,
    )

    assert result["ok"] is True
    assert result["state"] == "running"
    assert result["model_found"] is True
    assert calls == ["http://127.0.0.1:8010/v1/models"]


def test_health_checker_reports_codex_skill_metadata(tmp_path):
    health = load_health_module()
    skill_dir = tmp_path / "gh-fix-ci"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: gh-fix-ci\ndescription: Fix CI\n---\n")

    result = health.check_codex_skills(tmp_path, ["gh-fix-ci", "missing-skill"])

    assert result["ok"] is False
    assert result["skills"]["gh-fix-ci"]["ok"] is True
    assert result["skills"]["gh-fix-ci"]["has_metadata"] is True
    assert result["skills"]["missing-skill"]["ok"] is False


def test_health_checker_accepts_quoted_skill_name_metadata(tmp_path):
    health = load_health_module()
    skill_file = tmp_path / "SKILL.md"
    skill_file.write_text('---\nname: "gh-fix-ci"\ndescription: "Fix CI"\n---\n')

    assert health.skill_has_metadata(skill_file, "gh-fix-ci") is True


def test_health_checker_reports_vscode_recommendation_health(tmp_path):
    health = load_health_module()
    extensions = tmp_path / "extensions.json"
    extensions.write_text('{"recommendations":["charliermarsh.ruff"]}\n')

    result = health.check_vscode_recommendations(extensions, ["charliermarsh.ruff", "ms-vscode.powershell"])

    assert result["ok"] is False
    assert result["extensions"]["charliermarsh.ruff"]["recommended"] is True
    assert result["extensions"]["ms-vscode.powershell"]["recommended"] is False


def test_launchagent_check_reports_missing_program(tmp_path):
    health = load_health_module()
    plist = tmp_path / "local.test.missing.plist"
    plist.write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>local.test.missing</string>
<key>ProgramArguments</key><array><string>/no/such/script.sh</string></array>
</dict></plist>
"""
    )

    result = health.check_launchagent_plist(plist)

    assert result["label"] == "local.test.missing"
    assert result["ok"] is False
    assert result["program_exists"] is False
    assert result["classification"] == "broken"
