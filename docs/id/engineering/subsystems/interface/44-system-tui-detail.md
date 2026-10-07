# 44 — System: TUI Detail (TS no-build)

## Tujuan

Full lazygit-style TUI: split-panel, keyboard-first, diff per-hunk.

## Tech stack

| Komponen | Tech |
|---|---|
| Runtime | Deno (prefer) / Node 24 type-stripping |
| TUI builder | Cliffy / OpenTUI / stdlib (`[OPEN]`) |
| IPC client | JSONL stdio ke Python agent |
| Theme | Dark/light/user-defined |
| i18n | `tui/src/i18n.ts` |

## Layout struktur

```
TUI
├── main.ts          # entry point, IPC connect
├── ui.ts            # render loop, panel manager
├── ipc.ts           # JSONL client
├── protocol.ts      # mirror dari protocol.rs/py
├── i18n.ts          # string bilingual
└── theme.ts         # colors, borders
```

## Panel manager

```typescript
class PanelManager {
  panels: Panel[] = [filesPanel, chatPanel, diffPanel, terminalPanel];
  activeIndex = 0;

  focusNext() { this.activeIndex = (this.activeIndex + 1) % this.panels.length; }
  focusPrev() { this.activeIndex = (this.activeIndex - 1 + this.panels.length) % this.panels.length; }
  render() { this.panels.forEach(p => p.render()); }
}
```

## Keybinding system

```typescript
const keymaps = {
  global: {
    'ctrl+c': 'quit',
    'tab': 'focusNext',
    'shift+tab': 'focusPrev',
  },
  diffPanel: {
    'a': 'acceptHunk',
    'r': 'rejectHunk',
    'd': 'nextHunk',
    'u': 'prevHunk',
  },
  filesPanel: {
    'j': 'cursorDown',
    'k': 'cursorUp',
    'enter': 'openFile',
  },
};
```

## Diff pipeline

```typescript
function handleDiffEvent(diff: DiffEvent) {
  const hunks = splitIntoHunks(diff.old, diff.new);
  diffPanel.setHunks(hunks);
  diffPanel.activeHunk = 0;
}

function acceptHunk(index: number) {
  const hunk = diffPanel.hunks[index];
  applyHunkToFile(hunk);
  diffPanel.removeHunk(index);
  if (diffPanel.hunks.length === 0) {
    agent.notifyDiffResolved();
  }
}
```

## IPC client

```typescript
// tui/src/ipc.ts
export class IPCClient {
  constructor(private agentProcess: ChildProcess) {}

  send(request: Request) {
    this.agentProcess.stdin.write(JSON.stringify(request) + '\n');
  }

  *events(): Generator<Event> {
    for (const line of this.agentProcess.stdout) {
      yield JSON.parse(line);
    }
  }
}
```

## State sync

- TUI = client, agent = server
- TUI state: selected file, cursor panel, scroll, diff hunks
- Agent state: session history, LLM stream
- Tidak ada duplikasi state

## Render loop

```typescript
async function main() {
  const ipc = new IPCClient(spawnAgent());
  const ui = new UIManager();

  for await (const event of ipc.events()) {
    ui.handleEvent(event);
    ui.render();
  }
}
```
