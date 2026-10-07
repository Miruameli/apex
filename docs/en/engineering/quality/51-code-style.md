# 51 — Code Style Guide (Rust/Python/TS)

## Rust

### Formatter

```sh
cargo fmt
```

### Linter

```sh
cargo clippy -- -D warnings
```

### Konvensi

- `edition = "2024"`, `resolver = "3"`
- Error handling: `thiserror` untuk library, `anyhow` untuk binary
- No `unwrap()` di production code — gunakan `?` atau `expect()` dengan message
- Module per concern: `context.rs`, `protocol.rs`, `session.rs`, `skill.rs`
- Public API minimal: `pub fn` hanya yang dibutuhkan eksternal

### Template error

```rust
#[derive(thiserror::Error, Debug)]
pub enum ApexError {
    #[error("context scan failed: {0}")]
    ContextError(String),
    #[error("protocol error: {0}")]
    ProtocolError(String),
}
```

## Python

### Formatter & linter

```sh
ruff format
ruff check --fix
```

### Konvensi

- Python 3.12+ syntax (match/case, type hints wajib)
- `pydantic` untuk schema validation
- `asyncio` untuk async IO
- No `print()` di library — gunakan `logging`
- Type hints wajib untuk public function

### Template agent handler

```python
from typing import Iterator
from apex.protocol import AgentRequest, AgentEvent

class ApexAgent:
    def handle(self, request: AgentRequest) -> Iterator[AgentEvent]:
        match request:
            case ChatRequest(message=msg):
                yield from self._handle_chat(msg)
            case _:
                yield Error(code="UNSUPPORTED", message=str(request))
```

## TypeScript (TS no-build)

### Formatter & linter

```sh
deno fmt
deno lint
```

### Konvensi

- No build step: langsung `deno run` atau `node --experimental-strip-types`
- Interface over type untuk object shape
- `strict: true` di tsconfig (jika pakai Node)
- No `any` — gunakan `unknown` + narrowing
- Module: ES modules native

### Template IPC client

```typescript
export class IPCClient {
  constructor(private process: ChildProcess) {}

  send(request: Request): void {
    this.process.stdin!.write(JSON.stringify(request) + "\n");
  }

  *events(): Generator<Event> {
    for await (const line of this.process.stdout!) {
      yield JSON.parse(line.toString());
    }
  }
}
```

## Cross-language (protocol)

- Semua type di `protocol.rs` / `protocol.py` / `protocol.ts` harus match
- Fixtures di `tests/fixtures/protocol/**/*.json` = satu sumber kebenaran
- Deep-equal parsed JSON (sort keys), bukan raw string compare
