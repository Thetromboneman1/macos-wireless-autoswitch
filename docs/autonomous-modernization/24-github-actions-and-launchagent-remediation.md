# 24 - GitHub Actions And LaunchAgent Remediation

Date: 2026-06-23

## Implemented

- Replaced deprecated release actions with `softprops/action-gh-release@v2`.
- Added explicit read-only workflow permissions to validation.
- Extended `scripts/health/local-ai-health.py` with swap parsing, port checks, process snapshots, and LaunchAgent validation.
- Removed ignored local gitleaks sources from `backups/dnscrypt-20260622-105231/` and `tmp/star-downloads/`.
- Added repository, workflow, security, LaunchAgent, startup, monitoring, swap, and OnePassword docs.

## Findings

- `com.corn.vllm-mlx` is a disabled, broken legacy AI LaunchAgent and should stay out of startup.
- Current swap usage is high even with llama.cpp and Rapid-MLX stopped.
- Full gitleaks findings were local ignored artifacts, not tracked staged code.
- Boneman is the canonical 1Password vault.

## Remaining Manual Actions

- Decide whether to archive `~/Library/LaunchAgents/com.corn.vllm-mlx.plist`.
- Review dirty files in `Boneman_Projects`, `Hermes`, `Openclaw`, and `odysseus-gemma-docker` before any cross-repo push.
- Consider SHA pinning third-party GitHub Actions if this repo’s release process becomes high-risk.
