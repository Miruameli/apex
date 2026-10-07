# 34 — System: Tool Registry & Permissions

## Tujuan

Registry tunggal tool & skill di `apex/tools/` (Python). Rust host hanya validasi/enforce/spawn.

## Registry struktur

```python
# apex/tools/__init__.py
REGISTRY = {
    "fs_read": {"handler": fs_read, "permission": "fs:read"},
    "fs_write": {"handler": fs_write, "permission": "fs:write"},
    "shell_exec": {"handler": shell_exec, "permission": "shell:exec"},
    "git_status": {"handler": git_status, "permission": "git:read"},
    "lsp_symbols": {"handler": lsp_symbols, "permission": "lsp:read"},
}
```

## Permission model

| Permission | Aksi | Gate |
|---|---|---|
| `fs:read` | Baca file | Auto-allow (MVP) |
| `fs:write` | Tulis file | Approval diff per-hunk |
| `shell:exec` | Jalankan command | Approval y/n |
| `git:read` | Git status/diff | Auto-allow |
| `git:write` | Git commit/push | Approval y/n |
| `lsp:read` | Query LSP | Auto-allow |

## Permission enforcement

1. Agent emit `ToolCall` event dengan name + args
2. Host Rust lookup permission di registry (via bridge)
3. Jika ada permission write/exec → tampilkan approval gate (TUI/CLI)
4. Jika denied → event `Error` dengan code `PERMISSION_DENIED`
5. Jika approved → spawn tool/subprocess

## Skill permission

Di manifest `apex.skill.json`:

```json
{
  "permissions": {
    "fs": ["read", "write"],
    "shell": true,
    "net": ["https://api.example.com"]
  }
}
```

Host Rust enforce: subprocess tidak bisa akses di luar scope yang di-grant.

## Tool discovery

- Built-in: fs, shell, git, lsp (di `apex/tools/`)
- Custom: via skill (`SKILL.md` + script)
- MCP: via `type: "mcp"` skill
