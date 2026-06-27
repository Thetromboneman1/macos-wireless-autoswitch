#!/usr/bin/env bash
set -euo pipefail

ROOT="${ORNITH_GGUF_ROOT:-$HOME/Developer/ML-Models/Ornith}"
LLAMA_SERVER="${LLAMA_SERVER:-$HOME/Developer/ML-Models/Gemma4/repos/llama.cpp/build/bin/llama-server}"
MODEL="${ORNITH_GGUF_MODEL:-$ROOT/models/deepreinforce-ai-Ornith-1.0-35B-GGUF/ornith-1.0-35b-Q4_K_M.gguf}"
HOST="${ORNITH_GGUF_HOST:-127.0.0.1}"
PORT="${ORNITH_GGUF_PORT:-8003}"
CTX_SIZE="${ORNITH_GGUF_CTX_SIZE:-65536}"
PARALLEL="${ORNITH_GGUF_PARALLEL:-1}"
PID_FILE="${ORNITH_GGUF_PID_FILE:-$HOME/.local/state/ornith-gguf-coding-lane.pid}"
LOG_FILE="${ORNITH_GGUF_LOG_FILE:-$HOME/.local/state/ornith-gguf-coding-lane.log}"
TMUX_SESSION="${ORNITH_GGUF_TMUX_SESSION:-ornith-gguf-coding-lane}"
MODEL_ID="${ORNITH_GGUF_MODEL_ID:-ornith-1.0-35b-Q4_K_M.gguf}"

usage() {
  cat <<'USAGE'
Usage: scripts/ornith-gguf-coding-lane.sh <command>

Commands:
  start      Start the host-side llama.cpp Ornith GGUF lane on 127.0.0.1:8003
  stop       Stop the Ornith lane
  restart    Restart the Ornith lane
  status     Show PID, endpoint, model registry, and recent log tail
  logs       Tail the Ornith lane log
  bench      Run a compact coding benchmark against the lane

Environment overrides:
  ORNITH_GGUF_ROOT, LLAMA_SERVER, ORNITH_GGUF_MODEL, ORNITH_GGUF_HOST
  ORNITH_GGUF_PORT, ORNITH_GGUF_CTX_SIZE, ORNITH_GGUF_PARALLEL
USAGE
}

endpoint() {
  printf 'http://%s:%s/v1\n' "$HOST" "$PORT"
}

ensure_files() {
  for path in "$LLAMA_SERVER" "$MODEL"; do
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
  local deadline=$((SECONDS + 240))
  while [ "$SECONDS" -lt "$deadline" ]; do
    if curl -fsS --max-time 2 "$(endpoint)/models" >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done
  echo "Ornith lane did not become ready at $(endpoint) within 240 seconds." >&2
  return 1
}

start_lane() {
  ensure_files
  mkdir -p "$(dirname "$PID_FILE")" "$(dirname "$LOG_FILE")"
  if pid_running; then
    echo "Ornith lane already running as PID $(cat "$PID_FILE" 2>/dev/null || echo unknown) at $(endpoint)"
    return 0
  fi
  if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    echo "Port $PORT is already in use. Stop the conflicting service or set ORNITH_GGUF_PORT." >&2
    return 1
  fi
  if command -v tmux >/dev/null 2>&1; then
    tmux new-session -d -s "$TMUX_SESSION" \
      "exec '$LLAMA_SERVER' -m '$MODEL' -ngl 999 -fa on -c '$CTX_SIZE' --parallel '$PARALLEL' --host '$HOST' --port '$PORT' --no-ui >'$LOG_FILE' 2>&1"
    tmux list-panes -t "$TMUX_SESSION" -F '#{pane_pid}' > "$PID_FILE"
  else
    nohup "$LLAMA_SERVER" \
      -m "$MODEL" \
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
  echo "Ornith lane ready at $(endpoint) with $MODEL_ID"
}

stop_lane() {
  if command -v tmux >/dev/null 2>&1 && tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    tmux kill-session -t "$TMUX_SESSION"
    rm -f "$PID_FILE"
    echo "Stopped Ornith lane tmux session."
    return 0
  fi
  if pid_running; then
    local pid
    pid="$(cat "$PID_FILE")"
    kill "$pid" 2>/dev/null || true
    for _ in $(seq 1 20); do
      if ! kill -0 "$pid" 2>/dev/null; then
        rm -f "$PID_FILE"
        echo "Stopped Ornith lane."
        return 0
      fi
      sleep 1
    done
    kill -9 "$pid" 2>/dev/null || true
    rm -f "$PID_FILE"
    echo "Force-stopped Ornith lane."
  else
    rm -f "$PID_FILE"
    echo "Ornith lane is not running."
  fi
}

status_lane() {
  echo "Endpoint: $(endpoint)"
  echo "Model: $MODEL_ID"
  echo "Mode: llama.cpp Metal GGUF candidate"
  if pid_running; then
    if command -v tmux >/dev/null 2>&1 && tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
      echo "tmux session: $TMUX_SESSION"
    fi
    echo "PID: $(cat "$PID_FILE" 2>/dev/null || echo unknown)"
  else
    echo "PID: not running"
  fi
  if curl -fsS --max-time 5 "$(endpoint)/models" >/tmp/ornith-gguf-coding-models.json 2>/dev/null; then
    jq -r '.data[].id' /tmp/ornith-gguf-coding-models.json
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
  curl -sS --max-time 180 "$(endpoint)/chat/completions" \
    -H 'Content-Type: application/json' \
    -d "$req" >/tmp/ornith-gguf-coding-warm.json
  curl -sS --max-time 180 -w '\n%{time_total}\n' "$(endpoint)/chat/completions" \
    -H 'Content-Type: application/json' \
    -d "$req" >/tmp/ornith-gguf-coding-bench.txt
  python3 - <<'PY'
import json
from pathlib import Path

text = Path("/tmp/ornith-gguf-coding-bench.txt").read_text()
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
