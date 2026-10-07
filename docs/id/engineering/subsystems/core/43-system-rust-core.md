# 43 — System: Rust Core Detail

## Tujuan

Speed core: context scan, protocol, session, skill host, plugin host.

## Module structure

```
crates/apex-core/src/
  lib.rs           # public API
  context.rs       # ContextEngine: scan files, git, LSP hint
  protocol.rs      # Request/Response/Event enums + serde
  session.rs       # Session state machine + history
  skill.rs         # SkillManifest parse + run
  plugin.rs        # Plugin host (future WASM)
  security.rs      # Permission check + audit log
```

## `context.rs` draft

```rust
pub struct ContextEngine {
    root: PathBuf,
    ignore_rules: Vec<Pattern>,
}

pub fn scan(&self) -> Result<Vec<FileEntry>> {
    let mut entries = vec![];
    for entry in WalkDir::new(&self.root) {
        let entry = entry?;
        if self.should_ignore(&entry) { continue; }
        entries.push(FileEntry {
            path: entry.path().to_str().unwrap().into(),
            language: detect_language(entry.path()),
            size: entry.metadata()?.len(),
        });
    }
    Ok(entries)
}
```

## `protocol.rs` draft

```rust
#[derive(Serialize, Deserialize, Debug, PartialEq)]
#[serde(tag = "type")]
pub enum Request {
    #[serde(rename = "Chat")]
    Chat { message: String },
    #[serde(rename = "Fix")]
    Fix { target: String },
    #[serde(rename = "Review")]
    Review { path: String },
    #[serde(rename = "Context")]
    Context { root: String },
}

#[derive(Serialize, Deserialize, Debug, PartialEq)]
#[serde(tag = "type")]
pub enum Event {
    Thinking { content: String },
    ToolCall { name: String, args: serde_json::Value },
    Diff { path: String, old: String, new: String },
    Message { role: String, content: String },
    Done { usage: Usage },
    Error { message: String },
}
```

## `session.rs` draft

```rust
pub struct Session {
    pub id: Uuid,
    pub status: SessionStatus,
    pub history: Vec<Event>,
}

impl Session {
    pub fn new() -> Self { ... }
    pub fn handle(&mut self, req: Request) -> Vec<Event> { ... }
    pub fn add_event(&mut self, event: Event) { ... }
}
```

## `skill.rs` draft (lihat #41)

Permission check + subprocess spawn + JSONL comms.

## Error handling

```rust
#[derive(thiserror::Error, Debug)]
pub enum ApexError {
    #[error("context scan failed: {0}")]
    ContextError(String),
    #[error("protocol parse error: {0}")]
    ProtocolError(String),
    #[error("permission denied: {0}")]
    PermissionDenied(String),
    #[error("skill spawn failed: {0}")]
    SkillError(String),
}
```
