#!/usr/bin/env bash
set -euo pipefail

checkout="${UNDERSTAND_ANYTHING_REPO:-$HOME/.understand-anything/repo}"
cd "$checkout"

exec corepack pnpm --filter @understand-anything/dashboard dev "$@"
