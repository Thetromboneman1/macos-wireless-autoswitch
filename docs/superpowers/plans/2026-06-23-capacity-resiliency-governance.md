# Capacity Resiliency Governance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add enterprise reliability, capacity, model promotion, disaster recovery, and risk-management layers to the existing operational AI platform.

**Architecture:** Keep the platform oMLX-first and add small standard-library Python CLIs for model promotion gates and benchmark trend analysis. Use documentation for operating policy, DR procedures, capacity forecasts, SLO/SLA targets, and risk ownership; do not add daemons or autostart lab lanes.

**Tech Stack:** Python standard library, existing health/drift/benchmark JSON artifacts, Markdown governance docs, existing shell and repo validation tools.

---

## Task 1: Automation Tests

**Files:**

- Modify: `tests/test_aiops_operations.py`
- Create: `scripts/operations/model-governance/evaluate-promotion.py`
- Create: `scripts/operations/benchmark-trend-analysis.py`

- [x] **Step 1: Write failing tests**

Add tests for:

- model promotion gates rejecting high swap;
- model promotion gates accepting healthy benchmark, stability, health, tool-call, and documentation evidence;
- benchmark trend analysis detecting TTFT degradation across historical artifacts.

- [x] **Step 2: Verify red**

Run:

```bash
uvx pytest tests/test_aiops_operations.py
```

Expected: fail because the new scripts do not exist.

## Task 2: Automation Implementation

**Files:**

- Create: `scripts/operations/model-governance/evaluate-promotion.py`
- Create: `scripts/operations/benchmark-trend-analysis.py`

- [x] **Step 1: Implement model gates**

Create `evaluate_model_promotion()` to combine benchmark, stability, health, tool-call, and documentation inputs into pass/fail gate findings.

- [x] **Step 2: Implement trend analysis**

Create `analyze_trends()` to compare benchmark artifacts by engine/workload and flag degraded TTFT, throughput, swap, and reliability.

- [x] **Step 3: Verify green**

Run:

```bash
uvx pytest tests/test_aiops_operations.py
```

Expected: pass.

## Task 3: Enterprise Reliability Docs

**Files:**

- Create: `docs/capacity/platform-capacity-plan.md`
- Create: `docs/capacity/resource-forecast.md`
- Create: `docs/governance/model-promotion-framework.md`
- Create: `docs/governance/model-governance-automation.md`
- Create: `docs/operations/benchmark-trend-analysis.md`
- Create: `docs/governance/platform-slo-framework.md`
- Create: `docs/disaster-recovery/platform-dr-plan.md`
- Create: `docs/disaster-recovery/backup-validation.md`
- Create: `docs/disaster-recovery/restore-testing.md`
- Create: `docs/governance/platform-risk-register.md`
- Modify: `docs/README.md`

- [x] **Step 1: Create docs from live evidence**

Use the live health/capacity snapshot and existing platform docs to write capacity state, forecasts, SLO/SLA targets, DR/backup/restore validation, model promotion policy, and risk register.

- [x] **Step 2: Update docs index**

Add all new docs to `docs/README.md`.

## Task 4: Validation and Publish

**Files:**

- Create: `docs/autonomous-modernization/28-capacity-resiliency-governance.md`
- Modify: all files from Tasks 1-3.

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
scripts/health/local-ai-health.py --skip-chat --json /tmp/local-ai-health-capacity.json
scripts/health/drift-detection/check-platform-drift.py --health-json /tmp/local-ai-health-capacity.json --json /tmp/platform-drift-capacity.json
scripts/operations/run-aiops-cycle.sh
```

- [x] **Step 2: Commit and push**

Commit logical units, push to `origin/main`, and confirm `main...origin/main` is clean.
