"""ComfyUI MCP client wrapper for media generation (ADR-018).

Thin wrapper around the ComfyUI MCP driver (comfyui-mcp) providing a Python
interface for the media_generation_owner agent. Supports both API mode
(npx comfyui-mcp) and local mode with health checks and model variant selection.
"""

from __future__ import annotations

import json
import logging
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class HealthCheckResult:
    """Result of a ComfyUI health check."""

    status: str  # "healthy", "degraded", "unavailable"
    vram_free_mb: int = 0
    disk_free_gb: float = 0.0
    api_mode: bool = True
    error: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        pass


@dataclass
class GenerationResult:
    """Result of an image generation request."""

    status: str  # "generated", "unavailable", "error"
    output_paths: list[str] = field(default_factory=list)
    workflow_name: str = ""
    model_variant: str = ""
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        pass


class ComfyClient:
    """Client for ComfyUI MCP (comfyui-mcp) image generation.

    Supports two execution modes:
    - API mode (default): Uses Comfy Cloud / partner API nodes via npx comfyui-mcp
    - Local mode (opt-in): Uses local headless ComfyUI with VRAM/disk constraints
    """

    def __init__(
        self,
        *,
        api_mode: bool = True,
        host: str = "127.0.0.1",
        port: int = 8188,
        timeout: int = 120,
        workflow_templates_dir: str | Path | None = None,
    ) -> None:
        """Initialize ComfyUI client.

        Args:
            api_mode: If True, use API mode (Comfy Cloud). If False, use local mode.
            host: ComfyUI host (local mode only).
            port: ComfyUI port (local mode only).
            timeout: Request timeout in seconds.
            workflow_templates_dir: Path to workflow template library.
        """
        self.api_mode = api_mode
        self.host = host
        self.port = port
        self.timeout = timeout
        self.workflow_templates_dir = (
            Path(workflow_templates_dir) if workflow_templates_dir else None
        )
        self._workflow_cache: dict[str, dict[str, Any]] = {}

    def health_check(self) -> HealthCheckResult:
        """Run health check before generation.

        Validates VRAM and disk space for local mode, or API connectivity for API mode.
        """
        if self.api_mode:
            return self._health_check_api()
        return self._health_check_local()

    def _health_check_api(self) -> HealthCheckResult:
        """Health check for API mode (Comfy Cloud / partner nodes)."""
        try:
            # Test MCP server availability
            result = subprocess.run(
                ["npx", "comfyui-mcp", "--health-check"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                return HealthCheckResult(
                    status="healthy",
                    api_mode=True,
                    details={"output": result.stdout},
                )
            return HealthCheckResult(
                status="unavailable",
                api_mode=True,
                error=f"MCP health check failed: {result.stderr}",
            )
        except FileNotFoundError:
            return HealthCheckResult(
                status="unavailable",
                api_mode=True,
                error="npx not found. Install Node.js to use comfyui-mcp.",
            )
        except subprocess.TimeoutExpired:
            return HealthCheckResult(
                status="degraded",
                api_mode=True,
                error="Health check timed out (API may be slow)",
            )
        except (subprocess.SubprocessError, OSError) as exc:
            logger.exception("API health check failed")
            return HealthCheckResult(status="error", api_mode=True, error=str(exc))

    def _health_check_local(self) -> HealthCheckResult:
        """Health check for local mode (VRAM + disk validation)."""
        import shutil

        # Check disk space
        try:
            disk_usage = shutil.disk_usage(".")
            disk_free_gb = disk_usage.free / (1024**3)
        except OSError:
            disk_free_gb = 0.0

        # Check VRAM (best effort - requires GPU tools)
        vram_free_mb = 0
        try:
            import torch

            if torch.cuda.is_available():
                vram_total = torch.cuda.get_device_properties(0).total_memory
                vram_free_mb = (vram_total - torch.cuda.memory_allocated(0)) // (1024 * 1024)
            elif hasattr(torch, "mps") and torch.backends.mps.is_available():
                # Apple Silicon - no direct VRAM query, estimate from memory
                vram_free_mb = 8192  # Assume 8GB unified
        except ImportError:
            pass
        except RuntimeError:
            pass

        # Determine status based on constraints
        min_vram_mb = 4096  # 4GB minimum
        min_disk_gb = 20.0

        if vram_free_mb < min_vram_mb and vram_free_mb > 0:
            status = "degraded"
            error = f"VRAM low: {vram_free_mb}MB free (need {min_vram_mb}MB+)"
        elif disk_free_gb < min_disk_gb:
            status = "degraded"
            error = f"Disk low: {disk_free_gb:.1f}GB free (need {min_disk_gb}GB+)"
        elif vram_free_mb == 0 and disk_free_gb == 0:
            status = "unavailable"
            error = "Cannot determine local resources (no GPU tools, disk check failed)"
        else:
            status = "healthy"
            error = ""

        return HealthCheckResult(
            status=status,
            vram_free_mb=vram_free_mb,
            disk_free_gb=round(disk_free_gb, 1),
            api_mode=False,
            error=error,
            details={"min_vram_mb": min_vram_mb, "min_disk_gb": min_disk_gb},
        )

    def select_model_variant(self, vram_free_mb: int = 0) -> str:
        """Select appropriate model variant based on available VRAM.

        Args:
            vram_free_mb: Free VRAM in MB (from health_check)

        Returns:
            Model variant identifier (fp8, offload, fp16, etc.)
        """
        if vram_free_mb >= 16384:  # 16GB+
            return "fp16"
        elif vram_free_mb >= 8192:  # 8GB+
            return "fp8"
        elif vram_free_mb >= 4096:  # 4GB+
            return "offload"
        return "offload"  # fallback for low VRAM

    def load_workflow_template(self, template_name: str) -> dict[str, Any] | None:
        """Load a workflow template by name.

        Args:
            template_name: Name of the workflow template (without .json)

        Returns:
            Workflow JSON dict or None if not found.
        """
        if template_name in self._workflow_cache:
            return self._workflow_cache[template_name]

        if not self.workflow_templates_dir:
            logger.warning("No workflow templates directory configured")
            return None

        template_path = self.workflow_templates_dir / f"{template_name}.json"
        if not template_path.exists():
            # Try quick index
            index_path = self.workflow_templates_dir / "templates" / "_quick_index.json"
            if index_path.exists():
                try:
                    index = json.loads(index_path.read_text())
                    if template_name in index:
                        template_path = self.workflow_templates_dir / index[template_name]
                except (json.JSONDecodeError, OSError):
                    pass

        if template_path.exists():
            try:
                workflow: dict[str, Any] = json.loads(template_path.read_text())
                self._workflow_cache[template_name] = workflow
                return workflow
            except (json.JSONDecodeError, OSError) as exc:
                logger.error("Failed to load workflow %s: %s", template_name, exc)

        return None

    def compose_workflow(
        self,
        template_name: str,
        prompt: str,
        *,
        model_variant: str | None = None,
        seed: int | None = None,
        output_node_id: str | None = None,
    ) -> dict[str, Any] | None:
        """Compose a workflow from template with prompt and parameters.

        Args:
            template_name: Name of workflow template
            prompt: Generation prompt
            model_variant: Override model variant (fp8, offload, fp16)
            seed: Random seed
            output_node_id: Override output node ID

        Returns:
            Composed workflow JSON or None on failure.
        """
        workflow = self.load_workflow_template(template_name)
        if not workflow:
            return None

        # Basic prompt injection - templates should have a prompt node
        # This is a simplified version; real implementation depends on template schema
        for _node_id, node in workflow.items():
            if (
                node.get("class_type") in ("CLIPTextEncode", "Prompt", "TextEncode")
                and "inputs" in node
                and "text" in node["inputs"]
            ):
                node["inputs"]["text"] = prompt
                break

        if model_variant:
            # Model variant selection would modify checkpoint loader nodes
            pass

        if seed is not None:
            for _node_id, node in workflow.items():
                if (
                    node.get("class_type") in ("KSampler", "Sampler", "Seed")
                    and "inputs" in node
                    and "seed" in node["inputs"]
                ):
                    node["inputs"]["seed"] = seed
                    break

        if output_node_id:
            # Store output node reference for result extraction
            workflow["_output_node"] = output_node_id

        return workflow

    def generate(
        self,
        workflow: dict[str, Any],
        *,
        output_dir: str | Path | None = None,
    ) -> GenerationResult:
        """Execute generation via ComfyUI MCP.

        Args:
            workflow: Composed workflow JSON
            output_dir: Directory for output files (API mode uses temp)

        Returns:
            GenerationResult with output paths and metadata.
        """
        if self.api_mode:
            return self._generate_api(workflow, output_dir)
        return self._generate_local(workflow, output_dir)

    def _generate_api(
        self,
        workflow: dict[str, Any],
        output_dir: str | Path | None,
    ) -> GenerationResult:
        """Generate using API mode (Comfy Cloud / partner nodes)."""
        try:
            # Write workflow to temp file for MCP
            import tempfile

            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                json.dump(workflow, f)
                workflow_path = f.name

            # Invoke comfyui-mcp via npx
            cmd = [
                "npx",
                "comfyui-mcp",
                "--workflow",
                workflow_path,
                "--output",
                str(output_dir) if output_dir else "output",
            ]
            if self.workflow_templates_dir:
                cmd.extend(["--templates", str(self.workflow_templates_dir)])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )

            # Cleanup temp file
            Path(workflow_path).unlink(missing_ok=True)

            if result.returncode == 0:
                # Parse output for generated file paths
                output_paths = self._parse_output_paths(result.stdout)
                return GenerationResult(
                    status="generated",
                    output_paths=output_paths,
                    workflow_name=workflow.get("_output_node", "unknown"),
                    metadata={"stdout": result.stdout, "stderr": result.stderr},
                )

            return GenerationResult(
                status="error",
                error=f"Generation failed: {result.stderr}",
                metadata={"stdout": result.stdout, "returncode": result.returncode},
            )

        except subprocess.TimeoutExpired:
            return GenerationResult(
                status="error", error=f"Generation timed out after {self.timeout}s"
            )
        except FileNotFoundError:
            return GenerationResult(status="unavailable", error="npx not found. Install Node.js.")
        except (subprocess.SubprocessError, OSError) as exc:
            logger.exception("API generation failed")
            return GenerationResult(status="error", error=str(exc))

    def _generate_local(
        self,
        workflow: dict[str, Any],
        output_dir: str | Path | None,
    ) -> GenerationResult:
        """Generate using local mode (headless ComfyUI)."""
        # Local mode would invoke local ComfyUI server
        # This is a stub - real implementation depends on local ComfyUI setup
        return GenerationResult(
            status="unavailable",
            error="Local mode not yet implemented. Use API mode or set up local ComfyUI.",
        )

    def _parse_output_paths(self, stdout: str) -> list[str]:
        """Parse generated file paths from MCP stdout."""
        paths = []
        for line in stdout.splitlines():
            line = line.strip()
            if line and (line.endswith(".png") or line.endswith(".jpg") or line.endswith(".webp")):
                paths.append(line)
        return paths


def create_client(
    *,
    api_mode: bool = True,
    workflow_templates_dir: str | Path | None = None,
    **kwargs: Any,
) -> ComfyClient:
    """Factory function to create a configured ComfyClient.

    Args:
        api_mode: Use API mode (default True per ADR-018).
        workflow_templates_dir: Path to workflow template library.
        **kwargs: Additional arguments passed to ComfyClient.

    Returns:
        Configured ComfyClient instance.
    """
    return ComfyClient(
        api_mode=api_mode,
        workflow_templates_dir=workflow_templates_dir,
        **kwargs,
    )


__all__ = [
    "ComfyClient",
    "HealthCheckResult",
    "GenerationResult",
    "create_client",
]
