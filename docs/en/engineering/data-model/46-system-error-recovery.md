# 46 — System: Error Recovery Patterns

## Pattern 1: LLM timeout → retry → fallback

```python
def chat_with_retry(prompt: str, max_retries: int = 3) -> Iterator[str]:
    for attempt in range(max_retries):
        try:
            yield from llm.stream(prompt)
            return
        except TimeoutError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # backoff
            else:
                raise
```

## Pattern 2: Skill crash → error event → agent survive

```python
def run_skill(name: str, args: list[str]) -> Iterator[AgentEvent]:
    try:
        handle = host.spawn(name, args)
        for event in handle.events():
            yield event
    except SkillCrashError as e:
        yield Error(code="SKILL_CRASH", message=str(e), suggestion="check skill entrypoint")
        # Agent tetap hidup, session lanjut
```

## Pattern 3: Context scan partial failure

```python
def scan_context(root: str) -> ContextIndex:
    entries = []
    for path in walk(root):
        try:
            entries.append(read_file_metadata(path))
        except PermissionError:
            log.warn(f"Skipped {path}: permission denied")
        except UnicodeDecodeError:
            log.warn(f"Skipped {path}: binary file")
    return ContextIndex(entries)
```

## Pattern 4: Bridge import failure

```python
# apex/bridge.py
try:
    import apex_py
except ImportError as e:
    raise ApexBridgeError(
        "apex_py not found. Run: cargo build -p apex-py && python scripts/sync_apex_py.py"
    ) from e
```

## Pattern 5: Session corrupt recovery

```python
def load_session(session_id: str) -> Session:
    try:
        return Session.from_jsonl(f".apex/sessions/{session_id}.jsonl")
    except CorruptSessionError:
        log.error(f"Session {session_id} corrupt, starting new")
        return Session.new()
```

## Pattern 6: Git not initialized

```python
def run_review():
    if not Path(".git").exists():
        yield Error(code="NO_GIT", message="Not a git repository", suggestion="run git init first")
        return
    # lanjut review
```
