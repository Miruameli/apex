#!/usr/bin/env python3
"""Copy the compiled PyO3 extension into the active virtual environment.

Why this exists: `apex-py` builds a cdylib that Python can only import when it
sit inside site-packages. Copying it explicitly keeps the build step visible
and keeps the artifact out of the repository root, where it would shadow the
real package.

The script fails loudly. A missing build artifact is a build problem, and
silently skipping the copy would hide it behind a slower fallback.

Usage:
    uv run python scripts/sync_apex_py.py [--release] [--target <triple>]
"""

from __future__ import annotations

import argparse
import shutil
import sysconfig
from pathlib import Path

# Shared object suffixes per platform, most likely first.
LIBRARY_SUFFIXES = (".so", ".dylib", ".dll")

# Crate name of the PyO3 extension module, matching `crates/apex-py/Cargo.toml`.
MODULE_NAME = "apex_py"


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--release", action="store_true", help="use target/release")
    mode.add_argument("--target", help="explicit target directory name")
    return parser.parse_args()


def locate_artifact(profile: str, target_triple: str | None) -> Path:
    """Return the built library, or explain which build is missing."""
    directory = Path("target") / (target_triple or profile)

    for suffix in LIBRARY_SUFFIXES:
        candidate = directory / f"lib{MODULE_NAME}{suffix}"
        if candidate.exists():
            return candidate

    build_command = (
        f"cargo build -p apex-py --target {target_triple}"
        if target_triple
        else f"cargo build -p apex-py{' --release' if profile == 'release' else ''}"
    )
    raise SystemExit(
        f"error: no built library for '{MODULE_NAME}' in {directory}\n"
        f"hint: run '{build_command}' first."
    )


def destination_path(library: Path) -> Path:
    """Return the site-packages path Python expects for this interpreter.

    The suffix must match ``EXT_SUFFIX`` (``.cpython-312-<platform>.so`` on
    CPython). A hand-built tag is not importable, so read it from the running
    interpreter instead of guessing.
    """
    extension_suffix = sysconfig.get_config_var("EXT_SUFFIX") or library.suffix
    return Path(sysconfig.get_paths()["purelib"]) / f"{MODULE_NAME}{extension_suffix}"


def main() -> int:
    """Copy the artifact and report both paths."""
    arguments = parse_arguments()
    profile = "release" if arguments.release else "debug"
    library = locate_artifact(profile, arguments.target)
    destination = destination_path(library)

    shutil.copy2(library, destination)
    print(f"synced: {library} -> {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
