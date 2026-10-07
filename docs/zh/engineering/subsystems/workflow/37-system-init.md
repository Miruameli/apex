# 37 — System: Project Initialization

## Tujuan

`apex init` → setup proyek baru: scan, generate `APEX.md` + `apex.json`, siap chat.

## Flow

1. `apex init [root]`
2. Scan struktur proyek (root = cwd atau `[root]`)
3. Deteksi bahasa (from file extensions)
4. Deteksi framework/deps (`Cargo.toml`, `package.json`, `pyproject.toml`, `go.mod`)
5. Generate `apex.json` template (provider = custom/ollama default)
6. Generate `APEX.md` template (context = deteksi framework, rules = empty)
7. Buat `.apex/` folder (gitignore)
8. Output: "Apex initialized at <root>"

## Generated files

### `apex.json`

```json
{
  "model": "llama-3.1-8b",
  "provider": {
    "type": "ollama",
    "base_url": "http://localhost:11434",
    "api_key_env": ""
  },
  "fallback": [],
  "tools": {"fs": true, "shell": true, "git": true, "lsp": false}
}
```

### `APEX.md`

```markdown
# Project: <detected name>

## Context
<detected description / framework>

## Rules
- <empty — user isi>

## Preferred tools
- <detected formatter/linter jika ada>

## Skills allowed
- <empty>
```

## `.gitignore` update

Append:
```
.apex/
.env
*.so
target/
```

## Idempotency

- Jika `apex.json` sudah ada → tanya `overwrite/skip/merge`
- Jika `APEX.md` sudah ada → tanya `overwrite/skip/merge`
- `.apex/` selalu dibuat jika belum ada
