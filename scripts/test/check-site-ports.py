# Checks port-assignment parity for the Marketing Site (G-6, CTO ratification 2026-10-10).
#
# Guards the boundary in AGENTS.md §12/§13 and
# docs/organization/cto-ratification-marketing-site-dashboard-boundary.md:
# Vite dev = 1441, Vite preview = 1440. vite.config.ts is the source of
# truth for what Vite binds; ecosystem.config.cjs must mirror it (PM2 `port`
# is declarative metadata, parity enforced here for frontend-only PRs that
# never run the Python test suite).
#
# Runs in the site-principles-gate workflow (stdlib only, no project deps).
# Usage:
#     python scripts/test/check-site-ports.py
# Exit code 0 = pass, 1 = violation found.

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

VITE_DEV_PORT = 1441
VITE_PREVIEW_PORT = 1440


def _read(relpath: str) -> str:
    path = ROOT / relpath
    if not path.exists():
        print(f"::error::missing required file: {relpath}")
        raise SystemExit(1)
    return path.read_text(encoding="utf-8", errors="replace")


def _fail(msg: str, errors: list[str]) -> None:
    print(f"::error::{msg}")
    errors.append(msg)


def main() -> int:
    errors: list[str] = []

    vite = _read("vite.config.ts")
    server_match = re.search(r"server:\s*\{[^}]*?port:\s*(\d+)", vite, re.DOTALL)
    preview_match = re.search(r"preview:\s*\{[^}]*?port:\s*(\d+)", vite, re.DOTALL)
    if not server_match:
        _fail("vite.config.ts: server.port not found", errors)
    elif int(server_match.group(1)) != VITE_DEV_PORT:
        _fail(
            f"vite.config.ts: server.port = {server_match.group(1)}, "
            f"expected {VITE_DEV_PORT} (Marketing Site dev)",
            errors,
        )
    if not preview_match:
        _fail("vite.config.ts: preview.port not found", errors)
    elif int(preview_match.group(1)) != VITE_PREVIEW_PORT:
        _fail(
            f"vite.config.ts: preview.port = {preview_match.group(1)}, "
            f"expected {VITE_PREVIEW_PORT} (Marketing Site preview)",
            errors,
        )

    pm2 = _read("ecosystem.config.cjs")
    dev_match = re.search(r'name:\s*"vite-dev".*?port:\s*(\d+)', pm2, re.DOTALL)
    preview_pm2_match = re.search(r'name:\s*"vite-preview".*?port:\s*(\d+)', pm2, re.DOTALL)
    if not dev_match:
        _fail("ecosystem.config.cjs: vite-dev port not found", errors)
    elif int(dev_match.group(1)) != VITE_DEV_PORT:
        _fail(
            f"ecosystem.config.cjs: vite-dev port = {dev_match.group(1)}, "
            f"expected {VITE_DEV_PORT} — PM2 metadata drifted from vite.config.ts",
            errors,
        )
    if not preview_pm2_match:
        _fail("ecosystem.config.cjs: vite-preview port not found", errors)
    elif int(preview_pm2_match.group(1)) != VITE_PREVIEW_PORT:
        _fail(
            f"ecosystem.config.cjs: vite-preview port = {preview_pm2_match.group(1)}, "
            f"expected {VITE_PREVIEW_PORT} — PM2 metadata drifted from vite.config.ts",
            errors,
        )

    # Cross-file parity: the two files must agree even if someone changes both
    # to the same wrong value — the literals above are the ratified assignments.
    if errors:
        for msg in errors:
            print(msg)
        print(f"FAIL: {len(errors)} port-assignment violation(s)")
        return 1

    print(
        f"OK: vite dev={server_match.group(1)} preview={preview_match.group(1)} "
        f"match ecosystem.config.cjs ({dev_match.group(1)}/{preview_pm2_match.group(1)})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
