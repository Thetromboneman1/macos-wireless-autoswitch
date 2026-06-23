# Reusable Workflow Strategy

Date: 2026-06-23

## Current State

This repository has three small workflows. They are not yet large enough to require reusable workflow extraction inside this repo.

## Standard Patterns

| Pattern | Owner | Use |
|---|---|---|
| Core shell/plist validation | this repo | Keep in `validate.yml` until another repo needs identical checks. |
| Fork fast-forward sync | this repo | Keep repo-specific because upstream remote is hard-coded. |
| Release packaging | this repo | Keep repo-specific because package contents are product-specific. |

## Future Consolidation

Create a shared workflow only when at least two active repos need the same job contract. Candidate reusable jobs:

- shellcheck plus plist/XML validation;
- gitleaks staged diff scan;
- markdownlint and JSON/YAML/TOML validation;
- local AI docs validation.
