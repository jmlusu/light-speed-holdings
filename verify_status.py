"""Final verification status of all token consumption audit changes."""

import sys

sys.path.insert(0, r"C:\Users\jmlus\light-speed-holdings/src")


def check_change_1():
    """Optimized prompts default for specialists."""
    with open("src/ai_company/executor/agent_loop.py") as f:
        c = f.read()
    idx = c.index("use_optimized = (")
    cond = c[idx : idx + c[idx:].index(")") + 1]
    has_config = "self.config.use_optimized_prompts" in cond
    return "PASS" if not has_config else "FAIL", "config removed from condition"


def check_change_2():
    """max_iterations reduction."""
    with open("src/ai_company/executor/agent_loop.py") as f:
        c = f.read()
    has_class_5 = "max_iterations: int = 5" in c
    has_env_5 = False
    for line in c.split("\n"):
        if "AI_COMPANY_MAX_ITERS" in line and "5" in line:
            has_env_5 = True
    return (
        "PASS" if has_class_5 else "FAIL",
        f"class_default_5={has_class_5}, env_default_5={has_env_5}",
    )


def check_change_3():
    """min_similarity + task_type in recall_context."""
    with open("src/ai_company/memory/integration.py") as f:
        c = f.read()
    has_min_sim = "min_similarity: float = 0.0" in c
    has_task_type = 'task_type: str = "general"' in c
    return "PASS" if has_min_sim and has_task_type else "FAIL", ""


def check_change_4():
    """max_tokens_per_tool_summary 500->250."""
    with open("src/ai_company/executor/agent_loop.py") as f:
        c = f.read()
    has_250 = "max_tokens_per_tool_summary: int = 250" in c
    return "PASS" if has_250 else "FAIL", ""


def check_change_5():
    """Empty result prevention."""
    with open("src/ai_company/executor/agent_loop.py") as f:
        c = f.read()
    has_filter = "Filter out empty/meaningless tool results" in c
    return "PASS" if has_filter else "FAIL", ""


def check_change_6():
    """Task-type detection + recall call in loop.py."""
    with open("src/ai_company/executor/loop.py") as f:
        c = f.read()
    has_task_detect = "task_type = debug" in c or 'task_type = "debug"' in c
    has_recall_call = "recalled_memories = recall_context" in c
    return "PASS" if has_task_detect and has_recall_call else "FAIL", ""


if __name__ == "__main":
    results = []

    # Change 1
    status, detail = check_change_1()
    results.append(f"1. Optimized prompts default: {status} {detail}")

    # Change 2
    status, detail = check_change_2()
    results.append(f"2. max_iterations reduction: {status} {detail}")

    # Change 3
    status, detail = check_change_3()
    results.append(f"3. recall_context min_sim+task_type: {status} {detail}")

    # Change 4
    status, detail = check_change_4()
    results.append(f"4. max_tokens_per_tool_summary: {status} {detail}")

    # Change 5
    status, detail = check_change_5()
    results.append(f"5. Empty result prevention: {status} {detail}")

    # Change 6
    status, detail = check_change_6()
    results.append(f"6. Task-type detect + recall: {status} {detail}")

    print("=" * 70)
    print("FINAL VERIFICATION STATUS")
    print("=" * 70)
    print()
    for r in results:
        print(r)
    print()

    all_pass = all(r.startswith("PASS") for r in results)
    if all_pass:
        print("✅ ALL CHANGES VERIFIED COMPLETE")
    else:
        print("⚠️  SOME CHANGES HAVE ISSUES")

    print("=" * 70)

    # Cleanup
    import os

    os.remove(__file__)
