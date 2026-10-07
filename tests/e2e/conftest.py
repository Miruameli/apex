"""Shared fixtures and subprocess helpers for E2E tests.

These helpers let every E2E test exercise the full stack — Rust, Python,
and TypeScript — rather than calling internals in-process. The protocol
contract is only meaningful when all three languages agree, so the tests
spawn each language's toolchain and compare results.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "protocol"
CLI_BIN = REPO_ROOT / "target" / "debug" / "apex"
DENO_DIR = REPO_ROOT / "tui"


def fixture_files(subdir: str) -> list[Path]:
    """Return sorted JSON fixture paths under a protocol subdirectory."""
    directory = FIXTURES / subdir
    return sorted(directory.glob("*.json")) if directory.exists() else []


def run_rust_test(filter: str | None = None) -> subprocess.CompletedProcess:
    """Run the Rust workspace test suite, optionally filtered to a substring."""
    argv = ["uv", "run", "cargo", "test", "--workspace"]
    if filter is not None:
        argv += ["--", filter]
    return subprocess.run(
        argv,
        capture_output=True,
        text=True,
        timeout=180,
        cwd=REPO_ROOT,
        check=False,
    )


def run_ts_test() -> subprocess.CompletedProcess:
    """Run the TypeScript test suite via deno."""
    return subprocess.run(
        ["deno", "test", "--allow-all", "src/"],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=DENO_DIR,
        check=False,
    )


def run_cli(args: list[str], timeout: int = 30) -> subprocess.CompletedProcess:
    """Run the apex CLI binary with arguments, returning the result."""
    env = dict(os.environ)
    env["RUST_BACKTRACE"] = "1"
    if not CLI_BIN.exists():
        pytest.skip(f"CLI binary not found at {CLI_BIN}; run ./scripts/build.sh")
    return subprocess.run(
        [str(CLI_BIN)] + args,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
        cwd=REPO_ROOT,
        check=False,
    )


@pytest.fixture(scope="session")
def request_fixtures() -> list[Path]:
    """All request fixture files."""
    return fixture_files("requests")


@pytest.fixture(scope="session")
def event_fixtures() -> list[Path]:
    """All event fixture files (stream + terminal)."""
    return fixture_files("events/stream") + fixture_files("events/terminal")


def pytest_generate_tests(metafunc):
    """Parametrize tests that request individual fixtures by path."""
    if "request_fixture" in metafunc.fixturenames:
        paths = fixture_files("requests")
        metafunc.parametrize("request_fixture", paths, ids=lambda p: p.name)
    if "event_fixture" in metafunc.fixturenames:
        paths = fixture_files("events/stream") + fixture_files("events/terminal")
        metafunc.parametrize("event_fixture", paths, ids=lambda p: p.name)
