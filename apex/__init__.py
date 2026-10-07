"""Apex brain package: LLM orchestration, tools, and memory.

Importing this package does **not** import the Rust bridge. Use
`apex.bridge.core_hello()` when you need to prove the bridge is built; that
call raises `ApexBridgeError` with fix instructions when it is not.
"""

from __future__ import annotations

from apex.bridge import ApexBridgeError, core_hello

__version__ = "0.1.0"

__all__ = ["ApexBridgeError", "__version__", "core_hello"]
