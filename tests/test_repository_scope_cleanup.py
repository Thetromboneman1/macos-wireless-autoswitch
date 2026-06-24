from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_repository_governance_runtime_assets_are_not_active_in_wireless_repo():
    removed_paths = [
        "config/repository-governance/file-ownership-map.json",
        "config/repository-governance/tracked-files.txt",
        "scripts/repository-governance/generate-repository-governance.py",
        "tests/test_repository_governance.py",
    ]

    for relative in removed_paths:
        assert not (ROOT / relative).exists()


def test_repository_governance_docs_are_redirects_to_boneman_projects():
    redirect_docs = list((ROOT / "docs" / "repository-governance").glob("*.md"))

    assert redirect_docs
    for path in redirect_docs:
        text = path.read_text()
        assert "Status: Redirect" in text
        assert "Thetromboneman1/Boneman_Projects" in text
        assert "Boneman_Projects" in text


def test_wireless_docs_index_points_to_canonical_governance_repo():
    docs_index = (ROOT / "docs" / "README.md").read_text()
    readme = (ROOT / "README.md").read_text()

    assert "Thetromboneman1/Boneman_Projects" in docs_index
    assert "Thetromboneman1/Boneman_Projects" in readme
    assert "docs/repository-governance/local-repository-inventory.md" not in docs_index
