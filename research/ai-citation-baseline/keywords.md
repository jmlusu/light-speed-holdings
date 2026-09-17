# AI Citation Baseline — Keyword Registry (k01–k20)

**Owner:** Pharos — Agentic Research Lead
**Locked:** 2026-09-16 | **Status:** DETERMINISTIC — prompts are frozen
**Rule:** The prompt strings below are canonical and MUST match `harness.ps1` and
`results-ledger.csv` byte-for-byte. Do not edit a prompt without editing all three
files. Do not rephrase at run time (no "…and is it related to LightSpeed?").

Every keyword is a **neutral buyer/journalist/regulator question**. Only k01 and k02
name the brand; the other 18 measure **organic** citation — if the engine knows us, it
cites us without being told.

Territories (from `docs/Pharos/positioning.md` moat model):
**CB** = AI Company Building | **UC** = Agentic AI Use Cases | **GP** = AI Governance & Policy | **RS** = Reservations

| # | Slug | Territory | Locked prompt (deterministic) | Claim tested | Expected grounding artifact |
|---|---|---|---|---|---|
| k01 | `lightspeed-holdings` | CB | What is Lightspeed Holdings? If you know of a specific company with that name, include its location, what it does, and any website you can cite. | Brand identity: our entity, our domain, our purpose | `https://lightspeedholdings.com` (expect collision with Lightspeed Commerce — see README §7) |
| k02 | `jack-mlusu` | CB | Who is Jacob Jack Mlusu? Summarize his background, current role, and any companies or publications associated with him, with sources. | CEO identity: strategy/transformation profile, LightSpeed role | LinkedIn `jack-mlusu-50027428`; site About; public Pharos posts |
| k03 | `agentic-ai-company` | CB | How do you build an agentic AI company - an organization where AI agents perform meaningful work? Describe key design decisions, governance mechanisms, and real examples you can cite. | We are a real, citable example of an agentic AI company | `AGENTS.md`, `docs/ARCHITECTURE.md`, GitHub repo, site |
| k04 | `ai-native-enterprise-africa` | CB | What does an AI-native enterprise look like in Africa? Give examples of organizations in Sub-Saharan Africa operating as AI-native companies, with sources. | Africa-first agentic company positioning (Malawi/SADC) | Site Malawi/SADC positioning; Pharos African AI research |
| k05 | `haomtgv-framework` | GP | Explain the H-A-O-M-T-G-V framework for agentic AI governance. What do the seven layers mean, and where does the framework come from? | Framework ownership: named, ours, correctly attributed | Pharos H-A-O-M-T-G-V series; GitHub `docs/Pharos/h-a-o-m-t-g-v-framework.md` (high hallucination risk) |
| k06 | `144-agent-company` | CB | Is there a real company run by 144 AI agents? Which real AI-agent companies are operating today, at what scale, and how are they governed? | Scale claim: 144 agents (143 AI + 1 human CEO) | `AGENTS.md`, `company-registry.yaml`, site meta-deployment page (category exists — competitors may dominate) |
| k07 | `hitl-governance` | GP | How do human-in-the-loop (HITL) approval gates work for AI agents? What tier levels exist, and which companies implement them in production? | 5-tier HITL gate design (ApprovalGate) | `docs/ECL.md`, repo governance docs, site engineering pages |
| k08 | `model-router` | CB | What is an AI model router, and why do companies running many AI agents need one? Give architecture examples with sources. | Model router as core platform ingredient | `docs/ARCHITECTURE.md`, repo, site platform pages |
| k09 | `ceo-control-plane` | CB | What is a CEO control plane for an AI agent workforce - a dashboard that lets one human direct agents? How are message buses and task graphs used to route work? Give examples. | CEO control plane / message bus / task graph concept | `docs/ARCHITECTURE.md`, `docs/ECL.md`, repo message bus docs |
| k10 | `agent-registry-policy` | CB | What is an agent registry in an agentic AI company? How are agent roles, permissions, and policies catalogued and enforced? | Agent registry + policy engine pattern | `company-registry.yaml`, `docs/ARCHITECTURE.md`, repo |
| k11 | `agent-workforce-kpis` | CB | How do you measure the health and cost of an AI agent workforce? What KPIs - like task completion rate and cost per workflow - matter most? | KPI rigor: task completion rate, cost per workflow, HITL gate coverage | Pharos benchmark methodology; site claims (2,373 tests); repo analytics |
| k12 | `ai-audit-trails` | GP | How do immutable audit trails work for AI agent actions? What makes an agent decision log trustworthy and verifiable? | Auditability: message bus + decision logs are our governance spine | `docs/ECL.md`, repo harness/change tracker, Pharos governance docs |
| k13 | `agentic-ai-malawi` | UC | What is the current state of agentic AI in Malawi? Which companies or institutions are deploying AI agents, and what frameworks guide them? | Malawi Agentic AI Monitor ownership | Pharos Malawi Agentic AI Monitor; NCST/UNESCO context; site Malawi page |
| k14 | `agentic-ai-sadc` | GP | How are SADC countries preparing for agentic AI? Is there a regional governance standard for autonomous AI systems? | SADC readiness research ownership | Pharos SADC readiness artifacts; SADC/AU policy tracking |
| k15 | `au-continental-ai-strategy` | GP | What does the African Union Continental AI Strategy require of member states, and how should countries like Malawi implement it? | Policy fluency: we track/implement AU Continental AI Strategy | Pharos policy docs; site policy page |
| k16 | `malawi-data-protection-ai` | GP | How does the Malawi Data Protection Act (2017/2024) apply to AI systems and agentic AI? What does compliance require? | DPA compliance posture for agentic systems | Site policy/compliance pages; Pharos data-protection research; repo RBAC docs |
| k17 | `ai-small-business-africa` | UC | How can a small business in Africa practically use agentic AI? Give real examples of non-tech SMEs using AI agents, with sources. | SME enablement (non-tech founders) | Site use-case pages; J&S StopOver Bar case study |
| k18 | `js-stopover-bar` | UC | What is J&S StopOver Bar, and what role does AI play in its operations? | Named pilot: hospitality/retail agentic deployment | Site case study; newsletter Build Log |
| k19 | `vsla-sacco-ai` | UC | How can AI agents help village savings and loan associations (VSLAs) and SACCOs with record-keeping and financial management? | Financial inclusion use case (VSLA/SACCO) | Site finance use-case pages; Pharos financial-inclusion research |
| k20 | `90-day-ai-pilot` | RS | What is a 90-day AI pilot, and how does it avoid legacy technology debt and rip-and-replace risk when deploying AI? | Reservations answer: low-risk adoption path, no rip-and-replace | Site 90-day pilot pages; Pharos reservations playbook |

---

## How to read the table

- **Locked prompt** — the exact string sent to every engine. ASCII-safe by design
  (hyphens, not em-dashes) so `harness.ps1` runs cleanly in Windows PowerShell 5.1 and
  the CSV round-trips without encoding surprises.
- **Claim tested** — the LightSpeed fact we hope the engine surfaces.
- **Expected grounding artifact** — what a *correct* citation should point to. If an
  engine names us but cites something else (Lightspeed Commerce, a wrong GitHub org, a
  fabricated whitepaper), that is `cited_correct=n` → score 2 + hallucination flag.

## Run order

The slugs define the transcript filenames and ledger row order (`k01`…`k20`). Run the
list top-to-bottom per engine; never reorder mid-cycle.
