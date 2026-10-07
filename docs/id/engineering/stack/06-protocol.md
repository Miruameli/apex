# 06 — Protocol

## Prinsip

1. Satu sumber kebenaran = `tests/fixtures/protocol/**/*.json`.
2. Rust `protocol.rs`, Python `protocol.py`, TS `protocol.ts` adalah mirror — wajib round-trip fixtures yang sama.
3. Test 3 bahasa assert **deep-equal parsed JSON (sort keys)**, bukan raw string.
4. `check` task = `cargo build && sync && deno test && pytest && cargo test` — semua merah jika drift.

## Schema

### AgentRequest

```json
{
  "type": "Chat|Fix|Review|Context",
  ...payload
}
```

| Variant | Payload |
|---|---|
| `Chat` | `{ "message": string }` |
| `Fix` | `{ "target": string }` |
| `Review` | `{ "path": string }` |
| `Context` | `{ "root": string }` |

### AgentEvent

| Variant | Payload |
|---|---|
| `Thinking` | `{ "content": string }` |
| `ToolCall` | `{ "name": string, "args": any }` |
| `Diff` | `{ "path": string, "old": string, "new": string }` |
| `Message` | `{ "role": string, "content": string }` |
| `Done` | `{ "usage": { "prompt_tokens": number, "completion_tokens": number } }` |
| `Error` | `{ "message": string }` |

## Fixtures wajib

```
tests/fixtures/protocol/
  requests/
    chat_request.json
    fix_request.json
    review_request.json
    context_request.json
  events/
    stream/
      event_thinking.json
      event_toolcall.json
      event_diff.json
      event_message.json
    terminal/
      event_done.json
      event_error.json
```

Setiap fixture harus:
- Valid JSON
- Dapat di-deserialize oleh Rust (`serde`), Python (`pydantic`), TS (`JSON.parse`)
- Re-serialize dan parse lagi → deep-equal (sort keys, normalize whitespace)

## Konvensi IPC

- `stdout` = JSONL events, satu event per line. **Banner/log ke `stderr`.**
- Parser di sisi penerima wajib `try/catch` per-line: line bukan JSON → emit `Error` event, bukan crash stream.
- Encoding UTF-8. Newline `\n`.

## Contoh round-trip

Request:
```json
{"type":"Chat","message":"halo"}
```

Response stream:
```json
{"type":"Thinking","content":"..."}
{"type":"Message","role":"assistant","content":"..."}
{"type":"Done","usage":{"prompt_tokens":10,"completion_tokens":5}}
```
