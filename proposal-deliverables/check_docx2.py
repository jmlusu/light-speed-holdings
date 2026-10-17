def extract_text_docx(filepath):
    """Try to extract text from .docx by reading raw and decoding"""
    with open(filepath, "rb") as f:
        raw = f.read()
    # Try utf-8 with errors ignored
    text = raw.decode("utf-8", errors="ignore")
    return text


def extract_text_pptx(filepath):
    """Try to extract text from .pptx by reading raw and decoding"""
    with open(filepath, "rb") as f:
        raw = f.read()
    # Try utf-8 with errors ignored
    text = raw.decode("utf-8", errors="ignore")
    return text


# Check VillageReach USSD docx
vfile = "VillageReach-USSD-Consultant-Proposal.docx"
text = extract_text_docx(vfile)
print(f"VillageReach-USSD-Consultant-Proposal.docx length: {len(text)}")
# Search for key patterns
for s in [
    "1875",
    "2024",
    "Last updated",
    "45000",
    "54747",
    "Malawi",
    "Data Protection",
    "Jack Mlusu",
]:
    found = s in text
    print(f"  '{s}': {'FOUND' if found else 'MISSING'}")

# Also try searching for the dollar sign version
for s in ["$1,875", "$45,000", "USD 45,000"]:
    found = s in text
    print(f"  '{s}': {'FOUND' if found else 'MISSING'}")

print()

# Check Jack-Mlusu docx
jfile = r"C:\Users\jmlus\light-speed-holdings\Jack-Mlusu-Solo-Consulting-Proposal.docx"
text2 = extract_text_docx(jfile)
print(f"Jack-Mlusu-Solo-Consulting-Proposal.docx length: {len(text2)}")
for s in [
    "1875",
    "2024",
    "Last updated",
    "45000",
    "54747",
    "Malawi",
    "Data Protection",
    "Jack Mlusu",
]:
    found = s in text2
    print(f"  '{s}': {'FOUND' if found else 'MISSING'}")

print()

# Check Jack-Mlusu pptx
pfile = r"C:\Users\jmlus\light-speed-holdings\Jack-Mlusu-Solo-Consultant-Proposal-Slides.pptx"
text3 = extract_text_pptx(pfile)
print(f"Jack-Mlusi-Solo-Consultant-Proposal-Slides.pptx length: {len(text3)}")
for s in [
    "1875",
    "2024",
    "Last updated",
    "45000",
    "54747",
    "Malawi",
    "Data Protection",
    "Jack Mlusu",
]:
    found = s in text3
    print(f"  '{s}': {'FOUND' if found else 'MISSING'}")

print()
print("=== Also searching for stale values ===")
stale = ["23,960", "51,403", "998", "1,013", "2,570"]
for s in stale:
    for fname, text in [("VillageReach docx", text), ("Jack docx", text2), ("Jack pptx", text3)]:  # noqa: B020
        found = s in text
        if found:
            print(f"  STALE '{s}' FOUND in {fname}")
