# 09 — Thought Leadership: REA Feasibility

**Prepared by:** Pharos — Thought Leadership Lead, for the Human CEO (Jack Mlusu)
**Date:** 2026-10-17
**Corpus:** `reports/rea-feasibility/` (FEASIBILITY-STUDY.md + capability, market, security, strategy reports)
**Audience:** LinkedIn long-form / newsletter / whitepaper chapter
**Status:** Draft for Human CEO review before publication

**Evidence labels:** [V] verified against primary source · [D] directional estimate · [U] unverified · [S] synthesis inference

---

## Title options

1. **Evidence or It Didn't Happen: What a Reverse-Engineering Agent Teaches Malawi and SADC About Governed AI**
2. **The Agent That Takes Software Apart — And the Rules We Set Before Touching It**
3. **From 300,000 Stars to a Signed Decision: How to Evaluate an AI Agent That Reverse-Engineers Code**

**Selected title:** Option 1.

---

## The article

### Evidence or It Didn't Happen

Close to 300,000 stars. 75,000 forks. Six months old, still shipping several releases a week, and carrying 1,207 open issues. [V] That is the profile of REA — a tool that lets an AI agent take software apart and explain what it found.

My research team spent this week reading it. Not the launch posts. The security model, the licensing terms, the output contracts, and the fine print about what it refuses to promise. This is the first piece I have put my name to on a specific piece of technology, because the answer it forces is bigger than the tool.

Here it is: **an AI agent that can inspect software and hand back a labeled evidence record is something institutions in Malawi and SADC can genuinely use — not as a product to sell or a venture to raise on, but as a governed consulting service line we switch on only after its supply-chain conditions are met, and only behind a human approval gate.** [S]

Everything below is why, and where I am still uncertain.

### What the thing actually does, in plain language

REA is a local server and command-line tool. You point an AI agent at a target — a compiled program, a phone application, a website, a database, a network capture — and the agent asks it questions. The analysis runs on your own machine. REA does not write its own disassembler; it drives existing analysis engines and returns their findings wrapped in a standard format. [V]

That format is the part that matters to me. Every answer arrives as an **Evidence record**: the structured conclusion, a stable identifier, the raw engine output behind it, and the settings used. [V] Runs are keyed to the exact bytes of what you analyzed plus the operation, parameters, provider and settings — so a result can be reproduced and compared later instead of taken on faith. [V] And the record states what could not be resolved alongside what was found. Inventories come with a coverage flag, because an incomplete list that presents itself as complete is how audits go wrong. [V]

A tool that labels its own limits is rare. Most software sells you certainty. This one hands you a file and says: here is what I know, here is what I could not determine, here is how to check my work.

### Why Malawi and SADC should care first

The people who most need to verify software are the people who cannot read it. Regulators and CIOs here are asked to trust systems they did not write — payment SDKs sitting inside banking applications, third-party libraries handling personal data, public-sector platforms bought through procurement cycles that assume the vendor's word is enough.

Meanwhile the rules are catching up unevenly. Our Data Protection Act 2024 is in force and offers no interpretation for autonomous systems. [V] The National AI Strategy was validated in 2026, a public-sector AI bill is in draft, and at regional level the AU Continental AI Strategy and the SADC digital agenda are being written in real time. [V] Institutions drafting those documents are not short on commentary. They are short on people who have built the system and can show the evidence trail.

Data residency sharpens the point. REA's own documentation says analysis runs locally and the tool does not upload your application. [V] It also says something most vendors bury: results still flow to the agent's model provider, whose data policy then applies. [V] Local analysis is not automatically local privacy. That gap is exactly where a governed operator earns their keep — deciding, in writing, what leaves the machine and what never does.

The commercial framing is honest, too. Application security is roughly a US$67.2 billion market in 2026, growing about 15.5% a year. [V] The pure "reverse-engineering-as-a-service" slice inside it is likely under US$5 billion. [D] Large enough to matter. Narrow enough that I will not pretend it is a venture. That is why our feasibility verdict landed where it did: a conditional pilot run as a consulting service line — not a product, not a fundraise. [V]

### How we govern it, because trust is the product

Our position is not "AI can now reverse-engineer software." Anyone can say that. Our position is how it is authorized, evidenced, and stopped.

**Authorization.** The tool's own terms are explicit: it grants no license to the commercial engines it drives, operators must legally obtain those tools themselves, and cracked copies or shared keys are unauthorized. [V] Its stated purpose is lawful research on software you own or are authorized to examine. [V] We adopt that boundary as a client intake rule. If you cannot prove authorization, we do not open the file.

**Evidence.** Every finding carries its identifier, its raw output, and its stated coverage limits. Nothing goes to a client as a bare conclusion. The limitations travel with the finding, always.

**Human accountability.** Our five-tier approval system applies before anything leaves the lab. A human signs the finding, not the model. The audit trail records who approved what, when, and on what evidence.

**Honesty about the boundary.** REA's security documentation states plainly that it is not a sandbox — it offers no protection against a malicious process running as the same user. [V] We say the same thing to clients. A system that tells you where it stops is more trustworthy than one that does not, and naming the gap is how you close it with process.

**And the honesty badge on the pipeline itself:** analysis running locally still puts results in front of a model provider. Choosing that provider, constraining what is sent, and documenting the choice is a governance decision we own, not a default we inherit. [S]

### What blocks us today

Our security review came back "safe to proceed — with conditions." [V] Four supply-chain controls are prerequisites, not nice-to-haves: pin every dependency, mirror the lockfile with hashes, audit every install script, and disable automatic updates. [V] Until those land, there is no production use. I would rather publish that sentence than publish a demo.

Three further constraints I want on the record. The project ships multiple releases a week, and breaking changes are documented — version pinning is mandatory for any real engagement. [V] The primary author holds roughly 53% of top contributions, which is a bus factor of one. [V] And deep analysis on Windows is still experimental and read-only, with several target classes available only on Linux. [V] None of that is disqualifying. All of it changes how we scope a first engagement, and a client deserves to hear it in the first conversation rather than the fifth.

### What remains uncertain

Whether this converts into revenue inside Malawi's and SADC's buying cycles is unproven — the market figures above describe an industry, not our pipeline. [D] Whether a six-month-old, fast-moving upstream stays compatible with our pinned, audited setup over a multi-year engagement is an open operational question. [U] And a few primary-source details — the full disclaimer text, the exact tool count in the published catalog — were not verified in this pass. [U] I will not fill those gaps with confidence. I will fill them with a second reading.

### The declaration

The region does not need another person explaining what AI might do. It needs people who built it, showed the evidence, and wrote down the rules they operated under — in that order.

So we will build the capability here, under our own conditions. We will evidence it in public, with findings that carry their own limits. And we will take both into the rooms where Malawi's and SADC's AI governance is being drafted, because the institutions writing those rules should have a builder at the table, not only a commentator.

Build it. Evidence it. Then shape the policy. That is the sequence, and we are starting at the first step.

---

## Appendix — Adaptations

### LinkedIn hook variant

> Close to 300,000 stars. Six months old. 1,207 open issues.
>
> An AI agent that takes software apart and hands back a labeled evidence record is now mainstream — and almost nobody is asking the second question: under what rules should anyone in Malawi or SADC use it?
>
> Our answer: not a product, not a venture. A governed service line — conditional on four supply-chain controls, gated behind a human signature, and published with its limitations attached.
>
> Full piece: [link]

### Newsletter subject lines

1. Evidence or it didn't happen: our verdict on a reverse-engineering agent
2. 300,000 stars, 4 conditions, 1 human signature
3. What we will and won't do with an AI agent that reads software

### Executive summary (5 bullets)

- REA is a local MCP server and CLI that lets AI agents inspect software — binaries, apps, websites, databases, captures — and return findings as canonical Evidence records with stated coverage limits and reproducible snapshots. [V]
- Feasibility verdict: **conditional pilot as a governed consulting service line** — not a product, not a venture; security status is "safe to proceed — with conditions," blocked on four P0 supply-chain controls (pin, mirrored lockfile with hashes, install-script audit, no auto-update). [V]
- Malawi/SADC relevance: regulators and CIOs must trust software they cannot read, while DPA 2024 has no interpretation for autonomous systems; local analysis answers the data-residency question, but results still reach the model provider — a policy decision we own. [V]
- Market honesty: application security is ~US$67.2B in 2026 (+15.5% YoY) [V]; the pure reverse-engineering-as-a-service slice is likely under US$5B [D] — real, but not a venture thesis.
- Open risks carried into any pilot: single-maintainer concentration (~53% of top commits), multi-week release cadence requiring version pins, experimental read-only Windows analysis, and unverified market conversion in our buying environment. [V]/[D]/[U]

---

*Drafted by the Pharos thought-leadership team on behalf of the Human CEO. No client names. No internal budget figures. All statistics drawn from the feasibility corpus with evidence labels.*
