# 18 — System: Commit & Ship

## Tujuan

`apex commit` → atomic commit message dari staged diff. `apex ship` → PR + changelog.

## Komponen

| Komponen | Tech | Peran |
|---|---|---|
| Diff staged | shell `git diff --cached` | Ambil staged changes |
| Message generator | Python LLM | Prompt: diff + APEX.md conventions → commit message |
| Atomic checker | Python | Split large commit jadi beberapa logical commit (V1) |
| PR creator | Python + MCP/GitHub | Buat PR dengan deskripsi + checklist |
| Changelog writer | Python | Update `CHANGELOG.md` |

## Flow `apex commit`

1. `git diff --cached`
2. Jika kosong → error "tidak ada staged changes"
3. LLM generate message (Conventional Commits format)
4. Tampilkan draft → user confirm `y/n` / edit
5. `git commit -m ...`

## Format message

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`, `ci`.

## Flow `apex ship`

1. `git branch --show-current` → pastikan bukan main
2. Generate PR description dari commits branch
3. MCP GitHub create PR (atau output markdown untuk copy manual)
4. Update `CHANGELOG.md` under `Unreleased`

## Safety

- Tidak push otomatis tanpa `--push` flag
- Tidak merge PR otomatis
- PR description wajib review sebelum create
