# 07 — Skills & MCP

## Format skill

```
skills/<name>/
  SKILL.md        # deskripsi manusia + agent instructions
  apex.skill.json # manifest mesin
  main.py         # atau main.ts / binary
```

## `apex.skill.json` (schema draft)

```json
{
  "name": "vercel-deploy",
  "version": "0.1.0",
  "type": "skill",
  "entrypoint": "main.py",
  "runtime": "python",
  "permissions": {
    "fs": ["read", "write"],
    "shell": true,
    "net": ["https://api.vercel.com"]
  },
  "tools": ["deploy", "logs"],
  "mcp": false
}
```

## `SKILL.md`

- Nama, versi, deskripsi
- Permission yang dibutuhkan (fs/shell/net)
- Cara pakai (command examples)
- Tool yang di expose
- Instructions untuk agent (prompt tambahan)

## Rust host responsibilities

1. `apex skill add <name>` → scaffold folder + template
2. `apex skill list` → scan `skills/`, parse manifest
3. `apex skill run <name> [args]` → validate manifest, check permission, spawn subprocess
4. Permission enforcement: subprocess tidak boleh akses di luar `fs` grant, shell tidak boleh command tidak di-allow, net tidak boleh host tidak di-allow (V1: warning; MVP: subprocess isolation cukup)

## MCP

`type: "mcp"` di manifest. Host Rust spawn MCP server (stdio), route requests. Contoh:

```json
{
  "name": "github-mcp",
  "type": "mcp",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
}
```

## Marketplace (future)

- Lokal: `apex skill add <name>` dari repo Git
- Remote (V2): registry + trust + review process
- Tidak di-MVP.
