# Loop 4 - Model Serving Implementation

## Evidence

- oMLX health: `status=healthy`, `model_count=4`, `loaded_count=0`, memory ceiling about 50 GiB.
- GGUF lane files exist:
  - 16 GB `gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf`
  - 440 MB MTP draft model
  - 1.1 GB `mmproj-BF16.gguf`
- GGUF lane command uses `-ngl 999`, `-fa on`, `-c 65536`, `--parallel 1`, `--spec-type draft-mtp`, `--spec-draft-n-max 4`.

## Change

Added required wrappers:

- `scripts/local-ai/start-default-model.sh`
- `scripts/local-ai/stop-default-model.sh`
- `scripts/local-ai/healthcheck.sh`
- `scripts/local-ai/benchmark-smoke.sh`

These wrap the existing oMLX and `scripts/gemma4-gguf-coding-lane.sh` setup rather than installing another engine.

## Validation

- `scripts/local-ai/healthcheck.sh` returned oMLX and GGUF model lists.
- `scripts/local-ai/benchmark-smoke.sh` returned `OK` from oMLX and 128 GGUF completion tokens in `1.998155s`, about `64.06 output tok/s`.

