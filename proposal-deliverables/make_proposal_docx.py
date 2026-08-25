"""Generate the Technical & Financial Proposal (.docx) for the Digital Health Consultant engagement.

Run:  uv run --with python-docx python proposal-deliverables/make_proposal_docx.py
"""

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor

TEAL = RGBColor(0x0E, 0x5A, 0x66)
DARK = RGBColor(0x1C, 0x3B, 0x42)
CORAL = RGBColor(0xE8, 0x70, 0x3A)
GREY = RGBColor(0x5A, 0x6B, 0x6E)

doc = Document()

# ---------- base styles ----------
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(10.5)
normal.font.color.rgb = DARK
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.line_spacing = 1.15

for name, size in (("Heading 1", 16), ("Heading 2", 13), ("Heading 3", 11.5)):
    st = doc.styles[name]
    st.font.name = "Calibri"
    st.font.size = Pt(size)
    st.font.bold = True
    st.font.color.rgb = TEAL
    st.paragraph_format.space_before = Pt(14 if size > 13 else 10)
    st.paragraph_format.space_after = Pt(4)

sec = doc.sections[0]
sec.top_margin = sec.bottom_margin = Cm(2.2)
sec.left_margin = sec.right_margin = Cm(2.4)


def para(text="", bold=False, italic=False, color=None, size=None, align=None, space_after=None):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold, r.italic = bold, italic
    if color:
        r.font.color.rgb = color
    if size:
        r.font.size = Pt(size)
    if align:
        p.alignment = align
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    return p


def bullets(items, style="List Bullet"):
    for it in items:
        doc.add_paragraph(it, style=style)


def table(headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Light Grid Accent 1"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        r = hdr[i].paragraphs[0].add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            r = cells[i].paragraphs[0].add_run(str(v))
            r.font.size = Pt(9.5)
    if widths:
        for i, w in enumerate(widths):
            for row in t.rows:
                row.cells[i].width = Cm(w)
    return t


# ================= COVER PAGE =================
for _ in range(5):
    doc.add_paragraph()
para(
    "TECHNICAL & FINANCIAL PROPOSAL",
    bold=True,
    color=CORAL,
    size=13,
    align=WD_ALIGN_PARAGRAPH.CENTER,
    space_after=12,
)
para(
    "Consultant, Digital Health — ACHIEVE Project",
    bold=True,
    color=DARK,
    size=26,
    align=WD_ALIGN_PARAGRAPH.CENTER,
    space_after=8,
)
para(
    "Technical Architecture & Costed Roadmap for MaHIS–iCHIS Integration\n"
    "to Improve Maternal and Newborn Health Outcomes",
    color=TEAL,
    size=14,
    align=WD_ALIGN_PARAGRAPH.CENTER,
    space_after=36,
)

info = [
    ("Client", "Last Mile Health / Ministry of Health and Sanitation, Malawi"),
    ("Assignment Location", "Lilongwe, Malawi — MoH Digital Health Division"),
    ("Engagement Period", "Mid-August 2026 – 30 September 2026 (approx. 6.5 weeks)"),
    ("Professional Fees", "USD 3,000 – 4,000 per month"),
    (
        "Reporting Line",
        "Digital Health Specialist, Last Mile Health; technical coordination with Head, Systems Architecture & Security Unit, MoH Digital Health Division",
    ),
    ("Proposal Date", "August 2026"),
]
t = table(["Item", "Detail"], info, widths=[5.2, 10.6])
doc.add_page_break()

# ================= 1 EXECUTIVE SUMMARY =================
doc.add_heading("1. Executive Summary", level=1)
para(
    "This proposal responds to Last Mile Health's requirement for a Digital Health Consultant under the "
    "ACHIEVE Project to design the technical architecture and costed roadmap for integrating Malawi's "
    "facility-level health information system (MaHIS) with the Integrated Community Health Information "
    "System (iCHIS). The integration directly supports ACHIEVE Objective 3 — strengthening health systems "
    "through improved data use for decision-making — and Strategic Objective 1: enhancing iCHIS functionality "
    "and enabling secure, reliable data exchange for better maternal and newborn health (MNH) outcomes."
)
para(
    "The engagement will be delivered over approximately 6.5 weeks from within the Ministry of Health and "
    "Sanitation's Digital Health Division in Lilongwe, ensuring day-to-day access to system owners, technical "
    "teams and governance structures. The consultant will produce five deliverables: an Inception Report; a "
    "Technical Architecture & Requirements Document; a Costed Implementation Roadmap structured around four "
    "investment pillars (People, Platforms, Process, Time-to-Value); a Risk Analysis & Mitigation Plan; and a "
    "consolidated donor-ready Final Roadmap Package with presentation."
)
para(
    "The proposed approach combines rapid discovery (stakeholder interviews, district site visits, document "
    "review), participatory design workshops with MoH units and vendors, rigorous requirements engineering "
    "aligned to national digital health architecture and FHIR/OpenHIE standards, and transparent costing "
    "benchmarked against comparable LMIC digital health investments. The final package is designed to serve "
    "as an investment case for government and development partners, with clear phasing, sustainability "
    "pathways and risk mitigation.",
)

# ================= 2 BACKGROUND =================
doc.add_heading("2. Background & Context", level=1)
doc.add_heading("2.1 The ACHIEVE Project", level=2)
para(
    "ACHIEVE is a US Department of State–funded initiative implemented by Pact and partners in Malawi to "
    "accelerate sustainable reductions in maternal, neonatal and child mortality by improving access to, "
    "quality of, and continuity of care across pregnancy, childbirth, postnatal and early childhood services. "
    "The grant operates in Karonga, Balaka, Thyolo and Zomba districts, with Last Mile Health leading "
    "iCHIS-driven interventions in Balaka."
)
doc.add_heading("2.2 The Integration Challenge", level=2)
para(
    "Malawi operates two parallel health information ecosystems: MaHIS at facility/national level and iCHIS "
    "at community level. Today, community-generated MNH data (antenatal contacts, danger-sign referrals, "
    "postnatal visits) is captured separately, entered manually into national reporting, and reconciled with "
    "difficulty. The consequences are duplicate data entry, delayed and incomplete reporting, weak referral "
    "closure, and limited visibility of the full continuum of MNH care — precisely the gaps that undermine "
    "data-driven decision-making at national and district levels."
)
doc.add_heading("2.3 Why Now", level=2)
bullets(
    [
        "ACHIEVE provides a funded window to design integration properly rather than retrofit it later.",
        "National digital health strategy and governance structures are mature enough to anchor interoperability decisions.",
        "Community health worker capacity building in Balaka (Strategic Objective 2) will multiply data volumes — integration must precede scale.",
    ]
)

# ================= 3 UNDERSTANDING =================
doc.add_heading("3. Understanding of the Assignment", level=1)
para(
    "The assignment is a design-and-planning consultancy, not a software build. Its products are decision-grade "
    "artefacts: a technically validated architecture, a costed phased roadmap, a risk plan and a donor-ready "
    "package that MoH and partners can act upon immediately."
)
table(
    ["Dimension", "Understanding"],
    [
        [
            "Systems",
            "MaHIS (facility/HMIS) and iCHIS (community), with DHIS2 as the national analytics backbone",
        ],
        [
            "Scope of exchange",
            "CHW registrations, service delivery data, stock/commodity data, MNH indicators; unidirectional or bidirectional flows determined during inception",
        ],
        [
            "Priority use cases",
            "Automatic submission of CHW monthly summaries into HMIS; two-way referral tracking; consolidated MNH dashboards",
        ],
        [
            "Standards frame",
            "National digital health architecture and governance standards; HL7 FHIR, OpenHIE profiles, DHIS2 data model",
        ],
        [
            "Constraints",
            "~6.5-week window; USD 3–4k/month fee envelope; co-location in Lilongwe; Malawian national consultant",
        ],
    ],
    widths=[4.2, 11.6],
)

# ================= 4 APPROACH =================
doc.add_heading("4. Technical Approach & Methodology", level=1)
doc.add_heading("4.1 Guiding Principles", level=2)
bullets(
    [
        "Government-first: every artefact co-created with MoH units so ownership transfers on day one.",
        "Standards-based: prefer FHIR/OpenHIE-conformant patterns over bespoke point solutions.",
        "Evidence-led: current-state claims verified through site observation and vendor documentation.",
        "Cost honesty: budgets benchmarked, CAPEX/OPEX split, recurrent-cost ownership explicit.",
        "Design for donors: package structured to drop into Global Fund / USAID concept-note templates.",
    ]
)
doc.add_heading("4.2 Methodological Steps", level=2)
table(
    ["Step", "Method", "Output"],
    [
        [
            "Discovery",
            "Document review, 8–10 stakeholder interviews, 2 district site visits, vendor technical sessions",
            "Validated current-state assessment",
        ],
        [
            "Architecture design",
            "Options analysis (point-to-point vs middleware vs file-based), pattern selection workshop with MoH Interop team",
            "Endorsed integration architecture",
        ],
        [
            "Requirements engineering",
            "FR/NFR workshops, data mapping matrix, OpenAPI 3.0 draft spec, security & compliance review",
            "Technical Requirements Document",
        ],
        [
            "Roadmap & costing",
            "Four-phase plan; line-item costing across People/Platforms/Process/TTV pillars; donor mapping",
            "Costed Implementation Roadmap",
        ],
        [
            "Risk & consolidation",
            "P×I risk workshop; mitigation planning; executive summary and deck assembly",
            "Risk Plan + Final Package + Presentation",
        ],
    ],
    widths=[3.4, 7.6, 4.8],
)
doc.add_heading("4.3 Proposed Integration Pattern (indicative)", level=2)
para(
    "Based on regional experience, the recommended starting hypothesis is a mediated integration using an "
    "OpenHIE-aligned interoperability layer (e.g., OpenHIM) exposing FHIR APIs between iCHIS and MaHIS, with "
    "aggregate flows pushed to DHIS2. File-based exchange remains the documented fallback where API readiness "
    "is limited. This hypothesis will be confirmed or revised during Weeks 3–4 against vendor capability, "
    "infrastructure and governance findings."
)

# ================= 5 WORK PLAN =================
doc.add_heading("5. Work Plan & Timeline", level=1)
para(
    "The engagement runs approximately 6.5 weeks (mid-August to 30 September 2026) across seven phases, each "
    "closing with a formal quality checkpoint."
)
table(
    ["Phase", "Weeks", "Focus", "Gate"],
    [
        ["0 Pre-engagement", "W-1", "Access, document library, tooling, calendar", "—"],
        [
            "1 Inception & Discovery",
            "W1–2",
            "Kick-off, interviews, 2 district site visits, discovery synthesis",
            "CP1/CP2: Inception sign-off",
        ],
        [
            "2 Architecture & Requirements",
            "W3–4",
            "Pattern selection, FR/NFR workshops, data mapping, API spec draft",
            "CP4: Requirements sign-off",
        ],
        [
            "3 Roadmap & Costing",
            "W5–6",
            "Phasing, 4-pillar costing, donor alignment, validation workshop",
            "CP5: Roadmap sign-off",
        ],
        [
            "4 Risk & Final Package",
            "W7",
            "Risk workshop, package assembly, deck, handover, close-out",
            "CP7: Formal acceptance",
        ],
    ],
    widths=[4.4, 1.8, 7.0, 2.6],
)
para(
    "Detailed day-level activities, stakeholder time commitments, and the zero-float critical path are set out "
    "in the accompanying Project Plan document (project-plan-digital-health-consultant.md).",
    italic=True,
    color=GREY,
)

# ================= 6 DELIVERABLES =================
doc.add_heading("6. Deliverables & Acceptance Criteria", level=1)
table(
    ["#", "Deliverable", "Due", "Key acceptance criteria"],
    [
        [
            "D1",
            "Inception Report",
            "End W2",
            "Scope/RACI/workplan signed off; ≥10 risks logged; repository live",
        ],
        [
            "D2",
            "Technical Architecture & Requirements Document",
            "End W4",
            "Current state validated; integration pattern endorsed; ≥30 FRs, ≥15 measurable NFRs; OpenAPI 3.0 draft; compliance matrix",
        ],
        [
            "D3",
            "Costed Implementation Roadmap",
            "End W6",
            "4 phases with gates; monthly costing by pillar & org; CAPEX/OPEX; donor matrix; sustainability pathway",
        ],
        [
            "D4",
            "Risk Analysis & Mitigation Plan",
            "W7",
            "≥20 risks across 4 categories; full mitigations for High/Medium; monitoring cadence",
        ],
        [
            "D5",
            "Final Roadmap Package & Presentation",
            "30 Sep",
            "Executive summary ≤2pp; all docs integrated; annexes; 20-slide donor deck; formal sign-off",
        ],
    ],
    widths=[1.0, 5.2, 1.8, 7.8],
)

# ================= 7 RISK =================
doc.add_heading("7. Risk Management", level=1)
table(
    ["ID", "Risk", "P×I", "Mitigation"],
    [
        [
            "R1",
            "MoH staff availability constrained by competing priorities",
            "High",
            "Pre-booked calendars; sponsor escalation; flexible scheduling",
        ],
        [
            "R2",
            "Vendor API access/sandbox delayed",
            "Med-High",
            "Early MoH directive to vendors; contractual clauses; file-exchange fallback",
        ],
        [
            "R4",
            "Scope creep beyond MNH integration core",
            "Medium",
            "Inception baseline; change-control board",
        ],
        [
            "R5",
            "Donor funding misaligned with phased roadmap",
            "Medium-High",
            "Donor mapping in W6; modular phasing enabling partial funding",
        ],
        [
            "R7",
            "Security/compliance gaps block future deployment",
            "Low-Critical",
            "Early MoH ICT security review; privacy-by-design; DPA templates",
        ],
    ],
    widths=[1.2, 6.4, 2.0, 6.2],
)
para(
    "A living risk register with owners, triggers and weekly review cadence is maintained throughout the "
    "engagement; High residual risks escalate to the Steering Committee."
)

# ================= 8 BUDGET =================
doc.add_heading("8. Budget & Fees", level=1)
para(
    "Professional fees are quoted at USD 3,500 per month, within the advertised USD 3,000–4,000 band, "
    "totaling approximately USD 5,400 for the 6.5-week engagement. Indicative reimbursables:"
)
table(
    ["Category", "Est. USD"],
    [
        ["Consultant fees (6.5 wks @ $3,500/mo)", "5,400"],
        ["Local travel — 2 district visits", "400"],
        ["Workshops (venue, refreshments × 4)", "300"],
        ["Communications/internet", "150"],
        ["Printing & stationery", "100"],
        ["Contingency (~10%)", "635"],
        ["Total estimated", "6,985"],
    ],
    widths=[11.0, 3.0],
)
para(
    "All costs exclude taxes withheld per applicable law; reimbursables are payable against receipts and "
    "prior written approval."
)

# ================= 9 QUALIFICATIONS =================
doc.add_heading("9. Consultant Qualifications", level=1)
bullets(
    [
        "Degree in health informatics, computer science or public health, with progressive experience designing and costing digital health system integrations in LMIC settings.",
        "Hands-on experience with national health information systems (DHIS2, OpenMRS, CommCare, ODK, iCHIS-class platforms).",
        "Working knowledge of interoperability standards (HL7 FHIR, OpenHIE) and API design.",
        "Demonstrated data-governance experience: data sharing agreements, privacy/security requirements, donor compliance.",
        "Proven costing and budgeting for digital health programmes prepared for Global Fund, USAID, Gavi and World Bank audiences.",
        "Track record facilitating multi-stakeholder MoH consultations and building consensus across government, partners and vendors.",
        "Excellent written and verbal English; skilled at translating technical concepts for non-technical audiences.",
    ]
)

# ================= 10 GOVERNANCE =================
doc.add_heading("10. Governance, Reporting & Quality Assurance", level=1)
bullets(
    [
        "Daily stand-up with LMH Technical Lead and MoH counterpart; weekly written status report each Friday.",
        "Bi-weekly Steering Committee for strategic decisions and barrier removal.",
        "Seven formal quality checkpoints (CP1–CP7) with defined go/no-go criteria before any phase transition.",
        "Version control (draft → review → FINAL) and peer review prior to all formal submissions.",
        "Traceability matrix linking functional requirements → architecture → roadmap → costs → risks.",
    ]
)

# ================= 11 SUSTAINABILITY =================
doc.add_heading("11. Sustainability & Handover", level=1)
bullets(
    [
        "Complete handover pack: editable sources, costing model, risk register, API specs, decision register.",
        "Four knowledge-transfer sessions (architecture walkthrough, costing deep-dive, risk handover, donor dry-run).",
        "Sustainability mechanisms embedded in the roadmap: MoH ownership board, technical working group, budget-absorption tracking, vendor SLAs, annual roadmap review.",
        "Success test: the MoH lead can present the roadmap accurately without the consultant present.",
    ]
)

doc.add_paragraph()
para("Submitted by: [Consultant Name] — Lilongwe, Malawi — August 2026", italic=True, color=GREY)

out = "proposal-deliverables/Digital-Health-Consultant-Proposal.docx"
doc.save(out)
print("saved:", out)
