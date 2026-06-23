# GitHub Actions Node Runtime Migration

Date: 2026-06-23

## Driver

GitHub has announced the deprecation path for Node 20 on GitHub Actions
runners and recommends moving JavaScript actions to Node 24-compatible
versions where available.

Primary references:

- GitHub changelog:
  <https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/>
- `actions/checkout` releases:
  <https://github.com/actions/checkout/releases>
- `actions/setup-python` releases:
  <https://github.com/actions/setup-python/releases>

## Standard

Use these versions for first-party actions in owned repositories:

| Action | Standard Version | Notes |
| --- | --- | --- |
| `actions/checkout` | `v5` | Node 24-compatible release line. |
| `actions/setup-python` | `v6` | Node 24-compatible release line. |
| `docker/build-push-action` | `v6` | Current Docker build-push major used where already present. |

Do not bulk-update pinned SHA references or third-party actions without a
separate review of release notes and permissions.

## Repositories Updated

| Repository | Updated Files |
| --- | --- |
| `macos-wireless-autoswitch` | repository validation, release, fork sync, core validation workflows |
| `Ansible` | `lint.yml` |
| `Openclaw` | `auto-update.yml`, `compose-validate.yml` |
| `odysseus-gemma-docker` | `validate.yml` |
| `Hermes/hermes-webui` | release, tests, upstream sync workflows |
| `Hermes` | weekly sync/build workflow, Docker build-push action |

## Deferred

- `hermes-agent` contains many pinned action SHA references and is deeply
  behind upstream. It was inventoried but not rewritten.
- `hermes-desktop` is an ahead/behind reference checkout and was not merged.
- Scheduled workflows that create pull requests, publish containers, or send
  notifications were not manually dispatched during this pass.
