Commit the completed changes.

Before committing:
- Review the changes for unintended modifications.
- Confirm the changes are limited to the requested task.
- Run the appropriate local validation/tests where practical.

Then:
1. Create a clear, descriptive commit.
2. Push the commit if that is part of the repository workflow.
3. Monitor the resulting CI job(s) until they reach a definitive successful or failed state.
4. If CI fails, inspect the failure, identify the root cause, fix it, and commit the fix.
5. Re-run and monitor CI.
6. Repeat the debug → fix → commit → CI verification cycle until CI succeeds or a genuine blocker prevents completion.
7. Do not declare success while required CI checks are still failing or unresolved.

Do not make unrelated changes merely to achieve a green CI result. Keep every fix directly related to the task or CI failure.

Final report:
- Commit hash
- What was committed
- CI status
- Tests/checks run
- Any fixes made after the initial commit
- Remaining blockers, if any
- Recommended next step