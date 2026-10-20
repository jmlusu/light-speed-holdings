"""Make the deck tooling importable from the tests.

The deck tools live in ``scripts/presentation`` and import the shared
``deck_geometry`` module by name, so that directory goes on ``sys.path``
before the test modules load them.
"""

import sys
from pathlib import Path

PRESENTATION_DIR = Path(__file__).resolve().parents[2] / "scripts" / "presentation"

if str(PRESENTATION_DIR) not in sys.path:
    sys.path.insert(0, str(PRESENTATION_DIR))
