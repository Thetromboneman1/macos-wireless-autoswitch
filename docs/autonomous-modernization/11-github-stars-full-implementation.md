# 11 - GitHub Stars Full Implementation

## Baseline

- Timestamp: 2026-06-22T16:10:00Z
- Repo path: `/Users/corn/Documents/Corn_Automation/macos-wireless-autoswitch`
- Branch: `main`
- Current DNS state: Apps/Browsers -> AdGuard DNS Protection -> LocalDNSCrypt `127.0.0.1:53530` -> `dnscrypt-proxy 2.1.16` -> encrypted upstream resolvers.
- Commit status at start: clean, ahead of `origin/main` by 3 local commits.
- Source files:
  - `github-stars-refresh.json`
  - `github-stars-ranked.json`
  - `github-stars-implementation-plan.json`

## Implementation Rules

- Use every useful star through the safest useful path: existing-tool integration, docs, trial script, or benchmark harness.
- Do not install overlapping agent frameworks into the main stack.
- Do not pull large models or indexes without approval.
- Do not create paid-service dependencies.
- Do not push remote.
- Store future secrets in 1Password, not in this repo.

## Summary

| Classification | Count | Action |
| --- | ---: | --- |
| Implement With Existing Tool | 9 | Mapped to current Goose/Hermes/OpenClaw/local-stack docs. |
| Document Only | 22 | Captured as references or optional future trials. |
| Overlaps Existing Tool | 9 | Deferred to controlled trials; no main-stack replacement. |
| Needs Approval | 3 | Model/runtime items that may require large assets or runtime floor changes. |
| Skip | 2 | Low relevance to local AI/DNS/Codex/OpenCode/repo modernization. |

## Implemented With Existing Tools

### aaif-goose/goose

- Decision: Implement With Existing Tool.
- Action: Keep as existing local-stack agent component; no new install.
- Reason: Goose is already represented in local config and docs.
- Overlap check: complements Codex/OpenCode/Hermes when used as an agent runner; does not replace them.
- 1Password needed: no new secret in this pass.
- Files changed: this document and `docs/security/onepassword-secrets.md`.
- Validation: local repo inventory confirms Goose checkout exists.
- Rollback: documentation-only.
- Status: integrated by reference.

### Hermes repos and OpenClaw

- Decision: Implement With Existing Tool.
- Action: Treat `Thetromboneman1/hermes-*`, `NousResearch/hermes-agent`, and `Thetromboneman1/Openclaw` as existing stack components.
- Reason: local worktrees already exist and several are dirty; touching them from this repo would risk overwriting user work.
- Overlap check: these are the existing agent/UI/workspace stack.
- 1Password needed: no new secret in this pass.
- Files changed: this document.
- Validation: local repo status reviewed in the previous DNS/stars pass.
- Rollback: documentation-only.
- Status: integrated by reference; separate repo-specific commits needed later.

### garrytan/gbrain

- Decision: Implement With Existing Tool.
- Action: Document as a conceptual OpenClaw/Hermes brain reference, not an install.
- Reason: overlaps the existing Hermes/OpenClaw local agent architecture.
- Overlap check: direct overlap with local agent orchestration.
- 1Password needed: no.
- Files changed: this document.
- Validation: plan entry generated from GitHub star metadata and README check.
- Rollback: documentation-only.
- Status: reference.

## Documented Optional Trials

Use `scripts/star-tools/star-trial-plan.sh` to print the current trial matrix.

| Tool | Trial path | Approval needed before install |
| --- | --- | --- |
| `nvk/llm-wiki` | Knowledge-base trial for Codex/OpenCode docs. | No secret; approval before plugin install. |
| `headroomlabs-ai/headroom` | Token compression benchmark against existing logs/tool output. | Approval before proxy/MCP service. |
| `Egonex-AI/Understand-Anything` | Code graph trial on one selected repo. | Approval before indexing a large repo. |
| `StarTrail-org/LEANN` | Private RAG storage trial on a small docs subset. | Approval before indexing large data. |
| `SiliconScope` | Manual Apple Silicon telemetry during MLX vs llama.cpp bakeoff. | Approval before GUI install. |
| `google-gemma/gemma-skills` | Compare prompt/tool patterns against current Gemma role docs. | No secret. |
| `diegosouzapw/OmniRoute` | Gateway comparison only; do not replace current local path. | Approval before running service. |
| `Octopoda-OS`, `osaurus`, `OpenHands`, `npcsh`, `ECC` | Agent-framework comparison matrix. | Approval before installing/running. |

## Needs Approval

| Tool | Reason |
| --- | --- |
| `beamivalice/PonyExl3` | Model format/runtime trial; may require model assets and Python environment changes. |
| `john-rocky/coreai-model-zoo` | Core AI runtime floor is not current production fit; revisit after macOS/Xcode support aligns. |
| `TheStageAI/edge-lm` | Model download/runtime decision needed before use. |

## Skipped

| Tool | Reason |
| --- | --- |
| `Stirling-Tools/Stirling-PDF` | Useful app, not relevant to this local AI/DNS/repo modernization pass. |
| `iptv-org/iptv` | Not relevant to local AI/DNS/Codex/OpenCode/repo modernization. |

## Validation

Validation commands are recorded in the final response for the commit that includes this file.

## Approved Implementation Follow-up

The approved execution pass is documented in [12-approved-star-implementation.md](12-approved-star-implementation.md). It created the `Boneman Projects` 1Password vault, downloaded small README/reference snapshots for the approved lightweight trial set, and added a safe shallow-clone trial helper that writes only to ignored `tmp/star-downloads/`.
