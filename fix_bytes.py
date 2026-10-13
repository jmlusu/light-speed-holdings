#!/usr/bin/env python3
"""Fix Euro sign bytes in pipeline.py"""

with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "rb") as f:
    content = f.read()

# The Euro sign in UTF-8 is bytes 226 128 162 (U+20AC)
# Replace all occurrences with a regular hyphen 0x2d
count = content.replace(b'\xe2\x80\xa2', b'-').count(b'-')  # just check

# Actually replace the Euro sign bytes with hyphen
fixed = content.replace(b'\xe2\x80\xa2', b'-')  # This is actually the bullet character, not Euro
# Let me check what byte sequence we have
print(f"First occurrence of 0xe2 0x80 0xa2 position: {content.find(b'\\xe2\\x80\\xa2')}")

# Replace all occurrences of the 3-byte Euro sequence with a single hyphen
fixed = content.replace(b'\xe2\x80\xa2', b'-')  # This is actually the bullet • (U+2022)
# The actual bytes we saw were 226 128 162 = 0xE2 0x80 0xA2 = UTF-8 for €
fixed = content.replace(b'\xe2\x80\xa2', b'-')  # Wait, that's wrong

# Let me just directly replace the exact bytes we found
# 226 128 162 = bytes [0xE2, 0x80, 0xA2]
euro_bytes = b'\xe2\x80\xa2'  # Actually this is the bullet •
# The actual bytes from the output were: 226 (U+E2), 128 (U+80), 162 (U+A2)
# In hex that's E2 80 A2

# Let me just check what the actual byte sequence is
test_bytes = b'\xe2\x80\xa2'
print(f"Testing byte sequence: {test_bytes.hex()}")

# From the output, the bytes at pos 122-124 were: 226 128 162
# In decimal: 226 = 0xE2, 128 = 0x80, 162 = 0xA2
# So the byte sequence is b'\xe2\x80\xa2'

# Replace all occurrences of this 3-byte sequence with a single hyphen
fixed = content.replace(b'\xe2\x80\xa2', b'-')
# Also replace any other problematic sequences
# From the output, there were multiple occurrences at positions 122-124, 203-205, etc.
# These seem to be evenly spaced every ~77 bytes, which makes sense for text content

# Write the fixed content
with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "wb") as f:
    f.write(fixed)

print(f"Fixed {content.count(b'\xe2\x80\xa2')} occurrences of Euro sign bytes")
print(f"Now has {fixed.count(b'\xe2\x80\xa2')} remaining occurrences")