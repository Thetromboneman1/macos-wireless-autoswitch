# Approved GitHub-Star Trials

This folder documents lightweight trials for GitHub-starred tools. Trials are intentionally local, reversible, and non-default.

## Rules

- Trial checkouts go under `tmp/star-downloads/`.
- Do not commit trial checkouts or downloaded binaries.
- Download size, model size, bandwidth, and storage are no longer blockers for approved trials.
- Do not start services that replace DNSCrypt, AdGuard, Codex, OpenCode, Hermes, Goose, oMLX, or llama.cpp defaults unless the trial explicitly calls for that replacement.
- Store future secrets only in 1Password:
  - vault: `Boneman`
  - item naming: `<Tool Name> - API Token`, `<Tool Name> - Local AI`, or `<Tool Name> - Service Config`

## Commands

List all non-skipped plan items:

```bash
scripts/star-tools/star-trial-plan.sh
```

Create a shallow local checkout for an approved trial:

```bash
scripts/star-tools/run-approved-star-trial.sh nvk/llm-wiki
scripts/star-tools/run-approved-star-trial.sh headroomlabs-ai/headroom
scripts/star-tools/run-approved-star-trial.sh Egonex-AI/Understand-Anything
```

Remove all trial checkouts:

```bash
rm -rf tmp/star-downloads
```

Validate the deployed recommended tools:

```bash
scripts/star-tools/validate-star-deployments.sh
```

Start guarded local services only when you intend to use them:

```bash
scripts/star-tools/start-octopoda-local.sh
scripts/star-tools/start-headroom-proxy.sh http://127.0.0.1:18080
scripts/star-tools/start-omniroute-local.sh
scripts/star-tools/start-openhands-docker.sh
scripts/star-tools/start-understand-dashboard.sh
```

See `docs/autonomous-modernization/15-star-deployment-implementation.md` for the completed deployment map and rollback notes.

## Approved Lightweight Trial Set

- `nvk/llm-wiki`
- `headroomlabs-ai/headroom`
- `StarTrail-org/LEANN`
- `Egonex-AI/Understand-Anything`
- `kennss/SiliconScope`
- `beamivalice/PonyExl3`
- `john-rocky/coreai-model-zoo`
- `TheStageAI/edge-lm`
- `google-gemma/gemma-skills`
- `apple/container`
- `diegosouzapw/OmniRoute`

Reference README snapshots and checksums are stored in `docs/reference/github-stars/`.
