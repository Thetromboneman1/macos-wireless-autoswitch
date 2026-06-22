# 09 - Final Recommendations

## 2026-06-22 Star Deployment Update

The recommended starred repos from the deferred-star reassessment have now been implemented locally where safe. See [15-star-deployment-implementation.md](15-star-deployment-implementation.md) for installed paths, launch commands, validation results, safety notes, and rollback steps.

## 2026-06-22 Unified Platform Update

The installed star tools now have a shared platform architecture and operating model. See:

- [16-unified-ai-platform-architecture.md](16-unified-ai-platform-architecture.md)
- [17-ai-platform-integration-report.md](17-ai-platform-integration-report.md)
- [MCP topology](../architecture/mcp-topology.md)
- [Model routing](../architecture/model-routing.md)
- [Knowledge layer](../architecture/knowledge-layer.md)
- [Platform runbook](../operations/platform-runbook.md)
- [Secret inventory](../security/secret-inventory.md)

The canonical 1Password vault for local AI and star-tool secrets is `Boneman`. The older `Boneman Projects` vault is an empty duplicate and should not receive new items.

## What Changed

- Added autonomous modernization docs.
- Added MLX-vs-llama benchmark harness: `scripts/local-ai/benchmark-engine-bakeoff.py`.
- Captured benchmark results in `benchmark-results.json`.
- Captured raw and ranked GitHub stars.
- Added DNSCrypt audit at `docs/network/dnscrypt-audit.md`.
- Added unified platform routing, MCP, knowledge-layer, operations, and secret-inventory docs.
- Added `config/local-ai-platform/routing-policy.json`, `config/local-ai-platform/mcp-topology.json`, and `scripts/star-tools/platform-status.sh`.

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
