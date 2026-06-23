#!/usr/bin/env python3
"""Health checks for the local AI platform lanes."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_MODEL = "mlx-community--gemma-4-26b-a4b-it-4bit"


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
        return {"swapusage": out}
    except Exception as exc:
        return {"error": str(exc)}


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
