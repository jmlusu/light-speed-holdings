"""
Doctor report generation.
"""

from typing import List
from datetime import datetime
from pathlib import Path
import yaml

from ai_company.doctor.checks import CheckResult


def generate_report(checks: List[CheckResult]) -> str:
    passed = sum(1 for c in checks if c.passed)
    failed = sum(1 for c in checks if not c.passed)
    total = len(checks)

    report = []
    report.append("=" * 50)
    report.append("AI Company Builder - Health Report")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 50)
    report.append("")

    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        report.append(f"[{status}] {check.name}")
        report.append(f"  {check.message}")
        report.append("")

    report.append("-" * 50)
    report.append(f"Results: {passed}/{total} checks passed")

    if failed == 0:
        report.append("Status: HEALTHY")
    else:
        report.append(f"Status: {failed} issue(s) found")

    report.append("=" * 50)

    return "\n".join(report)


def save_report(checks: List[CheckResult], output_dir: str = ".opencode"):
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    report_text = generate_report(checks)
    report_file = output_path / "health_report.txt"
    report_file.write_text(report_text, encoding="utf-8")

    return report_file
