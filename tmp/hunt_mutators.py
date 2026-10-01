"""Grep tests for entrypoints that can write real repo files (report-only helper)."""
import pathlib
import re

root = pathlib.Path(r"C:\Users\jmlus\light-speed-holdings\tests")
pats = re.compile(
    r"AgentGenerator|generate_all|doctor|\"init\"|'init'|hr\.onboarding|"
    r"services\.onboarding|reports-to|write_file\(|repo_write",
    re.I,
)
out_lines = []
for p in sorted(root.rglob("*.py")):
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        continue
    for i, line in enumerate(lines, 1):
        if pats.search(line):
            clean = line.strip()[:150].encode("ascii", "replace").decode("ascii")
            out_lines.append(f"{p.relative_to(root)}:{i}:{clean}")
pathlib.Path(r"C:\Users\jmlus\light-speed-holdings\tmp\mutators.txt").write_text(
    "\n".join(out_lines) + "\n", encoding="utf-8"
)
print(f"wrote {len(out_lines)} hits to tmp\\mutators.txt")
