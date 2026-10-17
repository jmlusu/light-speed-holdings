---
name: reservations-playbook
description: "Turn the four skeptic objections to AI in low-bandwidth, resource-constrained environments (bandwidth, data protection, technology debt, AI skepticism) into credible, honesty-badged answers for demos, sales, and Pharos thought leadership. Use when writing objection copy, preparing demo scripts, drafting FAQ answers, or building trust messaging."
category: consulting
risk: safe
date_added: "2026-09-11"
author: light-speed-holdings
tags: [reservations, objections, trust, demos, thought-leadership, low-bandwidth, data-protection, tech-debt]
tools: [read, grep, list, bash, webfetch]
---

# The Four Reservations — Playbook

## Overview

Decision-makers in low-bandwidth, resource-constrained environments hold four
repeatable reservations about AI. This skill produces **credible, honesty-badged
answers** to all four, grounded in Lightspeed's real platform evidence and its
engineering capability DNA (never a named-person bio), and formats them for
demos, sales conversations, website FAQ copy, and Pharos thought leadership.

The four reservations:

1. **Low-bandwidth / resource-constrained** — "This won't work on our devices, our
   connectivity, or our electricity reality."
2. **Data protection** — "Where does our data go? Does it leave our country?"
3. **Technology debt** — "Won't this rip out what we have, or become a system we
   have to maintain forever?"
4. **Skepticism of AI** — "We tried AI before and it failed. Why would this be
   different, and how do we trust it?"

## When to Use

- Writing objection/FAQ copy for the client-facing website, chatbots, or pitch decks
- Building a portfolio demo script that lets a prospect probe the four reservations
- Drafting Pharos content that positions Lightspeed as the organization that
  understands these environments
- Reviewing any marketing copy for overclaiming or a missing honesty badge

Do NOT use for: platform engineering work itself, legal contract drafting, or
policy submissions (those live in their own lanes).

## Inputs

- Target surface: demo script / website FAQ / sales transcript / Pharos piece
- Audience: enterprise/gov CIO, NGO/donor M&E lead, local SME, policymaker
- Any real platform artifacts already in the repo (OmniRoute, offline sync, Ollama,
  governance gates, audit trails, cost tracker)

## The Four Answers (canonical doctrine)

Every answer follows the same shape: **the honest admission → what we do → the
engineering evidence → the proof posture (honesty badge)**. Never claim delivery
that did not happen; "pilot", "in active development", "fieldable in 2026", and
"proven in-house" are the only four badges available.

### 1. Low-bandwidth / resource-constrained

> We design for the reality. Offline-first architecture, local inference via free
> models (Ollama) when connectivity or budget demands it, WhatsApp-native
> interfaces with no app download, and a PWA that queues work offline and syncs
> on reconnect. We route traffic quota-first when a connection is weak, and we
> test where you operate because that is where we operate.

Evidence sources: `docs/ARCHITECTURE-OMNIROUTE.md` (auto/offline quota-first),
`docs/api/MOBILE-API.md` (offline sync), local Ollama inference, PWA offline
action queue. Capability DNA: process-optimization engineering — every workload
is a process to optimize; bandwidth is a budget, latency is a constraint we
engineer to.

### 2. Data protection

> Your data stays on your infrastructure. Sovereign in-country processing is the
> default; every cross-border flow to an LLM provider is documented in our
> governance gate process and routed to the most privacy-preserving option. Malawi
> Data Protection Act 2017/2024 and GDPR are built in from day one. We never use
> client data to train models.

Evidence sources: `docs/client-facing/USE-CASE-CATALOG.md` (sovereignty),
governance gates G1–G4, `docs/CEO-DIRECTIVE-BLUEPRINT-ADOPTION.md` (data
sovereignty interpretations owned by data-privacy-officer + ciso). Capability
DNA: enterprise data architecture across regulated telecom, finance, and
healthcare estates, plus public-sector regulatory delivery.

### 3. Technology debt

> Adopting AI should not mean ripping out what works. We integrate with your
> existing stack via API connectors during a 90-day pilot, we do not add a second
> system you must maintain, and your data and deliverables stay under your
> control — no lock-in. We hold ourselves to the same rule: our own engineering
> debt is tracked in a ledger, reviewed by architecture linting, and budgeted for
> paydown.

Evidence sources: 90-Day Pilot legacy connectors (FAQ), `docs/AGENT-REGISTRY-TABLE.md`
(vp-engineering owns technical debt reduction), ponytail-debt ledger, brooks-lint
reviews. Capability DNA: Fortune 500-scale ETL and data integration across
merged business divisions — legacy estate integration at scale is the norm, not
an exception.

### 4. Skepticism of AI

> Most AI failures in this region are governance failures, not technology
> failures — a chatbot that hallucinates, a tool that violates data sovereignty,
> a system with no audit trail. We are governance-first: 5-tier human-in-the-loop
> approvals, immutable audit trails, risk-classified agent tiers, circuit
> breakers, red-team testing, and evaluation gates. The system earns a Chief Risk
> Officer's "yes" before a user's "wow" — and we never fabricate proof.

Evidence sources: 5-tier HITL approvals, immutable JSONL audit trails, risk
matrix, `docs/CEO-DIRECTIVE-BLUEPRINT-ADOPTION.md` thought-leadership lines,
honesty ladder (`docs/superpowers/specs/2026-09-06-lightspeed-website-design.md`
§2.4). Capability DNA: development-sector M&E authority and global-health data
delivery in low-connectivity field settings.

## Capability DNA framing rule

Institutional capability lines may draw on the company's engineering history
(Fortune 500 data architecture, regulated public-sector delivery, last-mile
health data systems, process-optimization foundations) but must be phrased as
**"We have architected…", "Our engineering discipline…"** — never named-person
biography, never "the CEO is the value". See the guardrail "Never present the CEO
as the only value" in the messaging brief.

## Demo-script pattern

A reservation-probing demo has five beats:

1. **Capability frame** (institutional): one line establishing the engineering
   pedigree behind the platform.
2. **Show the real conditions**: throttle to 3G/offline; show the offline queue,
   local model fallback, and sub-response payload.
3. **Show the data boundary**: where data lives, what leaves, what is documented
   (the G1–G4 flow and consent).
4. **Show the legacy path**: connect an existing tool; no rip-and-replace; what
   the 90-day pilot integrates.
5. **Show the trust rails**: an HITL approval in flight, an audit trail entry,
   a risk classification — and the honesty badge for each claim.

Each beat ends by naming the honest status badge for what was just shown.

## Related skills (reuse, do not duplicate)

| Reservation | Skills to invoke |
|-------------|------------------|
| Low-bandwidth | `performance-optimizer`, `karpathy-guidelines` |
| Data protection | `security-and-hardening`, `api-endpoint-builder` |
| Technology debt | `ponytail-review`, `ponytail-debt`, `brooks-lint` |
| Skepticism | `grilling`, `code-review-and-quality`, `no-ai-slop` |
| Evidence | `k-dense-research-lookup`, `research` |
| Pharos output | `pharos-thought-leadership-author`, `pharos-research-lead` |

## Output format

Return the answer as a block with: the target surface, the audience, the answer
text (in brand voice), the evidence file:line cites, and the honesty badge to
display. Never return fluff.
