from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PORT_MAP = ROOT / "config" / "apple-container" / "port-map.json"
RUNTIME_PROFILES = ROOT / "config" / "runtime-profiles"


def load_health_module():
    path = ROOT / "scripts" / "health" / "local-ai-health.py"
    spec = importlib.util.spec_from_file_location("local_ai_health_apple_container", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_port_map_uses_isolated_localhost_range():
    data = json.loads(PORT_MAP.read_text())
    start = data["policy"]["reserved_range"]["start"]
    end = data["policy"]["reserved_range"]["end"]
    production_ports = set(data["policy"]["production_ports"])
    host_ports = [service["host_port"] for service in data["services"]]

    assert start == 19000
    assert end == 19999
    assert len(host_ports) == len(set(host_ports))
    assert not production_ports.intersection(host_ports)
    assert all(service["name"].startswith("ac-") for service in data["services"])
    assert all(service["host"] == "127.0.0.1" for service in data["services"])
    assert all(start <= port <= end for port in host_ports)


def test_apple_container_health_reports_missing_cli(monkeypatch, tmp_path):
    health = load_health_module()
    port_map = tmp_path / "port-map.json"
    port_map.write_text(PORT_MAP.read_text())
    monkeypatch.setattr(health.shutil, "which", lambda name: None)

    result = health.check_apple_container(port_map)

    assert result["installed"] is False
    assert result["ok"] is False
    assert "not installed" in result["error"]


def test_apple_container_health_fails_enabled_service_when_port_is_stopped(monkeypatch, tmp_path):
    health = load_health_module()
    port_map = tmp_path / "port-map.json"
    port_map.write_text(PORT_MAP.read_text())
    monkeypatch.setattr(health.shutil, "which", lambda name: "/usr/local/bin/container")
    monkeypatch.setattr(health, "command_output", lambda args, timeout=15: (True, "ok"))
    monkeypatch.setattr(health, "check_ports", lambda ports: [{"port": 19091, "listening": False, "listeners": []}])

    result = health.check_apple_container(port_map)

    assert result["ok"] is False
    assert "enabled service ac-ntfy is not listening on 19091" in result["findings"]


def test_docker_status_reports_missing_cli(monkeypatch):
    health = load_health_module()
    monkeypatch.setattr(health.shutil, "which", lambda name: None)

    result = health.check_docker()

    assert result["installed"] is False
    assert result["ok"] is False


@pytest.mark.parametrize("field", ["name", "host_port", "container_port", "health_url", "storage", "status"])
def test_all_services_have_required_operational_fields(field):
    data = json.loads(PORT_MAP.read_text())

    assert all(field in service for service in data["services"])


def test_ntfy_is_first_enabled_low_risk_mirror():
    data = json.loads(PORT_MAP.read_text())
    enabled = [service for service in data["services"] if service.get("enabled") is True]

    assert [service["name"] for service in enabled] == ["ac-ntfy"]
    ntfy = enabled[0]
    assert ntfy["host_port"] == 19091
    assert ntfy["container_port"] == 80
    assert ntfy["status"] == "dual-runtime-validated"
    assert ntfy["risk"] == "low"


def test_runtime_profiles_define_required_modes_without_secret_values():
    expected = {
        "production.json",
        "docker-current.json",
        "apple-container-pilot.json",
        "side-by-side.json",
        "native-ai.json",
        "rollback-safe.json",
    }

    assert {path.name for path in RUNTIME_PROFILES.glob("*.json")} == expected
    for path in RUNTIME_PROFILES.glob("*.json"):
        profile = json.loads(path.read_text())
        assert profile["secrets_source"] == "1Password: Boneman"
        assert "secret" not in json.dumps(profile).lower().replace("secrets_source", "")
        assert "token" not in json.dumps(profile).lower()
        assert profile["health_checks"]


@pytest.mark.parametrize(
    "script",
    [
        "start-all.sh",
        "stop-all.sh",
        "restart-all.sh",
        "status-all.sh",
        "health-all.sh",
        "logs-all.sh",
        "compare-all.sh",
        "repair-all.sh",
        "self-heal.sh",
    ],
)
def test_dual_runtime_operational_scripts_exist_and_use_port_map(script):
    path = ROOT / "scripts" / "apple-container" / script

    assert path.is_file()
    assert "config/apple-container/port-map.json" in path.read_text()


def test_start_all_only_starts_enabled_services():
    script = (ROOT / "scripts" / "apple-container" / "start-all.sh").read_text()

    assert 'select(.enabled == true)' in script
    assert "container run" in script
    assert "ac-ntfy" in script
    assert "0.0.0.0" not in script
