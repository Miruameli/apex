# 01 — Product Spec

## Visi

**Apex** adalah terminal AI coding agent yang *all in terminal*, *custom sendiri*, dan *lengkap walaupun berat*.

Tagline: `Apex — All in terminal. Custom sendiri.`

## Target spesifik

| Aspek | Nilai |
|---|---|
| Audiens primer | Solo open-source developer |
| Persona sekunder | Tidak ada (fokus penuh di primer) |
| Lisensi | MIT, gratis total, full open source |
| Platform | CLI + TUI, tidak ada web/VS Code extension |
| Skala visi | Saat matang: 5jt+ baris kode — modular sejak hari pertama |

## Positioning

| Produk | Strength | Apex pembeda |
|---|---|---|
| Aider | Ringan, git-first | Apex: all in terminal + review/commit/PR + skills |
| Claude Code | Agentic kuat | Apex: open-source + custom provider first + no key proxy |
| Cursor | IDE terintegrasi | Apex: terminal-first, multi-panel TUI |
| OpenHands | Autonomous sandbox | Apex: human-in-the-loop, approval + undo + diff per hunk |

## Keunggulan

1. **All in terminal** — chat, baca codebase, review, commit, PR, skills dalam satu tempat.
2. **Custom sendiri** — `apex.json` (provider), `APEX.md` (memory), `SKILL.md` (skill), tema.
3. **Lengkap walaupun berat** — cakupan fitur > ringan.
4. **Trust** — key lokal, no proxy, audit bebas.

## MVP scope (dikunci)

1. Chat + context scan (`apex chat`, `apex context`)
2. Review + commit + PR (`apex review`, `apex commit`, `apex ship`)
3. Skills/plugins + MCP (`apex skill add`, connector)
4. Full lazygit-style TUI (split-panel, diff per-hunk)

## Non-goals (MVP)

- Auto-fix error otomatis penuh
- Plan mode autonomous tanpa approval
- Local LLM sebagai default wajib
- Voice, cost tracker detail, kolaborasi real-time
- IDE pengganti

## Status keputusan terbuka `[OPEN]`

- Nama command CLI pasti (standar Apex vs standar Unix)
- TUI framework (Cliffy / OpenTUI / stdlib)
- Dokumentasi bahasa ketiga
- Posisi marketplace plugin (MVP/V1/V2)
- Tema/branding custom: UI-only atau produk juga
