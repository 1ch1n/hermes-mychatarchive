"""Hermes MyChatArchive plugin installer.

Creates a symlink (or copy on Windows) from $HERMES_HOME/plugins/mychatarchive
to the hermes_mychatarchive package directory so Hermes discovers it as a
memory provider.

Usage:
    python -m hermes_mychatarchive.install
    # or after pip install:
    hermes-mychatarchive-install
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


def _get_hermes_home() -> Path | None:
    """Return the Hermes home directory."""
    env = os.environ.get("HERMES_HOME", "").strip()
    if env:
        return Path(env)
    default = Path.home() / ".hermes"
    if default.exists():
        return default
    return None


def _get_package_dir() -> Path:
    """Return the directory containing the plugin files."""
    return Path(__file__).resolve().parent


def install() -> None:
    """Install the MyChatArchive plugin into Hermes."""
    hermes_home = _get_hermes_home()
    if not hermes_home:
        print("Hermes not found.")
        print("Expected: ~/.hermes/ or $HERMES_HOME set")
        print("Install Hermes first: https://github.com/NousResearch/hermes-agent")
        sys.exit(1)

    plugins_dir = hermes_home / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)

    target = plugins_dir / "mychatarchive"
    source = _get_package_dir()

    if target.exists() or target.is_symlink():
        print(f"Removing existing plugin at {target}")
        if target.is_symlink() or target.is_file():
            target.unlink()
        else:
            shutil.rmtree(target)

    if sys.platform == "win32":
        # Windows: copy instead of symlink (symlinks need elevated privileges)
        shutil.copytree(str(source), str(target))
        print(f"Copied plugin to {target}")
    else:
        target.symlink_to(source)
        print(f"Symlinked {target} -> {source}")

    print()
    print("MyChatArchive plugin installed.")
    print()
    print("Next steps:")
    print("  1. Populate your archive (if not already done):")
    print("       mychatarchive sync && mychatarchive embed")
    print("  2. Activate the plugin:")
    print("       hermes memory setup")
    print("     Select 'mychatarchive' from the provider list.")
    print()


if __name__ == "__main__":
    install()
