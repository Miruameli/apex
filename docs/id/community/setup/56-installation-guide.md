# 56 — Installation Guide (user)

> Status: belum ada rilis. Rilis pertama dengan tag `v0.1.0` belum dipublikasikan,
> jadi metode di bawah ini menjelaskan apa yang akan tersedia, bukan apa yang sudah
> ada. Untuk pengembangan lokal, lihat [`50-dev-setup.md`](50-dev-setup.md).

## Prasyarat

| Tool | Versi | Install |
|---|---|---|
| Python | 3.12 | `uv python install 3.12` |
| uv | terbaru | Lihat https://docs.astral.sh/uv/getting-started/installation/ |
| Deno (untuk TUI) | 2.x | Lihat https://docs.deno.com/runtime/getting_started/installation/ |

## Dari source (satu-satunya jalur yang berfungsi saat ini)

```sh
git clone https://github.com/apex/apex && cd apex
uv sync
./scripts/build.sh
./scripts/verify.sh
```

`./scripts/build.sh` membangun workspace Rust, menyalin bridge PyO3 ke virtual
environment, lalu memverifikasi `import apex`. `./scripts/verify.sh` menjalankan
sebelas gate: build, test tiga bahasa, lint, format, link docs, dan modularisasi.

Build wajib memakai `uv run cargo build` agar interpreter PyO3 terkunci pada
virtual environment proyek. Tanpa itu, pyo3 dapat mengambil Python lain dari
`PATH` dan menghasilkan cdylib yang gagal di-import dengan
`undefined symbol: Py_TYPE`.

## Build release dari source

```sh
uv run cargo build --workspace --release
uv run python scripts/sync_apex_py.py --release
uv run python -c "import apex; print(apex.core_hello())"
```

## Metode yang direncanakan

Metode berikut belum ada dan sengaja tidak ditulis sebagai command yang bisa
dijalankan:

| Metode | Isi | Status |
|---|---|---|
| Wheel Python | package Python + bridge | Direncanakan |
| Binary tunggal | `apex` beserta TUI | Direncanakan |
| Homebrew | `apex` binary | V1 |
| Rilis nightly | build dari `main` | V1 |

Rilis hanya dianggap sah bila disertai binary per platform, berkas `sha256`, dan
SBOM. Prosedurnya ada di
[`../../operations/runbook/release.md`](../../operations/runbook/release.md).

## Verifikasi setelah build

```sh
uv run python -c "import apex; print(apex.core_hello())"
# hello from apex-core
```

Perintah `apex --version` dan `apex chat` belum berfungsi: binary CLI masih
kerangka tanpa subcommand.

## Uninstall

```sh
uv run pip uninstall apex          # package Python
rm -rf .apex                        # runtime state lokal
```

Bridge di virtual environment dihapus dengan:

```sh
uv run python -c "import sysconfig, pathlib; p = pathlib.Path(sysconfig.get_paths()['purelib']); [f.unlink() for f in p.glob('apex_py*')]"
```
