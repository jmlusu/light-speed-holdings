#!/usr/bin/env python3
"""SCR-02 Step 2: gather real evidence about scraper/discovery subsystems.

ASCII-only stdout (console is cp1252).
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

JSONL_FILES = ["scrape_jobs.jsonl", "jobs.jsonl", "user_profiles.jsonl"]
ATHENA = os.path.join(ROOT, "company", "athena")


def sec(title):
    print("")
    print("=" * 60)
    print(title)
    print("=" * 60)


def inspect_jsonl(path):
    """Return (n_records, sources, field_union, statuses, issues)."""
    n = 0
    sources = set()
    fields = set()
    statuses = {}
    issues = []
    with open(path, "r", encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                issues.append("blank line at %d" % i)
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                issues.append("bad JSON line %d: %s" % (i, e))
                continue
            n += 1
            if not isinstance(rec, dict):
                issues.append("line %d not an object" % i)
                continue
            fields.update(rec.keys())
            src = rec.get("source")
            if src is not None:
                sources.add(str(src))
            st = rec.get("status")
            if st is not None:
                statuses[str(st)] = statuses.get(str(st), 0) + 1
    return n, sources, fields, statuses, issues


def main():
    sec("1. company/athena/ directory listing")
    if not os.path.isdir(ATHENA):
        print("MISSING: company/athena/")
        return
    for name in sorted(os.listdir(ATHENA)):
        p = os.path.join(ATHENA, name)
        if os.path.isfile(p):
            print("  file: %-28s %6d bytes" % (name, os.path.getsize(p)))
        else:
            print("  dir : %s" % name)

    sec("2. JSONL per-file stats")
    for name in JSONL_FILES:
        p = os.path.join(ATHENA, name)
        print("")
        print("-- %s" % name)
        if not os.path.isfile(p):
            print("   MISSING")
            continue
        if os.path.getsize(p) == 0:
            print("   EMPTY FILE (0 bytes)")
            continue
        n, sources, fields, statuses, issues = inspect_jsonl(p)
        print("   records      : %d" % n)
        print("   sources      : %s" % (sorted(sources) if sources else "NONE (no 'source' field)"))
        print("   fields (%d)  : %s" % (len(fields), sorted(fields)))
        if statuses:
            print("   statuses     : %s" % statuses)
        for iss in issues:
            print("   ISSUE        : %s" % iss)

    sec("3. field-by-field null/missing check (data quality)")
    for name in JSONL_FILES:
        p = os.path.join(ATHENA, name)
        if not os.path.isfile(p) or os.path.getsize(p) == 0:
            continue
        per_field_missing = {}
        n = 0
        all_keys = set()
        recs = []
        with open(p, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(rec, dict):
                    recs.append(rec)
                    all_keys.update(rec.keys())
                    n += 1
        for k in sorted(all_keys):
            miss = sum(1 for r in recs if r.get(k) in (None, "", [], {}))
            per_field_missing[k] = "%d/%d empty" % (miss, n)
        print("")
        print("-- %s (n=%d)" % (name, n))
        for k, v in per_field_missing.items():
            print("   %-24s %s" % (k, v))

    sec("4. TLS / privacy marker scan in athena files")
    markers = ["tls", "ssl", "https", "privacy", "consent", "robots", "rate_limit",
               "user_agent", "headers", "certificate"]
    hits = False
    for name in sorted(os.listdir(ATHENA)):
        p = os.path.join(ATHENA, name)
        if not os.path.isfile(p):
            continue
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read().lower()
        except OSError:
            continue
        found = [m for m in markers if m in text]
        if found:
            hits = True
            print("  %s -> markers: %s" % (name, found))
    if not hits:
        print("  NO TLS/privacy/robots/rate-limit markers found in any company/athena/ file")

    sec("5. scraper script dirs")
    for rel in [".agents/skills/junta-leiloeiro/scripts/scraper",
                "company/junta-leiloeiro",
                ".agents/skills/junta-leiloeiro"]:
        p = os.path.join(ROOT, rel)
        if os.path.isdir(p):
            names = []
            for base, _dirs, files in os.walk(p):
                for f in files:
                    names.append(os.path.relpath(os.path.join(base, f), p))
            print("  EXISTS: %s (%d files)" % (rel, len(names)))
            for nm in sorted(names)[:30]:
                print("     - %s" % nm)
        else:
            print("  MISSING: %s" % rel)

    sec("6. search for canonical job-board/source inventory")
    # grep-like scan of candidate files
    candidates = ["company-registry.yaml", "company/agent-registry.json",
                  "athena/config.yaml", "company/athena/config.yaml",
                  "company/athena/README.md", "config/athena.yaml"]
    for rel in candidates:
        p = os.path.join(ROOT, rel)
        print("  %s: %s" % (rel, "EXISTS" if os.path.isfile(p) else "absent"))

    # any yaml/json/md mentioning job boards or 'scrape' config anywhere in company/ and docs/
    board_pat = re.compile(r"(job.?board|scrap|crawler|crawl)", re.I)
    print("")
    print("  Files under company/ or config/ mentioning job-board/scrape/crawl:")
    found_any = False
    for top in ["company", "config", "docs", ".agents/skills"]:
        base = os.path.join(ROOT, top)
        if not os.path.isdir(base):
            continue
        for b, _d, fs in os.walk(base):
            for f in fs:
                if not f.endswith((".yaml", ".yml", ".json", ".md", ".toml")):
                    continue
                p = os.path.join(b, f)
                rel = os.path.relpath(p, ROOT)
                if "wayfinder" in rel or "superpowers" in rel:
                    continue
                try:
                    with open(p, "r", encoding="utf-8", errors="replace") as fh:
                        txt = fh.read()
                except OSError:
                    continue
                if board_pat.search(txt):
                    found_any = True
                    print("     %s" % rel)
    if not found_any:
        print("     NONE")

    sec("7. athena configs (yaml/json cfg files anywhere named athena*)")
    found_athena_cfg = False
    for b, _d, fs in os.walk(ROOT):
        if ".git" in b or "node_modules" in b or ".venv" in b:
            continue
        for f in fs:
            if f.lower().startswith("athena") and f.lower().endswith((".yaml", ".yml", ".json", ".toml", ".ini")):
                found_athena_cfg = True
                print("  %s" % os.path.relpath(os.path.join(b, f), ROOT))
    if not found_athena_cfg:
        print("  NO athena config files found (no canonical source inventory via athena cfg)")

    sec("8. company-registry.yaml: any source/board/scrape keys?")
    cr = os.path.join(ROOT, "company-registry.yaml")
    if os.path.isfile(cr):
        with open(cr, "r", encoding="utf-8", errors="replace") as fh:
            txt = fh.read()
        print("  size: %d bytes" % len(txt))
        for kw in ["board", "scrape", "crawl", "source", "athena", "tls", "junta"]:
            hits = [ln.strip() for ln in txt.splitlines() if re.search(kw, ln, re.I)]
            print("  keyword '%s': %d line(s)" % (kw, len(hits)))
            for h in hits[:5]:
                print("      %s" % h[:140])
    else:
        print("  company-registry.yaml: MISSING")

    sec("9. raw sample records (first record of each jsonl)")
    for name in JSONL_FILES:
        p = os.path.join(ATHENA, name)
        if not os.path.isfile(p) or os.path.getsize(p) == 0:
            continue
        with open(p, "r", encoding="utf-8") as fh:
            first = fh.readline().strip()
        print("")
        print("-- %s first record:" % name)
        print("   %s" % first[:600])


if __name__ == "__main__":
    main()
