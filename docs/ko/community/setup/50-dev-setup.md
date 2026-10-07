# 50 — Panduan Setup Developer

Dokumen ini membawa Anda dari `git clone` sampai `./scripts/verify.sh` hijau.
Semua perintah di bawah dijalankan dari root repo apa adanya.

Aturan kontribusi lengkap: [`../practice/10-contributing.md`](../practice/10-contributing.md).

## Prasyarat

| Tool | Versi | Cek |
|---|---|---|
| Rust | stable (edition 2024, resolver 3) | `cargo --version` |
| Python | 3.12 (dipin `.python-version`) | `uv run python --version` |
| uv | terbaru | `uv --version` |
| Deno | 2.x — wajib untuk TUI dan CI | `deno --version` |
| git | terbaru | `git --version` |

Deno dibutuhkan untuk TUI dan untuk gate CI. Workstation tanpa Deno tetap bisa
build dan test Rust serta Python, tetapi tidak bisa menjalankan `deno lint`,
`deno fmt`, dan `deno test`. Deno yang belum terpasang di sebuah mesin adalah
kekurangan lokal, bukan cacat repo.

## Setup pertama

```sh
git clone <repo-url>
cd apex
uv sync
uv run cargo build --workspace
uv run python scripts/sync_apex_py.py
uv run python -c "import apex; print(apex.core_hello())"
```

Output terakhir harus `hello from apex-core`. Itulah bukti extension Rust sudah
importable dari virtual environment aktif.

## Workflow bridge PyO3

Python memanggil Rust lewat extension module bernama `apex_py`. Tidak ada build
shim pihak ketiga; tiga langkah eksplisit saja:

1. `uv run cargo build -p apex-py` — compile cdylib ke `target/debug/`.
2. `uv run python scripts/sync_apex_py.py` — salin ke site-packages memakai tag
   ekstensi dari interpreter yang berjalan.
3. `uv run python -c "import apex; print(apex.core_hello())"` — buktikan bisa
   di-load.

### Build bridge lewat `uv run`, jangan `cargo` polos

PyO3 mencari interpreter dengan urutan: `PYO3_PYTHON`, lalu `VIRTUAL_ENV`, lalu
`python` atau `python3` dari `PATH`. `cargo build` polos tidak mengekspor
`VIRTUAL_ENV`, sehingga interpreter yang lebih baru di `PATH` — Python 3.14
teramati di workstation kontributor — menang pencarian. Extension lalu dikompilasi
untuk ABI yang tidak dimiliki virtual environment 3.12 dan baru gagal saat
import dengan `undefined symbol: Py_TYPE`.

`uv run cargo build -p apex-py` mengekspor `VIRTUAL_ENV` dan mengikat build ke
interpreter proyek. Pakai `uv run` untuk setiap perintah Rust di repo ini.

## Struktur repo

```
apex/
├── crates/
│   ├── apex-core/     # lib.rs, protocol.rs + test integrasi
│   ├── apex-cli/      # binary `apex`
│   └── apex-py/       # cdylib PyO3 (module `apex_py`)
├── apex/              # package Python: bridge.py, protocol.py
├── tui/               # TS no-build: deno.json, src/main.ts, src/protocol.ts
├── tests/
│   ├── fixtures/protocol/   # sumber kebenaran kontrak protocol
│   └── python/              # test pytest
├── scripts/           # build.sh, verify.sh, sync_apex_py.py, check_*.py
└── docs/              # blueprint: community, engineering, operations, product
```

## Command harian

| Task | Command |
|---|---|
| Build workspace | `uv run cargo build --workspace` |
| Build bridge saja | `uv run cargo build -p apex-py` |
| Sync bridge | `uv run python scripts/sync_apex_py.py` |
| Cek import bridge | `uv run python -c "import apex; print(apex.core_hello())"` |
| Test Rust | `uv run cargo test --workspace` |
| Test Python | `uv run pytest -q` |
| Test TUI (butuh Deno) | `deno test --allow-all tui/src` |
| Lint Python | `uv run ruff check .` |
| Format Python | `uv run ruff format .` |
| Format Rust | `uv run cargo fmt --all` |
| Lint TUI (butuh Deno) | `deno lint tui/src` |
| Gate link Markdown | `uv run python scripts/checks/check_docs_links.py` |
| Gate modularisasi | `uv run python scripts/checks/check_modularization.py` |

## Satu perintah untuk memverifikasi checkout

```sh
./scripts/verify.sh
```

Rantai yang dijalankan, berurutan, dan berhenti di kegagalan pertama:

1. build workspace
2. sync bridge PyO3
3. import bridge
4. `cargo test --workspace`
5. `deno lint tui/src`
6. `deno fmt --check tui/src`
7. `deno check tui/src/main.ts`
8. `deno test --allow-all tui/src`
9. `pytest -q`
10. `ruff check`
11. `ruff format --check`
12. `cargo fmt --check`
13. `clippy -D warnings`
14. link Markdown
15. modularisasi
16. semgrep (SAST)

Perintah persisnya ada di `scripts/verify.sh`; `./scripts/verify.sh` mencetak
`VERIFY OK` hanya bila seluruhnya hijau.

Gate Deno dan semgrep memakai tool yang di-pin: Deno 2.x (lihat ADR-0006) dan
`p/default` ruleset. Semgrep berjalan lewat `uvx`, jadi tidak perlu diinstal
dulu — `uvx` mengunduhnya ke cache pada pemakaian pertama.

## Gate yang wajib lolos

| Gate | Yang diperiksa |
|---|---|
| `scripts/checks/check_docs_links.py` | Semua link relatif Markdown resolve; path absolut ditolak |
| `scripts/checks/check_modularization.py` | Maks 5 file langsung per folder, maks 5 subfolder langsung per folder, maks 150 SLOC per file (`.rs`, `.py`, `.ts`) |

Kegagalan gate menyebut path yang bermasalah. Pecah file atau folder, jangan
melonggarkan batasnya.

## Troubleshooting

| Gejala | Penyebab | Perbaikan |
|---|---|---|
| `ModuleNotFoundError: apex_py` | Belum sync, atau sync ke venv lain | Jalankan ulang `uv run python scripts/sync_apex_py.py` |
| `undefined symbol: Py_TYPE` | Build memakai interpreter dari `PATH` | Build ulang dengan `uv run cargo build -p apex-py`, lalu sync lagi |
| `ApexBridgeError` dari `apex.bridge` | Extension tidak ada atau rusak | Pesan error sudah memuat perintah perbaikannya |
| Gate link Markdown gagal | Link menunjuk file yang tidak ada | Perbaiki target atau hapus referensinya |

Rincian diagnosis bridge: [`../../operations/runbook/bridge-sync.md`](../../operations/runbook/bridge-sync.md).

## Konvensi commit dan branch

Commit message mengikuti Conventional Commits:

```text
<type>(<scope>): <subject>
```

Type: `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `chore`.
Scope mengikuti pohon repo: `core`, `agent`, `cli`, `py`, `tui`, `skill`, `mcp`,
`docs`, `build`, `test`.

Branch: `main` protected, `feat/<name>`, `fix/<name>`, `docs/<name>`,
`refactor/<name>`.
