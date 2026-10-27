"""Normalize campaign copy: enforce U+2800 separators + wording fixes.

ASCII-only matching so the script never has to embed the Unicode bold
mathematical characters used in the copy itself.
"""

from pathlib import Path

SEP = "\u2800"  # BRAILLE PATTERN BLANK - used as invisible whitespace separator
BASE = Path("artifacts/campaigns/2026-10-26-pipeline-test/text")

# --- linkedin-primary: insert U+2800 between sections -----------------------
p = BASE / "linkedin-primary.md"
lines = p.read_text(encoding="utf-8").split("\n")

# Blank-line indices that currently separate major blocks (0-based).
separator_after = {1, 3, 5, 7, 9, 11, 13, 15}

out = []
for i, line in enumerate(lines):
    if i in separator_after:
        # Replace the plain blank line with a U+2800 separator line.
        out.append(SEP)
    else:
        out.append(line)

text = "\n".join(out)

# Wording precision fixes (ASCII substrings only).
text = text.replace(
    "89 AI agents managed by a single human CEO",
    "89 AI agents reporting to one human CEO",
)
text = text.replace("seams of improvement", "integration seams")

p.write_text(text, encoding="utf-8")

# --- enterprise: wording precision ----------------------------------------
p2 = BASE / "variant-enterprise.md"
t2 = p2.read_text(encoding="utf-8")
t2 = t2.replace("seams", "integration seams").replace(
    "integration integration seams", "integration seams"
)
p2.write_text(t2, encoding="utf-8")

# --- verification ---------------------------------------------------------
print("VERIFICATION")
print("-" * 46)
for f in ["linkedin-primary", "variant-policy", "variant-enterprise"]:
    t = (BASE / f"{f}.md").read_text(encoding="utf-8")
    print(
        f"{f:22} chars={len(t):5}  U+2800={t.count(SEP):2}  "
        f"TM={t.count(chr(0x2122))}  U+FFFD={t.count(chr(0xFFFD))}"
    )

lp = (BASE / "linkedin-primary.md").read_text(encoding="utf-8")
print("-" * 46)
print(f"linkedin-primary under 2800 chars: {len(lp) < 2800} ({len(lp)})")
