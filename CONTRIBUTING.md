# Contributing to Apex

Terima kasih ingin berkontribusi! Dokumen ini adalah ringkasan; panduan lengkap ada di [`docs/id/community/practice/10-contributing.md`](docs/id/community/practice/10-contributing.md) dan setup di [`docs/id/community/setup/50-dev-setup.md`](docs/id/community/setup/50-dev-setup.md).

## Prasyarat

- **Rust**: stable, edition 2024, resolver 3 (`rustup default stable`)
- **Python**: 3.12 via [`uv`](https://github.com/astral-sh/uv) (`uv python install 3.12`)
- **Deno**: 2.x untuk TUI (`curl -fsSL https://deno.land/install.sh | sh`)

## Quick Setup

```bash
git clone https://github.com/apex-org/apex
cd apex
uv sync
uv run cargo build --workspace
uv run python scripts/sync_apex_py.py
uv run python -c "import apex; print(apex.core_hello())"
```

Output `hello from apex-core` = bridge OK.

## Standar Kode

| Bahasa | Formatter | Linter | Test |
|--------|-----------|--------|------|
| Rust | `uv run cargo fmt --all` | `uv run cargo clippy --workspace --all-targets -- -D warnings` | `uv run cargo test --workspace` |
| Python | `uv run ruff format .` | `uv run ruff check .` | `uv run pytest -q` |
| TypeScript | `deno fmt --check tui/src` | `deno lint tui/src` | `deno test --allow-all tui/src` |

## Aturan Modularisasi

`scripts/checks/check_modularization.py` enforce:

| Aturan | Batas |
|--------|-------|
| File langsung per folder | 5 |
| Subfolder langsung per folder | 5 |
| SLOC per file (`.rs`, `.py`, `.ts`) | 150 |

Satu file = satu tanggung jawab. Satu folder = satu domain. Gate gagal = bagi file/folder.

## Konvensi Commit

**Conventional Commits** wajib:

```text
<type>(<scope>): <subject>
```

| Type | Scope (contoh) |
|------|----------------|
| `feat` | `core`, `agent`, `cli`, `py`, `tui`, `skill`, `mcp`, `docs`, `build`, `test` |
| `fix` | sama di atas |
| `docs` | `docs`, `readme`, `changelog` |
| `refactor` | `core`, `agent`, `cli`, `py`, `tui` |
| `test` | `core`, `agent`, `cli`, `py`, `tui` |
| `build` | `ci`, `cargo`, `uv`, `deno` |
| `chore` | `deps`, `cleanup`, `config` |

Subject ≤72 karakter, imperatif, tanpa titik akhir.

## Kontrak Protocol

1. Ubah `tests/fixtures/protocol/` **lebih dulu** (sumber kebenaran).
2. Update mirror: `protocol.rs`, `protocol.py`, `protocol.ts`.
3. Jalankan test ketiga bahasa (deep-equal pada JSON parsed, bukan raw string).
4. PR dengan fixture drift = ditolak.

## Sebelum Buka PR

```bash
./scripts/verify.sh
deno lint tui/src
deno fmt --check tui/src
deno test --allow-all tui/src
```

**Checklist wajib:**

- [ ] `./scripts/verify.sh` hijau (build, bridge, test, lint, format, gate docs)
- [ ] Test ketiga bahasa hijau
- [ ] Gate `check_docs_links.py` dan `check_modularization.py` hijau
- [ ] Tidak ada `console.log`/debug leftover di stdout
- [ ] Dokumentasi di-update bila perilaku berubah
- [ ] Tidak ada rahasia di commit (`.env`, key) — lihat [Security Key Custody](docs/id/community/practice/09-security-key-custody.md)

## Ukuran PR

- Satu fitur atau satu fix per PR.
- Branch dari `main`: `feat/`, `fix/`, `docs/`, `refactor/`.
- Perubahan logika wajib disertai test.
- Isi template `.github/PULL_REQUEST_TEMPLATE.md`.

## Open untuk Kontributor

Apex terbuka untuk semua. Tidak ada gatekeeper khusus. PR ditolak **hanya** bila checklist di atas tidak terpenuhi.

## Code of Conduct

Wajib dibaca: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — berbasis [Contributor Covenant](https://www.contributor-covenant.org/).

## Security

Lapor kerentanan ke [SECURITY.md](SECURITY.md) — **jangan** buka issue publik.