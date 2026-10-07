# 08 — Customization

## `apex.json` (provider LLM + model + tools)

```json
{
  "model": "custom-llama",
  "provider": {
    "type": "custom",
    "base_url": "http://localhost:11434",
    "api_key_env": "APEX_KEY"
  },
  "fallback": ["openai:gpt-5", "anthropic:claude-sonnet"],
  "tools": {
    "fs": true,
    "shell": true,
    "git": true,
    "lsp": false
  }
}
```

Konsep: satu file per proyek, bisa di-commit ke repo agar seluruh kontributor pakai provider yang sama (atau override lokal via env).

## `APEX.md` (memory & rules)

- Instruksi agent untuk proyek ini
- Preferensi kode (style, bahasa komentar)
- Konteks arsitektur penting
- List skill yang diizinkan

Dibaca setiap sesi. Tidak di-commit jika berisi rahasia lokal (umum: commit bagian non-rahasia, `.apex/` untuk cache rahasia).

## Tema & branding `[OPEN]`

- UI theme: dark/light/user-defined palette
- Branding produk: logo, warna — belum diputuskan, terbuka

## Review rules

Bisa di-override per proyek via `apex.json` → `review_rules` (V1).

## Persona & prompt

`apex/agent/prompts.py` = default system prompt. Bisa di-override via `APEX.md` (append/prepend).

## Bahasa UI

Bilingual-ready: struktur string terpisah, default TBD (Indonesia vs English). Dokumentasi wajib 3 bahasa (bahasa ketiga TBD).
