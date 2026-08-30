# Documentation Standards

> **Version**: v1.0
> **Date**: 2026-08-26
> **Author**: Technical Documentation Lead
> **Status**: Active — applies to all sections of the CEO Dashboard User Guide

---

## Table of Contents

1. [Voice and Tone](#1-voice-and-tone)
2. [Formatting Conventions](#2-formatting-conventions)
3. [Diagram Specifications](#3-diagram-specifications)
4. [Accessibility Requirements](#4-accessibility-requirements)
5. [Screenshot Placeholders](#5-screenshot-placeholders)
6. [Cross-Reference Conventions](#6-cross-reference-conventions)
7. [Version History](#7-version-history)
8. [Contributing to This Guide](#8-contributing-to-this-guide)
9. [Glossary Convention](#9-glossary-convention)

---

## 1. Voice and Tone

Write in a **professional but approachable** style. The CEO Dashboard User Guide is read by non-technical executives, operations leads, and technical stakeholders alike. Every sentence should be immediately understandable without requiring domain expertise.

### 1.1 Pronoun and Perspective Rules

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Second person for addressing the reader | "You can filter tasks by status." | "The user can filter tasks by status." |
| Active voice for all instructions | "Click **Approve** to confirm." | "The approval is confirmed by clicking **Approve**." |
| Present tense for UI descriptions | "The sidebar displays department names." | "The sidebar will display department names." |
| Past tense for completed actions | "You approved three tasks." | "You have approved three tasks." |

### 1.2 Tone Calibration

- **Instructions**: Direct and imperative. "Select **Settings**." not "You might want to consider selecting Settings."
- **Explanations**: Calm and factual. Avoid hedging ("should", "might", "could potentially").
- **Warnings**: Urgent but not alarmist. State the consequence, then the mitigation.
- **Tips**: Helpful and concise. Lead with the benefit.

### 1.3 Terminology Discipline

Use the canonical term on first mention in every section. Subsequent mentions may use abbreviations if defined. Never invent terminology — if a term is not in the [Glossary](#9-glossary-convention), add it there first.

---

## 2. Formatting Conventions

### 2.1 Heading Hierarchy

The guide follows a strict four-level heading hierarchy. Never skip a level.

| Level | Markdown | Usage | Example |
|-------|----------|-------|---------|
| 1 | `#` | Document title — one per file | `# CEO Dashboard User Guide` |
| 2 | `##` | Major sections | `## Getting Started` |
| 3 | `###` | Sub-sections within a major section | `### Navigating the Dashboard` |
| 4 | `####` | Detail areas within a sub-section | `#### Filtering by Department` |

> ⚠️ **Warning**: Heading level 5 (`#####`) is **prohibited**. If you find you need it, restructure the content into separate sub-sections.

### 2.2 Inline Formatting

| Element | Format | Example |
|---------|--------|---------|
| UI element names (buttons, menus, tabs, fields, links) | **Bold** | Click **Approve**. Select the **Tasks** tab. |
| Technical values (env vars, ports, commands, file paths, API routes) | `Code font` | Set `DASHBOARD_PORT` to `8420`. |
| Keys and keyboard shortcuts | `Code font` | Press `Ctrl + K` to open the command bar. |
| File names | `Code font` | Edit `company-registry.yaml`. |
| New terms (first use only) | **Bold**, then link to glossary | The **Org Health Score** ([see Glossary](#9-glossary-convention)). |
| Emphasis (sparingly) | *Italic* | This setting is *permanent* and cannot be undone. |

### 2.3 Blockquotes — Callouts

Use blockquotes with emoji prefixes for callouts. Always place a blank line after the callout opening.

#### Tips

```markdown
> 💡 **Tip**: You can pin frequently used filters to the sidebar for faster access.
```

> 💡 **Tip**: You can pin frequently used filters to the sidebar for faster access.

#### Warnings

```markdown
> ⚠️ **Warning**: Rejecting an approval request is irreversible. Confirm with your team before proceeding.
```

> ⚠️ **Warning**: Rejecting an approval request is irreversible. Confirm with your team before proceeding.

#### Notes

```markdown
> 📝 **Note**: The dashboard refreshes KPI data every 60 seconds by default. This interval is configurable via `KPI_REFRESH_INTERVAL`.
```

> 📝 **Note**: The dashboard refreshes KPI data every 60 seconds by default. This interval is configurable via `KPI_REFRESH_INTERVAL`.

### 2.4 Tables

- Every table **must** have a header row.
- Align columns for readability in source markdown (pipe alignment is optional but encouraged).
- Use tables for structured data: option lists, parameter references, state enumerations, and comparison matrices.
- Do not use tables for narrative text or multi-paragraph explanations.

### 2.5 Code Blocks

- Every fenced code block **must** specify a language.
- Use `bash` for shell commands, `python` for Python, `json` for JSON payloads, `yaml` for YAML config, `javascript` for frontend code.
- Include a one-line comment or label above non-trivial code blocks when context is needed.

```markdown
\`\`\`bash
ai-company dashboard start --port 8421
\`\`\`
```

### 2.6 Lists

- Use **numbered lists** for sequential steps or ranked items.
- Use **bullet lists** for unordered collections.
- Indent nested lists by two spaces.
- Keep list items to one sentence where possible. If an item requires explanation, follow it with a paragraph rather than nesting deeper.

---

## 3. Diagram Specifications

The CEO Dashboard User Guide requires the following diagrams. Each is specified here for a diagram author or tool to produce. Diagrams should use a dark-background palette consistent with the JARVIS theme (dark grays, neon cyan/green accents, muted borders).

### 3.1 Navigation Flow Diagram

**Purpose**: Show the user how the dashboard navigation is structured — from sidebar to pages to command bar.

**Components**:

```
┌──────────────────┐     ┌─────────────────────┐     ┌──────────────────┐
│     Sidebar       │────▶│      Page Area       │────▶│   Command Bar    │
│                   │     │                      │     │   (Ctrl + K)     │
│  ├─ Dashboard     │     │  ┌────────────────┐  │     │                  │
│  ├─ Agents        │     │  │ Page Content   │  │     │  Search tasks    │
│  ├─ Tasks         │     │  │ (KPIs, tables, │  │     │  Jump to agent   │
│  ├─ Approvals     │     │  │  charts)       │  │     │  Open settings   │
│  ├─ Escalations   │     │  └────────────────┘  │     │                  │
│  ├─ KPIs          │     │                      │     └──────────────────┘
│  ├─ Costs         │     └─────────────────────┘
│  └─ Settings      │
└──────────────────┘
```

**Label each node** with its page name. Show directional arrows for navigation paths. Include the keyboard shortcut for the command bar.

### 3.2 KPI Hierarchy Diagram

**Purpose**: Show how the Org Health Score is composed from its four component metrics and their source data.

**Components**:

```
┌─────────────────────────────────────────────────────────────┐
│                   ORG HEALTH SCORE                          │
│                     (composite)                              │
│                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────┐ ┌────────┐ │
│  │ Task Success  │ │Agent Utiliz. │ │Cost      │ │Error   │ │
│  │ Rate (30%)   │ │    (25%)     │ │Eff.(25%) │ │Rate    │ │
│  │              │ │              │ │          │ │ (20%)  │ │
│  │ ─ source ──▶ │ │ ─ source ──▶ │ │─ source▶ │ │─ src─▶ │ │
│  │ inbox.json   │ │ registry +   │ │ cost log │ │audit   │ │
│  │              │ │ task complet.│ │          │ │trail   │ │
│  └──────────────┘ └──────────────┘ └──────────┘ └────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Show**: the composite score at top, four component boxes with weights, and source data feeds beneath each component.

### 3.3 Authentication Flow Diagram

**Purpose**: Trace the full authentication lifecycle from login through API request authorization.

**Sequence**:

```
User ──▶ Dashboard Login Page ──▶ POST /api/v1/auth/login
         (credentials)              │
                                    ▼
                              Validate API Key
                              (X-API-Key header)
                                    │
                          ┌─────────┴──────────┐
                          │                    │
                       Valid               Invalid
                          │                    │
                          ▼                    ▼
                   Issue Session Token    401 Unauthorized
                   (JWT / cookie)
                          │
                          ▼
                   API Request + Token
                          │
                          ▼
                   RBAC Check
                   (admin / approve / run)
                          │
                   ┌──────┴──────┐
                   │             │
                Granted       Denied
                   │             │
                   ▼             ▼
              200 OK        403 Forbidden
```

**Show**: each step as a labeled box, decision points as diamonds or branching paths, and the three RBAC roles (admin, approve, run) as labels on the RBAC check node.

### 3.4 Task Lifecycle Diagram

**Purpose**: Map every task state and every valid transition between them.

**States and transitions**:

```
┌───────────┐     ┌───────────┐     ┌──────────────┐
│  Backlog   │────▶│   Ready   │────▶│ In Progress  │
└───────────┘     └───────────┘     └──────┬───────┘
                        ▲                    │
                        │              ┌─────┴─────┐
                        │              │           │
                   ┌────┴────┐    ┌────▼────┐ ┌───▼────┐
                   │ Reopened│    │ Review  │ │ Failed │
                   └─────────┘    └────┬────┘ └───┬────┘
                                       │           │
                                       ▼           ▼
                                  ┌─────────┐ ┌─────────┐
                                  │  Done   │ │ Escalated│
                                  └─────────┘ └────┬────┘
                                                    │
                                                    ▼
                                              ┌──────────┐
                                              │ Resolved │
                                              └──────────┘
```

**Label each transition arrow** with the action that triggers it (e.g., "assign", "submit for review", "approve", "reject", "escalate").

### 3.5 Escalation Flow Diagram

**Purpose**: Show the escalation lifecycle from trigger through resolution.

**Components**:

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Trigger      │────▶│  Escalation      │────▶│  Review Queue   │
│               │     │  Queue           │     │                 │
│ • Task fails  │     │  (.opencode/     │     │  Dashboard UI   │
│ • Timeout     │     │   escalations/)  │     │  /escalations   │
│ • Agent error │     │                  │     │                 │
│ • HITL block  │     │  Sorted by       │     │  CEO reviews    │
└──────────────┘     │  severity + time │     │  and decides    │
                      └──────────────────┘     └────────┬────────┘
                                                        │
                                                  ┌─────┴──────┐
                                                  │            │
                                                  ▼            ▼
                                            ┌──────────┐ ┌──────────┐
                                            │ Resolved │ │ Reassigned│
                                            └──────────┘ └──────────┘
```

**Show**: the three trigger categories, the queue mechanism, the review step, and the two resolution outcomes.

### 3.6 WebSocket Architecture Diagram

**Purpose**: Illustrate the real-time data flow between client and server via WebSocket.

**Components**:

```
┌──────────────────────┐                    ┌──────────────────────┐
│      CLIENT           │    WebSocket       │      SERVER          │
│   (Browser)           │◀══════════════════▶│   (FastAPI + ws.py)  │
│                       │   ws://host/ws/v1  │                      │
│  ┌─────────────────┐  │                    │  ┌────────────────┐  │
│  │ Alpine.js Store  │  │  subscribe        │  │ Topic Manager  │  │
│  │ (x-data)        │──┼───────────────────▶│  │                │  │
│  └─────────────────┘  │                    │  │ Topics:        │  │
│                       │  ◀────────────────┼──│  • kpi_update   │  │
│  ┌─────────────────┐  │  broadcast        │  │  • alert        │  │
│  │ Reactive UI      │  │                    │  │  • task_update  │  │
│  │ (auto-update)    │  │                    │  │  • escalation   │  │
│  └─────────────────┘  │                    │  │  • org_health   │  │
└──────────────────────┘                    └──────────────────────┘
```

**Show**: bidirectional data flow, the subscribe/unsubscribe model, all five topic names, and the reactive update loop on the client.

---

## 4. Accessibility Requirements

Every section of the CEO Dashboard User Guide must meet the following accessibility standards. These are non-negotiable.

### 4.1 Images and Diagrams

- Every image, diagram, and screenshot **must** include descriptive alt text.
- Alt text should describe the content and purpose of the image, not its appearance.
- Alt text format: `[Image: <description of what the image shows and why it matters>]`

**Example**:
```markdown
![Org Health Score dashboard showing a gauge at 82 with four component cards](path/to/image.png)
```
*Alt text: "The Org Health Score gauge displays 82 in the green band, with four component cards below showing Task Success Rate at 72%, Agent Utilization at 85%, Cost Efficiency at 68%, and Error Rate at 91%."*

### 4.2 Heading Hierarchy

- Heading levels must be **sequential** — never skip from `##` to `####`.
- Every section must have at least one `##` heading.
- Every `####` heading must have a parent `###` heading.

### 4.3 Color and Visual Indicators

- **Color is never the sole indicator** of meaning. Always pair color with text labels, icons, or symbols.
- When describing status bands (green, yellow, red), always include the text equivalent: "green band (healthy)".
- Dashboard tables must use both color badges **and** text status labels.

**Example**:
```markdown
> ⚠️ **Warning**: The status indicator shows both a colored badge and a text label.
> Never reference only the color — always include the text.
```

### 4.4 Tables

- All tables **must** have a header row.
- Tables must not be used for layout purposes — only for structured data.
- For complex tables, provide a brief introductory sentence explaining what the table contains.

### 4.5 Code Blocks

- Every fenced code block **must** specify a language for syntax highlighting.
- Screen readers and assistive technologies use the language hint to provide appropriate context.

---

## 5. Screenshot Placeholders

Screenshots are critical for a visual dashboard guide. Use the following convention to mark locations where screenshots should be added. This allows the document structure to be finalized before visual assets are produced.

### 5.1 Syntax

```markdown
[Screenshot: <description> — <page or feature>]
```

### 5.2 Rules

- The description should be specific enough that a screenshot author can capture the correct view.
- Place the placeholder on its own line, centered between the paragraphs it illustrates.
- After the screenshot is added, replace the placeholder with a standard markdown image reference.
- Never leave a placeholder in a published section without at least a TODO comment.

### 5.3 Examples

```markdown
[Screenshot: Full dashboard overview with Org Health Score gauge and four KPI cards — Dashboard Home]

[Screenshot: Task board filtered to "In Progress" status with three agent columns — Tasks Tab]

[Screenshot: Escalation detail panel showing trigger context and resolution options — Escalations Tab]

[Screenshot: Settings page with environment variable configuration fields — Settings Page]

[Screenshot: Command bar open with search results for "approval" — Command Bar (Ctrl+K)]
```

### 5.4 Screenshot Naming Convention

When screenshots are added, name them descriptively:

```
dashboard-home-overview.png
tasks-tab-filtered.png
escalation-detail-panel.png
settings-env-config.png
command-bar-search.png
```

Use lowercase, hyphen-separated names. Prefix with the page or feature name.

---

## 6. Cross-Reference Conventions

Cross-references link related content across sections of the guide. They improve navigability and reduce duplication.

### 6.1 Format

Use the standard markdown link format with an anchor target:

```markdown
[Section Name](#section-anchor)
```

### 6.2 Anchor Generation Rules

Anchors are derived from the section heading, lowercased, with spaces replaced by hyphens:

| Heading | Anchor |
|---------|--------|
| `## Getting Started` | `#getting-started` |
| `### Navigating the Dashboard` | `#navigating-the-dashboard` |
| `#### Filtering by Department` | `#filtering-by-department` |

### 6.3 Link Text

- Link text should be the **section name** — not "click here" or "see above".
- For links to other files in the guide, include the file name in parentheses:

```markdown
See [Diagram Specifications](08-documentation-standards.md#3-diagram-specifications) for details.
```

### 6.4 External Links

- Link to external documentation (FastAPI, Alpine.js, Chart.js, Tailwind) only when the reader needs to go deeper than the guide covers.
- Always use HTTPS URLs.
- Open external links in a new tab (if rendering supports it): `[FastAPI docs](https://fastapi.tiangolo.com/){:target="_blank"}`.

### 6.5 Rules

- Do not create circular references.
- Every cross-reference must resolve — never link to a section that does not exist yet.
- If a section is planned but not yet written, add a `TODO` comment instead of a broken link.

---

## 7. Version History

Track every substantive change to the User Guide in the version history table below. A "substantive change" is any edit that affects content, accuracy, or structure — not typo fixes or whitespace.

### 7.1 Format

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-08-26 | Technical Documentation Lead | Initial Documentation Standards appendix. Defined voice/tone, formatting, diagrams, accessibility, screenshots, cross-references, glossary convention, and contribution guide. |

### 7.2 Rules

- Version numbers follow [Semantic Versioning](https://semver.org/): `vMAJOR.MINOR.PATCH`.
  - **Major**: Breaking changes to section structure or removal of sections.
  - **Minor**: New sections, new diagrams, expanded content.
  - **Patch**: Corrections, clarifications, typo fixes.
- Date format: `YYYY-MM-DD`.
- Author: Use the role title or agent name — not a personal name.
- Changes: One sentence per change, beginning with a verb (Added, Updated, Removed, Fixed, Clarified).

---

## 8. Contributing to This Guide

This section describes how anyone — human or agent — can contribute to the CEO Dashboard User Guide.

### 8.1 How to Suggest an Edit

1. **Open a pull request** against the repository with your proposed change.
2. In the PR description, state:
   - Which section you are editing.
   - What the change is and why it is needed.
   - Whether the change affects other sections (cross-reference audit).
3. The Technical Documentation Lead reviews the PR for adherence to this standards document.

### 8.2 How to Add a New Section

1. **Check the Table of Contents** in the target file. Ensure the new section fits the existing structure.
2. **Follow the heading hierarchy** — do not create orphaned `###` or `####` headings.
3. **Add a version history entry** in both the new file's version table and any parent guide's version table.
4. **Update all cross-references** that may be affected.
5. **Run the ECL lint check** before submitting: `pwsh scripts/lint-ecl.ps1`.

### 8.3 How to Report an Error

1. **Open a GitHub issue** with the label `documentation`.
2. Include:
   - The file name and section heading.
   - The incorrect text (quote it exactly).
   - The correct information, with a source link if available.
3. For urgent accuracy issues (wrong port number, incorrect API endpoint, security-relevant error), tag the Technical Documentation Lead directly.

### 8.4 How to Add a Screenshot

1. Capture the screenshot using the JARVIS-themed dashboard (dark background, neon accents).
2. Follow the [screenshot naming convention](#54-screenshot-naming-convention).
3. Place images in the `docs/ceo-dashboard-user-guide/images/` directory.
4. Replace the corresponding `[Screenshot: ...]` placeholder with a standard markdown image reference.
5. Verify the alt text meets the [accessibility requirements](#41-images-and-diagrams).

### 8.5 Review Checklist

Before submitting a PR that modifies this guide, verify:

- [ ] Heading hierarchy is sequential (no skipped levels).
- [ ] All code blocks specify a language.
- [ ] All tables have header rows.
- [ ] Bold is used for UI elements, code font for technical values.
- [ ] Callouts use the correct emoji prefix (💡, ⚠️, 📝).
- [ ] Cross-references resolve to existing sections.
- [ ] Version history is updated.
- [ ] Screenshots have descriptive alt text.
- [ ] No color is used as a sole indicator.

---

## 9. Glossary Convention

The CEO Dashboard uses domain-specific terminology that must be consistent across all sections. This section defines the convention for how terms are managed.

### 9.1 Single Definition, Multiple References

- Every glossary term is defined **once**, in the Glossary section of the User Guide.
- All other sections reference the glossary definition by linking to it — they do **not** redefine the term.
- On first mention in a section, the term should be bolded and linked to the glossary.

**Example**:
```markdown
The **Org Health Score** ([see Glossary](#glossary)) is a weighted composite of four metrics.
```

### 9.2 Adding a New Term

1. Verify the term is not already defined in the Glossary.
2. Add the term in **alphabetical order** within the Glossary table.
3. Provide a one-sentence definition suitable for a non-technical reader.
4. Include the technical implementation detail in parentheses if relevant.
5. Update the Table of Contents if the Glossary section has moved.

### 9.3 Glossary Table Format

| Term | Definition |
|------|------------|
| **Approval Gate** | A human-in-the-loop checkpoint that requires explicit CEO approval before an agent action proceeds. Implemented via `orchestrator/approvals.yaml`. |
| **Command Bar** | A keyboard-activated search overlay (`Ctrl + K`) for quick navigation to pages, agents, and tasks. |
| **Escalation** | An issue that exceeds an agent's authority or capability and is routed to the CEO for resolution. Stored in `.opencode/inbox.json` with status `escalated`. |
| **JARVIS Theme** | The dashboard's dark visual theme — dark gray backgrounds with neon cyan and green accents. Defined in the Tailwind config and `style.css`. |
| **KPI** | Key Performance Indicator — a quantified metric used to measure department or organizational health. |
| **Org Health Score** | A composite score (0–100) aggregating task success rate, agent utilization, cost efficiency, and error rate into a single organizational health metric. Band: green (≥80), yellow (60–79), red (<60). |
| **RBAC** | Role-Based Access Control — the permission model for the dashboard. Three roles: `admin` (full access), `approve` (approve/reject tasks), `run` (execute tasks, read KPIs). |
| **Task** | A unit of work assigned to an agent, tracked through a lifecycle from backlog to done. Stored in `.opencode/inbox.json`. |
| **Topic** | A named WebSocket channel for real-time data push. Clients subscribe to topics (e.g., `kpi_update`, `alert`, `task_update`). |

### 9.4 Rules

- Definitions must be **stable** — do not change a term's meaning without updating every section that references it.
- Do not use acronyms in definitions without first spelling them out.
- If a term has both a business meaning and a technical meaning, lead with the business definition and add the technical detail second.
- When a term appears in a diagram label, use the bold form (e.g., **Org Health Score**) not the code form.

---

*This standards document is maintained by the Technical Documentation Lead. All sections of the CEO Dashboard User Guide must conform to the conventions defined here. When in doubt, refer to this appendix.*
