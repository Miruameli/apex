# 49 — CLI Command Surface (final)

> Bentuk final: `apex <command> [subcommand] [flags]`. `apex` tanpa argumen = launch TUI (seperti omp).

## Command utama

| Command | Subcommand | Deskripsi |
|---|---|---|
| `apex` | — | Launch TUI (default) |
| `apex chat` | — | Chat langsung (no TUI) |
| `apex context` | — | Scan codebase |
| `apex review` | — | Review diff |
| `apex commit` | — | Atomic commit |
| `apex ship` | — | PR + changelog |
| `apex skill` | `add` / `list` / `run` / `validate` / `remove` | Skill management |
| `apex config` | — | Edit/view apex.json |
| `apex init` | — | Init project |
| `apex undo` | — | Rollback last edit |
| `apex tui` | — | Explicit launch TUI |

## Flag global

| Flag | Deskripsi |
|---|---|
| `--config <path>` | Path custom ke apex.json |
| `--verbose` / `-v` | Debug log ke stderr |
| `--quiet` / `-q` | Output essential saja |
| `--json` | Machine-readable JSON output |
| `--lang <id/en>` | Override bahasa UI |
| `--no-approval` | Skip approval (HANYA untuk auto-test) |

## Subcommand detail

### `apex skill add <name>`

```sh
apex skill add vercel-deploy
# scaffold: skills/vercel-deploy/{SKILL.md, apex.skill.json, main.py}
```

### `apex skill run <name> [-- <args>]`

```sh
apex skill run vercel-deploy -- --env production
```

### `apex review [--staged | --branch <name>]`

```sh
apex review --staged
apex review --branch feature/auth
```

### `apex commit [--message <msg>]`

```sh
apex commit                    # generate dari diff
apex commit -m "feat: add auth" # manual override
```

### `apex ship [--push]`

```sh
apex ship              # buat PR, no push
apex ship --push       # push + buat PR
```

## Clap derive draft

```rust
#[derive(Parser)]
#[command(name = "apex", version, about)]
struct Cli {
    #[command(subcommand)]
    command: Option<Commands>,

    #[arg(long, global = true)]
    config: Option<PathBuf>,
    #[arg(short, long, global = true)]
    verbose: bool,
    #[arg(short, long, global = true)]
    quiet: bool,
    #[arg(long, global = true)]
    json: bool,
}

#[derive(Subcommand)]
enum Commands {
    Chat { message: Vec<String> },
    Context { root: Option<PathBuf> },
    Review { #[arg(long)] staged: bool, #[arg(long)] branch: Option<String> },
    Commit { #[arg(short, long)] message: Option<String> },
    Ship { #[arg(long)] push: bool },
    Skill { #[command(subcommand)] action: SkillAction },
    Config,
    Init,
    Undo,
    Tui,
}
```
