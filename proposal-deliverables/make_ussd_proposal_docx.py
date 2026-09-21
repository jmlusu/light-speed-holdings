"""Generate the Technical & Financial Proposal (.docx) for the VillageReach USSD Consultant engagement.

Run:  uv run --with python-docx python proposal-deliverables/make_ussd_proposal_docx.py

Last updated: 2026-09-18
"""

# Last generated: 2026-09-18 01:37:52
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor

OUT = Path("Jack-Mlusu-Solo-Consultant-Proposal.docx")

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


def monospace(text, size=None):
    """Render a USSD-style wireframe block in a monospaced font."""
    p = doc.add_paragraph()
    for line in text.splitlines():
        if line:
            r = p.add_run(line)
            r.font.name = "Consolas"
        else:
            p.add_run(" ")
        p.add_run().add_break()
    if size:
        for run in p.runs:
            run.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(10)
    return p


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
    "USSD Consultant — CHOICE Project",
    bold=True,
    color=DARK,
    size=26,
    align=WD_ALIGN_PARAGRAPH.CENTER,
    space_after=8,
)
para(
    "Design, Deployment & 24-Month Managed Service of an SRHR Information and Feedback\n"
    "Service on Short Code 54747 (Malawi)",
    color=TEAL,
    size=14,
    align=WD_ALIGN_PARAGRAPH.CENTER,
    space_after=36,
)

info = [
    ("Client", "VillageReach — CHOICE Project"),
    (
        "Assignment Location",
        "Lilongwe and Balaka, Malawi (service nationwide via short code 54747)",
    ),
    ("Engagement Period", "4-week setup (Weeks 1–4) + 24 months of managed service"),
    ("Professional Fees", "USD 45,000 total across the 24-month engagement"),
    (
        "Reporting Line",
        "VillageReach CHOICE Project team; technical coordination with TNM, Airtel and the data warehouse owner",
    ),
    ("Proposal Date", "2026-09-17"),
]
t = table(["Item", "Detail"], info, widths=[5.2, 10.6])
doc.add_page_break()

# ================= 1 EXECUTIVE SUMMARY =================
doc.add_heading("1. Executive Summary", level=1)
para(
    "This proposal responds to VillageReach's requirement for a USSD Consultant to design, deploy and manage "
    "a USSD module on short code 54747 that delivers sexual and reproductive health and rights (SRHR) "
    "information and a structured feedback channel for low-literacy users in Malawi under the CHOICE Project."
)
para(
    "Light Speed Holdings — led by Jack Mlusu (USSD Consultant) and backed by an in-house specialist agent "
    "team — proposes a 4-week rapid setup followed by a 24-month managed service: a GSM-standard, number-driven "
    "USSD menu (two paths: Info and Feedback) configured on short code 54747 in coordination with TNM and "
    "Airtel, a REST API pipeline that pushes de-identified session and feedback records to the VillageReach "
    "data warehouse, facilitated user acceptance testing (UAT) with ≥20 feature-phone users in Lilongwe and "
    "Balaka, and a management regime holding ≥99% uptime, a 4-hour response during working hours, up to 4 menu "
    "updates per 12 months, and monthly reports by the 5th of the following month."
)
para(
    "The approach is grounded in USSD's defining constraint — low-literacy, feature-phone-friendly interaction "
    "on a 182-character screen — and in an SRHR data governance posture that treats every session as sensitive "
    "by default: data minimization, de-identification at the edge, Malawi DPA (2024) alignment, and a feedback "
    "referral to \u201cFor urgent help, dial 54747\u201d with no callback. We deliver a governed, measurable, "
    "costed service (USD 45,000 or ≈ USD 1,875/month all-in) designed for handover-ready operation.",
)

# ================= 2 BACKGROUND =================
doc.add_heading("2. Background & Context", level=1)
doc.add_heading("2.1 The CHOICE Project and VillageReach", level=2)
para(
    "VillageReach strengthens health systems that bring health services to the last mile. Under the CHOICE "
    "Project in Malawi, VillageReach is advancing access to sexual and reproductive health and rights for "
    "young people and other underserved groups. A USSD channel is a uniquely suitable delivery vehicle: it "
    "works on every feature phone ever sold, requires no data plan, app installation or smartphone, and is "
    "already familiar to Malawian users across TNM and Airtel networks."
)
doc.add_heading("2.2 Why USSD, Why 54747", level=2)
bullets(
    [
        "Universal reach — works on all feature phones, no internet/data required.",
        "Real-time & free-to-end-user — the request triggers immediately and the session is free to the caller.",
        "Private in form — handset sessions do not persist content in an inbox visible to family members, reducing stigma risk for SRHR topics.",
        "Trackable — every session can be logged and aggregated for the data warehouse.",
    ]
)
para(
    "Short code 54747 is the CHS/CHOICE-anchored access point; this engagement configures and operates "
    "services on it."
)
doc.add_heading("2.3 The Users", level=2)
para(
    "The primary users are low-literacy, low-English, feature-phone users — including adolescents seeking SRHR "
    "information and community members who want to give feedback on the services they have received. The menu "
    "must therefore be icon-numeric, use plain Chichewa/national-language text, avoid free-text dependency, and "
    "keep every decision to one key press.",
)

# ================= 3 UNDERSTANDING =================
doc.add_heading("3. Understanding of the Assignment", level=1)
para(
    "This is a design–deploy–manage engagement, not a research-only consultancy. Its products are a working "
    "USSD service, an integration to the VillageReach data warehouse, a validated user acceptance test, and a "
    "governed 24-month service."
)
table(
    ["Dimension", "Our understanding"],
    [
        ["Channel", "USSD on short code 54747, GSM-standard (≤182 chars/screen)"],
        [
            "Core paths",
            "(1) Info — staged SRHR topics for low-literacy users; (2) Feedback — structured, then free-option feedback capture",
        ],
        [
            "Navigation",
            "Number-driven (\u201cEnter 1 for\u2026\u201d), \u201c99. Main menu\u201d on every screen, max 4 levels deep",
        ],
        [
            "Referral rule",
            "Final message \u201cFor urgent help, dial 54747\u201d; no callback / no outgoing call",
        ],
        [
            "Data",
            "Session logs + feedback records pushed via REST API to the VillageReach data warehouse, de-identified",
        ],
        [
            "Testing",
            "UAT with ≥20 feature-phone users, Lilongwe + Balaka (VillageReach organises participants; consultant facilitates)",
        ],
        [
            "Service regime",
            "≥99% uptime target; 4-hour response in Malawian working hours (08:00–17:00); up to 4 menu updates per 12 months; monthly report by the 5th",
        ],
        [
            "Timeline",
            "4-week setup phase (menu prototype Week 1, UAT Week 3, go-live + training/handover Week 4), then 24 months of management",
        ],
    ],
    widths=[4.0, 11.8],
)

# ================= 4 APPROACH =================
doc.add_heading("4. Technical Approach & Methodology", level=1)
doc.add_heading("4.1 Guiding Principles", level=2)
bullets(
    [
        "Low-literacy first — one key per decision, plain language, no reading walls, Chichewa/national-language menu text.",
        "USSD-native — every screen ≤182 chars, session-state-driven, resilient to interrupted sessions.",
        "Privacy by design — SRHR data is sensitive by default; minimize, de-identify, never expose personal content to third parties or inbox.",
        "Operator-aligned — TNM/Airtel connectivity managed via an aggregator/USSD gateway so short code 54747 is provisioned once and recovers fast.",
        "Measurable — uptime, response times, menu completion rates and feedback volume are instrumented and reported monthly.",
        "Handover-ready — the client (or a successor operator) can take the service over at any point with documentation and training.",
    ]
)
doc.add_heading("4.2 Platform Configuration (TNM / Airtel, Short Code 54747)", level=2)
bullets(
    [
        "Provision 54747 on both TNM and Airtel via a USSD gateway/aggregator with a single dial-string namespace so behavior is identical across networks.",
        "Configure the session flow: main menu → topic → content → referral (→ feedback) with session timeouts, retry logic for missed input, and a \u201cPress 0 to repeat this message\u201d pattern.",
        "Maintain staging and production short-code environments: staging for UAT and menu-update validation; production behind a go-live gate.",
        "Menu content is stored as versioned configuration (not hard-coded) so the up-to-4 menu updates per 12 months can be applied without re-provisioning the short code.",
    ]
)
doc.add_heading("4.3 Menu & Interface Design for Low-Literacy Users", level=2)
bullets(
    [
        "≤182 characters per USSD screen (hard limit).",
        "Every prompt begins with a number choice; user answers with digit(s) only.",
        "\u201c99. Main menu\u201d present on every non-main screen.",
        "Maximum 4 levels from root to deepest content.",
        "Short lines, one idea per line, consistent word order across screens.",
        "Final info screen always closes with the referral message.",
    ]
)
monospace(
    "[Session opens on 54747]\n"
    "\n"
    "A1  MAIN MENU\n"
    "    Welcome to SRHR info & feedback\n"
    "    1. Get information\n"
    "    2. Send feedback\n"
    "    (0. Repeat)\n"
    "\n"
    "If 1 -> INFO PATH\n"
    "B1  INFO TOPICS\n"
    "    1. Family planning\n"
    "    2. HIV & STI\n"
    "    3. Pregnancy & child health\n"
    "    4. Gender-based violence\n"
    "    5. Youth services\n"
    "    99. Main menu\n"
    "\n"
    "B2  (after topic) CONTENT (1-2 screens, <=182 chars each)\n"
    "    [Plain-language, pre-approved SRHR content]\n"
    "    99. Main menu\n"
    "    0. Repeat this message\n"
    "\n"
    "B3  REFERRAL (closes session - no callback)\n"
    "    For urgent help, dial 54747\n"
    "    Thank you. Goodbye.\n"
    "\n"
    "If 2 -> FEEDBACK PATH\n"
    "C1  FEEDBACK TOPIC\n"
    "    Your feedback is about:\n"
    "    1. Service you received\n"
    "    2. This 54747 service\n"
    "    99. Main menu\n"
    "\n"
    "C2  RATING\n"
    "    1. Good     2. OK    3. Poor\n"
    "\n"
    "C3  DETAIL (optional, structured)\n"
    "    Enter a number for extra detail:\n"
    "    1. Waited too long\n"
    "    2. Staff not supportive\n"
    "    3. Didn't get help\n"
    "    0. No extra detail\n"
    "\n"
    "C4  CONFIRMATION\n"
    "    Thank you. Your feedback is recorded\n"
    "    and anonymous. Goodbye.",
    size=8.5,
)
para(
    "Feedback is structured by default (topic → rating → detail) because low-literacy users answer reliably "
    "with digits; free-text is offered only as an opt-in numeric-coded option. This yields warehouse-grade, "
    "analyzable feedback without forcing typing.",
    italic=True,
    color=GREY,
)
doc.add_heading("4.4 REST API Data Pipeline to the VillageReach Data Warehouse", level=2)
bullets(
    [
        "Every completed and partial session is logged at the gateway and forwarded by a REST API to the VillageReach warehouse.",
        "Edge de-identification: MSISDN is hashed (salted) at the gateway before transmission; the warehouse receives an anonymous session key, timestamps, menu route, topic, rating, detail codes and completion state — not personal content.",
        "Payloads use a documented JSON schema; delivery is idempotent and retried with a dead-letter queue for warehouse outages; a checksummed daily reconciliation report guarantees no silent loss.",
        "Schema is versioned so the warehouse owner can evolve fields without breaking the live flow.",
    ]
)
doc.add_heading("4.5 UAT with ≥20 Feature-Phone Users (Lilongwe + Balaka)", level=2)
bullets(
    [
        "VillageReach organizes participants (≥20 feature-phone users across Lilongwe and Balaka); Light Speed Holdings facilitates.",
        "Each participant runs scripted tasks (find family-planning info; send \u201cpoor\u201d feedback; recover via \u201c99. Main menu\u201d) on a real feature phone against the staging short code.",
        "We capture pass/fail per task, time-to-complete, and a simple satisfaction rating, plus moderator observation of non-literate interaction.",
        "Exit criteria (UAT gate): ≥90% task completion, zero unrecoverable dead-ends, and all feedback records for the \u201cpoor\u201d task verifiably present in the warehouse.",
        "Findings feed a fix list; only non-blocking fixes are deferred past go-live.",
    ]
)
doc.add_heading("4.6 24-Month Management, Support & Uptime", level=2)
bullets(
    [
        "Uptime ≥99% — automated session and gateway health checks with alerting; operator interruption procedure with the aggregator.",
        "4-hour response during 08:00–17:00 Malawi time for P1/P2 issues via a monitored support inbox and ticketed tracking; 24-hour escalation for outages affecting the short code.",
        "Menu updates — up to 4 per 12 months, applied to staging, regression-tested, then promoted to production with a change record.",
        "Monthly reports by the 5th covering traffic, completion/abandonment rates, feedback themes, uptime, incidents and changes.",
        "24-Month Completion Report summarizing service performance and transfer-readiness.",
    ]
)
doc.add_heading("4.7 Data Privacy & Security Plan", level=2)
table(
    ["Area", "Measure"],
    [
        ["Sensitivity", "All SRHR sessions treated as sensitive/confidential content"],
        [
            "Minimization",
            "Collect only session, route, rating and codes necessary; no health narrative collected as free-text",
        ],
        [
            "De-identification",
            "MSISDN hashed+salted at the gateway; personal data never transmitted to warehouse",
        ],
        [
            "Legal basis",
            "Malawi Data Protection Act (2024) alignment; data processing agreement (DPA) with VillageReach and operator/aggregator",
        ],
        ["Storage", "Encrypted at rest and in transit (TLS); access role-based and logged"],
        [
            "Retention",
            "Session logs retained only as long as required (default 90 days) then purged; per VillageReach policy",
        ],
        [
            "Right to deletion",
            "De-identification makes individual deletion non-required; raw logs support erasure on request",
        ],
        [
            "Governance",
            "Privacy impact assessment at go-live; annual privacy review; breach notification within SLA",
        ],
    ],
    widths=[4.0, 11.8],
)

# ================= 5 WORK PLAN =================
doc.add_heading("5. Work Plan & Timeline", level=1)
para(
    "The engagement runs a 4-week setup phase followed by 24 months of managed service. Each setup phase "
    "closes with a formal quality gate."
)
table(
    ["Phase", "Period", "Focus", "Gate"],
    [
        [
            "1 Setup — Menu",
            "Week 1",
            "Menu prototype & wireframe, content finalization, 54747 provisioning with TNM/Airtel",
            "Menu Prototype sign-off",
        ],
        [
            "2 Setup — Integration",
            "Week 2",
            "Gateway configuration, REST API build, warehouse schema agreement, staging short code live",
            "Staging ready",
        ],
        [
            "3 UAT",
            "Week 3",
            "≥20 feature-phone users in Lilongwe + Balaka; fix list; exit criteria",
            "UAT pass",
        ],
        [
            "4 Go-Live & Handover",
            "Week 4",
            "Production enable, training & handover pack, go-live report, privacy sign-off",
            "Go-live",
        ],
        [
            "5–8 Managed service",
            "Months 1–3",
            "Uptime monitoring, first monthly reports, support",
            "Monthly reports",
        ],
        [
            "9–29 Managed service",
            "Months 4–23",
            "Menu updates (≤4/12mo), quarterly reviews, support",
            "Monthly + quarterly",
        ],
        [
            "30 Completion",
            "Month 24",
            "24-Month Completion Report, transfer readiness, close-out",
            "Final acceptance",
        ],
    ],
    widths=[4.2, 2.2, 6.8, 2.6],
)

# ================= 6 DELIVERABLES =================
doc.add_heading("6. Deliverables & Acceptance Criteria", level=1)
table(
    ["#", "Deliverable", "Due", "Key acceptance criteria"],
    [
        [
            "D1",
            "Menu Prototype & Wireframe",
            "End Week 1",
            "Both paths (Info + Feedback) mapped; every screen ≤182 chars; \u201c99. Main menu\u201d & referral on the right screens; ≤4 levels",
        ],
        [
            "D2",
            "UAT Completion Report",
            "End Week 3",
            "≥20 feature-phone users facilitated (Lilongwe + Balaka); ≥90% task completion; feedback verifiably in warehouse",
        ],
        [
            "D3",
            "Go-Live & Integration Report",
            "Week 4",
            "Short code 54747 live on TNM + Airtel; REST pipeline delivering; uptime instrumentation active",
        ],
        [
            "D4",
            "Training & Handover Pack",
            "Week 4",
            "Operator manual, menu-change procedure, privacy notes, contact/process matrix",
        ],
        [
            "D5",
            "Monthly Reports",
            "5th of each month",
            "Traffic, completion, feedback themes, uptime, incidents, changes",
        ],
        [
            "D6",
            "24-Month Completion Report",
            "Month 24",
            "24 months of KPIs, lessons, transfer-readiness checklist",
        ],
    ],
    widths=[1.0, 4.4, 2.0, 8.4],
)

# ================= 7 RISK =================
doc.add_heading("7. Risk Management", level=1)
table(
    ["ID", "Risk", "P×I", "Mitigation"],
    [
        [
            "R1",
            "Operator/aggregator short-code delay",
            "Med-High",
            "Early provisioning in Week 1; aggregator SLA; staging short code as fallback",
        ],
        [
            "R2",
            "Low-literacy users abandon menus",
            "High",
            "Number-driven ≤4-level design; \u201c0. Repeat\u201d; UAT iteration before go-live",
        ],
        [
            "R3",
            "SRHR content sensitivity / stigma",
            "High",
            "Privacy-by-design; anonymous sessions; no inbox persistence; referral (no callback)",
        ],
        [
            "R4",
            "Warehouse outage loses records",
            "Medium",
            "Idempotent API + retry + dead-letter queue + daily reconciliation",
        ],
        [
            "R5",
            "Menu content becomes stale",
            "Medium",
            "Versioned content; ≤4 updates/12mo process; annual SRHR content review",
        ],
        [
            "R6",
            "Uptime below ≥99%",
            "Medium",
            "Proactive health checks; operator escalation; 24-hr outage response",
        ],
        [
            "R7",
            "Data protection breach",
            "Low-Critical",
            "Edge de-identification; encryption; DPA; privacy review; breach SLA",
        ],
    ],
    widths=[1.2, 5.4, 2.0, 7.2],
)
para(
    "A living risk register with owners and a monthly review cadence is maintained for the full 24 months."
)

# ================= 8 BUDGET =================
doc.add_heading("8. Financial Proposal (Full Priced — USD)", level=1)
table(
    ["Category", "Amount (USD)"],
    [
        ["Setup (Weeks 1–4)", "13,350"],
        ["Recurring managed service (24 months)", "25,633"],
        ["Reimbursables (travel, testing SIMs, UAT participant incentives)", "1,926"],
        ["Subtotal", "40,909"],
        ["Contingency (10%)", "4,091"],
        ["TOTAL ENGAGEMENT VALUE", "45,000"],
    ],
    widths=[10.0, 5.8],
)
para(
    "Effective rate: $1,875/month all-in ($45,000 ÷ 24 months). All costs exclude applicable taxes withheld "
    "per law; reimbursables are payable against receipts and prior written approval where applicable."
)
para("Last updated: 2026-09-18")

doc.save(OUT)
print(f"Saved: {OUT}")
