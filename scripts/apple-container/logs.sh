#!/usr/bin/env bash
set -euo pipefail

service="${1:-}"

if ! command -v container >/dev/null 2>&1; then
  echo "container CLI is not installed" >&2
  exit 1
fi

if [[ -z "$service" ]]; then
  echo "Usage: $0 ac-service-name" >&2
  exit 2
fi

case "$service" in
  ac-*) ;;
  *)
    echo "Refusing to read logs for non-pilot container: $service" >&2
    exit 2
    ;;
esac

container logs "$service"
