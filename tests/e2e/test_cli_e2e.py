"""E2E: CLI binary behavior as a spawned subprocess.

Each subcommand must exit 0 (even as a stub) and produce a recognizable
message on stderr. stdout stays clean per the IPC contract: human-facing
output goes to stderr, so pipeline consumers only ever see JSONL.
"""

from __future__ import annotations

from conftest import run_cli


def test_cli_help_exits_zero() -> None:
    """`apex --help` must succeed and list known subcommands."""
    result = run_cli(["--help"])
    assert result.returncode == 0
    assert "chat" in result.stdout
    assert "review" in result.stdout
    assert "skill" in result.stdout


def test_cli_no_args_prints_phase3() -> None:
    """Bare invocation prints the phase-3 placeholder on stderr."""
    result = run_cli([])
    assert result.returncode == 0
    assert "not implemented yet (phase 3)" in result.stderr


def test_cli_chat_stub_exits_zero() -> None:
    """`apex chat` must exit 0 and warn on stderr."""
    result = run_cli(["chat"])
    assert result.returncode == 0
    assert "not implemented yet" in result.stderr


def test_cli_review_stub_exits_zero() -> None:
    """`apex review` must exit 0; path is accepted but unimplemented."""
    result = run_cli(["review", "crates/apex-core/src"])
    assert result.returncode == 0
    assert "not implemented yet" in result.stderr


def test_cli_skill_list_exits_zero() -> None:
    """`apex skill list` must exit 0."""
    result = run_cli(["skill", "list"])
    assert result.returncode == 0
    assert "not implemented yet" in result.stderr


def test_cli_context_stub_exits_zero() -> None:
    """`apex context` must exit 0."""
    result = run_cli(["context"])
    assert result.returncode == 0
    assert "not implemented yet" in result.stderr
