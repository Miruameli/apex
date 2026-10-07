#!/usr/bin/env python3
"""Enforce the Apex modularization rules across the repository.

The rules are the reason the codebase stays navigable:

1. At most 5 direct files per folder — otherwise create a subfolder.
2. At most 5 direct subfolders per folder — otherwise split the domain.
3. At most 150 source lines of code per file — otherwise split the file.

Repository-root manifests are exempt from rule 1 because tooling requires
them at fixed paths (``Cargo.toml``, ``pyproject.toml``, ``package.json``).
Generated and vendored directories are skipped entirely.

Usage:
    uv run python scripts/checks/check_modularization.py [root]
"""

from __future__ import annotations

import sys
from pathlib import Path

# Maximum direct files allowed in one folder.
MAX_FILES_PER_FOLDER = 5

# Maximum direct subfolders allowed in one folder.
MAX_SUBFOLDERS_PER_FOLDER = 5

# Maximum source lines of code allowed in one file.
MAX_SLOC_PER_FILE = 150

# Extensions counted as source code for the SLOC rule.
SOURCE_SUFFIXES = frozenset({".rs", ".py", ".ts"})

# Directories holding generated output, caches, or vendored dependencies.
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
        "deno_ast",
        "dist",
    }
)

# Folders exempt from the direct-file rule.
EXEMPT_FOLDERS = frozenset({"."})


def is_ignored(path: Path) -> bool:
    """Report whether any path component is an ignored directory."""
    return bool(IGNORED_DIRECTORIES.intersection(path.parts))


def source_lines(source_file: Path) -> int:
    """Count non-blank, non-comment lines in a source file."""
    count = 0
    for raw_line in source_file.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith(("//", "#", "//!", "///")):
            continue
        count += 1
    return count


def check_folders(root: Path) -> list[str]:
    """Return violations for the direct-file and direct-subfolder rules."""
    violations: list[str] = []

    for folder in sorted(path for path in root.rglob("*") if path.is_dir()):
        if is_ignored(folder):
            continue

        files = [item for item in folder.iterdir() if item.is_file()]
        subfolders = [item for item in folder.iterdir() if item.is_dir()]

        if (
            str(folder.relative_to(root)) not in EXEMPT_FOLDERS
            and len(files) > MAX_FILES_PER_FOLDER
        ):
            violations.append(
                f"{folder.relative_to(root)}: {len(files)} direct files "
                f"(max {MAX_FILES_PER_FOLDER})"
            )
        # Exempt repo root (.) and docs/ from subfolder limit: workspace configs and language mirrors must live here
        if len(subfolders) > MAX_SUBFOLDERS_PER_FOLDER and str(folder.relative_to(root)) not in {
            ".",
            "docs",
        }:
            violations.append(
                f"{folder.relative_to(root)}: {len(subfolders)} direct subfolders "
                f"(max {MAX_SUBFOLDERS_PER_FOLDER})"
            )
    return violations


def check_source_files(root: Path) -> list[str]:
    """Return violations for the per-file SLOC rule."""
    violations: list[str] = []

    for source_file in sorted(root.rglob("*")):
        if not source_file.is_file() or source_file.suffix not in SOURCE_SUFFIXES:
            continue
        if is_ignored(source_file.relative_to(root)):
            continue

        lines = source_lines(source_file)
        if lines > MAX_SLOC_PER_FILE:
            violations.append(
                f"{source_file.relative_to(root)}: {lines} SLOC (max {MAX_SLOC_PER_FILE})"
            )

    return violations


def main() -> int:
    """Run every modularization check and report the result."""
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    violations = check_folders(root) + check_source_files(root)

    if violations:
        print("Modularization violations found:\n")
        for violation in violations:
            print(f"  {violation}")
        print(f"\nTotal: {len(violations)}")
        return 1

    print(
        f"Modularization OK (max {MAX_FILES_PER_FOLDER} files/folder, "
        f"max {MAX_SUBFOLDERS_PER_FOLDER} subfolders/folder, "
        f"max {MAX_SLOC_PER_FILE} SLOC/file)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
