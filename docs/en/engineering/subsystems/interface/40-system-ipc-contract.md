# 40 — System: IPC Protocol Contract (full)

## Tujuan

Kontrak IPC yang menghubungkan SEMUA komponen: TUI ↔ CLI ↔ Agent ↔ Rust host ↔ Skills ↔ MCP.

## Topology

```
TUI (TS)  ──JSONL stdio──▶  Agent serve_stdio (Python)
CLI (Rust) ──JSONL stdio──▶  Agent serve_stdio (Python)
Agent ──PyO3──▶ Rust core (context/session/protocol)
Agent ──subprocess──▶ Skill runtime (Python/TS/binary)
Agent ──subprocess──▶ MCP server (stdio JSON-RPC)
Rust host ──permission check──▶ Skill spawn
```

## Request → Response mapping

| Client request | Agent handler | Rust bridge call | Tool routing | Event stream |
|---|---|---|---|---|
| `Chat` | `ApexAgent.handle_chat` | `scan_context(root)` | LLM call | `Thinking` → `Message` → `Done` |
| `Fix` | `ApexAgent.handle_fix` | `scan_context` + `lsp_diagnostics` | LLM + LSP | `Thinking` → `Diff` → `Done` |
| `Review` | `ApexAgent.handle_review` | `git_diff` | LLM reviewer | `Thinking` → `Message` → `Done` |
| `Context` | `ApexAgent.handle_context` | `scan_context(root)` | Context engine | `Message` (JSON list) → `Done` |

## Event types (complete)

| Event | Produced by | Consumed by |
|---|---|---|
| `Thinking` | LLM stream | TUI chat panel |
| `ToolCall` | Agent (tool dispatch) | TUI status panel |
| `Diff` | Agent (edit proposal) | TUI diff preview |
| `Message` | LLM | TUI chat panel |
| `Done` | Agent (usage) | TUI status + session |
| `Error` | Any failure | TUI + CLI stderr |
| `SkillOutput` | Skill subprocess | Agent tool routing |
| `MCPResponse` | MCP server | Agent tool routing |

## Session lifecycle

```
Idle → Chat request → Thinking → ToolCall(s) → Diff(s) → Approval → Message → Done → Idle
                       ↘ Error → Idle
```

## Fixture contract (complete list)

```
tests/fixtures/protocol/
  chat_request.json          # {"type":"Chat","message":"..."}
  fix_request.json           # {"type":"Fix","target":"..."}
  review_request.json        # {"type":"Review","path":"..."}
  context_request.json       # {"type":"Context","root":"..."}
  event_thinking.json        # {"type":"Thinking","content":"..."}
  event_toolcall.json        # {"type":"ToolCall","name":"...","args":{...}}
  event_diff.json            # {"type":"Diff","path":"...","old":"...","new":"..."}
  event_message.json         # {"type":"Message","role":"...","content":"..."}
  event_done.json            # {"type":"Done","usage":{...}}
  event_error.json           # {"type":"Error","message":"..."}
  skill_output.json          # {"type":"SkillOutput","data":...}
  mcp_response.json          # {"type":"MCPResponse","result":...}
```

## 3-bahasa contract test

Setiap fixture: parse → serialize → deep-equal parsed JSON (sort keys).

- Rust: `uv run cargo test -p apex-core protocol`
- Python: `uv run pytest -q tests/python/test_protocol.py`
- TS: `cd tui && deno test src/protocol_test.ts`

## Versioning protocol

- Semantic: breaking change = major bump di `protocol.py`/`protocol.rs`/`protocol.ts`
- Fixtures versioned: `tests/fixtures/protocol/v1/`, `v2/`
- Agent accept both v1 dan v2 events selama transisi (V1)
