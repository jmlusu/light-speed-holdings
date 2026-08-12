# ADR-010: T1 Event-Bus Alignment with the File-Based MessageBus

**Status:** Accepted
**Date:** 2026-08-12
**Deciders:** CTO, Wayfinder
**Technical Domain:** Task Queue & Event Bus

## Context

The T1 spec calls for an event-driven task queue (Redis / Kafka / RabbitMQ) with
sub-10ms message delivery latency, zero dropped tasks, and fan-out across up to
127 concurrent agents. The current runtime uses a hardened JSON `MessageBus`
(see ADR-002, ADR-005) that is **single-machine, file-based**, with atomic writes,
file locking, lease-based claiming, corrupt-inbox recovery, and a best-effort
SQLite write-through mirror (ADR-005, Sprint 2).

Two surfaces of T1 are in tension with the single-machine posture:

1. **Durability / task lifecycle / no dropped tasks** — already met by the
   hardened `MessageBus` (atomic writes, backups, quarantine + recovery,
   lease/stale-detection). This is the bus's actual production risk surface and
   it is covered.
2. **Sub-10ms *push* delivery latency** — the file bus is **tick/polling-driven**
   (an executor reads `inbox.json` on its loop); there is no publisher push. This
   is the genuine gap, but only under high fan-out / many agents.

## Decision

Keep the hardened JSON `MessageBus` as the default (supersede nothing — ADR-002
and ADR-005 remain in force). Concretely:

- T1's **durability, lifecycle, and no-dropped-tasks** requirements are considered
  satisfied by the current bus for the expected workload (<100 tasks/day,
  ~127 agents, single-node).
- **Sub-10ms delivery latency + 127-agent fan-out** are treated as a
  *reported target*, evidenced by a report-only benchmark at
  `tests/unit/test_message_bus_perf.py` (marked `performance`, never a CI gate).
- **No Redis/Postgres pub/sub adapter is added now.** The single-machine-first +
  infra-opt-in posture means a push bus is only introduced if the benchmark
  demonstrates the file bus cannot hold the target under fan-out — at which
  point an optional adapter behind the `MessageBus` interface is added without
  superseding the file-bus ADRs (they remain the fallback + local default).

## Consequences

- **Positive:** preserves the single-machine, no-external-services posture;
  avoids Windows Docker/Redis infra; keeps a simple, auditable, human-readable
  inbox; defers complexity with a measured trigger rather than a commitment.
- **Negative / risk:** latency under fan-out is *measured, not pre-emptively
  built*. If T1's fan-out target is breached, a second decision (supersede
  ADR-002) will be required. Mitigation: the benchmark runs every CI cycle on the
  `performance` marker and prints to the CI log, so regression is visible before
  it is a customer problem.
- **Neutral:** the SQLite write-through mirror already in place (ADR-005) can
  serve some downstream read consumers without a file read, which also lowers
  read latency for dashboard consumers regardless of bus choice.

## Links

- Ticket: #34 Decide the event-bus evolution (decision record)
- Map: #33 Wayfinder: mission-control dashboard spec
- ADR-002: JSON MessageBus
- ADR-005: File-based Persistence vs Database
- Evidence: `tests/unit/test_message_bus_perf.py`
