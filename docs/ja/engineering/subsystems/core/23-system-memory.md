# 23 — System: Memory & State

## `APEX.md` (project memory)

Dibaca setiap sesi. Isi:

```markdown
# Project: <name>

## Context
<deskripsi arsitektur singkat>

## Rules
- Style guide
- Naming convention
- Bahasa komentar

## Preferred tools
- Formatter
- Linter
- Test runner

## Skills allowed
- skill-1
- skill-2
```

## `.apex/` (runtime state)

```
.apex/
  cache/          # index file, embedding cache
  sessions/       # history JSONL per session
  logs/           # debug log
```

Di-ignore git. Tidak pernah di-commit.

## Session state

- ID: UUID v4
- History: list events (user + agent)
- Status: `idle`, `thinking`, `waiting_approval`, `done`, `error`
- Disimpan di `.apex/sessions/<id>.jsonl`

## Vector DB (future)

- V1+: embeddings code chunks → semantic search
- Storage: `.apex/cache/vectors.db` (SQLite-vss atau similar)
- Tidak di MVP

## Memory scope

- Project: `APEX.md` (commit-able, non-secret)
- User: `~/.apex/config.json` (future, user-specific)
- Session: `.apex/sessions/` (runtime only)
