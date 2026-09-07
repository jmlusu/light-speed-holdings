"""Archify integration — registry to typed JSON IR diagram sources + rendering.

Public entry points:

- :func:`ai_company.archify.converter.generate_specs` — build the default
  diagram set (architecture + workflow) from the loaded registry.
- :func:`ai_company.archify.renderer.deliver` — render a validated JSON IR
  source to a self-contained interactive HTML artifact.
"""

from ai_company.archify.converter import (
    build_architecture,
    build_dataflow,
    build_sequence,
    build_workflow,
    generate_specs,
)
from ai_company.archify.renderer import (
    ArchifyError,
    ArchifyNotAvailable,
    compare,
    deliver,
    guide,
    resolve_bin,
    resolve_skill_dir,
    validate,
)

__all__ = [
    "ArchifyError",
    "ArchifyNotAvailable",
    "build_architecture",
    "build_dataflow",
    "build_sequence",
    "build_workflow",
    "compare",
    "deliver",
    "generate_specs",
    "guide",
    "resolve_bin",
    "resolve_skill_dir",
    "validate",
]
