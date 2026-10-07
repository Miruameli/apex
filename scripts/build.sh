#!/usr/bin/env bash
# Build the Rust workspace, sync the PyO3 bridge, and prove it imports.
#
# Every `cargo` call is prefixed with `uv run` so the PyO3 build script resolves
# the interpreter from $VIRTUAL_ENV instead of PATH. A bare `cargo build` can
# pick up a different Python on PATH, producing a cdylib with an undefined
# `Py_TYPE` symbol. See docs/operations/adr/0004-pyo3-bound-bridge.md.
#
# Usage:
#   ./scripts/build.sh [--release]

set -euo pipefail

RELEASE=""
if [[ "${1:-}" == "--release" ]]; then
    RELEASE="release"
fi

mode="${RELEASE:-debug}"

if [[ -n "$RELEASE" ]]; then
    uv run cargo build -p apex-py --release
else
    uv run cargo build --workspace
fi

uv run python scripts/sync_apex_py.py "$*"
uv run python -c "import apex; print(apex.core_hello())"
