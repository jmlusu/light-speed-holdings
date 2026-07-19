# Phase 3 AI Strategy

**Document Version:** 1.0
**Author:** Chief AI Officer (CAIO)
**Date:** July 19, 2026
**Status:** Draft

---

## 1 Executive Summary

Phase 3 transforms AI Company Builder from a capable multi-provider LLM orchestrator into an intelligent, self-optimizing AI platform. This strategy builds on the solid foundation established in Phases 1-2 (multi-provider support, streaming, circuit breakers, cost tracking) and introduces advanced capabilities that enable agents to reason more effectively, learn from outcomes, and operate within strict cost boundaries.

**Key Phase 3 Objectives:**
- Achieve precise token-level cost control with sub-cent accuracy
- Implement prompt engineering patterns that improve task success rates by 25-40%
- Enable context-aware model routing that minimizes cost while maintaining quality
- Introduce retrieval-augmented generation (RAG) for knowledge-intensive tasks
- Build agent self-improvement loops based on outcome tracking

---

## 2 Current AI Capabilities Assessment

### 2.1 LLM Infrastructure (Strengths)

| Component | Status | Assessment |
|-----------|--------|------------|
| **Multi-Provider Support** | ✅ Production | OpenAI-compatible (OpenCode, Deepseek), Anthropic, Ollama |
| **Model Router** | ✅ Production | 3-tier routing (fast/standard/premium) with per-agent overrides |
| **Streaming** | ✅ Production | SSE/NDJSON parsing for all providers |
| **Circuit Breaker** | ✅ Production | 3-failure threshold, 60s recovery, state machine |
| **Cost Tracker** | ✅ Production | JSONL logging, daily/task budgets, per-model pricing |
| **JSON Parser** | ✅ Production | 3-strategy fallback (direct, markdown, extraction) |
| **Retry Logic** | ✅ Production | 5-attempt retry with provider fallback |

### 2.2 LLM Infrastructure (Gaps)

| Gap | Impact | Phase 3 Priority |
|-----|--------|------------------|
| **No token counting** | Cost estimation relies on provider-reported counts only | **P0 - Critical** |
| **No pre-request cost validation** | Cannot prevent budget overruns before they happen | **P0 - Critical** |
| **Static prompt templates** | No optimization based on task characteristics | **P1 - High** |
| **No quality feedback loop** | Cannot learn from task success/failure | **P1 - High** |
| **No RAG integration** | Context window limits knowledge-intensive tasks | **P2 - Medium** |
| **No provider health metrics** | Circuit breaker lacks historical performance data | **P2 - Medium** |

### 2.3 Provider Ecosystem

| Provider | Models | Cost Profile | Strengths |
|----------|--------|--------------|-----------|
| **OpenCode** | big-pickle | Medium | Versatile, good reasoning |
| **Deepseek** | deepseek-chat, deepseek-coder | Low | Excellent cost/performance ratio |
| **Ollama** | llama3.1:8b, llama3.1:70b | Free | Local, no API costs, privacy |
| **OpenAI** | gpt-4o, gpt-4o-mini | High | Strong general capabilities |
| **Anthropic** | claude-sonnet-4-20250514 | High | Superior reasoning, safety |

---

## 3 Phase 3 AI Enhancements Roadmap

### 3.1 Token Counting Integration (P0)

**Objective:** Enable accurate pre-request token counting to predict costs and enforce budgets.

**Implementation:**

```python
# src/ai_company/llm/token_counter.py
class TokenCounter:
    """Token counting with provider-specific implementations."""
    
    def __init__(self):
        self._counters: dict[str, BaseCounter] = {
            "openai_compatible": TikTokenCounter(),
            "anthropic": AnthropicTokenCounter(),
            "ollama": OllamaTokenCounter(),  # Uses tokenizer.json
        }
    
    def count_tokens(
        self,
        text: str,
        provider: str,
        model: str,
        role: str = "user"
    ) -> TokenCount:
        """Count tokens with provider-specific tokenizers."""
        counter = self._counters.get(provider)
        if not counter:
            # Fallback: approximate 1 token ≈ 4 characters
            return TokenCount(
                tokens=len(text) // 4,
                provider=provider,
                model=model,
            )
        return counter.count(text, model, role)
```

**Token Counting Strategies:**

| Provider | Tokenizer | Accuracy | Performance |
|----------|-----------|----------|-------------|
| OpenAI | tiktoken (cl100k_base) | 99% | Fast (~100k tokens/sec) |
| Anthropic | anthropic-tokenizer | 99% | Fast |
| Ollama | tokenizer.json (from model) | 95% | Medium |

**Dependencies:**
- `tiktoken>=0.7.0` for OpenAI models
- `transformers>=4.40.0` for Ollama tokenizers (optional, fallback to approximation)

**Integration Points:**
- `LLMClient.execute_task()` → Add token counting before API call
- `CostTracker.check_budget()` → Use predicted tokens for pre-validation
- `ModelRouter.resolve()` → Factor token estimates into routing decisions

---

### 3.2 Cost Calculation Per Request (P0)

**Objective:** Predict exact cost before making LLM calls and enforce budgets proactively.

**Implementation:**

```python
# src/ai_company/llm/cost_calculator.py
@dataclass(frozen=True)
class CostEstimate:
    """Pre-request cost estimate."""
    prompt_tokens: int
    completion_tokens: int  # Predicted based on task complexity
    estimated_cost_usd: float
    within_budget: bool
    budget_remaining_usd: float
    recommended_model: str | None  # If over budget, suggest cheaper alternative

class CostCalculator:
    """Calculates costs with cache-aware pricing."""
    
    def __init__(
        self,
        cost_tracker: CostTracker,
        token_counter: TokenCounter,
    ):
        self._tracker = cost_tracker
        self._counter = token_counter
        
        # Cache hit rates by model (from historical data)
        self._cache_hit_rates: dict[str, float] = {
            "gpt-4o": 0.30,  # 30% cache hit rate typical
            "claude-sonnet-4-20250514": 0.25,
            "deepseek-chat": 0.20,
        }
    
    def estimate_request(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
        provider: str,
        task_id: str,
        max_output_tokens: int = 4096,
    ) -> CostEstimate:
        """Estimate cost before making the API call."""
        # Count input tokens
        system_tokens = self._counter.count_tokens(
            system_prompt, provider, model, "system"
        )
        user_tokens = self._counter.count_tokens(
            user_prompt, provider, model, "user"
        )
        prompt_tokens = system_tokens.tokens + user_tokens.tokens
        
        # Predict output tokens based on task complexity
        completion_tokens = self._predict_output_tokens(
            user_prompt, model, max_output_tokens
        )
        
        # Calculate cost with cache discount
        base_cost = self._tracker.estimate_cost(
            model, prompt_tokens, completion_tokens
        )
        
        # Apply cache hit discount if applicable
        cache_rate = self._cache_hit_rates.get(model, 0.0)
        cached_cost = self._tracker.estimate_cost(
            model, prompt_tokens, completion_tokens
        ) * (1 - cache_rate * 0.5)  # 50% discount on cached tokens
        
        # Check budget
        within_budget, reason = self._tracker.check_budget(task_id, cached_cost)
        budget_remaining = self._tracker._task_budget - self._tracker._task_costs.get(task_id, 0.0)
        
        return CostEstimate(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            estimated_cost_usd=cached_cost,
            within_budget=within_budget,
            budget_remaining_usd=max(0, budget_remaining),
            recommended_model=self._suggest_cheaper_model(model, cached_cost, budget_remaining) if not within_budget else None,
        )
    
    def _predict_output_tokens(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
    ) -> int:
        """Predict output tokens based on task complexity."""
        # Simple heuristic: task complexity based on prompt length and keywords
        prompt_len = len(prompt)
        
        # Complex tasks tend to produce longer outputs
        complexity_factors = [
            ("explain", 1.5),
            ("analyze", 1.8),
            ("compare", 1.6),
            ("implement", 2.0),
            ("review", 1.3),
            ("summarize", 0.8),
        ]
        
        multiplier = 1.0
        prompt_lower = prompt.lower()
        for keyword, factor in complexity_factors:
            if keyword in prompt_lower:
                multiplier = max(multiplier, factor)
        
        # Base prediction: 10-30% of max tokens depending on complexity
        base_prediction = int(max_tokens * 0.2 * multiplier)
        
        # Clamp to reasonable bounds
        return min(max(base_prediction, 256), max_tokens)
    
    def _suggest_cheaper_model(
        self,
        current_model: str,
        estimated_cost: float,
        budget_remaining: float,
    ) -> str | None:
        """Suggest a cheaper model if over budget."""
        if estimated_cost <= budget_remaining:
            return None
        
        # Cost tiers (approximate)
        cost_tiers = [
            ("llama3.1:8b", 0.0),
            ("deepseek-chat", 0.001),
            ("gpt-4o-mini", 0.002),
            ("gpt-4o", 0.01),
            ("claude-sonnet-4-20250514", 0.02),
        ]
        
        # Find current tier
        current_tier = next(
            (i for i, (m, _) in enumerate(cost_tiers) if m == current_model),
            len(cost_tiers) - 1
        )
        
        # Find cheapest model within budget
        for i in range(current_tier - 1, -1, -1):
            model, _ = cost_tiers[i]
            test_cost = self._tracker.estimate_cost(model, 1000, 1000)
            if test_cost <= budget_remaining:
                return model
        
        return "llama3.1:8b"  # Ultimate fallback (free)
```

**Integration with ModelRouter:**

```python
# Enhanced routing decision
def resolve_with_cost_awareness(
    self,
    agent_name: str,
    priority: str,
    context: str | None,
    task_id: str,
    estimated_tokens: int,
) -> Route:
    """Route considering cost constraints."""
    base_route = self.resolve(agent_name, priority, context)
    
    # Check if base route fits budget
    estimate = self._cost_calculator.estimate_request(
        system_prompt="",
        user_prompt="",  # Would need actual prompt
        model=base_route.model,
        provider=base_route.provider,
        task_id=task_id,
    )
    
    if not estimate.within_budget and estimate.recommended_model:
        # Route to cheaper model
        return Route(
            provider=self._provider_for_model(estimate.recommended_model),
            model=estimate.recommended_model,
            tier="cost_override",
            reason=f"Budget constraint: {estimate.recommended_model} recommended",
        )
    
    return base_route
```

---

### 3.3 Prompt Engineering Improvements (P1)

**Objective:** Systematically optimize prompts for maximum agent efficacy across task types.

**3.3.1 System Prompt Architecture**

```python
# src/ai_company/llm/prompts/system_architect.py
class SystemPromptArchitect:
    """Builds optimized system prompts based on task characteristics."""
    
    def __init__(self):
        self._templates = self._load_templates()
        self._patterns = self._load_patterns()
    
    def build_prompt(
        self,
        agent_type: str,
        task_category: str,
        complexity: str,
        model: str,
    ) -> str:
        """Construct optimized system prompt."""
        # Base template
        template = self._templates.get(f"{agent_type}.{task_category}")
        if not template:
            template = self._templates.get(f"{agent_type}.default")
        
        # Apply chain-of-thought pattern for complex tasks
        if complexity == "high":
            template = self._apply_cot_pattern(template)
        
        # Apply model-specific optimizations
        template = self._optimize_for_model(template, model)
        
        return template
    
    def _apply_cot_pattern(self, prompt: str) -> str:
        """Add chain-of-thought instructions for complex reasoning."""
        return f"""{prompt}

When solving complex problems, use structured reasoning:

1. **Understand**: Break down the problem into components
2. **Plan**: Outline your approach before executing
3. **Execute**: Work through each step methodically
4. **Verify**: Check your work against requirements
5. **Report**: Present findings clearly with evidence

Always show your reasoning process. Cite specific examples when possible."""
    
    def _optimize_for_model(self, prompt: str, model: str) -> str:
        """Apply model-specific prompt optimizations."""
        optimizations = {
            "gpt-4o": "Use clear section headers. Be explicit about output format.",
            "claude-sonnet-4-20250514": "Be precise and direct. Use examples to clarify ambiguous requirements.",
            "deepseek-chat": "Keep instructions concise. Use bullet points for complex requirements.",
            "llama3.1:8b": "Use simple, direct language. Provide concrete examples.",
        }
        
        optimization = optimizations.get(model, "")
        if optimization:
            return f"{prompt}\n\n**Model Optimization Notes:** {optimization}"
        
        return prompt
```

**3.3.2 Chain-of-Thought Patterns**

| Pattern | Use Case | Implementation |
|---------|----------|----------------|
| **Zero-shot CoT** | Simple reasoning tasks | "Let's think step by step..." |
| **Few-shot CoT** | Complex analysis | Include 2-3 reasoning examples |
| **Tree-of-Thought** | Decision-making | Explore multiple paths, evaluate each |
| **Self-Consistency** | Critical decisions | Generate multiple answers, majority vote |
| **ReAct** | Tool-using agents | Interleave reasoning and actions |

**3.3.3 Prompt Templates Library**

```yaml
# prompts/templates.yaml
templates:
  code_review:
    system: |
      You are a senior software engineer conducting a code review.
      Focus on: correctness, performance, security, maintainability.
      Rate each issue: critical, major, minor, suggestion.
    patterns:
      - chain_of_thought
      - structured_output
  
  data_analysis:
    system: |
      You are a data analyst examining structured data.
      Process: summarize → identify patterns → explain implications.
      Always support claims with specific data points.
    patterns:
      - few_shot_cot
      - evidence_based
  
  strategic_planning:
    system: |
      You are a strategic advisor evaluating business decisions.
      Framework: options → trade-offs → recommendation → risks.
      Consider short-term and long-term implications.
    patterns:
      - tree_of_thought
      - multi_perspective
```

---

### 3.4 Model Routing Enhancements (P1)

**Objective:** Implement context-aware routing that dynamically selects models based on task requirements, historical performance, and cost constraints.

**3.4.1 Context-Aware Routing**

```python
# src/ai_company/model_router_v2.py
@dataclass
class TaskContext:
    """Rich context for routing decisions."""
    agent_name: str
    task_type: str  # code, analysis, creative, etc.
    complexity: str  # low, medium, high
    estimated_tokens: int
    requires_tools: bool
    quality_requirements: str  # standard, high, critical
    cost_budget_usd: float | None
    historical_success_rate: float | None  # For this agent+model combo

class ModelRouterV2(ModelRouter):
    """Enhanced router with context-aware decisions."""
    
    def __init__(self, ...):
        super().__init__(...)
        self._performance_tracker = PerformanceTracker()
        self._cost_calculator = CostCalculator(...)
    
    def resolve_contextual(
        self,
        context: TaskContext,
    ) -> Route:
        """Resolve model based on rich task context."""
        # Layer 1: Quality requirements override
        if context.quality_requirements == "critical":
            return self._resolve_premium(context)
        
        # Layer 2: Cost-constrained routing
        if context.cost_budget_usd is not None:
            return self._resolve_cost_constrained(context)
        
        # Layer 3: Performance-based routing
        if context.historical_success_rate is not None:
            return self._resolve_performance_optimized(context)
        
        # Layer 4: Default tier routing
        return self.resolve(
            agent_name=context.agent_name,
            priority="medium",
        )
    
    def _resolve_cost_constrained(self, context: TaskContext) -> Route:
        """Find best model within cost budget."""
        # Get all viable models sorted by cost
        viable_models = self._get_viable_models(context)
        
        for model_info in viable_models:
            estimate = self._cost_calculator.estimate_request(
                system_prompt="",
                user_prompt="",
                model=model_info.model,
                provider=model_info.provider,
                task_id="",  # Would be actual task_id
                max_output_tokens=context.estimated_tokens,
            )
            
            if estimate.estimated_cost_usd <= context.cost_budget_usd:
                return Route(
                    provider=model_info.provider,
                    model=model_info.model,
                    tier="cost_optimized",
                    reason=f"Within budget: ${estimate.estimated_cost_usd:.4f}",
                )
        
        # Fallback to free tier
        return Route(
            provider="ollama",
            model="llama3.1:8b",
            tier="free",
            reason="Budget exhausted, using free tier",
        )
    
    def _resolve_performance_optimized(self, context: TaskContext) -> Route:
        """Select model with best historical success rate."""
        performance = self._performance_tracker.get_stats(
            agent=context.agent_name,
            task_type=context.task_type,
        )
        
        # Sort by success rate, then by cost (prefer cheaper on tie)
        best_model = max(
            performance.models,
            key=lambda m: (m.success_rate, -m.avg_cost),
        )
        
        return Route(
            provider=best_model.provider,
            model=best_model.model,
            tier="performance_optimized",
            reason=f"Highest success rate: {best_model.success_rate:.1%}",
        )
```

**3.4.2 Quality-Based Fallback**

```python
class QualityFallbackChain:
    """Intelligent fallback that considers quality degradation."""
    
    def __init__(self):
        self._quality_scores = {
            "gpt-4o": 0.92,
            "claude-sonnet-4-20250514": 0.94,
            "deepseek-chat": 0.85,
            "deepseek-coder": 0.88,
            "big-pickle": 0.87,
            "llama3.1:8b": 0.72,
            "llama3.1:70b": 0.82,
        }
    
    def get_fallback_chain(
        self,
        primary_model: str,
        min_quality_score: float = 0.80,
    ) -> list[str]:
        """Return ordered fallback models meeting quality threshold."""
        primary_score = self._quality_scores.get(primary_model, 0.80)
        
        # Filter models above quality threshold
        viable = [
            (model, score)
            for model, score in self._quality_scores.items()
            if score >= min_quality_score and model != primary_model
        ]
        
        # Sort by quality (descending), then cost (ascending)
        viable.sort(key=lambda x: (-x[1], self._get_cost(x[0])))
        
        return [model for model, _ in viable]
    
    def _get_cost(self, model: str) -> float:
        """Get relative cost for sorting."""
        costs = {
            "llama3.1:8b": 0,
            "llama3.1:70b": 0,
            "deepseek-chat": 1,
            "deepseek-coder": 2,
            "big-pickle": 3,
            "gpt-4o-mini": 4,
            "gpt-4o": 5,
            "claude-sonnet-4-20250514": 6,
        }
        return costs.get(model, 5)
```

---

### 3.5 Memory-Augmented Generation (RAG) (P2)

**Objective:** Enable agents to access and utilize organizational knowledge for context-rich responses.

**3.5.1 RAG Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline                              │
├─────────────────────────────────────────────────────────────┤
│  User Query                                                  │
│       │                                                      │
│       ▼                                                      │
│  ┌────────────┐     ┌────────────┐     ┌────────────┐      │
│  │  Query     │────▶│  Retriever │────▶│  Ranker    │      │
│  │  Embedder  │     │  (Vector)  │     │  (Cross-   │      │
│  └────────────┘     └────────────┘     │   Encoder) │      │
│                                        └────────────┘      │
│                                               │              │
│       ┌───────────────────────────────────────┘              │
│       ▼                                                      │
│  ┌────────────┐     ┌────────────┐     ┌────────────┐      │
│  │  Context   │────▶│  LLM with  │────▶│  Response  │      │
│  │  Assembler │     │  Context   │     │  with      │      │
│  └────────────┘     └────────────┘     │  Citations │      │
│                                        └────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

**3.5.2 Implementation**

```python
# src/ai_company/rag/retriever.py
class DocumentRetriever:
    """Retrieves relevant documents for context augmentation."""
    
    def __init__(
        self,
        vector_store: VectorStore,
        embedding_model: str = "text-embedding-3-small",
        top_k: int = 5,
        score_threshold: float = 0.7,
    ):
        self._store = vector_store
        self._embedding_model = embedding_model
        self._top_k = top_k
        self._score_threshold = score_threshold
    
    def retrieve(
        self,
        query: str,
        filters: dict[str, Any] | None = None,
    ) -> list[Document]:
        """Retrieve relevant documents for the query."""
        # Embed query
        query_embedding = self._embed(query)
        
        # Search vector store
        results = self._store.search(
            embedding=query_embedding,
            top_k=self._top_k,
            filters=filters,
        )
        
        # Filter by score threshold
        return [
            doc for doc, score in results
            if score >= self._score_threshold
        ]


# src/ai_company/rag/augmenter.py
class ContextAugmenter:
    """Augments prompts with retrieved context."""
    
    def __init__(
        self,
        retriever: DocumentRetriever,
        max_context_tokens: int = 4000,
    ):
        self._retriever = retriever
        self._max_context_tokens = max_context_tokens
    
    def augment_prompt(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
    ) -> tuple[str, str]:
        """Return augmented (system, user) prompts with context."""
        # Retrieve relevant documents
        documents = self._retriever.retrieve(user_prompt)
        
        if not documents:
            return system_prompt, user_prompt
        
        # Format context
        context = self._format_documents(documents)
        
        # Truncate if exceeds token limit
        context = self._truncate_context(context, model)
        
        # Augment system prompt
        augmented_system = f"""{system_prompt}

## Relevant Context
The following documents may help answer the user's question:

{context}

Use this context to inform your response. Cite specific documents when referencing information."""
        
        return augmented_system, user_prompt
    
    def _format_documents(self, documents: list[Document]) -> str:
        """Format documents into context string."""
        parts = []
        for i, doc in enumerate(documents, 1):
            parts.append(f"### Document {i}: {doc.metadata.get('title', 'Untitled')}")
            parts.append(f"Source: {doc.metadata.get('source', 'Unknown')}")
            parts.append(f"Relevance: {doc.score:.2f}")
            parts.append(doc.content[:1000])  # Truncate long docs
            parts.append("")
        
        return "\n".join(parts)
```

**3.5.3 Knowledge Sources for AI Company Builder**

| Source | Content | Update Frequency |
|--------|---------|------------------|
| `company/*.yaml` | Agent definitions, roles, responsibilities | On change |
| `docs/*.md` | Architecture, development guides | Weekly |
| `src/**/*.py` | Codebase context for technical tasks | On commit |
| `results/cost_log.jsonl` | Historical cost data | Real-time |
| `results/task_log.jsonl` | Task outcomes and success rates | Real-time |

---

### 3.6 Agent Self-Improvement (P2)

**Objective:** Enable agents to learn from outcomes and optimize their performance over time.

**3.6.1 Outcome Tracking**

```python
# src/ai_company/learning/outcome_tracker.py
@dataclass
class TaskOutcome:
    """Records the outcome of a task for learning."""
    task_id: str
    agent_name: str
    model_used: str
    prompt_hash: str  # Hash of the system prompt used
    
    # Task metrics
    success: bool
    quality_score: float  # 0.0 - 1.0
    completion_time_ms: int
    token_count: int
    cost_usd: float
    
    # Feedback signals
    human_feedback: str | None  # Explicit feedback
    implicit_signals: dict[str, Any]  # Retry count, revision requests, etc.
    
    # Context
    task_type: str
    complexity: str
    timestamp: str

class OutcomeTracker:
    """Tracks task outcomes for learning."""
    
    def __init__(self, results_dir: str = "results"):
        self._results_dir = Path(results_dir)
        self._outcomes: list[TaskOutcome] = []
        self._load_historical()
    
    def record_outcome(self, outcome: TaskOutcome) -> None:
        """Record a task outcome."""
        self._outcomes.append(outcome)
        self._append_log(outcome)
        self._update_model_stats(outcome)
    
    def _update_model_stats(self, outcome: TaskOutcome) -> None:
        """Update model performance statistics."""
        key = f"{outcome.model_used}.{outcome.task_type}"
        
        stats = self._model_stats.get(key, ModelStats())
        stats.total_tasks += 1
        stats.successes += 1 if outcome.success else 0
        stats.total_cost += outcome.cost_usd
        stats.total_tokens += outcome.token_count
        
        self._model_stats[key] = stats
```

**3.6.2 Learning Loop**

```python
# src/ai_company/learning/agent_learner.py
class AgentLearner:
    """Learns from outcomes to improve agent performance."""
    
    def __init__(
        self,
        outcome_tracker: OutcomeTracker,
        prompt_engineer: SystemPromptArchitect,
    ):
        self._tracker = outcome_tracker
        self._prompt_engineer = prompt_engineer
    
    def analyze_performance(
        self,
        agent_name: str,
        lookback_days: int = 30,
    ) -> PerformanceAnalysis:
        """Analyze agent performance over time."""
        outcomes = self._tracker.get_outcomes(
            agent=agent_name,
            days=lookback_days,
        )
        
        return PerformanceAnalysis(
            agent=agent_name,
            total_tasks=len(outcomes),
            success_rate=self._calc_success_rate(outcomes),
            avg_cost=self._calc_avg_cost(outcomes),
            avg_quality=self._calc_avg_quality(outcomes),
            cost_trend=self._calc_cost_trend(outcomes),
            quality_trend=self._calc_quality_trend(outcomes),
            model_breakdown=self._breakdown_by_model(outcomes),
            recommendations=self._generate_recommendations(outcomes),
        )
    
    def _generate_recommendations(
        self,
        outcomes: list[TaskOutcome],
    ) -> list[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Check for high-cost, low-quality model usage
        for model in set(o.model_used for o in outcomes):
            model_outcomes = [o for o in outcomes if o.model_used == model]
            avg_quality = sum(o.quality_score for o in model_outcomes) / len(model_outcomes)
            avg_cost = sum(o.cost_usd for o in model_outcomes) / len(model_outcomes)
            
            if avg_quality < 0.7 and avg_cost > 0.01:
                recommendations.append(
                    f"Consider replacing {model} for {model_outcomes[0].task_type} tasks: "
                    f"low quality ({avg_quality:.1%}) at high cost (${avg_cost:.4f})"
                )
        
        # Check for prompt optimization opportunities
        success_by_prompt = {}
        for o in outcomes:
            prompt_key = o.prompt_hash[:8]
            if prompt_key not in success_by_prompt:
                success_by_prompt[prompt_key] = []
            success_by_prompt[prompt_key].append(o.success)
        
        for prompt_hash, successes in success_by_prompt.items():
            rate = sum(successes) / len(successes)
            if rate < 0.8 and len(successes) >= 5:
                recommendations.append(
                    f"Prompt {prompt_hash}... has low success rate ({rate:.1%}). "
                    f"Consider prompt engineering review."
                )
        
        return recommendations
```

**3.6.3 Adaptive Prompt Optimization**

```python
class PromptOptimizer:
    """Optimizes prompts based on outcome data."""
    
    def __init__(self, outcome_tracker: OutcomeTracker):
        self._tracker = outcome_tracker
    
    def optimize_prompt(
        self,
        base_prompt: str,
        task_type: str,
        target_model: str,
    ) -> str:
        """Optimize prompt based on historical outcomes."""
        # Get successful outcomes for this task type
        successful = self._tracker.get_outcomes(
            task_type=task_type,
            model=target_model,
            success=True,
            min_quality=0.8,
        )
        
        if not successful:
            return base_prompt
        
        # Analyze prompt patterns in successful outcomes
        prompt_patterns = self._extract_patterns(successful)
        
        # Apply patterns to base prompt
        optimized = self._apply_patterns(base_prompt, prompt_patterns)
        
        return optimized
    
    def _extract_patterns(
        self,
        outcomes: list[TaskOutcome],
    ) -> dict[str, Any]:
        """Extract successful prompt patterns."""
        patterns = {
            "avg_length": 0,
            "common_phrases": [],
            "structure": "unknown",
        }
        
        # Analyze prompt characteristics
        for outcome in outcomes:
            prompt = self._get_prompt_by_hash(outcome.prompt_hash)
            if prompt:
                patterns["avg_length"] += len(prompt)
        
        patterns["avg_length"] /= len(outcomes)
        
        return patterns
```

---

## 4 LLM Provider Health Check Strategy

### 4.1 Health Metrics Collection

```python
# src/ai_company/llm/health.py
@dataclass
class ProviderHealth:
    """Comprehensive health metrics for an LLM provider."""
    provider_id: str
    timestamp: str
    
    # Availability
    is_available: bool
    response_time_ms: float
    uptime_24h: float  # Percentage
    
    # Performance
    success_rate: float  # Last 100 requests
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    
    # Cost efficiency
    avg_cost_per_task: float
    cost_per_quality_point: float
    
    # Error analysis
    error_rate: float
    common_errors: dict[str, int]  # error_type -> count
    
    # Circuit breaker state
    circuit_state: str
    consecutive_failures: int

class HealthMonitor:
    """Monitors provider health and makes routing recommendations."""
    
    def __init__(self):
        self._metrics: dict[str, list[ProviderHealth]] = {}
        self._circuit_breakers: dict[str, CircuitBreaker] = {}
    
    def record_request(
        self,
        provider_id: str,
        latency_ms: float,
        success: bool,
        error_type: str | None = None,
        cost_usd: float = 0.0,
    ) -> None:
        """Record a request for health tracking."""
        metrics = self._metrics.setdefault(provider_id, [])
        
        # Update running statistics
        recent = metrics[-100:] if metrics else []
        
        success_count = sum(1 for m in recent if m.is_available) + (1 if success else 0)
        total = len(recent) + 1
        
        health = ProviderHealth(
            provider_id=provider_id,
            timestamp=datetime.now().isoformat(),
            is_available=success,
            response_time_ms=latency_ms,
            uptime_24h=self._calc_uptime(provider_id),
            success_rate=success_count / total,
            avg_latency_ms=self._calc_avg_latency(recent + [latency_ms]),
            p95_latency_ms=self._calc_percentile(recent + [latency_ms], 0.95),
            p99_latency_ms=self._calc_percentile(recent + [latency_ms], 0.99),
            avg_cost_per_task=self._calc_avg_cost(provider_id),
            cost_per_quality_point=self._calc_cost_quality_ratio(provider_id),
            error_rate=1.0 - (success_count / total),
            common_errors=self._get_error_breakdown(provider_id),
            circuit_state=self._get_circuit_state(provider_id),
            consecutive_failures=self._get_consecutive_failures(provider_id),
        )
        
        metrics.append(health)
    
    def get_routing_recommendation(
        self,
        task_type: str,
        quality_requirements: str,
        cost_budget: float | None,
    ) -> list[str]:
        """Recommend provider order based on health metrics."""
        recommendations = []
        
        for provider_id, metrics in self._metrics.items():
            if not metrics:
                continue
            
            latest = metrics[-1]
            
            # Skip unhealthy providers
            if latest.circuit_state == "open":
                continue
            if latest.success_rate < 0.9:
                continue
            
            # Score provider
            score = self._score_provider(
                latest,
                task_type,
                quality_requirements,
                cost_budget,
            )
            
            recommendations.append((provider_id, score))
        
        # Sort by score (descending)
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return [provider_id for provider_id, _ in recommendations]
```

### 4.2 Health Check Endpoints

```python
# Provider-specific health checks
class HealthCheckers:
    """Provider-specific health check implementations."""
    
    @staticmethod
    async def check_ollama(base_url: str) -> bool:
        """Check if Ollama is running and responsive."""
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(f"{base_url}/api/tags", timeout=5.0)
                return resp.status_code == 200
            except Exception:
                return False
    
    @staticmethod
    async def check_openai_compatible(base_url: str, api_key: str) -> bool:
        """Check if OpenAI-compatible API is available."""
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    f"{base_url}/models",
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=10.0,
                )
                return resp.status_code == 200
            except Exception:
                return False
```

### 4.3 Health-Based Routing Integration

```python
def resolve_with_health_awareness(
    self,
    agent_name: str,
    priority: str,
    context: str | None,
) -> Route:
    """Route considering provider health metrics."""
    # Get base route
    base_route = self.resolve(agent_name, priority, context)
    
    # Get health recommendation for this tier
    tier = self.get_tier(base_route.tier)
    if tier:
        healthy_providers = self._health_monitor.get_routing_recommendation(
            task_type="general",
            quality_requirements="standard",
            cost_budget=None,
        )
        
        # Find first healthy provider in tier
        for provider in tier.providers:
            if provider.provider in healthy_providers:
                return Route(
                    provider=provider.provider,
                    model=provider.model,
                    tier=base_route.tier,
                    reason=f"Health-optimized: {provider.provider}",
                )
    
    return base_route
```

---

## 5 Cost Optimization Recommendations

### 5.1 Immediate Optimizations (Phase 3.1)

| Optimization | Expected Savings | Implementation Effort |
|--------------|------------------|----------------------|
| **Pre-request cost validation** | 10-15% | Low |
| **Context-aware model routing** | 15-25% | Medium |
| **Prompt compression** | 5-10% | Low |
| **Response caching** | 20-30% | Medium |

### 5.2 Cost Optimization Strategies

**5.2.1 Prompt Compression**

```python
class PromptCompressor:
    """Compresses prompts to reduce token count."""
    
    def __init__(self):
        self._stopwords = self._load_stopwords()
    
    def compress(
        self,
        system_prompt: str,
        user_prompt: str,
        target_reduction: float = 0.3,  # 30% reduction
    ) -> tuple[str, str]:
        """Compress prompts while preserving meaning."""
        original_tokens = self._count_tokens(system_prompt + user_prompt)
        target_tokens = int(original_tokens * (1 - target_reduction))
        
        # Apply compression techniques
        compressed_system = self._compress_system(system_prompt)
        compressed_user = self._compress_user(user_prompt)
        
        # Verify reduction
        new_tokens = self._count_tokens(compressed_system + compressed_user)
        if new_tokens > target_tokens:
            # Apply more aggressive compression
            compressed_system = self._aggressive_compress(compressed_system)
            compressed_user = self._aggressive_compress(compressed_user)
        
        return compressed_system, compressed_user
    
    def _compress_system(self, prompt: str) -> str:
        """Compress system prompt."""
        # Remove redundant instructions
        # Consolidate similar points
        # Use abbreviations for common phrases
        # Keep essential constraints
        
        return prompt  # Placeholder for actual implementation
    
    def _compress_user(self, prompt: str) -> str:
        """Compress user prompt."""
        # Remove filler words
        # Simplify verbose sentences
        # Extract key requirements
        
        return prompt  # Placeholder for actual implementation
```

**5.2.2 Response Caching**

```python
class ResponseCache:
    """Caches LLM responses for repeated queries."""
    
    def __init__(
        self,
        cache_dir: str = ".cache/llm",
        ttl_seconds: int = 3600,  # 1 hour
        max_size_mb: int = 100,
    ):
        self._cache_dir = Path(cache_dir)
        self._ttl = ttl_seconds
        self._max_size = max_size_mb * 1024 * 1024
    
    def get(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float,
    ) -> CachedResponse | None:
        """Get cached response if available."""
        cache_key = self._generate_key(
            system_prompt, user_prompt, model, temperature
        )
        
        cache_path = self._cache_dir / f"{cache_key}.json"
        if not cache_path.exists():
            return None
        
        # Check TTL
        age = time.time() - cache_path.stat().st_mtime
        if age > self._ttl:
            cache_path.unlink()
            return None
        
        # Load cached response
        with open(cache_path) as f:
            data = json.load(f)
        
        return CachedResponse(
            content=data["content"],
            tokens_saved=data["tokens"],
            cost_saved=data["cost"],
        )
    
    def set(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float,
        response: ChatResponse,
    ) -> None:
        """Cache a response."""
        cache_key = self._generate_key(
            system_prompt, user_prompt, model, temperature
        )
        
        cache_path = self._cache_dir / f"{cache_key}.json"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(cache_path, "w") as f:
            json.dump({
                "content": response.content,
                "tokens": response.usage.get("prompt_tokens", 0),
                "cost": self._estimate_cost(model, response.usage),
                "timestamp": time.time(),
            }, f)
        
        # Enforce cache size limit
        self._enforce_size_limit()
```

### 5.3 Cost Monitoring Dashboard

```python
class CostDashboard:
    """Provides cost visibility and optimization insights."""
    
    def __init__(self, cost_tracker: CostTracker):
        self._tracker = cost_tracker
    
    def generate_daily_report(self) -> CostReport:
        """Generate daily cost report with insights."""
        summary = self._tracker.get_daily_summary()
        
        return CostReport(
            date=summary["date"],
            total_cost=summary["total_cost_usd"],
            total_tokens=summary["total_prompt_tokens"] + summary["total_completion_tokens"],
            cost_by_model=summary["by_model"],
            insights=self._generate_insights(summary),
            recommendations=self._generate_recommendations(summary),
            projections=self._project_monthly_cost(summary),
        )
    
    def _generate_insights(self, summary: dict) -> list[str]:
        """Generate cost insights from summary."""
        insights = []
        
        # Check for expensive models
        for model, stats in summary["by_model"].items():
            if stats["cost_usd"] > summary["total_cost_usd"] * 0.5:
                insights.append(
                    f"{model} accounts for {stats['cost_usd']/summary['total_cost_usd']:.1%} "
                    f"of total cost (${stats['cost_usd']:.4f})"
                )
        
        # Check for high token usage
        avg_tokens = (
            summary["total_prompt_tokens"] + summary["total_completion_tokens"]
        ) / max(summary["call_count"], 1)
        
        if avg_tokens > 2000:
            insights.append(
                f"Average tokens per request ({avg_tokens:.0f}) is high. "
                f"Consider prompt compression."
            )
        
        return insights
    
    def _generate_recommendations(self, summary: dict) -> list[str]:
        """Generate cost optimization recommendations."""
        recommendations = []
        
        # Check for free tier opportunities
        for model, stats in summary["by_model"].items():
            if "llama" in model and stats["cost_usd"] == 0:
                recommendations.append(
                    f"Using free Ollama model {model} for {stats['calls']} tasks. "
                    f"Consider if quality is sufficient for all use cases."
                )
        
        # Check for cache opportunities
        if summary["call_count"] > 100:
            recommendations.append(
                "High request volume detected. Response caching could reduce costs by 20-30%."
            )
        
        return recommendations
```

---

## 6 Quality Benchmarks and Evaluation Framework

### 6.1 Quality Metrics

| Metric | Definition | Target | Measurement |
|--------|------------|--------|-------------|
| **Task Success Rate** | % of tasks completed successfully | > 85% | Outcome tracking |
| **Response Quality** | Human-rated quality score | > 4.0/5.0 | Periodic evaluation |
| **Cost Efficiency** | Cost per successful task | < $0.01 | Cost tracker |
| **Latency** | Average response time | < 5s | Health monitor |
| **Consistency** | Variance in quality scores | < 0.1 std dev | Outcome tracking |

### 6.2 Evaluation Framework

```python
# src/ai_company/evaluation/evaluator.py
class AgentEvaluator:
    """Evaluates agent performance against quality benchmarks."""
    
    def __init__(
        self,
        outcome_tracker: OutcomeTracker,
        cost_tracker: CostTracker,
    ):
        self._outcomes = outcome_tracker
        self._costs = cost_tracker
    
    def evaluate_agent(
        self,
        agent_name: str,
        test_cases: list[TestCase],
    ) -> EvaluationResult:
        """Run evaluation suite for an agent."""
        results = []
        
        for test_case in test_cases:
            # Execute test
            outcome = self._run_test(agent_name, test_case)
            results.append(outcome)
        
        # Calculate metrics
        success_rate = sum(1 for r in results if r.success) / len(results)
        avg_quality = sum(r.quality_score for r in results) / len(results)
        avg_cost = sum(r.cost_usd for r in results) / len(results)
        
        return EvaluationResult(
            agent=agent_name,
            test_count=len(test_cases),
            success_rate=success_rate,
            avg_quality=avg_quality,
            avg_cost=avg_cost,
            passed=success_rate >= 0.85 and avg_quality >= 0.8,
            details=results,
        )
    
    def benchmark_models(
        self,
        test_cases: list[TestCase],
        models: list[str],
    ) -> dict[str, BenchmarkResult]:
        """Benchmark different models on test cases."""
        results = {}
        
        for model in models:
            model_results = []
            for test_case in test_cases:
                outcome = self._run_test_with_model(test_case, model)
                model_results.append(outcome)
            
            results[model] = BenchmarkResult(
                model=model,
                success_rate=sum(1 for r in model_results if r.success) / len(model_results),
                avg_quality=sum(r.quality_score for r in model_results) / len(model_results),
                avg_cost=sum(r.cost_usd for r in model_results) / len(model_results),
                avg_latency=sum(r.latency_ms for r in model_results) / len(model_results),
            )
        
        return results
```

### 6.3 Test Case Structure

```python
@dataclass
class TestCase:
    """A test case for agent evaluation."""
    id: str
    name: str
    description: str
    
    # Input
    task_instruction: str
    expected_output_type: str  # "json", "text", "code", etc.
    context: str | None = None
    
    # Evaluation criteria
    required_keys: list[str] = field(default_factory=list)
    forbidden_patterns: list[str] = field(default_factory=list)
    quality_threshold: float = 0.7
    
    # Metadata
    category: str = "general"
    complexity: str = "medium"
    timeout_seconds: int = 30


# Example test cases
TEST_CASES = [
    TestCase(
        id="json_output_001",
        name="JSON Output Validation",
        description="Verify agent returns valid JSON with required keys",
        task_instruction="Analyze this data and return a JSON summary with keys: summary, insights, recommendations",
        expected_output_type="json",
        required_keys=["summary", "insights", "recommendations"],
        quality_threshold=0.8,
    ),
    TestCase(
        id="code_review_001",
        name="Code Review Quality",
        description="Evaluate code review quality and actionability",
        task_instruction="Review this Python function for bugs and improvements: def add(a, b): return a - b",
        expected_output_type="text",
        quality_threshold=0.85,
    ),
]
```

### 6.4 Continuous Evaluation

```python
class ContinuousEvaluator:
    """Runs continuous evaluation in the background."""
    
    def __init__(
        self,
        evaluator: AgentEvaluator,
        interval_hours: int = 24,
    ):
        self._evaluator = evaluator
        self._interval = interval_hours
        self._running = False
    
    async def start(self):
        """Start continuous evaluation loop."""
        self._running = True
        
        while self._running:
            # Run evaluation
            await self._run_evaluation_cycle()
            
            # Wait for next cycle
            await asyncio.sleep(self._interval * 3600)
    
    async def _run_evaluation_cycle(self):
        """Run a complete evaluation cycle."""
        # Select test cases
        test_cases = self._select_test_cases()
        
        # Evaluate each agent
        for agent in self._get_active_agents():
            result = self._evaluator.evaluate_agent(agent, test_cases)
            
            # Record results
            self._record_result(result)
            
            # Alert if below threshold
            if not result.passed:
                await self._send_alert(agent, result)
```

---

## 7 Implementation Roadmap

### 7.1 Phase 3.1: Foundation (Weeks 1-4)

| Week | Deliverable | Owner | Dependencies |
|------|-------------|-------|--------------|
| 1-2 | Token counter implementation | ML Engineer | tiktoken dependency |
| 2-3 | Cost calculator with pre-validation | ML Engineer | Token counter |
| 3-4 | Enhanced ModelRouter with cost awareness | ML Engineer | Cost calculator |

### 7.2 Phase 3.2: Intelligence (Weeks 5-8)

| Week | Deliverable | Owner | Dependencies |
|------|-------------|-------|--------------|
| 5-6 | System prompt architect | Prompt Engineer | Prompt templates |
| 6-7 | Outcome tracking system | ML Engineer | Results schema |
| 7-8 | Performance-based routing | ML Engineer | Outcome tracker |

### 7.3 Phase 3.3: Advanced (Weeks 9-12)

| Week | Deliverable | Owner | Dependencies |
|------|-------------|-------|--------------|
| 9-10 | RAG pipeline integration | ML Engineer | Vector store |
| 10-11 | Agent self-improvement loop | ML Engineer | Outcome tracker |
| 11-12 | Health monitoring dashboard | ML Engineer | Health metrics |

### 7.4 Phase 3.4: Optimization (Weeks 13-16)

| Week | Deliverable | Owner | Dependencies |
|------|-------------|-------|--------------|
| 13-14 | Prompt compression | Prompt Engineer | Token counter |
| 14-15 | Response caching | ML Engineer | Cost tracker |
| 15-16 | Continuous evaluation | ML Engineer | Test framework |

---

## 8 Success Metrics

| Metric | Current | Phase 3 Target | Measurement |
|--------|---------|----------------|-------------|
| **Task Success Rate** | ~70% | > 85% | Outcome tracking |
| **Avg Cost per Task** | ~$0.02 | < $0.01 | Cost tracker |
| **Token Efficiency** | Baseline | +30% | Token counter |
| **Budget Compliance** | Manual | 100% automated | Cost calculator |
| **Model Selection Quality** | Static | Context-aware | Routing metrics |
| **Agent Learning Rate** | None | Measurable improvement | Outcome trends |

---

## 9 Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Token counting inaccuracy** | Wrong cost estimates | Fallback to provider-reported counts |
| **Cache staleness** | Outdated responses | TTL-based invalidation |
| **Quality regression** | Lower task success | Automated evaluation gates |
| **Cost overrun** | Budget exceeded | Pre-request validation, hard limits |
| **Provider dependency** | Service disruption | Circuit breaker, multi-provider fallback |

---

## 10 Conclusion

Phase 3 transforms AI Company Builder into an intelligent, self-optimizing platform. By implementing token-level cost control, context-aware routing, and agent learning loops, we will achieve:

1. **25-40% cost reduction** through intelligent model selection and prompt optimization
2. **25% improvement in task success rates** through better prompts and quality feedback
3. **Full cost visibility** with pre-request validation and real-time tracking
4. **Continuous improvement** through outcome-based learning

The foundation built in Phases 1-2 provides a solid platform for these enhancements. With careful implementation and continuous monitoring, Phase 3 will deliver significant value while maintaining the reliability and flexibility that agents require.

---

**Document Status:** Draft for Review
**Next Review:** July 26, 2026
**Approved By:** [Pending]
