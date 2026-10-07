# 36 — System: LSP Integration

## Tujuan

Apex ngerti kode: symbols, references, diagnostics, type info — bukan hanya text search.

## Tech

- LSP client: Rust/tokio (V1) atau Python `pygls` (MVP mock)
- Protocol: LSP (Language Server Protocol) JSON-RPC
- Server per bahasa: `rust-analyzer`, `pylsp`, `typescript-language-server`

## Capabilities

| Feature | LSP method | Apex use case |
|---|---|---|
| Symbol outline | `textDocument/documentSymbol` | Context scan |
| Go to definition | `textDocument/definition` | Navigate to code |
| Find references | `textDocument/references` | Impact analysis |
| Diagnostics | `textDocument/publishDiagnostics` | Review |
| Hover info | `textDocument/hover` | Type info untuk agent |
| Completion | `textDocument/completion` | Suggestion (future) |

## Flow

1. `apex context` → spawn LSP server per bahasa → `initialize`
2. Request `documentSymbol` untuk setiap file di context index
3. Cache symbols di `.apex/cache/symbols.db`
4. Agent query `apex_py.query_symbols(name)` → Rust → LSP → result

## MVP realitas

MVP: shell out ke `grep`/`rg` untuk text search. LSP nyata V1.

## Config

`apex.json` → `tools.lsp: true` enable LSP (V1).
