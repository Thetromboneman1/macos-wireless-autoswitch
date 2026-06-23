# OnePassword Runbook

Date: 2026-06-23

## Canonical Vault

```text
Boneman
```

Validated with:

```bash
op vault get Boneman --format json
```

## Usage Rules

- Store secret values in Boneman, not in Git.
- Store pointers and handling instructions in docs.
- Do not store local runtime API keys in GitHub Actions.
- For automation, prefer short-lived manual export from Boneman over committed `.env` files.

## Timeout Wrapper

Use a timeout for automation checks so a 1Password prompt does not hang validation:

```bash
timeout 20s op vault get Boneman --format json
```
