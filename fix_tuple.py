#!/usr/bin/env python3
with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find and fix the Key Decisions Required section
# The issue: tuple ( starts on line 615 but ) is on line 619
# Fix: ensure the tuple closes properly on line 615

# Look for the pattern and fix it
old = """            ("Key Decisions Required", ["Decision 1: Authorize first client pilots 3 Offer A, 1 Offer B, 1 Offer C", "  - Context: Pilots are gated on ratified G1-G4 governance + signed MSA/DPA", "  - Options: Proceed now (cash-flow + referenceable) vs wait for full SOC 2", "  - Recommendation: Proceed with Offer A pilots now; Offer B/C after Sep 5 review", "  - Deadline: Sep 1, 2026", "Decision 2: Ratify SaaS pricing band $49-$299/mo for Offer E (AI Company Builder)", "  - Context: Fee-based pricing in catalog; needs CFO + CEO sign-off to publish", "  - Options: $49-$299 band vs $99-$499 premium", "  - Recommendation: Approve $49-$299 to maximize developer-led adoption", "  - Deadline: Sep 1, 2026", "Decision 3: Confirm Y1 revenue target ($120K ARR) for investor materials", "  - Context: DIR-CEO-2026-001 Section 6.2 requires CFO sign-off on revenue projections", "  - Options: $120K target vs conservative ($60K) vs stretch ($200K)", "  - Recommendation: $120K ARR ($10K/mo) - consistent with finance KPI", "  - Deadline: Before next fundraise pitch"]),"""

# Actually, let me just look at what's there and fix the parenthesis issue
# The line ends with "])," but should end with ")," to close the tuple properly

# Let me just count and fix
if '"Key Decisions Required",' in content:
    # Replace the problematic section
    content = content.replace(
        '            ("Key Decisions Required", ["Decision 1: Authorize first client pilots 3 Offer A, 1 Offer B, 1 Offer C",',
        '            ("Key Decisions Required", ["Decision 1: Authorize first client pilots 3 Offer A, 1 Offer B, 1 Offer C",'
    )
    # Actually this is getting complex. Let me just directly fix the parenthesis
    
    # Find the position and fix
    idx = content.find('("Key Decisions Required",')
    if idx >= 0:
        # Get the section
        section = content[idx:idx+500]
        print("Found section at idx", idx)
        print("Section:", section[:200])
        
        # The issue is the closing. Let me just ensure proper structure
        # By replacing the end portion
        pass

print("Analysis complete")