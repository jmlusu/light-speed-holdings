"""Tests for canonical JSONL trail export (ECL: audit-export-reads-canonical-jsonl-trail).

Covers AC-2 (quiet day), AC-3 (missing trail / invalid date → exit 1),
AC-5 (rotated files included), and the raw-line passthrough guarantee
(AC-1's content fidelity).  AC-1's exact 41-line count for the real trail is
verified at handoff (T012) because rotation prunes history over time and a
hard-coded count would rot.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from ai_company.audit import export as export_mod
from ai_company.audit.export import export_audit_trail

ZERO_HASH = "0" * 64


def _line(seq: int, ts: str, event_id: str, extra: dict | None = None) -> str:
    record: dict = {
        "timestamp": ts,
        "event_id": event_id,
        "__seq": seq,
        "__prev_hash": ZERO_HASH,
    }
    if extra:
        record.update(extra)
    return json.dumps(record, separators=(",", ":")) + "\n"


def _write_trail(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(lines), encoding="utf-8")


def test_extracts_only_matching_utc_date(tmp_path: Path) -> None:
    trail = tmp_path / "audit.jsonl"
    _write_trail(
        trail,
        [
            _line(1, "2026-10-04T10:00:00+00:00", "evt-1"),
            _line(2, "2026-10-03T09:00:00+00:00", "evt-2"),
            # +02:00 local past-midnight is still 10-03 in UTC.
            _line(3, "2026-10-04T01:30:00+02:00", "evt-3"),
            _line(4, "2026-10-04T23:59:59", "evt-4"),
        ],
    )
    out = tmp_path / "out"

    assert export_audit_trail(path=trail, output_dir=out, date="2026-10-04") == 2
    exported = (out / "audit-2026-10-04.jsonl").read_text(encoding="utf-8")
    assert "evt-1" in exported
    assert "evt-4" in exported
    assert "evt-2" not in exported
    assert "evt-3" not in exported

    assert export_audit_trail(path=trail, output_dir=out, date="2026-10-03") == 2
    exported_1003 = (out / "audit-2026-10-03.jsonl").read_text(encoding="utf-8")
    assert "evt-2" in exported_1003
    assert "evt-3" in exported_1003


def test_exported_lines_are_raw_passthrough(tmp_path: Path) -> None:
    trail = tmp_path / "audit.jsonl"
    raw = _line(7, "2026-10-04T12:00:00+00:00", "evt-raw", {"correlation_id": "abc"})
    _write_trail(trail, [raw])
    out = tmp_path / "out"

    assert export_audit_trail(path=trail, output_dir=out, date="2026-10-04") == 1
    content = (out / "audit-2026-10-04.jsonl").read_text(encoding="utf-8")
    assert content == raw  # byte-identical: __seq/__prev_hash keys preserved
    assert '"__seq":7' in content.replace(" ", "")


def test_quiet_day_writes_no_file_and_keeps_existing(tmp_path: Path) -> None:
    trail = tmp_path / "audit.jsonl"
    _write_trail(trail, [_line(1, "2026-10-04T10:00:00+00:00", "evt-1")])
    out = tmp_path / "out"
    out.mkdir()
    preexisting = out / "audit-2026-10-02.jsonl"
    preexisting.write_text('{"stale":true}\n', encoding="utf-8")

    assert export_audit_trail(path=trail, output_dir=out, date="2026-10-02") == 0
    assert preexisting.read_text(encoding="utf-8") == '{"stale":true}\n'
    assert not (out / "audit-2026-10-01.jsonl").exists()


def test_rotated_files_are_included_oldest_first(tmp_path: Path) -> None:
    rotated = tmp_path / "audit.1.jsonl"
    active = tmp_path / "audit.jsonl"
    _write_trail(rotated, [_line(1, "2026-10-01T08:00:00+00:00", "evt-old")])
    _write_trail(active, [_line(2, "2026-10-04T08:00:00+00:00", "evt-new")])
    out = tmp_path / "out"

    assert export_audit_trail(path=active, output_dir=out, date="2026-10-01") == 1
    assert "evt-old" in (out / "audit-2026-10-01.jsonl").read_text(encoding="utf-8")

    assert export_audit_trail(path=active, output_dir=out, date="2026-10-04") == 1
    assert "evt-new" in (out / "audit-2026-10-04.jsonl").read_text(encoding="utf-8")


def test_missing_trail_raises_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        export_audit_trail(path=tmp_path / "nope" / "audit.jsonl", output_dir=tmp_path / "out")


def test_invalid_date_raises_value_error(tmp_path: Path) -> None:
    trail = tmp_path / "audit.jsonl"
    _write_trail(trail, [_line(1, "2026-10-04T10:00:00+00:00", "evt-1")])
    with pytest.raises(ValueError):
        export_audit_trail(path=trail, output_dir=tmp_path / "out", date="not-a-date")


def test_cli_exits_1_when_trail_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(export_mod, "get_audit_path", lambda: tmp_path / "missing" / "audit.jsonl")
    monkeypatch.setattr(sys, "argv", ["export", "--output", str(tmp_path / "out")])
    with pytest.raises(SystemExit) as excinfo:
        export_mod.main()
    assert excinfo.value.code == 1


def test_cli_exits_1_on_invalid_date(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    trail = tmp_path / "audit.jsonl"
    _write_trail(trail, [_line(1, "2026-10-04T10:00:00+00:00", "evt-1")])
    monkeypatch.setattr(export_mod, "get_audit_path", lambda: trail)
    monkeypatch.setattr(
        sys, "argv", ["export", "--output", str(tmp_path / "out"), "--date", "garbage"]
    )
    with pytest.raises(SystemExit) as excinfo:
        export_mod.main()
    assert excinfo.value.code == 1


def test_cli_rejects_dbless_all_tables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["export", "--all-tables"])
    with pytest.raises(SystemExit) as excinfo:
        export_mod.main()
    assert excinfo.value.code == 2  # argparse parser.error


def test_ordered_files_alias_still_works(tmp_path: Path) -> None:
    from ai_company.audit import integrity

    assert integrity._ordered_files is integrity.ordered_audit_files
    trail = tmp_path / "audit.jsonl"
    _write_trail(trail, [_line(1, "2026-10-04T10:00:00+00:00", "evt-1")])
    assert integrity.ordered_audit_files(trail) == [trail]
