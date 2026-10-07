# 33 — System: Provider LLM Interface

## Tujuan

Abstraksi provider LLM agar `apex.json` bisa custom/mengganti endpoint tanpa ubah kode.

## Interface

```python
class LLMProvider(Protocol):
    def chat(self, messages: list[dict], stream: bool = True) -> Iterator[str]: ...
    def complete(self, prompt: str) -> str: ...
```

## Implementasi

| Provider | Class | Auth | Endpoint |
|---|---|---|---|
| OpenAI | `OpenAIProvider` | API key | `api.openai.com/v1` |
| Anthropic | `AnthropicProvider` | API key | `api.anthropic.com/v1` |
| Custom | `CustomProvider` | API key env | `apex.json.base_url` |
| Ollama | `OllamaProvider` | Tidak | `localhost:11434` |

## `apex.json` provider config

```json
{
  "model": "llama-3.1-8b",
  "provider": {
    "type": "custom",
    "base_url": "http://localhost:11434/v1",
    "api_key_env": "APEX_KEY"
  }
}
```

## Fallback

```json
{
  "fallback": ["openai:gpt-4o", "anthropic:claude-sonnet"]
}
```

Jika primary gagal → event `Warn` → coba fallback. Jika semua gagal → event `Error`.

## Streaming

- SSE (Server-Sent Events) untuk OpenAI/Anthropic/Custom
- Chunked response untuk Ollama
- Python `httpx` async client
