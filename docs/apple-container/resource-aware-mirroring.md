# Resource-Aware Mirroring

Updated: 2026-06-24

Use `scripts/apple-container/start-safe-batch.sh` instead of starting every candidate mirror. The scheduler reads memory pressure, `vm_stat`, Docker usage, Apple Container usage, and `config/apple-container/resource-thresholds.json`; it starts at most one enabled candidate per batch unless thresholds are explicitly relaxed.
