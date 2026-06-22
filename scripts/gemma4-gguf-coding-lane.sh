#!/usr/bin/env bash
set -euo pipefail

ROOT="${GEMMA4_GGUF_ROOT:-$HOME/Developer/ML-Models/Gemma4}"
LLAMA_SERVER="${LLAMA_SERVER:-$ROOT/repos/llama.cpp/build/bin/llama-server}"
MODEL="${GEMMA4_GGUF_MODEL:-$ROOT/models/unsloth-gemma-4-26B-A4B-it-GGUF/gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf}"
MMPROJ="${GEMMA4_GGUF_MMPROJ:-$ROOT/models/unsloth-gemma-4-26B-A4B-it-GGUF/mmproj-BF16.gguf}"
HOST="${GEMMA4_GGUF_HOST:-127.0.0.1}"
PORT="${GEMMA4_GGUF_PORT:-8002}"
CTX_SIZE="${GEMMA4_GGUF_CTX_SIZE:-65536}"
PARALLEL="${GEMMA4_GGUF_PARALLEL:-1}"
PID_FILE="${GEMMA4_GGUF_PID_FILE:-$HOME/.local/state/gemma4-gguf-coding-lane.pid}"
LOG_FILE="${GEMMA4_GGUF_LOG_FILE:-$HOME/.local/state/gemma4-gguf-coding-lane.log}"
TMUX_SESSION="${GEMMA4_GGUF_TMUX_SESSION:-gemma4-gguf-coding-lane}"
MODEL_ID="gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf"

usage() {
  cat <<'USAGE'
Usage: scripts/gemma4-gguf-coding-lane.sh <command>

Commands:
  start      Start the host-side llama.cpp no-MTP GGUF coding lane on 127.0.0.1:8002
  stop       Stop the coding lane
  restart    Restart the coding lane
  status     Show PID, endpoint, model registry, and recent log tail
  logs       Tail the coding lane log
  bench      Run a 128-token coding benchmark against the lane

Environment overrides:
  GEMMA4_GGUF_ROOT, LLAMA_SERVER, GEMMA4_GGUF_MODEL, GEMMA4_GGUF_MMPROJ
  GEMMA4_GGUF_HOST, GEMMA4_GGUF_PORT, GEMMA4_GGUF_CTX_SIZE, GEMMA4_GGUF_PARALLEL
USAGE
}

endpoint() {
  printf 'http://%s:%s/v1\n' "$HOST" "$PORT"
}

ensure_files() {
  for path in "$LLAMA_SERVER" "$MODEL" "$MMPROJ"; do
    if [ ! -e "$path" ]; then
      echo "Missing required file: $path" >&2
      return 1
    fi
  done
}

pid_running() {
  if command -v tmux >/dev/null 2>&1 && tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    return 0
  fi
  [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null
}

wait_ready() {
  local deadline=$((SECONDS + 180))
  while [ "$SECONDS" -lt "$deadline" ]; do
    if curl -fsS --max-time 2 "$(endpoint)/models" >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done
  echo "Coding lane did not become ready at $(endpoint) within 180 seconds." >&2
  return 1
}

start_lane() {
  ensure_files
  mkdir -p "$(dirname "$PID_FILE")" "$(dirname "$LOG_FILE")"
  if pid_running; then
    echo "Coding lane already running as PID $(cat "$PID_FILE") at $(endpoint)"
    return 0
  fi
  if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    echo "Port $PORT is already in use. Stop the conflicting service or set GEMMA4_GGUF_PORT." >&2
    return 1
  fi
  if command -v tmux >/dev/null 2>&1; then
    tmux new-session -d -s "$TMUX_SESSION" \
      "exec '$LLAMA_SERVER' -m '$MODEL' --mmproj '$MMPROJ' -ngl 999 -fa on -c '$CTX_SIZE' --parallel '$PARALLEL' --host '$HOST' --port '$PORT' --no-ui >'$LOG_FILE' 2>&1"
    tmux list-panes -t "$TMUX_SESSION" -F '#{pane_pid}' > "$PID_FILE"
  else
    nohup "$LLAMA_SERVER" \
      -m "$MODEL" \
      --mmproj "$MMPROJ" \
      -ngl 999 \
      -fa on \
      -c "$CTX_SIZE" \
      --parallel "$PARALLEL" \
      --host "$HOST" \
      --port "$PORT" \
      --no-ui \
      >"$LOG_FILE" 2>&1 < /dev/null &
    echo $! > "$PID_FILE"
  fi
  wait_ready
  echo "Coding lane ready at $(endpoint) with $MODEL_ID in no-MTP mode"
}

stop_lane() {
  if command -v tmux >/dev/null 2>&1 && tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    tmux kill-session -t "$TMUX_SESSION"
    rm -f "$PID_FILE"
    echo "Stopped coding lane tmux session."
    return 0
  fi
  if pid_running; then
    local pid
    pid="$(cat "$PID_FILE")"
    kill "$pid" 2>/dev/null || true
    for _ in $(seq 1 20); do
      if ! kill -0 "$pid" 2>/dev/null; then
        rm -f "$PID_FILE"
        echo "Stopped coding lane."
        return 0
      fi
      sleep 1
    done
    kill -9 "$pid" 2>/dev/null || true
    rm -f "$PID_FILE"
    echo "Force-stopped coding lane."
  else
    rm -f "$PID_FILE"
    echo "Coding lane is not running."
  fi
}

status_lane() {
  echo "Endpoint: $(endpoint)"
  echo "Model: $MODEL_ID"
  echo "Mode: no-MTP Apple Silicon lane"
  if pid_running; then
    if command -v tmux >/dev/null 2>&1 && tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
      echo "tmux session: $TMUX_SESSION"
    fi
    echo "PID: $(cat "$PID_FILE" 2>/dev/null || echo unknown)"
  else
    echo "PID: not running"
  fi
  if curl -fsS --max-time 5 "$(endpoint)/models" >/tmp/gemma4-gguf-coding-models.json 2>/dev/null; then
    jq -r '.data[].id' /tmp/gemma4-gguf-coding-models.json
  else
    echo "Model registry: unreachable"
  fi
  if [ -f "$LOG_FILE" ]; then
    echo "Recent log:"
    tail -20 "$LOG_FILE"
  fi
}

bench_lane() {
  wait_ready
  local req
  req="$(jq -n --arg model "$MODEL_ID" --arg prompt 'Write a compact Python function that parses a unified diff and returns the changed file paths. Then explain two edge cases.' \
    '{model:$model,messages:[{role:"user",content:$prompt}],max_tokens:128,temperature:0,stream:false}')"
  curl -sS --max-time 120 "$(endpoint)/chat/completions" \
    -H 'Content-Type: application/json' \
    -d "$req" >/tmp/gemma4-gguf-coding-warm.json
  curl -sS --max-time 120 -w '\n%{time_total}\n' "$(endpoint)/chat/completions" \
    -H 'Content-Type: application/json' \
    -d "$req" >/tmp/gemma4-gguf-coding-bench.txt
  python3 - <<'PY'
import json
from pathlib import Path

text = Path("/tmp/gemma4-gguf-coding-bench.txt").read_text()
body, curl_time = text.rsplit("\n", 2)[0], text.rsplit("\n", 2)[1]
data = json.loads(body)
usage = data.get("usage") or {}
tokens = usage.get("completion_tokens") or usage.get("output_tokens") or 0
seconds = float(curl_time)
print(f"completion_tokens={tokens}")
print(f"curl_seconds={seconds:.6f}")
print(f"output_tok_s={(tokens / seconds) if seconds and tokens else 0:.2f}")
PY
}

cmd="${1:-}"
case "$cmd" in
  start) start_lane ;;
  stop) stop_lane ;;
  restart) stop_lane; start_lane ;;
  status) status_lane ;;
  logs) tail -f "$LOG_FILE" ;;
  bench) bench_lane ;;
  -h|--help|help|"") usage ;;
  *) echo "Unknown command: $cmd" >&2; usage; exit 2 ;;
esac
