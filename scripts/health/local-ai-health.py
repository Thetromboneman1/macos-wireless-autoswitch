#!/usr/bin/env python3
"""Health checks for the local AI platform lanes."""

from __future__ import annotations

import argparse
import json
import os
import plistlib
import re
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_MODEL = "mlx-community--gemma-4-26b-a4b-it-4bit"
DEFAULT_PORTS = (18080, 8002, 8010)
PROCESS_PATTERNS = ("oMLX", "omlx-server", "llama-server", "rapid-mlx", "Docker", "LM Studio")


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


def check_endpoint(name: str, base_url: str, model: str, api_key: str) -> dict[str, Any]:
    started = time.perf_counter()
    result: dict[str, Any] = {"name": name, "base_url": base_url, "model": model, "ok": False}
    try:
        models = request_json(f"{base_url.rstrip('/')}/models", api_key=api_key)
        ids = [item.get("id") for item in models.get("data", [])]
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
                "model_count": len(ids),
                "model_found": model in ids,
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="Write JSON report to this path.")
    parser.add_argument("--skip-chat", action="store_true", help="Reserved for future endpoint-only mode.")
    args = parser.parse_args()

    api_key = read_omlx_key()
    report = {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "system": vm_stat(),
        "ports": check_ports(),
        "processes": process_snapshot(),
        "launchagents": check_launchagents(),
        "lanes": [
            check_endpoint("omlx-production", "http://127.0.0.1:18080/v1", DEFAULT_MODEL, api_key),
        ],
    }
    report["ok"] = all(lane.get("ok") for lane in report["lanes"])
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
