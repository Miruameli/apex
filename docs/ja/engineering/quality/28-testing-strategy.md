# 28 — Testing Strategy

## Level test

| Level | Scope | Tool | Target |
|---|---|---|---|
| Unit | Fungsi kecil, parser, formatter | pytest/cargo test/deno test | >80% coverage untuk business logic |
| Integration | Agent loop, bridge, skill spawn | pytest + cargo test | Happy path + error path |
| Contract | Protocol fixtures 3 bahasa | pytest + cargo test + deno test | 100% fixtures pass |
| E2E | `apex chat`, `apex review`, `apex skill` | Script bash / pytest subprocess | Critical path |

## Contract test (wajib)

`tests/fixtures/protocol/**/*.json` = satu sumber kebenaran.

Test 3 bahasa:
1. Rust: `protocol::Request::from_json(fixture)` → `to_json()` → deep-equal
2. Python: `AgentRequest.model_validate_json(fixture)` → `model_dump_json()` → deep-equal
3. TS: `JSON.parse(fixture)` → `JSON.stringify(parsed)` → deep-equal

Semua harus pass. Jika ada drift → PR ditolak.

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

## E2E tests

| Scenario | Command | Expected |
|---|---|---|
| Chat basic | `apex chat "halo"` | JSONL events, no crash |
| Context scan | `apex context` | JSON list files |
| Review | `apex review --staged` | JSON list issues |
| Skill run | `apex skill run test-skill` | JSONL events |
| TUI smoke | `apex tui` | TUI render (manual test) |

## CI

Workflow: `.github/workflows/quality.yml`

- Stages: lint → format → test → security
- Gates: `lint`, `test`, `security`
- No merge jika CI merah

## Test isolation

- Setiap test: temp dir, temp `.apex/`, tidak menyentuh global state
- LLM calls di-mock atau pakai Ollama local
- Tidak ada network test di unit/integration
