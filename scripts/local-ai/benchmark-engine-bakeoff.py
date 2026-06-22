#!/usr/bin/env python3
"""Benchmark the operational MLX/oMLX, Rapid-MLX, and llama.cpp lanes."""

from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


OUT = Path(os.environ.get("LOCAL_AI_BENCH_OUTPUT", "docs/autonomous-modernization/benchmark-results.json"))

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
        [f"file_{i}.py changed: function_{i} validates endpoint behavior." for i in range(80)]
    )
    + "\nSummarize the riskiest integration points in five bullets.",
}

LONG_CONTEXT_PROMPTS = {
    "context_moderate": "\n".join(
        [f"module_{i}.py owns service_{i}; validate model routing and rollback." for i in range(180)]
    )
    + "\nIdentify routing, MCP, secret, and rollback risks in seven bullets.",
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
    {
        "name": "rapid-mlx-qwen36",
        "base_url": "http://127.0.0.1:8010/v1",
        "model": "qwen3.6-35b-4bit",
        "headers": {},
        "process_pattern": "rapid-mlx",
    },
]


def post_json(url: str, payload: dict, headers: dict[str, str], timeout: int = 90) -> tuple[float, dict]:
    body = json.dumps(payload).encode()
    req_headers = {"Content-Type": "application/json", **headers}
    req = urllib.request.Request(url, data=body, headers=req_headers, method="POST")
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode())
    return time.perf_counter() - started, data


def stream_chat(url: str, payload: dict, headers: dict[str, str], timeout: int = 90) -> dict:
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


def total_rss_kib(snapshot: list[dict]) -> int:
    return sum(row["rss_kib"] for row in snapshot)


def single_completion(engine: dict, workload: str, prompt: str, max_tokens: int = 96) -> dict:
    url = f"{engine['base_url']}/chat/completions"
    payload = {
        "model": engine["model"],
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0,
    }
    run = {"workload": workload}
    before = process_snapshot(engine["process_pattern"])
    try:
        run.update(stream_chat(url, payload, engine["headers"]))
        total_s, data = post_json(url, payload, engine["headers"])
    except urllib.error.URLError as exc:
        run["error"] = str(exc)
        return run
    after = process_snapshot(engine["process_pattern"])
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
            "rss_before_kib": total_rss_kib(before),
            "rss_after_kib": total_rss_kib(after),
            "rss_delta_kib": total_rss_kib(after) - total_rss_kib(before),
            "usage": usage,
            "timings": timings,
        }
    )
    return run


def run_engine(engine: dict) -> dict:
    result = {
        "engine": engine["name"],
        "model": engine["model"],
        "runs": [],
        "context_scaling": [],
        "concurrency": [],
    }
    for workload, prompt in PROMPTS.items():
        result["runs"].append(single_completion(engine, workload, prompt))
    for workload, prompt in LONG_CONTEXT_PROMPTS.items():
        result["context_scaling"].append(single_completion(engine, workload, prompt, max_tokens=96))
    for concurrency in (2,):
        prompt = PROMPTS["coding_patch"]
        started = time.perf_counter()
        before = process_snapshot(engine["process_pattern"])
        runs = []
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [
                executor.submit(single_completion, engine, f"concurrency_{concurrency}_{i}", prompt, 64)
                for i in range(concurrency)
            ]
            for future in as_completed(futures):
                runs.append(future.result())
        after = process_snapshot(engine["process_pattern"])
        completed = time.perf_counter() - started
        total_completion_tokens = sum(run.get("completion_tokens") or 0 for run in runs)
        result["concurrency"].append(
            {
                "concurrency": concurrency,
                "wall_s": round(completed, 6),
                "aggregate_completion_tokens": total_completion_tokens,
                "aggregate_output_tok_s_wall": round(total_completion_tokens / completed, 3)
                if total_completion_tokens and completed
                else None,
                "rss_before_kib": total_rss_kib(before),
                "rss_after_kib": total_rss_kib(after),
                "rss_delta_kib": total_rss_kib(after) - total_rss_kib(before),
                "runs": sorted(runs, key=lambda item: item.get("workload", "")),
            }
        )
    result["process_snapshot"] = process_snapshot(engine["process_pattern"])
    return result


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    selected_engines = {
        name.strip()
        for name in os.environ.get("LOCAL_AI_BENCH_ENGINES", ",".join(engine["name"] for engine in ENGINES)).split(",")
        if name.strip()
    }
    results = {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "methodology": "OpenAI-compatible operational smoke benchmark; streaming for TTFT, non-stream for usage/timing metadata, RSS deltas for KV/cache pressure proxy, moderate context, and 2-way concurrency only.",
        "engine_filter": sorted(selected_engines),
        "engines": [],
    }
    OUT.write_text(json.dumps(results, indent=2) + "\n")
    for engine in ENGINES:
        if engine["name"] not in selected_engines:
            continue
        results["engines"].append(run_engine(engine))
        OUT.write_text(json.dumps(results, indent=2) + "\n")
    OUT.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
