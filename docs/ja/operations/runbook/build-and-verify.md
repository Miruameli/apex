# Runbook: Build and Verify

Use this when a clean build fails, or when the full test suite is red and the
cause is not obvious.

## Objective

Get from a fresh checkout to a verified state where all three language test
suites pass.

## Prerequisites

- [ ] Rust stable toolchain with `rustfmt` and `clippy`
- [ ] Python 3.12 with `uv`
- [ ] Deno 2.x
- [ ] Working tree clean, or changes stashed

## Steps

### 1. Clean build

```sh
cargo build --workspace
```

A failure here means a manifest or source problem, not an environment problem.

### 2. Sync the PyO3 bridge

The Python package imports a compiled Rust extension. It must be copied into
the active virtual environment after every Rust change.

```sh
uv run python scripts/sync_apex_py.py
uv run python -c "import apex_py; print(apex_py.core_hello())"
```

Expected output: `hello from apex-core`. See
[`bridge-sync.md`](bridge-sync.md) when this fails.

### 3. Run all tests

```sh
uv run pytest -q
cargo test --workspace
cd tui && deno test --allow-all src/
```

### 4. Run lint and format gates

```sh
uv run ruff check .
uv run ruff format --check .
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
deno lint tui/src
deno fmt --check tui/src
uv run python scripts/checks/check_docs_links.py
uv run python scripts/checks/check_modularization.py
```

## Rollback plan

Nothing in this runbook modifies tracked files. To undo a build side effect:

```sh
rm -rf target/
rm -rf .venv/
```

## Escalation

| Symptom | Next step |
|---|---|
| Bridge import fails | [`bridge-sync.md`](bridge-sync.md) |
| Protocol fixtures fail in one language only | Check that language's `protocol` module against `docs/engineering/stack/06-protocol.md` |
| Fixtures fail in all three languages | Fixture file is malformed; run `python -m json.tool` on it |
| Modularization gate fails | Split the file or folder as the message describes |

## Last Updated: 2026-10-07
