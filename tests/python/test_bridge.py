"""Tests for the PyO3 bridge facade."""

from __future__ import annotations

from types import ModuleType

import pytest

from apex.bridge import FIX_INSTRUCTIONS, core_hello


def test_core_hello_reaches_rust() -> None:
    """The bridge returns the greeting produced by the Rust core."""
    assert core_hello() == "hello from apex-core"


def test_missing_bridge_error_explains_the_fix() -> None:
    """A missing extension reports the exact commands that repair it."""
    message = FIX_INSTRUCTIONS
    assert "cargo build -p apex-py" in message
    assert "scripts/sync_apex_py.py" in message


def test_bridge_error_is_a_runtime_error() -> None:
    """Callers can catch one specific exception type."""
    from apex.bridge import ApexBridgeError

    assert issubclass(ApexBridgeError, RuntimeError)


@pytest.mark.parametrize("attribute", ["core_hello", "ApexBridgeError", "__version__"])
def test_package_exports(attribute: str) -> None:
    """The package re-exports the bridge facade symbols."""
    import apex

    assert hasattr(apex, attribute)


def test_bridge_loads_once_and_caches(monkeypatch: pytest.MonkeyPatch) -> None:
    """`bridge()` runs the loader once and reuses that module on later calls."""
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

    assert len(loaded) == 1, "the loader ran more than once, so caching broke"
    assert second is first
