# Tool Sandbox Design — Resolved (Ticket #39)

> **Status**: DECIDED 2026-08-17. Grilled and locked.
> **Ticket**: [#39 — Decide the opt-in tool sandbox design](https://github.com/jmlusu/light-speed-holdings/issues/39)
> **Blocked by**: #34 (event-bus evolution — resolved: keep JSON MessageBus)
> **Prototype asset**: `docs/research/tool-sandbox-design.md` (this file)

---

## Problem

Requirement T4 demands containerized tool execution. Today, `ToolRunner._execute()` runs
`subprocess.run()` directly on the host. There is no isolation between the agent's command
and the host OS. We need an **opt-in** Docker-backed sandbox for the `bash` tool, while
keeping the in-process allowlist runner as the default.

## Scope

Only the `bash` tool (command execution) needs sandboxing. The other 6 canonical tools
(`read`, `edit`, `grep`, `list`, `webfetch`, `task`) are fine in-process — they do
file I/O or HTTP, not arbitrary command execution.

---

## Design Sketch

### 1. Backend abstraction

Extract the command execution into a **Strategy interface**. The `ToolRunner` delegates
`_execute()` to whichever backend is active:

```python
# src/ai_company/executor/tool_runner.py (new code)

from abc import ABC, abstractmethod

class CommandBackend(ABC):
    """Abstract base for command execution backends."""

    @abstractmethod
    def execute(
        self,
        tokens: list[str],
        cwd: Path,
        timeout: int = 120,
    ) -> subprocess.CompletedProcess[str]:
        """Run a command and return the result."""
        ...

    def health_check(self) -> bool:
        """Return True if the backend is ready to accept work."""
        return True


class InProcessBackend(CommandBackend):
    """Default: subprocess.run() on the host (current behavior)."""

    def execute(self, tokens, cwd, timeout=120):
        return subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(cwd),
        )


class DockerBackend(CommandBackend):
    """Opt-in: run commands inside a disposable Docker container."""

    def __init__(
        self,
        image: str = "python:3.12-slim",
        memory_limit: str = "256m",
        cpu_period: int = 100_000,
        cpu_quota: int = 50_000,
        network: str = "none",
        read_only: bool = True,
    ) -> None:
        self.image = image
        self.memory_limit = memory_limit
        self.cpu_period = cpu_period
        self.cpu_quota = cpu_quota
        self.network = network
        self.read_only = read_only

    def execute(self, tokens, cwd, timeout=120):
        docker_cmd = [
            "docker", "run", "--rm",
            "--network", self.network,
            "--memory", self.memory_limit,
            "--cpus", str(self.cpu_quota / self.cpu_period),
            "--read-only" if self.read_only else "",
            "-v", f"{cwd}:/workspace:rw",
            "-w", "/workspace",
            self.image,
            *tokens,
        ]
        docker_cmd = [t for t in docker_cmd if t]  # filter empty strings
        return subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 30,  # extra for container startup
        )

    def health_check(self) -> bool:
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True, timeout=5,
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
```

### 2. Config structure

New YAML section in `config/tool_sandbox.yaml`:

```yaml
# Tool Sandbox Configuration
# Controls whether commands run in-process or inside Docker containers.
# Default: in-process (no Docker dependency).

# Global default backend for the bash tool.
# Options: "in-process" | "docker"
default_backend: in-process

# Per-agent overrides. Agents listed here use the docker backend.
# Unlisted agents inherit the global default.
sandbox_agents: []
  # - ceo
  # - cto

# Docker backend settings (used when default_backend or agent override = docker).
docker:
  image: python:3.12-slim
  memory_limit: "256m"
  cpu_period: 100000
  cpu_quota: 50000       # 0.5 CPU
  network: none           # no network access inside container (per-agent overrideable)
  read_only: true         # read-only root filesystem
  timeout: 120            # extra seconds for container startup

# Degradation policy: what happens if Docker is unavailable?
# "fail" = return error to agent
# "fallback" = silently fall back to in-process
degradation: fallback
```

### 3. Wiring into ToolRunner

```python
class ToolRunner:
    def __init__(
        self,
        project_root: str | Path = ".",
        allowlist_path: str | Path | None = None,
        content_filter: ContentFilter | None = None,
        pii_detector: PIIDetector | None = None,
        sandbox_config: dict | None = None,  # NEW
    ) -> None:
        self.project_root = Path(project_root).resolve()
        self.allowed_commands = _load_allowlist(allowlist_path)
        self._content_filter = content_filter or get_content_filter()
        self._pii_detector = pii_detector or get_pii_detector()

        # Sandbox backend selection
        self._backend = self._resolve_backend(sandbox_config or {})

    def _resolve_backend(self, config: dict) -> CommandBackend:
        default = config.get("default_backend", "in-process")
        if default == "docker":
            docker_cfg = config.get("docker", {})
            backend = DockerBackend(**docker_cfg)
            if backend.health_check():
                return backend
            degradation = config.get("degradation", "fallback")
            if degradation == "fail":
                raise RuntimeError("Docker sandbox requested but Docker is unavailable")
            logger.warning("Docker unavailable — falling back to in-process backend")
        return InProcessBackend()
```

### 4. Degradation flow

```
Agent requests bash tool
  → ToolRunner._execute()
    → Check sandbox config for this agent/tool
    → If docker backend selected:
        → health_check() on DockerBackend
        → If healthy: run in container
        → If unhealthy:
            → degradation == "fallback" → InProcessBackend.execute()
            → degradation == "fail" → return error
    → If in-process backend: run directly (current behavior)
```

### 5. Boot-time budget

- Docker container startup: ~1-3s on first run (image pull cached after that)
- Subsequent runs in same session: ~200-500ms (image already local)
- `health_check()`: 5s timeout, called once at ToolRunner init, cached
- Total overhead budget: **5s** for first command, **1s** for subsequent

### 6. Security model

| Concern | In-Process | Docker |
|---------|-----------|--------|
| Path containment | `_safe_path()` | Volume mount to `/workspace` |
| Command allowlist | Checked before execution | Checked before execution |
| Shell metacharacters | Blocked | Blocked |
| Network access | Host network | `--network=none` (default) |
| Filesystem escape | `_safe_path()` + symlink resolution | `--read-only` root + volume mount |
| Resource limits | 120s timeout | `--memory=256m`, `--cpus=0.5`, 150s timeout |
| Output scanning | `ContentFilter` + `PIIDetector` | Same (output piped back) |
| Privilege escalation | No `shell=True` | Non-root in container |

### 7. File structure (new files)

```
src/ai_company/executor/
  tool_runner.py          # MODIFIED: extract CommandBackend, add backend dispatch
  command_backend.py      # NEW: CommandBackend, InProcessBackend, DockerBackend

config/
  tool_sandbox.yaml       # NEW: sandbox configuration
```

### 8. What stays unchanged

- `ToolRunner.run_plan()` — no changes, still dispatches to `_execute_tool()`
- `_execute_tool()` — dispatches `bash` to `_execute()` which delegates to backend
- All other tool handlers (`_read`, `_write`, `_grep`, `_list_dir`, `_webfetch`, `_delegate`) — unchanged
- `check_tool_authorization()` and `check_tier_rules()` — unchanged
- HITL gate integration — unchanged
- Content filtering and PII detection — unchanged
- `agent_loop.py` and `loop.py` — unchanged (ToolRunner interface preserved)

---

## Resolved Decisions (Grilled 2026-08-17)

| # | Question | Decision |
|---|----------|----------|
| Q1 | What needs sandboxing? | Only `bash`. Other 6 tools stay in-process. |
| Q2 | Config granularity? | Per-agent. Agents listed in `sandbox_agents` get Docker; unlisted inherit global default. |
| Q3 | Degradation policy? | Configurable (`fallback` or `fail`), default `fallback`. |
| Q4 | Docker image? | `python:3.12-slim` as default, configurable via `docker.image`. |
| Q5 | Network policy? | Configurable per agent, default `none`. |
| Q6 | Windows support? | In scope. Docker Desktop via WSL2; path conversion handled internally; degrades per Q3 if Docker unavailable. |
