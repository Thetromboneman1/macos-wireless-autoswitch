# Apple Container Pilot Rollback

Date: 2026-06-23

Rollback command:

```bash
scripts/apple-container/rollback-all.sh
```

The rollback command:

1. stops only Apple Container containers whose names start with `ac-`,
2. removes only those pilot containers,
3. preserves pilot logs and data,
4. re-validates the pilot port map,
5. confirms oMLX production health on `127.0.0.1:18080`.

It does not delete `~/.local/share/apple-container-pilot`, Docker containers, Docker volumes, native model files, or secrets.

`ac-ntfy` was also tested with a narrower self-heal path: stopping only the pilot container, running `scripts/apple-container/self-heal.sh`, and confirming Docker production ntfy remained healthy.
