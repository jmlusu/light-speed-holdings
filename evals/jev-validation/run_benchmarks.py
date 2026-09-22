#!/usr/bin/env python3
"""
Jev Validation Framework
Run benchmarks comparing Jev vs LLM vs Deterministic baselines.
"""

import json
import asyncio
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
from pathlib import Path
import statistics

# ============================================================================
# Data Models
# ============================================================================

@dataclass
class DecisionResult:
    """Result from a decision primitive."""
    value: Any
    probabilities: List[float]
    confidence: float
    question_type: str  # "choice", "score", "noul"

@dataclass
class BenchmarkResult:
    """Results for a single workflow benchmark."""
    workflow: str
    sample_size: int
    jev_agreement_pct: float
    llm_agreement_pct: float
    ece: float
    brier_score: float
    latency_p50_ms: float
    latency_p99_ms: float
    cost_per_decision_usd: float
    confidence_distribution: Dict[str, float]
    false_positive_rate: float
    false_negative_rate: float
    details: List[Dict[str, Any]]

@dataclass
class WorkflowSpec:
    """Specification for a validation workflow."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    questions: Dict[str, Dict[str, Any]]
    ground_truth_path: str
    success_criteria: Dict[str, float]


# ============================================================================
# Provider Interfaces
# ============================================================================

class DecisionProvider(ABC):
    """Abstract interface for decision providers (Jev, LLM, etc.)."""
    
    @abstractmethod
    async def ask_batch(self, questions: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, DecisionResult]:
        """Ask multiple questions in parallel against a state."""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        pass
    
    @property
    @abstractmethod
    def model_id(self) -> str:
        pass


class JevProvider(DecisionProvider):
    """TypeSafe Jev provider (to be implemented when SDK available)."""
    
    def __init__(self, api_key: str, model: str = "jev-1.13.0"):
        self.api_key = api_key
        self._model_id = model
        # TODO: Initialize TypeSafe SDK client
    
    async def ask_batch(self, questions: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, DecisionResult]:
        # TODO: Implement via TypeSafe SDK
        # For now, return mock results for framework testing
        results = {}
        for q_name, q_spec in questions.items():
            q_type = q_spec.get("type", "choice")
            if q_type == "choice":
                criteria = q_spec.get("criteria", {})
                results[q_name] = DecisionResult(
                    value=list(criteria.keys())[0],
                    probabilities=[0.9, 0.1],
                    confidence=0.9,
                    question_type="choice"
                )
            elif q_type == "score":
                criteria = q_spec.get("criteria", [])
                results[q_name] = DecisionResult(
                    value=criteria[1] if len(criteria) > 1 else criteria[0],
                    probabilities=[0.1, 0.7, 0.2],
                    confidence=0.7,
                    question_type="score"
                )
            elif q_type == "noul":
                results[q_name] = DecisionResult(
                    value=0.85,
                    probabilities=[0.85, 0.15],
                    confidence=0.85,
                    question_type="noul"
                )
        return results
    
    async def health_check(self) -> bool:
        return True
    
    @property
    def model_id(self) -> str:
        return self._model_id


class LLMProvider(DecisionProvider):
    """LLM-based decision provider using structured output (fallback)."""
    
    def __init__(self, model: str = "gpt-5.6-terra"):
        self._model_id = model
        # TODO: Initialize LLM client with Instructor
    
    async def ask_batch(self, questions: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, DecisionResult]:
        # TODO: Implement via LLM with structured output
        results = {}
        for q_name, q_spec in questions.items():
            q_type = q_spec.get("type", "choice")
            if q_type == "choice":
                criteria = q_spec.get("criteria", {})
                results[q_name] = DecisionResult(
                    value=list(criteria.keys())[0],
                    probabilities=[0.85, 0.15],
                    confidence=0.85,
                    question_type="choice"
                )
            elif q_type == "score":
                criteria = q_spec.get("criteria", [])
                results[q_name] = DecisionResult(
                    value=criteria[1] if len(criteria) > 1 else criteria[0],
                    probabilities=[0.15, 0.7, 0.15],
                    confidence=0.7,
                    question_type="score"
                )
            elif q_type == "noul":
                results[q_name] = DecisionResult(
                    value=0.8,
                    probabilities=[0.8, 0.2],
                    confidence=0.8,
                    question_type="noul"
                )
        return results
    
    async def health_check(self) -> bool:
        return True
    
    @property
    def model_id(self) -> str:
        return self._model_id


class DeterministicProvider(DecisionProvider):
    """Deterministic rule-based provider (baseline)."""
    
    def __init__(self):
        self._model_id = "deterministic-rules"
    
    async def ask_batch(self, questions: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, DecisionResult]:
        # Simple rule-based decisions for baseline
        results = {}
        for q_name, q_spec in questions.items():
            q_type = q_spec.get("type", "choice")
            if q_type == "choice":
                criteria = q_spec.get("criteria", {})
                results[q_name] = DecisionResult(
                    value=list(criteria.keys())[0],
                    probabilities=[1.0],
                    confidence=1.0,
                    question_type="choice"
                )
            elif q_type == "score":
                criteria = q_spec.get("criteria", [])
                results[q_name] = DecisionResult(
                    value=criteria[len(criteria)//2],
                    probabilities=[1.0],
                    confidence=1.0,
                    question_type="score"
                )
            elif q_type == "noul":
                results[q_name] = DecisionResult(
                    value=0.5,
                    probabilities=[0.5, 0.5],
                    confidence=0.5,
                    question_type="noul"
                )
        return results
    
    async def health_check(self) -> bool:
        return True
    
    @property
    def model_id(self) -> str:
        return self._model_id


# ============================================================================
# Evaluation Metrics
# ============================================================================

def expected_calibration_error(predictions: List[float], labels: List[int], n_bins: int = 10) -> float:
    """Calculate Expected Calibration Error (ECE)."""
    if len(predictions) != len(labels):
        raise ValueError("Predictions and labels must have same length")
    
    bin_boundaries = [i / n_bins for i in range(n_bins + 1)]
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]
    
    ece = 0.0
    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
        in_bin = [i for i, p in enumerate(predictions) if bin_lower <= p < bin_upper]
        if not in_bin:
            continue
        
        bin_accuracy = sum(labels[i] for i in in_bin) / len(in_bin)
        bin_confidence = sum(predictions[i] for i in in_bin) / len(in_bin)
        ece += (len(in_bin) / len(predictions)) * abs(bin_accuracy - bin_confidence)
    
    return ece


def brier_score(predictions: List[float], labels: List[int]) -> float:
    """Calculate Brier Score for probabilistic predictions."""
    if len(predictions) != len(labels):
        raise ValueError("Predictions and labels must have same length")
    return sum((p - l) ** 2 for p, l in zip(predictions, labels)) / len(predictions)


def calculate_agreement(pred_values: List[Any], true_values: List[Any]) -> float:
    """Calculate agreement rate between predictions and ground truth."""
    if len(pred_values) != len(true_values):
        raise ValueError("Lengths must match")
    matches = sum(1 for p, t in zip(pred_values, true_values) if p == t)
    return matches / len(pred_values) if pred_values else 0.0


# ============================================================================
# Benchmark Runner
# ============================================================================

class BenchmarkRunner:
    """Run benchmarks comparing providers on workflows."""
    
    def __init__(self, output_dir: str = "evals/jev-validation/results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.providers: Dict[str, DecisionProvider] = {}
    
    def register_provider(self, name: str, provider: DecisionProvider):
        self.providers[name] = provider
    
    async def run_workflow(self, workflow: WorkflowSpec, provider_name: str) -> BenchmarkResult:
        """Run benchmark for a single workflow with a provider."""
        provider = self.providers[provider_name]
        
        # Load ground truth
        with open(workflow.ground_truth_path) as f:
            ground_truth = json.load(f)
        
        results = []
        latencies = []
        costs = []
        
        for i, sample in enumerate(ground_truth["samples"]):
            state = sample["input"]
            expected = sample["expected"]
            
            start = time.perf_counter()
            try:
                predictions = await provider.ask_batch(workflow.questions, state)
                latency_ms = (time.perf_counter() - start) * 1000
            except Exception as e:
                print(f"Error on sample {i}: {e}")
                continue
            
            latencies.append(latency_ms)
            costs.append(0.0004)  # Jev estimated cost
            
            # Extract predictions for comparison
            pred_values = {}
            pred_confidences = {}
            for q_name, result in predictions.items():
                pred_values[q_name] = result.value
                pred_confidences[q_name] = result.confidence
            
            results.append({
                "sample_index": i,
                "predictions": pred_values,
                "confidences": pred_confidences,
                "expected": expected,
                "latency_ms": latency_ms
            })
        
        # Calculate metrics
        # For agreement, compare primary question (first in dict)
        primary_q = list(workflow.questions.keys())[0]
        pred_primary = [r["predictions"].get(primary_q) for r in results]
        true_primary = [r["expected"].get(primary_q) for r in results]
        
        agreement = calculate_agreement(pred_primary, true_primary)
        
        # Calibration metrics (for primary question)
        confidences = [r["confidences"].get(primary_q, 0.5) for r in results]
        # Convert to binary for ECE (correct/incorrect)
        binary_labels = [1 if p == t else 0 for p, t in zip(pred_primary, true_primary)]
        
        ece = expected_calibration_error(confidences, binary_labels)
        brier = brier_score(confidences, binary_labels)
        
        # Confidence distribution
        conf_dist = {
            "0.9-1.0": sum(1 for c in confidences if c >= 0.9) / len(confidences),
            "0.8-0.9": sum(1 for c in confidences if 0.8 <= c < 0.9) / len(confidences),
            "0.7-0.8": sum(1 for c in confidences if 0.7 <= c < 0.8) / len(confidences),
            "<0.7": sum(1 for c in confidences if c < 0.7) / len(confidences),
        }
        
        # False positive/negative rates (for binary questions)
        fp_rate = 0.0
        fn_rate = 0.0
        if len(set(true_primary)) == 2:  # Binary classification
            tp = sum(1 for p, t in zip(pred_primary, true_primary) if p == t == true_primary[0])
            fp = sum(1 for p, t in zip(pred_primary, true_primary) if p == true_primary[0] and t != true_primary[0])
            fn = sum(1 for p, t in zip(pred_primary, true_primary) if p != true_primary[0] and t == true_primary[0])
            tn = sum(1 for p, t in zip(pred_primary, true_primary) if p == t != true_primary[0])
            
            fp_rate = fp / (fp + tn) if (fp + tn) > 0 else 0.0
            fn_rate = fn / (fn + tp) if (fn + tp) > 0 else 0.0
        
        benchmark = BenchmarkResult(
            workflow=workflow.name,
            sample_size=len(results),
            jev_agreement_pct=agreement if provider_name == "jev" else 0,
            llm_agreement_pct=agreement if provider_name == "llm" else 0,
            ece=ece,
            brier_score=brier,
            latency_p50_ms=statistics.median(latencies) if latencies else 0,
            latency_p99_ms=sorted(latencies)[int(len(latencies) * 0.99)] if latencies else 0,
            cost_per_decision_usd=statistics.mean(costs) if costs else 0,
            confidence_distribution=conf_dist,
            false_positive_rate=fp_rate,
            false_negative_rate=fn_rate,
            details=results
        )
        
        # Save results
        output_file = self.output_dir / f"{workflow.name}_{provider_name}.json"
        with open(output_file, "w") as f:
            json.dump(asdict(benchmark), f, indent=2, default=str)
        
        return benchmark
    
    async def run_all_workflows(self, workflows: List[WorkflowSpec]) -> Dict[str, List[BenchmarkResult]]:
        """Run all workflows on all providers."""
        all_results = {}
        
        for workflow in workflows:
            print(f"\n=== Benchmarking {workflow.name} ===")
            workflow_results = []
            
            for provider_name in self.providers:
                print(f"  Running {provider_name}...")
                result = await self.run_workflow(workflow, provider_name)
                workflow_results.append(result)
                print(f"    Agreement: {result.jev_agreement_pct if provider_name == 'jev' else result.llm_agreement_pct:.2%}")
                print(f"    ECE: {result.ece:.4f}")
                print(f"    Latency p50: {result.latency_p50_ms:.1f}ms")
            
            all_results[workflow.name] = workflow_results
        
        return all_results
    
    def generate_comparison_report(self, results: Dict[str, List[BenchmarkResult]]) -> str:
        """Generate markdown comparison report."""
        lines = [
            "# Jev Validation Comparison Analysis",
            "",
            f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary Table",
            "",
            "| Workflow | Jev Agreement | LLM Agreement | Deterministic Agreement | Jev ECE | LLM ECE | Jev Latency p50 | LLM Latency p50 | Jev Cost | LLM Cost |",
            "|----------|---------------|---------------|------------------------|---------|---------|-----------------|-----------------|----------|----------|"
        ]
        
        for workflow_name, workflow_results in results.items():
            jev = next((r for r in workflow_results if r.workflow == workflow_name and "jev" in str(r)), None)
            llm = next((r for r in workflow_results if r.workflow == workflow_name and "llm" in str(r)), None)
            det = next((r for r in workflow_results if r.workflow == workflow_name and "det" in str(r)), None)
            
            # Find by provider name in details or re-run logic
            jev_r = next((r for r in workflow_results if "jev" in str(r.__dict__).lower()), None)
            llm_r = next((r for r in workflow_results if "llm" in str(r.__dict__).lower()), None)
            det_r = next((r for r in workflow_results if "det" in str(r.__dict__).lower()), None)
            
            # Simplified: just use first three
            if len(workflow_results) >= 3:
                jev_r, llm_r, det_r = workflow_results[0], workflow_results[1], workflow_results[2]
            
            jev_agree = f"{jev_r.jev_agreement_pct:.1%}" if jev_r else "N/A"
            llm_agree = f"{llm_r.llm_agreement_pct:.1%}" if llm_r else "N/A"
            det_agree = f"{det_r.jev_agreement_pct:.1%}" if det_r else "N/A"
            jev_ece = f"{jev_r.ece:.4f}" if jev_r else "N/A"
            llm_ece = f"{llm_r.ece:.4f}" if llm_r else "N/A"
            jev_lat = f"{jev_r.latency_p50_ms:.0f}ms" if jev_r else "N/A"
            llm_lat = f"{llm_r.latency_p50_ms:.0f}ms" if llm_r else "N/A"
            jev_cost = f"${jev_r.cost_per_decision_usd:.6f}" if jev_r else "N/A"
            llm_cost = f"${llm_r.cost_per_decision_usd:.6f}" if llm_r else "N/A"
            
            lines.append(f"| {workflow_name} | {jev_agree} | {llm_agree} | {det_agree} | {jev_ece} | {llm_ece} | {jev_lat} | {llm_lat} | {jev_cost} | {llm_cost} |")
        
        lines.extend([
            "",
            "## Decision Gate",
            "",
            "**Criteria**: Jev >=90% LLM agreement on >=4/5 workflows with ECE < 0.1",
            "",
            "| Workflow | Jev Agreement | ECE | GO? |",
            "|----------|---------------|-----|-----|"
        ])
        
        pass_count = 0
        for workflow_name, workflow_results in results.items():
            jev_r = workflow_results[0] if workflow_results else None
            if jev_r:
                goes = "[PASS]" if (jev_r.jev_agreement_pct >= 0.9 and jev_r.ece < 0.1) else "[FAIL]"
                if goes == "✅":
                    pass_count += 1
                lines.append(f"| {workflow_name} | {jev_r.jev_agreement_pct:.1%} | {jev_r.ece:.4f} | {goes} |")
        
        lines.append(f"| **Pass Count** | **{pass_count}/5** | | |")
        lines.append("")
        lines.append("## Recommendation")
        if pass_count >= 4:
            lines.append("[GO] - Proceed to Phase 2 (Prototype)")
        else:
            lines.append("[NO-GO] - Execute fallback plan (JEV-FB-01 through JEV-FB-04)")
        
        return "\n".join(lines)


# ============================================================================
# Workflow Definitions (from workflows.md)
# ============================================================================

def load_workflows() -> List[WorkflowSpec]:
    """Load workflow specifications."""
    workflows = [
        WorkflowSpec(
            name="intent_routing",
            description="Classify incoming task to correct specialist agent",
            input_schema={"task": "str", "context": "object", "history": "array"},
            questions={
                "intent": {"type": "choice", "criteria": {
                    "research": "Information gathering, analysis, synthesis",
                    "coding": "Code generation, refactoring, debugging",
                    "creative": "Writing, design, content creation",
                    "ops": "Infrastructure, deployment, monitoring",
                    "other": "General inquiries, coordination"
                }},
                "complexity": {"type": "score", "criteria": ["trivial", "standard", "expert", "novel"]},
                "risk": {"type": "choice", "criteria": {
                    "low": "Read-only, reversible",
                    "medium": "Write operations, reversible",
                    "high": "External API, data modification",
                    "critical": "Irreversible, production, security"
                }},
                "requires_human": {"type": "noul", "instructions": "Requires human approval?"}
            },
            ground_truth_path="evals/jev-validation/ground_truth/intent_routing.json",
            success_criteria={"agreement": 0.9, "ece": 0.1}
        ),
        WorkflowSpec(
            name="tool_verification",
            description="Verify tool arguments before execution",
            input_schema={"tool_name": "str", "tool_schema": "object", "arguments": "object", "task_context": "str"},
            questions={
                "tool_appropriate": {"type": "choice", "criteria": {
                    "yes": "Tool matches intent",
                    "no": "Tool inappropriate",
                    "ambiguous": "Unclear"
                }},
                "args_valid": {"type": "noul", "instructions": "Arguments match schema and intent?"},
                "policy_compliant": {"type": "choice", "criteria": {
                    "compliant": "Follows all policies",
                    "violates": "Violates policies",
                    "needs_review": "Borderline"
                }},
                "side_effect_risk": {"type": "score", "criteria": ["none", "reversible", "audited", "irreversible"]}
            },
            ground_truth_path="evals/jev-validation/ground_truth/tool_verification.json",
            success_criteria={"agreement": 0.9, "ece": 0.1}
        ),
        WorkflowSpec(
            name="trace_scoring",
            description="Score agent traces for anomalies and quality",
            input_schema={"trace_id": "str", "task": "str", "steps": "array", "final_output": "str"},
            questions={
                "anomaly_score": {"type": "score", "criteria": ["normal", "unusual", "suspicious", "malicious"]},
                "task_completion": {"type": "noul", "instructions": "Achieved stated objective?"},
                "policy_adherence": {"type": "choice", "criteria": {
                    "full": "All steps comply",
                    "minor_deviation": "Minor deviations",
                    "major_violation": "Significant violation"
                }},
                "tool_efficiency": {"type": "score", "criteria": ["optimal", "redundant", "excessive", "failed"]}
            },
            ground_truth_path="evals/jev-validation/ground_truth/trace_scoring.json",
            success_criteria={"agreement": 0.9, "ece": 0.1}
        ),
        WorkflowSpec(
            name="customer_triage",
            description="Classify and prioritize customer support requests",
            input_schema={"customer_tier": "str", "subject": "str", "body": "str", "history": "array"},
            questions={
                "category": {"type": "choice", "criteria": {
                    "billing": "Payment, subscription, invoices",
                    "technical": "Bugs, errors, config",
                    "security": "Vulnerabilities, access, compliance",
                    "feature": "Feature requests",
                    "general": "How-to, account management"
                }},
                "urgency": {"type": "score", "criteria": ["routine", "urgent", "critical", "catastrophic"]},
                "is_known_issue": {"type": "noul", "instructions": "Matches known issue?"},
                "requires_escalation": {"type": "noul", "instructions": "Requires immediate human escalation?"}
            },
            ground_truth_path="evals/jev-validation/ground_truth/customer_triage.json",
            success_criteria={"agreement": 0.9, "ece": 0.1}
        ),
        WorkflowSpec(
            name="policy_compliance",
            description="Verify actions comply with organizational policies",
            input_schema={"action_type": "str", "actor": "str", "resource": "str", "parameters": "object"},
            questions={
                "compliance": {"type": "choice", "criteria": {
                    "compliant": "Fully complies",
                    "conditional": "Compliant with conditions",
                    "non_compliant": "Violates policies",
                    "insufficient_info": "Cannot determine"
                }},
                "risk_level": {"type": "score", "criteria": ["none", "low", "medium", "high", "critical"]},
                "requires_approval": {"type": "noul", "instructions": "Requires human approval per policy?"},
                "policy_conflict": {"type": "noul", "instructions": "Conflicting policies create ambiguity?"}
            },
            ground_truth_path="evals/jev-validation/ground_truth/policy_compliance.json",
            success_criteria={"agreement": 0.9, "ece": 0.1}
        )
    ]
    return workflows


# ============================================================================
# Main
# ============================================================================

async def main():
    runner = BenchmarkRunner()
    
    # Register providers
    runner.register_provider("jev", JevProvider(api_key="test-key"))
    runner.register_provider("llm", LLMProvider())
    runner.register_provider("deterministic", DeterministicProvider())
    
    # Load workflows
    workflows = load_workflows()
    
    # Create ground truth directories
    for wf in workflows:
        gt_path = Path(wf.ground_truth_path)
        gt_path.parent.mkdir(parents=True, exist_ok=True)
        if not gt_path.exists():
            # Create template ground truth file
            template = {
                "workflow": wf.name,
                "samples": [
                    {"input": {"task": "example task"}, "expected": {list(wf.questions.keys())[0]: "example"}}
                ]
            }
            with open(gt_path, "w") as f:
                json.dump(template, f, indent=2)
            print(f"Created template: {gt_path}")
    
    # Run benchmarks
    print("Starting Jev validation benchmarks...")
    results = await runner.run_all_workflows(workflows)
    
    # Generate report
    report = runner.generate_comparison_report(results)
    report_path = Path("evals/jev-validation/comparison-analysis.md")
    with open(report_path, "w") as f:
        f.write(report)
    
    print(f"\nReport saved to {report_path}")
    print("\n" + "="*60)
    print(report)


if __name__ == "__main__":
    asyncio.run(main())