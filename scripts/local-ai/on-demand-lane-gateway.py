#!/usr/bin/env python3
"""Wake a local model lane on first OpenAI-compatible request, then proxy it."""

from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


ROOT = Path(os.environ.get("LOCAL_AI_PLATFORM_ROOT", Path(__file__).resolve().parents[2]))
POLICY = Path(os.environ.get("LOCAL_AI_RESIDENCY_POLICY", ROOT / "config/local-ai-platform/residency-policy.json"))
LOG_FILE = Path(os.environ.get("LOCAL_AI_GATEWAY_LOG", Path.home() / ".local/state/local-ai-on-demand-gateway.log"))

LANE_ENV = {
    "gemma-gguf-coding-fallback": {"GEMMA4_GGUF_PORT": "backend_port"},
    "ornith-35b-gguf": {"ORNITH_GGUF_PORT": "backend_port"},
    "rapid-mlx-qwen36": {"RAPID_MLX_PORT": "backend_port"},
}

START_TIMEOUT_SECONDS = {
    "gemma-gguf-coding-fallback": 240,
    "ornith-35b-gguf": 300,
    "rapid-mlx-qwen36": 300,
}

HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "host",
    "content-length",
}


def log(message: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(f"{stamp} {message}\n")


def load_policy() -> dict[str, Any]:
    return json.loads(POLICY.read_text())


def all_lanes(policy: dict[str, Any]) -> list[dict[str, Any]]:
    return list(policy.get("warm_when_running", [])) + list(policy.get("on_demand_heavy_lanes", []))


def lane_by_id(policy: dict[str, Any], lane_id: str) -> dict[str, Any]:
    for lane in all_lanes(policy):
        if lane.get("id") == lane_id:
            return lane
    raise SystemExit(f"Unknown lane id in {POLICY}: {lane_id}")


def port_listening(host: str, port: int, timeout: float = 0.3) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def manager_path(lane: dict[str, Any]) -> str:
    installed = str(lane.get("installed_manager") or "")
    if installed and Path(installed).exists():
        return installed
    manager = str(lane["manager"])
    candidate = ROOT / manager
    return str(candidate)


class LaneGateway:
    def __init__(self, lane: dict[str, Any]):
        self.lane = lane
        self.lane_id = str(lane["id"])
        self.public_port = int(lane["public_port"])
        self.backend_port = int(lane["backend_port"])
        self.backend_host = "127.0.0.1"
        self.backend_base_url = str(lane["backend_base_url"]).rstrip("/")
        self.lock = threading.Lock()

    def backend_running(self) -> bool:
        return port_listening(self.backend_host, self.backend_port)

    def status(self) -> dict[str, Any]:
        return {
            "gateway": True,
            "lane": self.lane_id,
            "public_port": self.public_port,
            "backend_port": self.backend_port,
            "backend_base_url": self.backend_base_url,
            "backend_running": self.backend_running(),
            "policy": str(POLICY),
        }

    def start_backend(self) -> None:
        if self.backend_running():
            return
        with self.lock:
            if self.backend_running():
                return
            path = manager_path(self.lane)
            if not Path(path).exists():
                raise RuntimeError(f"lane manager missing: {path}")
            env = os.environ.copy()
            for env_name, field in LANE_ENV.get(self.lane_id, {}).items():
                env[env_name] = str(self.lane[field])
            log(f"starting backend lane={self.lane_id} manager={path} backend_port={self.backend_port}")
            completed = subprocess.run([path, "start"], env=env, text=True, capture_output=True, timeout=START_TIMEOUT_SECONDS.get(self.lane_id, 240), check=False)
            if completed.returncode != 0:
                log(f"backend start failed lane={self.lane_id} rc={completed.returncode} stderr={completed.stderr.strip()}")
                raise RuntimeError(f"backend start failed for {self.lane_id}: {completed.stderr.strip() or completed.stdout.strip()}")
            log(f"backend lane ready lane={self.lane_id}")

    def proxy(self, handler: BaseHTTPRequestHandler) -> None:
        self.start_backend()
        target = f"http://127.0.0.1:{self.backend_port}{handler.path}"
        body = None
        length = handler.headers.get("Content-Length")
        if length:
            body = handler.rfile.read(int(length))
        headers = {k: v for k, v in handler.headers.items() if k.lower() not in HOP_BY_HOP_HEADERS}
        req = urllib.request.Request(target, data=body, headers=headers, method=handler.command)
        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                data = resp.read()
                handler.send_response(resp.status)
                for key, value in resp.headers.items():
                    if key.lower() not in HOP_BY_HOP_HEADERS:
                        handler.send_header(key, value)
                handler.send_header("Content-Length", str(len(data)))
                handler.end_headers()
                handler.wfile.write(data)
        except urllib.error.HTTPError as exc:
            data = exc.read()
            handler.send_response(exc.code)
            for key, value in exc.headers.items():
                if key.lower() not in HOP_BY_HOP_HEADERS:
                    handler.send_header(key, value)
            handler.send_header("Content-Length", str(len(data)))
            handler.end_headers()
            handler.wfile.write(data)


def build_handler(gateway: LaneGateway) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        server_version = "LocalAIOnDemandGateway/1.0"

        def log_message(self, fmt: str, *args: Any) -> None:
            log(f"{self.client_address[0]} {self.command} {self.path} {fmt % args}")

        def write_json(self, status: int, payload: dict[str, Any]) -> None:
            data = json.dumps(payload, indent=2).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def handle_any(self) -> None:
            if self.path in {"/__lane_status", "/health"}:
                self.write_json(200, gateway.status())
                return
            try:
                gateway.proxy(self)
            except Exception as exc:
                log(f"request failed lane={gateway.lane_id} path={self.path} error={exc}")
                self.write_json(503, {"error": str(exc), "lane": gateway.lane_id, "gateway": True})

        def do_GET(self) -> None:
            self.handle_any()

        def do_POST(self) -> None:
            self.handle_any()

        def do_OPTIONS(self) -> None:
            self.handle_any()

    return Handler


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lane", required=True, help="Lane id from residency-policy.json")
    args = parser.parse_args()

    policy = load_policy()
    lane = lane_by_id(policy, args.lane)
    gateway = LaneGateway(lane)
    server = ThreadingHTTPServer(("127.0.0.1", gateway.public_port), build_handler(gateway))
    log(f"gateway listening lane={gateway.lane_id} public_port={gateway.public_port} backend_port={gateway.backend_port}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
