"""Unit tests for ReportStore (C5) — timestamp normalization + head/tail."""

from __future__ import annotations

import json
from pathlib import Path

from ai_company.store.report_store import (
    ReportStore,
    normalize_timestamp,
)


def _write_json(path: Path, doc: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc), encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


def _mk_report(root: Path, bundle: str, ts: str, *, agent: str = "x") -> None:
    _write_json(
        root / bundle / "loop_result.json",
        {
            "task_id": bundle,
            "agent": agent,
            "timestamp": ts,
            "done": True,
        },
    )


class TestNormalizeTimestamp:
    def test_naive_assumed_utc(self) -> None:
        out = normalize_timestamp("2026-08-13T15:35:42.885519")
        assert out is not None
        assert out.tzinfo is not None
        offset = out.utcoffset()
        assert offset is not None
        assert offset.total_seconds() == 0

    def test_z_suffix(self) -> None:
        out = normalize_timestamp("2026-08-13T15:35:42Z")
        assert out is not None
        assert out.hour == 15

    def test_explicit_offset(self) -> None:
        out = normalize_timestamp("2026-08-13T15:35:42+02:00")
        assert out is not None
        offset = out.utcoffset()
        assert offset is not None
        assert offset.total_seconds() == 2 * 3600

    def test_epoch_seconds(self) -> None:
        out = normalize_timestamp(1723560000)
        assert out is not None

    def test_invalid_returns_none(self) -> None:
        assert normalize_timestamp("not-a-date") is None
        assert normalize_timestamp(None) is None
        assert normalize_timestamp(True) is None
        assert normalize_timestamp(-1) is None


class TestReportStoreBasics:
    def test_missing_root_is_empty(self, tmp_path: Path) -> None:
        store = ReportStore(tmp_path / "nope")
        assert store.reports() == []
        assert store.latest() == []
        assert store.oldest() == []

    def test_lists_datetime_mixed_order_correctly(self, tmp_path: Path) -> None:
        # Bundle names are created with intentionally unordered timestamps.
        _mk_report(tmp_path, "a", "2026-08-13T15:35:00Z")
        _mk_report(tmp_path, "b", "2026-08-14T00:00:00")  # naive, later
        _mk_report(tmp_path, "c", "2026-08-20T00:00:00+00:00")
        store = ReportStore(tmp_path)
        latest = store.latest(10)
        assert [r.name for r in latest] == ["c", "b", "a"]

    def test_latest_n(self, tmp_path: Path) -> None:
        for i in range(1, 6):
            _mk_report(tmp_path, f"r{i}", f"2026-08-{10 + i:02d}T00:00:00Z")
        store = ReportStore(tmp_path)
        latest = store.latest(2)
        assert [r.name for r in latest] == ["r5", "r4"]

    def test_oldest_n(self, tmp_path: Path) -> None:
        for i in range(1, 6):
            _mk_report(tmp_path, f"r{i}", f"2026-08-{10 + i:02d}T00:00:00Z")
        store = ReportStore(tmp_path)
        oldest = store.oldest(2)
        assert [r.name for r in oldest] == ["r1", "r2"]

    def test_filters(self, tmp_path: Path) -> None:
        _mk_report(tmp_path, "aa", "2026-08-13T00:00:00Z", agent="lead-x")
        _mk_report(tmp_path, "ab", "2026-08-14T00:00:00Z", agent="lead-y")
        _mk_report(tmp_path, "bb", "2026-08-15T00:00:00Z", agent="lead-x")
        store = ReportStore(tmp_path)
        assert [r.name for r in store.latest(10, agent="lead-x")] == ["bb", "aa"]
        assert [r.name for r in store.latest(10, bundle="aa")] == ["aa"]
        assert store.latest(10, name="missing") == []

    def test_jsonl_records(self, tmp_path: Path) -> None:
        _write_jsonl(
            tmp_path / "exp" / "run.jsonl",
            [
                {"task_id": "t1", "timestamp": "2026-08-17T14:55:00+00:00"},
                {"task_id": "t2", "timestamp": "2026-08-17T15:00:00+00:00"},
            ],
        )
        store = ReportStore(tmp_path)
        reports = store.latest(10, bundle="exp")
        assert len(reports) == 2
        assert reports[0].name == "t2"

    def test_malformed_json_skipped(self, tmp_path: Path) -> None:
        _mk_report(tmp_path, "good", "2026-08-13T10:00:00Z")
        bad_dir = tmp_path / "bad"
        bad_dir.mkdir(parents=True, exist_ok=True)
        (bad_dir / "loop_result.json").write_text("{ not json", encoding="utf-8")
        store = ReportStore(tmp_path)
        latest = store.latest(10)
        assert [r.name for r in latest] == ["good"]

    def test_no_timestamp_sorts_last(self, tmp_path: Path) -> None:
        _mk_report(tmp_path, "with_ts", "2026-08-13T00:00:00Z")
        nodir = tmp_path / "no_ts"
        _write_json(nodir / "loop_result.json", {"task_id": "no_ts"})
        store = ReportStore(tmp_path)
        i = store.reports()
        assert i[-1].name == "no_ts"
        assert i[-1].timestamp is None

    def test_to_dict_serializable(self, tmp_path: Path) -> None:
        _mk_report(tmp_path, "a", "2026-08-13T15:35:00Z")
        store = ReportStore(tmp_path)
        d = store.latest(1)[0].to_dict()
        json.dumps(d)  # must not raise


class TestReportStoreTsValues:
    def test_epoch_int(self, tmp_path: Path) -> None:
        epoch = 1723560000
        _write_json(
            tmp_path / "e" / "loop_result.json",
            {
                "task_id": "e",
                "timestamp": epoch,
            },
        )
        store = ReportStore(tmp_path)
        report = store.latest(1)[0]
        assert report.timestamp is not None
