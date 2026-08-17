#!/usr/bin/env python3
"""Validation script for token optimization A/B experiments.

Generates comprehensive token reduction reports comparing control vs treatment groups
across all optimization experiments.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_company.executor.ab_testing import get_ab_framework, ExperimentMetrics


def load_experiment_metrics(experiment_name: str, days: int = 7) -> list[ExperimentMetrics]:
    """Load metrics for an experiment from the last N days."""
    metrics_dir = Path("results/experiments")
    if not metrics_dir.exists():
        return []
    
    cutoff_date = (datetime.now() - timedelta(days=days)).date().isoformat()
    all_metrics: list[ExperimentMetrics] = []
    
    for file_path in metrics_dir.glob(f"{experiment_name}_*.jsonl"):
        # Extract date from filename
        try:
            date_str = file_path.stem.split("_")[-1]
            if date_str < cutoff_date:
                continue
        except (IndexError, ValueError):
            pass
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data = json.loads(line)
                        all_metrics.append(ExperimentMetrics(**data))
        except Exception as e:
            print(f"Warning: Failed to load {file_path}: {e}")
    
    return all_metrics


def compute_statistics(metrics: list[ExperimentMetrics]) -> dict[str, Any]:
    """Compute comprehensive statistics for a set of metrics."""
    if not metrics:
        return {"count": 0}
    
    total_tokens = [m.total_tokens for m in metrics]
    costs = [m.cost_usd for m in metrics]
    iterations = [m.iterations for m in metrics]
    durations = [m.duration_seconds for m in metrics]
    success_count = sum(1 for m in metrics if m.success)
    completion_count = sum(1 for m in metrics if m.task_completed)
    
    def percentile(data: list[float], p: float) -> float:
        if not data:
            return 0.0
        sorted_data = sorted(data)
        idx = int(len(sorted_data) * p)
        return sorted_data[min(idx, len(sorted_data) - 1)]
    
    return {
        "count": len(metrics),
        "tokens": {
            "mean": sum(total_tokens) / len(total_tokens),
            "median": percentile(total_tokens, 0.5),
            "p95": percentile(total_tokens, 0.95),
            "p99": percentile(total_tokens, 0.99),
            "min": min(total_tokens),
            "max": max(total_tokens),
            "total": sum(total_tokens),
        },
        "cost_usd": {
            "mean": sum(costs) / len(costs),
            "median": percentile(costs, 0.5),
            "p95": percentile(costs, 0.95),
            "total": sum(costs),
        },
        "iterations": {
            "mean": sum(iterations) / len(iterations),
            "median": percentile(iterations, 0.5),
            "p95": percentile(iterations, 0.95),
            "min": min(iterations),
            "max": max(iterations),
        },
        "duration_seconds": {
            "mean": sum(durations) / len(durations) if durations else 0,
            "median": percentile(durations, 0.5) if durations else 0,
            "p95": percentile(durations, 0.95) if durations else 0,
        },
        "success_rate": success_count / len(metrics),
        "completion_rate": completion_count / len(metrics),
    }


def compare_variants(control: list[ExperimentMetrics], treatment: list[ExperimentMetrics]) -> dict[str, Any]:
    """Compare control vs treatment and compute reduction percentages."""
    control_stats = compute_statistics(control)
    treatment_stats = compute_statistics(treatment)
    
    if control_stats["count"] == 0 or treatment_stats["count"] == 0:
        return {
            "error": "Insufficient data for comparison",
            "control": control_stats,
            "treatment": treatment_stats,
        }
    
    # Compute reductions (positive = treatment is better)
    token_reduction = (
        (control_stats["tokens"]["mean"] - treatment_stats["tokens"]["mean"])
        / control_stats["tokens"]["mean"] * 100
    )
    cost_reduction = (
        (control_stats["cost_usd"]["mean"] - treatment_stats["cost_usd"]["mean"])
        / control_stats["cost_usd"]["mean"] * 100
    ) if control_stats["cost_usd"]["mean"] > 0 else 0
    iteration_reduction = (
        (control_stats["iterations"]["mean"] - treatment_stats["iterations"]["mean"])
        / control_stats["iterations"]["mean"] * 100
    ) if control_stats["iterations"]["mean"] > 0 else 0
    duration_change = (
        (treatment_stats["duration_seconds"]["mean"] - control_stats["duration_seconds"]["mean"])
        / control_stats["duration_seconds"]["mean"] * 100
    ) if control_stats["duration_seconds"]["mean"] > 0 else 0
    
    # Quality comparison
    success_diff = treatment_stats["success_rate"] - control_stats["success_rate"]
    completion_diff = treatment_stats["completion_rate"] - control_stats["completion_rate"]
    
    return {
        "control": control_stats,
        "treatment": treatment_stats,
        "reductions": {
            "token_reduction_pct": round(token_reduction, 2),
            "cost_reduction_pct": round(cost_reduction, 2),
            "iteration_reduction_pct": round(iteration_reduction, 2),
            "duration_change_pct": round(duration_change, 2),
        },
        "quality": {
            "success_rate_diff": round(success_diff * 100, 2),
            "completion_rate_diff": round(completion_diff * 100, 2),
            "quality_maintained": success_diff >= -0.05 and completion_diff >= -0.05,  # Allow 5% degradation
        },
        "sample_sizes": {
            "control": control_stats["count"],
            "treatment": treatment_stats["count"],
        },
    }


def generate_report(experiment_names: list[str] | None = None, days: int = 7, output_format: str = "text") -> dict[str, Any]:
    """Generate comprehensive validation report."""
    framework = get_ab_framework()
    
    if experiment_names is None:
        experiment_names = list(framework._experiments.keys())
    
    report = {
        "generated_at": datetime.now().isoformat(),
        "period_days": days,
        "experiments": {},
        "summary": {
            "total_experiments": len(experiment_names),
            "experiments_with_data": 0,
            "experiments_meeting_target": 0,
        },
    }
    
    for exp_name in experiment_names:
        metrics = load_experiment_metrics(exp_name, days)
        if not metrics:
            report["experiments"][exp_name] = {"status": "no_data"}
            continue
        
        # Split by variant
        control = [m for m in metrics if m.variant == "control"]
        treatment = [m for m in metrics if m.variant == "treatment"]
        
        comparison = compare_variants(control, treatment)
        report["experiments"][exp_name] = comparison
        
        if "error" not in comparison:
            report["summary"]["experiments_with_data"] += 1
            # Check if 50% token reduction target met
            if comparison["reductions"]["token_reduction_pct"] >= 50:
                report["summary"]["experiments_meeting_target"] += 1
    
    return report


def print_text_report(report: dict[str, Any]) -> None:
    """Print human-readable text report."""
    print("=" * 80)
    print("TOKEN OPTIMIZATION VALIDATION REPORT")
    print("=" * 80)
    print(f"Generated: {report['generated_at']}")
    print(f"Period: Last {report['period_days']} days")
    print()
    
    print("SUMMARY")
    print("-" * 40)
    s = report["summary"]
    print(f"  Total experiments:     {s['total_experiments']}")
    print(f"  With data:             {s['experiments_with_data']}")
    print(f"  Meeting 50% target:    {s['experiments_meeting_target']}")
    print()
    
    for exp_name, data in report["experiments"].items():
        print(f"EXPERIMENT: {exp_name}")
        print("-" * 40)
        
        if data.get("status") == "no_data":
            print("  No data collected yet")
            print()
            continue
        
        if "error" in data:
            print(f"  Error: {data['error']}")
            print()
            continue
        
        c = data["control"]
        t = data["treatment"]
        r = data["reductions"]
        q = data["quality"]
        sz = data["sample_sizes"]
        
        print(f"  Sample sizes:    Control={sz['control']}, Treatment={sz['treatment']}")
        print()
        print("  TOKEN USAGE:")
        print(f"    Control:      {c['tokens']['mean']:,.0f} tokens (median: {c['tokens']['median']:,.0f})")
        print(f"    Treatment:    {t['tokens']['mean']:,.0f} tokens (median: {t['tokens']['median']:,.0f})")
        print(f"    Reduction:    {r['token_reduction_pct']:+.1f}%")
        print()
        print("  COST (USD):")
        print(f"    Control:      ${c['cost_usd']['mean']:.6f} (total: ${c['cost_usd']['total']:.4f})")
        print(f"    Treatment:    ${t['cost_usd']['mean']:.6f} (total: ${t['cost_usd']['total']:.4f})")
        print(f"    Reduction:    {r['cost_reduction_pct']:+.1f}%")
        print()
        print("  ITERATIONS:")
        print(f"    Control:      {c['iterations']['mean']:.1f} (median: {c['iterations']['median']:.1f})")
        print(f"    Treatment:    {t['iterations']['mean']:.1f} (median: {t['iterations']['median']:.1f})")
        print(f"    Change:       {r['iteration_reduction_pct']:+.1f}%")
        print()
        print("  DURATION:")
        print(f"    Control:      {c['duration_seconds']['mean']:.1f}s")
        print(f"    Treatment:    {t['duration_seconds']['mean']:.1f}s")
        print(f"    Change:       {r['duration_change_pct']:+.1f}%")
        print()
        print("  QUALITY:")
        print(f"    Success rate:     Control={c['success_rate']*100:.1f}%, Treatment={t['success_rate']*100:.1f}% ({q['success_rate_diff']:+.1f}%)")
        print(f"    Completion rate:  Control={c['completion_rate']*100:.1f}%, Treatment={t['completion_rate']*100:.1f}% ({q['completion_rate_diff']:+.1f}%)")
        print(f"    Quality maintained: {'YES' if q['quality_maintained'] else 'NO'}")
        print()
        
        # Target assessment
        target_met = r['token_reduction_pct'] >= 50
        quality_ok = q['quality_maintained']
        print(f"  TARGET (50% token reduction): {'MET' if target_met else 'NOT MET'} ({r['token_reduction_pct']:.1f}%)")
        print(f"  QUALITY GATE:                 {'PASSED' if quality_ok else 'FAILED'}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Validate token optimization experiments")
    parser.add_argument("--days", type=int, default=7, help="Days of data to analyze")
    parser.add_argument("--experiments", nargs="+", help="Specific experiments to analyze")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--target", type=float, default=50.0, help="Token reduction target percentage")
    
    args = parser.parse_args()
    
    report = generate_report(
        experiment_names=args.experiments,
        days=args.days,
        output_format=args.format,
    )
    
    if args.format == "json":
        output = json.dumps(report, indent=2, default=str)
    else:
        # Capture text output
        import io
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        print_text_report(report)
        sys.stdout = old_stdout
        output = buffer.getvalue()
    
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        print(output)
    
    # Exit code based on target
    if args.format == "text" or not args.output:
        # Check if any experiment meets target
        any_met = any(
            exp.get("reductions", {}).get("token_reduction_pct", 0) >= args.target
            for exp in report["experiments"].values()
            if "reductions" in exp
        )
        sys.exit(0 if any_met else 1)


if __name__ == "__main__":
    main()