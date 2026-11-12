#!/usr/bin/env python3
"""Replaceable tool adapters for creative production.

An adapter wraps one rendering backend behind a small, swappable interface:

* ``supports``  — which artifact types the backend can produce
* ``availability`` — a cheap, local probe (no third-party transmission)
* ``wired``     — whether this pipeline can actually produce with it today
* ``produce``   — write the artifact into the run directory, return outputs

Adapters are registered in an ``AdapterRegistry``; the pipeline selects the
first registered adapter that supports the artifact, probes available and is
wired. Everything else is recorded on the manifest as availability evidence.

MVP position: the presentation adapter (local, deterministic) is the wired
production backend. OpenDesign and ComfyUI are evaluated here as optional
backends only — neither is an MVP dependency.
"""

from __future__ import annotations

import shutil
import socket
from pathlib import Path
from typing import Callable, Protocol

from ai_company.creative.models import AdapterStatus, ArtifactType, CreativeBrief

#: deck_type values accepted by the existing presentation pipeline.
DECK_TYPES: frozenset[str] = frozenset({"investor_pitch", "board_meeting", "keynote", "training"})

#: Local ComfyUI default port (probed on loopback only).
COMFYUI_PORT = 8188


class ToolAdapter(Protocol):
    """Contract every creative tool adapter implements."""

    name: str
    wired: bool

    def supports(self, artifact: ArtifactType) -> bool:
        """Whether this adapter can produce the artifact type."""
        ...

    def availability(self) -> tuple[bool, str]:
        """Probe the backend locally; return (reachable, detail)."""
        ...

    def produce(self, brief: CreativeBrief, out_dir: Path) -> list[str]:
        """Produce the artifact in ``out_dir``; return output file paths."""
        ...


def _probe_comfyui(port: int = COMFYUI_PORT) -> bool:
    """Probe a local ComfyUI instance on loopback (no external traffic)."""
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.4):
            return True
    except OSError:
        return False


class PresentationAdapter:
    """Local deck renderer built on the existing presentation pipeline.

    Produces Marp markdown + PptxGenJS JSON with brand tokens enforced
    (navy #070A40, red #DC3641, cyan #00BFFF) — fully offline.
    """

    name = "presentation"
    wired = True

    def supports(self, artifact: ArtifactType) -> bool:
        return artifact is ArtifactType.DECK

    def availability(self) -> tuple[bool, str]:
        return True, "local renderer (Marp markdown + PptxGenJS JSON, brand tokens enforced)"

    def produce(self, brief: CreativeBrief, out_dir: Path) -> list[str]:
        from ai_company.presentation.pipeline import create_deck_from_brief

        deck_type = brief.format_hint if brief.format_hint in DECK_TYPES else "investor_pitch"
        out_dir.mkdir(parents=True, exist_ok=True)
        files = create_deck_from_brief(
            brief.production_payload(),
            output_dir=str(out_dir),
            deck_type=deck_type,
        )
        return [str(path) for path in files]


class OpenDesignAdapter:
    """OpenDesign (``od``) backend — probed, not wired into the MVP pipeline.

    When OpenDesign is not operational, production for these artifact types
    falls through to the specialist agent (ls-od-* skills), never to a rebuild
    of the rendering engine.
    """

    name = "opendesign"
    wired = False

    def __init__(self, probe: Callable[[], str | None] | None = None) -> None:
        self._probe: Callable[[], str | None] = probe or (lambda: shutil.which("od"))

    def supports(self, artifact: ArtifactType) -> bool:
        return artifact in {
            ArtifactType.WEBSITE,
            ArtifactType.DECK,
            ArtifactType.WHITEPAPER,
            ArtifactType.AD,
            ArtifactType.DIAGRAM,
            ArtifactType.INFOGRAPHIC,
        }

    def availability(self) -> tuple[bool, str]:
        found = self._probe()
        if found:
            return (
                True,
                f"OpenDesign CLI found ({found}); production delegated to ls-od-* agent skills",
            )
        return False, "OpenDesign (od) CLI not on PATH — optional backend, not an MVP dependency"

    def produce(self, brief: CreativeBrief, out_dir: Path) -> list[str]:
        raise RuntimeError(
            f"adapter '{self.name}' is not wired: production for "
            f"{brief.artifact_type.value} goes through the specialist agent"
        )


class ComfyUIAdapter:
    """Local ComfyUI image backend — probed on loopback, not wired for MVP."""

    name = "comfyui"
    wired = False

    def __init__(self, probe: Callable[[], bool] | None = None) -> None:
        self._probe: Callable[[], bool] = probe or _probe_comfyui

    def supports(self, artifact: ArtifactType) -> bool:
        return artifact in {ArtifactType.INFOGRAPHIC, ArtifactType.AD, ArtifactType.WEBSITE}

    def availability(self) -> tuple[bool, str]:
        if self._probe():
            return True, f"ComfyUI reachable on 127.0.0.1:{COMFYUI_PORT} (optional backend)"
        return False, f"ComfyUI not reachable on 127.0.0.1:{COMFYUI_PORT} — not an MVP dependency"

    def produce(self, brief: CreativeBrief, out_dir: Path) -> list[str]:
        raise RuntimeError(
            f"adapter '{self.name}' is not wired: media generation runs through "
            "the media-generation owner, not this pipeline"
        )


class AdapterRegistry:
    """Ordered set of adapters; selects a producer for an artifact type."""

    def __init__(self, adapters: list[ToolAdapter] | None = None) -> None:
        self._adapters: list[ToolAdapter] = list(adapters) if adapters else []

    def register(self, adapter: ToolAdapter) -> None:
        """Append an adapter (later registrations are lower priority)."""
        self._adapters.append(adapter)

    def statuses(self) -> list[AdapterStatus]:
        """Availability snapshot of every registered adapter (for the manifest)."""
        results: list[AdapterStatus] = []
        for adapter in self._adapters:
            try:
                available, detail = adapter.availability()
            except Exception as exc:  # noqa: BLE001 — a broken probe must not kill the run
                available, detail = False, f"probe failed: {exc}"
            results.append(
                AdapterStatus(
                    name=adapter.name, available=available, wired=adapter.wired, detail=detail
                )
            )
        return results

    def select(self, artifact: ArtifactType) -> ToolAdapter | None:
        """First registered adapter that supports, probes available and is wired."""
        for adapter in self._adapters:
            if not adapter.supports(artifact):
                continue
            try:
                available, _detail = adapter.availability()
            except Exception:  # noqa: BLE001 — unusable adapter, keep looking
                available = False
            if available and adapter.wired:
                return adapter
        return None


def default_registry() -> AdapterRegistry:
    """The standard adapter set: local presentation renderer + optional backends."""
    return AdapterRegistry(
        [
            PresentationAdapter(),
            OpenDesignAdapter(),
            ComfyUIAdapter(),
        ]
    )
