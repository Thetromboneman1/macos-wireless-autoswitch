# 1Password Secret Handling

## Policy

Secrets for local AI, DNS, GitHub-star trials, and agent integrations must not be committed to this repository.

Preferred storage:

```text
1Password vault: Boneman
Item naming:
  <Repo or Tool Name> - Local AI
  <Repo or Tool Name> - API Token
  <Repo or Tool Name> - Service Config
```

Observed CLI state on 2026-06-22:

- `op` CLI is installed.
- Signed-in account is visible.
- The canonical vault is `Boneman`.
- A previous run created `Boneman Projects`, but the user has corrected the target to `Boneman`.
- `Boneman Projects` was an empty duplicate and was removed on 2026-06-22.

No 1Password items were created in this pass because no implemented star required a secret.

## Current Vault

```text
1Password vault: Boneman
Status: available and already contains local AI/service items
Items created by this repo pass: none
```

## Documentation Pattern

When a future integration needs a secret, document it like this:

```text
1Password vault: Boneman
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

## Duplicate Vault Handling

`Boneman Projects` was empty when audited and was deleted on 2026-06-22. The safe validation path is:

```bash
op vault get "Boneman Projects" --format json
```

The command should fail after deletion. Keep using `Boneman` for all new local AI, agent, and star-tool secrets.
