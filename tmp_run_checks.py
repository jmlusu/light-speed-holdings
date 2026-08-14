from ai_company.doctor.checks import run_all_checks

results = run_all_checks()
for r in results:
    status = "PASS" if r.passed else "FAIL"
    print(f"{r.name}: {status} - {r.message}")
