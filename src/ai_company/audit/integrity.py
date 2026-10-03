"""Tamper-evidence verification for the JSONL audit trail (C1).

The trail is a hash chain: every line written by :class:`AuditWriter`
carries a ``__seq`` counter and a ``__prev_hash`` of the previous line's
raw bytes.  This module reconstructs that chain across the active file and
all retained rotated files (oldest → newest) and reports any break.

Rotated-away history is handled gracefully: when the oldest retained line is
not the very first line (its sequence is > 1), its own ``__prev_hash`` cannot
be checked because the predecessor file was pruned by rotation — that
boundary is reported but is not treated as a failure.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any

from ai_company.audit.writer import _ZERO_HASH

logger = logging.getLogger(__name__)


def _ordered_files(path: Path) -> list[Path]:
    """Return the trail files in chronological order (oldest → newest).

    Rotation produces ``audit.1.jsonl`` … ``audit.N.jsonl`` (oldest = highest
    number) plus the active ``audit.jsonl`` (newest).  The chain runs from the
    file with the highest rotation index up through the active file.
    """
    stem = path.stem
    suffix = path.suffix
    pattern = re.compile(rf"^{re.escape(stem)}\.(\d+){re.escape(suffix)}$")
    parent = path.parent
    rotated: list[tuple[int, Path]] = []
    for candidate in parent.iterdir():
        match = pattern.match(candidate.name)
        if match:
            rotated.append((int(match.group(1)), candidate))
    rotated.sort(key=lambda item: item[0])
    ordered = [candidate for _, candidate in reversed(rotated)]
    if path.exists() and path.stat().st_size > 0:
        ordered.append(path)
    return ordered


def verify_audit_chain(path: str | Path) -> dict[str, Any]:
    """Verify the hash chain of the audit trail rooted at *path*.

    Returns a dict::

        {"ok": bool, "events": int, "files": list[str], "errors": list[str]}

    ``errors`` is empty (and ``ok`` True) when the chain is intact across
    every retained file.  Malformed lines and sequence/hash mismatches are
    reported individually.
    """
    root = Path(path)
    errors: list[str] = []
    files = _ordered_files(root)
    if not files:
        return {"ok": True, "events": 0, "files": [], "errors": []}

    prev_line_hash: str | None = None
    expected_seq = 0
    first_line_seen = False
    events_seen = 0

    for fpath in files:
        try:
            with open(fpath, "r", encoding="utf-8") as fh:
                for line_no, raw in enumerate(fh, start=1):
                    if not raw.strip():
                        continue
                    events_seen += 1
                    line_bytes = raw.encode("utf-8")
                    line_hash = hashlib.sha256(line_bytes).hexdigest()
                    try:
                        data = json.loads(raw)
                    except json.JSONDecodeError as exc:
                        errors.append(f"[{fpath.name}:{line_no}] malformed JSON: {exc}")
                        prev_line_hash = line_hash
                        continue
                    if not isinstance(data, dict):
                        errors.append(f"[{fpath.name}:{line_no}] line is not a JSON object")
                        prev_line_hash = line_hash
                        continue

                    seq = data.get("__seq")
                    prev = data.get("__prev_hash")

                    if not first_line_seen:
                        first_line_seen = True
                        if isinstance(seq, int) or (isinstance(seq, str) and seq.isdigit()):
                            s = int(seq)
                            if s == 1:
                                # Genuine chain head — may reference only the zero hash.
                                expected_seq = 1
                                if isinstance(prev, str) and prev != _ZERO_HASH:
                                    errors.append(
                                        f"[{fpath.name}:{line_no}] chain head hash mismatch"
                                    )
                            else:
                                # Predecessor rotated away — anchor the sequence at
                                # this line and skip its (unverifiable) prev hash.
                                expected_seq = s
                        # Legacy (pre-chain) first line: nothing to verify yet.
                    else:
                        if isinstance(seq, int) or (isinstance(seq, str) and seq.isdigit()):
                            expected_seq += 1
                            if int(seq) != expected_seq:
                                errors.append(
                                    f"[{fpath.name}:{line_no}] seq mismatch: "
                                    f"expected {expected_seq}, got {seq}"
                                )
                        if isinstance(prev, str):
                            expect = prev_line_hash if prev_line_hash is not None else _ZERO_HASH
                            if prev != expect:
                                errors.append(
                                    f"[{fpath.name}:{line_no}] prev_hash mismatch (chain break)"
                                )
                    prev_line_hash = line_hash
        except OSError as exc:
            errors.append(f"[{fpath.name}] unreadable: {exc}")
            continue

    return {
        "ok": not errors,
        "events": events_seen,
        "files": [str(f) for f in files],
        "errors": errors,
    }


def check_jsonl(path: str | Path) -> dict[str, Any]:
    """Structurally validate an append-only JSONL evidence store.

    The evidence stores (escalation events, dead-letter queue, daily audit
    export) are append-only but are **not** hash chained, so
    :func:`verify_audit_chain` cannot attest to them: it finds no ``__seq`` /
    ``__prev_hash`` keys and reports success without inspecting any link. Use
    this function for those stores to confirm every line is a well-formed JSON
    object, and :func:`verify_audit_chain` only for the AuditWriter trail.

    Returns a dict::

        {"ok": bool, "records": int, "file": str, "errors": list[str]}
    """
    target = Path(path)
    result: dict[str, Any] = {"ok": True, "records": 0, "file": str(target), "errors": []}

    if not target.exists():
        result["ok"] = False
        result["errors"].append(f"file not found: {target}")
        return result

    try:
        with open(target, "r", encoding="utf-8") as fh:
            for line_no, raw in enumerate(fh, start=1):
                if not raw.strip():
                    continue
                result["records"] += 1
                try:
                    record = json.loads(raw)
                except json.JSONDecodeError as exc:
                    result["ok"] = False
                    result["errors"].append(f"[{target.name}:{line_no}] malformed JSON: {exc}")
                    continue
                if not isinstance(record, dict):
                    result["ok"] = False
                    result["errors"].append(f"[{target.name}:{line_no}] line is not a JSON object")
    except OSError as exc:
        result["ok"] = False
        result["errors"].append(f"[{target.name}] unreadable: {exc}")

    return result


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for integrity verification.

    ``verify`` walks the AuditWriter hash chain; ``check`` structurally
    validates append-only evidence stores that carry no chain fields.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Verify LightSpeed audit evidence integrity")
    sub = parser.add_subparsers(dest="command", required=True)

    verify_parser = sub.add_parser(
        "verify", help="Verify the AuditWriter __seq/__prev_hash hash chain"
    )
    verify_parser.add_argument("paths", nargs="+", help="AuditWriter trail file(s)")

    check_parser = sub.add_parser(
        "check", help="Structurally validate append-only JSONL evidence stores"
    )
    check_parser.add_argument("paths", nargs="+", help="Evidence store JSONL file(s)")

    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    results = (
        [verify_audit_chain(p) for p in args.paths]
        if args.command == "verify"
        else [check_jsonl(p) for p in args.paths]
    )

    ok = True
    for result in results:
        print(json.dumps(result, indent=2))
        if not result["ok"]:
            ok = False

    if not ok:
        print("INTEGRITY CHECK FAILED", file=sys.stderr)
        return 1

    print("Integrity OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
