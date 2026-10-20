# Review

## Intake Review

- Status: approved
- Notes: issue #484 carries the CI failure log and the three-part diagnosis. The one open question - what the threshold should be - was answered by measurement, not by opinion.

## Spec Review

- Status: approved
- Open high-impact clarifications: none
- WHAT/HOW separation: the spec states the outcomes (a gate that catches real regressions and ignores single-sample jitter, a registry read that is not repeated per request, and never a stale registry); the plan carries the implementation and the calibration.

## Plan Review

- Status: approved
- Spec gaps found from planning: two. A single global threshold does not fit endpoints that differ tenfold in cost, so the plan uses per-endpoint budgets. A TTL cache would show a stale org chart after a write from another process, so the plan keys the cache on the file revision instead.

## Code Review

- Status: approved
- Notes: the cache key includes the resolved path, so two workspaces (as in tests) can never share an entry. Callers get their own copies, so a caller that mutates what it receives cannot poison the next request. The perf gate keeps a hard ceiling, so a pathological case is still covered even though the median is the real assertion. The budgets carry their calibration date and method in the comment above them.

## Validation Review

- Status: approved
- Notes: see the Validation section of `summary.md` for the recorded gate outcomes.
