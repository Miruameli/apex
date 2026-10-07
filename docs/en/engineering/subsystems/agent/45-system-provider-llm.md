# 45 — System: Provider LLM Detail

## Interface

```python
class LLMProvider(Protocol):
    def stream(self, prompt: str) -> Iterator[str]: ...
    def complete(self, prompt: str) -> str: ...
```

## Provider implementations

### CustomProvider

```python
class CustomProvider:
    def __init__(self, base_url: str, api_key: str, model: str):
        self.client = httpx.AsyncClient(base_url=base_url)
        self.api_key = api_key
        self.model = model

    def stream(self, prompt: str) -> Iterator[str]:
        response = self.client.post("/v1/chat/completions", json={
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
        }, headers={"Authorization": f"Bearer {self.api_key}"})
        for line in response.iter_lines():
            if line.startswith("data: "):
                data = json.loads(line[6:])
                yield data["choices"][0]["delta"].get("content", "")
```

### OllamaProvider

```python
class OllamaProvider:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model

    def stream(self, prompt: str) -> Iterator[str]:
        response = requests.post(f"{self.base_url}/api/generate", json={
            "model": self.model,
            "prompt": prompt,
            "stream": True,
        }, stream=True)
        for line in response.iter_lines():
            data = json.loads(line)
            yield data.get("response", "")
```

## Factory

```python
def create_provider(config: ProviderConfig) -> LLMProvider:
    match config.type:
        case "custom":
            return CustomProvider(config.base_url, os.environ[config.api_key_env], config.model)
        case "ollama":
            return OllamaProvider(config.base_url, config.model)
        case "openai":
            return OpenAIProvider(os.environ[config.api_key_env], config.model)
        case _:
            raise ValueError(f"Unknown provider: {config.type}")
```

## Fallback chain

```python
def stream_with_fallback(prompt: str, providers: list[LLMProvider]) -> Iterator[str]:
    for i, provider in enumerate(providers):
        try:
            yield from provider.stream(prompt)
            return
        except LLMError as e:
            if i < len(providers) - 1:
                yield f"[WARN] Provider {type(provider).__name__} failed, trying fallback...\n"
            else:
                raise e
```
