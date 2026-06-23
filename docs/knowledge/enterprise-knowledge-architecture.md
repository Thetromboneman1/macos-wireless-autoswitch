# Enterprise Knowledge Architecture

Date: 2026-06-23
Owner: AI Workforce Program

## Purpose

The enterprise knowledge architecture gives operational agents trusted context for architecture, automation, platform operations, governance, and executive reporting. It uses existing docs, repositories, and retrieval tools; it does not create a new knowledge platform service.

## Knowledge Domains

| Domain | Primary sources | Consumers |
|---|---|---|
| Enterprise Architecture | TAP Lite examples, ADRs, architecture standards, platform architecture docs | Enterprise Architecture and Executive Communications Copilots |
| Automation Platform | AAP standards, playbooks, operational docs, upgrade guides, governance docs | AAP Platform and Automation Discovery Copilots |
| Satellite Platform | Lifecycle standards, content views, compliance notes, upgrade docs, patch runbooks | Satellite Platform and Operational Review Copilots |
| Operations | Health monitoring, drift detection, benchmark trends, capacity, DR, runbooks | Operational Review and Server Engineering Copilots |
| Governance | Documentation governance, model governance, SLOs, audit framework, risk register | All agents |
| Executive Evidence | Monthly updates, quarterly reviews, ROI notes, Summit notes, risk summaries | Executive Communications Copilot |

## Ingestion

| Source type | Ingestion method | Controls |
|---|---|---|
| Repo docs | Index `docs/`, `README.md`, and domain runbooks with LEANN or Understand-Anything | Exclude secrets, local backups, raw credentials, model caches |
| Standards and examples | Store approved examples under `docs/knowledge/` or linked reference folders | Record owner, review cadence, and source date |
| Operational evidence | Attach reports from `docs/operations/reports/` or generated JSON summaries to each run | Keep raw logs scoped to the task and redact secrets |
| Existing repositories | Index selected repos by explicit path only | Record repo, branch, commit, and ignored patterns |
| External vendor docs | Store citations or local notes only when approved | Separate vendor facts from local assumptions |

## Indexing

| Index | Scope | Refresh cadence | Validation |
|---|---|---|---|
| Enterprise architecture corpus | TAP Lite, ADRs, architecture standards, governance docs | Monthly or after standards changes | Sample TAP Lite retrieval includes current standards |
| AAP corpus | AAP standards, playbooks, upgrade notes, governance | Monthly or after upgrade changes | Sample question returns playbook and upgrade guidance |
| Satellite corpus | Lifecycle, content views, patch and compliance notes | Monthly patch cycle | Sample question returns lifecycle and compliance guidance |
| Operations corpus | Health, drift, benchmarks, capacity, DR, runbooks | Weekly or after incident | Sample question returns latest operational status evidence |
| Executive corpus | Monthly, quarterly, Summit, ROI, architecture updates | Before leadership reporting cycles | Sample summary cites source evidence |

## Retrieval

Agents should retrieve in this order:

1. Agent prompt contract in `docs/agents/`.
2. Domain knowledge base in `docs/knowledge/`.
3. Governance and operations docs in `docs/governance/`, `docs/operations/`, `docs/capacity/`, and `docs/disaster-recovery/`.
4. Current source evidence supplied with the request.
5. Existing repositories or external docs only when needed for the requested output.

## Maintenance

| Activity | Owner | Evidence |
|---|---|---|
| Refresh indexes | Domain owner | Index run log with source roots and timestamp |
| Review stale docs | AI Workforce Program | Documentation review output |
| Remove retired sources | Domain owner | Changelog or ADR reference |
| Validate retrieval quality | Agent owner | Evaluation run with pass/fail notes |
| Review access boundaries | Security owner | Secret exclusion check and Boneman pointer review |

## Validation

The knowledge architecture is usable when each agent can name its primary corpus, retrieve source evidence, cite missing evidence, avoid secret ingestion, and produce outputs that pass the evaluation framework.
