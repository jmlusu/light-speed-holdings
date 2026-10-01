#!/usr/bin/env python3
"""SCR-02 Step 6: self-verify map + template + plan markers. ASCII-only stdout."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAP = os.path.join(ROOT, "docs", "wayfinder", "map2-scraper-discovery-gap-analysis.md")
TPL = os.path.join(ROOT, ".agents", "skills", "wayfinder", "map_template.md")
PLAN = os.path.join(ROOT, "docs", "superpowers", "plans",
                    "2026-09-28-wayfinder-map2-scraper-discovery-gap-analysis.md")

MAP_PATTERNS = [
    ("wayfinder:map label", r"wayfinder:map"),
    ("child ticket types", r"wayfinder:(research|prototype|grilling|task)"),
    ("Decisions so far", r"Decisions so far"),
    ("Not yet specified", r"Not yet specified"),
    ("Out of scope", r"Out of scope"),
    ("## Destination heading", r"^## Destination"),
    ("## Notes heading", r"^## Notes"),
    ("## Scraper Sources heading", r"^## Scraper Sources"),
    ("## Data Quality Gaps heading", r"^## Data Quality Gaps"),
    ("## Integration Points heading", r"^## Integration Points"),
]

TEMPLATE_PATTERNS = [
    ("wayfinder:map", r"wayfinder:map"),
    ("Labels:", r"Labels:"),
    ("## Destination", r"^## Destination"),
    ("## Notes", r"^## Notes"),
    ("Decisions so far", r"Decisions so far"),
    ("Not yet specified", r"Not yet specified"),
    ("Out of scope", r"Out of scope"),
    ("Scraper Sources", r"Scraper Sources"),
    ("Data Quality Gaps", r"Data Quality Gaps"),
    ("Integration Points", r"Integration Points"),
]

PLAN_MARKERS = [
    "# [Wayfinder Map 2] Implementation Plan",
    "**Goal:**",
    "**Architecture:**",
    "**Tech Stack:**",
    "**Spec:**",
    "## Global Constraints",
    "## Review Focus",
    "## Gap Analysis: Wayfinder <-> Scraper Systems",
]


def check(path, patterns, title):
    print("")
    print("== %s ==" % title)
    if not os.path.isfile(path):
        print("FAIL  file missing: %s" % os.path.relpath(path, ROOT))
        return False
    text = open(path, encoding="utf-8").read()
    all_ok = True
    for name, pat in patterns:
        flags = re.M
        ok = re.search(pat, text, flags) is not None
        print("%-5s %s" % ("PASS" if ok else "FAIL", name))
        all_ok = all_ok and ok
    return all_ok


def main():
    ok_map = check(MAP, MAP_PATTERNS, "MAP: map2-scraper-discovery-gap-analysis.md")

    # Destination-first: first level-2 heading must be Destination
    text = open(MAP, encoding="utf-8").read()
    first_h2 = re.search(r"^## .+$", text, re.M)
    dest_ok = bool(first_h2) and first_h2.group(0).strip() == "## Destination"
    print("%-5s Destination is the FIRST ## section (found: %s)"
          % ("PASS" if dest_ok else "FAIL",
             first_h2.group(0).strip() if first_h2 else "none"))

    ok_tpl = check(TPL, TEMPLATE_PATTERNS, "TEMPLATE: map_template.md")

    print("")
    print("== PLAN markers (must still exist + new section) ==")
    plan_text = open(PLAN, encoding="utf-8").read()
    plan_ok = True
    for m in PLAN_MARKERS:
        ok = m in plan_text
        print("%-5s %s" % ("PASS" if ok else "FAIL", m))
        plan_ok = plan_ok and ok

    print("")
    print("SUMMARY: map=%s template=%s plan=%s destination_first=%s"
          % ("PASS" if ok_map else "FAIL",
             "PASS" if ok_tpl else "FAIL",
             "PASS" if plan_ok else "FAIL",
             "PASS" if dest_ok else "FAIL"))


if __name__ == "__main__":
    main()
