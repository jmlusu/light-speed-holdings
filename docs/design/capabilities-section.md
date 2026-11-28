# Design Spec — Six Capabilities Section (`/what-we-do`)

**Status:** Approved (CMO review + CPO final) — 2026-11-28
**Component:** `src/components/whatwedo/SixCapabilitiesSection.tsx`
**Owner:** Product Designer (layout), CMO (copy), CPO (product fit)

## 1. Section heading

- **Eyebrow:** `SIX CAPABILITY AREAS`
- **Title:** `What LightSpeed Builds`
- **Lead:** `Six capabilities, each mapped to the HAOMTGV operating model. Select one to see the problem it addresses, what we build, and how it connects to the pillars.`

## 2. Layout

- **Two-column split at `lg`:** left column = capability selector (sticky, scrollable list of 6 with status chip); right column = detail inspector. Mobile: horizontal scrollable chip row above a single detail panel.
- **Grouping:** keep two groups (Operational Execution 1–3; Strategy & Governance 4–6) but render as labeled dividers inside one list, not two separate grids, to reduce visual fragmentation. Group labels refined to `Build & Automate` (caps 1–3) and `Integrate & Govern` (caps 4–6).
- **Detail panel hierarchy (top → bottom):** (1) Title + status chip, (2) Overview, (3) Problem addressed (red callout), (4) What we build (checklist), (5) Architecture link (cyan callout), (6) Execution flow diagram (right rail on desktop, below on mobile), (7) Related research links, (8) inline CTA row.
- **Image:** move the architectural visualization to a thumbnail beside the title (not full-width aspect-video) to reduce scroll length; full image on hover/expand; remove if not essential. Alt text: `${title} — capability illustration`.
- **Inline CTA row (bottom of inspector):** `START A CONVERSATION → /contact` and `EXPLORE SOLUTIONS → /solutions`. Same CTAs on every capability (no "coming soon" dead-ends).

## 3. Capability data

Status values use the canonical `StatusBadge` set (`IN-HOUSE`, `PILOT`, `IN DEVELOPMENT`, `PROTOTYPE`, `EXPLORATION`). "Fieldable in 2026" maps to `PILOT`.

### 01 — AI-Native Company Building (IN-HOUSE)

- whatItIs: "A strategy and build capability for launching and operating companies where AI agents perform core execution, with human authority retained at the decision layer."
- problem: "New ventures face management overhead, hiring delays, and slow operational setup before they can deliver."
- whatWeBuild:
  - "Agent role hierarchies modelled on our own 90-role operating model (see research)."
  - "CEO control panels with budget and approval limits."
  - "Self-hosted or cloud deployment environments."
- architectureConnection: "Connects Human Authority (H) to Orchestration (O) and Value (V) measurement."
- diagramTitle: "Venture Creation Pipeline"
- diagramSteps: ["Opportunity Definition", "Operating Model Synthesis", "Agent Workforce Deployment", "Sovereign Launch"]
- relatedResearch: [{ title: "Inside a 90-Agent Company", slug: "inside-a-90-agent-company" }]

### 02 — Intelligent Workflow Automation (PILOT)

- whatItIs: "Automation that turns multi-step manual tasks into defined, auditable execution paths."
- problem: "Work waits for staff, manual copying between applications, and email-based approvals."
- whatWeBuild:
  - "Document and report pipelines starting from raw data."
  - "WhatsApp customer and order assistants."
  - "Airtel Money, TNM Mpamba, and PayChangu transaction integrations."
- architectureConnection: "Pairs Specialized Agents (A) with System Tools (T)."
- diagramTitle: "Workflow Compression Flow"
- diagramSteps: ["Multi-Source Ingestion", "Agent Decomposition", "Tool Invocations", "Verified Output"]

### 03 — Agentic Systems & Orchestration (IN-HOUSE)

- whatItIs: "Multi-agent task graphs that break complex work into coordinated subtasks with controlled state."
- problem: "General-purpose chatbots struggle with multi-step work that needs specialized roles and controlled state."
- whatWeBuild:
  - "Deterministic state machines for routing work."
  - "Parallel agent graphs with retries and regression checks."
  - "Agent-to-agent protocols with payload schema validation."
- architectureConnection: "Forms the Orchestration (O) engine coordinating Agents (A) and Memory (M)."
- diagramTitle: "Agent Network Routing"
- diagramSteps: ["Goal Parsing", "Task Decomposition", "Parallel Agent Execution", "Result Synthesis"]
- relatedResearch: [{ title: "Inside a 90-Agent Company", slug: "inside-a-90-agent-company" }]

### 04 — Enterprise AI Integration (IN DEVELOPMENT)

- whatItIs: "Integration architecture connecting AI models to ERP, CRM, database, and internal software systems."
- problem: "Isolated AI prototypes cannot securely access legacy databases or perform transactional writes."
- whatWeBuild:
  - "API gateway sandboxes with tokenized authentication."
  - "Connectors for SQL and unstructured data stores."
  - "Chichewa and English interfaces and API endpoints."
- architectureConnection: "Provides System Tools (T) and API boundaries for external execution."
- diagramTitle: "Integration Gateway"
- diagramSteps: ["API Authentication", "Tool Sandbox Boundary", "Enterprise Database Ingress", "Safe Execution"]

### 05 — Organizational Memory & Knowledge Systems (PILOT)

- whatItIs: "Persistent context storage for policies, historical lessons, and domain knowledge across sessions."
- problem: "Knowledge leaves when employees depart or rotate, so teams repeat solved problems."
- whatWeBuild:
  - "Vector stores with semantic indexing."
  - "Policy and standard operating procedure knowledge bases."
  - "Context retention across sessions and long-running projects."
- architectureConnection: "Implements Organizational Memory (M), supplying context to Agents (A) before decisions."
- diagramTitle: "Context Retrieval Architecture"
- diagramSteps: ["Query Embedding", "Vector Similarity Search", "Domain Context Injection", "Grounded Output"]

### 06 — AI Governance & Decision Infrastructure (IN-HOUSE)

- whatItIs: "A risk-classified governance framework with human approval gates, compliance checks, and cryptographic audit records."
- problem: "Uncontrolled AI deployment can cause reputational damage, regulatory breaches, and incorrect automated actions."
- whatWeBuild:
  - "A five-tier approval matrix (AUTO_APPROVE through CEO_ONLY)."
  - "Four execution gates (Contract, DPA, Compliance, Security)."
  - "Append-only SHA-256 audit logs."
- architectureConnection: "Forms the Governance (G) control layer across operations."
- diagramTitle: "Governance Gate Model"
- diagramSteps: ["Action Request", "Risk Classification", "Approval Gate Check", "SHA-256 Ledger Entry"]
- relatedResearch: [{ title: "The Five-Tier Approval Matrix", slug: "five-tier-approval-matrix" }]

## 4. Interaction notes

- Keyboard: arrow keys move between capability buttons; Enter/Space selects; focus ring visible.
- Mobile: horizontal scroll chip row; detail panel below; flow diagram collapses to vertical list.
- Status chips use `StatusBadge` (cyan/neutral only, no green — brand rule).

## 5. Accessibility notes

- Section has `aria-labelledby` pointing to title.
- Capability selector group uses `role="tablist"` with `role="tab"` children; `aria-pressed={isSelected}` (or `aria-selected`).
- Detail panel uses `aria-live="polite"` on selection change.
- Image alt text descriptive; decorative dividers marked `aria-hidden`.

## 6. Status label clarity (CPO tweak)

- `IN-HOUSE` renders with adjacent micro-copy: "Built and operated in our own company first."
- `IN DEVELOPMENT` renders with: "In development — available for scoped early engagement."
- `PILOT` renders with: "In pilot — available for scoped early engagement."

## 7. Notes

- Content changes are wording refinements; no invented metrics or client claims. "Proven in-house" retained only where the capability is exercised in our own 90-agent company.
- Footer wording: "Reference architecture" (not "Verified Architecture"); "HAOMTGV-aligned" (not "HAOMTGV Grounded").
- Subsection header: "What this capability includes" (not "What LightSpeed Builds & Configures").
- Group labels: "Build & Automate" / "Integrate & Govern".
