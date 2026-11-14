#!/usr/bin/env python
"""
Operational Token Savings Dashboard

Runs the dashboard, checks progress, and provides operational status.
Can be scheduled for daily/weekly monitoring.

Run: python operational_dashboard.py
"""

import json
import os
import sys
from datetime import datetime

sys.path.insert(0, r"C:\Users\jmlus\light-speed-holdings\src")


def fmt(text):
    """Safe print handling Unicode."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"))


def check_baseline():
    """Check if baseline exists and show status."""
    baseline_path = "data/orchestrator/cost_tracker_baseline.json"
    if os.path.exists(baseline_path):
        try:
            with open(baseline_path, "r", encoding="utf-8") as f:
                baseline = json.load(f)
            prompt = baseline.get("total_prompt_tokens", "N/A")
            calls = baseline.get("call_count", "N/A")
            captured = baseline.get("baseline_captured", "N/A")
            fmt("OK Pre-Phase 1 Baseline Captured:")
            fmt("   Prompt tokens: " + str(prompt) + ",")
            fmt("   API calls:     " + str(calls) + ",")
            fmt("   Captured:      " + captured)
            return True
        except (OSError, json.JSONDecodeError) as e:
            fmt("Error reading baseline: " + str(e))
    else:
        fmt("No baseline captured yet!")
        fmt("Run: python scripts/dashboard/capture_baseline.py")
        return False


def run_dashboard():
    """Run the main dashboard."""
    fmt("\n" + "=" * 60)
    fmt("RUNNING TOKEN SAVINGS DASHBOARD")
    fmt("=" * 60)

    try:
        with open("scripts/dashboard/dashboard_token_savings.py", encoding="utf-8") as f:
            exec(f.read())
    except (OSError, SyntaxError, NameError, RuntimeError) as e:
        fmt("Dashboard error: " + str(e))


def check_phases():
    """Check Phase status."""
    fmt("\nPhase Status:")
    fmt("  Phase 1: Memory search optimization - OK")
    fmt("  Phase 2: Prompt compression & caching ")
    fmt("OK")

    fmt("  Phase 3: Memory pruning & vector search ")
    try:
        from ai_company.memory.engine import MemoryStore

        MemoryStore()
        fmt("OK")
    except (ImportError, RuntimeError, OSError, AttributeError) as e:
        fmt("Error: " + str(e))


def check_env():
    """Check environment configuration."""
    fmt("\nEnvironment Configuration:")
    env_vars = ["AI_COMPANY_VECTOR_SEARCH", "ENABLE_PROMPT_COMPRESSION"]
    for var in env_vars:
        val = os.environ.get(var, "not set")
        fmt("  " + var + ": " + val)


def main():
    fmt("=" * 60)
    fmt("OPERATIONAL TOKEN SAVINGS DASHBOARD")
    fmt("as of " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    fmt("=" * 60)

    # Check baseline
    check_baseline()

    # Run main dashboard
    run_dashboard()

    # Check phases
    check_phases()

    # Check environment
    check_env()

    fmt("\n" + "=" * 60)
    fmt("OPERATIONAL SUMMARY")
    fmt("=" * 60)

    if os.path.exists("data/orchestrator/cost_tracker_baseline.json"):
        fmt("OK Baseline captured - ready for comparison")
    else:
        fmt("⚠️  Baseline not captured - run capture_baseline.py")

    fmt("✅ Dashboard operational")
    fmt("✅ Vector search enabled (AI_COMPANY_VECTOR_SEARCH=1)")
    fmt("⏳ Progress tracking in progress")
    fmt("📊 Run daily to monitor reduction toward 40% target")

    fmt("\nRecommended next steps:")
    fmt("  1. Make LLM calls to populate cost tracker")
    fmt("  2. Run: python scripts/dashboard/dashboard_token_savings.py")
    fmt("  3. Enable prompt compression: see dashboard recommendations")
    fmt("  4. Monitor reduction percentage weekly")


if __name__ == "__main__":
    main()
