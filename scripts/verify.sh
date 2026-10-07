#!/usr/bin/env bash
# Verify a clean checkout: build, bridge, tests, lint, format, docs, SAST.
#
# Every step is chained with `&&`, so the first failure stops the run and the
# exit code is trustworthy. Never pipe a gate and inspect `$?` afterwards —
# that hides the real failure behind a pipe.
#
# Usage:
#   ./scripts/verify.sh

set -euo pipefail

readonly STEP_WIDTH=44

run_step() {
  local label="$1"
  shift
  printf '→ %-*s' "$STEP_WIDTH" "$label"
  if "$@" >/tmp/apex-verify.log 2>&1; then
    printf 'ok\n'
  else
    printf 'FAILED\n\n'
    cat /tmp/apex-verify.log
    printf '\nFix the failing step, then re-run ./scripts/verify.sh\n'
    exit 1
  fi
}

printf 'Apex verification\n\n'

run_step 'build workspace'      uv run cargo build --workspace
run_step 'sync PyO3 bridge'     uv run python scripts/sync_apex_py.py
run_step 'import bridge'        uv run python -c 'import apex; print(apex.core_hello())'
run_step 'rust tests'           uv run cargo test --workspace
run_step 'deno lint'            deno lint tui/src
run_step 'deno fmt'             deno fmt --check tui/src
run_step 'deno check'           deno check tui/src/main.ts
run_step 'ts tests'             deno test --allow-all tui/src
run_step 'python tests'         uv run pytest -q
run_step 'ruff lint'            uv run ruff check .
run_step 'ruff format'          uv run ruff format --check .
run_step 'rustfmt'              uv run cargo fmt --all -- --check
run_step 'clippy'               uv run cargo clippy --workspace --all-targets -- -D warnings
run_step 'versions consistent'  uv run python scripts/checks/check_versions.py
run_step 'markdown links'       uv run python scripts/checks/check_docs_links.py
run_step 'modularization'       uv run python scripts/checks/check_modularization.py
run_step 'semgrep (SAST)'       uvx semgrep --config p/default --quiet --error \
  --exclude-rule eqeqeq .

printf '\nVERIFY OK\n'
