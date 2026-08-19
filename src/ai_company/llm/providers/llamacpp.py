"""llama.cpp provider — optimal for CPU-only inference with shared system RAM."""

from __future__ import annotations

import json
import os
import subprocess
import threading
import time
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from ai_company.llm.providers.base import (
    ChatResponse,
    LLMProvider,
    LLMProviderError,
    StreamChunk,
)


@dataclass
class LlamaCppConfig:
    """Configuration for llama.cpp server."""

    model_path: str
    n_ctx: int = 32768
    n_batch: int = 512
    n_threads: int = 8
    n_threads_batch: int = 8
    n_gpu_layers: int = 0
    use_mlock: bool = True
    use_mmap: bool = True
    rope_freq_base: float = 10000.0
    rope_freq_scale: float = 1.0
    temperature: float = 0.3
    top_p: float = 0.9
    top_k: int = 40
    repeat_penalty: float = 1.1
    seed: int = -1


class LlamaCppProvider(LLMProvider):
    """llama.cpp provider using llama-server for persistent model loading."""

    def __init__(
        self,
        name: str = "llamacpp",
        model_path: str = "",
        config: LlamaCppConfig | None = None,
        server_port: int = 8080,
        server_host: str = "127.0.0.1",
        use_server: bool = True,
        startup_timeout: float = 60.0,
        api_key: str = "",
    ) -> None:
        self.name = name
        self.model_path = model_path
        self.config = config or LlamaCppConfig(model_path=model_path)
        self.server_port = server_port
        self.server_host = server_host
        self.use_server = use_server
        self.startup_timeout = startup_timeout
        self.api_key = api_key
        self._server_process: subprocess.Popen[Any] | None = None
        self._server_ready = threading.Event()
        self._client = httpx.Client(
            base_url=f"http://{server_host}:{server_port}",
            timeout=300.0,
            headers={"X-API-Key": api_key} if api_key else {},
        )
        self._lock = threading.Lock()
        self._available: bool | None = None  # None = unknown, True/False = checked

    def _start_server(self) -> None:
        """Start llama-server in background. Logs warnings on failure instead of raising."""
        with self._lock:
            if self._server_process and self._server_process.poll() is None:
                return  # Already running

            llama_server = self._find_llama_server()
            if not llama_server:
                import logging

                logging.getLogger(__name__).warning(
                    "llama-server not found in PATH. Install llama.cpp for optimized CPU inference. "
                    "Falling back to Ollama for local inference."
                )
                self._available = False
                return

            if not self.model_path or not Path(self.model_path).exists():
                import logging

                logging.getLogger(__name__).warning(
                    "Model file not found: %s. Download GGUF models first.", self.model_path
                )
                self._available = False
                return

            cmd = [
                llama_server,
                "-m",
                self.model_path,
                "-c",
                str(self.config.n_ctx),
                "-b",
                str(self.config.n_batch),
                "-t",
                str(self.config.n_threads),
                "-tb",
                str(self.config.n_threads_batch),
                "-ngl",
                str(self.config.n_gpu_layers),
                "--port",
                str(self.server_port),
                "--host",
                self.server_host,
            ]

            # Only add load-mode flags if mlock or mmap is enabled
            load_modes = []
            if self.config.use_mlock:
                load_modes.append("mlock")
            if self.config.use_mmap:
                load_modes.append("mmap")
            if load_modes:
                cmd.extend(["--load-mode", ",".join(load_modes)])

            # Add rope scaling if needed
            if self.config.rope_freq_scale != 1.0:
                cmd.extend(["--rope-freq-scale", str(self.config.rope_freq_scale)])
            if self.config.rope_freq_base != 10000.0:
                cmd.extend(["--rope-freq-base", str(self.config.rope_freq_base)])

            # Add API key if configured (required by llama-server >= b5500)
            if self.api_key:
                cmd.extend(["--api-key", self.api_key])

            self._server_process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            # Wait for server to be ready
            self._wait_for_server()

    def _find_llama_server(self) -> str | None:
        """Find llama-server executable in PATH or common locations."""
        # Check PATH first
        for path in os.environ.get("PATH", "").split(os.pathsep):
            exe = (
                Path(path) / "llama-server.exe" if os.name == "nt" else Path(path) / "llama-server"
            )
            if exe.exists():
                return str(exe)

        # Check project bin directory (where we installed llama.cpp)
        # Navigate from src/ai_company/llm/providers/ up to project root
        project_root = Path(__file__).parent.parent.parent.parent.parent
        project_bin = project_root / "bin" / "llama-server.exe"
        if project_bin.exists():
            return str(project_bin)

        # Check common install locations
        common_paths = [
            Path.home() / ".local" / "bin" / "llama-server",
            Path("/usr/local/bin/llama-server"),
            Path("/opt/llama.cpp/llama-server"),
            Path("C:/llama.cpp/llama-server.exe"),
        ]
        for p in common_paths:
            if p.exists():
                return str(p)

        return None

    def _wait_for_server(self) -> None:
        """Wait for llama-server to be ready. Returns False on failure instead of raising."""
        import logging

        logger = logging.getLogger(__name__)
        headers = {"X-API-Key": self.api_key} if self.api_key else {}

        start = time.time()
        while time.time() - start < self.startup_timeout:
            try:
                resp = httpx.get(
                    f"http://{self.server_host}:{self.server_port}/health",
                    timeout=2.0,
                    headers=headers,
                )
                if resp.status_code == 200:
                    self._server_ready.set()
                    self._available = True
                    return
            except (httpx.ConnectError, httpx.TimeoutException, OSError):
                pass
            time.sleep(0.5)

        # Check if process died
        if self._server_process and self._server_process.poll() is not None:
            logger.warning(
                "llama-server failed to start (exit code: %d). Falling back to Ollama.",
                self._server_process.returncode,
            )
            self._available = False
            return

        logger.warning(
            "llama-server did not become ready within %.0fs. Falling back to Ollama.",
            self.startup_timeout,
        )
        self._available = False

    def _ensure_server(self) -> bool:
        """Ensure server is running, restart if needed. Returns False if unavailable."""
        if not self.use_server:
            return True
        if self._available is False:
            return False
        if not self._server_ready.is_set() or (
            self._server_process and self._server_process.poll() is not None
        ):
            self._server_ready.clear()
            self._start_server()
            return self._available is True
        return True

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
    ) -> ChatResponse:
        if not self._ensure_server():
            raise LLMProviderError(
                self.name,
                "llama.cpp server is not available. Install llama.cpp or use Ollama as fallback.",
            )

        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
            "top_k": self.config.top_k,
            "repeat_penalty": self.config.repeat_penalty,
            "stream": False,
            "n_predict": 4096,
        }

        if self.config.seed != -1:
            payload["seed"] = self.config.seed

        try:
            resp = self._client.post("/v1/chat/completions", json=payload)
        except httpx.ConnectError as exc:
            self._server_ready.clear()
            raise LLMProviderError(
                self.name,
                f"Cannot connect to llama-server at {self.server_host}:{self.server_port}.",
            ) from exc
        except httpx.TimeoutException as exc:
            raise LLMProviderError(self.name, f"Request timed out: {exc}") from exc
        except httpx.HTTPError as exc:
            raise LLMProviderError(self.name, f"HTTP error: {exc}") from exc

        if resp.status_code != 200:
            raise LLMProviderError(
                self.name,
                f"llama-server returned {resp.status_code}: {resp.text[:200]}",
                status_code=resp.status_code,
            )

        data = resp.json()
        choice = data["choices"][0]
        content = choice["message"]["content"]
        usage = data.get("usage", {})

        return ChatResponse(
            content=content,
            model=model or Path(self.model_path).stem,
            provider=self.name,
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
        )

    def chat_stream(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
    ) -> Generator[StreamChunk, None, None]:
        if not self._ensure_server():
            raise LLMProviderError(
                self.name,
                "llama.cpp server is not available. Install llama.cpp or use Ollama as fallback.",
            )

        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
            "top_k": self.config.top_k,
            "repeat_penalty": self.config.repeat_penalty,
            "stream": True,
            "n_predict": 4096,
        }

        if self.config.seed != -1:
            payload["seed"] = self.config.seed

        try:
            with self._client.stream("POST", "/v1/chat/completions", json=payload) as resp:
                if resp.status_code != 200:
                    body = resp.read().decode("utf-8", errors="replace")
                    raise LLMProviderError(
                        self.name,
                        f"llama-server returned {resp.status_code}: {body[:200]}",
                        status_code=resp.status_code,
                    )

                for line in resp.iter_lines():
                    if not line:
                        continue
                    if line.startswith("data: "):
                        line = line[6:]
                    if line.strip() == "[DONE]":
                        break
                    try:
                        chunk = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    choices = chunk.get("choices", [])
                    if not choices:
                        continue

                    delta = choices[0].get("delta", {})
                    content = delta.get("content", "")
                    finish_reason = choices[0].get("finish_reason")

                    if finish_reason:
                        usage = chunk.get("usage", {})
                        yield StreamChunk(
                            delta="",
                            finish_reason=finish_reason,
                            usage={
                                "prompt_tokens": usage.get("prompt_tokens", 0),
                                "completion_tokens": usage.get("completion_tokens", 0),
                            },
                        )
                        return

                    if content:
                        yield StreamChunk(delta=content)

        except httpx.ConnectError as exc:
            self._server_ready.clear()
            raise LLMProviderError(
                self.name,
                f"Cannot connect to llama-server at {self.server_host}:{self.server_port}.",
            ) from exc
        except httpx.TimeoutException as exc:
            raise LLMProviderError(self.name, f"Request timed out: {exc}") from exc
        except httpx.HTTPError as exc:
            raise LLMProviderError(self.name, f"HTTP error: {exc}") from exc

    def is_available(self) -> bool:
        # If we already determined it's unavailable, don't keep checking
        if self._available is False:
            return False

        if not self.use_server:
            exists = Path(self.model_path).exists() if self.model_path else False
            self._available = exists
            return exists

        if not self._server_ready.is_set():
            return False

        if self._server_process and self._server_process.poll() is not None:
            return False

        try:
            headers = {"X-API-Key": self.api_key} if self.api_key else {}
            resp = httpx.get(
                f"http://{self.server_host}:{self.server_port}/health", timeout=2.0, headers=headers
            )
            available = resp.status_code == 200
            self._available = available
            return available
        except (httpx.ConnectError, httpx.TimeoutException, OSError):
            self._available = False
            return False

    def shutdown(self) -> None:
        """Stop the llama-server process."""
        with self._lock:
            if self._server_process and self._server_process.poll() is None:
                self._server_process.terminate()
                try:
                    self._server_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self._server_process.kill()
                    self._server_process.wait()
                self._server_ready.clear()

    def __del__(self) -> None:
        self.shutdown()
