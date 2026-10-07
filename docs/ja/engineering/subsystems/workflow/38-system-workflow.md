# 38 — System: Review + Commit + Ship Integration

## Tujuan

Integrasi 3 fitur jadi workflow: review → commit → ship.

## Workflow

```
1. apex review --staged    → issues list
2. Fix issues (manual atau apex chat "fix ...")
3. apex review --staged    → verify clear
4. apex commit             → atomic message
5. apex ship               → PR + changelog
```

## Cross-cutting concerns

### Approval gates

| Step | Approval |
|---|---|
| Review | Show issues → user decide fix/ignore |
| Commit | Show message draft → confirm |
| Ship | Show PR description → confirm |

Tidak ada auto-merge. Tidak ada auto-push tanpa `--push`.

### Error recovery

| Error | Recovery |
|---|---|
| Review critical issue | User fix → re-review → lanjut |
| Commit fails (nothing staged) | Error message → user stage files |
| Ship fails (no branch) | Error message → user create branch |
| Ship fails (MCP timeout) | Retry → fallback manual markdown output |

### State sync

- Setiap step update session history
- Jika gagal di tengah → session status `error`, bisa resume
- `.apex/sessions/<id>.jsonl` record semua

## Safety checks sebelum `ship`

1. Semua tests pass? (`apex test` future)
2. Tidak ada secret di diff? (scan regex)
3. Tidak ada TODO/FIXME baru? (scan regex)
4. Branch bukan `main`? (check)

Gagal salah satu → blokir `ship` dengan error message jelas.
