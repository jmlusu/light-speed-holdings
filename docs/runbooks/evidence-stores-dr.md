# Disaster Recovery Runbook: Evidence Stores

**Version**: 1.0
**Last Updated**: 2026-10-01
**Owner**: Ops Lead / Platform Reliability Engineer
**Review Cadence**: Quarterly (aligned with §7.3 rotation)

---

## Overview

This runbook covers disaster recovery for the three evidence-separation stores mandated by AGENTS.md §9.3:

| Store | Path | Purpose | Retention |
|-------|------|---------|-----------|
| Escalation Events | `orchestrator/escalation_events.jsonl` | Escalation lifecycle events | 30 days |
| Dead-Letter Queue | `orchestrator/dead_letter.jsonl` | Task failures, retries, resolutions | 90 days |
| Audit Export | `reports/evidence/audit-*.jsonl` | Daily SQLite export | 90 days |

**Golden Rule**: Evidence stores are **append-only**. Never modify in place. Recovery = restore from source, not edit in place.

---

## Recovery Scenarios

### Scenario 1: Single Store Corrupted (Most Likely)

**Symptoms**: JSONL parse errors, missing lines, or `integrity check` reporting malformed records.

**Recovery Steps**:

```bash
# 1. Identify affected store
ls -la orchestrator/escalation_events.jsonl
ls -la orchestrator/dead_letter.jsonl
ls -la reports/evidence/audit-*.jsonl

# 2. Verify with integrity checker
python -m ai_company.audit.integrity check orchestrator/escalation_events.jsonl

# 3. Restore from Git (preferred — Git is source of truth)
git checkout HEAD -- orchestrator/escalation_events.jsonl

# 4. If Git also corrupted, restore from GitHub Artifact
# Go to GitHub Actions → audit-export workflow → Download artifact
# Unzip to reports/evidence/

# 5. Verify integrity after restore
python -m ai_company.audit.integrity check orchestrator/escalation_events.jsonl
```

**Verification**: The three evidence stores (escalation events, dead-letter queue, audit
export) are append-only but carry **no** `__seq`/`__prev_hash` fields, so they are not
hash chained. Verify them with `check`, which confirms every line is a well-formed JSON
object and prints `{"ok": true, "records": N, "errors": []}` followed by `Integrity OK`
and exit code 0. Use `verify` only for the AuditWriter trail under `.opencode/audit/`,
which is the only store that is tamper-evident; it prints `{"ok": true, "events": N, ...}`.
Both commands exit 1 and print `INTEGRITY CHECK FAILED` when anything is wrong.

---

### Scenario 2: All Evidence Stores Lost (Git + Artifacts Corrupted)

**Symptoms**: Git repo corrupted, GitHub artifacts expired/deleted, local files missing.

**Recovery Steps**:

```bash
# 1. Re-clone from upstream (if fork) or fresh clone
git clone https://github.com/jmlusu/light-speed-holdings.git recovery-repo
cd recovery-repo

# 2. Check if any evidence files exist in Git history
git log --oneline --all -- orchestrator/escalation_events.jsonl | head -5

# 3. If Git has history, restore from latest clean commit
git checkout <last-known-good-commit> -- orchestrator/escalation_events.jsonl

# 4. If no Git history, rebuild from source systems:
#    a) Escalation events → re-run from orchestrator/escalation.yaml config
#    b) Dead-letter → re-scan inbox for stale tasks
#    c) Audit export → re-run export from audit/audit.db

# 4a. Rebuild escalation events from config
python -c "
from ai_company.orchestrator.escalation import EscalationManager
em = EscalationManager()
em._save_events()  # Writes current in-memory events to JSONL
"

# 4b. Rebuild dead-letter from inbox
python -c "
from ai_company.executor.dead_letter import detect_stale_tasks, DeadLetterQueue
from ai_company.orchestrator.message_bus import MessageBus
bus = MessageBus()
dlq = DeadLetterQueue()
detect_stale_tasks(bus, dlq)  # Re-detects and writes to JSONL
"

# 4c. Rebuild audit export
python -m ai_company.audit.export --date $(date -u +%F)

# 6. Verify all stores
# The AuditWriter trail is the only hash-chained store.
python -m ai_company.audit.integrity verify .opencode/audit/audit.jsonl
python -m ai_company.audit.integrity check orchestrator/escalation_events.jsonl
python -m ai_company.audit.integrity check orchestrator/dead_letter.jsonl
python -m ai_company.audit.integrity check reports/evidence/audit-$(date -u +%F).jsonl
```

---

### Scenario 3: Rotation Failed (Store Stuck/Truncated)

**Symptoms**: Store size exceeds 500MB, rotation cron failed, file truncated mid-write.

```bash
# 1. Check rotation cron status
gh run list --workflow=audit-export.yml --limit=5

# 2. Check for partial rotation files
ls -la orchestrator/*.rotated-*.jsonl
ls -la reports/evidence/*.rotated-*.jsonl

# 2. If rotation interrupted, check for temp files
ls -la /tmp/.audit-tmp-* /tmp/.escalation-tmp-* /tmp/.dlq-tmp-*

# 3. Recover: If temp file exists, complete the rotation
# Example for escalation_events:
mv orchestrator/escalation_events.jsonl.tmp orchestrator/escalation_events.jsonl

# 4. If main file truncated, restore from last rotation
ls -la orchestrator/escalation_events.rotated-*.jsonl | tail -1
cp orchestrator/escalation_events.rotated-<latest>.jsonl orchestrator/escalation_events.jsonl

# 5. If no rotation file, rebuild from Git (Scenario 1)
```

---

### Scenario 4: Correlation ID Chain Broken

**Symptoms**: Auditor cannot trace incident across stores; `correlation_id` missing or mismatched.

```bash
# 1. Check correlation_id presence
grep -c correlation_id orchestrator/escalation_events.jsonl
grep -c correlation_id orchestrator/dead_letter.jsonl
grep -c correlation_id reports/evidence/audit-*.jsonl

# 2. If missing, rebuild correlation_id from timestamps
# This is a manual process — cross-reference by timestamp ±1 second
python -c "
import json, uuid
from datetime import datetime

def add_correlation_id(path):
    with open(path) as f:
        lines = f.readlines()
    with open(path + '.fixed', 'w') as f:
        for line in lines:
            data = json.loads(line)
            if 'correlation_id' not in data:
                # Generate deterministic ID from timestamp + task_id
                ts = data.get('timestamp', '')
                task = data.get('task_id', '')
                cid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f'{ts}-{task}'))
                data['correlation_id'] = cid
            f.write(json.dumps(data) + '\n')
    return path + '.fixed'

# Run for each store
"

# 3. Verify correlation chains
python -c "
import json
from collections import defaultdict

def check_chains():
    stores = {
        'escalation': 'orchestrator/escalation_events.jsonl',
        'dead_letter': 'orchestrator/dead_letter.jsonl',
        'audit': 'reports/evidence/audit-*.jsonl'
    }
    for name, path in stores.items():
        if '*' in path:
            import glob
            files = glob.glob(path)
        else:
            files = [path]
        for f in files:
            with open(f) as fp:
                cids = [json.loads(l).get('correlation_id') for l in fp if l.strip()]
            print(f'{name}: {len(cids)} events, {len(set(cids))} unique correlation_ids')
check_chains()
"
```

---

### Scenario 5: Git History Rewrite / Force Push (Emergency)

**Symptoms**: Force push removed evidence files from history; artifacts expired.

```bash
# 1. Check GitHub reflog (if accessible via API)
gh api repos/jmlusu/light-speed-holdings/commits --per_page=100

# 2. Check if any branch has the files
git branch -a --contains HEAD

# 3. Check GitHub Actions artifacts (90-day retention)
gh api repos/jmlusu/light-speed-holdings/actions/artifacts --per_page=100

# 4. If all lost, rebuild from source (Scenario 2, step 4)
```

---

## Verification Checklist (Post-Recovery)

After ANY recovery, run this checklist:

- [ ] `python -m ai_company.audit.integrity verify .opencode/audit/audit.jsonl` → OK (hash chain)
- [ ] `python -m ai_company.audit.integrity check orchestrator/escalation_events.jsonl` → OK
- [ ] `python -m ai_company.audit.integrity check orchestrator/dead_letter.jsonl` → OK
- [ ] `python -m ai_company.audit.integrity check reports/evidence/audit-$(date -u +%F).jsonl` → OK
- [ ] `python -m pytest tests/unit/test_evidence_separation.py -xvs` → 9 passed
- [ ] `python -m pytest tests/unit/test_alert_center_api.py tests/unit/test_dashboard_escalation_audit.py` → 12 passed
- [ ] `gh pr checks <pr-number>` → All green
- [ ] `python -m ai_company.audit.export --date $(date -u +%F)` → No errors
- [ ] `grep -c correlation_id <all stores>` → All events have correlation_id

---

## Contact Escalation

| Role | Contact | When to Escalate |
|------|---------|------------------|
| Ops Lead | @ops-lead | Single store recovery fails |
| Platform Reliability Engineer | @platform-reliability-engineer | Multiple stores lost, rotation failed |
| Chief of Staff | @chief-of-staff | All stores lost, Git corrupted |
| CEO | @human-ceo | All recovery options exhausted |

---

## Quick Reference: Key Commands

```bash
# Verify the AuditWriter hash chain (only hash-chained store)
python -m ai_company.audit.integrity verify .opencode/audit/audit.jsonl

# Structurally verify append-only evidence stores (no chain fields)
python -m ai_company.audit.integrity check orchestrator/escalation_events.jsonl
python -m ai_company.audit.integrity check orchestrator/dead_letter.jsonl

# Export audit DB
python -m ai_company.audit.export --date $(date -u +%F)

# Rotate stores manually
python -c "
from ai_company.orchestrator.escalation_events import get_escalation_event_store
from ai_company.orchestrator.dead_letter import get_dead_letter_store
get_escalation_event_store().rotate(30)
get_dead_letter_store().rotate(90)
"

# Check correlation IDs
python -c "
import json, glob
for f in glob.glob('orchestrator/*.jsonl') + glob.glob('reports/evidence/*.jsonl'):
    with open(f) as fp:
        cids = [json.loads(l).get('correlation_id') for l in fp if l.strip()]
    print(f'{f}: {len(set([c for c in cids if c]))} unique correlation_ids')
"

# Run all evidence tests
python -m pytest tests/unit/test_evidence_separation.py -xvs
```

---

## Post-Incident Actions

After ANY DR event:

1. **Document** in `knowledge/technology/bug-fixes/BUG-<date>-evidence-recovery.md`
2. **Update** this runbook with lessons learned
3. **Notify** stakeholders via Slack #ops-alerts
4. **Schedule** post-incident review within 48 hours
5. **Update** this runbook version and date

---

*This runbook is part of ADR-008 Evidence Separation Architecture. Review quarterly per operations-sop.md §7.3.*
