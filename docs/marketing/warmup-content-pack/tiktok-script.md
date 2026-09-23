# TikTok Script — 30s Hook + Demo

**Status:** Queued until accounts exist (#194)
**Platform:** TikTok — native video, vertical 1080×1920
**Format test (Week 2):** Hook + demo (30s) — hypothesis: demo > talking head for reach
**Voice:** Builder register, no emojis, no hype. Script clock ≈ 30 seconds (~80 words spoken).
**Facts source:** `company-registry.yaml`; `docs/Pharos/h-a-o-m-t-g-v-framework.md`

---

## Script

| Time | Visual | Audio |
|------|--------|-------|
| 0-3s | Hook: "90 agents" on navy card, red accent | "89 AI agents work for this company. A human approves every high-risk move." |
| 3-10s | Cut to simple whiteboard-style flow | "Most organizations fear AI because it acts without accountability. So we built the accountability in." |
| 10-22s | Animate the seven-layer stack H-A-O-M-T-G-V, then zoom into the Governance tier | "Every agent action sits on a seven-layer framework. High-risk actions pause and climb five approval tiers. Every decision is written to an immutable audit trail." |
| 22-27s | CTA card: logo, tagline, cyan line | "We built and run this in Malawi — 20 departments, one accountable human chain." |
| 27-30s | End card | "Follow for governed agentic AI. ASPIRE. ACT. ACHIEVE." |

---

## Production notes

- Spoken word count ≈ 80 (fits 30s at natural pace; record a dry run and trim to
  the second).
- Use the official icon-only logo (`brand/logos/icononly/icononly_transparent.png`
  or `static/brand/social/avatar-1024.png` mirror) on the end card; navy
  background, red accent, cyan line per `brand/tokens/brand-tokens.json`.
- When #314 template output lands, use the generated TikTok visual; until then
  the card-based navigation above is fully on-brand.
- Post natively (no scheduler). No links in bio early on; keep hashtag set small
  (`#AgenticAI`, `#AIGovernance`).
- Reply to every comment; where possible, pin a "part 2?" comment with the
  framework breakdown (drives repeat views).

## Fact checklist

| Claim | Source |
|-------|--------|
| 90 agents | `company-registry.yaml` (counted 2026-09-23) |
| Human approves every high-risk move (5-tier HITL) | `docs/Pharos/manifesto-draft.md:64-80` |
| Immutable audit trails | `docs/Pharos/manifesto-draft.md:64-80`; registry `platform_reliability_engineer` |
| Seven-layer H-A-O-M-T-G-V | `docs/Pharos/h-a-o-m-t-g-v-framework.md:16-35` |
| 20 departments | `company-registry.yaml` (counted 2026-09-16) |
| Tagline ASPIRE. ACT. ACHIEVE. | `brand/tokens/brand-tokens.json` |
