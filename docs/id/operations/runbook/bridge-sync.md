# Runbook: PyO3 Bridge Sync

Use this when `import apex_py` fails, or after any change to the `apex-py` or
`apex-core` crate.

## Objective

Make the compiled Rust extension importable from the active virtual environment
with no silent fallback.

## How it works

1. `cargo build -p apex-py` produces `target/<mode>/libapex_py.<ext>`.
2. `scripts/sync_apex_py.py` copies that artifact into the site-packages
   directory of the active interpreter, using the correct platform tag.
3. `import apex_py` then resolves the extension module.

## Prerequisites

- [ ] Rust toolchain installed
- [ ] Virtual environment active (`uv run` guarantees this)

## Steps

### Debug build (normal development)

```sh
cargo build -p apex-py
uv run python scripts/sync_apex_py.py
uv run python -c "import apex_py; print(apex_py.core_hello())"
```

### Release build

```sh
cargo build -p apex-py --release
uv run python scripts/sync_apex_py.py --release
```

## Diagnostics

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: apex_py` | Never synced, or synced into another venv | Run the sync script with `uv run` so it targets the active venv |
| `ImportError: ... undefined symbol` | Stale artifact after a dependency change | Rebuild, then sync again |
| Sync reports `source artifact not found` | `cargo build -p apex-py` has not run, or ran in release mode while syncing debug | Build in the matching mode |
| Works in the shell, fails in CI | CI has not run the sync step | Add the build and sync steps before the import check |

## Fallback policy

There is **no** silent fallback. If the extension is missing, `apex/bridge.py`
raises with the exact command that fixes it. A silent fallback would hide a
broken build behind a slower pure-Python path, which is exactly the drift the
project rules forbid.

## Rollback plan

```sh
rm -f "$(uv run python -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')"/apex_py*
```

## Last Updated: 2026-10-07
