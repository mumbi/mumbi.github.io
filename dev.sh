#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
PORT="${PORT:-1313}"

usage() {
  echo "Usage: $(basename "$0") [OPTIONS]"
  echo ""
  echo "Options:"
  echo "  --no-drafts  draft 포스트 제외"
  echo "  --help       이 도움말 표시"
  echo ""
  echo "Environment:"
  echo "  PORT         서버 포트 (기본: 1313)"
  exit 0
}

DRAFTS="--buildDrafts"
EXTRA_ARGS=()
for arg in "$@"; do
  case "$arg" in
    --help|-h) usage ;;
    --no-drafts) DRAFTS="" ;;
    *) EXTRA_ARGS+=("$arg") ;;
  esac
done

docker run --rm -p "${PORT}:1313" -v "${REPO_ROOT}:/src" \
  hugomods/hugo:exts server --bind 0.0.0.0 $DRAFTS ${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"}
