# Gitleaks Remediation

Date: 2026-06-23

## Summary

Initial full working-tree scan:

```text
gitleaks detect --no-git --source . --redact
findings: 360
```

All findings were in ignored local artifacts:

- `backups/dnscrypt-20260622-105231/`
- `tmp/star-downloads/`

No tracked staged changes contained leaks when checked with:

```text
gitleaks protect --staged --redact --verbose
```

## Classification

| Location | Findings | Classification | Action |
|---|---:|---|---|
| `backups/dnscrypt-20260622-105231/dnscrypt-proxy.toml` | 9 | local backup artifact | Removed ignored backup directory from working tree. |
| `tmp/star-downloads/Aider-AI__aider` | 31 | downloaded third-party tests/docs | Removed ignored download tree. |
| `tmp/star-downloads/OpenHands__OpenHands` | 23 | downloaded third-party tests/docs | Removed ignored download tree. |
| `tmp/star-downloads/RyjoxTechnologies__Octopoda-OS` | 12 | downloaded third-party tests/docs | Removed ignored download tree. |
| `tmp/star-downloads/affaan-m__ECC` | 11 | downloaded third-party tests/docs | Removed ignored download tree. |
| `tmp/star-downloads/diegosouzapw__OmniRoute` | 100+ | downloaded third-party tests/docs and examples | Removed ignored download tree. |
| `tmp/star-downloads/go-gitea__gitea` | 60+ | downloaded third-party fixtures/test keys | Removed ignored download tree. |
| `tmp/star-downloads/headroomlabs-ai__headroom` | 40+ | downloaded third-party tests/docs | Removed ignored download tree. |
| `tmp/star-downloads/osaurus-ai__osaurus` | 7 | downloaded third-party tests/vendor code | Removed ignored download tree. |
| Other `tmp/star-downloads/*` rows | remainder | downloaded third-party tests/docs | Removed ignored download tree. |

## Remediation Rule

Do not rewrite Git history for ignored local artifacts. Remove or regenerate them as needed. Keep `tmp/star-downloads/` and `backups/` ignored.
