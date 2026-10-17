"""Unit tests for the Pharos publishing rails (ADR-020 P1)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_company.publishing.formats import (
    LINKEDIN_CHAR_LIMIT,
    SUBSTACK_WORD_LIMIT,
    format_linkedin,
    format_substack,
)
from ai_company.publishing.publishers import (
    LINKEDIN_TOKEN_ENV,
    LINKEDIN_URL_ENV,
    SUBSTACK_TOKEN_ENV,
    SUBSTACK_URL_ENV,
    LinkedInPublisher,
    SubstackPublisher,
)
from ai_company.publishing.queue import KNOWN_PLATFORMS, PublishQueue

# ── queue CRUD ────────────────────────────────────────────────────────────────


def test_queue_enqueue_and_list(tmp_path: Path) -> None:
    queue = PublishQueue(tmp_path)
    record = queue.enqueue("linkedin", "Hello Pharos", "Body text here.")
    assert record.id.startswith("pub-linkedin-")
    assert record.status == "queued"
    assert queue.get(record.id) is not None
    assert len(queue.list()) == 1


def test_queue_rejects_unknown_platform(tmp_path: Path) -> None:
    queue = PublishQueue(tmp_path)
    with pytest.raises(ValueError):
        queue.enqueue("instagram", "Nope", "Body")


def test_queue_known_platforms() -> None:
    assert {"linkedin", "substack"} == KNOWN_PLATFORMS


def test_queue_mark_posted_and_failed(tmp_path: Path) -> None:
    queue = PublishQueue(tmp_path)
    record = queue.enqueue("substack", "Title", "Body")
    posted = queue.mark_posted(record.id, external_url="https://x.example/p")
    assert posted is not None and posted.status == "posted"
    assert posted.external_url == "https://x.example/p"

    failed = queue.mark_failed(record.id, notes="API 500")
    assert failed is not None and failed.status == "failed"
    assert failed.notes == "API 500"


def test_queue_persists_across_instances(tmp_path: Path) -> None:
    queue = PublishQueue(tmp_path)
    queue.enqueue("linkedin", "T", "B")
    reloaded = PublishQueue(tmp_path)
    assert len(reloaded.list()) == 1


def test_queue_stats_and_clear(tmp_path: Path) -> None:
    queue = PublishQueue(tmp_path)
    a = queue.enqueue("linkedin", "A", "a")
    queue.enqueue("linkedin", "B", "b")
    queue.mark_posted(a.id)
    stats = queue.stats()
    assert stats["queued"] == 1
    assert stats["posted"] == 1
    assert stats["total"] == 2
    queue.clear()
    assert queue.stats()["total"] == 0


def test_queue_mirror_to_bus(tmp_path: Path) -> None:
    """A provided bus receives a pharos-publish task for the record."""
    queue = PublishQueue(tmp_path)

    class FakeBus:
        def __init__(self) -> None:
            self.sent: list = []

        def send_task(self, task) -> None:  # type: ignore[no-untyped-def]
            self.sent.append(task)

    bus = FakeBus()
    record = queue.enqueue("linkedin", "Mirrored", "Body", bus=bus)
    assert len(bus.sent) == 1
    task = bus.sent[0]
    assert task.id == record.id
    assert "pharos-publish" in task.tags


# ── formatters ────────────────────────────────────────────────────────────────


def test_format_linkedin_under_limit() -> None:
    result = format_linkedin("Hello", "Small body.")
    assert result["platform"] == "linkedin"
    assert result["truncated"] is False
    assert "Hello" in result["text"]
    assert not result["text"].endswith("[continued in queue]")


def test_format_linkedin_truncation() -> None:
    long_body = "word " * (LINKEDIN_CHAR_LIMIT * 2)
    result = format_linkedin("Hi", long_body)
    assert result["truncated"] is True
    assert result["text"].endswith("[continued in queue]")
    core = result["text"].split("[continued in queue]")[0].rstrip()
    assert len(core) <= LINKEDIN_CHAR_LIMIT
    assert "word" in core


def test_format_substack_markdown() -> None:
    result = format_substack("A Title", "## Section\n\nSome **bold** text.")
    assert result["platform"] == "substack"
    assert result["markdown"].startswith("# A Title")
    assert "## Section" in result["markdown"]
    assert result["truncated"] is False


def test_format_substack_word_limit_flag() -> None:
    body = " ".join(["x"] * (SUBSTACK_WORD_LIMIT + 100))
    result = format_substack("Title", body)
    assert result["truncated"] is True


# ── publishers (buy-side, env-gated) ───────────────────────────────────────────


def test_linkedin_publisher_dry_run_when_unconfigured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(LINKEDIN_URL_ENV, raising=False)
    monkeypatch.delenv(LINKEDIN_TOKEN_ENV, raising=False)
    publisher = LinkedInPublisher()
    from ai_company.publishing.queue import PublishRecord

    record = PublishRecord(id="r1", platform="linkedin", title="T", body="B")
    result = publisher.publish(record)
    assert result.status == "dry_run"
    assert not result.url


def test_substack_publisher_live_posts_with_creds(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv(SUBSTACK_URL_ENV, "https://api.example/substack")
    monkeypatch.setenv(SUBSTACK_TOKEN_ENV, "secret")
    publisher = SubstackPublisher()

    from ai_company.publishing.queue import PublishRecord

    record = PublishRecord(id="r2", platform="substack", title="T", body="Body")

    def fake_post(url: str, token: str, formatted: dict) -> dict:  # type: ignore[no-untyped-def]
        assert url == "https://api.example/substack"
        assert token == "secret"
        assert formatted["markdown"].startswith("# T")
        return {"url": "https://substack.example/p/1"}

    monkeypatch.setattr(publisher, "_post", fake_post)
    result = publisher.publish(record, force_live=True)
    assert result.status == "posted"
    assert result.url == "https://substack.example/p/1"


def test_publisher_transport_error_becomes_failed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(LINKEDIN_URL_ENV, "https://api.example/linkedin")
    monkeypatch.setenv(LINKEDIN_TOKEN_ENV, "secret")
    publisher = LinkedInPublisher()

    from ai_company.publishing.queue import PublishRecord

    record = PublishRecord(id="r3", platform="linkedin", title="T", body="Body")

    def boom(url: str, token: str, formatted: dict) -> dict:  # type: ignore[no-untyped-def]
        raise ConnectionError("network down")

    monkeypatch.setattr(publisher, "_post", boom)
    result = publisher.publish(record, force_live=True)
    assert result.status == "failed"
    assert "network down" in result.error
