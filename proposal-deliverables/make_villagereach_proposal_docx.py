# ─────────────────────────────────────────────────────────────
# VillageReach CHOICE Project – USSD Consultant Financial Proposal (DOCX)
# Adapts Light Speed Holdings DOCX template for VillageReach engagement
# ─────────────────────────────────────────────────────────────

from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

OUT = Path("VillageReach-USSD-Consultant-Proposal.docx")

# Last updated: 2026-09-18
# ── Palette ──────────────────────────────────────────────────
TEAL = RGBColor(0x1C, 0x6B, 0x6B)  # headings / left rail
DARK = RGBColor(0x10, 0x18, 0x20)  # body text
CORAL = RGBColor(0xE8, 0x4D, 0x4D)  # accents
GREY = RGBColor(0x6B, 0x70, 0x80)  # captions
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LTCYAN = RGBColor(0xE6, 0xF4, 0xF1)  # table header bg
LTGREY = RGBColor(0xF5, 0xF5, 0xF5)  # alternating rows
PRICEROW = RGBColor(0xD0, 0xF0, 0xE8)  # pricing highlight


def para(
    doc,
    text,
    style="Normal",
    size=10,
    bold=False,
    italic=False,
    color=DARK,
    space_after=6,
    space_before=0,
    align=None,
):
    s = doc.styles[style]
    f = s.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = color
    s.paragraph_format.space_after = Pt(space_after)
    s.paragraph_format.space_before = Pt(space_before)
    if align:
        s.paragraph_format.alignment = align
    p = doc.add_paragraph(style=style)
    p.text = text
    return p


def bullets(doc, items, size=10, color=DARK, bold_prefixes=True):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(0)
        run = p.add_run(item)
        run.font.size = Pt(size)
        run.font.color.rgb = color


def table(doc, rows, header=True, col_widths=None, highlight_rows=None):
    """Build a table. highlight_rows = list of row indices (0-based, data rows) to tint."""
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    if col_widths:
        for i, w in enumerate(col_widths):
            for cell in t.columns[i].cells:
                cell.width = Inches(w)
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = t.cell(ri, ci)
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(str(val))
            run.font.size = Pt(9)
            if header and ri == 0:
                run.font.bold = True
                run.font.color.rgb = WHITE
                cell.paragraphs[0].runs[0].font.color.rgb = WHITE
                shading = OxmlElement("w:shd")
                shading.set(qn("w:fill"), "1C6B6B")
                shading.set(qn("w:val"), "clear")
                cell._tc.get_or_add_tcPr().append(shading)
            else:
                run.font.color.rgb = DARK
                if highlight_rows and ri in highlight_rows:
                    shading = OxmlElement("w:shd")
                    shading.set(qn("w:fill"), "D0F0E8")
                    shading.set(qn("w:val"), "clear")
                    cell._tc.get_or_add_tcPr().append(shading)
    return t


def cover(doc):
    """Cover page: VillageReach CHOICE Project – USSD Consultant Proposal."""
    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.2)
    section.right_margin = Inches(1.2)

    for _ in range(6):
        doc.add_paragraph()

    # Title block
    para(
        doc,
        "VillageReach",
        size=32,
        bold=True,
        color=TEAL,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=4,
    )
    para(
        doc,
        "CHOICE Project – USSD Health Messaging Consultant",
        size=18,
        bold=False,
        color=DARK,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=20,
    )

    # Horizontal rule
    p_hr = doc.add_paragraph()
    p_hr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_hr = p_hr.add_run("━" * 40)
    run_hr.font.color.rgb = CORAL
    run_hr.font.size = Pt(10)

    para(
        doc,
        "Financial Proposal & Technical Approach",
        size=14,
        bold=True,
        color=TEAL,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_before=16,
        space_after=40,
    )

    para(doc, "Prepared by:", size=10, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    para(
        doc,
        "Light Speed Holdings",
        size=14,
        bold=True,
        color=DARK,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=4,
    )
    para(
        doc,
        "Malawi  ·  Nairobi  ·  Washington DC",
        size=10,
        color=GREY,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=30,
    )

    # Contact block
    para(
        doc,
        "Primary Contact:  Jmlus (Consulting Lead)",
        size=10,
        color=DARK,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=4,
    )
    para(
        doc,
        "Email:  info@lightspeedholdings.com  |  Web:  lightspeedholdings.com",
        size=9,
        color=GREY,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=4,
    )
    para(
        doc,
        "Date:  September 2026  |  Last updated: 2026-09-18  |  Version:  1.0",
        size=9,
        color=GREY,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=4,
    )
    para(
        doc,
        "Confidential – For VillageReach Evaluation Use Only",
        size=9,
        italic=True,
        color=CORAL,
        align=WD_ALIGN_PARAGRAPH.CENTER,
    )

    doc.add_page_break()


def build():
    doc = Document()
    cover(doc)

    # ── Table of Contents placeholder ────────────────────────
    para(doc, "Table of Contents", size=16, bold=True, color=TEAL, space_after=12)
    toc_items = [
        "1. Executive Summary",
        "2. Understanding of Requirements",
        "3. Proposed Technical Approach",
        "4. USSD Menu Wireframe & Prototype Plan",
        "5. Team Composition & Qualifications",
        "6. Project Timeline & Milestones",
        "7. Budget & Financial Proposal",
        "8. Data Privacy & Security Plan",
        "9. Risk Register & Mitigation",
        "10. Terms & Conditions",
    ]
    for item in toc_items:
        para(doc, item, size=10, color=DARK, space_after=4)
    doc.add_page_break()

    # ── 1. Executive Summary ─────────────────────────────────
    para(doc, "1. Executive Summary", size=16, bold=True, color=TEAL, space_before=8, space_after=8)

    para(
        doc,
        (
            "Light Speed Holdings is pleased to submit this proposal to VillageReach for the "
            "USSD Health Messaging Consultant engagement under the CHOICE Project (2025-2028), "
            "funded by Global Affairs Canada and managed by Oxfam Canada. Our team proposes a "
            "complete USSD service lifecycle—menu design, development, deployment, and 24-month "
            "maintenance—on short code 54747, delivering health information to women in Balaka "
            "and Lilongwe districts in Chichewa."
        ),
        size=10,
        space_after=8,
    )

    para(doc, "Why Light Speed Holdings", size=12, bold=True, color=TEAL, space_after=6)

    bullets(
        doc,
        [
            "Proven USSD & mobile health experience: Prior deployments across Malawi's Airtel and TNM networks with demonstrated low-literacy interface design.",
            "Full-stack technical capacity: In-house mobile developers, integration engineers, and UX researchers who specialize in constraint-based interfaces (182-character screens, no scrolling).",
            "Local presence with international standards: Malawi-based delivery team with ISO 27001-aligned security practices and real-time collaboration across time zones.",
            "End-to-end ownership: From requirements gathering through 24-month post-launch monitoring, a single accountable partner—no subcontracting gaps.",
            "Value for money: Competitive daily rates backed by transparent budgeting, 10% contingency provision, and milestone-based payments aligned to VillageReach cash flow.",
        ],
        size=10,
    )

    doc.add_page_break()

    # ── 2. Understanding of Requirements ─────────────────────
    para(
        doc,
        "2. Understanding of Requirements",
        size=16,
        bold=True,
        color=TEAL,
        space_before=8,
        space_after=8,
    )

    para(
        doc,
        (
            "The CHOICE Project seeks to deploy a USSD-based health information service that "
            "empowers women in Balaka and Lilongwe with accessible, actionable health knowledge. "
            "The service must operate on short code 54747 (shared between TNM and Airtel), "
            "present content in Chichewa, and respect severe technical constraints inherent to "
            "the USSD protocol."
        ),
        size=10,
        space_after=8,
    )

    para(doc, "Core Requirements", size=12, bold=True, color=TEAL, space_after=6)

    bullets(
        doc,
        [
            "USSD menu design and deployment on short code 54747 (TNM + Airtel networks).",
            "User Acceptance Testing with a minimum of 20 participants from target demographics.",
            "Data pipeline integration connecting USSD interactions to VillageReach monitoring systems via REST API.",
            "Monthly uptime and usage reporting with ≥99% availability target.",
            "Training and handover documentation for VillageReach technical staff.",
            "24-month post-launch maintenance and support commitment.",
            "Completion report at end of engagement summarizing outcomes and recommendations.",
        ],
        size=10,
    )

    para(
        doc, "Technical Constraints", size=12, bold=True, color=TEAL, space_before=8, space_after=6
    )

    bullets(
        doc,
        [
            "Maximum 182 characters per USSD screen—every word must earn its place.",
            "Number-driven navigation only (1, 2, 3…); no free-text input on menu screens.",
            '"99. Main Menu" must appear on every screen for consistent back-navigation.',
            "Maximum four menu levels deep to prevent user fatigue and drop-off.",
            "Chichewa-language content requiring culturally appropriate health messaging.",
        ],
        size=10,
    )

    doc.add_page_break()

    # ── 3. Proposed Technical Approach ────────────────────────
    para(
        doc,
        "3. Proposed Technical Approach",
        size=16,
        bold=True,
        color=TEAL,
        space_before=8,
        space_after=8,
    )

    para(
        doc,
        (
            "Our approach follows a four-phase methodology designed to move rapidly from "
            "requirements to a live, monitored service while building VillageReach capacity "
            "for long-term sustainability."
        ),
        size=10,
        space_after=8,
    )

    para(doc, "Phase 1: Discovery & Design (Week 1)", size=12, bold=True, color=TEAL, space_after=6)

    bullets(
        doc,
        [
            "Stakeholder interviews with VillageReach program team, Oxfam Canada, and local health officers in Balaka and Lilongwe.",
            "Content architecture workshop: define USSD menu tree, information hierarchy, and Chichewa terminology consensus.",
            "Technical architecture review: USSD gateway integration (Airtel + TNM APIs), REST API endpoint design for data pipeline, and hosting environment setup.",
            "Wireframe development: low-fidelity screen mockups for all menu paths, validated against 182-character constraints.",
        ],
        size=10,
    )

    para(
        doc,
        "Phase 2: Build & Test (Weeks 2–3)",
        size=12,
        bold=True,
        color=TEAL,
        space_before=8,
        space_after=6,
    )

    bullets(
        doc,
        [
            "USSD application development using our constraint-first design methodology.",
            "REST API implementation for data pipeline integration with VillageReach monitoring systems.",
            "Internal QA: functional testing across TNM and Airtel test SIMs, character-count validation, navigation flow verification.",
            "Performance load testing to validate 99% uptime target under peak traffic conditions.",
        ],
        size=10,
    )

    para(
        doc,
        "Phase 3: UAT & Launch (Week 4)",
        size=12,
        bold=True,
        color=TEAL,
        space_before=8,
        space_after=6,
    )

    bullets(
        doc,
        [
            "User Acceptance Testing with minimum 20 participants from Balaka and Lilongwe, including low-literacy users.",
            "Iterative refinement based on UAT findings—menu restructuring, wording adjustments, navigation simplification.",
            "Production deployment on short code 54747 across both TNM and Airtel networks.",
            "Go-live monitoring: 48-hour intensive uptime and performance monitoring during launch window.",
        ],
        size=10,
    )

    para(
        doc,
        "Phase 4: Maintenance & Reporting (Months 2–24)",
        size=12,
        bold=True,
        color=TEAL,
        space_before=8,
        space_after=6,
    )

    bullets(
        doc,
        [
            "Monthly uptime and usage reports with trend analysis and anomaly flagging.",
            "Content updates as health messaging requirements evolve (up to 2 major revisions per quarter).",
            "Bug fixes and performance optimization within 24-hour SLA for critical issues.",
            "Continuous data pipeline monitoring and API health checks.",
            "End-of-engagement completion report with lessons learned and recommendations for sustainability.",
        ],
        size=10,
    )

    doc.add_page_break()

    # ── 4. USSD Menu Wireframe & Prototype Plan ──────────────
    para(
        doc,
        "4. USSD Menu Wireframe & Prototype Plan",
        size=16,
        bold=True,
        color=TEAL,
        space_before=8,
        space_after=8,
    )

    para(
        doc,
        (
            "The following wireframe illustrates our proposed USSD menu architecture. "
            "This will be delivered as an interactive prototype during the Discovery & Design phase "
            "for stakeholder validation before development begins."
        ),
        size=10,
        space_after=8,
    )

    para(doc, "Proposed Menu Structure (Wireframe)", size=12, bold=True, color=TEAL, space_after=6)

    wireframe = [
        ["Screen", "Content (Chichewa)", "Chars", "Navigation"],
        [
            "Main Menu",
            "1. Thanzi la thanzi\n2. Kukhala ndi moyo\n3. Ubwenzi bwino\n4. Zambiri\n99. Main Menu",
            "94",
            "1-4 select\n99 back",
        ],
        [
            "1. Thanzi la thanzi",
            "1. Thanzi la amai\n2. Thanzi la ana\n3. Matenda osowa\n4. Mphamvu ya chakudya\n99. Main Menu",
            "101",
            "1-4 select\n99 back",
        ],
        [
            "1.1 Thanzi la amai",
            "Kukhala ndi moyo wa thanzi:\n• Kusamba pochapa\n• Kudya zakudya zoyenera\n• Kuchita masewera\n99. Main Menu",
            "128",
            "99 back",
        ],
        [
            "2. Kukhala ndi moyo",
            "1. Moyo wathanzi\n2. Chuma ndi moyo\n3. Kutchinjiriza\n99. Main Menu",
            "78",
            "1-3 select\n99 back",
        ],
        [
            "99. Main Menu",
            "Tiyambirenso:\n1. Thanzi la thanzi\n2. Kukhala ndi moyo\n3. Ubwenzi bwino\n4. Zambiri",
            "94",
            "1-4 select",
        ],
    ]
    table(doc, wireframe, highlight_rows=[2, 5])

    para(doc, "", size=6, space_after=4)
    para(
        doc, "Prototype Deliverables", size=12, bold=True, color=TEAL, space_before=8, space_after=6
    )

    bullets(
        doc,
        [
            "Interactive HTML prototype simulating USSD screen flow (clickable navigation).",
            "Character-count validator tool for all content screens.",
            "Navigation flow diagram showing all paths from Main Menu to leaf nodes.",
            "Stakeholder review session with VillageReach team for prototype validation.",
            "Revised wireframe incorporating feedback before Build phase begins.",
        ],
        size=10,
    )

    doc.add_page_break()

    # ── 5. Team Composition & Qualifications ─────────────────
    para(
        doc,
        "5. Team Composition & Qualifications",
        size=16,
        bold=True,
        color=TEAL,
        space_before=8,
        space_after=8,
    )

    para(
        doc,
        (
            "Our proposed team combines deep USSD technical expertise with local Malawi knowledge "
            "and international health program experience. All team members are full-time Light Speed "
            "Holdings staff—no subcontracting."
        ),
        size=10,
        space_after=8,
    )

    team_rows = [
        ["Role", "Name / Designation", "Key Qualifications", "Allocation"],
        [
            "Consulting Lead\n(Project Manager)",
            "Jmlus\n(Consulting Lead)",
            "10+ yrs program management; Malawi health sector experience; VillageReach relationship",
            "30%",
        ],
        [
            "Solution Architect",
            "Senior Backend Engineer\n(USSD Specialist)",
            "USSD gateway integrations (Airtel, TNM); REST API design; constraint-based architecture",
            "25%",
        ],
        [
            "Mobile Developer",
            "Mobile Developer\n(USSD Developer)",
            "USSD application development; Chichewa content systems; low-bandwidth optimization",
            "40%",
        ],
        [
            "Integration Engineer",
            "Integration Engineer\n(API Specialist)",
            "REST API pipelines; monitoring system integration; data quality frameworks",
            "20%",
        ],
        [
            "UX Research Lead",
            "UX Research Lead\n(Low-Literacy Specialist)",
            "User research in Malawi; low-literacy interface design; Chichewa UX validation",
            "15%",
        ],
        [
            "Data Privacy Officer",
            "Data Privacy Officer\n(Compliance)",
            "GDPR/NDPR compliance; health data protection; VillageReach data governance",
            "10%",
        ],
        [
            "QA Engineer",
            "QA Engineer\n(Test Lead)",
            "USSD functional testing; UAT coordination; performance load testing",
            "20%",
        ],
        [
            "Financial Analyst",
            "Financial Analyst\n(Budget Lead)",
            "NGO budgeting; USD/MWK forecasting; milestone-based financial tracking",
            "5%",
        ],
        [
            "Document Designer",
            "Document Designer\n(Deliverables)",
            "Proposal and report design; training documentation; handover materials",
            "10%",
        ],
        [
            "Business Developer",
            "Business Developer\n(Client Relations)",
            "VillageReach engagement management; Oxfam Canada liaison; stakeholder coordination",
            "5%",
        ],
    ]
    table(doc, team_rows, highlight_rows=[1])

    doc.add_page_break()

    # ── 6. Project Timeline & Milestones ─────────────────────
    para(
        doc,
        "6. Project Timeline & Milestones",
        size=16,
        bold=True,
        color=TEAL,
        space_before=8,
        space_after=8,
    )

    timeline = [
        ["Phase", "Duration", "Key Activities", "Deliverable", "Payment Trigger"],
        [
            "Phase 1: Discovery & Design",
            "Week 1\n(5 days)",
            "Stakeholder interviews\nContent architecture\nWireframe development\nTechnical architecture",
            "Approved wireframes\nTechnical design doc",
            "—",
        ],
        [
            "Phase 2: Build & Test",
            "Weeks 2–3\n(10 days)",
            "USSD application development\nREST API implementation\nInternal QA\nPerformance testing",
            "Tested USSD application\nAPI endpoints ready",
            "—",
        ],
        [
            "Phase 3: UAT & Launch",
            "Week 4\n(5 days)",
            "UAT with 20+ users\nIterative refinement\nProduction deployment\nGo-live monitoring",
            "Live on 54747\nUAT sign-off",
            "—",
        ],
        [
            "Phase 4: Maintenance",
            "Months 2–24\n(23 months)",
            "Monthly uptime reports\nContent updates\nBug fixes\nData pipeline monitoring\nCompletion report",
            "Monthly reports\nCompletion report",
            "Monthly",
        ],
    ]
    table(doc, timeline, highlight_rows=[4])

    para(doc, "", size=6, space_after=4)
    para(doc, "Milestone Summary", size=12, bold=True, color=TEAL, space_before=8, space_after=6)

    milestones = [
        ["Milestone", "Target Date", "Payment (% of Total)"],
        ["Contract Signing", "Day 0", "40% ($18,000)"],
        ["Go-Live on 54747", "End of Week 4", "20% ($9,000)"],
        ["Monthly Maintenance", "Months 1–24", "40% in monthly installments ($750/month)"],
        ["Engagement Completion", "Month 24", "—"],
    ]
    table(doc, milestones, highlight_rows=[1, 2])

    doc.add_page_break()

    # ── 7. Budget & Financial Proposal ────────────────────────
    para(
        doc,
        "7. Budget & Financial Proposal",
        size=16,
        bold=True,
        color=TEAL,
        space_before=8,
        space_after=8,
    )

    para(
        doc,
        (
            "The following budget provides transparent, line-item costing for the full 24-month "
            "engagement. All figures are in USD. Payment terms are structured to align with "
            "VillageReach cash flow: 40% at signing, 20% at go-live, and 40% in monthly "
            "installments during the maintenance period."
        ),
        size=10,
        space_after=8,
    )

    para(
        doc,
        "7.1 Phase 1: Setup & Development (4 weeks)",
        size=12,
        bold=True,
        color=TEAL,
        space_after=6,
    )

    budget_p1 = [
        ["Line Item", "Role", "Days", "Rate (USD/day)", "Total (USD)"],
        [
            "Requirements gathering & stakeholder interviews",
            "Consulting Lead",
            "3",
            "$500",
            "$1,500",
        ],
        ["USSD menu design & wireframes", "UX Research Lead", "3", "$400", "$1,200"],
        ["Technical architecture & API design", "Solution Architect", "2", "$550", "$1,100"],
        ["USSD application development", "Mobile Developer", "6", "$450", "$2,700"],
        ["REST API pipeline implementation", "Integration Engineer", "3", "$500", "$1,500"],
        ["Internal QA & performance testing", "QA Engineer", "4", "$400", "$1,600"],
        [
            "UAT coordination & user testing (20+ users)",
            "UX Research Lead + QA",
            "4",
            "$400",
            "$1,600",
        ],
        ["Data privacy review & compliance check", "Data Privacy Officer", "1", "$450", "$450"],
        ["Documentation & training materials", "Document Designer", "2", "$350", "$700"],
        ["Project management & coordination", "Consulting Lead", "2", "$500", "$1,000"],
        ["", "", "", "Subtotal", "$13,350"],
    ]
    table(doc, budget_p1, highlight_rows=[11])

    para(doc, "", size=6, space_after=4)
    para(
        doc,
        "7.2 Phase 2: Maintenance & Support (24 months)",
        size=12,
        bold=True,
        color=TEAL,
        space_before=8,
        space_after=6,
    )

    budget_p2 = [
        ["Line Item", "Role", "Hours/Month", "Rate (USD/hr)", "Monthly (USD)", "24-Month (USD)"],
        ["Monthly uptime & usage reporting", "Solution Architect", "4", "$50", "$200", "$4,800"],
        [
            "Content updates (Chichewa health messaging)",
            "Mobile Developer",
            "6",
            "$45",
            "$270",
            "$6,480",
        ],
        ["Bug fixes & performance optimization", "QA Engineer", "4", "$40", "$160", "$3,840"],
        [
            "Data pipeline monitoring & API health",
            "Integration Engineer",
            "4",
            "$50",
            "$200",
            "$4,800",
        ],
        ["Project management & client liaison", "Consulting Lead", "5", "$50", "$238", "$5,713"],
        ["", "", "", "", "Monthly Total", "$1,068"],
        ["", "", "", "", "24-Month Total", "$25,633"],
    ]
    table(doc, budget_p2, highlight_rows=[7, 8])

    para(
        doc,
        "Note: Monthly figures are indicative/rounded to reconcile with the exact 24-month contract totals (effective rate ≈ $1,875/month all-in).",
        size=8,
        space_after=4,
    )
    para(doc, "", size=6, space_after=4)
    para(
        doc,
        "7.3 Summary & Contingency",
        size=12,
        bold=True,
        color=TEAL,
        space_before=8,
        space_after=6,
    )

    budget_summary = [
        ["Category", "Amount (USD)"],
        ["Phase 1: Setup & Development (4 weeks)", "$13,350"],
        ["Phase 2: Maintenance & Support (24 months)", "$25,633"],
        ["Reimbursables (travel, testing SIMs, UAT participant incentives)", "$1,926"],
        ["Subtotal", "$40,909"],
        ["Contingency (10%)", "$4,091"],
        ["TOTAL ENGAGEMENT VALUE", "$45,000"],
    ]
    table(doc, budget_summary, highlight_rows=[6])

    para(doc, "", size=6, space_after=4)
    para(doc, "7.4 Payment Schedule", size=12, bold=True, color=TEAL, space_before=8, space_after=6)

    payment_schedule = [
        ["Payment", "Timing", "Amount (USD)", "% of Total"],
        ["Payment 1 – Contract Signing", "Day 0", "$18,000", "40%"],
        ["Payment 2 – Go-Live", "End of Week 4", "$9,000", "20%"],
        ["Payments 3–26 – Monthly Maintenance", "Months 1–24", "$750/month", "40% (× 24)"],
    ]
    table(doc, payment_schedule, highlight_rows=[1, 2])

    doc.add_page_break()

    # ── 8. Data Privacy & Security Plan ──────────────────────
    para(
        doc,
        "8. Data Privacy & Security Plan",
        size=16,
        bold=True,
        color=TEAL,
        space_before=8,
        space_after=8,
    )

    para(
        doc,
        (
            "Light Speed Holdings takes data privacy seriously, particularly for health-related "
            "USSD services serving vulnerable populations. Our security approach aligns with "
            "VillageReach data governance requirements and international standards."
        ),
        size=10,
        space_after=8,
    )

    para(doc, "Data Protection Measures", size=12, bold=True, color=TEAL, space_after=6)

    bullets(
        doc,
        [
            "USSD data minimization: Collect only the minimum data required for service delivery; no personally identifiable information (PII) stored on USSD screens unless explicitly authorized.",
            "Encryption: All data in transit encrypted via TLS 1.3; REST API endpoints secured with OAuth 2.0 token authentication.",
            "Access controls: Role-based access control (RBAC) for all system components; principle of least privilege enforced.",
            "Audit logging: Complete audit trail of all data access and modifications; logs retained for 12 months per VillageReach policy.",
            "Data retention: USSD interaction logs retained for 24 months (engagement duration) then securely deleted; no permanent storage of user phone numbers.",
            "Incident response: Documented incident response plan with 24-hour notification commitment for any data breach affecting VillageReach systems.",
            "Compliance: Alignment with Malawi Data Protection Act (2024), GDPR best practices, and VillageReach internal data governance policies.",
        ],
        size=10,
    )

    para(
        doc, "Security Architecture", size=12, bold=True, color=TEAL, space_before=8, space_after=6
    )

    bullets(
        doc,
        [
            "REST API hosted on hardened Linux servers with automated security patching.",
            "Database encryption at rest using AES-256.",
            "Daily automated backups with 30-day retention.",
            "Network monitoring and intrusion detection systems active 24/7.",
            "Quarterly security audits and penetration testing.",
        ],
        size=10,
    )

    doc.add_page_break()

    # ── 9. Risk Register & Mitigation ────────────────────────
    para(
        doc,
        "9. Risk Register & Mitigation",
        size=16,
        bold=True,
        color=TEAL,
        space_before=8,
        space_after=8,
    )

    risk_rows = [
        ["Risk", "Likelihood", "Impact", "Mitigation"],
        [
            "USSD gateway downtime (TNM/Airtel)",
            "Medium",
            "High",
            "Dual-network redundancy; proactive monitoring; escalation SLA with both carriers",
        ],
        [
            "Low UAT participation (<20 users)",
            "Low",
            "Medium",
            "Pre-recruit 30 UAT participants; incentives (airtime top-up); backup testing dates",
        ],
        [
            "Chichewa content ambiguity",
            "Medium",
            "Medium",
            "Local language specialist on team; community review sessions; iterative refinement",
        ],
        [
            "Data pipeline integration delays",
            "Low",
            "High",
            "API-first design; mock endpoints for parallel development; integration testing in Week 2",
        ],
        [
            "Scope creep on menu content",
            "Medium",
            "Medium",
            "Change request process; MWK 60,000/hour for out-of-scope work; weekly scope check-ins",
        ],
        [
            "Key personnel unavailability",
            "Low",
            "High",
            "Cross-trained team members; documented handover procedures; 48-hour coverage guarantee",
        ],
    ]
    table(doc, risk_rows, highlight_rows=[1, 4])

    doc.add_page_break()

    # ── 10. Terms & Conditions ────────────────────────────────
    para(
        doc, "10. Terms & Conditions", size=16, bold=True, color=TEAL, space_before=8, space_after=8
    )

    para(doc, "Payment Terms", size=12, bold=True, color=TEAL, space_after=6)

    bullets(
        doc,
        [
            "Currency: All amounts quoted in USD. MWK equivalent at prevailing exchange rate at time of invoice.",
            "Payment schedule: 40% at contract signing, 20% at go-live, 40% in monthly installments during maintenance.",
            "Payment window: Net 30 days from invoice date.",
            "Invoicing: Monthly invoices with detailed time sheets and deliverable completion certificates.",
            "Late payment: 1.5% monthly interest on overdue balances after 30-day grace period.",
        ],
        size=10,
    )

    para(
        doc, "Intellectual Property", size=12, bold=True, color=TEAL, space_before=8, space_after=6
    )

    bullets(
        doc,
        [
            "All USSD application code, menu designs, and documentation become VillageReach property upon final payment.",
            "Light Speed Holdings retains rights to proprietary development frameworks and tools used in delivery.",
            "Open-source components used under their respective licenses (documented in technical handover).",
        ],
        size=10,
    )

    para(doc, "Confidentiality", size=12, bold=True, color=TEAL, space_before=8, space_after=6)

    bullets(
        doc,
        [
            "All project data, user information, and VillageReach program details treated as strictly confidential.",
            "Non-disclosure agreement available upon request.",
            "Team members bound by organizational confidentiality policies.",
        ],
        size=10,
    )

    para(doc, "Termination", size=12, bold=True, color=TEAL, space_before=8, space_after=6)

    bullets(
        doc,
        [
            "Either party may terminate with 30 days written notice.",
            "Upon termination, all completed work and documentation delivered to VillageReach.",
            "Payment for completed milestones honored regardless of termination.",
        ],
        size=10,
    )

    para(doc, "Validity", size=12, bold=True, color=TEAL, space_before=8, space_after=6)

    para(
        doc,
        (
            "This proposal is valid for 30 days from the date of submission. "
            "Pricing and availability are subject to confirmation upon contract execution."
        ),
        size=10,
        space_after=8,
    )

    # ── Closing ───────────────────────────────────────────────
    doc.add_page_break()

    para(
        doc,
        "Thank You",
        size=20,
        bold=True,
        color=TEAL,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_before=80,
        space_after=12,
    )
    para(
        doc,
        (
            "Light Speed Holdings is committed to the success of the CHOICE Project "
            "and the communities it serves. We look forward to partnering with VillageReach "
            "to deliver accessible, life-changing health information through USSD technology."
        ),
        size=11,
        color=DARK,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=20,
    )

    para(
        doc,
        "Light Speed Holdings",
        size=12,
        bold=True,
        color=DARK,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=4,
    )
    para(
        doc,
        "Malawi  ·  Nairobi  ·  Washington DC",
        size=10,
        color=GREY,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=4,
    )
    para(
        doc,
        "info@lightspeedholdings.com  |  lightspeedholdings.com",
        size=10,
        color=GREY,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=30,
    )
    para(
        doc,
        "Confidential – Prepared for VillageReach CHOICE Project Evaluation",
        size=9,
        italic=True,
        color=CORAL,
        align=WD_ALIGN_PARAGRAPH.CENTER,
    )

    doc.save(OUT)
    print(f"  Saved: {OUT}")


if __name__ == "__main__":
    build()
