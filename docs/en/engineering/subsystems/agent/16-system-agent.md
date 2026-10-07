# 16 — System: Agent Core

## Tujuan

Otak utama: terima request → ambil konteks → panggil LLM → stream event → eksekusi tool dengan approval.

## Komponen

| Komponen | Tech | Peran |
|---|---|---|
| `ApexAgent` | Python `apex/agent/core.py` | Handle request, orchestrate loop |
| `ApexAgent.serve_stdio` | Python asyncio | JSONL IPC server untuk TUI/CLI |
| LLM gateway | Python `openai`/`anthropic`/custom | Call provider, stream response |
| Tool registry | Python `apex/tools/` | Registry tunggal fs/shell/git/lsp |
| Prompt builder | Python `apex/agent/prompts.py` | System prompt + APEX.md context |
| Session state | Rust `apex-core/session.rs` | History, id, state machine |

## Loop

```
req → load APEX.md + apex.json
    → scan context (Rust bridge)
    → build prompt (system + context + history)
    → LLM stream
    → parse tool_call / diff / message
    → jika edit → diff preview → approval
    → jika tool_call → registry → Rust host spawn
    → emit event JSONL
    → Done
```

## Error handling

- LLM error → event `Error`, retry dengan backoff (V1)
- Tool error → event `Error` + reason, tidak crash session
- Context error → fallback Python scan + WARN

## State machine

```
Idle → Thinking → ToolCall → WaitingApproval → Done
              ↘ Error
```

## Approval gate

- Edit file: TUI tampilkan diff per-hunk, `a` accept / `r` reject
- Shell command: tampilkan command, `y` confirm / `n` cancel
- Tidak ada autonomous edit tanpa approval (MVP)
