#!/usr/bin/env python
"""
Capture Pre-Phase 1 Baseline

Captures the current token usage as the pre-Phase 1 baseline.
This must be run BEFORE deploying Phase 1 changes.

Run: python capture_baseline.py
"""

import json
import os
import shutil
import sys
from datetime import datetime

sys.path.insert(0, r"C:\Users\jmlus\light-speed-holdings\src")


def main():
    banner = "=" * 60
    title = "CAPTURE PRE-PHASE 1 BASELINE"
    subtitle = f"as of {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    print(f"{banner}")
    print(f"{title:^60}")
    print(f"{subtitle:^60}")
    print("-" * 60)

    # Step 1: Save current cost tracker as baseline
    baseline_path = "data/orchestrator/cost_tracker_baseline.json"

    if os.path.exists(baseline_path):
        overwrite = input("Baseline file already exists. Overwrite? (y/n): ")
        if overwrite.lower() != "y":
            print("Baseline capture aborted.")
            return

    # Read current cost tracker
    try:
        with open("data/orchestrator/cost_tracker.json", "r", encoding="utf-8") as f:
            current_data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error reading cost tracker: {e}")
        return

    # Create baseline copy
    baseline_data = dict(current_data)
    baseline_data["baseline_captured"] = datetime.now().isoformat()
    baseline_data["description"] = "Pre-Phase 1 baseline token usage"

    # Write baseline file
    try:
        with open(baseline_path, "w", encoding="utf-8") as f:
            json.dump(baseline_data, f, indent=2)
        print("✅ Baseline captured and saved to: data/orchestrator/cost_tracker_baseline.json")
    except OSError as e:
        print(f"Error writing baseline: {e}")
        return

    # Show baseline summary
    baseline_prompt = baseline_data.get("total_prompt_tokens", 0)
    baseline_total = baseline_data.get("total_tokens", 0)
    baseline_calls = baseline_data.get("call_count", 0)

    print("\nBaseline Summary:")
    print(f"  Prompt tokens:  {baseline_prompt:,}")
    print(f"  Total tokens:   {baseline_total:,}")
    print(f"  API calls:      {baseline_calls:,}")
    print("\n⚠️  IMPORTANT: Keep this file safe!")
    print("   This is your pre-Phase 1 baseline for comparison.")
    print("   Store it in a secure location (Git, cloud, etc.).")

    # Offer to backup
    backup_choice = input("\nCreate backup in scripts/dashboard/backups/? (y/n): ")
    if backup_choice.lower() == "y":
        try:
            os.makedirs("scripts/dashboard/backups", exist_ok=True)
            shutil.copy(baseline_path, "scripts/dashboard/backups/")
            print("✅ Backup created in: scripts/dashboard/backups/")
        except OSError as e:
            print(f"Backup warning: {e}")

    print(f"\n{banner}")
    print("BASELINE CAPTURE COMPLETE")
    print(f"{banner}")


if __name__ == "__main__":
    main()
