#!/usr/bin/env python3
"""Verify that the version string is consistent across all three language manifests.

In a polyglot repo, a version mismatch between Cargo.toml, pyproject.toml,
and tui/deno.json is a release blocker. This checker reads each manifest,
extracts its version, and fails if they disagree.

Usage:
    uv run python scripts/checks/check_versions.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# (label, file path, version regex — first capture group is the version)
MANIFESTS = [
    ("Cargo.toml", "Cargo.toml", r'version\s*=\s*"([^"]+)"'),
    ("pyproject.toml", "pyproject.toml", r'^version\s*=\s*"([^"]+)"'),
    ("tui/deno.json", "tui/deno.json", r'"version"\s*:\s*"([^"]+)"'),
]


def extract_version(file_path: Path, pattern: str) -> str:
    """Return the first version match in *file_path* or raise on miss."""
    text = file_path.read_text(encoding="utf-8")
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        raise FileNotFoundError(f"version not found in {file_path}")
    return match.group(1)


def main() -> int:
    """Compare versions across manifests and report any mismatch."""
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    versions: dict[str, str] = {}

    for label, rel_path, pattern in MANIFESTS:
        path = root / rel_path
        if not path.exists():
            print(f"error: {label} not found at {rel_path}")
            return 1
        versions[label] = extract_version(path, pattern)

    unique = set(versions.values())
    if len(unique) != 1:
        print("Version mismatch detected:\n")
        for label, version in versions.items():
            print(f"  {label}: {version}")
        print(f"\nAll must match. Found {len(unique)} distinct versions.")
        return 1

    version = unique.pop()
    print(f"Version consistent across all manifests: {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
