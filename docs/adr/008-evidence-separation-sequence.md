# Evidence Separation — Sequence Diagrams

This document contains Mermaid sequence diagrams for the evidence separation architecture.

---

## 1. Weekly Repository Audit — Evidence Flow

```mermaid
sequenceDiagram
    autonumber
    participant GH as GitHub Actions (cron)
    participant Det as Deterministic Scan
    participant Art as Artifact Store
    participant EM as EscalationManager
    participant DLQ as DeadLetterQueue
    participant AW as AuditWriter
    participant Exp as Export Job
    participant Aud as Auditor Agent
    participant GH2 as GitHub (commit)

    Note over GH,Exp: Weekly Repository Audit (Sun 06:00 UTC)

    GH->>Det: Trigger deterministic-audit
    Det->>Det: Run scans, produce evidence
    Det->>Art: Upload evidence-<date>.json
    Det->>Art: Upload stub report

    Note over GH,Exp: Phase 2 - Agent Deep Pass

    GH->>EM: Seed audit task (chief-of-staff)
    EM->>EM: Read evidence from Art
    EM->>EM: Analyze + write findings
    EM->>EM: Write report to reports/repo-audit-<date>.md
    EM->>EM: Append escalation events to orchestrator/escalation_events.jsonl
    EM->>Aud: Notify Auditor (via task)

    Auditor->>Aud: Read evidence from reports/evidence/<date>.json
    Auditor->>Aud: Read escalation events from orchestrator/escalation_events.jsonl
    Auditor->>Aud: Read dead-letter from orchestrator/dead_letter.jsonl
    Auditor->>Aud: Write final report to reports/repo-audit-<date>.md

    GH->>GH2: Commit report + evidence

    Note over GH,Exp: Daily Audit Export (07:00 UTC)

    GH2->>Exp: Trigger audit-export workflow
    Exp->>Exp: Read audit/audit.db
    Exp->>Exp: Export to reports/evidence/audit-<date>.jsonl
    Exp->>Art: Upload audit-<date>.jsonl artifact
    Exp->>GH2: Commit evidence file
```

---

## 2. Escalation Event Lifecycle

```mermaid
sequenceDiagram
    autonumber
    participant Agent as Task Agent
    participant EM as EscalationManager
    participant EES as EscalationEventStore
    participant AW as AuditWriter
    participant GH as GitHub Actions (rotation)

    Note over Agent,GH: Escalation Triggered

    Agent->>EM: trigger_escalation(task_id, rule_id, from_agent, reason)
    EM->>EM: Create EscalationEvent (correlation_id = uuid_v7())
    EM->>EES: append(event)
    EES->>EES: Append JSONL line to orchestrator/escalation_events.jsonl
    EES->>AW: Write AuditEvent(ESCALATION_TRIGGERED, correlation_id)
    AW->>AW: Write to .opencode/audit (hash-chained JSONL)

    Note over Agent,GH: Resolution

    Agent->>EM: resolve_escalation(task_id)
    EM->>EM: event.resolved = True
    EM->>EM: _save_events() → EES.append(resolution_event)
    EES->>EES: Append resolution JSONL line (same correlation_id)
    EES->>AW: Write AuditEvent(ESCALATION_RESOLVED, correlation_id)

    Note over GH: Monthly Rotation (cron)

    GH->>EES: rotate(30)
    EES->>EES: Read all events
    EES->>EES: Split by age (cutoff = now - 30 days)
    EES->>EES: Write current to temp file
    EES->>EES: os.replace(temp, main)  // ATOMIC
    EES->>EES: Write rotated to escalation_events.rotated-<ts>.jsonl
    EES->>AW: Write AuditEvent(EVIDENCE_ROTATED, correlation_id=rotation_id)
```

---

## 3. Dead-Letter Queue Lifecycle

```mermaid
sequenceDiagram
    autonumber
    participant Bus as MessageBus
    participant DLQ as DeadLetterQueue
    participant DLS as DeadLetterStore
    participant AW as AuditWriter
    participant GH as GitHub Actions (rotation)

    Note over Bus,GH: Task Becomes Stale

    Bus->>DLQ: detect_stale_tasks()
    DLQ->>DLQ: _task_is_stale() → reason
    DLQ->>DLS: append(DeadLetterEntry)
    DLS->>DLS: Append JSONL line to orchestrator/dead_letter.jsonl
    DLS->>AW: Write AuditEvent(DEAD_LETTER_MOVED, correlation_id)

    Note over Bus,GH: Retry or Retire

    alt Retry Budget Remaining
        DLQ->>Bus: retry_dlq_task(task_id)
        Bus->>Bus: Re-enqueue as pending
        DLS->>DLS: mark_resolved(id, "requeued")
        DLS->>AW: Write AuditEvent(DEAD_LETTER_RESOLVED, correlation_id)
    else Budget Exhausted
        DLQ->>DLS: Entry stays in DLQ
        DLS->>AW: Write AuditEvent(DEAD_LETTER_ARCHIVED, correlation_id)
    end

    Note over GH: Monthly Rotation (cron)

    GH->>DLS: rotate(90)
    DLS->>DLS: Read all entries
    DLS->>DLS: Split by age (cutoff = now - 90 days)
    DLS->>DLS: Write current to temp file
    DLS->>DLS: os.replace(temp, main)  // ATOMIC
    DLS->>DLS: Write rotated to dead_letter.rotated-<ts>.jsonl
    DLS->>AW: Write AuditEvent(EVIDENCE_ROTATED, correlation_id=rotation_id)
```

---

## 4. Daily Audit Export

```mermaid
sequenceDiagram
    autonumber
    participant GH as GitHub Actions (cron 07:00 UTC)
    participant Exp as Export Job
    participant DB as audit/audit.db
    participant EV as reports/evidence/
    participant AW as AuditWriter
    participant Art as Artifact Store
    participant GH2 as GitHub (commit)

    Note over GH,GH2: Daily Audit Export (07:00 UTC)

    GH->>Exp: Trigger audit-export workflow
    Exp->>Exp: Read date from input (or today)
    Exp->>DB: SELECT * FROM audit_log ORDER BY timestamp
    Exp->>EV: Write audit-<date>.jsonl
    EV->>AW: Write AuditEvent(EVIDENCE_EXPORTED, correlation_id=export_batch_id)
    EV->>Art: Upload artifact (90-day retention)
    EV->>GH2: Commit evidence files

    Note over GH2,AW: Auditor Consumption

    Auditor->>Auditor: Read reports/evidence/audit-<date>.jsonl
    Auditor->>Auditor: Join with escalation_events.jsonl (by correlation_id)
    Auditor->>Auditor: Join with dead_letter.jsonl (by correlation_id)
    Auditor->>Auditor: Produce forensic report
```

---

## 5. Auditor Workflow — Evidence Separation Enforcement

```mermaid
sequenceDiagram
    autonumber
    participant Aud as Auditor Agent
    participant EV as reports/evidence/
    participant EES as orchestrator/escalation_events.jsonl
    participant DLS as orchestrator/dead_letter.jsonl
    participant EV2 as reports/evidence/audit-*.jsonl
    participant Out as reports/repo-audit-<date>.md

    Note over Aud,Out: Auditor Workflow (Read-Only Evidence)

    Aud->>EV: Read evidence-<date>.json
    Aud->>EES: Read escalation_events.jsonl
    Aud->>DLS: Read dead_letter.jsonl
    Aud->>EV2: Read audit-<date>.jsonl

    Note over Aud: All reads from EVIDENCE directories only

    Aud->>Aud: Analyze, correlate by correlation_id
    Aud->>Out: Write findings to reports/repo-audit-<date>.md

    Note over Aud: Write set = {Out} (disjoint from all evidence dirs)

    alt Violation Attempt
        Aud->>EV: Attempt write to reports/evidence/
        EV->>Aud: PermissionError / Guardrail blocks
        Aud->>Aud: Report violation per §9.3
    end
```

---

## 6. Cross-Store Correlation ID Flow

```mermaid
sequenceDiagram
    autonumber
    participant Trigger as Task Trigger
    participant EM as EscalationManager
    participant DLQ as DeadLetterQueue
    participant Exp as Export Job
    participant Corr as correlation_id

    Note over Trigger,Exp: Single Incident, Three Stores, One correlation_id

    Trigger->>EM: Task fails → trigger_escalation()
    EM->>EM: correlation_id = uuid_v7()
    EM->>EES: Append {correlation_id, ...}

    alt Task Also Goes to DLQ
        Task->>DLQ: move_task()
        DLQ->>DLS: Append {correlation_id, ...}
    end

    alt Task Audited
        Exp->>Exp: export_audit_log()
        Exp->>EV: Append {correlation_id, ...}
    end

    Note over EES,DLS,EV: All three stores now have events with SAME correlation_id

    Auditor->>Auditor: Query all three stores by correlation_id
    Auditor->>Auditor: Reconstruct full incident timeline
```

---

## 7. DR Recovery Flow

```mermaid
sequenceDiagram
    autonumber
    participant Ops as Ops Team
    participant Git as Git Repo
    participant Art as Artifact Store
    participant EV as reports/evidence/
    participant EES as orchestrator/escalation_events.jsonl
    participant DLS as orchestrator/dead_letter.jsonl

    Note over Ops,Art: DR Scenario — Evidence Corruption/Loss

    alt Git Available
        Ops->>Git: Clone repo (latest main)
        Ops->>EV: Verify reports/evidence/ exists
        Ops->>EES: Verify orchestrator/escalation_events.jsonl
        Ops->>DLS: Verify orchestrator/dead_letter.jsonl
    else Git Corrupted
        Ops->>Art: Download latest audit-evidence artifact
        Ops->>Art: Download latest audit-report artifact
        Ops->>EV: Restore from artifact
    end

    Note over Ops: Verify Integrity

    Ops->>Ops: Run integrity.py verify on the AuditWriter trail (.opencode/audit)
    Ops->>Ops: Run integrity.py check on the three evidence stores
    Ops->>Ops: Confirm all lines are well-formed JSON (stores carry no chain fields)
    Ops->>Ops: Verify rotation integrity (no gaps in sequence)

    Note over Ops: Recovery Complete

    Ops->>Ops: Document recovery in postmortem
    Ops->>Ops: Update DR runbook with lessons learned
```

---

## Legend

| Symbol | Meaning |
|--------|---------|
| → | Synchronous call |
| →> | Asynchronous / event |
| alt/else | Conditional branch |
| Note over | Annotation |
| /// | Evidence separation boundary |

---

*Generated as part of ADR-008 Evidence Separation Architecture*
