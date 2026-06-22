#!/usr/bin/env python3
"""Validate OpenAI-compatible local Hermes/MLX endpoints."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


DEFAULT_OUT = Path("docs/autonomous-modernization/hermes-mlx-validation-results.json")


@dataclass
class CheckResult:
    name: str
    ok: bool
    seconds: float
    detail: dict[str, Any]


def headers_for_api_key(api_key: str | None) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def safe_headers_for_report(headers: dict[str, str]) -> dict[str, str]:
    safe = dict(headers)
    if "Authorization" in safe:
        safe["Authorization"] = "Bearer <redacted>"
    return safe


def tool_call_payload(model: str) -> dict[str, Any]:
    return {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": "Call the validation tool with status ok. Do not answer in prose.",
            }
        ],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "record_validation",
                    "description": "Record that local tool calling works.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["ok"],
                            }
                        },
                        "required": ["status"],
                        "additionalProperties": False,
                    },
                },
            }
        ],
        "tool_choice": {
            "type": "function",
            "function": {"name": "record_validation"},
        },
        "max_tokens": 96,
        "temperature": 0,
    }


def post_json(url: str, payload: dict[str, Any], headers: dict[str, str], timeout: int) -> tuple[float, dict[str, Any]]:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return time.perf_counter() - started, json.loads(resp.read().decode("utf-8"))


def get_json(url: str, headers: dict[str, str], timeout: int) -> tuple[float, dict[str, Any]]:
    req = urllib.request.Request(url, headers=headers, method="GET")
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return time.perf_counter() - started, json.loads(resp.read().decode("utf-8"))


def chat_payload(model: str) -> dict[str, Any]:
    return {
        "model": model,
        "messages": [{"role": "user", "content": "Reply with exactly: OK"}],
        "max_tokens": 8,
        "temperature": 0,
    }


def result_from_exception(name: str, started: float, exc: Exception) -> CheckResult:
    detail = {"error": str(exc)}
    if isinstance(exc, urllib.error.HTTPError):
        detail["status"] = exc.code
        try:
            detail["body"] = exc.read().decode("utf-8", "replace")[:1000]
        except Exception:
            pass
    return CheckResult(name=name, ok=False, seconds=round(time.perf_counter() - started, 6), detail=detail)


def check_models(base_url: str, headers: dict[str, str], model: str, timeout: int) -> CheckResult:
    started = time.perf_counter()
    try:
        seconds, data = get_json(f"{base_url.rstrip('/')}/models", headers, timeout)
        model_ids = [item.get("id") for item in data.get("data", [])]
        return CheckResult(
            "models",
            model in model_ids,
            round(seconds, 6),
            {"model_found": model in model_ids, "model_count": len(model_ids), "model_ids": model_ids},
        )
    except Exception as exc:
        return result_from_exception("models", started, exc)


def check_chat(base_url: str, headers: dict[str, str], model: str, timeout: int) -> CheckResult:
    started = time.perf_counter()
    try:
        seconds, data = post_json(f"{base_url.rstrip('/')}/chat/completions", chat_payload(model), headers, timeout)
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return CheckResult(
            "chat_completion",
            isinstance(content, str) and content.strip().rstrip(".") == "OK",
            round(seconds, 6),
            {"content": content, "usage": data.get("usage", {})},
        )
    except Exception as exc:
        return result_from_exception("chat_completion", started, exc)


def check_tool_call(base_url: str, headers: dict[str, str], model: str, timeout: int) -> CheckResult:
    started = time.perf_counter()
    try:
        seconds, data = post_json(f"{base_url.rstrip('/')}/chat/completions", tool_call_payload(model), headers, timeout)
        message = data.get("choices", [{}])[0].get("message", {})
        tool_calls = message.get("tool_calls") or []
        ok = any(
            call.get("function", {}).get("name") == "record_validation"
            and json.loads(call.get("function", {}).get("arguments") or "{}").get("status") == "ok"
            for call in tool_calls
        )
        return CheckResult(
            "tool_call",
            ok,
            round(seconds, 6),
            {"tool_call_count": len(tool_calls), "content_present": bool(message.get("content")), "usage": data.get("usage", {})},
        )
    except Exception as exc:
        return result_from_exception("tool_call", started, exc)


def build_report(args: argparse.Namespace, headers: dict[str, str], results: list[CheckResult]) -> dict[str, Any]:
    return {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "endpoint": {
            "name": args.name,
            "base_url": args.base_url,
            "model": args.model,
            "headers": safe_headers_for_report(headers),
        },
        "checks": [asdict(result) for result in results],
        "ok": all(result.ok for result in results),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", default="omlx", help="Endpoint label for reports.")
    parser.add_argument("--base-url", default="http://127.0.0.1:18080/v1")
    parser.add_argument("--model", default="mlx-community--gemma-4-26b-a4b-it-4bit")
    parser.add_argument("--api-key", default=os.environ.get("OMLX_API_KEY", "mlx-local"))
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--skip-tool-call", action="store_true", help="Use only when the endpoint does not support tools.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    headers = headers_for_api_key(args.api_key)
    results = [
        check_models(args.base_url, headers, args.model, args.timeout),
        check_chat(args.base_url, headers, args.model, args.timeout),
    ]
    if not args.skip_tool_call:
        results.append(check_tool_call(args.base_url, headers, args.model, args.timeout))
    report = build_report(args, headers, results)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
