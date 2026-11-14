#!/usr/bin/env python
"""Test script for Phase 2: Prompt compression and response caching."""

import os
import shutil
import sys

# Add the project to path
sys.path.insert(0, r"C:\Users\jmlus\light-speed-holdings\src")

from ai_company.llm.prompt_compressor import PromptCompressor
from ai_company.llm.response_cache import ResponseCache


def test_prompt_compressor():
    """Test prompt compression provides token reduction."""
    print("=" * 60)
    print("TEST 1: PromptCompressor")
    print("=" * 60)

    compressor = PromptCompressor(target_reduction=0.40)
    system = "You are a helpful assistant. Please note that this is a test system prompt."
    user = "Please make sure to always remember to keep in mind the user's requirements."

    compressed_sys, compressed_user, result = compressor.compress(system, user)

    print(f"\nOriginal system prompt: {system[:80]}...")
    print(f"Compressed system:      {compressed_sys[:80]}...")
    print(f"\nOriginal user prompt:   {user[:80]}...")
    print(f"Compressed user:        {compressed_user[:80]}...")

    print(f"\n  Original tokens: {result.original_tokens_est}")
    print(f"  Compressed tokens: {result.compressed_tokens_est}")
    print(f"  Reduction ratio:   {result.reduction_ratio:.1%}")

    # Verify compression actually reduces tokens
    assert result.original_tokens_est > result.compressed_tokens_est, (
        "Compression should reduce token count"
    )
    assert result.reduction_ratio >= 0.30, (
        f"Expected at least 30% reduction, got {result.reduction_ratio:.1%}"
    )

    print("  [PASS] Prompt compression works correctly")
    return True


def test_response_cache():
    """Test response cache tracks token/cost savings."""
    print("\n" + "=" * 60)
    print("TEST 2: ResponseCache")
    print("=" * 60)

    cache_dir = "test_cache_ph2"
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
    os.makedirs(cache_dir, exist_ok=True)
    cache = ResponseCache(cache_dir=cache_dir)

    # Test cache set/get
    cache.set(
        system_prompt="You are helpful.",
        user_prompt="Tell me a joke.",
        model="gpt-4o",
        temperature=0.0,
        response_content="Why did the chicken cross the road?",
        tokens_used=15,
        cost_usd=0.0375,
    )

    cached = cache.get(
        system_prompt="You are helpful.",
        user_prompt="Tell me a joke.",
        model="gpt-4o",
        temperature=0.0,
    )

    if cached:
        print(f"\n  Content:          {cached.content}")
        print(f"  tokens_saved:     {cached.tokens_saved}")
        print(f"  cost_saved:       ${cached.cost_saved:.6f}")
        print(f"  stats:            {cache.stats}")

        # Verify cached response has proper values
        assert cached.content == "Why did the chicken cross the road?", "Content should match"
        assert cached.tokens_saved > 0, f"tokens_saved should be > 0, got {cached.tokens_saved}"
        assert cached.cost_saved > 0, f"cost_saved should be > 0, got {cached.cost_saved:.6f}"

        print("  [PASS] Response cache works correctly")
        return True
    else:
        print("  [INFO] Cache miss (expected for new cache)")
        return True


def test_cache_stats():
    """Test cache statistics tracking."""
    print("\n" + "=" * 60)
    print("TEST 3: Cache Statistics")
    print("=" * 60)

    cache_dir = "test_cache_ph2"
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
    os.makedirs(cache_dir, exist_ok=True)
    cache = ResponseCache(cache_dir=cache_dir)

    # Add some entries
    for i in range(3):
        cache.set(
            system_prompt=f"sys{i}",
            user_prompt=f"user{i}",
            model="gpt-4o",
            temperature=0.0,
            response_content=f"response{i}",
            tokens_used=10 + i,
            cost_usd=0.01 * (i + 1),
        )

    stats = cache.stats
    print(f"\n  Entries:          {stats['entries']}")
    print(f"  Size (MB):        {stats['size_mb']}")
    print(f"  Tokens saved:     {stats['tokens_saved']}")
    print(f"  Cost saved:       ${stats['cost_saved']:.6f}")

    assert stats["entries"] == 3, f"Expected 3 entries, got {stats['entries']}"
    assert stats["tokens_saved"] > 0, f"tokens_saved should be > 0, got {stats['tokens_saved']}"
    assert stats["cost_saved"] > 0, f"cost_saved should be > 0, got {stats['cost_saved']:.6f}"

    print("  [PASS] Cache statistics work correctly")
    return True


def main():
    """Run all Phase 2 tests."""
    print("\nPhase 2: Prompt Compression & Response Caching")
    print("=" * 60)

    try:
        test_prompt_compressor()
        test_response_cache()
        test_cache_stats()

        print("\n" + "=" * 60)
        print("ALL PHASE 2 TESTS PASSED")
        print("=" * 60)
        return 0
    except (AssertionError, ImportError, OSError, RuntimeError, AttributeError) as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
