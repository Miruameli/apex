# 20 — System: MCP (Model Context Protocol)

## Tujuan

Standard connector ke GitHub, DB, Notion, Linear via MCP servers (stdio).

## Integrasi di Apex

- MCP server = skill tipe `"mcp"`
- Manifest `apex.skill.json` punya `command` + `args` + `env`
- Host Rust spawn MCP process, route JSON-RPC

## Manifest MCP

```json
{
  "name": "github-mcp",
  "type": "mcp",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
}
```

## Flow

1. `apex skill list` → tampilkan MCP servers
2. Agent butuh tool → Rust host spawn MCP process
3. MCP process ready → host kirim `tools/list` request
4. Tool call dari agent → host route `tools/call` ke MCP
5. Response → host parse → emit event

## Security

- `env` vars: token via env, bukan hardcode
- Host validasi permission `net` di manifest
- MCP process di-sandbox sama dengan skill biasa
- Auto-install `npx` = opt-in, bukan default

## Stdio lifecycle

```
host spawn → initialize handshake → tools/list → tools/call loop → close
```

Jika MCP process crash → event `Error`, tidak crash agent. Restart V1.
