import sys
sys.path.insert(0, ".")
from ai_company.generator import AgentGenerator

g = AgentGenerator()
brief = {
    "topic": "AI Company Builder",
    "audience": "investors",
    "objective": "secure seed funding",
    "deck_type": "investor_pitch"
}
spec = g.generate_presentation_phases(brief)
print(f"Generated spec with {spec.slide_count} slides")
print(f"Thesis: {spec.thesis[:60]}...")
print(f"Narrative: {spec.narrative[:60]}...")
for i, slide in enumerate(spec.slides, 1):
    print(f"  Slide {i}: {slide.title} ({len(slide.bullets)} bullets, notes={bool(slide.speaker_notes)})")