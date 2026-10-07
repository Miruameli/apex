# 19 — System: Skills Lifecycle

## Lifecycle

```
install/scaffold → validate manifest → list → run → sandbox exec → report
```

## Commands

| Command | Aksi |
|---|---|
| `apex skill add <name>` | Scaffold folder + template `SKILL.md` + `apex.skill.json` |
| `apex skill list` | Scan `skills/`, parse manifest, tampilkan name/version/permission |
| `apex skill run <name> [args]` | Validate → enforce permission → spawn subprocess → JSONL comms |
| `apex skill remove <name>` | Hapus folder (dengan konfirmasi) |
| `apex skill validate <path>` | Cek manifest schema tanpa jalan |

## Manifest schema (draft)

```json
{
  "name": "string (required, unique)",
  "version": "semver (required)",
  "type": "skill|mcp (required)",
  "entrypoint": "path relatif (required)",
  "runtime": "python|node|deno|binary (required)",
  "description": "string",
  "permissions": {
    "fs": ["read"|"write"|"admin"],
    "shell": true|false,
    "net": ["host1", "host2"]
  },
  "tools": ["string"],
  "env": ["VAR1", "VAR2"]
}
```

## Validation rules

- `name` wajib, alphanumeric + dash, lowercase
- `version` wajib semver
- `entrypoint` wajib ada di disk
- `runtime` harus sesuai dengan entrypoint extension (atau `binary`)
- `permissions` default deny-all jika tidak ada

## Sandbox (MVP minimal)

- Subprocess terisolasi (bukan in-process)
- Permission violation → abort + error event
- V1: cgroups/seccomp/container
- MVP: permission check + subprocess isolation cukup

## JSONL protocol skill ↔ host

Skill output ke stdout:
```json
{"type":"Message","content":"..."}
{"type":"ToolCall","name":"...","args":{...}}
{"type":"Done","result":"..."}
{"type":"Error","message":"..."}
```
