# Platform Audit Framework

Date: 2026-06-23
Owner: Platform Governance

## Purpose

The audit framework defines recurring reviews for GitHub Actions, LaunchAgents, AI services, model lanes, skills, dependencies, secret references, and documentation.

## Monthly Audit

Run:

```bash
scripts/operations/run-aiops-cycle.sh
uvx pytest
shellcheck install.sh wireless.sh scripts/**/*.sh
markdownlint docs/operations/*.md docs/governance/*.md docs/architecture/*.md docs/macos/*.md docs/security/*.md docs/skills/*.md
gitleaks detect --no-banner --redact --source .
```

Review:

- health and drift report;
- LaunchAgent inventory;
- dependency report;
- documentation review;
- Boneman pointer docs.

## Quarterly Audit

Review:

- production and lab-lane benchmarks;
- model lifecycle states;
- GitHub Actions versions and permissions;
- VS Code extensions and Codex skills;
- MCP topology;
- Docker image inventory.

## Annual Audit

Review:

- platform architecture fit;
- model strategy;
- security posture;
- continuity and rollback procedures;
- whether dormant experiments should be archived.

## Audit Outputs

Store decision-grade evidence in current docs or `docs/benchmarks/`. Keep noisy generated snapshots out of Git unless they support a decision.
