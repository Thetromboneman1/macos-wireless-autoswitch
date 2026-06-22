#!/usr/bin/env bash
set -euo pipefail

HOST="${DNSCRYPT_HEALTH_HOST:-127.0.0.1}"
PORT="${DNSCRYPT_HEALTH_PORT:-53530}"
QUERY="${DNSCRYPT_HEALTH_QUERY:-example.com}"
LOG_FILE="${DNSCRYPT_HEALTH_LOG:-$HOME/Library/Logs/dnscrypt-healthcheck.log}"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
  printf '%s %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$*" >>"$LOG_FILE"
}

check_dnscrypt() {
  lsof -nP -iUDP:"$PORT" -iTCP:"$PORT" 2>/dev/null | grep -q "$HOST:$PORT" &&
    dig +time=5 +tries=1 @"$HOST" -p "$PORT" "$QUERY" >/dev/null
}

if check_dnscrypt; then
  log "ok host=$HOST port=$PORT query=$QUERY"
  exit 0
fi

log "initial-fail host=$HOST port=$PORT query=$QUERY; restarting dnscrypt-proxy"
brew services restart dnscrypt-proxy >>"$LOG_FILE" 2>&1 || true
sleep 3

if check_dnscrypt; then
  log "recovered host=$HOST port=$PORT query=$QUERY"
  exit 0
fi

log "failed host=$HOST port=$PORT query=$QUERY"
exit 1
