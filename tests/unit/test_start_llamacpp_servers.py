"""Regression tests for llama-server startup command building.

The launcher previously passed ``--load-mode mmap+mlock`` to llama-server,
which is not a supported flag, so every server failed to start. It also
indexed ``PRIORITY_MODELS`` by position in the process list during restarts,
which misaligned after any skipped server. These tests pin the corrected
command shape and pair-tracked process registry.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

_SCRIPT = Path(__file__).parents[2] / "scripts" / "start_llamacpp_servers.py"


def _load_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("start_llamacpp_servers", _SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODEL = {
    "name": "llama3.1-8b-32k",
    "file": "llama-3.1-8b-instruct-q4_K_M.gguf",
    "port": 8088,
    "ctx": 32768,
    "threads": 8,
    "batch": 512,
    "api_key": "local",
}


def _cmd() -> list[str]:
    return _load_module().build_server_cmd(MODEL, "llama-server")


def test_cmd_pins_memory_with_load_mode_mlock() -> None:
    cmd = _cmd()
    assert "--load-mode" in cmd
    idx = cmd.index("--load-mode")
    assert cmd[idx + 1] == "mlock"


def test_cmd_starts_with_server_path() -> None:
    assert _cmd()[0] == "llama-server"


def test_cmd_model_context_batch_and_threads() -> None:
    cmd = _cmd()
    expected_model_path = str(Path(_SCRIPT).parents[1] / "models" / MODEL["file"])
    pairs = dict(zip(cmd, cmd[1:], strict=False))
    assert pairs["-m"] == expected_model_path
    assert pairs["-c"] == str(MODEL["ctx"])
    assert pairs["-b"] == str(MODEL["batch"])
    assert pairs["-t"] == str(MODEL["threads"])
    assert pairs["-tb"] == str(MODEL["threads"])


def test_cmd_network_and_auth_arguments() -> None:
    pairs = dict(zip(_cmd(), _cmd()[1:], strict=False))
    assert pairs["-ngl"] == "0"
    assert pairs["--port"] == str(MODEL["port"])
    assert pairs["--host"] == "127.0.0.1"
    assert pairs["--api-key"] == MODEL["api_key"]


def test_cmd_flag_ordering_preserved() -> None:
    cmd = _cmd()
    assert cmd.index("-ngl") < cmd.index("--load-mode") < cmd.index("--port")


def test_process_registry_tracks_model_pairs() -> None:
    module = _load_module()
    assert isinstance(module.processes, list)
    for entry in module.processes:
        model, proc = entry
        assert isinstance(model, dict)
        assert hasattr(proc, "poll")
