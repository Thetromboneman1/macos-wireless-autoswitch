# Hermes MLX Troubleshooting

Date: 2026-06-22

## Tool Calls Fail

Run the validator before blaming the model:

```bash
scripts/local-ai/validate-hermes-mlx.py --name omlx-gemma26
```

If chat works but tool calls fail, try the Rapid-MLX lab lane, then llama.cpp, and record the backend-specific failure in the validation JSON.

## `host.docker.internal` Fails From Host

Use `127.0.0.1` for host tools like the Hermes CLI. Keep `host.docker.internal` for Docker consumers.

## Rapid-MLX Memory Warning

Stop optional large lanes and close memory-heavy apps:

```bash
tmux kill-session -t rapid-mlx-qwen 2>/dev/null || true
pkill -f 'rapid-mlx serve qwen3.6-35b-4bit' || true
scripts/gemma4-gguf-coding-lane.sh stop
vm_stat
```

Then restart only the lane you need.

## MTP Accidentally Enabled

The GGUF launcher should not contain `--spec-type draft-mtp` or `--model-draft`.

```bash
rg 'draft-mtp|model-draft' scripts/gemma4-gguf-coding-lane.sh
```

No matches are expected.

## Restore Default

```bash
scripts/local-ai/rollback-hermes-mlx.sh
open -a oMLX
```
