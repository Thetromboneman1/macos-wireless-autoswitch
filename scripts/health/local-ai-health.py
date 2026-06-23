#!/usr/bin/env python3
"""Health checks for the local AI platform lanes."""

from __future__ import annotations

import argparse
import json
import os
import plistlib
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_MODEL = "mlx-community--gemma-4-26b-a4b-it-4bit"
DEFAULT_PORTS = (18080, 8002, 8010)
APPLE_CONTAINER_PORT_MAP = Path.cwd() / "config" / "apple-container" / "port-map.json"
PROCESS_PATTERNS = ("oMLX", "omlx-server", "llama-server", "rapid-mlx", "Docker", "LM Studio")
EXPECTED_CODEX_SKILLS = (
    "gh-address-comments",
    "gh-fix-ci",
    "migrate-to-codex",
    "openai-docs",
    "playwright",
    "playwright-interactive",
    "security-best-practices",
    "security-ownership-map",
    "security-threat-model",
    "yeet",
)
EXPECTED_VSCODE_RECOMMENDATIONS = (
    "charliermarsh.ruff",
    "davidanson.vscode-markdownlint",
    "hashicorp.terraform",
    "ms-kubernetes-tools.vscode-kubernetes-tools",
    "ms-vscode.powershell",
    "tamasfe.even-better-toml",
)


def read_omlx_key() -> str:
    env_key = os.environ.get("OMLX_API_KEY", "").strip()
    if env_key:
        return env_key
    settings = Path.home() / ".omlx" / "settings.json"
    try:
        return json.loads(settings.read_text()).get("auth", {}).get("api_key", "")
    except Exception:
        return ""


def request_json(url: str, *, method: str = "GET", payload: dict[str, Any] | None = None, api_key: str = "", timeout: int = 15) -> dict[str, Any]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def vm_stat() -> dict[str, Any]:
    try:
        out = subprocess.check_output(["sysctl", "-n", "vm.swapusage"], text=True).strip()
        return {"swapusage": out, "swap": parse_swapusage(out)}
    except Exception as exc:
        return {"error": str(exc)}


def parse_swapusage(value: str) -> dict[str, Any]:
    fields = {}
    for name in ("total", "used", "free"):
        match = re.search(rf"{name}\s*=\s*([0-9.]+)M", value)
        fields[f"{name}_mb"] = float(match.group(1)) if match else None
    total = fields.get("total_mb") or 0
    used = fields.get("used_mb") or 0
    used_percent = round((used / total) * 100, 1) if total else None
    if used_percent is None:
        pressure = "unknown"
    elif used_percent >= 75:
        pressure = "high"
    elif used_percent >= 40:
        pressure = "elevated"
    else:
        pressure = "normal"
    fields["used_percent"] = used_percent
    fields["pressure"] = pressure
    return fields


def check_launchagent_plist(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"path": str(path), "ok": False}
    try:
        data = load_plist(path)
    except Exception as exc:
        result.update({"label": path.stem, "error": str(exc), "classification": "broken"})
        return result

    label = str(data.get("Label") or path.stem)
    args = data.get("ProgramArguments")
    program = data.get("Program")
    if isinstance(args, list) and args:
        program = str(args[0])
    elif program:
        program = str(program)
    else:
        program = ""
    program_exists = bool(program and Path(program).exists())
    logs = {
        "stdout": data.get("StandardOutPath", ""),
        "stderr": data.get("StandardErrorPath", ""),
    }
    classification = "healthy" if program_exists else "broken"
    result.update(
        {
            "label": label,
            "program": program,
            "program_exists": program_exists,
            "run_at_load": bool(data.get("RunAtLoad", False)),
            "start_interval": data.get("StartInterval"),
            "logs": logs,
            "classification": classification,
            "ok": program_exists,
        }
    )
    return result


def load_plist(path: Path) -> dict[str, Any]:
    try:
        data = plistlib.loads(path.read_bytes())
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    out = subprocess.check_output(["plutil", "-convert", "json", "-o", "-", str(path)], text=True)
    data = json.loads(out)
    if not isinstance(data, dict):
        raise ValueError("plist root is not a dictionary")
    return data


def check_launchagents(directory: Path | None = None) -> list[dict[str, Any]]:
    launch_dir = directory or (Path.home() / "Library" / "LaunchAgents")
    return [check_launchagent_plist(path) for path in sorted(launch_dir.glob("*.plist"))]


def check_ports(ports: tuple[int, ...] = DEFAULT_PORTS) -> list[dict[str, Any]]:
    rows = []
    for port in ports:
        try:
            out = subprocess.check_output(["lsof", "-nP", f"-iTCP:{port}", "-sTCP:LISTEN"], text=True, stderr=subprocess.DEVNULL)
            listeners = [line for line in out.splitlines()[1:] if line.strip()]
            rows.append({"port": port, "listening": bool(listeners), "listeners": listeners[:5]})
        except subprocess.CalledProcessError:
            rows.append({"port": port, "listening": False, "listeners": []})
    return rows


def command_output(args: list[str], timeout: int = 15) -> tuple[bool, str]:
    try:
        out = subprocess.check_output(args, text=True, stderr=subprocess.STDOUT, timeout=timeout)
        return True, out.strip()
    except Exception as exc:
        output = getattr(exc, "output", "")
        message = str(exc)
        if output:
            message = f"{message}: {output.strip()}"
        return False, message


def check_apple_container(port_map: Path | None = None) -> dict[str, Any]:
    path = port_map or APPLE_CONTAINER_PORT_MAP
    result: dict[str, Any] = {
        "installed": False,
        "system_running": False,
        "port_map": str(path),
        "ok": True,
        "services": [],
    }
    container = shutil.which("container")
    result["installed"] = bool(container)
    result["container_path"] = container or ""
    if not container:
        result.update({"ok": False, "error": "container CLI is not installed"})
        return result

    version_ok, version = command_output([container, "--version"])
    result["version"] = version
    status_ok, status = command_output([container, "system", "status"])
    result["system_running"] = status_ok
    result["system_status"] = status
    if not version_ok:
        result["ok"] = False

    try:
        data = json.loads(path.read_text())
    except Exception as exc:
        result.update({"ok": False, "error": f"cannot read port map: {exc}"})
        return result

    service_ports = tuple(int(item["host_port"]) for item in data.get("services", []))
    observed_ports = check_ports(service_ports)
    observed_by_port = {row["port"]: row for row in observed_ports}
    production_ports = {int(port) for port in data.get("policy", {}).get("production_ports", [])}
    prefix = data.get("policy", {}).get("pilot_prefix", "ac-")
    seen_ports: set[int] = set()
    findings = []
    for item in data.get("services", []):
        port = int(item["host_port"])
        result["services"].append(
            {
                "name": item["name"],
                "host": item.get("host"),
                "host_port": port,
                "enabled": bool(item.get("enabled", False)),
                "status": item.get("status"),
                "listening": bool(observed_by_port.get(port, {}).get("listening")),
                "health_url": item.get("health_url"),
            }
        )
        if not str(item.get("name", "")).startswith(prefix):
            findings.append(f"{item.get('name')} does not use the pilot prefix")
        if item.get("host") != "127.0.0.1":
            findings.append(f"{item.get('name')} does not bind to 127.0.0.1")
        if port in seen_ports:
            findings.append(f"duplicate pilot port {port}")
        if port in production_ports:
            findings.append(f"pilot port {port} reuses a production port")
        if item.get("enabled") is True and not bool(observed_by_port.get(port, {}).get("listening")):
            findings.append(f"enabled service {item.get('name')} is not listening on {port}")
        seen_ports.add(port)
    result["findings"] = findings
    result["ok"] = bool(result["ok"] and not findings)
    return result


def check_docker() -> dict[str, Any]:
    result: dict[str, Any] = {"installed": False, "ok": False}
    docker = shutil.which("docker")
    result["installed"] = bool(docker)
    result["docker_path"] = docker or ""
    if not docker:
        result["error"] = "docker CLI is not installed"
        return result
    version_ok, version = command_output([docker, "version", "--format", "{{json .}}"])
    ps_ok, ps_output = command_output([docker, "ps", "--format", "{{.Names}}\t{{.Status}}\t{{.Ports}}"])
    result.update(
        {
            "version_ok": version_ok,
            "version": version,
            "services_ok": ps_ok,
            "services": [line for line in ps_output.splitlines() if line.strip()] if ps_ok else [],
            "ok": version_ok and ps_ok,
        }
    )
    if not ps_ok:
        result["error"] = ps_output
    return result


def process_snapshot() -> list[dict[str, Any]]:
    try:
        out = subprocess.check_output(["ps", "-axo", "pid,rss,%mem,%cpu,etime,command"], text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return []
    rows = []
    for line in out.splitlines()[1:]:
        if not any(pattern.lower() in line.lower() for pattern in PROCESS_PATTERNS):
            continue
        parts = line.split(None, 5)
        if len(parts) != 6:
            continue
        rows.append(
            {
                "pid": int(parts[0]),
                "rss_kib": int(parts[1]),
                "mem_percent": parts[2],
                "cpu_percent": parts[3],
                "etime": parts[4],
                "command": parts[5][:220],
            }
        )
    return rows


def check_endpoint(name: str, base_url: str, model: str, api_key: str, *, skip_chat: bool = False) -> dict[str, Any]:
    started = time.perf_counter()
    result: dict[str, Any] = {"name": name, "base_url": base_url, "model": model, "ok": False}
    try:
        models = request_json(f"{base_url.rstrip('/')}/models", api_key=api_key)
        ids = [item.get("id") for item in models.get("data", [])]
        result.update({"model_count": len(ids), "model_found": model in ids})
        if skip_chat:
            result.update({"ok": model in ids, "chat_skipped": True})
        else:
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": "Reply with exactly OK."}],
                "max_tokens": 8,
                "temperature": 0,
            }
            chat_started = time.perf_counter()
            chat = request_json(f"{base_url.rstrip('/')}/chat/completions", method="POST", payload=payload, api_key=api_key)
            content = chat.get("choices", [{}])[0].get("message", {}).get("content", "")
            result.update(
                {
                    "ok": model in ids and isinstance(content, str) and content.strip().rstrip(".") == "OK",
                    "chat_seconds": round(time.perf_counter() - chat_started, 6),
                    "usage": chat.get("usage", {}),
                }
            )
    except Exception as exc:
        result["error"] = str(exc)
        if isinstance(exc, urllib.error.HTTPError):
            result["status"] = exc.code
    result["seconds"] = round(time.perf_counter() - started, 6)
    return result


def port_is_listening(ports: list[dict[str, Any]], port: int) -> bool:
    return any(row.get("port") == port and row.get("listening") for row in ports)


def check_optional_lane(
    name: str,
    base_url: str,
    model: str,
    api_key: str,
    port: int,
    ports: list[dict[str, Any]],
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "name": name,
        "base_url": base_url,
        "model": model,
        "port": port,
        "expected": "manual",
    }
    if not port_is_listening(ports, port):
        result.update({"ok": True, "state": "stopped"})
        return result

    started = time.perf_counter()
    result["state"] = "running"
    try:
        models = request_json(f"{base_url.rstrip('/')}/models", api_key=api_key)
        ids = [item.get("id") for item in models.get("data", [])]
        result.update({"ok": bool(ids), "model_count": len(ids), "model_found": model in ids})
    except Exception as exc:
        result["ok"] = False
        result["error"] = str(exc)
        if isinstance(exc, urllib.error.HTTPError):
            result["status"] = exc.code
    result["seconds"] = round(time.perf_counter() - started, 6)
    return result


def skill_has_metadata(path: Path, expected_name: str) -> bool:
    try:
        lines = path.read_text().splitlines()
    except Exception:
        return False
    if not lines or lines[0].strip() != "---":
        return False
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return False
    metadata = {}
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata.get("name") == expected_name and bool(metadata.get("description"))


def check_codex_skills(
    skills_root: Path | None = None,
    expected_skills: tuple[str, ...] | list[str] = EXPECTED_CODEX_SKILLS,
) -> dict[str, Any]:
    root = skills_root or (Path.home() / ".codex" / "skills")
    skills = {}
    for name in expected_skills:
        skill_file = root / name / "SKILL.md"
        exists = skill_file.is_file()
        has_metadata = skill_has_metadata(skill_file, name) if exists else False
        skills[name] = {
            "path": str(skill_file),
            "exists": exists,
            "has_metadata": has_metadata,
            "ok": exists and has_metadata,
        }
    return {"root": str(root), "ok": all(item["ok"] for item in skills.values()), "skills": skills}


def check_vscode_recommendations(
    extensions_json: Path | None = None,
    expected_extensions: tuple[str, ...] | list[str] = EXPECTED_VSCODE_RECOMMENDATIONS,
) -> dict[str, Any]:
    path = extensions_json or (Path.cwd() / ".vscode" / "extensions.json")
    try:
        data = json.loads(path.read_text())
        recommendations = {str(item).lower() for item in data.get("recommendations", [])}
    except Exception as exc:
        return {"path": str(path), "ok": False, "error": str(exc), "extensions": {}}

    extensions = {}
    for extension in expected_extensions:
        recommended = extension.lower() in recommendations
        extensions[extension] = {"recommended": recommended, "ok": recommended}
    return {"path": str(path), "ok": all(item["ok"] for item in extensions.values()), "extensions": extensions}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="Write JSON report to this path.")
    parser.add_argument("--skip-chat", action="store_true", help="Check /v1/models without sending a chat completion.")
    parser.add_argument("--production-only", action="store_true", help="Skip Apple Container pilot checks.")
    parser.add_argument("--docker-only", action="store_true", help="Only report Docker Desktop service state.")
    parser.add_argument("--apple-container-only", action="store_true", help="Only report Apple Container pilot checks.")
    parser.add_argument("--side-by-side", action="store_true", help="Report production lanes and Apple Container pilot state.")
    args = parser.parse_args()

    api_key = read_omlx_key()
    ports = check_ports()
    report: dict[str, Any] = {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "system": vm_stat(),
    }
    if args.docker_only:
        report["docker"] = check_docker()
    elif not args.apple_container_only:
        report.update(
            {
                "ports": ports,
                "processes": process_snapshot(),
                "launchagents": check_launchagents(),
                "lanes": [
                    check_endpoint("omlx-production", "http://127.0.0.1:18080/v1", DEFAULT_MODEL, api_key, skip_chat=args.skip_chat),
                    check_optional_lane(
                        "llama-cpp-gguf",
                        "http://127.0.0.1:8002/v1",
                        "gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf",
                        "",
                        8002,
                        ports,
                    ),
                    check_optional_lane("rapid-mlx", "http://127.0.0.1:8010/v1", "qwen3.6-35b-4bit", "", 8010, ports),
                ],
                "codex_skills": check_codex_skills(),
                "vscode_recommendations": check_vscode_recommendations(),
                "docker": check_docker(),
            }
        )
    if not args.production_only:
        report["apple_container"] = check_apple_container()
    report["ok"] = (
        all(lane.get("ok") for lane in report.get("lanes", []))
        and report.get("codex_skills", {"ok": True}).get("ok", False)
        and report.get("vscode_recommendations", {"ok": True}).get("ok", False)
        and report.get("docker", {"ok": True}).get("ok", False)
        and report.get("apple_container", {"ok": True}).get("ok", False)
    )
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
