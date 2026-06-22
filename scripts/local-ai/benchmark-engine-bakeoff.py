#!/usr/bin/env python3
"""Benchmark the operational MLX/oMLX and llama.cpp OpenAI-compatible lanes."""

from __future__ import annotations

import json
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path


OUT = Path("docs/autonomous-modernization/benchmark-results.json")

PROMPTS = {
    "coding_patch": (
        "You are auditing a Python CLI. Write a compact function that parses a "
        "unified diff and returns changed file paths, then list three edge cases."
    ),
    "agent_plan": (
        "Given a repo with dirty docs and a local model server, produce a concise "
        "plan with validation steps and rollback commands."
    ),
    "context_scale": "\n".join(
        [f"file_{i}.py changed: function_{i} validates endpoint behavior." for i in range(220)]
    )
    + "\nSummarize the riskiest integration points in five bullets.",
}

ENGINES = [
    {
        "name": "omlx-mlx",
        "base_url": "http://127.0.0.1:18080/v1",
        "model": "mlx-community--gemma-4-26b-a4b-it-4bit",
        "headers": {"Authorization": "Bearer mlx-local"},
        "process_pattern": "oMLX|omlx-server",
    },
    {
        "name": "llama-cpp-gguf",
        "base_url": "http://127.0.0.1:8002/v1",
        "model": "gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf",
        "headers": {},
        "process_pattern": "llama-server",
    },
]


def post_json(url: str, payload: dict, headers: dict[str, str], timeout: int = 240) -> tuple[float, dict]:
    body = json.dumps(payload).encode()
    req_headers = {"Content-Type": "application/json", **headers}
    req = urllib.request.Request(url, data=body, headers=req_headers, method="POST")
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode())
    return time.perf_counter() - started, data


def stream_chat(url: str, payload: dict, headers: dict[str, str], timeout: int = 240) -> dict:
    stream_payload = dict(payload)
    stream_payload["stream"] = True
    body = json.dumps(stream_payload).encode()
    req_headers = {"Content-Type": "application/json", "Accept": "text/event-stream", **headers}
    req = urllib.request.Request(url, data=body, headers=req_headers, method="POST")
    started = time.perf_counter()
    first = None
    chunks = 0
    chars = 0
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        for raw in resp:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data: "):
                continue
            value = line[6:]
            if value == "[DONE]":
                break
            chunks += 1
            if first is None:
                first = time.perf_counter()
            try:
                event = json.loads(value)
            except json.JSONDecodeError:
                continue
            delta = event.get("choices", [{}])[0].get("delta", {})
            text = delta.get("content") or delta.get("reasoning_content") or ""
            chars += len(text)
    ended = time.perf_counter()
    return {
        "ttft_s": None if first is None else round(first - started, 6),
        "stream_total_s": round(ended - started, 6),
        "stream_chunks": chunks,
        "stream_chars": chars,
    }


def process_snapshot(pattern: str) -> list[dict]:
    try:
        out = subprocess.check_output(
            ["ps", "-axo", "pid,rss,%cpu,etime,command"], text=True, stderr=subprocess.DEVNULL
        )
    except subprocess.SubprocessError:
        return []
    rows = []
    for line in out.splitlines()[1:]:
        if pattern.lower().replace("|", " ") and any(part.lower() in line.lower() for part in pattern.split("|")):
            parts = line.split(None, 4)
            if len(parts) == 5:
                rows.append(
                    {
                        "pid": parts[0],
                        "rss_kib": int(parts[1]),
                        "cpu_percent": parts[2],
                        "etime": parts[3],
                        "command": parts[4][:220],
                    }
                )
    return rows


def run_engine(engine: dict) -> dict:
    url = f"{engine['base_url']}/chat/completions"
    result = {"engine": engine["name"], "model": engine["model"], "runs": []}
    for workload, prompt in PROMPTS.items():
        payload = {
            "model": engine["model"],
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 192,
            "temperature": 0,
        }
        run = {"workload": workload}
        try:
            run.update(stream_chat(url, payload, engine["headers"]))
            total_s, data = post_json(url, payload, engine["headers"])
        except urllib.error.URLError as exc:
            run["error"] = str(exc)
            result["runs"].append(run)
            continue
        usage = data.get("usage") or {}
        timings = data.get("timings") or {}
        completion_tokens = usage.get("completion_tokens") or usage.get("output_tokens") or timings.get("predicted_n")
        prompt_tokens = usage.get("prompt_tokens") or usage.get("input_tokens") or timings.get("prompt_n")
        run.update(
            {
                "nonstream_total_s": round(total_s, 6),
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "output_tok_s_wall": round(completion_tokens / total_s, 3) if completion_tokens and total_s else None,
                "tpot_s_wall": round(total_s / completion_tokens, 6) if completion_tokens and total_s else None,
                "usage": usage,
                "timings": timings,
            }
        )
        result["runs"].append(run)
    result["process_snapshot"] = process_snapshot(engine["process_pattern"])
    return result


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    results = {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "methodology": "OpenAI-compatible server benchmark for operational agent paths; streaming for TTFT, non-stream for usage/timing metadata.",
        "engines": [run_engine(engine) for engine in ENGINES],
    }
    OUT.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
