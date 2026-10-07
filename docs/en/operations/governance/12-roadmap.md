# 12 — Roadmap

## Fase 0 — Blueprint (done)

- [x] Reset workspace
- [x] Product spec
- [x] Tech stack
- [x] Architecture
- [x] Protocol
- [x] Skills & MCP
- [x] Customization
- [x] Security
- [x] Contributing
- [x] CoC
- [x] TUI library decision — OpenTUI (D18)
- [x] Nama command CLI — `apex` (D1/D1'Q1)
- [x] Dokumentasi bahasa ketiga — 5-bahasa mirror tree (D17)
- [x] CI pipeline — `.github/workflows/quality.yml` (D'Q14)

## Fase 0.5 — Release Automation (new)

- [x] Auto-release via `release-please` (`.github/workflows/release-please.yml`)
- [x] Workspace version inheritance (`version.workspace = true`)
- [x] `scripts/checks/check_versions.py` consistency gate
- [x] `Cargo.lock` tracked for reproducible builds
- [x] Version check added to `quality.yml` + `verify.sh`

## Fase 1 — Foundation (MVP core)

- [x] Rust workspace: `apex-core` (hello, version, protocol)
- [ ] Rust `apex-core` context scan (Phase 1 remaining)
- [ ] Python: `ApexAgent.handle` untuk Chat/Context (Phase 1 remaining)
- [x] Bridge: `import apex_py` proven, no silent fallback
- [x] Protocol fixtures + test 3 bahasa
- [x] `check` script jujur (build → sync → import → test)
- [x] Release automation (auto-version + auto-tag + artifact workflow)

## Fase 2 — MVP fitur

- [ ] `apex chat` streaming
- [ ] `apex context` real scan
- [ ] `apex review` diff + safety
- [ ] `apex commit` atomic message
- [ ] `apex ship` PR mock lokal
- [ ] `apex skill add/run` subprocess

## Fase 3 — TUI full

- [ ] Split-panel: files | chat | diff | terminal
- [ ] Diff pipeline per-hunk accept/reject
- [ ] Keybindings keyboard-first
- [ ] Undo/rollback terintegrasi

## Fase 4 — V1

- [ ] Auto-fix error (LSP + LLM)
- [ ] Plan mode approval gate
- [ ] GitHub MCP connector nyata
- [ ] Marketplace skill (registry + trust)
- [ ] Cost tracker

## Fase 5 — V2

- [ ] Voice input
- [ ] Kolaborasi `apex share`
- [ ] Multi-agent orchestrator
- [ ] Sandbox Docker default

## Open decision `[OPEN]`

Open questions have all been [DECIDED] and recorded in
[`32-open-questions.md`](../decisions/32-open-questions.md). See
[`31-decisions.md`](../decisions/31-decisions.md) for the decision log.
