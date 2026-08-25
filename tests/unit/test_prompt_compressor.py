"""Unit tests for PromptCompressor — rules-based prompt compression."""

from __future__ import annotations

from ai_company.llm.prompt_compressor import PromptCompressor, _estimate_tokens


class TestPromptCompressor:
    """Compression preserves meaning while reducing token count."""

    def test_empty_prompts(self) -> None:
        comp = PromptCompressor()
        s, u, result = comp.compress("", "")
        assert s == ""
        assert u == ""
        assert result.original_tokens_est == 0

    def test_filler_removal(self) -> None:
        comp = PromptCompressor()
        system = "Please note that you are a helpful assistant."
        user = "It is important to note that this is a test."
        s, u, result = comp.compress(system, user)
        assert "Please note that" not in s
        assert "It is important to note that" not in u
        assert result.compressed_tokens_est <= result.original_tokens_est

    def test_whitespace_normalization(self) -> None:
        comp = PromptCompressor()
        system = "You are\n\n\n\n\nhelpful."
        user = "Do  this   task  please"
        s, u, result = comp.compress(system, user)
        assert "\n\n\n" not in s
        assert "  " not in u

    def test_meaning_preserved(self) -> None:
        comp = PromptCompressor()
        system = "You are a code reviewer."
        user = "Review the function for bugs."
        s, u, result = comp.compress(system, user)
        assert "code reviewer" in s
        assert "Review" in u
        assert "bugs" in u

    def test_deduplication(self) -> None:
        comp = PromptCompressor()
        text = "Rule one: be concise.\nRule one: be concise.\nRule two: be clear."
        s, _, result = comp.compress(text, "task")
        assert s.count("Rule one: be concise.") == 1
        assert result.compressed_tokens_est < result.original_tokens_est

    def test_reduction_ratio(self) -> None:
        comp = PromptCompressor(target_reduction=0.1)
        system = "Please note that you are a helpful assistant. " * 10
        user = "It is important to note that you must be careful. " * 10
        s, u, result = comp.compress(system, user)
        assert result.reduction_ratio > 0.0
        assert result.compressed_tokens_est < result.original_tokens_est


class TestEstimateTokens:
    """Token estimation sanity checks."""

    def test_empty(self) -> None:
        assert _estimate_tokens("") == 0
        assert _estimate_tokens("   ") == 0

    def test_single_word(self) -> None:
        assert _estimate_tokens("hello") >= 1

    def test_longer_text(self) -> None:
        text = "a" * 100
        # ~4 chars/token → ~25 tokens
        tokens = _estimate_tokens(text)
        assert 20 <= tokens <= 30
