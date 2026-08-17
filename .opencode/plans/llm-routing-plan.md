# LLM Model Routing & Chain Rotation Strategy — Implementation Plan

## Phase 1: Dynamic Free-Model Discovery & Core Routing (Week 1-2)

### Objective
Build the foundation: dynamic model catalog, task-type routing, free-tier support, token-limit error detection.

### Key Decisions (User-Approved)
- Default tier for new agents: **free** (zero-cost, Opencode free + Ollama fallback)
- Token budget scope: **per-task** (unchanged from current)
- Rotation strategy: **sequential tiers** (fast→standard→premium)
- Gemini: Fast tier, preferred for token-limit rotation, "free-ish" cost
- Dynamic free-model discovery: **YES** — fetch from Opencode Zen API, sort by context window

### Tasks

#### 1.1: Dynamic Free-Model Discovery
**Goal**: Replace static free-tier provider list with dynamic catalog fetch from Opencode Zen API.

**Implementation**:
```python
# model_router.py additions

import aiohttp
from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class FreeModel:
    """Represents a free Opencode model with metadata."""
    id: str
    name: str
    context: int  # context window in tokens
    provider: str = "opencode"
    priority: int = 0  # higher = preferred for rotation

# New method on ModelRouter
async def _fetch_free_model_catalog(self) -> List[FreeModel]:
    """Fetch free models from OpenCode Zen API, sorted by context window descending.
    
    Returns list of FreeModel sorted by context (largest first), ready for rotation.
    Caches result for 1 hour (models rarely change daily).
    Falls back to static list if API unavailable.
    """
    cache_key = "free_model_catalog"
    cached = self._get_cached(cache_key)
    if cached:
        return cached
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://opencode.ai/zen/v1/models",
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    models = []
                    for m in data.get("data", []):
                        if m.get("free", False) or m.get("price", {}).get("usd", 0) == 0:
                            ctx = m.get("max_tokens", 0) or m.get("context_length", 0) or 0
                            # Extract provider/model from id
                            mid = m.get("id", "")
                            prov, model = (mid.split("/", 1) if "/" in mid else ("opencode", mid))
                            priority = 1000 - ctx  # larger context = higher priority
                            models.append(FreeModel(
                                id=mid,
                                name=m.get("name", model),
                                context=ctx,
                                provider=prov,
                                model=model,
                                priority=priority,
                            ))
                    # Sort by context descending, then priority
                    models.sort(key=lambda m: (-m.context, -m.priority))
                    
                    # Cache for 1 hour
                    self._set_cache(cache_key, models, ttl=3600)
                    return models
    except Exception:
        pass  # Fall through to static fallback
    
    # Static fallback list (current free models)
    return [
        FreeModel(id="opencode/big-pickle", name="Big Pickle", context=200000, priority=800),
        FreeModel(id="opencode/gpt-5-nano", name="GPT-5 Nano", context=128000, priority=920),  # permanently free
        FreeModel(id="opencode/kimi-k2.5-free", name="Kimi K2.5 Free", context=262144, priority=738),
        FreeModel(id="opencode/qwen3.6-plus-free", name="Qwen 3.6 Plus Free", context=262144, priority=738),
        FreeModel(id="opencode/minimax-m2.5-free", name="MiniMax M2.5 Free", context=204800, priority=795),
        FreeModel(id="opencode/glm-4.7-free", name="GLM-4.7 Free", context=200000, priority=800),
    ]

# Cache helper methods added to ModelRouter
def _get_cached(self, key: str) -> Optional[list]:
    """Check in-memory cache for key. Returns None if not found or expired."""
    if key in self._model_cache and self._cache_time.get(key):
        if datetime.now() - self._cache_time[key] < timedelta(seconds=3600):
            return self._model_cache[key]
    return None

def _set_cache(self, key: str, value: list, ttl: int = 3600) -> None:
    """Set in-memory cache with timestamp."""
    self._model_cache[key] = value
    self._cache_time[key] = datetime.now()
```

**Files changed**: `src/ai_company/model_router.py`

#### 1.2: Task-Type Routing Enhancement
**Goal**: Map 12 task types to optimal free models from the dynamic catalog.

**Implementation**:
- Add `task_type_to_tier` mapping using dynamic model priorities
- Low complexity → highest priority free model (largest context first)
- Medium complexity → mid-tier free models
- High complexity → standard/premium tiers as before

**Updated `models.yaml` additions**:
```yaml
task_type_routing:
  read_only: free
  single_file_edit: free
  simple_command: free
  boilerplate: free
  code_review: standard
  debugging: standard
  refactor: standard
  integration: standard
  architecture: premium
  planning: premium
  security: premium
  performance: premium
```

**Files changed**: `src/ai_company/model_router.py`, `company/models.yaml`

#### 1.3: `free` Tier with Dynamic Providers
**Goal**: Define `free` tier that uses dynamic model catalog instead of static providers.

**Implementation**:
```yaml
# In models.yaml, replace static free-tier providers with:
tiers:
  free:
    description: "Zero-cost tier using dynamic Opencode free models"
    # No static providers list - ModelRouter will pull from dynamic catalog
    # ModelRouter.resolve() will:
    # 1. Fetch dynamic catalog if not cached
    # 2. Select first available free model
    # 3. Fall back to Ollama if no free models available
```

**Alternative**: Keep `free` tier but have ModelRouter resolve providers dynamically during `resolve()` instead of reading from YAML static list.

**Files changed**: `src/ai_company/model_router.py`, `company/models.yaml`

#### 1.4: Token Limit Error Detection & Rotation
**Goal**: Detect when LLM response indicates context window exceeded, then rotate through free models.

**Implementation** in `model_router.py`:
```python
# Error patterns that indicate token limit exceeded
TOKEN_LIMIT_PATTERNS = [
    "context length", "max_tokens", "token limit", "too many tokens",
    "exceeds maximum", "context window", "maximum context",
    "input too long", "prompt too long", "message too long",
]

# In resolve_with_complexity or a new method
def rotate_on_token_limit(self, failed_model: str, task_prompt: str) -> Optional[Route]:
    """Rotate to next free model with larger context window.
    
    1. Get current model's context
    2. Find next free model with larger context from dynamic catalog
    3. If found, return route with that model
    4. If none larger, try next tier up (sequential)
    5. If no tier up, return route with prompt truncation suggestion
    """
    # Get current model's context from catalog
    current_model = self._find_model(failed_model)
    if not current_model:
        return None
    
    # Find next model with larger context
    for model in self._free_catalog:
        if model.context > current_model.context and model.id != current_model.id:
            # Rotate to this model
            tier = self._get_tier_for_model(model)
            return Route(
                provider=model.provider,
                model=model.model,
                tier=tier,
                reason=f"token-limit rotation: {current_model.context}→{model.context} context window"
            )
    
    # No larger free model available → go up a tier
    return self._rotate_to_next_tier("standard")
```

**Files changed**: `src/ai_company/model_router.py`

#### 1.5: Integration with LLMClient
**Goal**: Wire token-limit rotation into `LLMClient.execute_task()` so it automatically rotates models when context is exceeded.

**Implementation** in `client.py`:
- After a provider returns an error, check if it's a token-limit error
- If yes, call `router.rotate_on_token_limit()` to get next model
- Retry with new model (up to 2 additional attempts)
- Log the rotation decision

**Files changed**: `src/ai_company/llm/client.py`

### Phase 1 Deliverables

| File | Change |
|------|--------|
| `src/ai_company/model_router.py` | Dynamic catalog fetch, task-type routing, token-limit rotation, cache helpers |
| `company/models.yaml` | task_type_routing mapping, free tier description updated |
| `src/ai_company/llm/client.py` | Token-limit error detection + rotation integration |
| `tests/unit/test_model_router.py` | New unit tests for dynamic catalog, task routing, rotation |
| `tests/integration/test_token_rotation.py` | Integration tests with mocked API responses |

### Verification Gates (Phase 1)

- [ ] `ruff check src/ && mypy src/` passes
- [ ] `pytest tests/unit/test_model_router.py -v` all pass
- [ ] Dynamic catalog fetches models from Opencode Zen API (or falls back gracefully)
- [ ] Task-type routing maps all 12 task types correctly
- [ ] Token-limit rotation falls back to sequential tier when no larger free model
- [ ] `LOCAL_FIRST=false` default works (cloud-first)

### Open Questions for Phase 1

1. **Cache TTL**: 1 hour seems reasonable, but should we check more frequently?
2. **Error classification**: Should `TOKEN_LIMIT` be a new `ProviderErrorCategory`? Or just pattern-matching on error messages?
3. **What if API returns non-free models?** Filter strictly by `free: true` or by `price: $0`?
4. **Rate limiting**: Opencode Zen API - is there a rate limit we need to respect?

---

## Phase 2: Budget-Aware Degradation (Week 2-3)

### Objective
Implement gradual tier reduction based on daily budget pressure (80%/90%/95%).

### Key Tasks
- [ ] Add `daily_budget_pressure()` to `CostTracker`
- [ ] Create `BudgetAwareRouter` wrapper
- [ ] Wire into `LLMClient` with priority protection
- [ ] Update `models.yaml` with degradation thresholds

### Files
- `src/ai_company/llm/cost_tracker.py` — budget pressure calculation
- `src/ai_company/model_router.py` — BudgetAwareRouter
- `src/ai_company/llm/client.py` — integration
- `company/models.yaml` — degradation thresholds

---

## Phase 3: Streaming Token Budget Enforcement (Week 3-4)

### Objective
Enforce token budgets during streaming responses with mid-stream checkpoints.

### Key Tasks
- [ ] Add pre-flight prompt token estimation
- [ ] Add mid-stream completion token estimation every N chunks
- [ ] Auto-truncate + return partial result when budget exceeded
- [ ] Log budget events to dashboard

### Files
- `src/ai_company/llm/client.py` — streaming budget enforcement
- `src/ai_company/llm/token_counter.py` — improved estimates
- Dashboard metrics updates

---

## Phase 4: Local-First & Ollama Integration (Week 4)

### Objective
Opt-in local model preference when cloud is unavailable or budget exhausted.

### Key Tasks
- [ ] Add `local_first` env var + config flag
- [ ] Ollama availability check at startup
- [ ] Model size selection (8b vs 70b based on VRAM)
- [ ] Fallback chain: cloud free → local Ollama → fail gracefully

### Files
- `src/ai_company/model_router.py` — local_first logic
- `src/ai_company/llm/providers/ollama.py` — model size detection
- `.env.example` — LOCAL_FIRST flag
- Dashboard — local model indicator

---

## Phase 5: Testing, Docs & ADR (Week 4-5)

### Objective
Complete verification, update documentation, create architectural decision record.

### Key Tasks
- [ ] Unit tests for all routing scenarios
- [ ] Integration tests with mocked Opencode API
- [ ] Update `MODEL-ROUTING-POLICY.md`
- [ ] Create `ADR-005: Token-Aware Model Routing`
- [ ] Pre-commit/hooks verification
- [ ] Dashboard routing display updates

### Files
- `tests/unit/` — comprehensive test suite
- `tests/integration/` — end-to-end flows
- `docs/MODEL-ROUTING-POLICY.md` — updated policy
- `docs/adr/005-token-aware-rotation.md` — new ADR
- `docs/LLM-ROUTING-STRATEGY.md` — this plan

---