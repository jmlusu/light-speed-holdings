"""Tests for the logo-usage gate's retired-asset detection.

The gate must catch the retired lighthouse-in-shield filenames even when they
appear without the old ``brand/logos/`` prefix — copy-pasting ``icononly.png``
into a new artifact is the failure mode the prefix-only tokens missed. It must
*not* fire on the same words used as ordinary English or CSS.
"""

from __future__ import annotations

import pytest

from scripts.qa.check_logo_usage import LEGACY_ASSET_RE, LEGACY_PATH_TOKENS


@pytest.mark.parametrize(
    "text",
    [
        "fulllogo.png",
        "fulllogo.jpg",
        "`icononly.png`",
        "textonly.svg",
        "grayscale.png",
        "icononly_transparent.png",
        "fulllogo_transparent_nobuffer.png",
        "icononly_transparent_nobuffer.png",
        "grayscale_nobuffer.png",
        "`grayscale/`",
        "`icononly/`",
        "primary: fulllogo_transparent",
        "icons/fulllogo/fulllogo.png",
        '"icononly" in src',
    ],
)
def test_flags_retired_asset_names(text: str) -> None:
    assert LEGACY_ASSET_RE.search(text) is not None


@pytest.mark.parametrize(
    "text",
    [
        "filter: grayscale(0.72)",
        "-moz-osx-font-smoothing: grayscale",
        "text-only prompt",
        "logo-mark.png",
        "logo-no-background.png",
        "logo-full-transparent.svg",
        "logo-avatar.png",
    ],
)
def test_ignores_current_assets_and_unrelated_prose(text: str) -> None:
    assert LEGACY_ASSET_RE.search(text) is None


def test_prefix_tokens_still_cover_old_directory() -> None:
    joined = " ".join(LEGACY_PATH_TOKENS)
    for expected in ("brand/logos/", "logos/fulllogo", "logos/grayscale"):
        assert expected in joined
