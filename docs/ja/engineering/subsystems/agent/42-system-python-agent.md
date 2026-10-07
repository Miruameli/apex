# 42 — System: Python Agent Detail

## Tujuan

Otak utama: orchestrate request → context → LLM → tools → response.

## Class structure

```python
# apex/agent/core.py
class ApexAgent:
    def __init__(self, config: ApexConfig):
        self.config = config
        self.tools = ToolRegistry()
        self.llm = create_provider(config.provider)
        self.context = ContextEngine()  # via bridge

    def handle(self, request: AgentRequest) -> Iterator[AgentEvent]:
        match request:
            case ChatRequest(msg):
                yield from self.handle_chat(msg)
            case FixRequest(target):
                yield from self.handle_fix(target)
            case ReviewRequest(path):
                yield from self.handle_review(path)
            case ContextRequest(root):
                yield from self.handle_context(root)

    def handle_chat(self, message: str) -> Iterator[AgentEvent]:
        ctx = self.context.scan()
        prompt = self.build_prompt(message, ctx)
        yield Thinking(content="...")
        for chunk in self.llm.stream(prompt):
            yield Message(role="assistant", content=chunk)
        yield Done(usage=...)

    def serve_stdio(self):
        """JSONL stdin → handle → JSONL stdout"""
        for line in sys.stdin:
            req = AgentRequest.from_json(line)
            for event in self.handle(req):
                print(event.to_json(), flush=True)
```

## Prompt building

```python
def build_prompt(self, message: str, context: ContextIndex) -> str:
    system = DEFAULT_SYSTEM_PROMPT
    if self.has_apex_md():
        system += "\n\n" + self.load_apex_md()
    ctx_summary = self.summarize_context(context)
    return f"{system}\n\n---\nContext:\n{ctx_summary}\n\nUser: {message}"
```

## Async handling

```python
async def serve_stdio_async(self):
    reader = asyncio.StreamReader()
    for line in await reader.readline():
        req = AgentRequest.from_json(line)
        async for event in self.handle_async(req):
            sys.stdout.write(event.to_json() + "\n")
            sys.stdout.flush()
```

## Error handling

```python
try:
    yield from self.handle_chat(msg)
except LLMError as e:
    yield Error(code="LLM_ERROR", message=str(e), suggestion="check apex.json provider config")
except ContextError as e:
    yield Error(code="CONTEXT_ERROR", message=str(e), suggestion="run apex init first")
```
