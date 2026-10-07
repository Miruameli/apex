# 47 — System: Build & Sync Detail

Dokumen ini membahas detail mekanisme build dan sync bridge. Rantai perintah
yang lengkap ada di [`29-build-release.md`](29-build-release.md); prosedur
operasional ada di [`../../operations/runbook/bridge-sync.md`](../../operations/runbook/bridge-sync.md).

## Full build pipeline

`scripts/build.sh` adalah skrip yang berjalan. Setiap perintah `cargo` memakai
`uv run` agar `VIRTUAL_ENV` terkunci pada interpreter proyek.

```sh
#!/usr/bin/env bash
set -euo pipefail

uv run cargo build --workspace
uv run python scripts/sync_apex_py.py
uv run python -c "import apex; print(apex.core_hello())"
```

Mode release:

```sh
./scripts/build.sh --release
```

## Kenapa `uv run` wajib

pyo3 mencari interpreter dengan urutan: `PYO3_PYTHON`, lalu `VIRTUAL_ENV`, lalu
`python`/`python3` dari `PATH`. `cargo build` polos tidak mengekspor
`VIRTUAL_ENV`. Bila `PATH` memuat Python yang lebih baru, pyo3 mengaktifkan cfg
versi yang lebih tinggi, `Py_TYPE` berubah dari helper inline menjadi simbol
extern, dan cdylib gagal saat import dengan `undefined symbol: Py_TYPE`.

Verifikasi config pyo3 setelah build:

```sh
uv run python -c "import sys; print(sys.version_info[:2])"   # (3, 12)
```

## Sync script detail

Nama file tujuan harus memakai suffix dari interpreter yang berjalan. Tag yang
dirakit manual tidak bisa di-import.

```python
# scripts/sync_apex_py.py (inti logika)
import argparse, pathlib, shutil, sysconfig

LIBRARY_SUFFIXES = (".so", ".dylib", ".dll")
MODULE_NAME = "apex_py"

mode = "release" if args.release else "debug"
directory = pathlib.Path("target") / mode

for suffix in LIBRARY_SUFFIXES:
    candidate = directory / f"lib{MODULE_NAME}{suffix}"
    if candidate.exists():
        library = candidate
        break
else:
    raise SystemExit(f"error: no built library in {directory}; run cargo build -p apex-py")

extension_suffix = sysconfig.get_config_var("EXT_SUFFIX")
destination = pathlib.Path(sysconfig.get_paths()["purelib"]) / f"{MODULE_NAME}{extension_suffix}"

shutil.copy2(library, destination)
print(f"synced: {library} → {destination}")
```

Script gagal keras saat artifact tidak ditemukan. Melewatkan copy akan
menyembunyikan build yang rusak di balik fallback yang lebih lambat.

## Verify script

`scripts/verify.sh` menjalankan sebelas gate berurutan dan mencetak `VERIFY OK`
hanya bila semuanya hijau:

```sh
build workspace → sync bridge → import bridge → cargo test → pytest →
ruff check → ruff format --check → cargo fmt --check → clippy →
link Markdown → modularisasi
```

Gate Deno (`deno lint`, `deno fmt --check`, `deno test`) terpisah karena butuh
Deno terpasang; CI menjalankannya lewat `denoland/setup-deno@v2`.

## Task Deno

`deno.json` pada `tui/` hanya berisi task TUI. Rantai `check` seluruh repo
berada di `scripts/verify.sh` agar tidak terduplikasi di dua tempat.
