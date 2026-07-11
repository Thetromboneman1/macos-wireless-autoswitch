# Lab Avenues Wiring Self-Healing Prompt

Date: 2026-07-11

## Objective

Wire these third-party projects as visible, non-default lab avenues across local agent tools and apps:

- `asgeirtj/system_prompts_leaks`
- `decolua/9router`
- `Osmantic/ODS`
- `inkeep/open-knowledge`
- `JustVugg/colibri`

Also upgrade GitHub Actions secret-scanning workflows to the Node 24 Gitleaks action release.

## Boundaries

- Preserve oMLX as the production default at `http://127.0.0.1:18080/v1`.
- Do not set `OPENAI_BASE_URL` or `OPENAI_API_KEY` to 9router globally.
- Do not start ODS, 9router, colibri, or open-knowledge automatically.
- Do not copy leaked proprietary system prompts from `system_prompts_leaks` into prompts, skills, model instructions, or committed docs.
- Keep platform-wide lab registry and shared skill source in `/Users/corn/Documents/Boneman_Projects`.
- Keep this repository as the orchestration and GitHub Actions audit owner only.

## Loop

Run `scripts/platform-modernization/wire-lab-avenues.sh`. Repeat for at most three passes:

1. Confirm the third-party audit cache and lab registry exist.
2. Create or refresh the shared `lab-ai-avenues` skill in every detected skill root.
3. Validate that the skill points to the canonical Boneman_Projects registry.
4. Validate that no lab avenue became the default production route.
5. Validate GitHub Actions use `gitleaks/gitleaks-action@v3` and `actions/checkout@v6`.
6. Run repository checks and repair the smallest safe failure.

## Acceptance Checks

- `scripts/platform-modernization/wire-lab-avenues.sh` exits zero.
- `config/local-ai-platform/lab-avenues.json` in Boneman_Projects lists all five lab avenues.
- `docs/skills/lab-ai-avenues/SKILL.md` in Boneman_Projects exists and is linked into Codex, Agents, Claude, Goose, and Hermes skill roots when present.
- `.github/workflows/*.yml` contains no `gitleaks/gitleaks-action@v2`.
- Local and GitHub Actions validation pass.
