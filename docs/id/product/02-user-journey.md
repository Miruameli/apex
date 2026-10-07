# 02 — User Journey (hari pertama)

## Skenario 1 — Setup

```sh
pip install apex          # install brain Python
apptui                    # install TUI runtime (deno/node)
apex init                 # scan project, tulis APEX.md
```

Setelah `apex init`, struktur:
```
project/
  APEX.md          # memory + rules + konteks
  apex.json        # provider LLM + model + tools
  .apex/           # runtime state, index, cache (di-ignore git)
```

## Skenario 2 — Chat dengan konteks

```sh
apex chat "kenapa test eder flaky?"
```

Agent:
1. Baca APEX.md + apex.json
2. Scan file relevan (context engine Rust)
3. Kirim ke LLM via custom provider
4. Stream jawaban ke terminal
5. Jika propose edit → tampilkan diff → tunggu approval

## Skenario 3 — Review + commit + PR

```sh
apex review --staged       # review staged changes: security/perf/clean
apex commit                # atomic commit message dari diff
apex ship                  # buka PR (mock lokal dulu, GitHub nyusul)
```

## Skenario 4 — TUI interaktif

```sh
apex                       # launch TUI
```

Panel:
```
┌─ files ─────┬─ chat/agent ──────┬─ diff preview ─┐
│ explorer    │ thinking/calls    │ accept/reject  │
├─────────────┼───────────────────┼────────────────┤
│ terminal    │ input ›           │ status/cost    │
└─────────────┴───────────────────┴────────────────┘
```

Keybindings (draft): `j/k` navigasi, `a/r` accept/reject hunk, `Ctrl+K` panggil Apex, `q` keluar.

## Skenario 5 — Tambah skill

```sh
apex skill add vercel-deploy
# → tulis skills/vercel-deploy/SKILL.md + main.py + apex.skill.json
apex skill run vercel-deploy
```

Host Rust validasi manifest, enforce permission (fs/shell/net), spawn subprocess, komunikasi JSONL.
