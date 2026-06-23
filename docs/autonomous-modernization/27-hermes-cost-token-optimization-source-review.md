# 27 - Hermes Cost Token Optimization Source Review

Date: 2026-06-23
Owner: Platform Operations

## Source

Primary source: `/Users/corn/Downloads/Cost & Token Optimization Megathread - Hermes Agent (June 2026) : r:hermesagent.pdf`.

Extracted evidence: `docs/autonomous-modernization/evidence/hermes-token-optimization/source-pdf-text.txt`.

The PDF is a Reddit community megathread. Its recommendations are useful test candidates, not authoritative configuration. Every accepted change below was checked against the installed Hermes CLI and this Mac's local-first oMLX architecture.

## Recommendation Map

| Source recommendation | Current local state | Applicability | Risk | Validation method | Decision | Status |
|---|---|---|---|---|---|---|
| Use cheap cloud providers such as DeepSeek Flash for default work. | Hermes default is local oMLX Gemma 4 26B-A4B at `127.0.0.1:18080/v1`. | Low for private local work. | Cloud privacy and spend risk. | Provider inventory and local health check. | Keep local-first; no new cloud default. | Rejected with evidence |
| Prefer direct provider APIs over OpenRouter for single-provider cloud use. | No new paid cloud provider configured in this pass. | Applicable if cloud fallback is later approved. | Secrets and data handling. | Secret inventory and provider data-handling runbook. | Document direct-provider preference. | Partially implemented |
| Disable unused toolsets to reduce fixed schema overhead. | CLI had browser, vision, image generation, TTS, cron, messaging, and computer-use enabled. | High. | Breaking workflows that need those tools. | `hermes tools list`, `hermes prompt-size --json`, Hermes one-shot. | Disabled high-cost CLI defaults; keep profile-based opt-in. | Implemented |
| Use `hermes-tool-router` if stable. | Not installed or verified here. | Deferred. | Plugin security and stability unknown. | Official source/security review required. | Do not install globally. | Deferred |
| Keep SOUL.md and USER.md compact. | SOUL/USER total is 184 words and about 1.2 KB. | Already optimized. | Losing durable preferences. | `wc -w` and file inspection. | No prompt compaction needed. | Already optimized |
| Prune stale or duplicate memory. | Built-in memory files are tiny: `MEMORY.md` 9 bytes, `USER.md` 15 bytes. | Low. | Destructive memory loss. | `hermes memory status`, file inventory. | No deletion; keep safe review runbook. | Already optimized |
| Compression should be enabled at 50% threshold, target ratio 20%, protect last 20. | Installed config already has `compression.enabled: true`, `threshold: 0.5`, `target_ratio: 0.2`, `protect_last_n: 20`. | High. | Context loss if too aggressive. | Config audit and Hermes one-shot. | Keep current defaults. | Already optimized |
| Do not lower compression below 0.30. | Current threshold is 0.50. | Applicable. | Context loss. | Config audit. | Document guardrail. | Implemented |
| Ensure compression model has enough context. | Summary model is local E4B; `context_length_cache.yaml` exists but pair quality was not exhaustively benchmarked. | Applicable. | Silent summary failure if too small. | Auxiliary model strategy doc. | Keep E4B for now; require long-context test before changing. | Partially implemented |
| Use prompt caching and verify hits, especially Anthropic. | Local oMLX health returned cached tokens `0`; Anthropic not configured in this pass. | Provider-specific. | Unsupported keys can break config. | Health usage fields and prompt-caching doc. | Do not add unsupported cache keys. | Partially implemented |
| Use local model primary plus controlled cloud fallback. | Local oMLX is primary; llama.cpp and Rapid-MLX are manual lanes. | High. | Cloud privacy and runaway spend. | Local health, port checks, routing policy. | Preserve local-first routing. | Already optimized |
| Avoid Gemma for Hermes because community reports tool-call issues. | This Mac previously validated Gemma tool calls; current oMLX one-shot and health pass. | Low without local failure. | Unnecessary model churn. | Local validation artifacts. | Do not demote Gemma without fresh failures. | Rejected with evidence |
| Avoid browser automation when APIs/CLI/text retrieval work. | Browser and computer-use were enabled for CLI. | High. | Losing browser-required workflows. | Toolset trim plus opt-in runbook. | Disable by default for CLI; use `-t browser` when needed. | Implemented |
| Schedule cron jobs off-peak and restrict job toolsets. | Hermes cron tooling supports per-job `enabled_toolsets`; no Hermes cron jobs were created here. | Applicable. | Duplicate jobs and hidden spend. | Source audit of `cronjob_tools.py` and runbook. | Document no unattended new cron jobs. | Implemented |
| Add weekly cost dashboard/audit. | AIOps cycle existed without Hermes token-cost section. | High. | Duplicated reporting. | Tests and generated JSON. | Added `scripts/operations/hermes-cost-report.py` and AIOps integration. | Implemented |
| Set provider budget alerts and hard caps. | No paid provider configured here. | Deferred until cloud approval. | Account spend and secrets exposure. | Security docs. | Document required Boneman/provider-dashboard controls. | Partially implemented |

## Key Evidence

Baseline fixed prompt estimate from `hermes prompt-size --json`:

| Component | Estimated tokens |
|---|---:|
| System prompt | 5,570 |
| Skills index | 2,788 |
| Memory | 38 |
| User profile | 40 |
| Tool schema | 11,694 |
| Total | 20,130 |

After disabling high-cost CLI defaults, `hermes tools list --platform cli` showed those tools disabled, but `hermes prompt-size --json` still reported the same 29-tool, 20,130-token estimate. Treat this as a Hermes measurement limitation or schema-loading behavior until a request-level dump proves actual reduction.

## Implementation Decision

The safe implemented optimization is availability trimming, not a claimed token-savings victory:

```bash
hermes tools disable --platform cli browser vision image_gen tts cronjob messaging computer_use
```

Rollback uses the backed-up config recorded in `docs/autonomous-modernization/evidence/hermes-token-optimization/config-backup-dir.txt` or explicit re-enable commands.
