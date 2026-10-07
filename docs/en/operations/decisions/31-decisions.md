# 31 — Decision Log

| ID | Keputusan | Alasan | Trade-off | Status |
|---|---|---|---|---|
| D1 | Nama fix: Apex | Simpel, powerful, available | Tidak ada | Final |
| D2 | Target: solo OSS dev | Persona primer tunggal, fokus | Tidak ada persona sekunder | Final |
| D3 | Lisensi: MIT | Gratis total, permissive | Tidak ada | Final |
| D4 | Platform: CLI+TUI only | Tidak ada web/IDE ext overhead | Tidak ada desktop IDE integration | Final |
| D5 | Stack: Py+Rust+TS | Sesuai kebutuhan: Python LLM, Rust speed, TS UI | Beban kompleksitas 3 bahasa | Final |
| D6 | Bridge: PyO3 0.25 + Python 3.12 | Modern, stabil untuk Py 3.12; pin nyata di `crates/apex-py/Cargo.toml` + `Cargo.lock` (pyo3 0.25.1) dan `.python-version` (3.12) | Pin 3.12, tunggu 3.14 | Final |
| D7 | Skills: Rust host + subprocess | Security, isolation, authoring mudah | Tidak bisa Rust cdylib (perf trade-off) | Final |
| D8 | MCP: sebagai skill type | Satu runtime, tidak duplikasi | Tidak ada native MCP runtime | Final |
| D9 | Protocol: JSON fixtures + 3 test | Kontrak jelas, drift terdeteksi | Overhead mantenance fixtures | Final |
| D10 | Key custody: local-only | Security, trust, no proxy | User manage key sendiri | Final |
| D11 | MVP scope: chat+review+skills+TUI | Nilai core, bukti produk | Auto-fix/plan mode nyusul | Final |
| D12 | TUI dulu, CLI menyusul | TUI = pembeda, CLI = standar | Solo dev effort tinggi | Final |
| D13 | Runtime TS: no-build | Simple dev, hot-reload | Tidak bisa pakai lib yang butuh build | Final |
| D14 | PyYAML fixture optional | Mencegah parse error live | Tambahan dev dep | Final |
| D15 | Sync bridge: Python shutil.copy2 | Hindari cp issue | Script Python wajib | Final |
| D16 | Formatter/linter TS: `deno fmt` + `deno lint` | Satu toolchain dengan runtime TUI, nol dependensi npm, satu sumber kebenaran format | Toolchain TUI terikat Deno; tidak kompatibel tooling npm (ADR-0006) | Final |
| D17 | Dokumentasi 5 bahasa | Akses global kontributor; mirror tree `docs/{en,id,zh,ja,ko}/`; terjemahan iteratif V1+ | Upfront effort struktur; maintenance 5x docs | Final |
| D18 | TUI library: OpenTUI | Satu-satunya dengan native split-panel + Flexbox layout; lazygit-style reference; production-proven (OpenCode); Deno 2.x native; in-memory testing | Zig FFI dep; komunitas lebih kecil dari Cliffy | Final |
| D19 | Marketplace plugin: V2 | Platform infrastructure (registry, trust, security, discovery), bukan feature. Solo OSS dev tidak bisa kredibel operasikan di V1. V2 selaras dengan Docker sandbox + multi-agent. ADR-0009 | Hosting commitment tertunda; user tidak bisa `apex skill add <remote>` sampai V2 | Final |
| D20 | Tema/branding: UI theme only | Dark/light/user palette via `ui.theme`. Product branding (logo, colors, name "Apex") fixed. | User tidak bisa rebrand Apex. Enterprise demand → `ui.branding` override V2+ | Final |
| D21 | Model bisnis: Sponsorship + Future Commercial | GitHub Sponsors + Open Collective V1-V2. Commercial dual-license evaluation V2+ jika enterprise demand. MIT tetap. ADR-0011 | Tidak ada income terjamin; komersial bisa alienasi puris. Mitigasi: transparan, additive only. | Final |
| D22 | Target akuisisi: GitHub + HN + Twitter/X | Primary: GitHub (permanent discovery), HN (launch validation), Twitter/X (community). Secondary: Reddit cross-post. ADR-0012 | Algoritma HN/Twitter dependency; no owned channel. Mitigasi: email capture di Sponsors page. | Final |
| D23 | Auto-release via release-please | CI automatically bumps version, changelog, and tag from conventional commits; eliminates manual version editing for small changes | Change goes through a release PR (not fully hands-off); requires consistent conventional commits | Final |