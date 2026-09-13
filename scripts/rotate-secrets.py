#!/usr/bin/env python3
"""
Rotate a placeholder API key.

Generates a new cryptographically secure key with ``secrets.token_urlsafe(32)``
and prints it together with rotation instructions.  The script is intentionally
read-only against the environment: it never writes to ``.env`` files or any
other config, so the operator decides where the new key goes.

Usage:
    python scripts/rotate-secrets.py                # rotate default placeholder
    python scripts/rotate-secrets.py --name GITHUB_TOKEN
"""

from __future__ import annotations

import argparse
import secrets
import sys


def _rotate(name: str) -> str:
    """Generate a new placeholder API key and print rotation instructions."""
    new_key = secrets.token_urlsafe(32)

    lines = [
        f"Rotated placeholder API key for: {name}",
        "",
        f"New key: {new_key}",
        "",
        "Next steps (manual, do NOT auto-persist):",
        "  1. Update the secret in your secret store / .env file.",
        "  2. Rotate any references in CI/CD variables.",
        "  3. Revoke the previous key once the new one is verified.",
        "",
        "Security notes:",
        f"  - Generated with secrets.token_urlsafe(32) ({len(new_key)} chars, ~256 bits).",
        "  - This script does not persist the key anywhere.",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--name",
        default="PLACEHOLDER_API_KEY",
        help="Name of the secret being rotated (default: PLACEHOLDER_API_KEY)",
    )
    args = parser.parse_args()

    print(_rotate(args.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
