# 15 — System: Context Engine

## Tujuan

Ingest kode proyek, git history, LSP hints → index cepat untuk agent.

## Komponen

| Komponen | Tech | Peran |
|---|---|---|
| Scanner | Rust `apex-core` | Walk file, deteksi bahasa, size, ignore rules |
| Git reader | Rust `git2` crate (future) | History, diff, blame, staged |
| LSP client | Rust/tokio (future) | Symbols, references, diagnostics |
| Index cache | `.apex/cache/` (SQLite/sled) | Persistent index per repo |
| Query API | Rust → Python via PyO3 | `scan_context(root)`, `query_files(q)` |

## Flow

1. `apex context [root]` → scan file
2. Filter: `.gitignore`, `node_modules`, binary, hidden
3. Deteksi bahasa via extension + content sniff
4. Build tree index → `.apex/cache/index.db`
5. Output: JSON list `{path, language, size, relevance}`

## Output schema

```json
[
  {"path": "src/main.rs", "language": "rust", "size": 1234, "git": {"last_commit": "..."}}
]
```

## Future

- Semantic search via embeddings
- Call graph via LSP
- Dependency graph (Cargo.toml, package.json)
