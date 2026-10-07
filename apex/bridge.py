"""Facade over the compiled Rust `apex_py` extension.

Importing `apex` must fail loudly when the bridge is missing. A silent
pure-Python fallback would let a broken build look healthy, which is exactly
the kind of drift this project forbids.
"""

from __future__ import annotations

import importlib
from types import ModuleType

# Instructions shown when the compiled extension is unavailable.
FIX_INSTRUCTIONS = (
    "Apex bridge (apex_py) is not built.\n"
    "Fix:\n"
    "  cargo build -p apex-py\n"
    "  uv run python scripts/sync_apex_py.py"
)


class ApexBridgeError(RuntimeError):
    """Raisen when the compiled Rust extension cannot be loaded."""


def load_bridge() -> ModuleType:
    """Return the `apex_py` extension module.

    Returns:
        The imported extension module.

    Raises:
        ApexBridgeError: If the extension is missing or broken.
    """
    try:
        return importlib.import_module("apex_py")
    except ImportError as error:  # pragma: no cover - depends on build state
        raise ApexBridgeError(f"{FIX_INSTRUCTIONS}\n\nCause: {error}") from error


_bridge: ModuleType | None = None


def bridge() -> ModuleType:
    """Return the cached bridge module, loading it on first use."""
    global _bridge
    if _bridge is None:
        _bridge = load_bridge()
    return _bridge


def core_hello() -> str:
    """Return the greeting from the Rust core, proving the bridge works."""
    return str(bridge().core_hello())
