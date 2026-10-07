# 27 — Error Handling Strategy

## Error taxonomy

| Category | Contoh | Handling |
|---|---|---|
| Config | `apex.json` tidak valid, key hilang | Event `Error` + cara fix, exit code 2 |
| LLM | Network timeout, rate limit, invalid key | Retry 3x backoff → `Error` event |
| Context | File tidak readable, binary file | Skip file + WARN, lanjut scan |
| Tool | Shell command gagal, LSP tidak available | `Error` event, session tetap hidup |
| Skill | Manifest tidak valid, subprocess crash | `Error` event, tidak kill agent |
| Security | Permission denied, secret terdeteksi | Abort + `Error` event + audit log |
| Bridge | `import apex_py` gagal | `ApexBridgeError` dengan cara fix |

## Error event schema

```json
{
  "type": "Error",
  "code": "CONFIG_INVALID|LLM_TIMEOUT|TOOL_FAILED|PERMISSION_DENIED|BRIDGE_ERROR",
  "message": "human-readable",
  "details": {...},
  "suggestion": "cara fix"
}
```

## Logging

| Level | Tujuan | Output |
|---|---|---|
| `DEBUG` | Development | stderr, via `--verbose` |
| `INFO` | Progress | stderr |
| `WARN` | Fallback/non-fatal | stderr |
| `ERROR` | Gagal | stderr + event `Error` |

stdout: hanya data (JSONL events atau final result). Tidak ada log.

## Recovery

| Error | Recovery |
|---|---|
| LLM timeout | Retry 3x → fallback provider → `Error` |
| Tool crash | Event `Error`, agent lanjut |
| Skill crash | Event `Error`, host tetap hidup |
| Bridge error | Instruksi fix, tidak fallback silent |
| Session corrupt | Log + start new session |

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Runtime error (LLM, tool, skill) |
| 2 | Usage error (bad args, config invalid) |
| 3 | Security violation (permission denied, secret) |
