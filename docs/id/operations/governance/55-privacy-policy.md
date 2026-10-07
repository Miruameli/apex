# 55 — Privacy Policy (draft)

## Data yang tidak di-collect

Apex tidak mengirim data apapun ke server Apex. Tidak ada telemetri, analytics, atau tracking.

## Data yang disimpan lokal

| Data | Lokasi | Isi |
|---|---|---|
| Session history | `.apex/sessions/<id>.jsonl` | Chat, events, tool calls |
| Context cache | `.apex/cache/` | Index file, symbols |
| Audit log | `.apex/logs/audit.jsonl` | Edit history, approval |
| Config | `apex.json`, `APEX.md` | Provider config, memory |

Semua disimpan lokal di project directory. Tidak pernah dikirim ke cloud.

## LLM provider

- LLM calls dikirim ke provider yang user configure di `apex.json`
- Key API disimpan di `env` atau OS keyring, tidak pernah di-proxy
- Apex tidak menyimpan prompt/response di server manapun

## Skill runtime

- Skill subprocess punya akses ke fs/shell/net sesuai manifest permission
- Apex tidak mengirim data skill ke marketplace (V2 opt-in)

## User data rights

- Hapus session: `rm -rf .apex/sessions/`
- Hapus cache: `rm -rf .apex/cache/`
- Reset semua: `rm -rf .apex/`

## Changes

Updates ke privacy policy akan di-notify via `CHANGELOG.md`.
