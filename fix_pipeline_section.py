#!/usr/bin/env python3
"""Fix the Key Decisions Required section in pipeline.py"""

with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find and replace the problematic section
old_text = """("Key Decisions Required", ["Decision 1: Authorize first client pilots 3 Offer A, 1 Offer B, 1 Offer C", "  - Context: Pilots are gated on ratified G1-G4 governance + signed MSA/DPA", "  - Options: Proceed now (cash-flow + referenceable) vs wait for full SOC 2", "  - Recommendation: Proceed with Offer A pilots now; Offer B/C after Sep 5 review", "  - Deadline: Sep 1, 2026", "Decision 2: Ratify SaaS pricing band $49-$299/mo for Offer E (AI Company Builder)", "  - Context: Fee-based pricing in catalog; needs CFO + CEO sign-off to publish", "  - Options: $49-$299 band vs $99-$499 premium", "  - Recommendation: Approve $49-$299 to maximize developer-led adoption", "  - Deadline: Sep 1, 2026", "Decision 3: Confirm Y1 revenue target ($120K ARR) for investor materials", "  - Context: DIR-CEO-2026-001 Section 6.2 requires CFO sign-off on revenue projections", "  - Options: $120K target vs conservative ($60K) vs stretch ($200K)", "  - Recommendation: $120K ARR ($10K/mo) - consistent with finance KPI", "  - Deadline: Before next fundraise pitch"])"""

new_text = '''("Key Decisions Required", ["Decision 1: Authorize first client pilots (3× Offer A, 1× Offer B, 1× Offer C)", "  • Context: Pilots are gated on ratified G1–G4 governance + signed MSA/DPA", "  • Options: Proceed now (cash-flow + referenceable) vs wait for full SOC 2", "  • Recommendation: Proceed with Offer A pilots now; Offer B/C after Sep 5 review", "  • Deadline: Sep 1, 2026", "Decision 2: Ratify SaaS pricing band $49–$299/mo for Offer E (AI Company Builder)", "  • Context: Fee-based pricing in catalog; needs CFO + CEO sign-off to publish", "  • Options: $49–$299 band vs $99–$499 premium", "  • Recommendation: Approve $49–$299 to maximize developer-led adoption", "  • Deadline: Sep 1, 2026", "Decision 3: Confirm Y1 revenue target ($120K ARR) for investor materials", "  • Context: DIR-CEO-2026-001 Section 6.2 requires CFO sign-off on revenue projections", "  • Options: $120K target vs conservative ($60K) vs stretch ($200K)", "  • Recommendation: $120K ARR ($10K/mo) — consistent with finance KPI", "  • Deadline: Before next fundraise pitch"])'''

if old_text in content:
    content = content.replace(old_text, new_text)
    with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Replacement successful")
else:
    print("Old text not found - will try alternative approach")
    # Try a simpler approach - just fix the parenthesis issue
    # Find the line with the issue and fix it
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'Key Decisions Required' in line and i > 600:
            print(f"Found at line {i+1}: {line[:200]}")
            # Check for unmatched parens
            open_parens = line.count('(')
            close_parens = line.count(')')
            print(f"  Open parens: {open_parens}, Close parens: {close_parens}")
            break