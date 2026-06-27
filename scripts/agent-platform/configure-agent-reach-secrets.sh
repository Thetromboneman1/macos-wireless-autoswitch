#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

usage() {
  cat <<'EOF'
Configure credential-backed Agent Reach channels from 1Password item fields.

No secret values are stored by this script. Put the values in vault "Boneman",
then run only the channels you want:

  configure-agent-reach-secrets.sh groq
  configure-agent-reach-secrets.sh twitter
  configure-agent-reach-secrets.sh xhs

Expected 1Password items and fields:

  Agent Reach Groq
    credential: API key

  Agent Reach Twitter
    auth_token: Twitter auth_token cookie value
    ct0: Twitter ct0 cookie value

  Agent Reach XHS
    cookies: Cookie-Editor JSON array or header string

Xueqiu currently uses Agent Reach browser import:

  agent-reach configure --from-browser chrome

Run that manually while logged in to xueqiu.com; macOS may prompt for Keychain.
EOF
}

read_op_field() {
  local item="$1"
  local field="$2"
  op read "op://Boneman/${item}/${field}"
}

case "${1:-}" in
  groq)
    key="$(read_op_field 'Agent Reach Groq' 'credential')"
    agent-reach configure groq-key "$key"
    ;;
  twitter)
    auth_token="$(read_op_field 'Agent Reach Twitter' 'auth_token')"
    ct0="$(read_op_field 'Agent Reach Twitter' 'ct0')"
    agent-reach configure twitter-cookies "$auth_token" "$ct0"
    ;;
  xhs)
    cookies="$(read_op_field 'Agent Reach XHS' 'cookies')"
    agent-reach configure xhs-cookies "$cookies"
    ;;
  -h|--help|help|"")
    usage
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
