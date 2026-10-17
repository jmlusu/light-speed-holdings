def check_file(filepath, searchterms):
    with open(filepath, "rb") as f:
        raw = f.read()
    results = {}
    for s in searchterms:
        idx = raw.find(s.encode() if isinstance(s, str) else s)
        results[s] = idx >= 0
    return results


# Check VillageReach USSD docx
vfile = "VillageReach-USSD-Consultant-Proposal.docx"
terms = [
    "1,875",
    "2024",
    "Last updated",
    "$45,000",
    "54747",
    "Malawi",
    "Data Protection",
    "Jack Mlusu",
]
results = check_file(vfile, terms)
print("VillageReach-USSD-Consultant-Proposal.docx:")
for k, v in results.items():
    print(f"  {k}: {'FOUND' if v else 'MISSING'}")

# Check Jack-Mlusu docx
jfile = r"C:\Users\jmlus\light-speed-holdings\Jack-Mlusu-Solo-Consulting-Proposal.docx"
results2 = check_file(jfile, terms)
print("\nJack-Mlusu-Solo-Consulting-Proposal.docx:")
for k, v in results2.items():
    print(f"  {k}: {'FOUND' if v else 'MISSING'}")

# Check Jack-Mlusi pptx
pfile = r"C:\Users\jmlus\light-speed-holdings\Jack-Mlusu-Solo-Consultant-Proposal-Slides.pptx"
results3 = check_file(pfile, terms)
print("\nJack-Mlusi-Solo-Consultant-Proposal-Slides.pptx:")
for k, v in results3.items():
    print(f"  {k}: {'FOUND' if v else 'MISSING'}")
