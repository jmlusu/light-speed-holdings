#!/usr/bin/env python3
"""Start llama.cpp servers for priority models.

Run this to warm up the models before starting the agent system.
Keeps 3 priority models hot in memory (~18 GB RAM).
"""

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

MODELS_DIR = Path(__file__).parent.parent / "models"

# Priority models (keep warm based on workload: 30% coding, 40% reasoning, 30% general)
PRIORITY_MODELS = [
    {
        "name": "llama3.1-8b-32k",
        "file": "llama-3.1-8b-instruct-q4_K_M.gguf",
        "port": 8088,
        "ctx": 32768,
        "threads": 8,
        "batch": 512,
        "api_key": "local",
    },
    {
        "name": "qwen2.5-coder-7b-32k",
        "file": "qwen2.5-coder-7b-instruct-q4_K_M.gguf",
        "port": 8089,
        "ctx": 32768,
        "threads": 8,
        "batch": 512,
        "api_key": "local",
    },
    {
        "name": "deepseek-r1-64k",
        "file": "deepseek-r1-distill-qwen-7b-q4_K_M.gguf",
        "port": 8090,
        "ctx": 32768,
        "threads": 8,
        "batch": 256,
        "api_key": "local",
    },
]

# Optional: Additional models (start on demand)
OPTIONAL_MODELS = [
    {
        "name": "mistral-7b-32k",
        "file": "mistral-7b-instruct-v0.3-q4_K_M.gguf",
        "port": 8091,
        "ctx": 16384,
        "threads": 8,
        "batch": 512,
        "api_key": "local",
    },
]

processes: list[subprocess.Popen] = []


def find_llama_server() -> str | None:
    """Find llama-server executable."""
    # Check project bin directory first
    project_bin = Path(__file__).parent.parent / "bin" / "llama-server.exe"
    if project_bin.exists():
        return str(project_bin)

    # Check PATH
    for path in os.environ.get("PATH", "").split(os.pathsep):
        exe = Path(path) / ("llama-server.exe" if os.name == "nt" else "llama-server")
        if exe.exists():
            return str(exe)

    return None


def start_server(model: dict) -> subprocess.Popen | None:
    """Start a llama-server for a model."""
    llama_server = find_llama_server()
    if not llama_server:
        print("ERROR: llama-server not found. Install llama.cpp first.")
        return None

    model_path = MODELS_DIR / model["file"]
    if not model_path.exists():
        print(f"WARNING: Model not found: {model_path} - skipping")
        return None

    cmd = [
        llama_server,
        "-m",
        str(model_path),
        "-c",
        str(model["ctx"]),
        "-b",
        str(model["batch"]),
        "-t",
        str(model["threads"]),
        "-tb",
        str(model["threads"]),
        "-ngl",
        "0",  # CPU only
        "--load-mode",
        "mlock,mmap",
        "--port",
        str(model["port"]),
        "--host",
        "127.0.0.1",
        "--api-key",
        model["api_key"],
    ]

    print(f"Starting {model['name']} on port {model['port']}...")
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return proc


def wait_for_server(port: int, timeout: float = 60.0) -> bool:
    """Wait for server to be ready."""
    import httpx

    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = httpx.get(
                f"http://127.0.0.1:{port}/health",
                timeout=2.0,
                headers={"X-API-Key": "local"},
            )
            if resp.status_code == 200:
                return True
        except (httpx.HTTPError, OSError):
            pass
        time.sleep(0.5)

    return False


def signal_handler(sig, frame):
    print("\nShutting down servers...")
    for proc in processes:
        if proc.poll() is None:
            proc.terminate()
    for proc in processes:
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("=" * 60)
    print("Starting llama.cpp servers for priority models")
    print("=" * 60)

    for model in PRIORITY_MODELS:
        proc = start_server(model)
        if proc:
            processes.append(proc)
            if wait_for_server(model["port"]):
                print(f"  OK {model['name']} ready on port {model['port']}")
            else:
                print(f"  SKIP {model['name']} failed to start")
        else:
            print(f"  SKIP {model['name']} skipped (model file missing)")

    print()
    print("All priority servers started. Press Ctrl+C to stop.")
    print()
    print("Server endpoints:")
    for model in PRIORITY_MODELS:
        print(f"  {model['name']}: http://127.0.0.1:{model['port']}/v1/chat/completions")

    # Keep running
    try:
        while True:
            time.sleep(10)
            for i, proc in enumerate(processes):
                if proc.poll() is not None:
                    print(f"WARNING: {PRIORITY_MODELS[i]['name']} server died, restarting...")
                    new_proc = start_server(PRIORITY_MODELS[i])
                    if new_proc:
                        processes[i] = new_proc
                        wait_for_server(PRIORITY_MODELS[i]["port"])
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)


if __name__ == "__main__":
    main()
