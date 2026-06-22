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
