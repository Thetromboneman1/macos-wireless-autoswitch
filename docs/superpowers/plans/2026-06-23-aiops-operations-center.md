# AIOps Operations Center Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the governance and automation layer for a self-maintaining local AI platform.

**Architecture:** Add small Python CLIs under `scripts/operations/` that consume existing health, drift, benchmark, docs, and dependency artifacts without introducing new daemons or secret storage. Documentation under `docs/operations/`, `docs/governance/`, `docs/executive/`, and `docs/roadmap/` defines ownership, cadence, escalation, reporting, and roadmap policy.

**Tech Stack:** Python standard library, existing shell/JSON/TOML/YAML validation tools, existing oMLX and drift scripts, Markdown documentation.

---

## Task 1: AIOps Automation Scripts

**Files:**

- Create: `scripts/operations/generate-platform-report.py`
- Create: `scripts/operations/benchmark-governance.py`
- Create: `scripts/operations/documentation-review.py`
- Test: `tests/test_aiops_operations.py`

- [x] **Step 1: Write failing tests**

Create tests that assert:

```python
def test_platform_report_combines_health_and_drift(tmp_path): ...
def test_benchmark_governance_flags_ttft_regression(tmp_path): ...
def test_documentation_review_finds_missing_review_date(tmp_path): ...
```

- [x] **Step 2: Run tests to verify failure**

Run: `uvx pytest tests/test_aiops_operations.py`

Expected: FAIL because the scripts do not exist yet.

- [x] **Step 3: Implement minimal scripts**

Implement:

- report generation from health JSON, drift JSON, and optional dependency JSON;
- benchmark comparison from baseline/current JSON with TTFT and throughput regression thresholds;
- documentation review for missing `Date:`/`Last reviewed:` and missing ownership in current docs.

- [x] **Step 4: Run focused tests**

Run: `uvx pytest tests/test_aiops_operations.py`

Expected: PASS.

## Task 2: Governance Documentation

**Files:**

- Create: `docs/operations/platform-operations-center.md`
- Create: `docs/operations/benchmark-governance.md`
- Create: `docs/operations/model-lifecycle-management.md`
- Create: `docs/operations/dependency-governance.md`
- Create: `docs/operations/drift-governance.md`
- Create: `docs/governance/documentation-review-policy.md`
- Create: `docs/operations/platform-reporting.md`
- Create: `docs/executive/ai-platform-executive-summary.md`
- Create: `docs/roadmap/ai-platform-roadmap.md`
- Create: `docs/governance/platform-audit-framework.md`
- Modify: `docs/README.md`

- [x] **Step 1: Create docs**

Each document must include owner, review cadence, automation hooks, validation commands, rollback/remediation expectations, and the oMLX-first architecture contract where relevant.

- [x] **Step 2: Update docs index**

Add all new current docs to `docs/README.md`.

## Task 3: Validation and Publish

**Files:**

- Modify: staged files from Tasks 1-2.

- [x] **Step 1: Run validation**

Run:

```bash
uvx pytest
shellcheck install.sh wireless.sh scripts/**/*.sh
markdownlint <changed docs>
jq empty <changed JSON files>
taplo check /Users/corn/.codex/config.toml
yamllint .github/workflows/*.yml .github/FUNDING.yml
actionlint
gitleaks detect --no-banner --redact --source .
git diff --check
scripts/health/local-ai-health.py --skip-chat
scripts/health/drift-detection/check-platform-drift.py --health-json /tmp/local-ai-health.json
```

- [x] **Step 2: Commit and push**

Use logical commits, push to `origin/main`, and confirm `main...origin/main` is clean.
