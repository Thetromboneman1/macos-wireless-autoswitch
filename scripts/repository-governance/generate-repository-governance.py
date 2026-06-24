#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TODAY = date.today().isoformat()


@dataclass(frozen=True)
class OwnerRule:
    prefix: str
    owner: str
    classification: str
    destination: str
    purpose: str


OWNER_RULES = [
    OwnerRule("wireless.sh", "macos-wireless-autoswitch", "Keep", "wireless.sh", "Core wireless switching entrypoint."),
    OwnerRule("install.sh", "macos-wireless-autoswitch", "Keep", "install.sh", "Project installer."),
    OwnerRule("README.md", "macos-wireless-autoswitch", "Keep", "README.md", "Project README."),
    OwnerRule("AGENTS.md", "macos-wireless-autoswitch", "Keep", "AGENTS.md", "Repo agent instructions."),
    OwnerRule(".github/workflows/", "macos-wireless-autoswitch", "Keep", ".github/workflows/", "Project CI."),
    OwnerRule(".vscode/", "macos-wireless-autoswitch", "Requires review", ".vscode/", "Editor integration; may contain platform tasks."),
    OwnerRule("launchd/", "macos-wireless-autoswitch", "Keep", "launchd/", "Related macOS LaunchAgent support."),
    OwnerRule("com.computernetworkbasics.wifionoff.plist", "macos-wireless-autoswitch", "Keep", "com.computernetworkbasics.wifionoff.plist", "Wireless LaunchAgent."),
    OwnerRule("local.macos-wireless-autoswitch.fork-sync.plist", "macos-wireless-autoswitch", "Keep", "local.macos-wireless-autoswitch.fork-sync.plist", "Repository fork sync agent."),
    OwnerRule("spec/", "macos-wireless-autoswitch", "Keep", "spec/", "Project specifications."),
    OwnerRule("docs/apple-container/", "Boneman_Projects", "Move", "docs/apple-container/", "Apple Container platform governance."),
    OwnerRule("scripts/apple-container/", "Boneman_Projects", "Move", "scripts/apple-container/", "Apple Container platform tooling."),
    OwnerRule("config/apple-container/", "Boneman_Projects", "Move", "config/apple-container/", "Apple Container mirror configuration."),
    OwnerRule("config/runtime-profiles/", "Boneman_Projects", "Move", "config/runtime-profiles/", "Runtime profile governance."),
    OwnerRule("config/local-ai-platform/", "Boneman_Projects", "Move", "config/local-ai-platform/", "Local AI platform configuration."),
    OwnerRule("scripts/local-ai/", "Boneman_Projects", "Move", "scripts/local-ai/", "Local AI operations tooling."),
    OwnerRule("scripts/health/", "Boneman_Projects", "Move", "scripts/health/", "Platform health and drift tooling."),
    OwnerRule("scripts/operations/", "Boneman_Projects", "Move", "scripts/operations/", "AIOps and operations tooling."),
    OwnerRule("docs/operations/", "Boneman_Projects", "Move", "docs/operations/", "Platform operations runbooks."),
    OwnerRule("docs/capacity/", "Boneman_Projects", "Move", "docs/capacity/", "Platform capacity planning."),
    OwnerRule("docs/governance/", "Boneman_Projects", "Move", "docs/governance/", "Platform governance."),
    OwnerRule("docs/security/", "Boneman_Projects", "Requires review", "docs/security/", "Security docs; split repo-specific from platform-wide."),
    OwnerRule("docs/architecture/", "Boneman_Projects", "Move", "docs/architecture/", "Local AI architecture."),
    OwnerRule("docs/benchmarks/", "Boneman_Projects", "Move", "docs/benchmarks/", "Platform benchmarks."),
    OwnerRule("docs/disaster-recovery/", "Boneman_Projects", "Move", "docs/disaster-recovery/", "Platform disaster recovery."),
    OwnerRule("docs/repository-governance/", "Boneman_Projects", "Move", "docs/repository-governance/", "Cross-repository governance."),
    OwnerRule("docs/autonomous-modernization/", "Boneman_Projects", "Archive", "docs/archive/2026/autonomous-modernization/", "Historical modernization evidence."),
    OwnerRule("docs/hermes/", "Hermes", "Move", "docs/hermes/", "Hermes-specific operational docs."),
    OwnerRule("docs/macos/hermes-", "Hermes", "Move", "docs/macos/", "Hermes LaunchAgent guidance."),
    OwnerRule("scripts/gemma4-gguf-coding-lane.sh", "Boneman_Projects", "Move", "scripts/local-ai/gemma4-gguf-coding-lane.sh", "Local AI coding lane."),
    OwnerRule("scripts/odysseus-docker.sh", "odysseus-gemma-docker", "Move", "scripts/odysseus-docker.sh", "Docker stack helper."),
    OwnerRule("odysseus/", "odysseus-gemma-docker", "Move", "odysseus/", "Docker compose and service config."),
    OwnerRule("docs/ODYSSEUS_GEMMA_DOCKER.md", "odysseus-gemma-docker", "Move", "docs/ODYSSEUS_GEMMA_DOCKER.md", "Docker stack documentation."),
    OwnerRule("docs/network/", "Boneman_Projects", "Move", "docs/network/", "Host DNS and network platform docs."),
    OwnerRule("docs/agents/", "Boneman_Projects", "Move", "docs/agents/", "Agent platform governance."),
    OwnerRule("docs/skills/", "Boneman_Projects", "Move", "docs/skills/", "Skill platform documentation."),
    OwnerRule("docs/star-tools/", "Boneman_Projects", "Archive", "docs/archive/2026/star-tools/", "Historical starred-tool trials."),
    OwnerRule("scripts/star-tools/", "Boneman_Projects", "Requires review", "scripts/star-tools/", "Experimental support tooling."),
    OwnerRule("tests/test_apple_container_pilot.py", "Boneman_Projects", "Move", "tests/test_apple_container_pilot.py", "Apple Container platform tests."),
    OwnerRule("tests/test_local_ai_scripts.py", "Boneman_Projects", "Move", "tests/test_local_ai_scripts.py", "Local AI script tests."),
    OwnerRule("tests/test_platform_drift_detection.py", "Boneman_Projects", "Move", "tests/test_platform_drift_detection.py", "Platform drift tests."),
    OwnerRule("tests/test_aiops_operations.py", "Boneman_Projects", "Move", "tests/test_aiops_operations.py", "AIOps tests."),
    OwnerRule("tests/agents/", "Boneman_Projects", "Move", "tests/agents/", "Agent platform tests."),
]


def run(args: list[str], cwd: Path = ROOT) -> str:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=True).stdout.strip()


def run_optional(args: list[str], cwd: Path = ROOT) -> str:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def tracked_files() -> list[str]:
    output = run(["git", "ls-files", "--cached", "--others", "--exclude-standard"])
    return sorted(path for path in output.splitlines() if path)


def classify(path: str) -> dict[str, str]:
    for rule in OWNER_RULES:
        if path == rule.prefix or path.startswith(rule.prefix):
            destination = rule.destination if rule.destination.endswith("/") else rule.destination
            if rule.destination.endswith("/"):
                destination = f"{rule.destination}{Path(path).name}"
            return {
                "classification": rule.classification,
                "correct_owner": rule.owner,
                "destination_path": destination,
                "purpose": rule.purpose,
            }

    if path.startswith("docs/reference/"):
        return {
            "classification": "Third-party reference",
            "correct_owner": "Boneman_Projects",
            "destination_path": f"docs/reference/{Path(path).name}",
            "purpose": "Vendored reference material from external repositories.",
        }
    if path.startswith("docs/") or path.startswith("scripts/"):
        return {
            "classification": "Requires review",
            "correct_owner": "Boneman_Projects",
            "destination_path": path,
            "purpose": "Non-wireless platform content requiring owner confirmation.",
        }
    if path.startswith("tests/"):
        return {
            "classification": "Requires review",
            "correct_owner": "macos-wireless-autoswitch",
            "destination_path": path,
            "purpose": "Test file requiring scope confirmation.",
        }
    return {
        "classification": "Keep",
        "correct_owner": "macos-wireless-autoswitch",
        "destination_path": path,
        "purpose": "Repository metadata or project-local asset.",
    }


def reference_hints(path: str) -> dict[str, list[str]]:
    basename = Path(path).name
    refs = []
    if basename:
        output = run_optional(["rg", "-l", "--fixed-strings", basename])
        refs = [line for line in output.splitlines() if line and line != path][:25]
    return {
        "incoming_references": refs,
        "outgoing_references": [],
        "github_actions_references": [ref for ref in refs if ref.startswith(".github/")],
        "launchagent_references": [ref for ref in refs if ref.endswith(".plist") or "launch" in ref.lower()],
        "vscode_references": [ref for ref in refs if ref.startswith(".vscode/")],
        "test_references": [ref for ref in refs if ref.startswith("tests/")],
        "documentation_links": [ref for ref in refs if ref.endswith(".md")],
        "environment_references": [ref for ref in refs if ref.endswith((".env", ".json", ".yml", ".yaml", ".toml"))],
    }


def discover_repos() -> list[dict[str, str]]:
    roots = [Path.home() / name for name in ("Documents", "Projects", "Developer", "Boneman")]
    repos = []
    for root in roots:
        if not root.exists():
            continue
        for git_dir in root.rglob(".git"):
            if not git_dir.is_dir():
                continue
            repo = git_dir.parent
            rel = str(repo)
            status = run_optional(["git", "status", "--short", "--branch"], repo).splitlines()
            remote = run_optional(["git", "remote", "get-url", "origin"], repo)
            branch = run_optional(["git", "branch", "--show-current"], repo)
            default_branch = run_optional(["git", "symbolic-ref", "refs/remotes/origin/HEAD"], repo).replace("refs/remotes/origin/", "")
            repos.append(
                {
                    "path": rel,
                    "remote": remote or "none",
                    "current_branch": branch or "detached-or-unknown",
                    "default_branch": default_branch or "unknown",
                    "status": "dirty" if any(line and not line.startswith("##") for line in status) else "clean",
                    "purpose": infer_repo_purpose(repo.name, rel),
                    "recommended_scope": infer_repo_scope(repo.name, rel),
                }
            )
    return sorted(repos, key=lambda item: item["path"])


def infer_repo_purpose(name: str, path: str) -> str:
    lower = path.lower()
    if "macos-wireless-autoswitch" in lower:
        return "macOS wireless autoswitching and related LaunchAgent automation."
    if "boneman_projects" in lower:
        return "Central local AI platform, governance, operations, and cross-repository standards."
    if "hermes" in lower:
        return "Hermes product, agent, UI, or routing code."
    if "openclaw" in lower:
        return "OpenClaw gateway and runtime integration."
    if "odysseus" in lower:
        return "Docker-based Odysseus/Gemma support stack."
    if "ansible" in lower:
        return "Ansible lab automation."
    if "llama.cpp" in lower:
        return "GGUF inference engine source."
    return f"Local repository: {name}."


def infer_repo_scope(name: str, path: str) -> str:
    lower = path.lower()
    if "macos-wireless-autoswitch" in lower:
        return "Keep wireless switching, dock/undock networking, related macOS automation, and project CI only."
    if "boneman_projects" in lower:
        return "Own local AI platform docs, Apple Container governance, AIOps, drift, health, and repo standards."
    if "hermes" in lower:
        return "Own Hermes-specific providers, UI, agents, cost controls, and product runbooks."
    if "openclaw" in lower:
        return "Own OpenClaw Docker socket constraints, gateway, and runtime compatibility."
    if "odysseus" in lower:
        return "Own Docker Compose stacks and model-supporting services such as ntfy and ChromaDB."
    return "Requires review before moving content into or out of this repository."


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    write(path, json.dumps(data, indent=2, sort_keys=True) + "\n")


def emit_outputs() -> None:
    files = tracked_files()
    repos = discover_repos()
    entries = []
    for path in files:
        info = classify(path)
        refs = reference_hints(path)
        entries.append(
            {
                "current_path": path,
                **info,
                **refs,
                "runtime_dependencies": [],
                "migration_status": "not-moved",
            }
        )

    write(ROOT / "config/repository-governance/tracked-files.txt", "\n".join(files) + "\n")
    write_json(
        ROOT / "config/repository-governance/file-ownership-map.json",
        {
            "schema_version": 1,
            "updated": TODAY,
            "repository": "macos-wireless-autoswitch",
            "allowed_classifications": [
                "Keep",
                "Move",
                "Archive",
                "Delete",
                "Generated",
                "Third-party reference",
                "Requires review",
            ],
            "files": entries,
        },
    )

    repo_rows = "\n".join(
        f"| `{repo['path']}` | {repo['purpose']} | {repo['recommended_scope']} | {repo['current_branch']} | {repo['default_branch']} | {repo['status']} | `{repo['remote']}` |"
        for repo in repos
    )
    write(
        ROOT / "docs/repository-governance/repository-purpose-and-ownership-map.md",
        f"""# Repository Purpose and Ownership Map

Updated: {TODAY}

This map was generated from local git repository discovery under Documents, Projects, Developer, and Boneman roots. It is the first gate before moving files out of macos-wireless-autoswitch.

| Repository | Purpose | Recommended scope | Branch | Default | Status | Remote |
|---|---|---|---|---|---|---|
{repo_rows}
""",
    )

    counts: dict[str, int] = {}
    for entry in entries:
        counts[entry["classification"]] = counts.get(entry["classification"], 0) + 1
    count_lines = "\n".join(f"- {key}: {value}" for key, value in sorted(counts.items()))
    write(
        ROOT / "docs/repository-governance/macos-wireless-autoswitch-scope-audit.md",
        f"""# macos-wireless-autoswitch Scope Audit

Updated: {TODAY}

macos-wireless-autoswitch should retain wireless switching, dock/undock network behavior, related macOS automation, LaunchAgents, tests, and project-specific CI. The current tree also contains local AI platform, Apple Container, Hermes, OpenClaw, Docker, AIOps, security, benchmark, and repository-governance material.

## Classification Counts

{count_lines}

## Migration Gate

No source file is ready for removal until its destination repository validates the copied content, references are updated, and the migration provenance register records source and destination commits.
""",
    )

    owner_lines = "\n".join(
        [
            "- macos-wireless-autoswitch: wireless switching, dock/undock network behavior, related LaunchAgents, project CI, and project-specific tests.",
            "- Boneman_Projects: local AI platform architecture, Apple Container governance, AIOps, drift detection, capacity, benchmarks, skills integration, and cross-repository standards.",
            "- Hermes and subrepositories: Hermes providers, UI, agents, model provider configuration, cost controls, and Hermes-specific tests.",
            "- OpenClaw: OpenClaw gateway, Docker socket constraints, runtime compatibility, and OpenClaw-specific compose/configuration.",
            "- odysseus-gemma-docker: Docker Compose stacks, ntfy production definition, ChromaDB and model-supporting services.",
        ]
    )
    write(
        ROOT / "docs/repository-governance/canonical-repository-ownership.md",
        f"""# Canonical Repository Ownership

Updated: {TODAY}

{owner_lines}

The default destination for cross-repository governance is Boneman_Projects unless a product repository has a clearer lifecycle owner. macos-wireless-autoswitch remains the source of record only for wireless automation.
""",
    )

    move_edges = [entry for entry in entries if entry["classification"] in {"Move", "Archive", "Requires review"}]
    edge_lines = "\n".join(
        f"- `{entry['current_path']}` -> {entry['correct_owner']} `{entry['destination_path']}`; references sampled: {len(entry['incoming_references'])}"
        for entry in move_edges[:200]
    )
    write(
        ROOT / "docs/repository-governance/cross-repository-dependency-graph.md",
        f"""# Cross-Repository Dependency Graph

Updated: {TODAY}

This initial graph records candidate ownership edges before any move. Each move batch must re-run reference validation across shell scripts, Python imports, Markdown links, Actions, VS Code tasks, LaunchAgents, JSON, YAML, TOML, Docker Compose, tests, and Codex instructions.

{edge_lines}
""",
    )

    write(
        ROOT / "docs/repository-governance/repository-reorganization-plan.md",
        f"""# Repository Reorganization Plan

Updated: {TODAY}

This plan narrows macos-wireless-autoswitch back to wireless automation while preserving platform content in the correct destination repositories.

## Atomic Batches

1. Repository-governance documents to Boneman_Projects.
2. Apple Container platform tooling and config to Boneman_Projects.
3. Local AI health, drift, and runtime-profile configuration to Boneman_Projects.
4. Docker/Odysseus assets to odysseus-gemma-docker.
5. Hermes-specific docs and tests to the relevant Hermes repository.
6. Historical modernization reports to `docs/archive/2026/` in the canonical governance repo.
7. Wireless repo README, docs, tests, LaunchAgents, and CI narrowing after destination validation.

## Commit Order

For each batch: add destination copy, validate destination, commit and push destination, update source references, remove source copy, validate source, commit and push source, then record both commits in the provenance register.
""",
    )

    write(
        ROOT / "docs/repository-governance/migration-provenance-register.md",
        f"""# Migration Provenance Register

Updated: {TODAY}

No files have been moved in this batch. Future entries must include original path, destination path, source commit, destination commit, validation command, validation result, link repair result, and rollback note.

| Source path | Destination repository | Destination path | Source commit | Destination commit | Status |
|---|---|---|---|---|---|
| macos-wireless-autoswitch | Boneman_Projects | pending | pending | pending | inventory-only |
""",
    )

    write(
        ROOT / "docs/governance/document-retention-and-archive-policy.md",
        f"""# Document Retention and Archive Policy

Updated: {TODAY}

Documents are classified as current, canonical, historical evidence, superseded, obsolete, or third-party reference before they move or archive.

Archived documents must include this banner:

```text
Status: Archived
Superseded by: <canonical path>
Archived on: <date>
Reason: <reason>
```

Do not rewrite third-party reference content. Exclude archived or third-party content from linting only with a narrow, documented rule.
""",
    )

    write(
        ROOT / "docs/governance/document-migration-register.md",
        f"""# Document Migration Register

Updated: {TODAY}

```text
Status: Active
Superseded by: n/a
Archived on: n/a
Reason: Migration register for document consolidation.
```

| Document group | Canonical owner | Action | Status |
|---|---|---|---|
| autonomous-modernization reports | Boneman_Projects | Archive historical evidence | planned |
| Apple Container docs | Boneman_Projects | Move platform governance | planned |
| Hermes docs | Hermes | Move product-specific guidance | planned |
| Wireless docs | macos-wireless-autoswitch | Retain focused project docs | planned |
""",
    )

    write(
        ROOT / "docs/apple-container/full-docker-mirror-plan.md",
        f"""# Full Docker Mirror Plan

Updated: {TODAY}

Docker remains production. Apple Container mirrors are side-by-side candidates only. The validated pattern is `ac-ntfy` on `127.0.0.1:19091`, isolated from Docker production data and compared with Docker ntfy on `127.0.0.1:8091`.

Next candidates must pass resource gates, ARM64 image checks, isolated storage checks, health checks, restart checks, rollback checks, and side-by-side comparison before they are left running.
""",
    )

    write(
        ROOT / "docs/apple-container/resource-aware-mirroring.md",
        f"""# Resource-Aware Mirroring

Updated: {TODAY}

Use `scripts/apple-container/start-safe-batch.sh` instead of starting every candidate mirror. The scheduler reads memory pressure, `vm_stat`, Docker usage, Apple Container usage, and `config/apple-container/resource-thresholds.json`; it starts at most one enabled candidate per batch unless thresholds are explicitly relaxed.
""",
    )

    write(
        ROOT / "docs/apple-container/mirror-expansion-results.md",
        f"""# Mirror Expansion Results

Updated: {TODAY}

| Workload | Docker state | Apple Container state | Disposition |
|---|---|---|---|
| ntfy | running on 127.0.0.1:8091 | running on 127.0.0.1:19091 | keep mirror running |
| OpenClaw gateway | running, Docker socket dependent | not mirrored | Docker-only until runtime-neutral socket replacement exists |
| ChromaDB | running | not started | defer behind resource gate |
| Open WebUI | running | not started | defer behind resource gate |
| Hermes UI | running | not started | defer behind resource gate |
""",
    )

    write(
        ROOT / "docs/autonomous-modernization/34-repository-reorganization-and-container-mirror.md",
        f"""# Repository Reorganization and Container Mirror

Updated: {TODAY}

This milestone converts the successful ntfy side-by-side pilot into a governed expansion program. It adds repository ownership discovery, a full file ownership manifest for macos-wireless-autoswitch, migration provenance requirements, document retention rules, and a resource-aware Apple Container starter.

No broad source removals are performed in this milestone. The next safe action is the first atomic destination-copy batch after Boneman_Projects is validated as the canonical governance owner.
""",
    )


if __name__ == "__main__":
    emit_outputs()
