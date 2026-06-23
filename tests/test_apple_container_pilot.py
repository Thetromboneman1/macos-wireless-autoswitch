from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PORT_MAP = ROOT / "config" / "apple-container" / "port-map.json"


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


@pytest.mark.parametrize("field", ["name", "host_port", "container_port", "health_url", "storage", "status"])
def test_all_services_have_required_operational_fields(field):
    data = json.loads(PORT_MAP.read_text())

    assert all(field in service for service in data["services"])
