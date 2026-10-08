"""E2E: bridge connectivity — Python reaching Rust end-to-end.

The PyO3 bridge is the thin facade that lets the Python brain call the Rust
speed core. These tests prove the bridge loads, returns the exact values the
contract promises, caches the module, and fails loudly with fix instructions
when the extension is absent.
"""

from __future__ import annotations

from types import ModuleType

import pytest
from conftest import run_rust_test

from apex.bridge import FIX_INSTRUCTIONS, core_hello


def test_core_hello_returns_exact_greeting() -> None:
    """The greeting must match apex-core exactly, no drift allowed."""
    assert core_hello() == "hello from apex-core"


def test_core_version_matches_rust() -> None:
    """Python must report the same version Rust reports.

    Reads the expected version from ``Cargo.toml`` — the Rust source of
    truth that release-please updates — so that version bumps do not
    require manual test edits.
    """
    import re
    from pathlib import Path

    import apex_py

    cargo_toml = Path(__file__).resolve().parents[2] / "Cargo.toml"
    m = re.search(
        r'^version\s*=\s*"([^"]+)"',
        cargo_toml.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    assert m is not None, "version not found in Cargo.toml"
    assert apex_py.core_version() == m.group(1)


def test_rust_tests_validate_bridge_surface() -> None:
    """The Rust test suite validates the greeting the bridge exposes."""
    result = run_rust_test(filter="hello")
    assert result.returncode == 0, f"Greeting test failed:\n{result.stdout}"
    assert "test result: ok" in result.stdout


def test_bridge_error_explains_the_fix() -> None:
    """A missing extension must report exact repair commands."""
    assert "cargo build -p apex-py" in FIX_INSTRUCTIONS
    assert "scripts/sync_apex_py.py" in FIX_INSTRUCTIONS


def test_bridge_error_is_runtime_error() -> None:
    """Callers can catch ApexBridgeError via RuntimeError."""
    from apex.bridge import ApexBridgeError

    assert issubclass(ApexBridgeError, RuntimeError)


def test_bridge_loads_once_and_caches(monkeypatch: pytest.MonkeyPatch) -> None:
    """`bridge()` must call the loader exactly once, then reuse the module."""
    from apex import bridge as bridge_module

    loaded: list[ModuleType] = []

    def counting_loader() -> ModuleType:
        sentinel = ModuleType("apex_py_stub")
        loaded.append(sentinel)
        return sentinel

    monkeypatch.setattr(bridge_module, "_bridge", None)
    monkeypatch.setattr(bridge_module, "load_bridge", counting_loader)

    first = bridge_module.bridge()
    second = bridge_module.bridge()

    assert len(loaded) == 1, "loader ran more than once"
    assert second is first
