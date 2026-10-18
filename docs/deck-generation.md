# Deck Generation Navigation

Pointer: static/brand/templates/generate-pitch-deck.py --- Adapted script that converts ai_venture_studio_client_presentation.md (Part 5) into a 13-slide PPTX using brand tokens from brand/tokens/.

Branches (trigger reaching):
- ai_venture_studio_client_presentation.md is present and complete ---> run uv run python static/brand/templates/generate-pitch-deck.py
- Presentation spec ai_venture_studio_client_presentation_deck_spec.md needs review first ---> read spec, verify slide count (13), then run script
- Brand compliance check brand/guidelines/brand-guidelines.md Sec. 9 must pass ---> verify navy rail, color palette, type scale before delivery
- CTO validation: PORTFOLIO D (Consumer Platforms) must appear in Slide 4 ---> confirmed via company-registry.yaml agent roles

Leading word: generate --- when this word is invoked in a prompt, the agent reaches the pointer and the three resources above.

One source of truth: company-registry.yaml --- agent roles and KPIs (ATC >90%, velocity <60d, correction ratio, 3x capital efficiency) are the single source of truth; the deck references these but the registry is authoritative.

Cut identity: The brand tokens (navy #070A40, red #E63946, cyan #00BFFF) and compliance checklist (Sec. 9) are also defined in brand/tokens/brand-tokens.json and brand/guidelines/brand-guidelines.md; this pointer directs to the primary references only.
