#!/usr/bin/env python3
"""Rewrite pipeline.py with clean structure - fix all parenthesis issues"""

with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "r", encoding="utf-8") as f:
    content = f.read()

# The file has inconsistent parenthesis placement across slides.
# Each slide appears to have this pattern:
#   ("Slide Title", [bullet items...]),   <- tuple with title and bullets
#   "Description text",                    <- description
#   {}),                                   <- empty dict + ) that closes previous tuple + , separates slides
# 
# The problem: the ")" in "{}), " closes the tuple from 2 lines above,
# which is invalid Python. Need to restructure so each tuple closes on its own line.

# Strategy: Replace the broken pattern with a clean structure.
# New pattern:
#   ("Slide Title", [bullet items...]),   <- tuple, ) on same line
#   "Description text",                    <- description  
#   {} ,                                   <- empty dict, comma separates slides

# Find and replace the problematic pattern
# Pattern: "{}),\n" appears multiple times - these are the "})," lines

# Let me just replace the entire file content with a clean version
# Based on the existing structure but with fixed parenthesis

# First, let me identify all the slide definitions and restructure them

# The file seems to have sections defined as:
# - Slide titles and bullet points as tuples
# - Description strings
# - Empty dicts

# Let me just take the approach of ensuring every tuple closes on the same line.
# I'll scan for ("pattern and ensure ) is on the same line.

# Actually, the simplest fix: just remove the ")" from the "{}),\" lines
# and add them to the tuple lines instead.

# But this is getting complex. Let me take the nuclear option: rewrite the
# slide definitions section with clean structure.

# Let me find where the slide definitions start and end
# Looking at the file, it seems like the slide definitions are in the
# generate_presentation_phases function or similar.

# For now, let me just try to import the module and see what specific
# errors remain, then fix those.

# Actually, let me just try a simpler approach: replace the "{}),\n" patterns
# with just "},\n" (remove the closing paren) and see if that helps.

# But wait - the ")" might be needed somewhere. Let me check what the parse error was.

# The parse error was: "closing parenthesis ')' does not match opening parenthesis '[' on line 619"
# This suggests line 619 has ")" but the matching "[" is elsewhere.

# Let me just try removing the ")" from lines that have "{})," and see if the module imports.

# Find all occurrences of "{})," and replace with "{}", (removing the closing paren)
import re
# Count occurrences
count = len(re.findall(r'\{},\s*\)', content))
print(f"Found {count} occurrences of '{{}}),' pattern")

# Let me just try a different approach - write the whole file new
print("Taking alternative approach - will fix specific known issues")

# For now, let me just try to import and see what errors we get