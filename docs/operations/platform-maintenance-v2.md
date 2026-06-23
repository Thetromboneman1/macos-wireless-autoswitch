# Platform Maintenance V2

Date: 2026-06-23

## Monthly

- Run low-impact health:
  `scripts/health/local-ai-health.py --skip-chat`
- Run drift detection.
- Review `~/Library/LaunchAgents` for missing programs or new AI startup entries.
- Check Docker container memory with `docker stats --no-stream`.
- Review `Boneman` secret pointers without copying secret values into Git.

## Quarterly

- Re-run production oMLX benchmarks.
- Run lab-lane benchmark windows for llama.cpp and Rapid-MLX if they are still useful.
- Review the AI service catalog for dormant or redundant tools.
- Review GitHub Actions for deprecated actions or permission drift.
- Reassess model roles and keep the four-role Gemma contract unless intentionally changed.

## Before Long Benchmarks

- Unload unused oMLX models.
- Stop manual lab lanes that are not under test.
- Consider closing Docker Desktop, Sideloadly, LM Studio, and other large apps if they are not needed.
- Capture `sysctl -n vm.swapusage` before and after.

## After Long Benchmarks

- Run `scripts/omlx-power-policy.sh unload-large`.
- Run endpoint-only health and drift detection.
- Document benchmark output paths and model residency state.

## Review Outputs

Store benchmark and stability evidence under `docs/benchmarks/`. Keep temporary full health snapshots in `/tmp` unless they are intentionally summarized into docs.
