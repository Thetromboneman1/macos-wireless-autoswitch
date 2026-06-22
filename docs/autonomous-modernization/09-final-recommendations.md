# 09 - Final Recommendations

## 2026-06-22 Star Deployment Update

The recommended starred repos from the deferred-star reassessment have now been implemented locally where safe. See [15-star-deployment-implementation.md](15-star-deployment-implementation.md) for installed paths, launch commands, validation results, safety notes, and rollback steps.

## What Changed

- Added autonomous modernization docs.
- Added MLX-vs-llama benchmark harness: `scripts/local-ai/benchmark-engine-bakeoff.py`.
- Captured benchmark results in `benchmark-results.json`.
- Captured raw and ranked GitHub stars.
- Added DNSCrypt audit at `docs/network/dnscrypt-audit.md`.

## What Was Installed

The latest deployment pass installed LEANN, Octopoda, edge-lm, PonyExl3, turbovec, SiliconScope CLI, llm-wiki, Understand-Anything, OmniRoute dependencies, headroom proxy, and the OpenHands agent-server image. See [15-star-deployment-implementation.md](15-star-deployment-implementation.md).

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
