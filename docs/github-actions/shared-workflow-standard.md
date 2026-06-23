# Shared Workflow Standard

Date: 2026-06-23

## Action Versions

Use current supported first-party action major versions:

- `actions/checkout@v5`
- `actions/setup-python@v6`

Use ecosystem actions only after checking release notes and permission changes.

## Trigger Pattern

Validation workflows should prefer:

```yaml
on:
  push:
    paths:
      - ".github/workflows/**"
      - "docs/**"
      - "scripts/**"
  pull_request:
  workflow_dispatch:
```

Avoid combining validation with publishing, notification, branch rewrite, or
pull-request creation side effects.

## Permissions

Default to:

```yaml
permissions:
  contents: read
```

Escalate job permissions only where required and document why.

## Local Checks

Run these before pushing workflow changes:

```bash
actionlint .github/workflows/*.yml
yamllint -d '{extends: default, rules: {line-length: disable, document-start: disable, truthy: disable}}' .github/workflows/*.yml
```

Use stricter repository configs when a repo already has them.
