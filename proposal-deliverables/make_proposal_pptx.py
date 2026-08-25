"""Generate the proposal slide deck (.pptx) for the Digital Health Consultant engagement.

Design: deep teal institutional palette, warm sand background, coral accent,
Arial typography, card layouts + chevron roadmap. 16:9.

Run:  uv run --with python-pptx python proposal-deliverables/make_proposal_pptx.py
"""

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

TEAL = RGBColor(0x0E, 0x5A, 0x66)
TEAL2 = RGBColor(0x1B, 0x7F, 0x8C)
SAND = RGBColor(0xF7, 0xF5, 0xF0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CORAL = RGBColor(0xE8, 0x70, 0x3A)
DARK = RGBColor(0x1C, 0x3B, 0x42)
GREY = RGBColor(0x5A, 0x6B, 0x6E)
LINE = RGBColor(0xD9, 0xE2, 0xE4)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
PAGE = [0]


def box(s, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE):
    shp = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.shadow.inherit = False
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(1)
    return shp


def _apply(p, tf_p, d):
    p.alignment = d.get("align", PP_ALIGN.LEFT)
    if d.get("space_after") is not None:
        p.space_after = Pt(d["space_after"])
    if d.get("space_before") is not None:
        p.space_before = Pt(d["space_before"])
    runs = d.get("runs") or [(d.get("text", ""), {})]
    for text, o in runs:
        r = p.add_run()
        r.text = text
        f = r.font
        f.name = "Arial"
        f.size = Pt(o.get("size", d.get("size", 11)))
        f.bold = o.get("bold", d.get("bold", False))
        f.italic = o.get("italic", d.get("italic", False))
        f.color.rgb = o.get("color", d.get("color", DARK))


def txt(s, x, y, w, h, paras, anchor=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, 0)
    for i, d in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        _apply(p, tf, d)
    return tb


def shape_txt(shp, paras, anchor=MSO_ANCHOR.MIDDLE):
    tf = shp.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, Inches(0.06))
    for i, d in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        _apply(p, tf, d)


def header(s, kicker, title):
    txt(s, 0.6, 0.38, 12.1, 0.3, [dict(text=kicker.upper(), size=11.5, bold=True, color=CORAL)])
    txt(s, 0.6, 0.66, 12.1, 0.75, [dict(text=title, size=26, bold=True, color=DARK)])
    box(s, 0.6, 1.5, 1.5, 0.035, TEAL)
    PAGE[0] += 1
    txt(
        s,
        9.6,
        7.14,
        3.13,
        0.25,
        [
            dict(
                text=f"Digital Health Consultant Proposal · {PAGE[0]}",
                size=8,
                color=GREY,
                align=PP_ALIGN.RIGHT,
            )
        ],
    )


def card(s, x, y, w, h, border=True):
    return box(s, x, y, w, h, WHITE, LINE if border else None)


# ---------- S1 TITLE ----------
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, 13.333, 7.5, TEAL)
box(s, 0, 0, 0.22, 7.5, CORAL)
txt(
    s,
    1.1,
    1.95,
    10.5,
    0.35,
    [dict(text="TECHNICAL & FINANCIAL PROPOSAL", size=13, bold=True, color=CORAL)],
)
txt(
    s,
    1.1,
    2.4,
    10.9,
    1.7,
    [
        dict(text="MaHIS–iCHIS Integration for", size=37, bold=True, color=WHITE),
        dict(text="Maternal & Newborn Health", size=37, bold=True, color=WHITE),
    ],
)
txt(
    s,
    1.1,
    4.2,
    10.9,
    0.45,
    [
        dict(
            text="Technical Architecture & Costed Roadmap · ACHIEVE Project · Malawi",
            size=16,
            color=SAND,
        )
    ],
)
box(s, 1.1, 4.95, 3.6, 0.03, CORAL)
txt(
    s,
    1.1,
    6.35,
    10.9,
    0.75,
    [
        dict(
            text="Last Mile Health  ×  Ministry of Health & Sanitation",
            size=12,
            bold=True,
            color=WHITE,
            space_after=2,
        ),
        dict(text="Lilongwe · August 2026", size=11, color=SAND),
    ],
)

# ---------- S2 CONTEXT ----------
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, 13.333, 7.5, SAND)
header(s, "Context", "The ACHIEVE Project")
cards2 = [
    (
        "What ACHIEVE is",
        "US Department of State–funded initiative implemented by Pact and partners "
        "to accelerate sustainable reductions in maternal, neonatal and child mortality "
        "across pregnancy, childbirth, postnatal and early childhood services.",
    ),
    (
        "Where it works",
        "Karonga, Balaka, Thyolo and Zomba districts. Last Mile Health leads the design "
        "and implementation of iCHIS-driven interventions in Balaka district.",
    ),
    (
        "Objective 3 — system strengthening",
        "Strengthening emergency referral systems, commodity management and supply chain, "
        "enhanced use of data for decision-making, and preparedness for public health emergencies.",
    ),
    (
        "LMH Strategic Objectives",
        "SO1: Enhance iCHIS functionality and develop the architecture and costed roadmap "
        "for MaHIS–iCHIS integration for improved MNH outcomes.\n"
        "SO2: Build CHW capacity in Balaka on iCHIS and community-based maternal & neonatal care (CBMNC).",
    ),
]
for i, (h, b) in enumerate(cards2):
    cx = 0.6 + (i % 2) * 6.18
    cy = 1.85 + (i // 2) * 2.6
    card(s, cx, cy, 5.95, 2.42)
    txt(s, cx + 0.25, cy + 0.18, 5.45, 0.35, [dict(text=h, size=13, bold=True, color=TEAL)])
    txt(
        s,
        cx + 0.25,
        cy + 0.6,
        5.45,
        1.7,
        [dict(text=b.replace("\n", "\u2028"), size=10.5, color=DARK)],
    )

# ---------- S3 CHALLENGE ----------
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, 13.333, 7.5, SAND)
header(s, "The challenge", "Two Systems, One Continuum of Care — Not Yet Connected")
pts = [
    "MaHIS captures facility data; iCHIS captures community data — parallel worlds today.",
    "Duplicate entry of MNH service data into national reporting.",
    "Manual reconciliation delays reports and degrades quality.",
    "Referrals between HSAs and facilities are rarely tracked to closure.",
    "Decision-makers lack visibility of the full continuum of MNH care.",
]
for i, t in enumerate(pts):
    y = 2.0 + i * 0.92
    box(s, 0.6, y + 0.08, 0.14, 0.14, CORAL)
    txt(s, 0.92, y - 0.04, 5.9, 0.85, [dict(text=t, size=12, color=DARK)])
b1 = box(s, 7.2, 1.95, 2.5, 1.2, TEAL)
shape_txt(
    b1,
    [
        dict(text="iCHIS", size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER, space_after=2),
        dict(text="Community level — HSAs / CHWs", size=9.5, color=SAND, align=PP_ALIGN.CENTER),
    ],
)
b2 = box(s, 10.2, 1.95, 2.5, 1.2, TEAL)
shape_txt(
    b2,
    [
        dict(text="MaHIS", size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER, space_after=2),
        dict(text="Facility / HMIS", size=9.5, color=SAND, align=PP_ALIGN.CENTER),
    ],
)
g = box(s, 9.62, 2.35, 0.58, 0.4, CORAL)
shape_txt(g, [dict(text="GAP", size=9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)])
box(s, 8.28, 3.25, 0.34, 0.55, TEAL2, shape=MSO_SHAPE.DOWN_ARROW)
box(s, 11.29, 3.25, 0.34, 0.55, TEAL2, shape=MSO_SHAPE.DOWN_ARROW)
bb = box(s, 7.2, 3.95, 5.5, 1.2, DARK)
shape_txt(
    bb,
    [
        dict(
            text="Delayed, duplicated MNH reporting · weak referral closure · weak decisions",
            size=11,
            color=WHITE,
            align=PP_ALIGN.CENTER,
        )
    ],
)
txt(
    s,
    7.2,
    5.4,
    5.5,
    0.5,
    [
        dict(
            text="Integration closes this gap — one trusted flow of MNH data.",
            size=11,
            italic=True,
            color=GREY,
        )
    ],
)

# ---------- S4 UNDERSTANDING ----------
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, 13.333, 7.5, SAND)
header(s, "Scope", "Understanding of the Assignment")
rows = [
    (
        "Systems",
        "MaHIS (facility / HMIS) ↔ iCHIS (community), with DHIS2 as the national analytics backbone",
    ),
    (
        "Data domains",
        "CHW registrations · service delivery data · stock / commodity data · priority MNH indicators",
    ),
    (
        "Use cases",
        "Automatic submission of CHW monthly summaries into HMIS · two-way referral tracking · "
        "consolidated MNH dashboards",
    ),
    (
        "Standards frame",
        "National digital health architecture & governance standards; HL7 FHIR, OpenHIE profiles, "
        "DHIS2 data model",
    ),
    (
        "Constraints",
        "~6.5-week window · USD 3,000–4,000/month fee band · co-location in Lilongwe · "
        "Malawian national consultant",
    ),
]
for i, (lab, body) in enumerate(rows):
    y = 1.88 + i * 1.02
    ch = box(s, 0.6, y, 2.5, 0.78, TEAL)
    shape_txt(ch, [dict(text=lab, size=11.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)])
    card(s, 3.3, y, 9.43, 0.78)
    txt(
        s,
        3.55,
        y + 0.09,
        8.95,
        0.62,
        [dict(text=body, size=11.5, color=DARK)],
        anchor=MSO_ANCHOR.MIDDLE,
    )

# ---------- S5 METHODOLOGY ----------
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, 13.333, 7.5, SAND)
header(s, "Approach", "From Discovery to Donor-Ready Package in Five Steps")
steps = [
    (
        "01",
        "Discovery",
        "Document review · 8–10 interviews · 2 district site visits · vendor sessions",
        "Validated current-state assessment",
    ),
    (
        "02",
        "Architecture design",
        "Pattern options analysis · selection workshop with MoH interoperability team",
        "Endorsed integration architecture",
    ),
    (
        "03",
        "Requirements engineering",
        "FR/NFR workshops · data-mapping matrix · OpenAPI 3.0 draft · security review",
        "Technical requirements document",
    ),
    (
        "04",
        "Roadmap & costing",
        "Four-phase plan · People / Platforms / Process / TTV pillars · donor mapping",
        "Costed implementation roadmap",
    ),
    (
        "05",
        "Risk & consolidation",
        "P×I risk workshop · mitigation planning · executive summary · deck assembly",
        "Final package + presentation",
    ),
]
for i, (num, name, how, out) in enumerate(steps):
    cx = 0.6 + i * 2.455
    card(s, cx, 1.95, 2.31, 3.25)
    txt(s, cx + 0.18, 2.1, 1.0, 0.45, [dict(text=num, size=20, bold=True, color=CORAL)])
    txt(s, cx + 0.18, 2.62, 1.95, 0.55, [dict(text=name, size=12.5, bold=True, color=DARK)])
    txt(s, cx + 0.18, 3.2, 1.95, 1.25, [dict(text=how, size=9.5, color=GREY)])
    txt(
        s,
        cx + 0.18,
        4.5,
        1.95,
        0.62,
        [
            dict(
                runs=[("Output:  ", dict(bold=True, color=TEAL)), (out, dict(color=DARK))], size=9.5
            )
        ],
    )
strip = box(s, 0.6, 5.6, 12.13, 0.7, TEAL)
shape_txt(
    strip,
    [
        dict(
            text="Government-first   ·   Standards-based (FHIR / OpenHIE)   ·   "
            "Evidence-led   ·   Cost honesty   ·   Donor-ready outputs",
            size=12,
            bold=True,
            color=WHITE,
            align=PP_ALIGN.CENTER,
        )
    ],
)

# ---------- S6 ARCHITECTURE ----------
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, 13.333, 7.5, SAND)
header(s, "Indicative architecture", "A Standards-Based Interoperability Layer")
ichis = box(s, 0.8, 2.35, 3.1, 1.3, TEAL)
shape_txt(
    ichis,
    [
        dict(text="iCHIS", size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER, space_after=2),
        dict(text="Community level — HSAs / CHWs", size=9.5, color=SAND, align=PP_ALIGN.CENTER),
    ],
)
box(s, 3.98, 2.84, 0.62, 0.32, TEAL2, shape=MSO_SHAPE.RIGHT_ARROW)
il = box(s, 4.68, 2.35, 3.95, 1.3, CORAL)
shape_txt(
    il,
    [
        dict(
            text="Interoperability layer",
            size=14,
            bold=True,
            color=WHITE,
            align=PP_ALIGN.CENTER,
            space_after=2,
        ),
        dict(
            text="OpenHIM + FHIR APIs (OpenHIE-aligned)",
            size=9.5,
            color=WHITE,
            align=PP_ALIGN.CENTER,
        ),
    ],
)
box(s, 8.71, 2.84, 0.62, 0.32, TEAL2, shape=MSO_SHAPE.RIGHT_ARROW)
mahis = box(s, 9.41, 2.35, 3.1, 1.3, TEAL)
shape_txt(
    mahis,
    [
        dict(text="MaHIS", size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER, space_after=2),
        dict(text="Facility / HMIS", size=9.5, color=SAND, align=PP_ALIGN.CENTER),
    ],
)
box(s, 6.47, 3.75, 0.36, 0.48, TEAL2, shape=MSO_SHAPE.DOWN_ARROW)
dh = box(s, 5.06, 4.3, 3.2, 0.95, DARK)
shape_txt(
    dh,
    [
        dict(text="DHIS2", size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER, space_after=2),
        dict(text="National analytics & dashboards", size=9.5, color=SAND, align=PP_ALIGN.CENTER),
    ],
)
sec = box(s, 4.68, 5.5, 3.95, 0.5, WHITE, LINE)
shape_txt(
    sec,
    [
        dict(
            text="OAuth2 · TLS encryption · audit logging",
            size=10,
            color=GREY,
            align=PP_ALIGN.CENTER,
        )
    ],
)
txt(
    s,
    0.8,
    6.25,
    11.73,
    0.6,
    [
        dict(
            text="Starting hypothesis — confirmed or revised in Weeks 3–4 against vendor capability, "
            "infrastructure and governance findings. File-based exchange documented as fallback.",
            size=10.5,
            italic=True,
            color=GREY,
        )
    ],
)

# ---------- S7 DELIVERABLES ----------
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, 13.333, 7.5, SAND)
header(s, "Deliverables", "Five Decision-Grade Products")
delivs = [
    (
        "D1",
        "Inception Report",
        "End Week 2",
        "Scope, RACI & workplan signed off; ≥10 risks logged; repository live.",
        False,
    ),
    (
        "D2",
        "Technical Architecture & Requirements",
        "End Week 4",
        "Validated current state; ≥30 FRs, ≥15 measurable NFRs; OpenAPI draft; compliance matrix.",
        False,
    ),
    (
        "D3",
        "Costed Implementation Roadmap",
        "End Week 6",
        "Four phases with gates; monthly costing by pillar; CAPEX/OPEX split; donor matrix.",
        True,
    ),
    (
        "D4",
        "Risk Analysis & Mitigation Plan",
        "Week 7",
        "≥20 risks across four categories; every High/Medium risk owned with trigger.",
        False,
    ),
    (
        "D5",
        "Final Package & Presentation",
        "30 Sep",
        "Executive summary ≤2 pages; annexes; 20-slide donor deck; formal sign-off.",
        False,
    ),
]
for i, (num, name, due, acc, core) in enumerate(delivs):
    cx = 0.6 + i * 2.455
    c = card(s, cx, 2.0, 2.31, 4.15, border=not core)
    if core:
        c.line.color.rgb = CORAL
        c.line.width = Pt(2)
        tag = box(s, cx, 1.78, 1.5, 0.32, CORAL)
        shape_txt(
            tag, [dict(text="CORE PRODUCT", size=8, bold=True, color=WHITE, align=PP_ALIGN.CENTER)]
        )
    txt(s, cx + 0.18, 2.18, 1.0, 0.4, [dict(text=num, size=17, bold=True, color=CORAL)])
    txt(s, cx + 0.18, 2.62, 1.95, 0.85, [dict(text=name, size=11.5, bold=True, color=DARK)])
    ch = box(s, cx + 0.18, 3.55, 1.35, 0.34, SAND)
    shape_txt(ch, [dict(text=due, size=8.5, bold=True, color=TEAL, align=PP_ALIGN.CENTER)])
    txt(s, cx + 0.18, 4.05, 1.95, 1.9, [dict(text=acc, size=9, color=GREY)])

# ---------- S8 COSTED ROADMAP ----------
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, 13.333, 7.5, SAND)
header(s, "Core product", "The Costed Implementation Roadmap")
card(s, 0.6, 1.9, 4.4, 4.25)
txt(s, 0.85, 2.05, 3.9, 0.35, [dict(text="Four phases", size=13, bold=True, color=TEAL)])
phases = [
    (
        "Phase 0 · Preparation & Governance",
        "Months 1–2",
        "Alignment, working group, data-sharing agreements",
    ),
    (
        "Phase 1 · Design & Prototyping",
        "Months 3–5",
        "Data mapping, limited-site pilot build, testing",
    ),
    (
        "Phase 2 · Pilot Rollout",
        "Months 6–11",
        "District deployment, training, monitoring & refinement",
    ),
    (
        "Phase 3 · Scale-Up & Institutionalisation",
        "Months 12–18+",
        "National rollout, SOPs, handover to MoH",
    ),
]
for i, (nm, dur, ds) in enumerate(phases):
    y = 2.5 + i * 0.92
    txt(
        s,
        0.85,
        y,
        2.95,
        0.8,
        [
            dict(text=nm, size=10, bold=True, color=DARK, space_after=1),
            dict(text=ds, size=8.5, color=GREY),
        ],
    )
    ch = box(s, 3.85, y + 0.03, 1.0, 0.3, SAND)
    shape_txt(ch, [dict(text=dur, size=8, bold=True, color=TEAL, align=PP_ALIGN.CENTER)])
pillars = [
    (
        "People",
        "Integration architect, developers, data engineer, PM & M&E, trainers, "
        "TWG coordination — person-months × local rates",
    ),
    (
        "Platforms",
        "Middleware / API management licences, hosting & storage, security tooling, "
        "maintenance retainers",
    ),
    (
        "Process",
        "Mapping & terminology harmonisation, QA environments, legal & DSA reviews, "
        "documentation, change management",
    ),
    (
        "Time-to-Value",
        "Efficiency narrative — reduced duplication, faster reporting — and the "
        "quantified cost of delay if integration stalls",
    ),
]
for i, (nm, body) in enumerate(pillars):
    px = 5.25 + (i % 2) * 3.86
    py = 1.9 + (i // 2) * 2.22
    card(s, px, py, 3.62, 2.03)
    txt(s, px + 0.2, py + 0.15, 3.2, 0.35, [dict(text=nm, size=12.5, bold=True, color=CORAL)])
    txt(s, px + 0.2, py + 0.55, 3.22, 1.4, [dict(text=body, size=9.5, color=DARK)])
strip = box(s, 0.6, 6.35, 12.13, 0.55, SAND)
shape_txt(
    strip,
    [
        dict(
            text="Monthly granularity · CAPEX/OPEX split · 15% contingency · benchmarked "
            "vs regional projects · mapped to Global Fund / USAID / Gavi windows",
            size=10,
            bold=True,
            color=TEAL,
            align=PP_ALIGN.CENTER,
        )
    ],
)

# ---------- S9 ROADMAP CHEVRONS ----------
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, 13.333, 7.5, SAND)
header(s, "Implementation roadmap", "Phased Path to National Scale")
chev = [
    (
        "Phase 0 · Preparation & Governance",
        "Months 1–2",
        [
            "Stakeholder alignment",
            "Technical working group established",
            "Data-sharing agreements drafted",
        ],
        "Gate: governance endorsed",
    ),
    (
        "Phase 1 · Design & Prototyping",
        "Months 3–5",
        ["Detailed data mapping", "Limited-site pilot development", "Initial testing & validation"],
        "Gate: pilot ready",
    ),
    (
        "Phase 2 · Pilot Rollout",
        "Months 6–11",
        [
            "Deploy in selected districts/facilities",
            "Train users & technical staff",
            "Monitor, troubleshoot, refine",
        ],
        "Gate: go/no-go to scale",
    ),
    (
        "Phase 3 · Scale-Up & Institutionalisation",
        "Months 12–18+",
        [
            "National / multi-region rollout",
            "SOPs, job aids, routine operations",
            "Handover to government",
        ],
        "Gate: sustainable handover",
    ),
]
fills = [TEAL, TEAL2, TEAL, TEAL2]
for i, (nm, dur, acts, gate) in enumerate(chev):
    cx = 0.6 + i * 3.07
    cv = box(s, cx, 1.95, 3.35, 1.05, fills[i], shape=MSO_SHAPE.CHEVRON)
    shape_txt(
        cv,
        [
            dict(text=nm, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER, space_after=1),
            dict(text=dur, size=9, color=SAND, align=PP_ALIGN.CENTER),
        ],
    )
    txt(
        s,
        cx + 0.12,
        3.25,
        2.8,
        1.9,
        [dict(text="• " + a, size=9.5, color=DARK, space_after=4) for a in acts],
    )
    txt(s, cx + 0.12, 5.3, 2.8, 0.5, [dict(text=gate, size=9.5, bold=True, color=CORAL)])
txt(
    s,
    0.6,
    6.35,
    12.13,
    0.5,
    [
        dict(
            text="Durations indicative — validated and re-baselined during Weeks 5–6 of the consultancy.",
            size=10.5,
            italic=True,
            color=GREY,
        )
    ],
)

# ---------- S10 WORK PLAN ----------
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, 13.333, 7.5, SAND)
header(s, "Work plan", "Six and a Half Weeks, Seven Checkpoints")
segs = [
    (
        3.53,
        "W1–2 · Inception & Discovery",
        TEAL,
        "Kick-off · interviews · 2 district visits · discovery synthesis",
        "CP1 baseline · CP2 discovery validation",
    ),
    (
        3.53,
        "W3–4 · Architecture & Requirements",
        TEAL2,
        "Pattern selection · FR/NFR workshops · data mapping · API spec draft · clinical validation",
        "CP3 architecture review · CP4 requirements sign-off",
    ),
    (
        3.53,
        "W5–6 · Roadmap & Costing",
        CORAL,
        "Phasing · four-pillar costing model · donor alignment · validation workshop",
        "CP5 roadmap sign-off",
    ),
    (
        1.24,
        "W7 · Risk & Close",
        DARK,
        "Risk workshop · package assembly · final review · handover",
        "CP6 package review · CP7 formal acceptance",
    ),
]
x = 0.6
for w, lab, col, acts, cps in segs:
    sg = box(s, x, 2.1, w, 0.85, col)
    shape_txt(sg, [dict(text=lab, size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)])
    txt(s, x, 3.15, w, 1.35, [dict(text=acts, size=9.5, color=DARK)])
    txt(s, x, 4.6, w, 0.75, [dict(text=cps, size=9, bold=True, color=CORAL)])
    x += w + 0.1
cad = box(s, 0.6, 5.6, 12.13, 1.1, WHITE, LINE)
shape_txt(
    cad,
    [
        dict(
            text="Cadence & quality:   daily stand-up · weekly written status report (Fri) · "
            "bi-weekly steering committee · version control v0.x → v1.0 FINAL · "
            "peer review before every formal submission",
            size=11,
            color=DARK,
            align=PP_ALIGN.CENTER,
        )
    ],
)

# ---------- S11 GOVERNANCE ----------
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, 13.333, 7.5, SAND)
header(s, "Governance & stakeholders", "Co-Located With the Decision-Makers")
card(s, 0.6, 1.9, 5.6, 4.9)
txt(s, 0.85, 2.08, 5.1, 0.35, [dict(text="Engagement governance", size=13, bold=True, color=TEAL)])
gov = [
    (
        "Reporting line",
        "Digital Health Specialist, Last Mile Health — with close technical coordination "
        "with the Head, Systems Architecture & Security Unit, MoH Digital Health Division",
    ),
    ("Cadence", "Daily stand-up · weekly status report · bi-weekly steering committee"),
    (
        "Quality",
        "Seven checkpoints (CP1–CP7) with go/no-go criteria; traceability from requirements → "
        "architecture → roadmap → cost → risk",
    ),
    ("Change control", "Scope changes only through steering-committee impact assessment"),
]
yy = 2.55
for h, b in gov:
    txt(
        s,
        0.85,
        yy,
        5.1,
        1.05,
        [
            dict(text=h.upper(), size=9, bold=True, color=CORAL, space_after=2),
            dict(text=b, size=10, color=DARK),
        ],
    )
    yy += 1.08
card(s, 6.45, 1.9, 6.28, 4.9)
txt(
    s,
    6.7,
    2.08,
    5.8,
    0.35,
    [dict(text="Stakeholders engaged weekly", size=13, bold=True, color=TEAL)],
)
chips = [
    "MoH Digital Health Division",
    "Reproductive Health Unit",
    "District DHMTs (pilot districts)",
    "HSAs & CHWs",
    "Development partners — Global Fund, USAID, Gavi, UNICEF",
    "System vendors — iCHIS (Baobab) & MaHIS",
    "LMH country & technical teams",
]
for i, c in enumerate(chips):
    cx = 6.7 + (i % 2) * 2.95
    cy = 2.55 + (i // 2) * 1.0
    cp = box(s, cx, cy, 2.8, 0.85, SAND)
    shape_txt(cp, [dict(text=c, size=9.5, color=DARK, align=PP_ALIGN.CENTER)])

# ---------- S12 RISKS ----------
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, 13.333, 7.5, SAND)
header(s, "Risk management", "Named Risks, Owned Mitigations — Reviewed Weekly")
risks = [
    (
        "MoH staff availability constrained by competing priorities",
        "HIGH",
        "Pre-booked calendars; sponsor escalation; flexible scheduling",
    ),
    (
        "Vendor API access or sandbox delayed",
        "MED–HIGH",
        "Early MoH directive to vendors; contractual clauses; file-exchange fallback",
    ),
    (
        "Scope creep beyond the MNH integration core",
        "MEDIUM",
        "Inception baseline; formal change-control board",
    ),
    (
        "Donor funding misaligned with phased roadmap",
        "MED–HIGH",
        "Donor mapping in Week 6; modular phasing enables partial funding",
    ),
    (
        "Existing data quality undermines integration value",
        "HIGH",
        "Data-quality assessment in discovery; cleansing sprint budgeted in Phase 1",
    ),
    (
        "Security/compliance gaps block future deployment",
        "LOW × CRITICAL",
        "Early MoH ICT security review; privacy-by-design; DPA templates ready",
    ),
]
chip_col = {"HIGH": CORAL, "MED–HIGH": CORAL, "MEDIUM": TEAL2, "LOW × CRITICAL": GREY}
for i, (r, sev, m) in enumerate(risks):
    y = 1.9 + i * 0.84
    card(s, 0.6, y, 12.13, 0.74)
    txt(
        s,
        0.85,
        y + 0.08,
        4.9,
        0.6,
        [dict(text=r, size=10.5, bold=False, color=DARK)],
        anchor=MSO_ANCHOR.MIDDLE,
    )
    chp = box(s, 5.9, y + 0.19, 1.5, 0.36, chip_col[sev])
    shape_txt(chp, [dict(text=sev, size=8.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)])
    txt(s, 7.6, y + 0.08, 4.95, 0.6, [dict(text=m, size=9.5, color=GREY)], anchor=MSO_ANCHOR.MIDDLE)

# ---------- S13 INVESTMENT ----------
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, 13.333, 7.5, SAND)
header(s, "Investment case", "Transparent Fees, Realistic Reimbursables")
card(s, 0.6, 1.9, 5.6, 3.4)
txt(s, 0.85, 2.08, 5.1, 0.35, [dict(text="Professional fees", size=13, bold=True, color=TEAL)])
txt(
    s,
    0.85,
    2.55,
    5.1,
    2.6,
    [
        dict(text="USD 3,500 per month", size=22, bold=True, color=DARK, space_after=4),
        dict(
            text="Within the advertised USD 3,000–4,000 band.", size=10.5, color=DARK, space_after=8
        ),
        dict(
            text="≈ USD 5,400 total professional fees across the 6.5-week engagement.",
            size=10.5,
            color=DARK,
            space_after=8,
        ),
        dict(
            text="Excludes withholding taxes per applicable law.", size=9.5, italic=True, color=GREY
        ),
    ],
)
card(s, 6.45, 1.9, 6.28, 3.4)
txt(
    s,
    6.7,
    2.08,
    5.8,
    0.35,
    [dict(text="Indicative reimbursables (USD)", size=13, bold=True, color=TEAL)],
)
items = [
    ("Local travel — 2 district visits", "400"),
    ("Workshops (venue, refreshments × 4)", "300"),
    ("Communications / internet", "150"),
    ("Printing & stationery", "100"),
    ("Contingency (~10%)", "635"),
]
yy = 2.55
for lab, amt in items:
    txt(s, 6.7, yy, 4.4, 0.3, [dict(text=lab, size=10.5, color=DARK)])
    txt(
        s,
        11.3,
        yy,
        1.2,
        0.3,
        [dict(text=amt, size=10.5, bold=True, color=DARK, align=PP_ALIGN.RIGHT)],
    )
    yy += 0.42
box(s, 6.7, yy + 0.02, 5.8, 0.02, LINE)
txt(
    s,
    6.7,
    yy + 0.12,
    3.4,
    0.35,
    [dict(text="Total estimated engagement", size=10.5, bold=True, color=TEAL)],
)
txt(
    s,
    10.5,
    yy + 0.12,
    2.0,
    0.35,
    [dict(text="6,985", size=12, bold=True, color=CORAL, align=PP_ALIGN.RIGHT)],
)
strip = box(s, 0.6, 5.65, 12.13, 0.95, TEAL)
shape_txt(
    strip,
    [
        dict(
            text="One roadmap, multiple funding doors — formatted for Global Fund RSSH, "
            "USAID Digital Health, Gavi HSS and World Bank concept notes.",
            size=12,
            bold=True,
            color=WHITE,
            align=PP_ALIGN.CENTER,
        )
    ],
)

# ---------- S14 WHY THIS CONSULTANT ----------
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, 13.333, 7.5, SAND)
header(s, "Qualifications", "Built for This Exact Brief")
col1 = [
    "Progressive LMIC experience designing and costing digital-health system integrations",
    "Hands-on with national HIS platforms — DHIS2, OpenMRS, CommCare/ODK, iCHIS-class tools",
    "Working command of interoperability standards — HL7 FHIR, OpenHIE, API design",
    "Data-governance track record — data-sharing agreements, privacy and security compliance",
]
col2 = [
    "Costing prepared for Global Fund, USAID, Gavi and World Bank audiences",
    "Facilitated multi-stakeholder MoH consultations to consensus",
    "Translates technical concepts for non-technical audiences",
    "Excellent English; based in Lilongwe for full-time co-location",
]
for ci, col in enumerate((col1, col2)):
    for bi, t in enumerate(col):
        x = 0.6 + ci * 6.28
        y = 2.0 + bi * 0.98
        box(s, x, y + 0.07, 0.14, 0.14, CORAL)
        txt(s, x + 0.32, y - 0.05, 5.7, 0.9, [dict(text=t, size=11.5, color=DARK)])
ban = box(s, 0.6, 6.0, 12.13, 0.75, WHITE, LINE)
shape_txt(
    ban,
    [
        dict(
            runs=[
                ("Differentiator:  ", dict(bold=True, color=CORAL)),
                (
                    "familiarity with Malawi's digital-health ecosystem and Ministry "
                    "of Health digital-health priorities.",
                    dict(color=DARK),
                ),
            ],
            size=12,
            align=PP_ALIGN.CENTER,
        )
    ],
)

# ---------- S15 SUSTAINABILITY ----------
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, 13.333, 7.5, SAND)
header(s, "Sustainability", "Handover Is the Deliverable")
card(s, 0.6, 1.9, 5.95, 3.7)
txt(s, 0.85, 2.08, 5.45, 0.35, [dict(text="Handover pack", size=13, bold=True, color=TEAL)])
hp = [
    "Editable sources — Word, Excel, PowerPoint",
    "Costing model with assumptions tab (unlocked)",
    "Living risk register with owners and triggers",
    "OpenAPI specs and data-mapping matrices",
    "Decision register and meeting logs",
]
for i, t in enumerate(hp):
    txt(
        s,
        0.85,
        2.55 + i * 0.58,
        5.45,
        0.5,
        [dict(runs=[("✓  ", dict(bold=True, color=CORAL)), (t, dict(color=DARK))], size=10.5)],
    )
card(s, 6.78, 1.9, 5.95, 3.7)
txt(
    s,
    7.03,
    2.08,
    5.45,
    0.35,
    [dict(text="Mechanisms that outlast the consultancy", size=13, bold=True, color=TEAL)],
)
sm = [
    "MoH ownership board — quarterly steering",
    "Technical working group — monthly coordination",
    "Recurrent budget-absorption tracking (Phase 1 onward)",
    "Vendor SLAs embedded in Phase-1 contracts",
    "Annual roadmap review and refresh",
]
for i, t in enumerate(sm):
    txt(
        s,
        7.03,
        2.55 + i * 0.58,
        5.45,
        0.5,
        [dict(runs=[("✓  ", dict(bold=True, color=CORAL)), (t, dict(color=DARK))], size=10.5)],
    )
st = box(s, 0.6, 5.9, 12.13, 0.8, SAND)
shape_txt(
    st,
    [
        dict(
            runs=[
                ("Success test:  ", dict(bold=True, color=CORAL)),
                (
                    "the MoH lead can present the roadmap accurately — without the "
                    "consultant in the room.",
                    dict(color=DARK, italic=True),
                ),
            ],
            size=12,
            align=PP_ALIGN.CENTER,
        )
    ],
)

# ---------- S16 NEXT STEPS ----------
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, 13.333, 7.5, TEAL)
box(s, 0, 0, 0.22, 7.5, CORAL)
txt(s, 1.1, 1.0, 10.5, 0.35, [dict(text="NEXT STEPS", size=13, bold=True, color=CORAL)])
txt(
    s,
    1.1,
    1.4,
    10.9,
    0.8,
    [dict(text="Ready to Start Within Days of Signature", size=30, bold=True, color=WHITE)],
)
steps = [
    ("1", "Approve proposal and countersign the engagement letter"),
    ("2", "Confirm MoH workspace access, badging and stakeholder calendars (Week −1)"),
    ("3", "Kick-off meeting with LMH and the MoH Digital Health Division"),
    ("4", "First deliverable draft — Inception Report — by end of Week 2"),
]
for i, (n, t) in enumerate(steps):
    y = 2.75 + i * 0.95
    cir = box(s, 1.1, y, 0.5, 0.5, CORAL, shape=MSO_SHAPE.OVAL)
    shape_txt(cir, [dict(text=n, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)])
    txt(s, 1.85, y + 0.05, 10.2, 0.5, [dict(text=t, size=14, color=WHITE)])
box(s, 1.1, 6.55, 3.6, 0.03, CORAL)
txt(
    s,
    1.1,
    6.75,
    10.9,
    0.4,
    [dict(text="[Consultant Name] · Lilongwe, Malawi · [email address]", size=11, color=SAND)],
)

out = "proposal-deliverables/Digital-Health-Consultant-Proposal-Slides.pptx"
prs.save(out)
print("saved:", out, "| slides:", len(prs.slides.__iter__.__self__._sldIdLst))
