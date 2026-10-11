"""
GAP-003: 5-Tier Approval Matrix Configuration

Defines the organization's approval tier hierarchy and seniority-based
authorization thresholds. Wired into ToolRunner.check_tool_authorization()
and ToolRunner.check_tier_rules() in src/ai_company/executor/tool_runner.py.

Tier Scale (higher = stricter approval required):
  Tier 0 - AUTO_APPROVE    : No human approval needed; execute immediately.
  Tier 1 - NOTIFY          : Low-risk write; auto-approved but humans notified.
  Tier 2 - SINGLE_APPROVER : Code/test change; one human must approve.
  Tier 3 - TWO_PERSON      : Production/DB change; two humans must approve.
  Tier 4 - CEO_ONLY        : Financial/legal/security; CEO must approve.

Seniority → Max Auto-Approve Tier Mapping:
  junior   : 0  (must go through approval for anything beyond auto)
  mid      : 1  (can auto-approve notify-level)
  senior   : 1  (same as mid, for now)
  lead     : 2  (can auto-approve single-approver)
  executive: 2  (can auto-approve single-approver)
  specialist: 1  (consistent with mid; specialist agents require notify-level auto-approval)

Tool Default Tiers (per tool type):
  read, list, grep, webfetch, web_search, websearch, glob, search, ping, view       -> Tier 0 (AUTO_APPROVE)
  write, execute, bash, edit                                                                            -> Tier 2 (SINGLE_APPROVER)
  delegate, task                                                                                         -> Tier 1 (NOTIFY)

Sensitive path escalation (write/edit/execute/bash):
  - Secret/credentials paths      -> Tier 4 (CEO_ONLY)
  - Production/deploy paths       -> Tier 3 (TWO_PERSON)
  - Source code paths (src/, tests/)  -> Tier 2 (SINGLE_APPROVER)
  - Config/docs paths             -> Tier 1 (NOTIFY)

Privileged Tool Call Decision Matrix:

| Tool              | Default Tier | Seniority | Scenario                              | Tier Result | HITL Required | Authorized |
|-------------------|-------------|-----------|---------------------------------------|-------------|---------------|------------|
| read              | 0           | lead      | reading source file                   | 0           | False         | True       |
| write src/app.py  | 2           | mid       | writing to source                     | 2           | True          | False      |
| write src/app.py  | 2           | lead      | writing to source (lead seniority)    | 1           | False         | True       |
| write config.yaml | 2           | mid       | writing config (low-risk)             | 1           | False         | True       |
| write config/secrets.yaml | 2   | mid       | writing secrets (sensitive path)      | 4           | True          | False      |
| execute "rm -rf /"| 2           | executive | dangerous command (exec seniority)    | 4           | True          | False      |
| bash "ls -la"     | 2           | specialist| basic listing (specialist seniority) | 1           | False         | True       |
| task delegate     | 1           | mid       | delegating task                      | 1           | False         | True       |

Integration with ToolRunner:

```python
from ai_company.executor.tool_runner import ToolRunner

runner = ToolRunner(project_root=".")

# Check authorization for a tool action
tier_info = ToolRunner.check_tool_authorization(
    tool_name="write",
    args={"path": "src/app.py", "content": "def foo(): pass"},
    agent_id="agent-123",
    seniority="lead",  # or "executive", "specialist", "mid", "junior"
    risk_level="medium",
    task_id="task-42",
)

# tier_info keys: tier (int), tier_label (str), needs_hitl (bool),
#                 description (str), authorized (bool)
print(f"Tier: {tier_info['tier']} ({tier_info['tier_label']})")
print(f"HITL required: {tier_info['needs_hitl']}")
print(f"Authorized: {tier_info['authorized']}")

# In run_plan, the tier determines execution path:
# - needs_hitl=True, blocking=True:  -> hitl_gate.request_and_wait_sync()
# - needs_hitl=True, blocking=False: -> raise HITLParked (GAP-004)
# - needs_hitl=False:              -> execute directly
```

Approval Level Constants (for registry/configuration):

```python
# Maps agent approval_level from company-registry.yaml to seniority thresholds
APPROVAL_LEVEL_THRESHOLDS = {
    "exec":    {"seniority": "executive", "max_auto_tier": 2},
    "lead":    {"seniority": "lead",       "max_auto_tier": 2},
    "specialist": {"seniority": "specialist", "max_auto_tier": 1},
}

# Example: Using approval_level from registry to determine HITL requirement
def check_approval_from_registry(tool_name, args, agent_approval_level, seniority, ...):
    """Derive HITL requirement from agent's approval_level + seniority."""
    tier_info = ToolRunner.check_tier_rules(
        tool_name=tool_name,
        args=args,
        agent_id="",
        seniority=seniority,
        risk_level="medium",
        task_id="",
    )
    
    # If agent's approval_level is "specialist", enforce max_auto_tier=1
    if agent_approval_level == "specialist":
        max_auto = 1  # specialist seniority ceiling
        if tier_info["tier"] > max_auto:
            tier_info["needs_hitl"] = True
            tier_info["authorized"] = False
    
    # If agent's approval_level is "exec" or "lead", allow up to tier 2
    elif agent_approval_level in ("exec", "lead"):
        max_auto = 2
        if tier_info["tier"] > max_auto:
            tier_info["needs_hitl"] = True
            tier_info["authorized"] = False
    
    return tier_info
```
"""