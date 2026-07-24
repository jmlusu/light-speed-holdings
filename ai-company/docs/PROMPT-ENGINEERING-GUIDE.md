# Prompt Engineering Guide for AI Company Builder

This guide covers prompt design patterns for the agent hierarchy, ReAct loop, tool use, and approval tier classification.

---

## 1. System Prompt Design for the Agent Hierarchy

### 1.1 Agent Spec Cards

Every agent has a **spec card** (`AgentContext`) that feeds the system prompt. The generator builds these from `company-registry.yaml` via the Jinja2 template at `templates/agents/agent.md.j2`.

**Key fields in a system prompt:**

| Field | Purpose | Example |
|-------|---------|---------|
| `name` | Agent identity | `lead-backend` |
| `role` | One-line purpose | "Senior backend engineer" |
| `type` | Hierarchy tier | `executive`, `specialist`, `lead` |
| `tools` | Allowed tool list | `["read", "write", "execute", "grep"]` |
| `permissions` | Approval tier overrides | `{"write": 2, "execute": 3}` |
| `reporting_to` | Manager agent | `chief_of_staff` |

### 1.2 System Prompt Structure

The system prompt for every agent follows this template:

```
You are {name}, a {type} agent in the AI Company Builder hierarchy.

Role: {role}
Reports to: {reporting_to}

## Allowed Tools
{tool_list_with_descriptions}

## Output Format
Always respond with valid JSON:
{
  "thought": "Your reasoning about the task",
  "plan": [{"tool": "...", "args": {...}}],
  "result": "Final answer (when done)",
  "done": true|false
}

## Rules
1. Only use tools listed above.
2. Plan one step at a time; wait for tool results before planning next.
3. If unsure, ask your manager before acting.
4. Signal done=true when the task is complete.
```

### 1.3 Best Practices

**Be explicit about constraints.** Don't assume the LLM knows what tools exist. List every allowed tool with a one-line description.

**Declare the output format in the system prompt, not the user prompt.** The system prompt persists across all iterations; repeating the format each turn wastes tokens.

**Use role-appropriate language.** Executive agents get strategic language ("prioritize", "delegate", "escalate"). Specialist agents get operational language ("implement", "test", "verify").

**Include escalation rules.** Tell the agent when to ask for help:

```
Escalate to your manager when:
- A tool action requires Tier 3+ approval
- You encounter ambiguity that blocks progress
- The task exceeds your domain expertise
```

---

## 2. Chain-of-Thought Patterns for ReAct Loops

The agent loop follows the **ReAct** pattern: Reason → Act → Observe → Repeat.

### 2.1 Single-Step ReAct Prompt

For simple tasks (one tool call):

```json
{
  "thought": "The user wants the current server status. I need to read the health check file.",
  "plan": [
    {"tool": "read", "args": {"path": "health.json"}}
  ],
  "result": "",
  "done": false
}
```

### 2.2 Multi-Step ReAct Prompt

For complex tasks (sequential tool calls):

```json
{
  "thought": "I need to: 1) find the config file, 2) read it, 3) update the port, 4) write it back.",
  "plan": [
    {"tool": "glob", "args": {"pattern": "**/config.yaml"}},
    {"tool": "read", "args": {"path": "{{result_from_step_0}}"}},
    {"tool": "write", "args": {"path": "{{result_from_step_1}}", "content": "..."}}
  ],
  "result": "",
  "done": false
}
```

### 2.3 Iteration Feedback Pattern

After each tool execution, the loop feeds results back to the LLM:

```
=== Iteration {n}/{max} ===
Tool results:
  Step 1: {tool_name} → {status}
    {result_summary}

Plan the next step or signal done=true.
```

**Best practice:** Keep iteration feedback concise. Summarize tool results in 1-2 lines; don't dump raw JSON back to the LLM (it wastes context window).

### 2.4 CoT Guardrails

| Problem | Fix |
|---------|-----|
| LLM skips reasoning, goes straight to tools | Add `"You must explain your reasoning in 'thought' before planning tools."` |
| LLM plans too many tools at once | Add `"Plan at most 3 tools per iteration. Wait for results before planning more."` |
| LLM never signals done | Add `"When all steps are complete, set done=true and put the final answer in 'result'."` |
| LLM hallucinates tool names | Include exact tool names in the system prompt; the tool runner rejects unknown tools |

---

## 3. Tool Use Prompt Patterns

### 3.1 Tool Description Format

Each tool is described in the system prompt as:

```
## Tool: {tool_name}
Description: {one_line_description}
Arguments:
  - {arg_name} ({type}): {description} [required|optional]
Approval tier: {default_tier}
```

**Example:**

```
## Tool: read
Description: Read the contents of a file
Arguments:
  - path (string): File path relative to workspace root [required]
Approval tier: 0 (auto-approve)
```

### 3.2 Tool Argument Validation

The `ToolRunner` validates arguments before execution. Prompts should teach agents to produce well-formed arguments:

```
When planning a tool call, always provide:
1. The exact tool name (case-sensitive)
2. All required arguments as a JSON object
3. Use relative paths (e.g., "src/main.py", not "/absolute/path")

Bad:  {"tool": "Read", "args": {"file": "/etc/passwd"}}
Good: {"tool": "read", "args": {"path": "src/main.py"}}
```

### 3.3 Tool Result Interpretation

Teach agents to interpret common tool statuses:

```
Tool result statuses:
- "success": The tool executed correctly. Use the result.
- "error": The tool failed. Plan a fix or escalate.
- "approval_pending": The tool requires human approval. Wait.
- "approval_rejected": A human rejected this action. Explain why and try an alternative.
```

### 3.4 Conditional Tool Planning

For tools that depend on previous results:

```
Plan your tool calls sequentially. If a tool returns an error,
do NOT continue with dependent steps. Instead:
1. Analyze the error.
2. Try a corrective action (fix the error, try a different path).
3. Then resume the original plan.

Example flow:
  glob → finds "config.yaml"
  read → reads "config.yaml"
  write → updates "config.yaml" (only if read succeeded)
```

---

## 4. Approval Tier Classification Prompt Optimization

The 5-tier approval system (Tiers 0-4) uses an LLM classifier to determine the risk level of tool actions.

### 4.1 Classification Prompt Structure

The classifier prompt (in `orchestrator/approval_prompts.py`) follows this structure:

```
1. Define the 5 tiers with examples
2. Provide classification rules (tool default → path escalation → command escalation)
3. Give the input: tool name, args summary, agent seniority, risk level
4. Request: respond with tier number only (0-4)
```

### 4.2 Optimizing Classification Accuracy

**Rule 1: Tool default is the baseline.** Read/list/grep → Tier 0. Write/edit → Tier 2. Execute → Tier 2.

**Rule 2: Path overrides escalate.** A `write` to `secrets/api_key.yaml` → Tier 4, not Tier 2.

**Rule 3: Seniority affects auto-approval.** Executives may auto-approve Tier ≤ 2 actions.

**Rule 4: Task risk escalates.** A critical-priority task escalates all tool actions by one tier.

### 4.3 Classification Prompt Best Practices

| Practice | Why |
|----------|-----|
| Use numbered tiers (0-4) in the prompt | LLMs parse numbers better than names |
| Give concrete path examples | `"secrets/" → Tier 4` is unambiguous |
| End with "Respond with the tier number only" | Prevents verbose explanations that waste tokens |
| Include agent seniority as context | Prevents unnecessary escalation for executive agents |

### 4.4 Handling Edge Cases

**Ambiguous actions:** When the classifier is unsure, it should default to the higher tier:

```
If an action could belong to multiple tiers, always choose the higher tier.
Safety over speed.
```

**Unknown tools:** Tools not in the classification list should default to Tier 2 (single approver):

```
For any tool not listed above, classify as Tier 2 and flag for review.
```

**Bulk operations:** If a plan contains multiple tool calls, classify the *highest-risk* individual action, not the aggregate:

```
Classify each tool call independently. The plan's tier is the maximum
of all individual tool tiers.
```

---

## 5. Model Router Integration

### 5.1 Domain-Aware Routing

The model router detects task domains from keyword heuristics in the user prompt:

| Domain | Keywords (≥2 hits) | Default Tier |
|--------|---------------------|--------------|
| `finance` | financial, budget, audit, tax, revenue | `standard` or `premium` |
| `legal` | contract, agreement, regulation, patent | `standard` or `premium` |
| `security` | vulnerability, exploit, breach, encryption | `premium` |
| `code_review` | review, pull request, diff, refactor | `standard` |
| `deployment` | deploy, release, production, rollback | `standard` |
| `data_science` | training, dataset, feature, epoch | `premium` |

**Configure in `models.yaml`:**

```yaml
routing:
  - context: domain_finance
    tier: standard
  - context: domain_security
    tier: premium
  - context: domain_code_review
    tier: fast
```

### 5.2 Quality-Based Fallback

When all providers in the current tier fail, the router automatically promotes to the next tier:

```
fast → standard → premium
```

The `resolve_with_fallback()` method returns an ordered list of routes. The agent loop iterates through them until a provider responds successfully.

### 5.3 Priority Forwarding (GAP-012 Fix)

The agent loop now forwards the actual task priority to the model router instead of hardcoding `"medium"`. Priority affects routing:

| Priority | Effect |
|----------|--------|
| `low` | Routes to `fast` tier (cheapest models) |
| `medium` | Routes to `standard` tier (balanced) |
| `high` | Routes to `premium` tier (best quality) |
| `critical` | Routes to `premium` tier + escalation context |

---

## 6. Testing Prompts

### 6.1 Unit Test Pattern

Test prompt builders with known inputs:

```python
from ai_company.executor.prompts import build_system_prompt_typed
from ai_company.executor.context import AgentContext

def test_system_prompt_includes_tool_list():
    agent = AgentContext(
        name="test_agent",
        type="specialist",
        role="Test specialist",
        tools=["read", "write"],
    )
    prompt = build_system_prompt_typed(agent)
    assert "read" in prompt
    assert "write" in prompt
    assert "execute" not in prompt  # Not in tool list
```

### 6.2 Integration Test Pattern

Test the full loop with a mock LLM provider:

```python
def test_agent_loop_completes():
    mock_provider = MockLLMProvider(response={"done": True, "result": "OK"})
    llm = LLMClient(providers=[mock_provider])
    runner = ToolRunner(tools={"read": MockReadTool()})

    loop = AgentLoop(llm=llm, runner=runner)
    agent = AgentContext(name="test", type="specialist", role="Test", tools=["read"])
    result = loop.run(agent, "Read the file")

    assert result.done
    assert result.iterations == 1
```

### 6.3 Prompt Regression Tests

Save prompts to snapshot files and diff on changes:

```python
def test_approval_classification_prompt_snapshot():
    prompt = build_tier_classification_prompt(
        tool="write",
        args={"path": "src/main.py"},
        context={"seniority": "mid", "risk_level": "medium"},
    )
    snapshot_path = Path("tests/snapshots/tier_classification.txt")
    if UPDATE_SNAPSHOTS:
        snapshot_path.write_text(prompt)
    assert prompt == snapshot_path.read_text()
```

---

## 7. Quick Reference

| Pattern | When to Use |
|---------|-------------|
| ReAct (plan → tools → feedback) | All multi-turn agent tasks |
| CoT in `thought` field | Every iteration; forces reasoning before action |
| Tool result summarization | Keep iteration feedback under 200 chars per tool |
| Domain keyword detection | Route finance/legal/security tasks to appropriate models |
| Quality fallback | When the primary tier's providers are all down |
| Tier classification prompt | Every tool action before execution |
| Priority forwarding | Every `_call_llm` call in the agent loop |
