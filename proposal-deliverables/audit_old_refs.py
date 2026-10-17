# -*- coding: utf-8 -*-
"""Audit proposal deliverables for old budget figures and DPA year.

Searches each file's extracted text for forbidden strings (23,960 / 51,403 /
998 / 2,570 / 1,013 / DPA 2017 / Data Protection Act 2017 / bare 2017) and
required strings (45,000 / 1,875 / 2024 / Last updated / 54747). Writes a
report to audit_report.txt. Handles md/txt/py as text, docx via python-docx
(incl. tables), pptx via python-pptx (all shapes+notes).
"""

import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

FORBIDDEN = [
    "23,960",
    "51,403",
    "998",
    "2,570",
    "1,013",
    "DPA (2017)",
    "Data Protection Act (2017)",
    "DPA 2017",
    "Data Protection Act 2017",
]
REQUIRED = ["45,000", "1,875", "2024", "Last updated", "54747"]

TARGETS = [
    r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\villagereach-ussd-consultant-proposal.md",
    r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\VillageReach-USSD-Consultant-Proposal.docx",
    r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\VillageReach-USSD-Consultant-Proposal-Slides.pptx",
    r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\make_ussd_proposal_docx.py",
    r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\make_villagereach_proposal_docx.py",
    r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\make_villagereach_proposal_pptx.py",
    r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\make_proposal_docx.py",
    r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\make_proposal_pptx.py",
    r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\Jack-Mlusu-Solo-Consultant-Proposal.docx",
    r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\Jack-Mlusu-Solo-Consultant-Proposal.txt",
    r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\Jack-Mlusu-Solo-Consultant-Proposal-Slides.pptx",
    r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\Digital-Health-Consultant-Proposal.docx",
    r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\Digital-Health-Consultant-Proposal-Slides.pptx",
]


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def read_docx(path):
    from docx import Document

    doc = Document(path)
    parts = [p.text for p in doc.paragraphs]
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    parts.append(p.text)
    return "\n".join(parts)


def read_pptx(path):
    from pptx import Presentation

    prs = Presentation(path)
    parts = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                parts.append(shape.text_frame.text)
            if shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:
                        parts.append(cell.text)
        if slide.has_notes_slide:
            parts.append(slide.notes_slide.notes_text_frame.text)
    return "\n".join(parts)


def extract(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".md", ".txt", ".py"):
        return read_text(path)
    if ext == ".docx":
        return read_docx(path)
    if ext == ".pptx":
        return read_pptx(path)
    return ""


def scan(text, needles):
    lines = text.split("\n")
    hits = {}
    for idx, line in enumerate(lines, 1):
        for n in needles:
            if n in line:
                hits.setdefault(n, []).append((idx, line.strip()))
    return hits


report = []
for path in TARGETS:
    name = os.path.basename(path)
    if not os.path.exists(path):
        report.append("MISSING  %s" % path)
        continue
    try:
        text = extract(path)
    except Exception as exc:  # noqa: BLE001
        report.append("ERROR    %s : %s" % (path, exc))
        continue
    forb = scan(text, FORBIDDEN)
    req = scan(text, REQUIRED)
    lines = [path]
    lines.append("  forbidden:")
    if forb:
        for n in FORBIDDEN:
            if n in forb:
                for ln, txt in forb[n][:6]:
                    lines.append("    L%04d [%s] %s" % (ln, n, txt[:160]))
                if len(forb[n]) > 6:
                    lines.append("    ... +%d more" % (len(forb[n]) - 6))
    else:
        lines.append("    (none)")
    lines.append("  required:")
    for n in REQUIRED:
        cnt = len(req.get(n, []))
        lines.append("    %-15s x%d" % (n, cnt))
    report.append("\n".join(lines))

out = "\n\n".join(report)
with open(
    r"C:\Users\jmlus\light-speed-holdings\proposal-deliverables\audit_report.txt",
    "w",
    encoding="utf-8",
) as fh:
    fh.write(out)
print("audit_report.txt written, %d bytes" % len(out.encode("utf-8")))
