"""Snapshot content hashes of tracked-mutation-candidate files (before/after diff)."""
import hashlib
import pathlib
import sys

root = pathlib.Path(r"C:\Users\jmlus\light-speed-holdings")
paths = sorted((root / ".opencode" / "agents").glob("*.md"))
paths += [
    root / "company-registry.yaml",
    root / "company" / "agent-registry.json",
    root / "tests" / "memory" / "dual_path_hash_report.txt",
    root / "docs" / "AGENT-REGISTRY-TABLE.md",
]
lines = []
for p in paths:
    if p.exists():
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        lines.append(f"{p.relative_to(root)} {digest}")
    else:
        lines.append(f"{p.relative_to(root)} MISSING")
out = pathlib.Path(sys.argv[1])
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(lines)} entries)")
