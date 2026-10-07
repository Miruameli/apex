# 17 — System: Review Engine

## Tujuan

`apex review` → analisis diff (staged/branch) untuk security, perf, clean code.

## Komponen

| Komponen | Tech | Peran |
|---|---|---|
| Diff reader | Rust/git2 (future) / `git diff` shell | Ambil diff |
| Rule engine | Python | Pattern rules (secrets, TODO, complexity) |
| LLM reviewer | Python | Prompt berisi diff + APEX.md rules → rekomendasi |
| Output formatter | Python | JSON / markdown / TUI panel |

## Flow

1. `apex review --staged` atau `--branch <name>`
2. Ambil diff
3. Rule engine scan cepat: secrets (regex), TODO, large function, nested loop
4. LLM review: prompt = system review rules + diff + konteks file
5. Output: list issue `{severity, file, line, message, suggestion}`

## Output schema

```json
[
  {"severity": "high", "file": "src/main.rs", "line": 42, "message": "possible secret", "suggestion": "use env var"}
]
```

## Severity

- `critical` — blokir PR
- `high` — wajib fix
- `medium` — saran kuat
- `low` — nice-to-have

## Rules override

`apex.json` → `review_rules` (V1): tambah rule custom per proyek.
