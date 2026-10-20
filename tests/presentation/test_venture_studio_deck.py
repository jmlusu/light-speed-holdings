"""Regression tests for the AI Venture Studio client deck.

These guard the defect fixed in PR #480: a logo placed with ``a:srcRect``
verifies clean in ``python-pptx`` but renders as the full uncropped square in
LibreOffice, which drew the lockup's baked-in tagline over the slide 13
tagline. The gates must reject that geometry, and the committed deck must
still be the one the generator produces.
"""

import importlib
import importlib.util
import io
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest
from PIL import Image
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Inches

REPO_ROOT = Path(__file__).resolve().parents[2]
PRESENTATION_DIR = REPO_ROOT / "scripts" / "presentation"
GENERATOR = PRESENTATION_DIR / "generate-ai-venture-studio-deck.py"
VERIFIER = PRESENTATION_DIR / "verify-venture-studio-deck.py"
COMMITTED_DECK = REPO_ROOT / "ai_venture_studio_client_presentation.pptx"

geometry = importlib.import_module("deck_geometry")


def load_module(name: str, path: Path):
    """Load a hyphenated deck tool as a module."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


verifier = load_module("verify_venture_studio_deck", VERIFIER)


def picture_on(slide) -> object:
    return next(sh for sh in slide.shapes if sh.shape_type == MSO_SHAPE_TYPE.PICTURE)


@pytest.fixture(scope="session")
def generated_deck(tmp_path_factory) -> Path:
    """Build the deck once with the shipped generator."""
    out = tmp_path_factory.mktemp("deck") / "deck.pptx"
    result = subprocess.run(
        [sys.executable, str(GENERATOR), "--output", str(out)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return out


def test_generated_deck_passes_every_check(generated_deck: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(VERIFIER), str(generated_deck)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ALL 11 CHECKS PASSED" in result.stdout


def test_generated_logo_is_pre_cropped(generated_deck: Path) -> None:
    """No srcRect anywhere, and the embedded asset is the cropped lockup."""
    with zipfile.ZipFile(generated_deck) as archive:
        for slide in ("slide1.xml", "slide13.xml"):
            assert "srcRect" not in archive.read(f"ppt/slides/{slide}").decode()
        media = [n for n in archive.namelist() if n.startswith("ppt/media/")]
        assert len(media) == 1
        size = Image.open(io.BytesIO(archive.read(media[0]))).size
    left, top, right, bottom = geometry.LOGO_SRC_BOX
    assert size == (right - left, bottom - top)


def test_generated_frame_matches_shared_geometry(generated_deck: Path) -> None:
    """The generator and the gates must agree on where the lockup sits."""
    prs = Presentation(generated_deck)
    cover = picture_on(list(prs.slides)[0])
    closing = picture_on(list(prs.slides)[12])
    assert cover.left == Inches(geometry.COVER_LOGO_X_IN)
    assert cover.top == Inches(geometry.COVER_LOGO_Y_IN)
    assert cover.width == Inches(geometry.COVER_LOGO_W_IN)
    assert closing.left == Inches(geometry.CLOSING_LOGO_X_IN)
    assert closing.top == Inches(geometry.CLOSING_LOGO_Y_IN)
    assert closing.width == Inches(geometry.CLOSING_LOGO_W_IN)
    assert closing.height == Inches(geometry.CLOSING_LOGO_W_IN / geometry.LOGO_ASPECT)


def test_committed_deck_matches_the_generator(generated_deck: Path) -> None:
    """The deck in the repository must be the one the generator produces.

    Media is compared by pixels rather than by file bytes: the PNG encoder
    version may differ between machines, but the artwork must not.
    """
    assert COMMITTED_DECK.exists(), f"missing deck: {COMMITTED_DECK}"
    with zipfile.ZipFile(COMMITTED_DECK) as committed, zipfile.ZipFile(generated_deck) as built:
        assert sorted(committed.namelist()) == sorted(built.namelist())
        for name in committed.namelist():
            if name.startswith("ppt/media/"):
                left = Image.open(io.BytesIO(committed.read(name)))
                right = Image.open(io.BytesIO(built.read(name)))
                assert left.size == right.size, f"{name} size drifted"
                assert left.tobytes() == right.tobytes(), f"{name} pixels drifted"
            else:
                assert committed.read(name) == built.read(name), f"{name} drifted"


def test_src_rect_geometry_is_rejected(generated_deck: Path, tmp_path: Path) -> None:
    """The pre-fix geometry (square frame + srcRect) must fail the logo check."""
    broken = tmp_path / "src-rect.pptx"
    prs = Presentation(generated_deck)
    picture = picture_on(list(prs.slides)[12])
    picture.crop_left = 0.15152
    picture.crop_right = 0.14673
    picture.crop_top = 0.18501
    picture.crop_bottom = 0.24641
    picture.width = Inches(3.42)
    picture.height = Inches(3.42)
    prs.save(broken)

    ok, detail = verifier.check_logo(Presentation(broken))
    assert not ok
    assert "srcRect" in detail


def test_logo_overrunning_the_tagline_is_rejected(generated_deck: Path, tmp_path: Path) -> None:
    """A frame that reaches the tagline must fail the clearance check."""
    broken = tmp_path / "overrun.pptx"
    prs = Presentation(generated_deck)
    picture = picture_on(list(prs.slides)[12])
    picture.top = Inches(5.40)
    prs.save(broken)

    ok, detail = verifier.check_logo(Presentation(broken))
    assert not ok
    assert "gap" in detail


def test_logo_landing_on_text_is_rejected(generated_deck: Path, tmp_path: Path) -> None:
    """A logo sitting on the tagline must be reported as a collision."""
    broken = tmp_path / "collision.pptx"
    prs = Presentation(generated_deck)
    picture = picture_on(list(prs.slides)[12])
    picture.top = Inches(6.20)
    prs.save(broken)

    ok, detail = verifier.check_collisions(Presentation(broken))
    assert not ok
    assert "ASPIRE" in detail


def test_generator_refuses_an_unexpected_logo_size(tmp_path: Path) -> None:
    """A replaced brand asset must fail loudly instead of cropping blindly."""
    generator = load_module("generate_ai_venture_studio_deck", GENERATOR)
    fake = tmp_path / "logo.png"
    Image.new("RGBA", (10, 10), (0, 0, 0, 0)).save(fake)
    generator.LOGO_PATH = str(fake)

    with pytest.raises(SystemExit) as excinfo:
        generator._cropped_logo()
    assert "expected" in str(excinfo.value)
