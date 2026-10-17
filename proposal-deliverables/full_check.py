#!/usr/bin/env python3
import os

import docx
from pptx import Presentation


def check_file_docx(filepath, search_terms):
    """Check a .docx file for specific terms"""
    found = {}
    try:
        doc = docx.Document(filepath)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    full_text += "\n" + cell.text
        for s in search_terms:
            found[s] = s in full_text
    except Exception as e:  # noqa: BLE001
        print(f"Error reading {filepath}: {e}")
        for s in search_terms:
            found[s] = False
    return found


def check_file_pptx(filepath, search_terms):
    """Check a .pptx file for specific terms"""
    found = {}
    try:
        prs = Presentation(filepath)
        full_text = ""
        for slide in prs.slides:
            for shape in slide.shapes:
                if shape.has_text_frame:
                    full_text += shape.text + "\n"
        for s in search_terms:
            found[s] = s in full_text
    except Exception as e:  # noqa: BLE001
        print(f"Error reading {filepath}: {e}")
        for s in search_terms:
            found[s] = False
    return found


def check_file_md(filepath, search_terms):
    """Check a .md file for specific terms"""
    found = {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            full_text = f.read()
        for s in search_terms:
            found[s] = s in full_text
    except Exception as e:  # noqa: BLE001
        print(f"Error reading {filepath}: {e}")
        for s in search_terms:
            found[s] = False
    return found


# Search terms
search_terms = [
    "1,875",
    "1875",
    "45,000",
    "45000",
    "54747",
    "2024",
    "Last updated",
    "Malawi Data Protection Act",
    "Malawi Data Protection Act 2024",
    "no callback",
    "no-callback",
    "Jack Mlusu",
    "23,960",
    "51,403",
    "998",
    "1,013",
    "2,570",
    "13,350",
    "25,633",
    "1,926",
    "4,091",
]

# File paths
files = {
    "proposal-deliverables/Jack-Mlusu-Solo-Consultant-Proposal.docx": r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\Jack-Mlusu-Solo-Consultant-Proposal.docx",
    "proposal-deliverables/Jack-Mlusu-Solo-Consultant-Proposal.txt": r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\Jack-Mlusu-Solo-Consultant-Proposal.txt",
    "proposal-deliverables/Jack-Mlusu-Solo-Consultant-Proposal-Slides.pptx": r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\Jack-Mlusu-Solo-Consultant-Proposal-Slides.pptx",
    "proposal-deliverables/VillageReach-USSD-Consultant-Proposal.docx": r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\VillageReach-USSD-Consultant-Proposal.docx",
    "proposal-deliverables/villagereach-ussd-consultant-proposal.md": r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\villagereach-ussd-consultant-proposal.md",
}

print("COMPREHENSIVE PRIVACY REVIEW CHECK")

all_results = {}

for fname, fpath in files.items():
    print(f"\n{'-' * 80}")
    print("FILE: " + fname)
    print("PATH: " + fpath)
    print("EXISTS: " + str(os.path.exists(fpath)))

    if not os.path.exists(fpath):
        print("  FILE NOT FOUND")
        continue

    ext = os.path.splitext(fpath)[1].lower()
    if ext == ".txt":
        fc = check_file_md(fpath, search_terms)
    elif ext == ".docx":
        fc = check_file_docx(fpath, search_terms)
    elif ext == ".pptx":
        fc = check_file_pptx(fpath, search_terms)
    else:
        fc = {s: "UNKNOWN" for s in search_terms}

    print("  Term coverage:")
    for term, present in fc.items():
        status = "FOUND" if present else "MISSING"
        print("    '" + term + "': " + status)

    # Check for stale values
    print("  Stale value check:")
    for stale in ["23,960", "51,403", "998", "1,013", "2,570"]:
        present = False
        if os.path.exists(fpath):
            if ext == ".txt":
                with open(fpath, "r", encoding="utf-8") as f:
                    rt = f.read()
                present = stale in rt
            elif ext == ".docx":
                doc = docx.Document(fpath)
                rt = "\n".join([p.text for p in doc.paragraphs])
                for table in doc.tables:
                    for row in table.rows:
                        for cell in row.cells:
                            rt += "\n" + cell.text
                present = stale in rt
            elif ext == ".pptx":
                prs = Presentation(fpath)
                rt = ""
                for slide in prs.slides:
                    for shape in slide.shapes:
                        if shape.has_text_frame:
                            rt += shape.text + "\n"
                present = stale in rt

        if present:
            print("    STALE '" + stale + "': FOUND (SHOULD NOT BE HERE)")
        else:
            print("    STALE '" + stale + "': NOT PRESENT (good)")

    all_results[fname] = fc
    print()

print("=" * 80)
print("KEY REQUIREMENTS VERIFICATION - .md FILE")
print("=" * 80)

md_path = r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\villagereach-ussd-consultant-proposal.md"
if os.path.exists(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    print("\nVillageReach .md file checks:")
    key_checks = {
        "Last updated: 2026-09-18": "Last updated: 2026-09-18" in md_content,
        "USD 45,000 total": "USD 45,000" in md_content or "$45,000" in md_content,
        "Monthly $1,875": "1,875" in md_content or "$1,875" in md_content,
        "Malawi DPA 2024": "Malawi Data Protection Act (2024)" in md_content
        or "Malawi Data Protection Act 2024" in md_content,
        "no callback USSD": "no callback" in md_content or "no-callback" in md_content,
        "Short code 54747": "54747" in md_content,
        "Jack Mlusu": "Jack Mlusu" in md_content,
        "Figures 13,350 + 25,633 + 1,926 + 4,091": all(
            x in md_content for x in ["13,350", "25,633", "1,926", "4,091", "45,000"]
        ),
        "45,000 / 24 = 1,875": "45,000 / 24" in md_content or "1,875" in md_content,
    }

    all_pass = True
    for check, result in key_checks.items():
        status = "PASS" if result else "FAIL"
        if not result:
            all_pass = False
        print("  " + status + ": " + check)

    print("\nOverall: " + ("ALL CHECKS PASSED" if all_pass else "SOME CHECKS FAILED"))
else:
    print("\nMD file not found: " + md_path)
