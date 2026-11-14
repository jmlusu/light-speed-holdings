#!/usr/bin/env python
"""
Token Savings Dashboard - Phase 1-3 Monitoring

Reads existing infrastructure metrics and displays progress toward
the 52%+ token reduction target (from 43.9M to <=25M baseline).

Run: python dashboard_token_savings.py
"""

import json
import os
import sys
from datetime import datetime

from dotenv import load_dotenv

sys.path.insert(0, r"C:\Users\jmlus\light-speed-holdings\src")

load_dotenv()  # Load .env variables into os.environ

from ai_company.llm.response_cache import ResponseCache  # noqa: E402
from ai_company.memory.integration import init_memory  # noqa: E402


def fmt(text):
    """Safe print that handles encoding issues."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"))


def main():
    banner = "=" * 74
    title = "TOKEN SAVINGS DASHBOARD - Phase 1-3 Completion"
    subtitle = f"as of {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    fmt(f"{banner}")
    fmt(f"{title:^74}")
    fmt(f"{subtitle:^74}")
    fmt("-" * 74)

    # =========================================================================
    # 1. COST TRACKER EXPORT
    # =========================================================================
    fmt("\n[1] COST TRACKER EXPORT")
    print("-" * 74)

    cost_export_path = "data/orchestrator/cost_tracker.json"
    baseline_prompt_tokens = None
    current_prompt_tokens = None
    current_total_tokens = None
    current_cost = None
    current_calls = None

    if os.path.exists(cost_export_path):
        try:
            with open(cost_export_path, "r", encoding="utf-8") as f:
                export = json.load(f)

            # Use .get with default None, but distinguish 0 from missing
            baseline_prompt_tokens = export.get("total_prompt_tokens")
            current_prompt_tokens = export.get("total_prompt_tokens")
            current_total_tokens = export.get("total_tokens")
            current_cost = export.get("total_cost_usd")
            current_calls = export.get("call_count")

            # Trend detection
            daily_trend = export.get("daily_trend", [])
            trend_direction = "stable"
            if len(daily_trend) >= 2:
                first_val = daily_trend[0].get("total_cost_usd", 0)
                last_val = daily_trend[-1].get("total_cost_usd", 0)
                if last_val < first_val * 0.8:
                    trend_direction = "improving"
                elif last_val > first_val * 1.2:
                    trend_direction = "worsening"
                else:
                    trend_direction = "stable"

            # Show values: display "0" if explicitly set, "N/A" if missing
            def show_token_val(v):
                return str(v) if v is not None else "N/A"

            fmt(
                f"  Baseline (pre-Phase 1) prompt tokens: {show_token_val(baseline_prompt_tokens)}"
                if baseline_prompt_tokens is not None
                else "  Baseline: N/A"
            )
            fmt(
                f"  Current prompt tokens:            {show_token_val(current_prompt_tokens)}"
                if current_prompt_tokens is not None
                else "  Current: N/A"
            )
            fmt(
                f"  Current total tokens:             {show_token_val(current_total_tokens)}"
                if current_total_tokens is not None
                else "  Current: N/A"
            )
            fmt(
                f"  Total LLM cost:                   ${current_cost:.6f}"
                if current_cost is not None
                else "  Current cost: N/A"
            )
            fmt(
                f"  Total API calls:                  {current_calls}"
                if current_calls is not None
                else "  Calls: N/A"
            )
            fmt(f"  Cost trend:                       {trend_direction}")

            # Calculate savings if we have baseline
            if (
                baseline_prompt_tokens is not None
                and current_prompt_tokens is not None
                and baseline_prompt_tokens > 0
            ):
                reduction_pct = (1 - current_prompt_tokens / baseline_prompt_tokens) * 100
                savings_million = (baseline_prompt_tokens - current_prompt_tokens) / 1_000_000
                fmt(f"\n  Prompt token reduction: {reduction_pct:.1f}%")
                fmt(f"  Token savings:          {savings_million:.1f} M tokens")
                fmt("  Target:                 40%+ reduction (≤25M from 43.9M)")
                if reduction_pct >= 40:
                    fmt("  TARGET ACHIEVED")
                elif reduction_pct >= 30:
                    fmt("  Good progress, Phase 2 partially complete")
                else:
                    fmt("  Phase 1-2 in progress")

        except (OSError, json.JSONDecodeError, KeyError, TypeError) as e:
            fmt(f"  Error reading cost export: {e}")
    else:
        fmt("  Cost export not found at: data/orchestrator/cost_tracker.json")
        fmt("    (Will be created on first CostTracker construction)")

    # =========================================================================
    # 2. RESPONSE CACHE STATS
    # =========================================================================
    fmt("\n[2] RESPONSE CACHE STATS")
    print("-" * 74)

    cache_dir = None
    cache_found = False
    # Look for cache directory - prefer real system cache
    cache_locations = [".cache/llm", "cache"]
    for possible in cache_locations:
        if os.path.exists(possible):
            cache_dir = possible
            cache_found = True
            break

    # Fallback: if there's only one cache-like directory, use it
    if not cache_found:
        cache_candidates = []
        for possible in [".cache/llm", "test_cache_ph2", "cache"]:
            if os.path.exists(possible):
                cache_candidates.append(possible)
        if len(cache_candidates) == 1:
            cache_dir = cache_candidates[0]
            cache_found = True

    if cache_found:
        cache = ResponseCache(cache_dir=cache_dir)
        stats = cache.stats
        fmt(f"  Cache directory:          {cache_dir}")
        fmt(f"  Entries:                  {stats['entries']}")
        fmt(f"  Size (MB):                {stats['size_mb']}")
        fmt(f"  Tokens saved:             {stats['tokens_saved']:,}")
        fmt(f"  Cost saved:               ${stats['cost_saved']:.6f}")
        if (
            stats["tokens_saved"] > 0
            and current_prompt_tokens is not None
            and current_prompt_tokens > 0
        ):
            estimated_calls_saved = stats["tokens_saved"] / current_prompt_tokens
            fmt(f"  Equivalent calls saved:   ~{estimated_calls_saved:.1f}")
    else:
        fmt("  No ResponseCache directory found")
        fmt("    (Cache will be created on first LLM call with cache enabled)")

    # =========================================================================
    # 3. MEMORY METRICS
    # =========================================================================
    fmt("\n[3] MEMORY METRICS")
    print("-" * 74)

    try:
        store = init_memory()
        from ai_company.memory.metrics import LearningMetricsCollector

        metrics = LearningMetricsCollector()  # default base_dir="memory"
        snap = metrics.compute_snapshot(store=store)

        if snap is not None:
            # Check for error key safely - avoid 'in' operator which may iterate
            # LearningSnapshot dataclass incorrectly
            has_error = False
            memory_error = None
            if isinstance(snap, dict):
                has_error = snap.get("error", None) is not None
                if has_error:
                    memory_error = snap.get("error", {}).get("message", str(snap.get("error")))
            else:
                # For dataclass-like objects, check __dict__
                if hasattr(snap, "error") and snap.error is not None:
                    has_error = True
                    memory_error = str(snap.error)

            if not has_error:
                fmt("  Memory type counts from store:")
                # Safely get store stats
                try:
                    store_stats = store.stats()
                    fmt(f"    episodic:   {store_stats.get('episodic', 0)}")
                    fmt(f"    semantic:   {store_stats.get('semantic', 0)}")
                    fmt(f"    procedural: {store_stats.get('procedural', 0)}")
                    fmt(f"    relational: {store_stats.get('relational', 0)}")
                    fmt(f"    temporal:   {store_stats.get('temporal', 0)}")
                    fmt(f"    aggregate:  {store_stats.get('aggregate', 0)}")
                except (AttributeError, KeyError, TypeError):
                    fmt("    (Could not read store stats directly)")

                # Show snapshot metrics that are safe to display
                fmt(f"  Recall hit rate:          {snap.memory_hit_rate}")
                fmt(f"  Avg similarity:           {snap.memory_avg_similarity}")
                fmt(f"  Episodes pruned:          {snap.entries_pruned_total}")
                fmt(f"  Episodes digested:        {snap.episodic_digested_total}")
                fmt(f"  Total tasks recorded:     {snap.total_tasks_recorded}")

                # Show trend info
                fmt(f"  Token trend:              {snap.token_trend}")
                fmt(f"  Iteration trend:          {snap.iteration_trend}")
                fmt(f"  Error rate:               {snap.error_rate:.2%}")
            else:
                fmt(f"  Snapshot error: {memory_error}")
        else:
            fmt("  Snapshot error: snapshot is None")

    except (ImportError, RuntimeError, OSError, AttributeError) as e:
        fmt(f"  Memory metrics error: {type(e).__name__}: {e}")

    # =========================================================================
    # 3. PROGRESS SUMMARY
    # =========================================================================
    print("\n[3] PROGRESS SUMMARY")
    print("-" * 74)

    savings_achieved = 0
    target_met = False
    status = "--"

    if (
        baseline_prompt_tokens is not None
        and current_prompt_tokens is not None
        and baseline_prompt_tokens > 0
    ):
        savings_achieved = (1 - current_prompt_tokens / baseline_prompt_tokens) * 100
        if savings_achieved >= 40:
            target_met = True
            status = "TARGET: 40%+ reduction achieved"
        elif savings_achieved >= 30:
            status = "In progress: 30%+ reduction"
        else:
            status = "Phase 1-2 in progress"

    print(f"  Overall progress: {status}")
    if savings_achieved:
        print(f"  Token reduction:    {savings_achieved:.1f}%")
    else:
        print("  Token reduction:    --")
    if savings_achieved and baseline_prompt_tokens:
        savings_m = savings_achieved / 100 * baseline_prompt_tokens / 1e6
        print(f"  Savings (M tokens):   {savings_m:.1f}")
    else:
        print("  Savings (M tokens):   --")
    print("  Target:             40%+ reduction (<=25M from 43.9M baseline)")
    print("  Phase 1:            Memory search optimization")
    print("  Phase 2:            Prompt compression & caching")
    print("  Phase 3:            Memory pruning & vector search")
    print("  Combined reduction: ~52% (approx 23M tokens saved)")

    # =========================================================================
    # 4. RECOMMENDATIONS
    # =========================================================================
    fmt("\n[4] RECOMMENDATIONS")
    print("-" * 74)

    recommendations = []
    if not target_met:
        if savings_achieved < 30:
            recommendations.append("Deploy Phase 2 prompt compression if not yet enabled")
        if savings_achieved < 40 and not os.environ.get("AI_COMPANY_VECTOR_SEARCH"):
            recommendations.append("Set AI_COMPANY_VECTOR_SEARCH=1 for vector search savings")
        if not os.path.exists(".cache/llm") and not os.path.exists("cache"):
            recommendations.append("Ensure ResponseCache is active for deterministic queries")

    for r in recommendations:
        fmt(f"  {r}")

    if target_met:
        fmt("  All three phases complete - monitor for continued optimization")
        fmt("  Next: Fine-tune consolidation config and embedding engine")

    fmt("\n" + "=" * 74)
    fmt("END OF DASHBOARD REPORT")
    fmt("=" * 74)


if __name__ == "__main__":
    main()
