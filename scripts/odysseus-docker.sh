#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ODYSSEUS_DIR="$ROOT_DIR/odysseus"
ENV_FILE="$ODYSSEUS_DIR/.env"
ENV_EXAMPLE="$ODYSSEUS_DIR/.env.example"
COMPOSE_FILE="$ODYSSEUS_DIR/docker-compose.yml"
PROJECT_NAME="${ODYSSEUS_PROJECT_NAME:-odysseus-gemma}"

usage() {
  cat <<'USAGE'
Usage: scripts/odysseus-docker.sh <command>

Commands:
  install     Create odysseus/.env, build/start Docker stack, configure Gemma roles
  up          Start Docker stack
  configure   Seed/update Odysseus Gemma endpoints and role defaults
  ps          Show containers
  logs        Tail Odysseus logs
  down        Stop containers
  url         Print local UI URL

Edit odysseus/.env to change Gemma endpoint URLs, model IDs, auth, or ports.
USAGE
}

ensure_env() {
  if [ ! -f "$ENV_FILE" ]; then
    cp "$ENV_EXAMPLE" "$ENV_FILE"
    echo "Created $ENV_FILE from .env.example"
  fi
}

load_env() {
  ensure_env
  set -a
  # shellcheck disable=SC1090
  . "$ENV_FILE"
  set +a
}

compose() {
  docker compose --env-file "$ENV_FILE" -p "$PROJECT_NAME" -f "$COMPOSE_FILE" "$@"
}

app_url() {
  local port="${APP_PORT:-7000}"
  printf 'http://127.0.0.1:%s\n' "$port"
}

wait_for_odysseus() {
  local url
  url="$(app_url)"
  local deadline=$((SECONDS + 180))
  while [ "$SECONDS" -lt "$deadline" ]; do
    if curl -fsS "$url" >/dev/null 2>&1; then
      return 0
    fi
    sleep 3
  done
  echo "Odysseus did not answer at $url within 180 seconds. Check: scripts/odysseus-docker.sh logs" >&2
  return 1
}

configure_gemma() {
  load_env
  wait_for_odysseus
  local gemma_api_key="${ODYSSEUS_GEMMA_API_KEY:-}"
  if [ -z "$gemma_api_key" ] && [ -f "$HOME/.omlx/settings.json" ]; then
    gemma_api_key="$(python3 - <<'PY'
import json
from pathlib import Path
try:
    data = json.loads(Path.home().joinpath(".omlx/settings.json").read_text(encoding="utf-8"))
    print((data.get("auth") or {}).get("api_key") or "")
except Exception:
    print("")
PY
)"
  fi
  compose exec -T \
    -e ODYSSEUS_GEMMA_BASE_URL="${ODYSSEUS_GEMMA_BASE_URL:-http://host.docker.internal:18080/v1}" \
    -e ODYSSEUS_GEMMA_PRIMARY_BASE_URL="${ODYSSEUS_GEMMA_PRIMARY_BASE_URL:-}" \
    -e ODYSSEUS_GEMMA_CODING_BASE_URL="${ODYSSEUS_GEMMA_CODING_BASE_URL:-}" \
    -e ODYSSEUS_GEMMA_FAST_BASE_URL="${ODYSSEUS_GEMMA_FAST_BASE_URL:-}" \
    -e ODYSSEUS_GEMMA_SMALL_BASE_URL="${ODYSSEUS_GEMMA_SMALL_BASE_URL:-}" \
    -e ODYSSEUS_GEMMA_PRIMARY_MODEL="${ODYSSEUS_GEMMA_PRIMARY_MODEL:-mlx-community--gemma-4-31b-it-4bit}" \
    -e ODYSSEUS_GEMMA_CODING_MODEL="${ODYSSEUS_GEMMA_CODING_MODEL:-mlx-community--gemma-4-26b-a4b-it-4bit}" \
    -e ODYSSEUS_GEMMA_FAST_MODEL="${ODYSSEUS_GEMMA_FAST_MODEL:-mlx-community--gemma-4-e4b-it-4bit}" \
    -e ODYSSEUS_GEMMA_SMALL_MODEL="${ODYSSEUS_GEMMA_SMALL_MODEL:-mlx-community--gemma-4-e2b-it-4bit}" \
    -e ODYSSEUS_GEMMA_API_KEY="$gemma_api_key" \
    odysseus python - <<'PY'
import json
import os
from datetime import datetime

from core.database import SessionLocal, ModelEndpoint, init_db
from src.settings import load_settings, save_settings

base = os.environ.get("ODYSSEUS_GEMMA_BASE_URL", "http://host.docker.internal:18080/v1").rstrip("/")
api_key = os.environ.get("ODYSSEUS_GEMMA_API_KEY", "")

roles = {
    "primary": {
        "id": "gemma-primary",
        "name": "Gemma 4 31B - primary chat/reasoning",
        "url": os.environ.get("ODYSSEUS_GEMMA_PRIMARY_BASE_URL") or base,
        "model": os.environ.get("ODYSSEUS_GEMMA_PRIMARY_MODEL", "mlx-community--gemma-4-31b-it-4bit"),
        "purpose": "primary chat/reasoning",
    },
    "coding": {
        "id": "gemma-coding",
        "name": "Gemma 4 26B A4B - coding/edit/apply",
        "url": os.environ.get("ODYSSEUS_GEMMA_CODING_BASE_URL") or base,
        "model": os.environ.get("ODYSSEUS_GEMMA_CODING_MODEL", "mlx-community--gemma-4-26b-a4b-it-4bit"),
        "purpose": "coding/edit/apply",
    },
    "fast": {
        "id": "gemma-fast",
        "name": "Gemma 4 E4B - fast chat/edit/apply/autocomplete",
        "url": os.environ.get("ODYSSEUS_GEMMA_FAST_BASE_URL") or base,
        "model": os.environ.get("ODYSSEUS_GEMMA_FAST_MODEL", "mlx-community--gemma-4-e4b-it-4bit"),
        "purpose": "fast chat/edit/apply/autocomplete",
    },
    "small": {
        "id": "gemma-small",
        "name": "Gemma 4 E2B - small/routing tasks",
        "url": os.environ.get("ODYSSEUS_GEMMA_SMALL_BASE_URL") or base,
        "model": os.environ.get("ODYSSEUS_GEMMA_SMALL_MODEL", "mlx-community--gemma-4-e2b-it-4bit"),
        "purpose": "small/routing tasks",
    },
}

init_db()
db = SessionLocal()
try:
    now = datetime.utcnow()
    for role in roles.values():
        ep = db.query(ModelEndpoint).filter(ModelEndpoint.id == role["id"]).first()
        if ep is None:
            ep = ModelEndpoint(id=role["id"], created_at=now)
            db.add(ep)
        ep.name = role["name"]
        ep.base_url = role["url"].rstrip("/")
        ep.api_key = api_key
        ep.is_enabled = True
        ep.cached_models = json.dumps([role["model"]])
        ep.pinned_models = json.dumps([role["model"]])
        ep.hidden_models = json.dumps([])
        ep.model_type = "llm"
        ep.endpoint_kind = "local"
        ep.model_refresh_mode = "manual"
        ep.supports_tools = True
        ep.owner = None
        ep.updated_at = now
    db.commit()

    settings = load_settings()
    settings.update({
        "default_endpoint_id": roles["primary"]["id"],
        "default_model": roles["primary"]["model"],
        "research_endpoint_id": roles["primary"]["id"],
        "research_model": roles["primary"]["model"],
        "utility_endpoint_id": roles["small"]["id"],
        "utility_model": roles["small"]["model"],
        "task_endpoint_id": roles["small"]["id"],
        "task_model": roles["small"]["model"],
        "default_model_fallbacks": [
            {"endpoint_id": roles["coding"]["id"], "model": roles["coding"]["model"]},
            {"endpoint_id": roles["fast"]["id"], "model": roles["fast"]["model"]},
            {"endpoint_id": roles["small"]["id"], "model": roles["small"]["model"]},
        ],
        "utility_model_fallbacks": [
            {"endpoint_id": roles["fast"]["id"], "model": roles["fast"]["model"]},
        ],
        "vision_model": roles["primary"]["model"],
        "vision_model_fallbacks": [
            {"endpoint_id": roles["fast"]["id"], "model": roles["fast"]["model"]},
        ],
    })
    save_settings(settings)

    os.makedirs("/app/data", exist_ok=True)
    with open("/app/data/gemma-role-map.json", "w", encoding="utf-8") as fh:
        json.dump({
            "configured_by": "scripts/odysseus-docker.sh",
            "roles": roles,
            "odysseus_settings": {
                "default": "primary",
                "research": "primary",
                "utility": "small",
                "task": "small",
                "fallback_order": ["coding", "fast", "small"],
            },
        }, fh, indent=2)
    print("Configured Gemma endpoints:")
    for key, role in roles.items():
        print(f"- {key}: {role['model']} @ {role['url']}")
finally:
    db.close()
PY
}

cmd="${1:-}"
case "$cmd" in
  install)
    load_env
    compose up -d --build
    configure_gemma
    echo "Odysseus is available at $(app_url)"
    ;;
  up)
    load_env
    compose up -d
    echo "Odysseus is available at $(app_url)"
    ;;
  configure)
    configure_gemma
    ;;
  ps)
    load_env
    compose ps
    ;;
  logs)
    load_env
    compose logs -f --tail=160 odysseus
    ;;
  down)
    load_env
    compose down
    ;;
  url)
    load_env
    app_url
    ;;
  -h|--help|help|"")
    usage
    ;;
  *)
    echo "Unknown command: $cmd" >&2
    usage >&2
    exit 2
    ;;
esac
