#!/usr/bin/env python3
"""Site Principles Gate: reject fake-success form states (Guiding Principles §10).

Enforces: "Never show a success state unless the enquiry has actually been sent
and recorded." A component that flips a *Submitted/success flag to true must
contain a real network send (fetch/axios/FormData+XHR to a backend), otherwise
the success UI is a fake the visitor could never have triggered.

Scans the client-facing SPA only: src/components and src/pages. The internal
product/dashboard (src/ai_company) is out of scope and never scanned.

Usage:
    python scripts/check-site-form-backend.py
Exit code 0 = pass, 1 = violation found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = (ROOT / "src" / "components", ROOT / "src" / "pages")
# A success-state toggle that must be backed by a real send in the same file.
SUBMIT_TOGGLE = re.compile(r"set\w*[Ss]ubmitted\s*\(\s*[Tt]rue\s*\)")
# Real network-send primitives (any one in the file satisfies the guard).
SEND_MARKERS = re.compile(
    r"fetch\s*\(|axios|XMLHttpRequest|/api/|new\s+Request\s*\(|navigator\.sendBeacon"
)


def main() -> int:
    violations: list[tuple[str, int]] = []
    for base in SCAN_DIRS:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.tsx")):
            text = path.read_text(encoding="utf-8", errors="replace")
            hits = list(SUBMIT_TOGGLE.finditer(text))
            if not hits:
                continue
            if SEND_MARKERS.search(text):
                continue
            for hit in hits:
                line = text.count("\n", 0, hit.start()) + 1
                violations.append((str(path.relative_to(ROOT)), line))

    if violations:
        print("::error::Guiding Principles §10 violated — success state with no backend send:")
        for rel, line in violations:
            print(
                f"  {rel}:{line} — toggles a *Submitted(success) state with no fetch/axios/api call in the file"
            )
        return 1

    print("OK: every success-state toggle in the public site is backed by a real send.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
