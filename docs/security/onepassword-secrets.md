# 1Password Secret Handling

## Policy

Secrets for local AI, DNS, GitHub-star trials, and agent integrations must not be committed to this repository.

Preferred storage:

```text
1Password vault: Boneman Projects
Item naming:
  <Repo or Tool Name> - Local AI
  <Repo or Tool Name> - API Token
  <Repo or Tool Name> - Service Config
```

Observed CLI state on 2026-06-22:

- `op` CLI is installed.
- Signed-in account is visible.
- A vault named `Boneman Projects` was not initially listed by `op vault list`.
- The approval prompt allowed creating `Boneman Projects` when `Boneman` existed.
- `Boneman Projects` was created successfully and is the confirmed target vault.

No 1Password items were created in this pass because no implemented star required a secret.

## Current Vault

```text
1Password vault: Boneman Projects
Status: created and available
Items created by this repo pass: none
```

## Documentation Pattern

When a future integration needs a secret, document it like this:

```text
1Password vault: Boneman Projects
Item: <Tool Name> - API Token
Field: credential
Used by: <script/config path>
Runtime env var: <ENV_VAR_NAME>
```

Do not document secret values, token prefixes, session cookies, private keys, or raw config files containing credentials.

## Validation

Before committing secret-aware changes:

```bash
git diff | grep -Ei 'secret|token|password|apikey|api_key|private_key|BEGIN RSA|BEGIN OPENSSH' || true
git diff --cached | grep -Ei 'secret|token|password|apikey|api_key|private_key|BEGIN RSA|BEGIN OPENSSH' || true
```

Inspect any hits manually. Documentation that names secret handling policy is acceptable; real values are not.
