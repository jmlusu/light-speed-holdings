#!/usr/bin/env python3
"""Pipeline for AI agent slide deck production.

Separates intellectual labor (Phase 1: content generation) from visual rendering (Phase 2: layout engine).
"""

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class SlideSpec:
    """Represents a single slide in the deck."""

    title: str
    bullets: List[str] = field(default_factory=list)
    description: str = ""
    # Metadata dict - can hold additional info like speaker notes, etc.
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PresentationSpec:
    """Complete presentation specification generated in Phase 1."""

    deck_type: str  # "investor_pitch", "board_meeting", "keynote", "training"
    topic: str
    audience: str
    objective: str
    narrative: str
    slides: List[SlideSpec] = field(default_factory=list)


def generate_content_from_brief(
    brief: Dict[str, Any],
    deck_type: str = "investor_pitch",
    registry_path: str = "company-registry.yaml",
) -> PresentationSpec:
    """Phase 1: Generate presentation content from brief.

    Creates the PresentationSpec with slide structure, bullets, speaker notes.
    Separates intellectual labor from visual rendering.

    Args:
        brief: Dictionary with topic, audience, objective, narrative, deck_type
        deck_type: One of "investor_pitch", "board_meeting", "keynote", "training"
        registry_path: Path to company-registry.yaml for real metrics
    """
    topic = brief.get("topic", "Unknown Topic")
    audience = brief.get("audience", "Unknown Audience")
    objective = brief.get("objective", "Unknown Objective")
    narrative = brief.get("narrative", "")

    # Determine slide count based on deck type
    if deck_type == "investor_pitch":
        slide_count = 14
    elif deck_type == "board_meeting":
        slide_count = 10
    elif deck_type == "keynote":
        slide_count = 13
    elif deck_type == "training":
        slide_count = 8
    else:
        slide_count = 10

    # Generate slide specs
    slides = _build_slides(topic, audience, objective, narrative, deck_type, slide_count)

    return PresentationSpec(
        deck_type=deck_type,
        topic=topic,
        audience=audience,
        objective=objective,
        narrative=narrative,
        slides=slides,
    )


def create_deck_from_brief(
    brief: Dict[str, Any],
    output_dir: str = ".opencode/agents",
    deck_type: str = "investor_pitch",
    registry_path: str = "company-registry.yaml",
) -> List[str]:
    """Generate a complete presentation deck.

    Phase 1: Generate content (narrative, slide sequence, bullets, speaker notes)
    Phase 2: Render layout (Marp Markdown, PptxGenJS JSON, PPTX with brand tokens)

    Returns list of output file paths.
    """
    # Phase 1: Generate presentation spec
    spec = generate_content_from_brief(brief, deck_type, registry_path)

    # Phase 2: Render the deck
    output_files = _render_deck(spec, output_dir, deck_type)

    return output_files


def _build_slides(
    topic: str, audience: str, objective: str, narrative: str, deck_type: str, slide_count: int
) -> List[SlideSpec]:
    """Build the slide specification list."""

    # Base slide titles for different deck types
    title_templates = {
        "investor_pitch": [
            "Executive Summary",
            "Problem & Market",
            "Solution & Product",
            "Business Model",
            "Go-to-Market Strategy",
            "Competitive Landscape",
            "Trajectory & Milestones",
            "Key Decisions Required",
            "Customer Success Report",
            "Financial Projections",
            "Team & Advisors",
            "Key Metrics & KPIs",
            "Next Steps",
            "Closing",
        ],
        "board_meeting": [
            "Operational Update",
            "Financial Performance",
            "Key Metrics & KPIs",
            "Product Roadmap",
            "Customer Success",
            "Competitive Landscape",
            "Risk & Governance",
            "Key Decisions Required",
            "Strategic Priorities",
            "Closing",
        ],
        "keynote": [
            "Opening & Vision",
            "Market Opportunity",
            "Our Solution",
            "Customer Success Stories",
            "Competitive Differentiation",
            "Technology & Innovation",
            "Roadmap & Milestones",
            "Key Decisions Required",
            "Financial Overview",
            "Team & Execution",
            "Future Outlook",
            "Call to Action",
            "Closing",
        ],
        "training": [
            "Introduction & Objectives",
            "Module 1: Core Concepts",
            "Module 2: Key Processes",
            "Module 3: Best Practices",
            "Hands-on Exercise",
            "Q&A Session",
            "Key Decisions Required",
            "Wrap-up & Next Steps",
        ],
    }

    titles = title_templates.get(deck_type, title_templates["board_meeting"])

    # Ensure we have enough titles
    if slide_count > len(titles):
        # Repeat titles if needed
        while len(titles) < slide_count:
            titles.extend(title_templates.get(deck_type, title_templates["board_meeting"]))
        titles = titles[:slide_count]

    # Generate slide specs
    slides = []
    for i in range(slide_count):
        title = titles[i] if i < len(titles) else f"Slide {i + 1}"

        # Generate bullets based on slide position and content
        bullets = _generate_bullets(title, narrative, deck_type, i)

        # Generate description based on slide type
        description = _generate_description(title, deck_type, i)

        slides.append(
            SlideSpec(
                title=title,
                bullets=bullets,
                description=description,
            )
        )

    return slides


def _generate_bullets(title: str, narrative: str, deck_type: str, index: int) -> List[str]:
    """Generate bullet points for a slide."""
    # Base bullet templates per slide type and position
    bullet_templates = {
        "investor_pitch": {
            0: ["Executive summary highlighting market opportunity and unique value proposition"],
            1: ["Large and growing total addressable market (TAM > $X billion)"],
            2: ["Core product/service solving specific customer pain point"],
            3: ["Revenue model: recurring + transaction-based streams"],
            4: ["Go-to-market: strategic partnerships + direct sales approach"],
            5: ["Competitive moat and sustainable differentiators"],
            6: ["Trajectory: Y1 milestones + Y2 growth targets"],
            7: ["Key client pilots authorized; governance gated on G1-G4 + MSA/DPA"],
            8: ["SaaS pricing band approved: $49-$299/mo for Offer E"],
            9: ["Customer success metrics: retention > 90%, NPS > 50"],
            10: ["Y1 revenue target: $120K ARR consistent with finance KPI"],
            14: ["Founder-led team with relevant industry experience"],
            11: ["ATC >90% velocity, correction ratio within target"],
            12: ["Next fundraise: before next round, $120K ARR run-rate"],
            13: ["Aspire. Act. Achieve. - closing strategic thesis"],
        },
        "board_meeting": {
            0: ["Quarterly operational update and strategic direction"],
            1: ["Revenue performance vs. board-approved targets"],
            2: ["Key performance indicators and trend analysis"],
            3: ["Product roadmap milestones and delivery timeline"],
            4: ["Customer success metrics and retention rates"],
            5: ["Competitive positioning and market share analysis"],
            6: ["Risk assessment and governance framework update"],
            7: ["Key decisions requiring board authorization"],
            8: ["Strategic priorities for next quarter"],
            9: ["Closing: next meeting date and strategic thrust"],
        },
        "keynote": {
            0: ["Opening vision: why this moment matters now"],
            1: ["Market opportunity size and growth trajectory"],
            2: ["Our solution: unique approach and value proposition"],
            3: ["Customer success: real-world results and case studies"],
            4: ["Competitive landscape and our differentiators"],
            5: ["Technology innovation and competitive advantage"],
            6: ["Roadmap: key milestones over coming quarters"],
            7: ["Decisions needed from leadership today"],
            8: ["Financial overview: unit economics and trajectory"],
            9: ["Team capabilities and execution capacity"],
            10: ["Future outlook: where we're headed"],
            11: ["Call to action: what happens next"],
            12: ["Closing thesis: aspirational but grounded"],
        },
        "training": {
            0: ["Session objectives and expected outcomes"],
            1: ["Core concepts: foundational knowledge"],
            2: ["Key processes: how things work day-to-day"],
            3: ["Best practices: lessons learned and patterns"],
            4: ["Hands-on exercise: apply what you've learned"],
            5: ["Q&A session: address questions and clarify concepts"],
            6: ["Decisions required from participants"],
            7: ["Wrap-up and next steps for continued learning"],
        },
    }

    templates = bullet_templates.get(deck_type, bullet_templates["board_meeting"])
    t = templates.get(index, [])

    # If no specific bullets for this slide, generate generic ones
    if not t:
        t = [
            f"Key point {index + 1} related to {title.lower()}",
            f"Supporting detail for {title.lower()}",
        ]

    return list(t)


def _generate_description(title: str, deck_type: str, index: int) -> str:
    """Generate description text for a slide."""
    descriptions = {
        "investor_pitch": {
            0: "Executive summary highlighting market opportunity and unique value proposition",
            1: "Large and growing total addressable market (TAM > $X billion)",
            2: "Core product/service solving specific customer pain point",
            3: "Revenue model: recurring + transaction-based streams",
            4: "Go-to-market: strategic partnerships + direct sales approach",
            5: "Competitive moat and sustainable differentiators",
            6: "Trajectory: Y1 milestones + Y2 growth targets",
            7: "Key client pilots authorized; governance gated on G1-G4 + MSA/DPA",
            8: "SaaS pricing band approved: $49-$299/mo for Offer E (AI Company Builder)",
            9: "Customer success metrics: retention > 90%, NPS > 50",
            10: "Y1 revenue target: $120K ARR consistent with finance KPI",
            14: "Founder-led team with relevant industry experience",
            11: "Next fundraise: before next round, $120K ARR run-rate",
            12: "Aspire. Act. Achieve. - closing strategic thesis",
            13: "Closing slide sets the date for the next meeting and reinforces the brand thesis",
            15: "Closing slide sets the date for the next meeting and reinforces the brand thesis",
        },
        "board_meeting": {
            0: "Quarterly operational update and strategic direction",
            1: "Revenue performance vs. board-approved targets",
            2: "Key performance indicators and trend analysis",
            3: "Product roadmap milestones and delivery timeline",
            4: "Customer success metrics and retention rates",
            5: "Competitive positioning and market share analysis",
            6: "Risk assessment and governance framework update",
            7: "Key decisions requiring board authorization",
            8: "Strategic priorities for next quarter",
            9: "Closing: next meeting date and strategic thrust",
        },
        "keynote": {
            0: "Opening vision: why this moment matters now",
            1: "Market opportunity size and growth trajectory",
            2: "Our solution: unique approach and value proposition",
            3: "Customer success: real-world results and case studies",
            4: "Competitive landscape and our differentiators",
            5: "Technology innovation and competitive advantage",
            6: "Roadmap: key milestones over coming quarters",
            7: "Decisions needed from leadership today",
            14: "Financial overview: unit economics and trajectory",
            10: "Team capabilities and execution capacity",
            8: "Future outlook: where we're headed",
            9: "Call to action: what happens next",
            13: "Closing: strategic vision and next steps",
            11: "Closing slide sets the date for the next meeting and reinforces the brand thesis",
            12: "Closing slide sets the date for the next meeting and reinforces the brand thesis",
        },
        "training": {
            0: "Session objectives and expected outcomes",
            1: "Core concepts: foundational knowledge",
            2: "Key processes: how things work day-to-day",
            3: "Best practices: lessons learned and patterns",
            4: "Hands-on exercise: apply what you've learned",
            5: "Q&A: address questions and clarify concepts",
            6: "Decisions required from participants",
            7: "Wrap-up and next steps for continued learning",
        },
    }

    desc_templates = descriptions.get(deck_type, descriptions["board_meeting"])
    return desc_templates.get(index, f"Slide {index + 1} content")


def _render_deck(spec: PresentationSpec, output_dir: str, deck_type: str) -> List[str]:
    """Phase 2: Render the deck into output files.

    Generates:
    1. Marp Markdown (.md) - for visual verification/PNG export
    2. PptxGenJS JSON (.json) - deterministic PPTX rendering spec
    3. PPTX (.pptx) - final brand-token-enforced PowerPoint
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    output_files = []

    # Generate Marp Markdown
    marp_path = os.path.join(
        output_dir, f"deck_{spec.deck_type}_{spec.topic[:20].replace(' ', '_')}.md"
    )
    _write_marp_md(marp_path, spec)
    output_files.append(marp_path)

    # Generate PptxGenJS JSON
    pptxgen_path = os.path.join(
        output_dir, f"deck_{spec.deck_type}_{spec.topic[:20].replace(' ', '_')}.json"
    )
    _write_pptxgen_json(pptxgen_path, spec)
    output_files.append(pptxgen_path)

    # Generate PPTX (would use python-pptx with brand token enforcement)
    # pptx_path = os.path.join(output_dir, f"deck_{spec.deck_type}_{spec.topic[:20].replace(' ', '_')}.pptx")
    # _write_pptx(pptx_path, spec)
    # output_files.append(pptx_path)

    # For now return Marp and JSON; PPTX generation is handled by CLI
    return output_files


def _write_marp_md(path: str, spec: PresentationSpec) -> None:
    """Write Marp Markdown file."""
    lines = []
    lines.append("---\n")
    lines.append("marp: true\n")
    lines.append("---\n\n")

    # Title slide
    lines.append(f"# {spec.topic}\n\n")
    lines.append(f"*{spec.audience}*\n\n")

    # Content slides
    for slide in spec.slides:
        lines.append(f"## {slide.title}\n\n")
        if slide.bullets:
            for bullet in slide.bullets:
                lines.append(f"- {bullet}\n")
        if slide.description:
            lines.append(f"{slide.description}\n\n")
        if slide.metadata.get("speaker_notes"):
            lines.append(f"*Speaker notes: {slide.metadata['speaker_notes']}*\n\n")

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)


def _write_pptxgen_json(path: str, spec: PresentationSpec) -> None:
    """Write PptxGenJS JSON rendering specification."""
    # Brand tokens enforcement
    brand_tokens = {
        "navy": "#070A40",
        "red": "#E63946",
        "cyan": "#00BFFF",
        "grey": "#F2F2F2",
    }

    # Build slide layouts
    slides_json = []
    for i, slide in enumerate(spec.slides):
        slide_data = {
            "title": slide.title,
            "bullets": slide.bullets,
            "description": slide.description,
            "brand_tokens": brand_tokens,
            "slide_index": i,
        }
        slides_json.append(slide_data)

    spec_data = {
        "deck_type": spec.deck_type,
        "topic": spec.topic,
        "audience": spec.audience,
        "objective": spec.objective,
        "narrative": spec.narrative,
        "slides": slides_json,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(spec_data, f, indent=2, ensure_ascii=False)


# Legacy function names for backward compatibility
generate_presentation_phases = generate_content_from_brief
create_deck = create_deck_from_brief
