# Agent Operationalization Knowledge Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the documented enterprise agent workforce into operational docs, knowledge architecture, evaluation criteria, memory design, orchestration workflows, executive automation, business value measurement, and regression tests.

**Architecture:** This plan adds operational overlays to the existing oMLX-first platform and agent catalog. It does not add new platform plumbing, governance layers, LaunchAgents, services, or alternate model defaults.

**Tech Stack:** Markdown documentation, pytest, repo-local oMLX/Gemma runtime contract, existing Codex/OpenCode/Hermes/Goose/OpenClaw integration surfaces.

---

## Tasks

### Task 1: Required Agent And Knowledge Deliverables

**Files:**

- Create: `docs/agents/operationalization-plan.md`
- Create: `docs/agents/agent-evaluation-framework.md`
- Create: `docs/agents/agent-memory-architecture.md`
- Create: `docs/agents/agent-orchestration.md`
- Create: `docs/agents/executive-automation-workflows.md`
- Create: `docs/agents/business-value-framework.md`
- Create: `docs/knowledge/enterprise-knowledge-architecture.md`
- Create: `docs/knowledge/tap-lite-knowledge-base.md`
- Create: `docs/knowledge/aap-knowledge-base.md`
- Create: `docs/knowledge/satellite-knowledge-base.md`
- Create: `docs/knowledge/redhat-summit-assistant.md`

- [ ] **Step 1: Create the operational deliverables**

Write each file with `Date`, `Owner`, `Purpose`, source dependencies, runtime constraints, operational workflows, validation criteria, and measurable outcomes.

- [ ] **Step 2: Check for placeholder language**

Run:

```bash
rg -n "TBD|TODO|FIXME|placeholder|fill in|later" docs/agents docs/knowledge
```

Expected: no findings in the new operational deliverables.

### Task 2: Catalog, Runtime, And Skills Updates

**Files:**

- Modify: `docs/agents/agent-catalog.md`
- Modify: `docs/agents/agent-runtime-architecture.md`
- Modify: `docs/skills/codex-skills.md`

- [ ] **Step 1: Link operational artifacts**

Add references from the agent catalog and runtime architecture to the operationalization plan, evaluation framework, memory architecture, orchestration workflow, and business value framework.

- [ ] **Step 2: Add skills operational guidance**

Add a short section describing how skills support agent operational runs without replacing the oMLX-first runtime contract.

### Task 3: Continuous Agent Regression Tests

**Files:**

- Create: `tests/agents/test_agent_operationalization_docs.py`

- [ ] **Step 1: Add documentation contract tests**

Create pytest checks for required files, required runtime strings, required agent names, evaluation dimensions, orchestration handoffs, knowledge base capabilities, and business value metrics.

- [ ] **Step 2: Run targeted tests**

Run:

```bash
uvx pytest tests/agents -q
```

Expected: all tests pass.

### Task 4: Repository Validation And Commit

**Files:**

- All files changed by Tasks 1-3.

- [ ] **Step 1: Run available validation**

Run:

```bash
uvx pytest
markdownlint README.md docs/**/*.md
shellcheck install.sh wireless.sh scripts/**/*.sh
gitleaks detect --no-banner --redact --source .
```

Expected: pytest passes; any missing tools or pre-existing findings are recorded.

- [ ] **Step 2: Review git status**

Run:

```bash
git status --short
git diff --stat
```

Expected: only planned docs and tests changed.

- [ ] **Step 3: Commit logical unit**

Run:

```bash
git add docs/agents docs/knowledge docs/skills tests/agents docs/superpowers/plans/2026-06-23-agent-operationalization-knowledge-platform.md
git commit -m "docs: operationalize enterprise agent workforce"
```

Expected: commit succeeds.
