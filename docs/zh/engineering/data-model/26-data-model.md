# 26 — Data Model

## Entities

### Session

```json
{
  "id": "uuid",
  "project_root": "/path/to/project",
  "started_at": "ISO8601",
  "status": "idle|thinking|waiting_approval|done|error",
  "history": [Event]
}
```

### Event

```json
{
  "type": "Chat|Fix|Review|Context|Thinking|ToolCall|Diff|Message|Done|Error",
  "timestamp": "ISO8601",
  "payload": {...}
}
```

### ContextIndex

```json
[
  {
    "path": "src/main.rs",
    "language": "rust",
    "size": 1234,
    "git": {"last_commit": "abc123", "author": "...", "date": "..."},
    "symbols": ["fn main", "struct X"]
  }
]
```

### SkillManifest

```json
{
  "name": "string",
  "version": "semver",
  "type": "skill|mcp",
  "entrypoint": "path",
  "runtime": "python|node|deno|binary",
  "permissions": {"fs": [...], "shell": bool, "net": [...]},
  "tools": ["string"],
  "env": ["string"]
}
```

### ProviderConfig (apex.json)

```json
{
  "model": "string",
  "provider": {
    "type": "custom|openai|anthropic|ollama",
    "base_url": "string",
    "api_key_env": "string"
  },
  "fallback": ["string"],
  "tools": {"fs": bool, "shell": bool, "git": bool, "lsp": bool}
}
```

### ReviewResult

```json
[
  {
    "severity": "critical|high|medium|low",
    "file": "path",
    "line": 42,
    "message": "string",
    "suggestion": "string"
  }
]
```

### CommitDraft

```json
{
  "type": "feat|fix|docs|...",
  "scope": "string",
  "subject": "string",
  "body": "string",
  "footer": "string"
}
```

## Storage

| Data | Path | Format | Git |
|---|---|---|---|
| Project config | `apex.json` | JSON | Commit |
| Project memory | `APEX.md` | Markdown | Commit |
| Session history | `.apex/sessions/<id>.jsonl` | JSONL | Ignore |
| Context cache | `.apex/cache/index.db` | SQLite | Ignore |
| Audit log | `.apex/logs/audit.jsonl` | JSONL | Ignore |
| User config | `~/.apex/config.json` | JSON | N/A |

## Relationships

```
Session --has_many--> Event
Event --has_one--> (ToolCall | Diff | Message | Done | Error)
ApexAgent --has_one--> ProviderConfig (from apex.json)
ApexAgent --has_one--> ContextIndex
SkillManifest --belongs_to--> Project
```
