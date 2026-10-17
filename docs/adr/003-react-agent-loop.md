# ADR-003: Why ReAct Pattern for Agent Loop

**Status:** Accepted
**Date:** 2026-07-17
**Deciders:** CTO, CAIO
**Technical Domain:** Agent Execution

## Context

AI Company Builder needs an agent execution loop that:
- Processes tasks assigned via the MessageBus
- Allows agents to reason about tasks before acting
- Enables multi-step task completion (agent thinks, acts, observes, repeats)
- Enforces budget limits per task and per day
- Supports human-in-the-loop (HITL) approval gates for dangerous operations
- Tracks LLM token usage and costs at each iteration

## Decision

We use the **ReAct (Reason + Act) pattern** for the agent execution loop.

## The ReAct Pattern

```
Task arrives
  → Agent REASONs about the task (LLM call)
  → Agent ACTs (tool call or response)
  → Agent OBSERVES the result
  → If done: complete the task
  → If not: loop back to REASON
  → Budget check at each iteration
  → HITL gate for dangerous actions
```

## Options Considered

### 1. ReAct pattern (chosen)

```
observe → think → act → observe → think → act → ... → done
```

**Pros:**
- Well-understood pattern with strong academic backing (Yao et al., 2022)
- Natural fit for multi-step tasks that require tool use
- Transparent reasoning chain — easy to debug and audit
- Budget enforcement at each iteration boundary
- Easy to inject HITL gates between think and act

**Cons:**
- Can loop indefinitely without proper termination conditions
- Each iteration costs tokens (reasoning overhead)

### 2. Chain-of-Thought (single-shot)

```
think → act (one shot)
```

**Pros:**
- Lower latency, fewer tokens
- Simpler implementation

**Cons:**
- Cannot handle multi-step tasks
- No opportunity to observe results and adjust
- Not suitable for tasks requiring tool interaction

### 3. Plan-and-Execute

```
plan (full plan) → execute steps sequentially
```

**Pros:**
- More efficient for well-structured tasks
- Clear progress tracking

**Cons:**
- Rigid — cannot adapt plan based on intermediate results
- Planning LLM call is expensive (long output)
- Harder to implement HITL gates mid-execution

### 4. Autonomous (no loop)

```
LLM call → single response → done
```

**Pros:**
- Simplest implementation
- Lowest latency

**Cons:**
- Cannot use tools
- Cannot complete multi-step tasks
- Limited to tasks solvable in a single LLM response

## Consequences

### Positive

- **Multi-step capability**: Agents can chain tool calls to complete complex tasks
- **Budget safety**: `CostTracker.check_budget()` runs at each iteration, halting if exceeded
- **HITL integration**: `HITLGate` can intercept between think and act for approval
- **Transparency**: Full reasoning trace is logged for debugging and auditing
- **Flexibility**: Agents can adapt their approach based on intermediate results
- **Cost control**: `LoopConfig.max_iterations` prevents runaway loops

### Negative

- **Token overhead**: Each reasoning step costs tokens (mitigated: budget caps)
- **Loop risk**: Without termination conditions, agents could loop indefinitely (mitigated: max_iterations)
- **Complexity**: More complex than single-shot (mitigated: well-structured executor code)

### Mitigations

- `LoopConfig.max_iterations` (default: 10) caps the number of think-act cycles
- `CostTracker` enforces per-task and daily budget limits
- `HITLGate` intercepts dangerous tool calls for human approval
- Agent loops terminate on: completion signal, budget exceeded, max iterations, or fatal error

## Implementation

```python
# Simplified AgentLoop.run()
for iteration in range(max_iterations):
    # Budget check
    allowed, reason = cost_tracker.check_budget(task_id)
    if not allowed:
        break

    # Reason (LLM call)
    response = llm_client.complete(messages, tools=available_tools)

    # Act (tool call or final answer)
    if response.tool_calls:
        for tool_call in response.tool_calls:
            # HITL gate check
            if hitl_gate.requires_approval(tool_call):
                approval = hitl_gate.request_approval(tool_call)
                if not approval.approved:
                    continue

            result = tool_runner.execute(tool_call)
            messages.append(result)
    else:
        # Final answer — task complete
        break
```

## Evidence

- The executor loop in `src/ai_company/executor/loop.py` implements this pattern
- Budget enforcement halts loops that would exceed limits
- HITL gates intercept dangerous operations before execution
- 466 tests cover the executor loop with various scenarios

## References

- Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (2022)
- `src/ai_company/executor/loop.py` — Agent execution loop
- `src/ai_company/executor/hitl_gate.py` — Human-in-the-loop gates
- `src/ai_company/llm/cost_tracker.py` — Budget enforcement
- `docs/ARCHITECTURE.md` — Executor module documentation
