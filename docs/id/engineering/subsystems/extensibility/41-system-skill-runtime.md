# 41 — System: Skill Runtime Detail

## Lifecycle detail

```
apex skill add <name>
  → scaffold folder
  → template SKILL.md + apex.skill.json + main.py
  → validate manifest schema

apex skill list
  → scan skills/*/
  → parse apex.skill.json
  → validate schema (name, version, entrypoint exists)
  → output table

apex skill run <name> [args]
  → load manifest
  → check permission (fs/shell/net)
  → resolve runtime (python/node/deno/binary)
  → spawn subprocess
  → JSONL comms
  → emit SkillOutput events
```

## Manifest schema (full)

```json
{
  "name": "string (required, unique, lowercase+dash)",
  "version": "string semver (required)",
  "type": "\"skill\" | \"mcp\" (required)",
  "description": "string (optional)",
  "author": "string (optional)",
  "license": "string (optional, default MIT)",
  "entrypoint": "string path relatif (required untuk skill)",
  "runtime": "\"python\" | \"node\" | \"deno\" | \"binary\" (required untuk skill)",
  "command": "string (required untuk mcp)",
  "args": ["string"] (untuk mcp),
  "env": {"VAR": "value"} (untuk mcp),
  "permissions": {
    "fs": ["read" | "write" | "admin"],
    "shell": true | false,
    "net": ["host1", "host2"] atau ["*"]
  },
  "tools": ["string"] (tools yang di-expose),
  "min_apex_version": "string semver (optional)"
}
```

## Permission enforcement (MVP)

| Permission | Check saat run |
|---|---|
| `fs.read` | Subprocess boleh baca file di project root |
| `fs.write` | Subprocess boleh tulis file (di project root only) |
| `shell` | Subprocess boleh spawn shell command |
| `net` | Subprocess boleh network ke host di list |

Violation → subprocess killed + event `Error` code `PERMISSION_DENIED`.

## Subprocess spawn (Rust host)

```rust
// crates/apex-core/src/skill.rs
pub fn run_skill(manifest: &SkillManifest, args: &[&str]) -> Result<SkillHandle> {
    let mut cmd = Command::new(manifest.runtime.command());
    cmd.arg(manifest.entrypoint);
    cmd.args(args);
    cmd.stdin(Stdio::piped());
    cmd.stdout(Stdio::piped());
    cmd.stderr(Stdio::piped());
    // Permission check sebelum spawn
    validate_permissions(manifest)?;
    let child = cmd.spawn()?;
    Ok(SkillHandle { child, manifest })
}
```

## JSONL comms (skill → host)

Skill tulis ke stdout:
```json
{"type":"SkillOutput","data":{"message":"..."}}
{"type":"SkillOutput","data":{"progress":50}}
{"type":"Done","result":"success"}
```

Host parse line-by-line, forward ke agent sebagai event stream.
