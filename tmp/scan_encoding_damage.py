"""Scan 4 owned files for CP1252/UTF-8 mojibake damage. ASCII-only output."""

import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\jmlus\light-speed-holdings")
FILES = [
    "company-registry.yaml",
    "company/agent-registry.json",
    ".opencode/agents/qa-lead.md",
    ".opencode/agents/ai-ethics-board-chair.md",
]
COMPARE_HEAD = {"company-registry.yaml", "company/agent-registry.json"}

# CP1252 artifact markers (as text patterns)
ARTIFACT_PATTERNS = [
    "\u00e2\u20ac",   # â€  (mojibake of E2 80 xx)
    "\\xE2",
    "\x92", "\x93", "\x94", "\x96", "\x97",  # raw control remnant bytes as chars
]


def cp(ch: str) -> str:
    return "U+%04X" % ord(ch)


def scan_file(rel: str) -> Counter:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    counts: Counter = Counter()
    print("=== %s ===" % rel)
    for lineno, line in enumerate(text.splitlines(), 1):
        for ch in line:
            if ord(ch) > 0x7F:
                counts[ch] += 1
        # flag artifact patterns per line (repr only, ASCII)
        for pat in ARTIFACT_PATTERNS:
            if pat in line:
                print("  ARTIFACT line %d pattern=%r" % (lineno, pat.encode("ascii", "backslashreplace")))
    # summary of non-ascii codepoints
    if counts:
        print("  non-ASCII codepoints (char: count):")
        for ch, n in sorted(counts.items(), key=lambda kv: ord(kv[0])):
            print("    %s %s count=%d" % (cp(ch), ascii(ch), n))
    else:
        print("  no non-ASCII chars")
    # line numbers for each non-ascii char occurrence
    for lineno, line in enumerate(text.splitlines(), 1):
        hits = sorted({ch for ch in line if ord(ch) > 0x7F})
        if hits:
            print("  line %d chars: %s" % (lineno, ", ".join("%s(%d)" % (cp(c), line.count(c)) for c in hits)))
    print()
    return counts


def head_text(rel: str) -> str:
    out = subprocess.run(
        ["git", "show", "HEAD:" + rel],
        cwd=str(ROOT), capture_output=True,
    )
    if out.returncode != 0:
        print("  git show failed for %s: %r" % (rel, out.stderr[:200]))
        return ""
    return out.stdout.decode("utf-8", errors="replace")


def diff_vs_head(rel: str, wt: Counter) -> None:
    ht = head_text(rel)
    head_counts: Counter = Counter(ch for ch in ht if ord(ch) > 0x7F)
    worktree_only = wt - head_counts   # chars in worktree not in HEAD (excess)
    head_only = head_counts - wt       # chars lost vs HEAD
    print("--- codepoint multiset diff vs HEAD: %s ---" % rel)
    if worktree_only:
        print("  WORKTREE-ONLY (suspected damage):")
        for ch, n in sorted(worktree_only.items(), key=lambda kv: ord(kv[0])):
            print("    %s %s excess=%d" % (cp(ch), ascii(ch), n))
    else:
        print("  worktree-only: none")
    if head_only:
        print("  HEAD-ONLY (chars lost / legit content removal):")
        for ch, n in sorted(head_only.items(), key=lambda kv: ord(kv[0])):
            print("    %s %s missing=%d" % (cp(ch), ascii(ch), n))
    else:
        print("  head-only: none")
    print()


def main() -> None:
    for rel in FILES:
        wt = scan_file(rel)
        if rel in COMPARE_HEAD:
            diff_vs_head(rel, wt)


if __name__ == "__main__":
    main()
