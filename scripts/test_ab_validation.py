#!/usr/bin/env python3
"""Quick validation test - generates synthetic A/B test data and runs comparison."""

from __future__ import annotations

import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_company.executor.ab_testing import (
    get_ab_framework,
    ExperimentMetrics,
    record_experiment_metrics,
)


def generate_synthetic_data():
    """Generate synthetic A/B test data for validation."""
    framework = get_ab_framework()
    
    # Enable all experiments at 50% split
    for exp_name in framework._experiments:
        framework.enable_experiment(exp_name, 0.5)
    
    print("Generating synthetic A/B test data...")
    
    # Control group: higher tokens (simulating baseline)
    control_base_tokens = 8000
    control_variance = 2000
    
    # Treatment group: 50-60% reduction
    treatment_reduction = 0.55  # 55% reduction
    
    for i in range(100):
        task_id = f"test-task-{i:04d}"
        agent_name = random.choice(["lead-backend", "lead-frontend", "senior-backend", "specialist-api"])
        
        # Determine variant
        for exp_name in framework._experiments:
            variant = framework.get_variant(exp_name, agent_name, task_id)
            
            # Generate metrics
            if variant == "control":
                total_tokens = int(random.gauss(control_base_tokens, control_variance))
                total_tokens = max(2000, total_tokens)
            else:
                total_tokens = int(random.gauss(control_base_tokens * (1 - treatment_reduction), control_variance * 0.5))
                total_tokens = max(1000, total_tokens)
            
            prompt_tokens = int(total_tokens * 0.7)
            completion_tokens = total_tokens - prompt_tokens
            cost = total_tokens * 0.000001  # ~$1/1M tokens
            iterations = random.randint(3, 8)
            duration = random.uniform(10, 60)
            
            # Quality: treatment slightly better or equal
            success = random.random() > 0.05
            completion = random.random() > 0.10
            
            metrics = ExperimentMetrics(
                experiment_name=exp_name,
                variant=variant,
                task_id=task_id,
                agent_name=agent_name,
                timestamp=datetime.now(timezone.utc).isoformat(),
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                cost_usd=cost,
                iterations=iterations,
                duration_seconds=duration,
                success=success,
                task_completed=completion,
            )
            record_experiment_metrics(metrics)
    
    # Flush
    framework._flush_metrics()
    print("Synthetic data generated and flushed.")


def run_validation():
    """Run the validation script."""
    import subprocess
    
    result = subprocess.run([
        sys.executable, "scripts/validate_token_optimization.py",
        "--days", "1",
        "--format", "text"
    ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    print(f"Exit code: {result.returncode}")


if __name__ == "__main__":
    generate_synthetic_data()
    run_validation()