# YouTube Short — Tutorial Clip Script

**Status:** Queued until accounts exist (#194)
**Platform:** YouTube — Short, vertical 1080×1920, ~55 seconds
**Format test (Week 2):** Short (tutorial clip) — hypothesis: clips > teasers for subs
**Voice:** Builder register, no emojis, no hype, tutorial register.
**Facts source:** `docs/Pharos/h-a-o-m-t-g-v-framework.md`; `company-registry.yaml`

---

## Title (for when the account exists)

"How a 5-tier approval gate stops an AI agent"

## Script

| Time | Visual | Audio |
|------|--------|-------|
| 0-5s | Hook: agent request card hitting a red "APPROVAL REQUIRED" gate | "What stops an AI agent from acting on its own? Five tiers of human approval. Here is how it works." |
| 5-15s | Diagram: agent -> risk classification -> tier determination | "When an agent wants to do something high-risk, it does not just execute. Its action is classified by risk first." |
| 15-35s | Diagram: tier ladder 1-5, human authorizes at the top, audit log entry appears | "Higher risk means a higher approval tier. Irreversible or high-impact actions pause and wait for a named human to authorize. The human stays accountable." |
| 35-48s | Audit trail: append-only log lines appear | "Every decision path is recorded — the tool invoked, the memory retrieved, the action taken — in an immutable audit trail." |
| 48-55s | End card: logo + tagline + site | "That is the governance layer of our H-A-O-M-T-G-V framework — humans authorize, agents act. LightSpeed Holdings Limited™. Follow for the next layer." |

---

## Production notes

- Spoken word count ≈ 140 (comfortable for ~55s; record a dry run and trim).
- Visuals: brand palette only (navy `#070A40`, red `#E63946`, cyan `#00BFFF`),
  Arial type, official icon-only logo. Keep the approval ladder legible on mobile.
- When #314 template output lands, use the generated Short thumbnail; until then
  the end card above is the branded poster frame.
- Post natively; no scheduler. After posting, comment once on the Short with the
  framework name ("H-A-O-M-T-G-V — humans authorize, agents act") to seed
  discussion.
- Reply to all comments within 24h.

## Fact checklist

| Claim | Source |
|-------|--------|
| 5-tier HITL approval | `docs/Pharos/manifesto-draft.md:64-80`; registry `decision_engine_owner` (approval matrix) |
| Immutable audit trails / every decision path logged | `docs/Pharos/manifesto-draft.md:66-70`; registry `platform_reliability_engineer` |
| H-A-O-M-T-G-V framework | `docs/Pharos/h-a-o-m-t-g-v-framework.md:16-35` (Human Authorize / Agents Act) |
| Brand colors and type | `brand/tokens/brand-tokens.json` |
