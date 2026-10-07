# 21 — System: TUI

## Tujuan

Full lazygit-style TUI: split-panel, keyboard-first, diff per-hunk accept/reject.

## Layout (draft)

```
┌─ files ─────────┬─ chat ──────────┬─ diff preview ─┐
│ explorer tree   │ thinking/calls  │ accept/reject  │
│                 │ messages        │ per-hunk       │
├─────────────────┼─────────────────┼────────────────┤
│ terminal panel  │ input ›         │ status/cost    │
└─────────────────┴─────────────────┴────────────────┘
```

## Panel

| Panel | Isi | Keybindings |
|---|---|---|
| files | Tree file proyek | `j/k` navigasi, `enter` buka, `space` select |
| chat | Agent stream + user input | ` Ctrl+K` focus, `enter` send, `esc` cancel |
| diff | Diff per-hunk | `a` accept, `r` reject, `d` next hunk, `u` prev hunk |
| terminal | Shell output | `t` focus, `Ctrl+C` kill |
| status | State, cost, git branch | read-only |

## Diff pipeline

1. Agent emit `Diff` event → TUI split jadi hunks
2. Per-hunk: show context + change
3. `a` → apply hunk ke file
4. `r` → skip hunk
5. Semua hunk resolved → status `Done` atau manual save

## Framework (OPEN)

| Kandidat | Pro | Kontra |
|---|---|---|
| Cliffy (TS) | Deno native, no-build | Maturity TUI |
| OpenTUI (TS) | Aktif, diff component | Lebih baru |
| Bubbletea (Go) | Proven, lazygit-like | Bahasa Go (di luar stack) |
| stdlib (Deno/Node) | Zero dep | Manual layout, effort tinggi |

Keputusan: PoC kecil per kandidat, pilih yang paling cocok diff pipeline.

## Theme

- Dark/light/user-defined
- String bilingual (Indonesia/English) di `tui/src/i18n.ts`

## State sync

- TUI = client JSONL ke agent serve_stdio
- State lokal: selected file, cursor panel, scroll position
- Tidak ada state agent di TUI
