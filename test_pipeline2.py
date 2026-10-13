#!/usr/bin/env python3
"""Test the full pipeline end-to-end"""
import sys
sys.path.insert(0, '.')

from ai_company.generator import AgentGenerator

g = AgentGenerator()

# Test generate_presentation_phases
brief = {
    "topic": "AI Company Builder",
    "audience": "Investors",
    "objective": "Raise $5M Series A",
    "narrative": "Building an AI company platform for agent hierarchies",
}

spec = g.generate_presentation_phases(brief)
print(f"PresentationSpec created:")
print(f"  Deck type: {spec.deck_type}")
print(f"  Topic: {spec.topic}")
print(f"  Audience: {spec.audience}")
print(f"  Objective: {spec.objective}")
print(f"  Narrative length: {len(spec.narrative)} chars")
print(f"  Number of slides: {len(spec.slides)}")
for i, slide in enumerate(spec.slides[:3]):
    print(f"  Slide {i+1}: {slide.title} - {len(slide.bullets)} bullets - '{slide.description[:50]}...'")
print()

# Test create_deck_from_brief
output_files = g.create_deck_from_brief(brief, output_dir=".opencode/agents-test", deck_type="investor_pitch")
print(f"Output files: {output_files}")
print()
print("SUCCESS - Full pipeline test passed!")