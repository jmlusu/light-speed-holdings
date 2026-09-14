# Issue #45 — Health & Anomaly Monitor (F4)

**Requirement F4**: Real-time agent health monitor that detects stuck loops, token spikes,
hallucination risk, failed tool calls, and produces red-flag indicators with
reset/pause/context-window controls.

**Status**: Design — open for implementation
**Date**: 2026-08-19
**Owner**: AI Safety Lead
**Related files**: `dashboard/monitoring.py`, `dashboard/org_health.py`, `dashboard/api.py`,
`dashboard/ws.py`, `dashboard/static/js/health.js`, `config/org_health.yaml`

---

## 0. Existing State

| Layer | What exists | Gap |
|-------|------------|-----|
| Z-score anomaly detector | `OrgHealthCalculator.detect_anomalies()` — runs on org-health component deltas (task_success_rate, agent_utilization, cost_efficiency, error_rate) | Only detects org-level score drift; no per-agent or per-invocation detectors |
| Daemon health file | `ExecutorDaemon` writes `logs/executor-daemon.json` with PID/uptime/ticks | Checked by `/api/v1/daemon/status`; no auto-recovery wiring |
| `/health` endpoint | Deep check: inbox, registry, agents, audit, disk, memory, DLQ | No agent-level health semantics (stuck loop, token spike, etc.) |
| `/metrics` (Prometheus) | LLM cost, error rate, circuit breaker, task status, per-agent success/failure | Counter-only; no windowed rate detectors or sliding-window buffers |
| Frontend | Alpine.js `healthMonitor()` — org health score, trend chart, anomaly list | No per-agent health cards, no action controls, no real-time WS health topic |
| WebSocket | `ConnectionManager` with topic subscriptions (`kpis`, `tasks`, `alerts`, `org_health`, `daemon`) | No `health` topic; no per-agent health broadcast |

---

## 1. Detector Catalog

All detectors live in a new module `src/ai_company/dashboard/health_detectors.py`.
Each detector is a class conforming to the `HealthDetector` protocol. The monitor
runs all detectors on a configurable cadence (default: every 30 seconds) and
emits `HealthEvent` records.

### 1.1 Detector Protocol

```python
class HealthDetector(Protocol):
    """Base protocol for all health detectors."""

    name: str
    severity_default: str  # "info" | "warning" | "critical"

    def evaluate(
        self,
        agent_id: str,
        audit_events: list[dict[str, Any]],
        task_history: list[dict[str, Any]],
        sliding_window: SlidingWindow,
    ) -> HealthEvent | None:
        """Return a HealthEvent if an anomaly is detected, else None."""
        ...
```

### 1.2 New Detectors

| # | Detector | Signal source | Detection logic | Default severity |
|---|----------|--------------|----------------|-----------------|
| D1 | **Stuck Loop Detector** | Audit log `tool_call` events (same tool + same args hash) | If ≥5 consecutive identical tool calls (same tool name + SHA-256 of args) within a 10-minute window, emit `stuck_loop`. Severity escalates to `critical` at ≥10 repeats. | warning → critical |
| D2 | **Token Spike Detector** | Audit log `tool_call` / `tool_result` events (prompt_tokens + completion_tokens) | Compute per-agent rolling 15-minute token rate. Z-score > 2.5 against the agent's 24h baseline = `token_spike`. Hard cap: if tokens/minute exceeds `TOKEN_HARD_CAP` (configurable, default 50,000), always `critical`. | warning → critical |
| D3 | **Hallucination Risk Signals** | Audit log events with `severity: error` + output format violations | Track (a) consecutive refusals (tool_result containing refusal patterns), (b) output format violations (malformed JSON/Markdown when structured output expected). ≥3 refusals in 5 minutes or ≥2 format violations in 10 minutes = `hallucination_risk`. | warning |
| D4 | **Failed Tool Call Rate Monitor** | Audit log `tool_result` events with `success: false` | Sliding-window error rate over last 10 calls per agent. If error_rate > 50% (≥5 of last 10 failed), emit `high_tool_failure_rate`. If error_rate > 80%, escalate to `critical`. | warning → critical |
| D5 | **Response Latency Outlier Detector** | Audit log `tool_call` → `tool_result` pairs (delta of timestamps) | Per-agent median latency over last 20 calls. If current call latency > 3× median, emit `latency_outlier`. If latency > 60 seconds for any single call, emit `critical_latency`. | warning → critical |

### 1.3 Existing Z-Score Detector (Preserved)

The existing `OrgHealthCalculator.detect_anomalies()` (z-score on org-health component deltas) continues to run unchanged. It feeds into the org-level anomaly timeline. The new detectors operate at the **per-agent** level and compose into the same `HealthEvent` format.

### 1.4 Data Structures

```python
@dataclass
class HealthEvent:
    """A single health anomaly detected for an agent."""

    id: str                          # UUID
    agent_id: str
    detector: str                    # e.g. "stuck_loop", "token_spike"
    severity: str                    # "info" | "warning" | "critical"
    timestamp: str                   # ISO 8601
    message: str                     # Human-readable description
    metadata: dict[str, Any]         # Detector-specific payload
    action_taken: str | None = None  # "auto_paused" | "context_reset" | None

    def to_dict(self) -> dict[str, Any]: ...


@dataclass
class AgentHealthStatus:
    """Rolling health summary for a single agent."""

    agent_id: str
    status: str                      # "healthy" | "degraded" | "critical" | "paused"
    active_anomalies: list[HealthEvent]
    last_check: str
    consecutive_failures: int
    token_rate_15m: float            # tokens/min
    tool_error_rate_10: float        # 0.0–1.0
    stuck_loop_detected: bool
    paused_by: str | None            # "auto" | "manual" | None
    paused_at: str | None

    def to_dict(self) -> dict[str, Any]: ...
```

---

## 2. Severity Classification

Severity is assigned per-event by the detector and maps to agent-level status:

| Agent Status | Condition | Colour |
|-------------|-----------|--------|
| `healthy` | No active anomalies, or only `info`-level events | Green |
| `degraded` | ≥1 `warning`-level anomaly active | Amber |
| `critical` | ≥1 `critical`-level anomaly active, OR ≥3 warnings in 10 minutes | Red |
| `paused` | Agent was auto-paused or manually paused | Grey with pause icon |

### 2.1 Severity → Action Matrix

| Severity | Auto-action | Dashboard action available |
|----------|------------|---------------------------|
| `info` | Log only | View details |
| `warning` | Log + broadcast WS event | View details, manual pause, reset context |
| `critical` | Auto-pause agent (after cool-down, see §3) + broadcast WS alert | Resume, reset context, view logs, adjust thresholds |

### 2.2 Composite Severity Roll-up

An agent's composite status is the **maximum** severity of its active anomalies, subject to the 3-warnings → critical escalation rule:

```python
def _rollup_status(events: list[HealthEvent]) -> str:
    critical_count = sum(1 for e in events if e.severity == "critical")
    warning_count = sum(1 for e in events if e.severity == "warning")
    if critical_count > 0 or warning_count >= 3:
        return "critical"
    if warning_count > 0:
        return "degraded"
    return "healthy"
```

---

## 3. Auto-Pause Wiring

### 3.1 Trigger Conditions

An agent is auto-paused when **any** of the following hold:

| Trigger | Condition | Cooldown before pause |
|---------|-----------|----------------------|
| Critical anomaly | ≥1 event with `severity: "critical"` | 60 seconds (allows transient spikes to self-resolve) |
| Sustained degradation | ≥3 warnings within 10 minutes | 120 seconds |
| Stuck loop (critical) | ≥10 consecutive identical tool calls | Immediate (no cooldown — loop is self-confirming) |
| Token hard cap | Token rate > `TOKEN_HARD_CAP` for > 2 minutes | 30 seconds |

### 3.2 Cool-down Mechanism

```python
class AutoPauseController:
    """Manages auto-pause lifecycle for agents."""

    _pending_pauses: dict[str, float]  # agent_id → timestamp when pause was first warranted
    _paused_agents: dict[str, PausedAgentRecord]

    def evaluate(self, agent_id: str, status: str) -> PauseAction | None:
        """Return a PauseAction if the agent should be paused, else None.

        Implements the cool-down: the agent must be in a triggering state
        for the full cool-down period before the pause fires.
        """
        ...

    def resume(self, agent_id: str, reason: str) -> None: ...
    def force_reset(self, agent_id: str) -> None: ...
```

### 3.3 Recovery Conditions

An auto-paused agent resumes automatically when:

1. **All active critical anomalies have cleared** (no critical events in the last 5 minutes).
2. **Cool-down satisfied**: the agent has been anomaly-free for ≥5 minutes.
3. **Manual override**: a human clicks "Resume" on the dashboard (bypasses cool-down).

Upon resume, the agent receives a `context_reset` signal that clears its sliding-window state and starts fresh.

### 3.4 Pause/Resume Implementation

The auto-pause controller integrates with the existing MessageBus:

```python
# When auto-pause fires:
def _auto_pause_agent(agent_id: str, event: HealthEvent) -> None:
    # 1. Write pause record to .opencode/health/pauses.json
    # 2. Set agent task receiver to reject new tasks (MessageBus filter)
    # 3. Broadcast WS "health" event with action: "auto_paused"
    # 4. Log to audit trail
    ...

# When resume fires:
def _resume_agent(agent_id: str, reason: str) -> None:
    # 1. Remove pause record
    # 2. Re-enable task receiver
    # 3. Reset agent's sliding window state
    # 4. Broadcast WS "health" event with action: "resumed"
    # 5. Log to audit trail
    ...
```

### 3.5 Context Window Controls

| Action | Endpoint | Effect |
|--------|----------|--------|
| Reset context | `POST /api/v1/agents/:id/context/reset` | Clears the agent's sliding-window buffers, resets token counters, restarts anomaly baselines |
| View context | `GET /api/v1/agents/:id/context` | Returns current sliding-window state (recent tool calls, token usage, error counts) |
| Adjust thresholds | `PATCH /api/v1/agents/:id/health/thresholds` | Override detector thresholds per-agent (stored in `config/agent_health_overrides.yaml`) |

---

## 4. UI Contract

### 4.1 Per-Agent Health Cards

Each agent gets a card in the health dashboard. Layout:

```
┌──────────────────────────────────────────────────┐
│  🟢 ceo-strategist                    Healthy    │
│  ──────────────────────────────────────────────  │
│  Tasks: 47 completed  │  Errors: 2.1%           │
│  Token rate: 1,240 tok/min  │  Latency: 3.2s    │
│  Last anomaly: 2h ago (info: latency_outlier)    │
│                                                  │
│  [Pause]  [Reset Context]  [View Logs]           │
└──────────────────────────────────────────────────┘
```

Status indicator colours:
- Healthy: green dot (`bg-emerald-500`)
- Degraded: amber dot with pulse animation (`bg-amber-500 animate-pulse`)
- Critical: red dot with pulse (`bg-red-500 animate-pulse`)
- Paused: grey dot with pause icon (`bg-slate-500`)

### 4.2 Anomaly Timeline

A scrollable list below the agent cards, showing all recent anomalies across all agents:

```
┌─ Anomaly Timeline ──────────────────────────────────┐
│ 🔴 12:03  ceo-strategist  stuck_loop               │
│    └ Identical tool_call ×8 in 7min (read file)     │
│    [Auto-paused at 12:04]                            │
│                                                      │
│ ⚠️  11:58  finance-analyst  token_spike              │
│    └ Token rate 48,200 tok/min (baseline: 12,000)   │
│    [View Details]                                    │
│                                                      │
│ 📊 11:45  (org-level) cost_efficiency drop           │
│    └ Cost efficiency: 72% → 51% (-29.2%)            │
│    [View Details]                                    │
└──────────────────────────────────────────────────────┘
```

### 4.3 Action Controls

| Button | Visible when | Action | RBAC |
|--------|-------------|--------|------|
| **Pause** | Agent status ≠ `paused` | `POST /api/v1/agents/:id/pause` | `approve` |
| **Resume** | Agent status = `paused` | `POST /api/v1/agents/:id/resume` | `approve` |
| **Reset Context** | Always visible | `POST /api/v1/agents/:id/context/reset` | `run` |
| **View Logs** | Always visible | Opens agent audit log panel (filtered to last 50 events) | None |
| **Adjust Thresholds** | On agent detail modal | `PATCH /api/v1/agents/:id/health/thresholds` | `admin` |

### 4.4 Frontend Component Structure

```
health-dashboard.js (new)
├── agentHealthCard(agent)      — Per-agent status card
├── anomalyTimeline(events)     — Scrollable anomaly feed
├── healthActionPanel(agent)    — Pause/Resume/Reset controls
├── detectorConfigModal(agent)  — Threshold override editor
└── healthWSTarget()            — WebSocket subscriber for "health" topic
```

Integration point: the existing `healthMonitor()` Alpine.js component in `health.js` is extended to:
1. Load agent health statuses from `GET /api/v1/agents/health`
2. Subscribe to the `health` WebSocket topic for real-time updates
3. Render agent cards and anomaly timeline alongside existing org-health views

---

## 5. WebSocket Integration

### 5.1 New `health` Topic

A new WebSocket topic `health` carries per-agent health events in real-time.

**Broadcast helper** (add to `ws.py`):

```python
async def broadcast_health_event(event: dict[str, Any]) -> None:
    """Push a per-agent health event to subscribed dashboard clients."""
    await manager.broadcast(
        {
            "type": "health_event",
            "topic": "health",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": event,
        }
    )
```

**Message shapes**:

```jsonc
// New anomaly detected
{
  "type": "health_event",
  "topic": "health",
  "event": "anomaly_detected",
  "payload": {
    "id": "uuid",
    "agent_id": "ceo-strategist",
    "detector": "stuck_loop",
    "severity": "critical",
    "message": "Identical tool_call ×8 in 7min (read file)",
    "metadata": { "repeat_count": 8, "tool": "read", "window_seconds": 420 }
  }
}

// Agent status change
{
  "type": "health_event",
  "topic": "health",
  "event": "status_change",
  "payload": {
    "agent_id": "ceo-strategist",
    "previous_status": "degraded",
    "new_status": "paused",
    "reason": "auto_paused: stuck_loop (critical)"
  }
}

// Auto-pause triggered
{
  "type": "health_event",
  "topic": "health",
  "event": "auto_paused",
  "payload": {
    "agent_id": "ceo-strategist",
    "trigger_event_id": "uuid",
    "cooldown_seconds": 60,
    "resumes_at": "2026-08-19T12:05:00Z"
  }
}
```

### 5.2 Client Subscription

Frontend subscribes on dashboard load:

```javascript
// In health.js init()
ws.send(JSON.stringify({
  type: 'subscribe',
  topics: ['health']
}));
```

### 5.3 Broadcast Cadence

| Event type | Trigger | Rate limit |
|-----------|---------|-----------|
| `anomaly_detected` | Detector fires | Every detector evaluation (30s default) |
| `status_change` | Agent health status transitions | Immediate on transition |
| `auto_paused` | Auto-pause fires | Immediate |
| `health_snapshot` | Periodic full-state push | Every 5 minutes (catch-up for reconnected clients) |

---

## 6. API Endpoints (New)

| Method | Path | Description | RBAC |
|--------|------|-------------|------|
| `GET` | `/api/v1/agents/health` | Return `AgentHealthStatus` for all agents | `run` |
| `GET` | `/api/v1/agents/:id/health` | Return `AgentHealthStatus` for one agent | `run` |
| `GET` | `/api/v1/agents/:id/health/events` | Return recent health events for an agent (paginated) | `run` |
| `POST` | `/api/v1/agents/:id/pause` | Manually pause an agent | `approve` |
| `POST` | `/api/v1/agents/:id/resume` | Resume a paused agent | `approve` |
| `POST` | `/api/v1/agents/:id/context/reset` | Reset agent's sliding-window state | `run` |
| `GET` | `/api/v1/agents/:id/context` | View agent's current sliding-window state | `run` |
| `PATCH` | `/api/v1/agents/:id/health/thresholds` | Override detector thresholds per-agent | `admin` |

---

## 7. Configuration

### 7.1 Detector Config (`config/health_detectors.yaml`)

```yaml
# Health detector configuration
cadence_seconds: 30

detectors:
  stuck_loop:
    enabled: true
    min_repeats_warning: 5
    min_repeats_critical: 10
    window_seconds: 600  # 10 minutes

  token_spike:
    enabled: true
    z_score_threshold: 2.5
    baseline_window_hours: 24
    evaluation_window_minutes: 15
    hard_cap_per_minute: 50000

  hallucination_risk:
    enabled: true
    refusal_threshold: 3        # refusals in window
    format_violation_threshold: 2
    refusal_window_seconds: 300  # 5 minutes
    format_window_seconds: 600   # 10 minutes

  tool_failure_rate:
    enabled: true
    window_size: 10             # last N calls
    warning_rate: 0.5           # 50%
    critical_rate: 0.8          # 80%

  latency_outlier:
    enabled: true
    multiplier_warning: 3.0     # × median
    single_call_critical_sec: 60
    baseline_window: 20         # last N calls for median

auto_pause:
  cool_down_seconds:
    critical: 60
    sustained_degradation: 120
    stuck_loop_critical: 0      # immediate
    token_hard_cap: 30
  recovery_anomaly_free_minutes: 5
  token_hard_cap_per_minute: 50000
```

### 7.2 Per-Agent Overrides (`config/agent_health_overrides.yaml`)

```yaml
# Per-agent threshold overrides (optional)
overrides:
  ceo-strategist:
    token_spike:
      hard_cap_per_minute: 80000  # higher cap for CEO agent
  finance-analyst:
    tool_failure_rate:
      warning_rate: 0.3           # stricter for finance
```

---

## 8. File Layout (New/Modified)

| File | Change | Purpose |
|------|--------|---------|
| `src/ai_company/dashboard/health_detectors.py` | **New** | All detector classes, `HealthEvent`, `AgentHealthStatus`, `AutoPauseController` |
| `src/ai_company/dashboard/monitoring.py` | **Modify** | Add `GET /api/v1/agents/health` and agent health endpoints |
| `src/ai_company/dashboard/ws.py` | **Modify** | Add `broadcast_health_event()` helper |
| `src/ai_company/dashboard/api.py` | **Modify** | Wire auto-pause into MessageBus lifecycle; add pause/resume/context endpoints |
| `src/ai_company/dashboard/static/js/health.js` | **Modify** | Extend `healthMonitor()` with agent cards, anomaly timeline, action controls |
| `config/health_detectors.yaml` | **New** | Detector thresholds and auto-pause config |
| `config/agent_health_overrides.yaml` | **New** | Per-agent threshold overrides |
| `tests/dashboard/test_health_detectors.py` | **New** | Unit tests for all detectors |

---

## 9. Implementation Phases

| Phase | Scope | Estimated effort |
|-------|-------|-----------------|
| **P1: Detectors** | Implement `HealthDetector` protocol + D1–D5 detectors + `HealthEvent` / `AgentHealthStatus` dataclasses + unit tests | 2–3 days |
| **P2: Auto-Pause** | `AutoPauseController` + cooldown logic + MessageBus integration + audit logging | 1–2 days |
| **P3: API Layer** | New endpoints in `monitoring.py` + `api.py` + WebSocket `health` topic broadcast | 1–2 days |
| **P4: Frontend** | Agent health cards + anomaly timeline + action controls in `health.js` | 2–3 days |
| **P5: Config & Tuning** | YAML config loading, per-agent overrides, threshold tuning against production audit data | 1 day |

**Total**: 7–11 days

---

## 10. Open Questions

1. **Should auto-pause affect the MessageBus task assignment, or only the executor daemon?** Recommendation: MessageBus filter (reject new tasks for paused agents) + executor skip (don't pick up paused agents' pending tasks).

2. **Token hard cap: per-request or per-minute rolling window?** Recommendation: per-minute rolling window (already specified above). A single large request shouldn't trigger a false positive.

3. **Should the `health_snapshot` periodic broadcast include full `AgentHealthStatus` for all agents, or only changed agents?** Recommendation: full snapshot every 5 minutes (lightweight; there are typically <20 agents).

4. **Hallucination risk: should we add LLM-based output quality scoring (e.g., checking for coherence) or stick to signal-based detection?** Recommendation: signal-based only for v1 (refusals + format violations). LLM-based scoring can be a future detector (D6).

---

## 11. Success Criteria

- [ ] All 5 detectors (D1–D5) implemented with unit tests covering normal, warning, and critical thresholds
- [ ] Auto-pause fires correctly with cool-down; resume works after anomaly clearance
- [ ] WebSocket `health` topic delivers real-time events to subscribed dashboard clients
- [ ] Agent health cards render with correct status colours and action buttons
- [ ] Anomaly timeline shows all recent events with expandable details
- [ ] Context reset clears sliding-window state and restarts baselines
- [ ] Per-agent threshold overrides load from YAML and take effect on next evaluation cycle
