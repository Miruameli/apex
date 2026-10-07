# 04 — Tech Stack (detail)

## Prinsip pembagian

| Lapisan | Tech | Kenapa | Bukan tugasnya |
|---|---|---|---|
| Otak (brain) | Python 3.12+ via `uv` | Ekosistem LLM Python paling lengkap (OpenAI/Anthropic/Ollama client) | Jangan taruh loop IO-heavy / file scan besar di Python |
| Speed core | Rust `edition 2024`, `resolver = "3"` | Scan/index/protocol/session cepat, type-safe, plugin host | Jangan taruh LLM call di Rust |
| UI | TypeScript no-build (Deno / Node 24 type-stripping / Bun) | TUI interaktif, hot-reload, IPC JSONL mudah | Jangan taruh logic agent berat di TS |
| Bridge | PyO3 `0.25` (modern Bound API) | `import apex_py` dari Python, akselerasi Rust | Jangan taruh semua logic di bridge — bridge = facade |
| IPC | JSONL over stdio | 3 bahasa bisa bicara sama tanpa gRPC/proto | Jangan stdoutcampur banner/human-readable |

## Versi & pin

| Tool | Versi | Alasan |
|---|---|---|
| Python | `3.12` (`.python-version`) | Pin(version) eksplisit; interpreter di-resolve pyo3 dari PATH bisa salah |
| Rust | `edition 2024`, `resolver = "3"` | Fitur modern, lint ketat |
| PyO3 | `0.25.x` (pin di `Cargo.lock`) | Modern `Bound` API; cdylib `apex_py` |
| TS runtime | Deno (prefer) / Node 24 type-stripping | No-build, langsung jalan. CI memakai `denoland/setup-deno@v2` |
| uv | `managed = true` | Lockfile di-commit (aplikasi, bukan library) |
| Cargo | workspace `resolver 3` | Multi-crate monorepo rapi |

## Komposisi repo (rencana)

```
apex/
├── crates/                 # Rust workspace
│   ├── apex-core/          # context, protocol, session, plugin host
│   ├── apex-cli/           # binary `apex` (clap)
│   └── apex-py/            # PyO3 cdylib → `import apex_py`
├── apex/                   # Python package
│   ├── agent/              # ApexAgent, serve_stdio, prompts
│   ├── tools/              # fs, shell, lsp, git, registry tunggal
│   ├── bridge.py           # facade ke Rust, error jelas tanpa fallback senyap
│   ├── protocol.py         # mirror dari protocol.rs
│   └── memory/             # APEX.md reader
├── tui/                    # TS no-build
│   ├── src/                # main, ui, ipc, protocol
│   └── deno.json / package.json
├── tests/fixtures/protocol/# JSON fixtures — satu sumber kebenaran
├── scripts/                # sync_apex_py.py, build.sh, verify.sh, gate checker
├── docs/                   # blueprint ini
└── APEX.md / apex.json     # user config
```

## Bridge jujur

- `apex/bridge.py` TIDAK diam-diam fallback. Jika `import apex_py` gagal → `ApexBridgeError` berisi perintah perbaikan.
- `scripts/sync_apex_py.py` copy `target/<mode>/libapex_py.so` ke platlib `.venv` dengan suffix `EXT_SUFFIX` dari interpreter aktif (gunakan `shutil.copy2`, bukan `cp` — menghindari issue filesystem). Tidak ada copy ke root yang shadow site-packages.
- Build WAJIB via `uv run cargo build` agar `VIRTUAL_ENV` mengunci interpreter. Tanpa itu, build script pyo3 bisa mengambil Python lain dari `PATH` dan menghasilkan cdylib dengan simbol `Py_TYPE` undefined yang gagal saat import.
- Gate lengkap: `./scripts/verify.sh` — chain `&&`, bukan pipe + `$?` (hindari masalah pipefail).
