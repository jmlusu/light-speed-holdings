"""Pre-persistence secret redaction (F-05 / P0-T5). Synthetic values only."""

from __future__ import annotations

from ai_company.security.redact import contains_secret_pattern, redact_secrets


class TestRedactSecrets:
    def test_openai_style_key_redacted(self) -> None:
        redacted, hits = redact_secrets("key is sk-abcd1234EFGH5678ijkm")
        assert "sk-" not in redacted
        assert "[REDACTED]" in redacted
        assert "openai_sk" in hits

    def test_key_name_preserved(self) -> None:
        redacted, hits = redact_secrets("API_KEY=supersecretvalue")
        assert redacted.startswith("API_KEY=[REDACTED]")
        assert "api_key_assign" in hits

    def test_benign_text_untouched(self) -> None:
        redacted, hits = redact_secrets("The registry lists 72 projects.")
        assert redacted == "The registry lists 72 projects."
        assert hits == []

    def test_empty_string(self) -> None:
        assert redact_secrets("") == ("", [])

    def test_bearer_token(self) -> None:
        redacted, hits = redact_secrets("Authorization: Bearer abcdef1234567890")
        assert "abcdef1234567890" not in redacted
        assert "bearer_token" in hits

    def test_contains_pattern_never_returns_values(self) -> None:
        text = "token sk-abcdefgh12345678 here"
        ids = contains_secret_pattern(text)
        assert "openai_sk" in ids
        assert "abcdefgh12345678" not in " ".join(ids)
