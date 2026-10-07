# 25 — System: PyO3 Bridge

## Tujuan

Expose Rust speed core (`apex-core`) sebagai cdylib Python `apex_py`.

## Flow

1. `uv run cargo build -p apex-py` → `target/debug/libapex_py.so`
2. `uv run python scripts/sync_apex_py.py` → copy ke platlib venv dengan suffix `EXT_SUFFIX`
3. `uv run python -c "import apex; print(apex.core_hello())"` → proven

## Kenapa build wajib lewat `uv run`

Build script pyo3 me-resolve interpreter dari `PATH`. Bila `PATH` memuat Python
lain (misal 3.14), pyo3 mengaktifkan cfg `Py_3_14`, dan `Py_TYPE` berubah dari
helper inline menjadi simbol extern. Hasilnya: cdylib yang gagal di-import dengan
`undefined symbol: Py_TYPE`.

`uv run` menyetel `VIRTUAL_ENV`, sehingga pyo3 memakai interpreter venv (3.12)
dan cfg versi menjadi benar. Verifikasi:

```sh
uv run python -c "import sys; print(sys.version_info[:2])"   # (3, 12)
```

## Sync script

Suffix modul harus dibaca dari interpreter (`sysconfig.get_config_var("EXT_SUFFIX")`),
bukan dirakit manual — tag yang salah tidak bisa di-import.

```python
# scripts/sync_apex_py.py (inti logika)
import shutil, sysconfig, pathlib
src = pathlib.Path("target/debug/libapex_py.so")
suffix = sysconfig.get_config_var("EXT_SUFFIX")
dst = pathlib.Path(sysconfig.get_paths()["purelib"]) / f"apex_py{suffix}"
shutil.copy2(src, dst)
print(f"synced: {src} → {dst}")
```

## Fallback policy

- **Tidak ada silent fallback**. Jika `import apex_py` gagal → error jelas + cara fix.
- Di `apex/bridge.py`: wrap import, jika gagal raise `ApexBridgeError` dengan message cara fix (`cargo build -p apex-py && python scripts/sync_apex_py.py`).

## PyO3 version

- Pin `0.25.x` (modern `Bound` API), terkunci di `Cargo.lock`
- Python dipin `3.12` lewat `.python-version` agar konfigurasi pyo3 deterministik
- `Cargo.toml`: `pyo3 = { version = "0.25", features = ["extension-module"] }`

## Exposed API

```python
import apex
apex.core_hello()             # → "hello from apex-core"
apex.bridge.core_version()    # → "0.1.0"
```

Planner: `scan_context`, `run_skill` belum ada — ditambahkan saat core-nya diimplementasikan.

## Cargo.toml snippet

```toml
[package]
name = "apex-py"
version = "0.1.0"
edition = "2024"

[lib]
name = "apex_py"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.25", features = ["extension-module"] }
apex-core = { path = "../apex-core" }
```
