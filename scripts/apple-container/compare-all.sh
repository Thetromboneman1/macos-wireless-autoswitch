#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PORT_MAP="$ROOT/config/apple-container/port-map.json"
REPORT="${1:-}"

tmp_report="$(mktemp)"
printf '{"created_at":"%s","results":[' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$tmp_report"
first=1

while IFS= read -r service; do
  name="$(jq -r '.name' <<<"$service")"
  docker_url="$(jq -r '.docker_health_url' <<<"$service")"
  pilot_url="$(jq -r '.health_url' <<<"$service")"
  docker_status="fail"
  pilot_status="fail"
  docker_ms="$(curl -fsS -o /dev/null -w '%{time_total}' --max-time 10 "$docker_url" 2>/dev/null || true)"
  pilot_ms="$(curl -fsS -o /dev/null -w '%{time_total}' --max-time 10 "$pilot_url" 2>/dev/null || true)"
  if [[ -n "$docker_ms" ]]; then docker_status="pass"; else docker_ms="null"; fi
  if [[ -n "$pilot_ms" ]]; then pilot_status="pass"; else pilot_ms="null"; fi
  if [[ "$first" -eq 0 ]]; then printf ',' >> "$tmp_report"; fi
  first=0
  jq -n \
    --arg service "$name" \
    --arg docker_url "$docker_url" \
    --arg pilot_url "$pilot_url" \
    --arg docker_status "$docker_status" \
    --arg pilot_status "$pilot_status" \
    --argjson docker_seconds "$docker_ms" \
    --argjson pilot_seconds "$pilot_ms" \
    '{service:$service,docker:{url:$docker_url,status:$docker_status,seconds:$docker_seconds},apple_container:{url:$pilot_url,status:$pilot_status,seconds:$pilot_seconds}}' >> "$tmp_report"
done < <(jq -c '.services[] | select(.enabled == true)' "$PORT_MAP")

printf ']}\n' >> "$tmp_report"
if [[ -n "$REPORT" ]]; then
  mkdir -p "$(dirname "$REPORT")"
  cp "$tmp_report" "$REPORT"
fi
cat "$tmp_report"
rm -f "$tmp_report"
