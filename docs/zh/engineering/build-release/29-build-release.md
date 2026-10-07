# 29 — Build & Release Pipeline

## Build steps

```sh
# 1. Build workspace + bridge, sync, dan verifikasi dalam satu perintah
./scripts/build.sh

# 2. Gate lengkap: build, test, lint, link docs, modularisasi
./scripts/verify.sh
```

Langkah manual bila perlu debugging:

```sh
# Build Rust
uv run cargo build --workspace

# Build PyO3 bridge
uv run cargo build -p apex-py

# Sync bridge ke Python venv
uv run python scripts/sync_apex_py.py

# Verify import
uv run python -c "import apex; print(apex.core_hello())"

# Test tiga bahasa
uv run cargo test --workspace
uv run pytest -q
cd tui && deno test --allow-all src/
```

Wajib `uv run` untuk setiap perintah `cargo`: pyo3 me-resolve interpreter dari
`PATH` tanpa `VIRTUAL_ENV`, dan cdylib yang dibangun dengan interpreter salah
gagal saat import dengan `undefined symbol: Py_TYPE`.

## Rantai `check` yang jujur

`./scripts/verify.sh` memakai `set -euo pipefail`, sehingga kegagalan di langkah
mana pun menghentikan seluruh rantai dan exit code tetap dapat dipercaya.

```sh
#!/usr/bin/env bash
set -euo pipefail  # bukan -x: log gadiah, exit code tetap jujur

uv run cargo build --workspace
uv run python scripts/sync_apex_py.py
uv run python -c "import apex; print(apex.core_hello())"
uv run cargo test --workspace
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
uv run cargo fmt --all -- --check
uv run cargo clippy --workspace --all-targets -- -D warnings
uv run python scripts/checks/check_docs_links.py
uv run python scripts/checks/check_modularization.py
```

Bukan: `cargo check | uv run python` lalu memeriksa `$?` — nilai itu berasal dari
pipe pertama, bukan dari proses yang gagal.

## Release artifacts

| Artifact | Path | Distributable |
|---|---|---|
| `apex` binary (CLI) | `target/release/apex` | GitHub Releases |
| `apex_py` cdylib | `target/release/libapex_py.so` | Disalin ke venv saat build |
| Python package | `dist/apex-0.1.0-py3-none-any.whl` | PyPI |
| TUI source | `tui/` | Repo |
| Docs | `docs/` | GitHub Pages (V1) |

## Versioning

- `Cargo.toml` workspace version
- `pyproject.toml` version
- `tui/deno.json` version

Ketiganya harus cocok sebelum tag. Rilis hanya source code tanpa binary,
checksum, dan SBOM bukan rilis; prosedurnya ada di
[`../../operations/runbook/release.md`](../../operations/runbook/release.md).

## CI release

1. Tag `vX.Y.Z`
2. Build semua artifacts per platform
3. Jalankan gate `./scripts/verify.sh`
4. Buat GitHub Release
5. Upload binaries, `sha256`, dan SBOM
6. Update `CHANGELOG.md`
