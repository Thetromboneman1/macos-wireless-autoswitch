# Third-Party AI Tooling Self-Healing Setup Prompt

Date: 2026-07-11

## Objective

Download, classify, install, and wire the approved parts of these repositories into the local toolchain without breaking the existing oMLX-first local AI architecture:

- `mukul975/Anthropic-Cybersecurity-Skills`
- `asgeirtj/system_prompts_leaks`
- `decolua/9router`
- `Osmantic/ODS`
- `itsfatduck/optimizerDuck`
- `inkeep/open-knowledge`
- `JustVugg/colibri`
- `tirth8205/code-review-graph`

## Boundaries

- Keep this repository focused on macOS wireless autoswitching and direct LaunchDaemon support.
- Put downloaded third-party source checkouts and platform-wide audit state under `/Users/corn/Documents/Boneman_Projects/local-ai-platform/third-party-tool-audit`.
- Preserve local model routing defaults:
  - oMLX: `http://127.0.0.1:18080/v1`
  - llama.cpp GGUF coding lane: `http://127.0.0.1:8002/v1`
  - Rapid-MLX lab lane: `http://127.0.0.1:8010/v1`
  - no Ollama default unless fresh benchmark evidence changes the architecture.
- Never copy leaked proprietary system prompts into tool instructions, model prompts, or committed docs.
- Never commit secrets. Store secret references only, using 1Password vault `Boneman`.

## Loop

Run `scripts/platform-modernization/install-third-party-ai-tooling.sh` from this repository. Repeat for at most three passes:

1. Inventory local repo state, GitHub Actions state, available tools, and existing agent skill roots.
2. Clone or refresh the eight requested repositories into the Boneman_Projects audit cache.
3. Classify every repository as `installed`, `audit-only`, `lab-candidate`, or `rejected`.
4. Install only approved assets:
   - install Apache-licensed cybersecurity skills into local agent skill roots with a `cybersecurity-` prefix;
   - verify `code-review-graph` availability, but do not replace the existing indexed `codebase-memory-mcp` unless it is explicitly better in a future measured comparison;
   - keep router/runtime/platform replacements disabled unless they pass an oMLX-first compatibility review.
5. Generate a local audit report and a machine-readable manifest.
6. Validate repository workflows and changed docs/scripts.
7. If validation fails, apply the smallest safe fix and repeat.

Stop early when clone, classification, installation, manifest generation, and validation all pass.

## Remediation Rules

- If a clone fails, retry with a shallow fetch once, then mark the repo `blocked`.
- If a tool install would rewrite `OPENAI_BASE_URL`, `OPENAI_API_KEY`, Codex config, Claude config, Goose config, Hermes config, or MCP config, capture a dry-run note instead of applying it.
- If a repo is Windows-only, mark it `audit-only` on this Mac.
- If a repo contains leaked system prompts, keep it outside all prompt/skill roots and record only metadata.
- If a repo introduces a competing model server or gateway, treat it as `lab-candidate` and do not start it automatically.
- If pre-existing local dirty work is found outside this change set, preserve it and report it.

## Acceptance Checks

- `scripts/platform-modernization/install-third-party-ai-tooling.sh` exits zero.
- `docs/github-actions/third-party-ai-tooling-audit.md` records every requested repo with status and rationale.
- `.github/workflows/*.yml` passes `actionlint`.
- Changed shell scripts pass `shellcheck`.
- Markdown docs pass `markdownlint`.
- `gitleaks detect --no-banner --redact --source .` passes for this repository.
