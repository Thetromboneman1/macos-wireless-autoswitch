from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_file_ownership_map_classifies_every_tracked_file():
    tracked = {
        line.strip()
        for line in (ROOT / "config" / "repository-governance" / "tracked-files.txt").read_text().splitlines()
        if line.strip()
    }
    data = json.loads((ROOT / "config" / "repository-governance" / "file-ownership-map.json").read_text())
    entries = data["files"]
    paths = {entry["current_path"] for entry in entries}

    assert data["schema_version"] == 1
    assert tracked
    assert tracked <= paths
    assert all(entry["classification"] in data["allowed_classifications"] for entry in entries)
    assert all(entry["correct_owner"] for entry in entries)
    assert all("migration_status" in entry for entry in entries)


def test_required_repository_governance_documents_exist():
    required = [
        "repository-purpose-and-ownership-map.md",
        "canonical-repository-ownership.md",
        "macos-wireless-autoswitch-scope-audit.md",
        "cross-repository-dependency-graph.md",
        "repository-reorganization-plan.md",
        "migration-provenance-register.md",
    ]

    for name in required:
        path = ROOT / "docs" / "repository-governance" / name
        text = path.read_text()
        assert text.startswith("# ")
        assert "macos-wireless-autoswitch" in text


def test_document_retention_and_migration_registers_exist():
    for name in ["document-retention-and-archive-policy.md", "document-migration-register.md"]:
        text = (ROOT / "docs" / "governance" / name).read_text()
        assert text.startswith("# ")
        assert "Archived on:" in text


def test_safe_batch_script_and_thresholds_are_configured():
    thresholds = json.loads((ROOT / "config" / "apple-container" / "resource-thresholds.json").read_text())
    script = (ROOT / "scripts" / "apple-container" / "start-safe-batch.sh").read_text()

    assert thresholds["schema_version"] == 1
    assert thresholds["limits"]["max_new_services_per_batch"] == 1
    assert thresholds["limits"]["memory_pressure_allowed"] == ["normal"]
    assert "memory_pressure" in script
    assert "vm_stat" in script
    assert "docker stats" in script
    assert "container stats" in script
    assert "start-all.sh" in script


def test_modernization_controller_is_bounded():
    script = (ROOT / "scripts" / "platform-modernization" / "reconcile-and-mirror.sh").read_text()

    assert "MAX_ITERATIONS" in script
    assert "generate-repository-governance.py" in script
    assert "start-safe-batch.sh" in script
    assert "git diff --check" in script
