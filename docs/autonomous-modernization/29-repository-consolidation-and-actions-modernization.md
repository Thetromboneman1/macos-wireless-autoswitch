# Repository Consolidation And Actions Modernization

Date: 2026-06-23

## Executive Summary

Reviewed 13 local repositories. Changed only `macos-wireless-autoswitch`; preserved dirty local work in Boneman_Projects, Hermes, Openclaw, and odysseus-gemma-docker. Removed one tracked macOS metadata file, added repository governance docs, scoped markdownlint deliberately, modernized Actions, and updated Hermes cost reporting to separate reported static overhead from enabled runtime tools.

## Repository Results

| Repository | Initial state | Action | Final disposition |
|---|---|---|---|
| macos-wireless-autoswitch | clean and synchronized at `e8bec08` | Updated docs, Actions, cost reporting, tests; removed `.DS_Store` | Commit/push pending this pass. |
| Boneman_Projects | synchronized but dirty docs | Preserved | Manual review before commit. |
| Hermes workspace | ahead 1, behind 2, dirty | Preserved | Manual reconciliation required. |
| Openclaw | synchronized but dirty compose | Preserved | Manual review before commit. |
| odysseus-gemma-docker | synchronized but dirty local AI files | Preserved | Manual review before commit. |
| llama.cpp | clean, behind 161 | No edit | Update only during benchmark window. |
| hermes-agent | clean, behind 1302 | No edit | Fork refresh decision required. |
| hermes-desktop | clean, ahead 3 behind 84 | No edit | Divergent reference checkout. |
| YTKillerPlus | clean, behind 8 | No edit | Upstream update optional. |
| Ansible, Goose, OmniRoute, hermes-webui | clean/synchronized for tracked branch | No edit | Healthy. |

## GitHub Actions Results

| Workflow | Previous condition | Change | Validation |
|---|---|---|---|
| Validate Core Files | No timeout or concurrency | Added timeout and concurrency | `actionlint` and `yamllint` pass locally. |
| Create Release | No timeout or concurrency | Added timeout and concurrency | `actionlint` and `yamllint` pass locally. |
| Sync Fork From Upstream | Every 30 minutes | Reduced to daily and added concurrency | `actionlint` and `yamllint` pass locally. |
| Repository Validation | Missing | Added docs/scripts/tests/config/workflow validation | New workflow validates locally; remote run will start after push. |

## Hermes Follow-Up

`hermes tools list --platform cli` shows the trimmed toolsets remain disabled. `hermes prompt-size --json` still reports 29 tools and about 20,130 estimated tokens, so the report now treats that as reported/static overhead and records enabled runtime toolsets separately.

## Documentation Results

Created repository governance docs, a document status register, Actions inventory/recommendations/dependency strategy, Actions threat model, and a runbook. Markdownlint now excludes only historical or third-party/reference paths with reasons.

## Security Results

Local `gitleaks detect --no-banner --redact --source .` found no leaks. Workflows use `contents: read` by default, with write permission retained only where the job requires it.

## Remaining Risks

- Dirty local work in adjacent repos still needs owner review before commit/push.
- Remote workflow verification requires pushing this commit and watching the new run.
- Upstream/fork refreshes for llama.cpp, hermes-agent, hermes-desktop, and YTKillerPlus are intentionally deferred.
