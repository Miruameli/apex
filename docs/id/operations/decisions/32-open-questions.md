# 32 — Open Questions & Decisions Needed

Format: `[OPEN]` = belum diputuskan. Isi `[DECIDED]` = sudah final.
Status `[DECIDED]` selalu diikuti path repo yang membuktikannya; keputusan final dicatat di `31-decisions.md`.

## Produk

| # | Pertanyaan | Status | Pilihan |
|---|---|---|---|
| Q1 | Nama command CLI pasti? | `[DECIDED]` | Standar Apex — `docs/operations/blueprint/49-cli-final.md` menetapkan `apex chat`, `apex review`, `apex commit`, `apex ship`, `apex skill`; `apex` tanpa argumen = TUI. Sudah dikode di `crates/apex-cli/src/main.rs` (clap: chat, review, context) |
| Q2 | TUI library? | `[DECIDED]` | OpenTUI (`@opentui/core`, `@opentui/react`, `@opentui/solid`) — native Zig core + Yoga/Flexbox layout, split panels built-in, lazygit-style reference app (opentui-git), Deno 2.x TS bindings via JSR, in-memory testing, powers OpenCode in production. ADR-0008 |
| Q3 | Bahasa default UI? | `[DECIDED]` | English — `apex.json` → `ui.language: "en"` (runtime override lewat flag `--lang`). `docs/` tetap bahasa Indonesia, UI dan kode English. Catatan: `docs/engineering/quality/30-i18n.md` masih menulis TBD, perlu disinkron |
| Q4 | Bahasa dokumentasi? | `[DECIDED]` | 5 bahasa: English (`docs/en/`), Indonesian (`docs/id/`), Chinese (`docs/zh/`), Japanese (`docs/ja/`), Korean (`docs/ko/`) — struktur mirror tree lengkap siap; terjemahan iteratif mulai V1 |
| Q5 | Marketplace plugin? | `[DECIDED]` | V2 — marketplace adalah infrastructure platform (registry hosting, trust model, security scanning, discovery API), bukan feature. `docs/engineering/subsystems/extensibility/39-system-marketplace.md` sudah V2. Solo OSS dev tidak bisa kredibel operasikan marketplace di V1. V2 selaras dengan Docker sandbox default + multi-agent orchestrator. ADR-0009 |
| Q6 | Tema/branding custom? | `[DECIDED]` | UI theme only (dark/light/user palette via `apex.json` → `ui.theme`). Product branding (logo, colors, name "Apex") fixed — not customizable. Brand consistency > customization untuk solo OSS dev tool. UI theming = palette swap (ANSI/CSS), bukan component override. ADR-0010 |
| Q7 | Review rules override? | `[DECIDED]` | V1 — `docs/community/setup/08-customization.md`: bisa di-override per proyek via `apex.json` → `review_rules` (V1) |
| Q8 | Cost tracker & budget limit? | `[DECIDED]` | V1 — `docs/product/03-feature-matrix.md` (cost tracker butuh token usage instrumentation) + `docs/community/practice/09-security-key-custody.md` (budget limit V1) |

## Teknis

| # | Pertanyaan | Status | Pilihan |
|---|---|---|---|
| Q9 | Runtime TS final? | `[DECIDED]` | Deno — `tui/deno.json` (tasks `deno run`, `deno test`, `deno check`), `tui/src/protocol_test.ts` mengimpor `jsr:@std/assert`, dan `.github/workflows/quality.yml` memasang `denoland/setup-deno@v2` (Deno v2.x). Catatan jujur: Deno belum terpasang di workstation ini, jadi `deno test` lokal belum bisa jalan; CI yang memasangnya |
| Q10 | Vector DB masuk MVP? | `[DECIDED]` | Tidak di MVP, baru V1+ — `docs/engineering/stack/05-architecture.md` dan `docs/engineering/subsystems/core/23-system-memory.md` |
| Q11 | GitHub MCP nyata kapan? | `[DECIDED]` | V1 — `docs/product/03-feature-matrix.md`: MVP memakai PR mock lokal, GitHub connector nyusul; fase 4 (V1) di `docs/operations/blueprint/48-master-blueprint.md` memuat MCP nyata |
| Q12 | Auto-fix error apaan? | `[DECIDED]` | V1 — `docs/product/03-feature-matrix.md` (perlu LSP stabil + LLM function calling) + fase 4 di `docs/operations/blueprint/48-master-blueprint.md` |
| Q13 | Sandbox Docker wajib MVP? | `[DECIDED]` | Tidak wajib — MVP memakai subprocess isolation: `docs/engineering/subsystems/core/24-system-security.md` (level 1 = MVP, level 3 Docker = V1) dan `docs/product/03-feature-matrix.md` (Docker default = V2) |
| Q14 | CI pipeline kapan? | `[DECIDED]` | Fase 1 — `.github/workflows/quality.yml` jalan di push dan PR ke `main`, gate: lint/format (ruff check, ruff format, cargo fmt, clippy `-D warnings`, deno lint, deno fmt), docs (`scripts/checks/check_docs_links.py`, `scripts/checks/check_modularization.py`), test tiga bahasa (cargo test, pytest, deno test), security (gitleaks, cargo audit, pip-audit) |

## Bisnis & operasional

| # | Pertanyaan | Status | Pilihan |
|---|---|---|---|
| Q15 | Model bisnis? | `[DECIDED]` | GitHub Sponsors + Open Collective (V1-V2). Commercial dual-license evaluation di V2+ jika enterprise demand terbukti. MIT license tetap. ADR-0011 |
| Q16 | Target skala 100 users di mana? | `[DECIDED]` | Primary: GitHub (permanent discovery via stars/topics/SEO), Hacker News (launch validation via Show HN), Twitter/X (ongoing community). Secondary: Reddit cross-post only (r/rust, r/neovim, r/programmingtools). ADR-0012 |
| Q17 | Docs hosting? | `[DECIDED]` | GitHub Pages (V1) — `docs/engineering/build-release/29-build-release.md` |
| Q18 | Release channel? | `[DECIDED]` | Stable only untuk sekarang — `docs/operations/governance/13-release.md`: stable = tag `vX.Y.Z`; nightly (build `main`) dan beta (`vX.Y.Z-beta.N`) baru V1 |

## Aturan

- Setiap keputusan baru: tulis di `docs/operations/decisions/31-decisions.md` + update docs terkait.
- Deadline keputusan: sebelum setup kode fase 1.
- Jika ambiguity tinggi + blast radius besar: buat ADR di `docs/operations/adr/`.
