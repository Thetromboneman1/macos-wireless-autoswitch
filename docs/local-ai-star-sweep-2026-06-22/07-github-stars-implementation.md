# Loop 6 - GitHub Stars Implementation

## Evidence

- Exported 45 starred repos to `github-stars.json`.
- Relevant high-signal stars included `nvk/llm-wiki`, `addyosmani/agent-skills`, `headroomlabs-ai/headroom`, `ApodexAI/AgentHarness`, `aaif-goose/goose`, `google-gemma/gemma-skills`, `osaurus-ai/osaurus`, `apple/container`, `NousResearch/hermes-agent`, `dodo-reach/hermes-desktop`, and `Egonex-AI/Understand-Anything`.

## Implemented

| Star / source | Action | Why |
| --- | --- | --- |
| `nvk/llm-wiki` | Documented as a future Codex/OpenCode knowledge-base candidate | High relevance, but install should wait for a chosen wiki corpus. |
| `google-gemma/gemma-skills` | Documented as an agent-skill watch item | Relevant to Gemma/tool-use behavior; no install needed today. |
| `NousResearch/hermes-agent` / local Hermes stack | Validated existing local wiring instead of replacing it | Local repos already carry Hermes/OpenCode integration work. |
| `ggml-org/llama.cpp` local checkout | Standardized wrapper scripts around the existing lane | Highest practical value because it is already built, loaded, and benchmarked. |

## Skipped or Deferred

| Star | Reason |
| --- | --- |
| `headroomlabs-ai/headroom` | Interesting token compression, but adding a proxy/MCP layer now would increase complexity before a concrete bottleneck. |
| `ApodexAI/AgentHarness` | Evaluation harness is useful later; no Apodex model is currently selected for serving. |
| `apple/container` | Useful Apple Silicon container tech, but Docker Desktop is already running and model serving must stay host-side. |
| `osaurus-ai/osaurus` | Overlaps agent harness territory; evaluate separately before installing. |
| `Aider-AI/aider` | Duplicates existing Codex/OpenCode/Hermes workflows. |
| `LEANN`, `turbovec`, `Understand-Anything` | Promising RAG/code-map tools, but require a separate indexing scope and storage plan. |
| `Kimi-K2.7-Code-GGUF` | Large multi-part model with non-Apache license metadata; defer download until explicitly approved. |

