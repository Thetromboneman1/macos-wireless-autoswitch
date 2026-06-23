# 1Password Secret Handling

Date: 2026-06-23
Owner: Platform Operations

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

The 2026-06-23 skills and VS Code integration pass also created no new 1Password items. Newly installed editor extensions and Codex skills either use existing local sessions, no credentials, or are documented as deferred/manual approval when they would require external tokens.

## Current Vault

```text
1Password vault: Boneman
Status: available and already contains local AI/service items
Items created by this repo pass: none
```

Operational runbook: [onepassword-runbook.md](../operations/onepassword-runbook.md).

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

## 1Password CLI Hangs

If `op` appears to hang, treat it as an authorization/session issue before retrying blindly:

```bash
timeout 20s op vault get Boneman --format json
```

Operational guidance:

- keep Boneman as the only target vault for this stack;
- do not store raw local runtime config files in docs or Git;
- document secret locations and item names, not values;
- retry once after unlocking 1Password, then record the blocker in the runbook if it still hangs.

## Tooling Added on 2026-06-23

The following installed tooling may need secrets only when live external integrations are enabled:

| Tool | Secret status |
|---|---|
| Codex `gh-address-comments`, `gh-fix-ci`, `yeet` skills | Uses existing `gh` auth; no repo secret. |
| VS Code Kubernetes Tools | Uses local kubeconfig/keychain; store cluster credentials in `Boneman` if created. |
| VS Code Terraform | Store Terraform Cloud token in `Boneman` only if cloud features are enabled. |
| VS Code PowerShell | Store remote Windows/Linux administration credentials in `Boneman` only if needed. |
| Sentry, Notion, deployment skills | Deferred/manual approval; store tokens in `Boneman` before use. |

## Duplicate Vault Handling

`Boneman Projects` was empty when audited and was deleted on 2026-06-22. The safe validation path is:

```bash
op vault get "Boneman Projects" --format json
```

The command should fail after deletion. Keep using `Boneman` for all new local AI, agent, and star-tool secrets.
