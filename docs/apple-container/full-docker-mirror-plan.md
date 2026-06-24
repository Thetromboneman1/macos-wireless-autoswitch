# Full Docker Mirror Plan

Updated: 2026-06-24

Docker remains production. Apple Container mirrors are side-by-side candidates only. The validated pattern is `ac-ntfy` on `127.0.0.1:19091`, isolated from Docker production data and compared with Docker ntfy on `127.0.0.1:8091`.

Next candidates must pass resource gates, ARM64 image checks, isolated storage checks, health checks, restart checks, rollback checks, and side-by-side comparison before they are left running.
