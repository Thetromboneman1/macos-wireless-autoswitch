# 09 - Final Recommendations

## What Changed

- Added autonomous modernization docs.
- Added MLX-vs-llama benchmark harness: `scripts/local-ai/benchmark-engine-bakeoff.py`.
- Captured benchmark results in `benchmark-results.json`.
- Captured raw and ranked GitHub stars.
- Added DNSCrypt audit at `docs/network/dnscrypt-audit.md`.

## What Was Installed

Nothing.

## What Was Removed

Nothing.

## Inference Recommendation

Primary default remains oMLX/MLX for the local agent stack. llama.cpp remains the best specialist GGUF coding lane and production-simulation server.

## DNS Recommendation

Do not switch DNS to local DNSCrypt until the service is running and UDP/TCP behavior is understood. First decide the front filter/resolver layer: AdGuard, Unbound, or dnscrypt-proxy standalone.

## Rollback

```bash
rm -rf docs/autonomous-modernization
rm -f docs/network/dnscrypt-audit.md
rm -f scripts/local-ai/benchmark-engine-bakeoff.py
git revert <commit>
```

