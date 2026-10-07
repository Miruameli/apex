# 52 — Panduan Test (kontributor)

Dokumen ini menjelaskan test yang benar-benar ada di repo dan cara menjalankannya.
Rantai lengkap ada di `./scripts/verify.sh`.

## Level test

| Level | Tool | Lokasi | Status |
|---|---|---|---|
| Unit (Rust) | `cargo test` | `crates/*/tests/*.rs`, `crates/*/src/*.rs` | Aktif |
| Unit (Python) | `pytest` | `tests/python/` | Aktif |
| Unit (TS) | `deno test` | `tui/src/*_test.ts` | Aktif |
| Contract | `cargo test` + `pytest` + `deno test` | `tests/fixtures/protocol/` | Aktif |
| Integration | `pytest` | `tests/integration/` | Belum ada |
| E2E | `pytest` subprocess | `tests/e2e/` | Belum ada |

Folder yang belum ada sengaja tidak dicantumkan sebagai command yang bisa
dijalankan. Tambahkan saat implementasinya benar-benar ada.

## Menjalankan test

```sh
# Semua (Rust + Python + TypeScript)
./scripts/verify.sh

# Per bahasa
uv run cargo test --workspace
uv run pytest -q
cd tui && deno test --allow-all src/

# Contract test saja
uv run cargo test -p apex-core protocol
uv run pytest -q tests/python/test_protocol.py
cd tui && deno test src/protocol_test.ts
```

## Struktur test saat ini

```
tests/
├── fixtures/protocol/        # sumber kebenaran kontrak
│   ├── requests/             # chat, fix, review, context
│   └── events/
│       ├── stream/           # thinking, toolcall, diff, message
│       └── terminal/         # done, error
└── python/                   # test pytest: protocol + bridge
```

## Menulis test baru

### Unit test Python

```python
# tests/python/test_protocol.py
import json
import pathlib

FIXTURES = pathlib.Path("tests/fixtures/protocol")


def test_chat_request_roundtrip():
    """Fixture deserialize lalu serialize lagi harus identik secara makna."""
    raw = (FIXTURES / "requests/chat_request.json").read_text()
    parsed = json.loads(raw)
    assert parsed["type"] == "Chat"
    assert "message" in parsed
```

### Contract test

Contract test membandingkan JSON yang sudah di-parse dengan key terurut, bukan
raw string. Raw string rapuh terhadap urutan key dan whitespace.

```python
# tests/python/test_protocol.py
import json
import pathlib

FIXTURES = pathlib.Path("tests/fixtures/protocol")


def test_all_fixtures_are_valid_json():
    """Semua fixture harus bisa di-parse."""
    for fixture in FIXTURES.rglob("*.json"):
        json.loads(fixture.read_text())
```

### Unit test Rust

```rust
// crates/apex-core/tests/core_test.rs
#[test]
fn version_matches_the_manifest() {
    assert_eq!(apex_core::VERSION, env!("CARGO_PKG_VERSION"));
}
```

## Test isolation

- Pakai `tmp_path` fixture pytest untuk setiap test yang menyentuh filesystem
- Test tidak boleh menyentuh `.apex/` global
- Panggilan LLM dimock atau diarahkan ke Ollama lokal (`localhost:11434`)
- Tidak ada jaringan di unit dan integration test
- Test tidak boleh bergantung pada urutan eksekusi

## Test fixtures

Lokasi: `tests/fixtures/protocol/**/*.json`

Setiap fixture wajib:

1. Valid JSON
2. Dapat di-deserialize oleh Rust, Python, dan TypeScript
3. Re-serialize lalu parse lagi menghasilkan deep-equal dengan key terurut

## CI

Workflow: `.github/workflows/quality.yml`

| Job | Isi |
|---|---|
| `lint` | `ruff check`, `ruff format --check`, `cargo fmt --check`, `clippy -D warnings`, `deno lint`, `deno fmt`, gate link docs, gate modularisasi |
| `test` | `cargo test --workspace`, `pytest -q`, `deno test` |
| `security` | gitleaks, `cargo audit`, `pip-audit`, semgrep (SAST) |

## Coverage

Tiga bahasa diukur dengan tool bawaan masing-masing stack. Perintah ini
menghasilkan angka yang sama di lokal maupun di workstation contributor.

```sh
# Python — pytest-cov, konfigurasi ada di pyproject.toml
uv run pytest -q --cov=apex --cov-branch --cov-report=term-missing

# TypeScript — coverage bawaan Deno, tanpa dependensi tambahan
deno test --allow-all --coverage=/tmp/apex-cov --clean tui/src
deno coverage /tmp/apex-cov

# Rust — LLVM instrumentation
cargo llvm-cov --workspace --summary-only
```

Target coverage:

| Area | Target |
|---|---|
| Kontrak protocol | 100% |
| Business logic | >90% |
| Critical path | 100% |

Baseline yang diukur pada 2026-10-07:

| Area | Angka | Catatan |
|---|---|---|
| `apex` (Python) | 100% statement dan branch | 17 test |
| `tui/src/parse.ts` | 99,0% baris, 97,4% branch | 20 test |
| `apex-core/src/protocol.rs` | 100% | contract test lewat API publik |
| `apex-core/src/lib.rs` | 100% | |
| `apex-py/src/lib.rs` | tidak terukur | Dipanggil dari test Python, bukan `cargo test`, jadi LLVM tidak melihatnya |
| `apex-cli/src/main.rs` | 0% | Stub; belum ada logika untuk diuji |

Dua baris terakhir itu batas pengukuran, bukan regresi. `apex-py` benar-benar
dieksekusi — `test_core_hello_reaches_rust` melewati Python → PyO3 → Rust dan
memerlukan hasilnya persis — tetapi `cargo llvm-cov` hanya melihat test yang
dijalankan Rust. Mengukur lapisan itu dari sisi Python butuh instrumentasi
terpisah; pekerjaan terpisah, bukan tambahan diam-diam.

Angka ini belum jadi gate. Menjadikannya gate butuh baseline yang dikomit dan
ambang penurunan, supaya "turun 5%" punya arti. Kebijakan itu belum diputuskan,
jadi untuk sekarang coverage hanya dilaporkan, belum menjadi syarat lulus.
