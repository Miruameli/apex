#!/usr/bin/env python3
"""Verify every relative Markdown link in the repository resolves.

Broken links silently rot documentation. This checker makes that failure
explicit and exits non-zero so CI blocks the change.

Rules:
- Relative links only. ``http``, ``https``, ``mailto``, and ``#anchor`` are
  skipped because they are not verifiable offline.
- Fragment anchors are not resolved; only the target file must exist.
- Generated or vendored directories are ignored.

Usage:
    uv run python scripts/checks/check_docs_links.py [root]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Directories that hold generated output or vendored dependencies.
IGNORED_DIRECTORIES = frozenset(
    {
        ".git",
        ".venv",
        "target",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        "dist",
    }
)

# Matches the target of an inline Markdown link: [label](target).
LINK_PATTERN = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


def is_ignored(path: Path) -> bool:
    """Report whether any path component is an ignored directory."""
    return bool(IGNORED_DIRECTORIES.intersection(path.parts))


def check_markdown_file(file_path: Path, root: Path) -> list[str]:
    """Return unresolved links found in one Markdown file."""
    violations: list[str] = []
    text = file_path.read_text(encoding="utf-8")

    for _label, target in LINK_PATTERN.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        # Strip fragment for file resolution.
        file_target = target.split("#")[0]
        if not file_target:
            continue

        resolved = (file_path.parent / file_target).resolve()
        if not resolved.exists():
            violations.append(
                f"{file_path.relative_to(root)}: link target '{target}' "
                f"does not resolve to {resolved.relative_to(root)}"
            )

    return violations


def main() -> int:
    """Check every Markdown file and report broken links."""
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    violations: list[str] = []

    for file_path in sorted(root.rglob("*.md")):
        if is_ignored(file_path.relative_to(root)):
            continue
        violations.extend(check_markdown_file(file_path, root))

    if violations:
        print("Broken documentation links found:\n")
        for violation in violations:
            print(f"  {violation}")
        print(f"\nTotal: {len(violations)}")
        return 1

    print("Documentation links OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
