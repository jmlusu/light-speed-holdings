def extract_text(filepath, encoding="utf-8"):
    try:
        with open(filepath, "rb") as f:
            raw = f.read()
        text = raw.decode(encoding, errors="ignore")
        return text
    except Exception:  # noqa: BLE001
        return None


# Try different encodings for VillageReach docx
vfile = "VillageReach-USSD-Consultant-Proposal.docx"
for enc in ["utf-8", "latin-1", "cp1252", "iso-8859-1", "windows-1252"]:
    text = extract_text(vfile, enc)
    if text:
        print(f"\n=== {enc} ===")
        for s in [
            "1875",
            "2024",
            "Last updated",
            "45000",
            "54747",
            "Malawi",
            "Data Protection",
            "Jack Mlusu",
            "$45,000",
            "$1,875",
            "USD",
        ]:
            found = s in text
            print(f"  '{s}': {'FOUND' if found else 'MISSING'}")

# Try the Jack-Mlusu docx
print("\n\n=== Jack-Mlusu-Solo-Consulting-Proposal.docx ===")
jfile = r"C:\Users\jmlus\light-speed-holdings\Jack-Mlusu-Solo-Consulting-Proposal.docx"
for enc in ["utf-8", "latin-1", "cp1252", "iso-8859-1", "windows-1252"]:
    text = extract_text(jfile, enc)
    if text:
        print(f"\n--- {enc} (len={len(text)}) ---")
        for s in [
            "1875",
            "2024",
            "Last updated",
            "45000",
            "54747",
            "Malawi",
            "Data Protection",
            "Jack Mlusu",
            "$45,000",
            "$1,875",
            "USD",
        ]:
            found = s in text
            print(f"  '{s}': {'FOUND' if found else 'MISSING'}")

# Try the Jack-Mlusu pptx
print("\n\n=== Jack-Mlusu-Solo-Consultant-Proposal-Slides.pptx ===")
pfile = r"C:\Users\jmlus\light-speed-holdings\Jack-Mlusi-Solo-Consultant-Proposal-Slides.pptx"
for enc in ["utf-8", "latin-1", "cp1252", "iso-8859-1", "windows-1252"]:
    text = extract_text(pfile, enc)
    if text:
        print(f"\n--- {enc} (len={len(text)}) ---")
        for s in [
            "1875",
            "2024",
            "Last updated",
            "45000",
            "54747",
            "Malawi",
            "Data Protection",
            "Jack Mlusu",
            "$45,000",
            "$1,875",
            "USD",
        ]:
            found = s in text
            print(f"  '{s}': {'FOUND' if found else 'MISSING'}")
