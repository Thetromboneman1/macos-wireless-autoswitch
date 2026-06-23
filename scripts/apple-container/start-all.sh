#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PORT_MAP="$ROOT/config/apple-container/port-map.json"
PILOT_ROOT="${APPLE_CONTAINER_PILOT_ROOT:-$HOME/.local/share/apple-container-pilot}"

"$ROOT/scripts/apple-container/validate-port-map.sh"

if ! command -v container >/dev/null 2>&1; then
  echo "container CLI is not installed" >&2
  exit 1
fi

if ! container system status >/dev/null 2>&1; then
  echo "Apple Container system service is not running. Start it with: container system start" >&2
  exit 1
fi

case "$PILOT_ROOT" in
  "$HOME"/.local/share/apple-container-pilot*) ;;
  *)
    echo "Refusing unsafe pilot root: $PILOT_ROOT" >&2
    exit 2
    ;;
esac

mkdir -p "$PILOT_ROOT/data" "$PILOT_ROOT/volumes" "$PILOT_ROOT/logs" "$PILOT_ROOT/state" "$PILOT_ROOT/env" "$PILOT_ROOT/backups" "$PILOT_ROOT/benchmarks" "$PILOT_ROOT/evidence"

while IFS= read -r service; do
  name="$(jq -r '.name' <<<"$service")"
  image="$(jq -r '.image' <<<"$service")"
  host="$(jq -r '.host' <<<"$service")"
  host_port="$(jq -r '.host_port' <<<"$service")"
  container_port="$(jq -r '.container_port' <<<"$service")"
  protocol="$(jq -r '.protocol' <<<"$service")"
  storage="$PILOT_ROOT/volumes/$name"
  cache="$storage/cache"

  case "$name" in
    ac-ntfy) ;;
    *)
      echo "No reviewed Apple Container start recipe for enabled service: $name" >&2
      exit 2
      ;;
  esac

  mkdir -p "$cache"
  chmod 700 "$storage" "$cache"

  if container inspect "$name" >/dev/null 2>&1; then
    echo "Starting existing pilot container: $name"
    container start "$name" >/dev/null || true
  else
    echo "Creating pilot container: $name"
    container run \
      -d \
      --name "$name" \
      --platform linux/arm64 \
      -p "${host}:${host_port}:${container_port}/${protocol}" \
      --mount "type=bind,source=${cache},target=/var/cache/ntfy" \
      -e "NTFY_BASE_URL=http://${host}:${host_port}" \
      -l "com.corn.apple-container-pilot=true" \
      "$image" serve
  fi
done < <(jq -c '.services[] | select(.enabled == true)' "$PORT_MAP")

"$ROOT/scripts/apple-container/health-all.sh"
