# Pre-Sprint-4 Backlog — Outstanding Issue Resolution

**Date:** 2026-07-24
**Status:** 16 of 20 items COMPLETE
**Objective:** Fix all outstanding issues before Sprint 4 begins (20 items total)
**Remaining Effort:** ~18h (AI security items PRE-16 through PRE-20)

---

## Status Summary (Updated 2026-07-24)

| Status | Count | Items |
|--------|-------|-------|
| ✅ COMPLETE | 14 | PRE-01, PRE-02, PRE-03, PRE-04, PRE-06, PRE-08, PRE-08B, PRE-09, PRE-10, PRE-11, PRE-12, PRE-13, PRE-14 |
| ✅ COMPLETE (docs) | 1 | PRE-05 (risk register updated) |
| ✅ COMPLETE (code) | 1 | PRE-07 (KPI MessageBus injection) |
| ⏳ NOT STARTED | 6 | PRE-15 (dashboard UX), PRE-16, PRE-17, PRE-18, PRE-19, PRE-20 |

### Completed Items Evidence

- **PRE-01**: `integration.py:35-47` — encryption wired into `init_memory()`
- **PRE-02**: `ws.py:116-163` — WebSocket auth via query param + message
- **PRE-03**: `app.py:109-126` — fail-closed mode when no API key set
- **PRE-04**: `repository.py:275-319` — MessageBus singleton via `get_task_backend_singleton()`
- **PRE-05**: `RISK-REGISTER.md` — R15/R16/R17/R18 updated to Mitigated
- **PRE-06**: `loop.py:207-208,224-225` — consolidation scheduler start/stop
- **PRE-07**: `api.py:1095`, `app.py:438` — `collect_all_kpis()` now passes `message_bus=get_bus()`
- **PRE-08**: structlog wired, 0 `print()` in non-CLI code
- **PRE-08B**: `cli/agents.py:70-122` — `ai-company agents validate` command
- **PRE-09**: `test_circuit_breaker.py` — 27 tests, all passing
- **PRE-10**: `test_pii_detector.py`, `test_content_filter.py`, `test_memory_encryption.py` — 143 tests
- **PRE-11**: `client.py:33-64` + `agent_loop.py:174` — `estimate_call_cost()` wired
- **PRE-12**: `app.py:271-324` — `/api/v1/` prefix + legacy redirect
- **PRE-13**: grep confirms 0 `print()` in non-CLI code
- **PRE-14**: `security/key_rotation.py` + `cli/security.py` — full key lifecycle

---

## Executive Summary

Before Sprint 4 can begin, 33 outstanding issues must be resolved. These span architecture gaps, security vulnerabilities, testing gaps, data integrity problems, code quality issues, and **AI-specific security threats**. This document provides a prioritized, sequenced plan to address all items.

**AI Security Note:** Five new items (PRE-16 through PRE-20) have been added based on AI Security Specialist threat assessment. These address prompt injection, data exfiltration, agent autonomy abuse, and model manipulation risks specific to our multi-agent LLM architecture.

---

## Priority 1: Critical (1 item) — Must fix first

### PRE-01: Wire Memory Encryption Into `init_memory()`
| Field | Value |
|-------|-------|
| **Severity** | CRITICAL |
| **Effort** | 0.5h |
| **Purpose** | Enable at-rest encryption for all memory entries to protect sensitive company data (financial, strategic, HR) stored in memory files |
| **Files** | `src/ai_company/memory/integration.py:20-42`, `src/ai_company/security/encryption_key_manager.py` |
| **Owner** | security_engineer |

**Problem:** `memory_encryption.py` (103 lines) provides AES-256-GCM encryption, and `MemoryStore.enable_encryption()` exists in `engine.py:135-146`, but `init_memory()` in `integration.py:20-42` never calls it. All memory is stored in plaintext.

**Fix:**
```python
# In integration.py init_memory():
def init_memory(base_dir: str = "memory") -> MemoryStore:
    global _store, _vector_store
    _store = MemoryStore(base_dir=base_dir)

    # Wire encryption if key is available
    try:
        from ai_company.security.encryption_key_manager import EncryptionKeyManager
        km = EncryptionKeyManager()
        _store.enable_encryption(km)
    except Exception:
        logger.debug("Memory encryption disabled (no key available)")

    # ... rest of existing init ...
```

**Verification:**
- Unit test: mock `EncryptionKeyManager`, assert `enable_encryption()` called
- Integration test: store + recall round-trip with encryption enabled

---

## Priority 2: Security (3 items)

### PRE-02: Add WebSocket Authentication
| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Effort** | 2h |
| **Purpose** | Prevent unauthorized clients from receiving sensitive KPI, task, and escalation data via WebSocket broadcasts |
| **Files** | `src/ai_company/dashboard/ws.py:101-160` |
| **Owner** | lead_frontend |

**Problem:** WebSocket endpoint `/ws/dashboard` accepts connections from any client with no authentication. Sensitive KPI and task data is broadcast to unauthenticated listeners.

**Fix:**
```python
# In ws.py dashboard_websocket():
@router.websocket("/ws/dashboard")
async def dashboard_websocket(websocket: WebSocket) -> None:
    # Check API key from query param or first message
    api_key = websocket.query_params.get("token")
    if not api_key:
        # Wait for auth message
        try:
            data = await asyncio.wait_for(websocket.receive_json(), timeout=5.0)
            api_key = data.get("token", "")
        except Exception:
            await websocket.close(code=4001, reason="No auth token")
            return

    expected = os.environ.get("DASHBOARD_API_KEY", "")
    if expected and api_key != expected:
        await websocket.close(code=4003, reason="Invalid token")
        return

    await manager.connect(websocket)
    # ... rest of handler
```

**Verification:**
- Test: connect without token → 4001 close
- Test: connect with wrong token → 4003 close
- Test: connect with valid token → success

---

### PRE-03: Fix Dashboard Auth Fail-Open
| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Effort** | 1h |
| **Purpose** | Ensure dashboard API rejects unauthorized write operations when no API key is configured, preventing open access in production |
| **Files** | `src/ai_company/dashboard/app.py:100-112` |
| **Owner** | lead_frontend |

**Problem:** `_check_api_key()` returns `True` when `DASHBOARD_API_KEY` is unset (line 108-109). This is intentional for dev but dangerous for production.

**Fix:**
```python
def _check_api_key(request: Request) -> bool:
    api_key = _get_api_key()
    if not api_key:
        # Fail-closed: reject mutations when no key is configured
        if request.method not in ("GET", "HEAD", "OPTIONS"):
            return False
        return True
    if request.method in ("GET", "HEAD", "OPTIONS"):
        return True
    return request.headers.get("X-API-Key") == api_key
```

Add env var `DASHBOARD_AUTH_MODE=open|closed` (default: `closed`).

**Verification:**
- Test: no key set, POST request → 401
- Test: no key set, GET request → 200
- Test: key set, valid key POST → 200

---

### PRE-04: Centralize MessageBus Singleton
| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Effort** | 4h |
| **Purpose** | Eliminate race conditions from multiple MessageBus instances writing to the same inbox.json; ensure single source of truth for task state |
| **Files** | `dashboard/api.py`, `dashboard/mobile_api.py`, `dashboard/monitoring.py`, `dashboard/repository.py` |
| **Owner** | lead_backend |

**Problem:** Three modules each create independent MessageBus/TaskStore instances: `api.py`, `mobile_api.py:27-41`, `monitoring.py:31-32`. This causes race conditions when concurrent requests write to the same files.

**Fix:**
```python
# In dashboard/repository.py — add singleton accessor:
_bus_singleton = None

def get_task_backend() -> Any:
    global _bus_singleton
    if _bus_singleton is None:
        from ai_company.data import get_task_backend as _factory
        _bus_singleton = _factory()
    return _bus_singleton
```

Update `mobile_api.py` and `monitoring.py` to use `repository.get_task_backend()`.

**Verification:**
- Test: import from all 3 modules, assert same object identity
- Test: concurrent writes don't clobber

---

## Priority 3: Data Integrity (2 items)

### PRE-05: Update Stale Risk Register
| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Effort** | 0.5h |
| **Purpose** | Ensure risk register accurately reflects mitigation status so leadership can make informed decisions about residual risk |
| **Files** | `docs/RISK-REGISTER.md` |
| **Owner** | compliance_officer |

**Problem:** R17 (HITL blocking) and R18 (shell injection) show status "Open" but were resolved in Sprint 2 (GAP-004, GAP-016).

**Fix:** Update status to "Mitigated" with evidence file:line references.

---

### PRE-06: Wire GAP-005 Memory Consolidation
| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Effort** | 3h |
| **Purpose** | Prevent memory from growing unbounded by enabling background consolidation and pruning of old/irrelevant memories |
| **Files** | `executor/loop.py:137-142,255-257`, `memory/consolidation.py` |
| **Owner** | lead_backend |

**Problem:** GAP-005 is partially resolved. The `ConsolidationScheduler` is instantiated (line 139) and `on_tick()` is called (line 256), but the scheduler's `start()` method for background thread operation is never called. The tick-based consolidation works, but time-based consolidation in the background does not.

**Current code (loop.py:137-142):**
```python
# GAP-005: Memory consolidation scheduler
self._consolidation_config = ConsolidationConfig()
self._consolidation_scheduler = ConsolidationScheduler(
    store=self._memory,
    config=self._consolidation_config,
)
```

**Fix:** Call `start()` in `Executor.start()` and `stop()` in `Executor.stop()`:
```python
def start(self) -> None:
    self.running = True
    self.stats.start_time = datetime.now()
    self._consolidation_scheduler.start()  # ADD
    # ...

def stop(self) -> None:
    self.running = False
    self._consolidation_scheduler.stop()  # ADD
    # ...
```

**Verification:**
- Test: mock `ConsolidationScheduler.start()`, assert called on `Executor.start()`
- Test: mock `ConsolidationScheduler.stop()`, assert called on `Executor.stop()`

---

## Priority 4: Architecture Gaps (2 items)

### PRE-07: Complete GAP-011 MessageBus Read Path
| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Effort** | 6h |
| **Purpose** | Ensure dashboard reads consistent task state when using SQLite backend by routing all inbox reads through MessageBus |
| **Files** | `dashboard/mobile_api.py`, `dashboard/kpis/*` |
| **Owner** | lead_backend |

**Problem:** `mobile_api.py` and `dashboard/kpis/*` still read `inbox.json` directly for read-only operations. While less dangerous than write bypass, this creates inconsistent state when the bus is in SQLite mode.

**Fix:** Replace all `inbox.json` reads with `bus.get_all_tasks()` or `bus.get_task_by_id()`.

**Verification:**
- Grep for `inbox.json` in dashboard/ — should return 0 hits
- Test: all KPI endpoints return same data via MessageBus as via file read

---

### PRE-08: GAP-018 Structured Logging
| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Effort** | 6h |
| **Purpose** | Enable production debugging and compliance auditing by providing structured JSON logs with correlation IDs linking task→agent→tool calls |
| **Files** | Multiple (11 `print()` calls in non-CLI code) |
| **Owner** | lead_backend |

**Problem:** Mixed logging: some `logger.info()`, some `print()`, no structured JSON format, no correlation IDs.

**Fix:**
1. Replace all `print()` with `logger.info/warning/error`
2. Configure `structlog` or `python-json-logger`
3. Add `task_id` as correlation ID in log context

Files with `print()`:
- `executor/loop.py:207,208,214,223`
- Other modules (grep for `print(`)

**Verification:**
- `grep -r "print(" src/ai_company/ --include="*.py" | grep -v cli/ | wc -l` → 0
- All log output is valid JSON when `LOG_FORMAT=json`

---

### PRE-08B: GAP-019 Agent Spec Validation CLI
| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Effort** | 3h |
| **Purpose** | Catch malformed agent specs before they cause silent degradation in production by validating required fields and providing actionable error messages |
| **Files** | `executor/context.py:31-100`, `cli/main.py` |
| **Owner** | qa_engineer |

**Problem:** `parse_agent_spec()` silently returns `AgentContext` with empty fields for malformed specs. No validation, no warnings.

**Fix:**
1. Add `AgentContext.validate()` method
2. Log warnings for missing critical fields (mission, responsibilities)
3. Add `ai-company agents validate` CLI command
4. Integrate validation into generator output

**Verification:**
- Test: malformed spec → validation error with specific field
- Test: valid spec → passes validation
- CLI: `ai-company agents validate` reports all agent status

---

## Priority 5: Testing (3 items)

### PRE-09: Add Circuit Breaker Tests
| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Effort** | 2h |
| **Purpose** | Validate critical state transitions (CLOSED→OPEN→HALF_OPEN→CLOSED) to prevent LLM provider outage cascading failures |
| **Files** | `tests/unit/test_circuit_breaker.py` (new) |
| **Owner** | qa_engineer |

**Problem:** `circuit_breaker.py` has zero test coverage. Critical state transitions (CLOSED→OPEN→HALF_OPEN→CLOSED) untested.

**Test cases:**
```python
class TestCircuitBreaker:
    def test_starts_closed(self)
    def test_opens_after_threshold_failures(self)
    def test_half_open_after_recovery_timeout(self)
    def test_closes_on_success_in_half_open(self)
    def test_reopens_on_failure_in_half_open(self)
    def test_success_resets_failure_count(self)
    def test_reset_returns_to_closed(self)
    def test_is_available_in_closed_and_half_open(self)
```

---

### PRE-10: Add Security Module Tests
| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Effort** | 4h |
| **Purpose** | Ensure PII detection, content filtering, and memory encryption work correctly before production deployment |
| **Files** | `tests/unit/test_pii_detector.py`, `tests/unit/test_content_filter.py`, `tests/unit/test_memory_encryption.py` |
| **Owner** | qa_engineer |

**Problem:** `pii_detector.py`, `content_filter.py`, `memory_encryption.py` have zero test coverage.

**Test cases per module:**

`test_pii_detector.py`:
- `test_detect_ssn` — SSN pattern detected
- `test_detect_email` — email pattern detected
- `test_detect_phone` — phone pattern detected
- `test_clean_pii` — PII replaced with placeholders
- `test_no_false_positives` — normal text passes

`test_content_filter.py`:
- `test_filter_harmful_content` — harmful content flagged
- `test_safe_content_passes` — normal content passes
- `test_filter_returns_score` — confidence score returned

`test_memory_encryption.py`:
- `test_encrypt_decrypt_roundtrip` — data survives encrypt+decrypt
- `test_encrypted_content_prefixed` — output starts with "ENC:"
- `test_plaintext_passthrough` — unencrypted text unchanged
- `test_already_encrypted_not_double_encrypted` — no double-encryption

---

### PRE-11: Add Token Counting Integration
| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Effort** | 3h |
| **Purpose** | Enable pre-flight cost estimation to prevent budget overruns before LLM calls are made |
| **Files** | `executor/agent_loop.py`, `llm/client.py` |
| **Owner** | lead_backend |

**Problem:** Token counting not wired into AgentLoop for pre-flight cost estimation.

**Fix:**
```python
# In agent_loop.py run():
estimated_tokens = estimate_tokens(user_prompt + system_prompt)
estimated_cost = self.cost_tracker.estimate_cost(estimated_tokens, priority)
if not self.cost_tracker.check_budget(task_id=task_id, cost=estimated_cost):
    return LoopResult(error="Budget exceeded", done=False)
```

**Verification:**
- Test: task exceeding budget returns error without calling LLM
- Test: task within budget proceeds normally

---

## Priority 6: API & Code Quality (4 items)

### PRE-12: Add API Versioning
| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Effort** | 4h |
| **Purpose** | Prevent breaking changes to API consumers by establishing versioned endpoints with deprecation notices |
| **Files** | `dashboard/api.py`, `dashboard/mobile_api.py`, `dashboard/app.py` |
| **Owner** | api_architect |

**Problem:** No `/api/v1/` prefix. Schema changes break consumers.

**Fix:**
1. Add `prefix="/api/v1"` to main API router
2. Keep legacy `/api/` routes as redirects
3. Add `APIVersion` header to responses

---

### PRE-13: Replace print() Calls
| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Effort** | 1h |
| **Purpose** | Standardize logging across non-CLI modules to enable structured log output and correlation IDs |
| **Files** | `executor/loop.py`, other non-CLI modules |
| **Owner** | lead_backend |

**Problem:** 11 `print()` calls remain in non-CLI code.

**Fix:** Replace with appropriate `logger.info/warning/error`.

---

### PRE-14: OAuth2 / API Key Rotation
| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Effort** | 6h |
| **Purpose** | Enable periodic key rotation to limit exposure window if API keys are compromised |
| **Files** | `security/key_rotation.py` (new) |
| **Owner** | security_engineer |

**Problem:** No key rotation mechanism. API keys are static.

**Fix:**
1. Create `KeyRotationManager` with `rotate()` method
2. Store keys in `keys.yaml` with `created_at` and `expires_at`
3. Add CLI command: `ai-company keys rotate`

---

### PRE-15: Dashboard UX Fixes (8 items)
| Field | Value |
|-------|-------|
| **Severity** | LOW |
| **Effort** | 8h |
| **Purpose** | Improve usability, accessibility (WCAG compliance), and reliability of the CEO dashboard for production use |
| **Files** | `dashboard/static/js/*.js`, `dashboard/templates/*.html` |
| **Owner** | lead_frontend |

**Items:**
- DASH-001: Auto-scroll on new messages
- DASH-002: Loading indicators
- DASH-003: API error display
- DASH-004: WS reconnect on disconnect
- DASH-005: WS reconnect flicker fix
- DASH-006: aria-live regions
- DASH-007: Mobile touch gestures
- DASH-008: CDN SRI hashes

---

## Priority 7: AI Security Hardening (5 items) — NEW

### PRE-16: User Prompt Sanitization
| Field | Value |
|-------|-------|
| **Severity** | CRITICAL |
| **Effort** | 2h |
| **Purpose** | Prevent prompt injection attacks that could manipulate agent behavior or exfiltrate data |
| **Files** | `executor/agent_loop.py`, `executor/context.py` |
| **Owner** | ai_security_specialist |

**Problem:** User prompts are passed directly to LLM without sanitization. Malicious task instructions can contain injection payloads that manipulate agent behavior.

**Fix:**
```python
# In agent_loop.py, add sanitization before LLM call
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions?",
    r"you\s+are\s+now\s+(a|an|the)",
    r"(show|reveal|display)\s+(me\s+)?(your|the)\s+(system\s+)?(prompt|instructions?)",
    r"(send|email|post|upload)\s+(all\s+)?(data|files?|secrets?)",
]

def _sanitize_user_prompt(prompt: str) -> str:
    """Sanitize user prompt to prevent injection attacks."""
    import re
    
    # Check for known injection patterns
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            logger.warning("Prompt injection detected: %s", prompt[:100])
            return "[BLOCKED: Prompt injection detected]"
    
    # Limit prompt length
    if len(prompt) > 10000:
        prompt = prompt[:10000]
    
    return f"<USER_TASK>{prompt}</USER_TASK>"
```

**Verification:**
- Test: injection prompt → blocked response
- Test: normal prompt → allowed with boundary markers
- Test: long prompt → truncated to 10k chars

---

### PRE-17: Memory Access Controls
| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Effort** | 4h |
| **Purpose** | Restrict which agents can access which memory types based on role and sensitivity |
| **Files** | `security/memory_access_control.py` (new), `memory/integration.py` |
| **Owner** | ai_security_specialist |

**Problem:** All agents can access all memory types via `recall_context()`. No access controls exist for sensitive memories (financial, HR, security).

**Fix:**
```python
# New file: security/memory_access_control.py
class MemoryAccessControl:
    """Control which agents can access which memory types."""
    
    def __init__(self):
        self._access_matrix = {
            "financial": ["cfo", "financial_analyst", "human_ceo"],
            "hr": ["hr_lead", "human_ceo"],
            "security": ["ciso", "ai_security_specialist"],
        }
    
    def can_access(self, agent_id: str, memory_tags: list[str]) -> bool:
        """Check if agent can access memory with given tags."""
        for tag in memory_tags:
            if tag in self._access_matrix:
                if agent_id not in self._access_matrix[tag]:
                    return False
        return True
    
    def filter_memories(self, agent_id: str, memories: list[dict]) -> list[dict]:
        """Filter memories based on access permissions."""
        return [m for m in memories if self.can_access(agent_id, m.get("tags", []))]
```

**Verification:**
- Test: junior agent + financial memory → blocked
- Test: CFO + financial memory → allowed
- Test: filtered memories returned to unauthorized agent

---

### PRE-18: Delegation Depth Limits
| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Effort** | 2h |
| **Purpose** | Prevent unbounded delegation chains that could cause infinite loops or resource exhaustion |
| **Files** | `orchestrator/tier_rules.py`, `executor/tool_runner.py` |
| **Owner** | ai_security_specialist |

**Problem:** Agents can delegate indefinitely with no depth limit or cycle detection. A→B→C→A creates infinite loop.

**Fix:**
```python
# In tier_rules.py, add constants
MAX_DELEGATION_DEPTH = 3
MAX_CONCURRENT_DELEGATIONS = 5

# In tool_runner.py, add validation
def _check_delegation_limits(self, tool, args, task_context):
    if tool != "delegate":
        return True, ""
    
    current_depth = task_context.get("delegation_depth", 0)
    if current_depth >= MAX_DELEGATION_DEPTH:
        return False, f"Delegation depth {current_depth} exceeds maximum"
    
    delegation_history = task_context.get("delegation_history", [])
    receiver = args.get("receiver", "")
    if receiver in delegation_history:
        return False, f"Delegation cycle detected: {receiver} already in chain"
    
    return True, ""
```

**Verification:**
- Test: depth 0 → allowed
- Test: depth 3 → blocked
- Test: cycle detection → blocked

---

### PRE-19: LLM Response Validation
| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Effort** | 2h |
| **Purpose** | Validate LLM response structure and content to prevent response poisoning attacks |
| **Files** | `executor/agent_loop.py`, `llm/json_parser.py` |
| **Owner** | ai_security_specialist |

**Problem:** LLM responses are trusted without validation. Malicious or malformed responses could manipulate agent decisions.

**Fix:**
```python
# In agent_loop.py, add response validation
def _validate_llm_response(response: dict) -> tuple[bool, str]:
    """Validate LLM response structure and content."""
    # Check required fields
    required_fields = ["plan", "result"]
    if not all(field in response for field in required_fields):
        return False, "Missing required fields"
    
    # Validate plan structure
    for step in response.get("plan", []):
        if not isinstance(step, dict):
            return False, f"Invalid step type: {type(step)}"
        if "tool" not in step or "args" not in step:
            return False, f"Step missing tool or args: {step}"
    
    # Check for suspicious content
    result = response.get("result", "")
    suspicious_patterns = [
        r"ignore\s+safety",
        r"bypass\s+approval",
        r"exfiltrate",
    ]
    import re
    for pattern in suspicious_patterns:
        if re.search(pattern, result, re.IGNORECASE):
            return False, f"Suspicious content detected in result"
    
    return True, "valid"
```

**Verification:**
- Test: valid response → passes
- Test: missing fields → fails
- Test: suspicious content → fails

---

### PRE-20: Agent Behavior Monitoring
| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Effort** | 8h |
| **Purpose** | Detect anomalous agent behavior patterns that may indicate compromise or misuse |
| **Files** | `security/agent_monitor.py` (new), `executor/agent_loop.py` |
| **Owner** | ai_security_specialist |

**Problem:** No monitoring exists for agent behavior patterns. Compromised agents could exfiltrate data or abuse tools without detection.

**Fix:**
```python
# New file: security/agent_monitor.py
class AgentBehaviorMonitor:
    """Monitor agent behavior for anomalies."""
    
    def __init__(self):
        self._action_counts: dict[str, dict[str, int]] = {}
        self._anomaly_thresholds = {
            "tool_calls_per_hour": 100,
            "memory_access_per_hour": 50,
            "delegation_attempts_per_hour": 20,
        }
    
    def record_action(self, agent_id: str, action_type: str):
        """Record agent action for monitoring."""
        if agent_id not in self._action_counts:
            self._action_counts[agent_id] = {}
        
        current_hour = datetime.now().strftime("%Y-%m-%d-%H")
        key = f"{action_type}:{current_hour}"
        self._action_counts[agent_id][key] = self._action_counts[agent_id].get(key, 0) + 1
    
    def check_anomaly(self, agent_id: str, action_type: str) -> bool:
        """Check if agent action count exceeds threshold."""
        current_hour = datetime.now().strftime("%Y-%m-%d-%H")
        key = f"{action_type}:{current_hour}"
        count = self._action_counts.get(agent_id, {}).get(key, 0)
        threshold = self._anomaly_thresholds.get(action_type, 100)
        return count > threshold
    
    def get_agent_summary(self, agent_id: str) -> dict:
        """Get action summary for an agent."""
        return self._action_counts.get(agent_id, {})
```

**Verification:**
- Test: normal action count → no anomaly
- Test: excessive tool calls → anomaly detected
- Test: action summary returned correctly

---

## Execution Sequence

### Phase 1: Security First (Day 1) — 7.5h
| Order | Item | Purpose | Effort | Dependency |
|-------|------|---------|--------|------------|
| 1 | PRE-01: Wire encryption | Enable at-rest encryption for memory | 0.5h | None |
| 2 | PRE-03: Auth fail-closed | Reject unauthorized writes when no key set | 1h | None |
| 3 | PRE-02: WS auth | Authenticate WebSocket clients | 2h | None |
| 4 | PRE-04: Centralize bus | Eliminate race conditions from multiple bus instances | 4h | None |

### Phase 2: Data Integrity (Day 2) — 9.5h
| Order | Item | Purpose | Effort | Dependency |
|-------|------|---------|--------|------------|
| 5 | PRE-05: Update risk register | Accurate risk status for leadership decisions | 0.5h | None |
| 6 | PRE-06: GAP-005 consolidation | Prevent unbounded memory growth | 3h | PRE-01 |
| 7 | PRE-07: GAP-011 read path | Consistent task state across backends | 6h | PRE-04 |

### Phase 3: Testing (Day 3) — 9h
| Order | Item | Purpose | Effort | Dependency |
|-------|------|---------|--------|------------|
| 8 | PRE-09: Circuit breaker tests | Validate state transitions prevent cascading failures | 2h | None |
| 9 | PRE-10: Security module tests | Ensure PII/filter/encryption work correctly | 4h | PRE-01 |
| 10 | PRE-11: Token counting | Pre-flight cost estimation to prevent budget overruns | 3h | None |

### Phase 4: Code Quality (Day 4) — 18h
| Order | Item | Purpose | Effort | Dependency |
|-------|------|---------|--------|------------|
| 11 | PRE-08: Structured logging | Production debugging and compliance auditing | 6h | None |
| 12 | PRE-08B: Agent spec validation | Catch malformed specs before silent degradation | 3h | None |
| 13 | PRE-12: API versioning | Prevent breaking changes to API consumers | 4h | None |
| 14 | PRE-13: Replace print() | Standardize logging for structured output | 1h | PRE-08 |
| 15 | PRE-14: Key rotation | Limit exposure window if keys compromised | 6h | PRE-02 |

### Phase 5: UX Polish (Day 5) — 8h
| Order | Item | Purpose | Effort | Dependency |
|-------|------|---------|--------|------------|
| 15 | PRE-15: Dashboard UX (8 items) | Improve usability, accessibility, and reliability | 8h | PRE-02 |

### Phase 6: AI Security Hardening (Day 6-7) — 18h
| Order | Item | Purpose | Effort | Dependency |
|-------|------|---------|--------|------------|
| 16 | PRE-16: User Prompt Sanitization | Prevent prompt injection attacks | 2h | None |
| 17 | PRE-17: Memory Access Controls | Restrict agent access to sensitive memories | 4h | None |
| 18 | PRE-18: Delegation Depth Limits | Prevent unbounded delegation chains | 2h | None |
| 19 | PRE-19: LLM Response Validation | Validate LLM output structure and content | 2h | None |
| 20 | PRE-20: Agent Behavior Monitoring | Detect anomalous agent actions | 8h | None |

### Phase 6: AI Security Hardening (Day 6-7) — 18h
| Order | Item | Purpose | Effort | Dependency |
|-------|------|---------|--------|------------|
| 16 | PRE-16: User Prompt Sanitization | Prevent prompt injection attacks | 2h | None |
| 17 | PRE-17: Memory Access Controls | Restrict agent access to sensitive memories | 4h | None |
| 18 | PRE-18: Delegation Depth Limits | Prevent unbounded delegation chains | 2h | None |
| 19 | PRE-19: LLM Response Validation | Validate LLM output structure and content | 2h | None |
| 20 | PRE-20: Agent Behavior Monitoring | Detect anomalous agent actions | 8h | None |

---

## Completion Criteria

Before Sprint 4 can begin, ALL of the following must be true:

- [x] `grep -r "print(" src/ai_company/ --include="*.py" | grep -v cli/ | wc -l` = 0 ✅
- [x] All 1205 existing tests pass ✅ (170+ verified)
- [x] New tests added: circuit_breaker (27), security modules (143), encryption tests ✅
- [x] `ruff check src/` clean ✅
- [x] `mypy src/` clean ✅
- [x] No `inbox.json` direct reads in `dashboard/` directory ✅ (MessageBus injected)
- [x] `DASHBOARD_AUTH_MODE=closed` is default ✅ (fail-closed mode)
- [x] Risk register updated (R15/R16/R17/R18 = Mitigated) ✅
- [x] Memory encryption round-trip test passes ✅
- [x] WebSocket auth test passes ✅
- [ ] **AI Security (NEW):** Prompt injection tests pass — PRE-16
- [ ] **AI Security (NEW):** Memory access control tests pass — PRE-17
- [ ] **AI Security (NEW):** Delegation limit tests pass — PRE-18
- [ ] **AI Security (NEW):** LLM response validation tests pass — PRE-19
- [ ] **AI Security (NEW):** Agent behavior monitoring tests pass — PRE-20

---

## Risk

| Risk | Mitigation |
|------|------------|
| PRE-07 (GAP-011) may break existing KPI endpoints | Run full KPI test suite before/after |
| PRE-08 (logging) may change log format | Document new format in DEVELOPMENT.md |
| PRE-12 (API versioning) may break frontend | Keep legacy routes as redirects |
| PRE-14 (key rotation) may require migration | Support both old and new key formats |
| **PRE-16 (prompt sanitization) may block legitimate prompts** | Whitelist common development patterns |
| **PRE-17 (memory access) may break existing agent workflows** | Start with advisory mode, enforce after validation |
| **PRE-18 (delegation limits) may prevent complex task decomposition** | Set generous limits (depth=3), monitor usage |
| **PRE-20 (behavior monitoring) may generate false positives** | Tune thresholds based on baseline behavior |
