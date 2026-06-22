# 08 - Repository Sweep

## Local Repo Status

| Repo | Status | Action |
| --- | --- | --- |
| `macos-wireless-autoswitch` | active repo, one prior local commit ahead before this pass | Add modernization docs and benchmark harness. |
| `Boneman_Projects` | dirty with local AI docs | Do not mix into this commit. |
| `Hermes` | dirty and behind upstream | Separate reconciliation needed. |
| `Openclaw` | dirty Docker compose | Separate audit needed. |
| `odysseus-gemma-docker` | dirty local AI docs/scripts | Separate commit in that repo if desired. |
| `llama.cpp` | local checkout | Do not edit upstream checkout. |

## Broken or Risky Configs Found

- DNSCrypt config exists but is not in active resolver path.
- UDP DNS to router timed out during direct `dig`, though TCP and macOS resolver APIs worked.
- Some repo states are dirty or divergent and should not be merged blindly.

