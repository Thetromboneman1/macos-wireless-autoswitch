# Weekly AI Repository Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Review the June 24, 2026 AI repository candidates, document security and placement decisions, and implement only safe, reversible local integration gates.

**Architecture:** Keep upstream code outside this repository in a controlled temporary review directory. Store durable evidence and decisions in `docs/ai-trending-repos/2026-06-24/` and machine-readable inventories in `config/ai-trending-repos/`. Do not install tools globally unless security, placement, and validation evidence justify it.

**Tech Stack:** GitHub CLI, uv isolated tool execution, Docker/Apple container inventory, local oMLX/GGUF endpoints, Markdown, JSON, gitleaks, markdownlint, jq.

---

## Task 1: Discovery And Upstream Pinning

**Files:**

- Create: `config/ai-trending-repos/upstream-versions-2026-06-24.json`
- Create: `docs/ai-trending-repos/2026-06-24/environment-inventory.md`

- [x] Record host, OS, local runtimes, containers, agents, and repository status.
- [x] Verify every upstream repository using GitHub metadata and exact default-branch commit SHA.
- [x] Clone reviewed repositories into `/tmp/codex-ai-repo-review-2026-06-24`.

## Task 2: Security And Placement Matrix

**Files:**

- Create: `docs/ai-trending-repos/2026-06-24/candidate-matrix.md`
- Create: `docs/ai-trending-repos/2026-06-24/security-review.md`
- Create: `docs/ai-trending-repos/2026-06-24/placement-decisions.md`

- [x] Inspect manifests, install paths, service exposure, secret use, cookies/session access, telemetry, and dependency/toolchain requirements.
- [x] Select final disposition for each candidate.
- [x] Keep unrelated tools out of `macos-wireless-autoswitch` except for the central review record.

## Task 3: Validation Evidence

**Files:**

- Create: `docs/ai-trending-repos/2026-06-24/benchmark-results.md`
- Create: `config/ai-trending-repos/validation-results-2026-06-24.json`

- [x] Run bounded `uvx` smoke tests for SkillSpector and Agent-Reach.
- [x] Run SkillSpector against one synthetic malicious skill and one defensive third-party skill.
- [x] Probe local AI endpoints and local tool availability.
- [x] Record blocked validations with exact reason.

## Task 4: Final Report Package

**Files:**

- Create: `docs/ai-trending-repos/2026-06-24/README.md`
- Create: `docs/ai-trending-repos/2026-06-24/executive-summary.md`
- Create: `docs/ai-trending-repos/2026-06-24/implementation-results.md`
- Create: `docs/ai-trending-repos/2026-06-24/known-limitations.md`
- Create: `docs/ai-trending-repos/2026-06-24/rollback-plan.md`
- Create: `docs/ai-trending-repos/2026-06-24/secret-references.md`

- [x] Document what was adopted, piloted, deferred, rejected, or kept document-only.
- [x] Confirm no secret values are required or committed.
- [x] Provide rollback and follow-up commands.

## Task 5: Verification And Git Hygiene

**Files:**

- Modify only files created for this review.

- [ ] Run `markdownlint` on the review docs.
- [ ] Run `jq empty` on the JSON inventory files.
- [ ] Run `gitleaks detect --no-banner --redact --source .`.
- [ ] Review `git status -sb` and staged diff before commit.
- [ ] Commit and push only the weekly review files if validation passes.
