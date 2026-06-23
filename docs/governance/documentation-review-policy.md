# Documentation Review Policy

Date: 2026-06-23
Owner: Documentation Governance

## Purpose

Documentation governance prevents stale operational instructions from becoming platform drift.

## Automated Review

```bash
scripts/operations/documentation-review.py \
  docs/operations docs/governance docs/architecture docs/macos docs/security docs/skills docs/executive docs/roadmap docs/capacity docs/disaster-recovery \
  --json /tmp/documentation-review.json
```

The review checks current documentation for:

- review date metadata;
- owner metadata;
- current-doc coverage in the documentation index.

## Metadata Standard

Current operational docs should include:

```text
Date: YYYY-MM-DD
Owner: <role>
```

Historical reports under `docs/autonomous-modernization/` may remain dated evidence and do not need current ownership metadata.

## Broken Links and Superseded Docs

- Validate local links during monthly review.
- Mark superseded docs in `docs/README.md` instead of rewriting historical evidence.
- Prefer canonical docs under `docs/operations/`, `docs/architecture/`, `docs/macos/`, `docs/security/`, and `docs/governance/` for current runbooks.

## Review Cadence

| Trigger | Required review |
|---|---|
| Monthly platform audit | current docs metadata and index |
| New model lane | routing, lifecycle, benchmark, and operations docs |
| New LaunchAgent | inventory, security audit, rollback docs |
| New secret-bearing integration | secret inventory and Boneman pointer docs |
