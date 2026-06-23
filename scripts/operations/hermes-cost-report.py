#!/usr/bin/env python3
"""Build a secret-safe Hermes token and cost observability report."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def estimate_tokens(chars_or_bytes: int | float | None) -> int:
    """Use the common four-character approximation when exact tokens are absent."""
    value = int(chars_or_bytes or 0)
    return int(round(value / 4))


def prompt_overhead(path: Path) -> dict[str, Any]:
    data = load_json(path)
    system_chars = int(data.get("system_prompt", {}).get("chars") or 0)
    skills_chars = int(data.get("skills_index", {}).get("chars") or 0)
    memory_chars = int(data.get("memory", {}).get("chars") or 0)
    user_chars = int(data.get("user_profile", {}).get("chars") or 0)
    tool_bytes = int(data.get("tools", {}).get("json_bytes") or 0)
    total_units = system_chars + skills_chars + memory_chars + user_chars + tool_bytes
    return {
        "path": str(path),
        "model": data.get("model"),
        "tool_count": int(data.get("tools", {}).get("count") or 0),
        "estimated_system_tokens": estimate_tokens(system_chars),
        "estimated_skills_tokens": estimate_tokens(skills_chars),
        "estimated_memory_tokens": estimate_tokens(memory_chars),
        "estimated_user_profile_tokens": estimate_tokens(user_chars),
        "estimated_tool_schema_tokens": estimate_tokens(tool_bytes),
        "estimated_total_tokens": estimate_tokens(total_units),
    }


def iter_json_records(path: Path) -> list[dict[str, Any]]:
    if path.suffix == ".jsonl":
        records = []
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                records.append(parsed)
        return records
    parsed = load_json(path)
    if isinstance(parsed.get("records"), list):
        return [item for item in parsed["records"] if isinstance(item, dict)]
    return [parsed]


def find_usage_objects(value: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(value, dict):
        usage = value.get("usage")
        if isinstance(usage, dict):
            found.append(usage)
        for child in value.values():
            found.extend(find_usage_objects(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(find_usage_objects(child))
    return found


def aggregate_usage(paths: list[Path]) -> dict[str, Any]:
    input_tokens = 0
    output_tokens = 0
    cached_input_tokens = 0
    records = 0
    for path in paths:
        for record in iter_json_records(path):
            for usage in find_usage_objects(record):
                prompt = int(usage.get("prompt_tokens") or usage.get("input_tokens") or 0)
                completion = int(usage.get("completion_tokens") or usage.get("output_tokens") or 0)
                details = usage.get("prompt_tokens_details") or {}
                cached = int(details.get("cached_tokens") or usage.get("cached_input_tokens") or 0)
                if prompt or completion or cached:
                    records += 1
                    input_tokens += prompt
                    output_tokens += completion
                    cached_input_tokens += cached
    cache_hit_percent = round((cached_input_tokens / input_tokens) * 100, 1) if input_tokens else 0.0
    return {
        "record_count": records,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cached_input_tokens": cached_input_tokens,
        "cache_hit_percent": cache_hit_percent,
    }


def build_cost_report(
    *,
    prompt_size_paths: list[Path] | None = None,
    session_paths: list[Path] | None = None,
    health_path: Path | None = None,
) -> dict[str, Any]:
    prompt_size_paths = prompt_size_paths or []
    session_paths = session_paths or []
    platforms = {}
    for path in prompt_size_paths:
        data = load_json(path)
        platform = str(data.get("platform") or path.stem)
        platforms[platform] = prompt_overhead(path)

    sections: dict[str, Any] = {
        "fixed_prompt_overhead": {"platforms": platforms},
        "usage": aggregate_usage(session_paths),
    }
    if health_path:
        health = load_json(health_path)
        sections["local_ai_health"] = {
            "ok": bool(health.get("ok")),
            "swap_pressure": health.get("system", {}).get("swap", {}).get("pressure"),
            "lanes": [
                {
                    "name": lane.get("name"),
                    "ok": lane.get("ok"),
                    "state": lane.get("state", "running"),
                    "usage": lane.get("usage", {}),
                }
                for lane in health.get("lanes", [])
            ],
        }

    return {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ok": True,
        "sections": sections,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt-size-json", type=Path, action="append", default=[])
    parser.add_argument("--session-json", type=Path, action="append", default=[])
    parser.add_argument("--health-json", type=Path)
    parser.add_argument("--json", type=Path, help="Write report JSON to this path.")
    args = parser.parse_args(argv)

    report = build_cost_report(
        prompt_size_paths=args.prompt_size_json,
        session_paths=args.session_json,
        health_path=args.health_json,
    )
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
