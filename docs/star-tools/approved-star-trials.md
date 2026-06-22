# Approved GitHub-Star Trials

This folder documents lightweight trials for GitHub-starred tools. Trials are intentionally local, reversible, and non-default.

## Rules

- Trial checkouts go under `tmp/star-downloads/`.
- Do not commit trial checkouts or downloaded binaries.
- Do not pull models larger than 20 GB without explicit approval.
- Do not start services that replace DNSCrypt, AdGuard, Codex, OpenCode, Hermes, Goose, oMLX, or llama.cpp defaults.
- Store future secrets only in 1Password:
  - vault: `Boneman Projects`
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
