"""Shared design-intent geometry for the AI Venture Studio client deck.

One source of truth for the three deck tools:

- ``generate-ai-venture-studio-deck.py`` places the artwork from these values.
- ``verify-venture-studio-deck.py`` asserts the built deck matches them.
- ``render-venture-studio-deck.py`` measures rendered pixels against them.

When the layout changes, the expectations move with it instead of silently
diverging between the generator and the gates that police it.

The invariants live here too. ``MIN_GAP_IN`` is the clear space the artwork
must keep from the nearest text on every slide, whatever the layout does.
"""

from __future__ import annotations

# ----------------------------------------------------------------- slide frame
SLIDE_W_IN = 10.0
SLIDE_H_IN = 7.5

# --------------------------------------------------------------------- artwork
# Artwork bbox (left, top, right, bottom) of the lockup inside the square
# brand/logo/logo-full.png. The crop drops the baked-in tagline so the picture
# frame can equal the visible artwork in every renderer -- LibreOffice ignores
# `a:srcRect` and would otherwise stretch the whole square over the slide.
LOGO_SRC_BOX = (190, 232, 1070, 945)
# The crop box is only valid for this source size; the generator refuses to
# run against a differently sized asset instead of cropping the wrong region.
LOGO_SRC_SIZE = (1254, 1254)
LOGO_ASPECT = (LOGO_SRC_BOX[2] - LOGO_SRC_BOX[0]) / (LOGO_SRC_BOX[3] - LOGO_SRC_BOX[1])
# Plate colour that the `a:clrChange` effect removes from the logo background.
LOGO_BG_HEX = "02062F"

# Cover (slide 1) lockup: top-left, above the title. x, y, width in inches.
COVER_LOGO_X_IN, COVER_LOGO_Y_IN, COVER_LOGO_W_IN = 0.65, 0.55, 1.90
COVER_LOGO_H_IN = COVER_LOGO_W_IN / LOGO_ASPECT
COVER_LOGO_BOTTOM_IN = COVER_LOGO_Y_IN + COVER_LOGO_H_IN

# Closing (slide 13) lockup: centred, above the tagline. x, y, width in inches.
CLOSING_LOGO_X_IN, CLOSING_LOGO_Y_IN, CLOSING_LOGO_W_IN = 3.80, 3.95, 2.40
CLOSING_LOGO_H_IN = CLOSING_LOGO_W_IN / LOGO_ASPECT
CLOSING_LOGO_BOTTOM_IN = CLOSING_LOGO_Y_IN + CLOSING_LOGO_H_IN

# Top edge of the closing-slide tagline ("ASPIRE. ACT. ACHIEVE.").
TAGLINE_Y_IN = 6.24
# Top edge of the cover title ("AI Venture Studio").
COVER_TITLE_Y_IN = 2.50

# Invariant: clear space between artwork and the nearest text.
MIN_GAP_IN = 0.15
