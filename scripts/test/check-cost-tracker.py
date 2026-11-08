#!/usr/bin/env python3
"""Guard: data/orchestrator/cost_tracker.json must not carry fake spend data.

Incident: PR #565 committed a dummy block into the tracked cost tracker
(call_count=2, gpt-4 / live_tracking, $0.0264, prompt 220 / completion 330,
daily_trend 2026-11-08) with no ``by_source`` source tag. The file is the
dashboard's single source of truth for LLM spend (CostTracker export), so an
untagged non-zero block is indistinguishable from real spend on the
dashboard and must fail the gate.

Rule:
  - Zero state (call_count=0, totals 0, empty breakdowns) -> OK.
  - Non-zero data WITH a ``by_source`` source tag (real ``sync-opencode``
    export) -> OK, provided completeness holds (see below).
  - Non-zero data WITHOUT a source tag (missing or empty ``by_source``)
    -> FAIL. This is the dummy signature and must never merge.

Completeness (sourced non-zero spend only):
  - ``call_count`` must equal the line count of ``results/cost_log.jsonl``,
    resolved as ``../.. /results/cost_log.jsonl`` from ``data/orchestrator``
    (i.e. ``<repo-root>/results/cost_log.jsonl`` for the default path) or via
    an explicit ``--log-path`` override.
  - Log missing while sourced spend is present -> FAIL (truncated export).
  - Line-count mismatch -> FAIL (truncated export).
  - Zero state skips the completeness check.

Usage:
    python scripts/test/check-cost-tracker.py
    python scripts/test/check-cost-tracker.py --path <json-file>
    python scripts/test/check-cost-tracker.py --path <json-file> --log-path <jsonl-file>

Exit 0 = safe; exit 1 = dummy/untagged spend or truncated/incomplete export.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PATH = REPO_ROOT / "data" / "orchestrator" / "cost_tracker.json"


def _fnum(value: object) -> float:
    """Best-effort numeric coercion (invalid values count as anomalous)."""
    try:
        return float(value) if value is not None else 0.0
    except (TypeError, ValueError):
        return 0.0


def _default_log_path(path: Path) -> Path:
    """Resolve ``results/cost_log.jsonl`` relative to the tracker ``--path``.

    For the default ``data/orchestrator/cost_tracker.json`` the results dir is
    ``../.. /results`` from ``data/orchestrator`` (i.e. the repo root), so the
    log is ``<repo-root>/results/cost_log.jsonl``. From the tracker file that
    is three levels up (file -> orchestrator -> data -> repo root).
    """
    return path.resolve().parents[2] / "results" / "cost_log.jsonl"


def _count_log_lines(log_path: Path) -> int:
    """Count lines in the cost log (one JSON object per line)."""
    total = 0
    with log_path.open(encoding="utf-8") as handle:
        for _line in handle:
            total += 1
    return total


def _check(path: Path, log_path: Path | None = None) -> tuple[bool, list[str]]:
    """Return (passed, report lines) for the given JSON path."""
    if not path.is_file():
        return False, [
            f"FAIL: {path} is missing - the committed file must exist and "
            "report zero state (do not delete it; the dashboard reads zeros)."
        ]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return False, [f"FAIL: {path} is not valid JSON: {exc}"]

    call_count = _fnum(data.get("call_count"))
    total_spent = _fnum(data.get("total_spent", data.get("total_cost_usd")))
    total_tokens = _fnum(data.get("total_tokens"))
    by_source = data.get("by_source")
    has_source_tag = isinstance(by_source, dict) and len(by_source) > 0

    is_zero = (
        call_count == 0
        and total_spent == 0
        and total_tokens == 0
        and not data.get("by_model")
        and not data.get("by_agent")
        and not data.get("by_source")
    )

    if is_zero:
        return True, [f"OK: {path} is zero state (call_count=0, totals 0, no breakdowns)."]

    if not has_source_tag:
        lines = [
            "FAIL: cost_tracker.json has non-zero spend without a "
            "`by_source` source tag (dummy signature, PR #565):"
        ]
        lines.append(f"  - call_count={call_count:g}")
        lines.append(f"  - total_spent={total_spent:g}")
        lines.append(f"  - total_tokens={total_tokens:g}")
        lines.append(f"  - by_source={'missing' if by_source is None else 'empty'}")
        if data.get("by_model"):
            lines.append(f"  - by_model={json.dumps(data['by_model'])}")
        if data.get("by_agent"):
            lines.append(f"  - by_agent={json.dumps(data['by_agent'])}")
        lines.append(
            "  Regenerate zeros with an empty CostTracker (no real sync "
            "data) or export real data with sync-opencode so `by_source` "
            "carries the source."
        )
        return False, lines

    effective_log = log_path if log_path is not None else _default_log_path(path)
    if not effective_log.is_file():
        return False, [
            f"FAIL: {path} carries sourced spend "
            f"(call_count={call_count:g}, total_spent={total_spent:g}, "
            f"by_source={sorted(by_source)}) but cost log "
            f"{effective_log} is missing - truncated export. A sourced "
            "export is only complete when results/cost_log.jsonl holds one "
            "line per call (call_count == log lines); regenerate a full "
            "sync-opencode export or a zero-state tracker."
        ]
    try:
        log_lines = _count_log_lines(effective_log)
    except (OSError, UnicodeDecodeError) as exc:
        return False, [
            f"FAIL: could not count lines in cost log {effective_log}: {exc} - "
            "truncated export; regenerate a full sync-opencode export."
        ]
    if call_count != log_lines:
        return False, [
            f"FAIL: {path} call_count={call_count:g} does not match cost log "
            f"{effective_log} line count ({log_lines}) - truncated export. "
            "call_count must equal the results/cost_log.jsonl line count; "
            "regenerate a full sync-opencode export or a zero-state tracker."
        ]
    return True, [
        f"OK: {path} carries sourced spend "
        f"(call_count={call_count:g}, total_spent={total_spent:g}, "
        f"by_source={sorted(by_source)}). Log complete: call_count="
        f"{call_count:g} matches {effective_log} lines={log_lines}."
    ]


def main(argv: list[str]) -> int:
    path = DEFAULT_PATH
    log_path: Path | None = None
    args = argv[1:]
    if "--path" in args:
        idx = args.index("--path")
        if idx + 1 >= len(args):
            print("FAIL: --path requires a file argument")
            return 1
        path = Path(args[idx + 1])
    if "--log-path" in args:
        idx = args.index("--log-path")
        if idx + 1 >= len(args):
            print("FAIL: --log-path requires a file argument")
            return 1
        log_path = Path(args[idx + 1])
    passed, lines = _check(path, log_path)
    for line in lines:
        print(line)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
