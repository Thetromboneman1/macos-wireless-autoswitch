# Hermes Browser Cost Controls

Date: 2026-06-23
Owner: Platform Operations

## Decision

Browser, vision, and computer-use toolsets are disabled for default CLI sessions. This prevents screenshot-heavy workflows from becoming accidental defaults.

Use this preference order:

1. API
2. CLI
3. Structured text retrieval
4. Browser automation only when necessary

## Browser-Required Opt-In

```bash
hermes -z "..." -t web,browser,vision,file,skills,clarify
```

Do not remove Playwright, browser, or vision capabilities globally; Codex/UI validation and specific Hermes workflows may still require them.
