# 10 — Contributing

Aturan singkat untuk membuka pull request. Setup lengkap ada di
[`../setup/50-dev-setup.md`](../setup/50-dev-setup.md).

## Prasyarat

Rust stable (edition 2024, resolver 3), Python 3.12 via `uv`, dan Deno 2.x
untuk TUI. Setup pertama yang bisa langsung dijalankan:

```sh
git clone <repo-url>
cd apex
uv sync
uv run cargo build --workspace
uv run python scripts/sync_apex_py.py
uv run python -c "import apex; print(apex.core_hello())"
```

Dua perintah terakhir membangun extension PyO3 lalu menyalinnya ke virtual
environment. Output `hello from apex-core` berarti bridge hidup.

## Standar kode

| Bahasa | Formatter | Linter | Test |
|---|---|---|---|
| Rust | `uv run cargo fmt --all` | `uv run cargo clippy --workspace --all-targets -- -D warnings` | `uv run cargo test --workspace` |
| Python | `uv run ruff format .` | `uv run ruff check .` | `uv run pytest -q` |
| TypeScript | `deno fmt --check tui/src` | `deno lint tui/src` | `deno test --allow-all tui/src` |

Command TypeScript butuh Deno 2.x terpasang.

## Aturan modularisasi

`scripts/checks/check_modularization.py` menolak perubahan yang melanggar:

| Aturan | Batas |
|---|---|
| File langsung per folder | 5 |
| Subfolder langsung per folder | 5 |
| SLOC per file (`.rs`, `.py`, `.ts`) | 150 |

Satu file satu tanggung jawab, satu folder satu domain. Kalau gate gagal, bagi
file atau folder tersebut.

## Konvensi commit

Conventional Commits untuk setiap commit message:

```text
<type>(<scope>): <subject>
```

Type: `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `chore`.
Scope: `core`, `agent`, `cli`, `py`, `tui`, `skill`, `mcp`, `docs`, `build`,
`test`.

## Kontrak protocol

- Ubah `tests/fixtures/protocol/` lebih dulu; fixture itu satu sumber kebenaran.
- Update mirror di `protocol.rs`, `protocol.py`, dan `protocol.ts`.
- Jalankan test ketiga bahasa; pembandingannya deep-equal atas hasil parse,
  bukan string mentah.
- PR yang fixtures-nya drift ditolak.

## Sebelum membuka PR

```sh
./scripts/verify.sh
deno lint tui/src
deno fmt --check tui/src
deno test --allow-all tui/src
```

Checklist:

- [ ] `./scripts/verify.sh` hijau: build, bridge, test, lint, format, gate docs
- [ ] Test ketiga bahasa hijau
- [ ] Gate `check_docs_links.py` dan `check_modularization.py` hijau
- [ ] Tidak ada `console.log` atau debug leftover di stdout
- [ ] Dokumentasi di-update bila perilaku berubah
- [ ] Tidak ada rahasia di commit (`.env`, key) — lihat
      [`09-security-key-custody.md`](09-security-key-custody.md)

## Ukuran PR

- Satu fitur atau satu fix per PR.
- Branch dari `main`: `feat/`, `fix/`, `docs/`, `refactor/`.
- Perubahan logika selalu disertai test.
- Isi template `.github/PULL_REQUEST_TEMPLATE.md`.

## Open untuk kontributor

Apex terbuka untuk kontributor. Tidak ada gatekeeper khusus; PR ditolak hanya
bila checklist di atas tidak terpenuhi.
