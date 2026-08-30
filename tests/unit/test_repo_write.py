"""Tests for the guarded repo-write primitive (lock + CAS + ownership)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_company.store.repo_write import (
    RepoWriteConflict,
    read_file,
    set_owner_registry,
    sha256_digest,
    write_file,
)


class TestReadDigest:
    def test_missing_file_returns_none(self, tmp_path: Path) -> None:
        target = tmp_path / "missing.txt"
        assert read_file(target) == (None, None)
        assert sha256_digest(target) is None

    def test_content_and_digest(self, tmp_path: Path) -> None:
        target = tmp_path / "a.txt"
        target.write_text("hello", encoding="utf-8")
        content, digest = read_file(target)
        assert content == "hello"
        assert digest == sha256_digest(target)
        assert len(digest) == 64


class TestWriteFileBasic:
    def test_writes_and_returns_hashes(self, tmp_path: Path) -> None:
        target = tmp_path / "b.txt"
        result = write_file(target, "first")
        assert result["conflict"] is False
        assert result["owner_conflict"] is False
        assert result["before_hash"] is None  # file did not exist
        assert result["after_hash"] == sha256_digest(target)
        assert target.read_text(encoding="utf-8") == "first"

        # Second write: before_hash reflects the previous content.
        result2 = write_file(target, "second")
        assert result2["before_hash"] == result["after_hash"]
        assert target.read_text(encoding="utf-8") == "second"

    def test_bak_snapshot_created(self, tmp_path: Path) -> None:
        target = tmp_path / "c.txt"
        write_file(target, "v1")
        write_file(target, "v2")
        bak = target.with_suffix(target.suffix + ".bak")
        assert bak.exists()
        assert bak.read_text(encoding="utf-8") == "v1"


class TestWriteFileCas:
    def test_matching_digest_writes(self, tmp_path: Path) -> None:
        target = tmp_path / "d.txt"
        write_file(target, "base")
        _, digest = read_file(target)
        result = write_file(target, "updated", expected_digest=digest)
        assert result["conflict"] is False
        assert target.read_text(encoding="utf-8") == "updated"

    def test_stale_digest_conflicts(self, tmp_path: Path) -> None:
        target = tmp_path / "e.txt"
        write_file(target, "base")
        _, stale = read_file(target)
        # Another writer changes the file in between.
        target.write_text("someone else", encoding="utf-8")

        with pytest.raises(RepoWriteConflict):
            write_file(target, "mine", expected_digest=stale)

        # Original content preserved (no overwrite).
        assert target.read_text(encoding="utf-8") == "someone else"

    def test_conflict_raises_via_conflict_flag_never(self, tmp_path: Path) -> None:
        # The exception API is the contract; ensure no silent last-writer-wins.
        target = tmp_path / "f.txt"
        write_file(target, "base")
        _, stale = read_file(target)
        target.write_text("other", encoding="utf-8")
        with pytest.raises(RepoWriteConflict):
            write_file(target, "x", expected_digest=stale)


class TestWriteFileOwnership:
    def test_owner_conflict_denies(self, tmp_path: Path) -> None:
        target = tmp_path / "g.txt"
        target.write_text("held by other", encoding="utf-8")

        def deny(path: Path, owner: object) -> bool:
            # Deny writes to any file except the matching owner's scratch path.
            return path.name != "mine.txt" or owner != "task-1"

        set_owner_registry(deny)
        try:
            result = write_file(target, "attempt", owner="task-9", claimed_by_owner=True)
            assert result["owner_conflict"] is True
            assert target.read_text(encoding="utf-8") == "held by other"

            # Claimant may write.
            mine = tmp_path / "mine.txt"
            res = write_file(mine, "ok", owner="task-1", claimed_by_owner=True)
            assert res["owner_conflict"] is False
            assert mine.read_text(encoding="utf-8") == "ok"
        finally:
            set_owner_registry(None)

    def test_no_owner_no_enforcement(self, tmp_path: Path) -> None:
        target = tmp_path / "h.txt"
        result = write_file(target, "plain")  # owner=None => no ownership check
        assert result["owner_conflict"] is False
        assert target.read_text(encoding="utf-8") == "plain"
