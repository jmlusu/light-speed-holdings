#!/usr/bin/env python3
"""Download optimized GGUF models for llama.cpp CPU inference.

Models selected for AMD Ryzen 7 PRO 5850U (8C/16T, 32GB RAM, CPU-only):
- q4_K_M quantization: Best speed/quality balance for 7-8B models
- q5_K_M quantization: Better quality for 9B+ models
"""

import subprocess
import sys
import os
import time
import shutil
from pathlib import Path
from typing import Optional

MODELS = [
    {
        "name": "llama-3.1-8b-instruct-q4_K_M.gguf",
        "repo": "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF",
        "file": "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
        "size_gb": 4.9,
        "description": "General purpose, balanced quality/speed",
    },
    {
        "name": "mistral-7b-instruct-v0.3-q4_K_M.gguf",
        "repo": "bartowski/Mistral-7B-Instruct-v0.3-GGUF",
        "file": "Mistral-7B-Instruct-v0.3-Q4_K_M.gguf",
        "size_gb": 4.4,
        "description": "Fast general tasks, lower latency",
    },
    {
        "name": "gemma-2-9b-it-q5_K_M.gguf",
        "repo": "bartowski/gemma-2-9b-it-GGUF",
        "file": "gemma-2-9b-it-Q5_K_M.gguf",
        "size_gb": 6.8,
        "description": "Higher quality general tasks (premium tier)",
    },
    {
        "name": "qwen2.5-coder-7b-instruct-q4_K_M.gguf",
        "repo": "bartowski/Qwen2.5-Coder-7B-Instruct-GGUF",
        "file": "Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf",
        "size_gb": 4.7,
        "description": "Coding specialist (30% workload)",
    },
    {
        "name": "deepseek-r1-distill-qwen-7b-q4_K_M.gguf",
        "repo": "bartowski/DeepSeek-R1-Distill-Qwen-7B-GGUF",
        "file": "DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf",
        "size_gb": 4.7,
        "description": "Reasoning specialist (40% workload)",
    },
]

MAX_RETRIES = 3
INITIAL_TIMEOUT = 600  # 10 minutes
MAX_TIMEOUT = 3600  # 1 hour


def check_huggingface_cli() -> bool:
    """Check if hf or huggingface-cli is available."""
    for cmd in ["hf", "huggingface-cli"]:
        try:
            subprocess.run([cmd, "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    return False


def get_file_size(path: Path) -> int:
    """Get file size in bytes."""
    try:
        return path.stat().st_size
    except OSError:
        return 0


def format_size(bytes_val: int) -> str:
    """Format bytes as human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f} TB"


def download_with_retry(
    model: dict,
    models_dir: Path,
    hf_token: Optional[str] = None,
    cmd: str = "hf"
) -> bool:
    """Download a model with retry logic and exponential backoff."""
    output_path = models_dir / model["name"]
    expected_size = int(model["size_gb"] * 1024 * 1024 * 1024)

    env = os.environ.copy()
    if hf_token:
        env["HF_TOKEN"] = hf_token

    # Check if already downloaded completely
    if output_path.exists():
        actual_size = get_file_size(output_path)
        if actual_size >= expected_size * 0.95:  # Allow 5% variance
            print(f"[OK] {model['name']} already exists ({format_size(actual_size)}), skipping")
            return True
        else:
            print(f"[RESUME] {model['name']} partial ({format_size(actual_size)}/{format_size(expected_size)}), resuming...")

    base_cmd = [
        cmd,
        "download",
        model["repo"],
        model["file"],
        "--local-dir",
        str(models_dir),
    ]

    timeout = INITIAL_TIMEOUT
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"  [Attempt {attempt}/{MAX_RETRIES}] Downloading {model['name']} ({model['size_gb']} GB)...")
            print(f"    Command: {' '.join(base_cmd)}")
            print(f"    Timeout: {timeout}s")

            result = subprocess.run(
                base_cmd,
                check=True,
                env=env,
                timeout=timeout,
                capture_output=False,
            )

            # Verify download
            downloaded = models_dir / model["file"]
            if downloaded.exists():
                actual_size = get_file_size(downloaded)
                if actual_size >= expected_size * 0.95:
                    if downloaded != output_path:
                        downloaded.rename(output_path)
                    print(f"    [OK] Downloaded {model['name']} ({format_size(actual_size)})")
                    return True
                else:
                    print(f"    [ERROR] File too small: {format_size(actual_size)} (expected ~{format_size(expected_size)})")
            else:
                print(f"    [ERROR] Downloaded file not found")

        except subprocess.TimeoutExpired:
            print(f"    [TIMEOUT] Timeout after {timeout}s")
        except subprocess.CalledProcessError as e:
            print(f"    [ERROR] Command failed with exit code {e.returncode}")
        except FileNotFoundError:
            print(f"    [ERROR] {cmd} not found")
            return False

        if attempt < MAX_RETRIES:
            wait_time = 2 ** attempt  # 2s, 4s, 8s
            print(f"    Retrying in {wait_time}s...")
            time.sleep(wait_time)
            timeout = min(timeout * 2, MAX_TIMEOUT)  # Exponential backoff

    return False


def download_model(model: dict, models_dir: Path, hf_token: Optional[str] = None) -> bool:
    """Download a single model using hf or huggingface-cli with retries."""
    print(f"\n{'='*60}")
    print(f"Downloading: {model['name']}")
    print(f"Description: {model['description']}")
    print(f"Size: {model['size_gb']} GB")
    print(f"Repo: {model['repo']}")
    print(f"{'='*60}")

    # Try hf first, then huggingface-cli
    for cmd in ["hf", "huggingface-cli"]:
        if download_with_retry(model, models_dir, hf_token, cmd):
            return True
        print(f"  {cmd} failed, trying next CLI...")

    print(f"[ERROR] Failed to download {model['name']} after all retries")
    return False


def main():
    models_dir = Path(__file__).parent.parent / "models"
    models_dir.mkdir(exist_ok=True)

    # Read HF_TOKEN from .env
    hf_token = None
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        env_content = env_path.read_text()
        for line in env_content.splitlines():
            line = line.strip()
            if line.startswith("HF_TOKEN="):
                hf_token = line.split("=", 1)[1].strip()
                print(f"Found HF_TOKEN in .env: {hf_token[:10]}...")
                break

    if not check_huggingface_cli():
        print("ERROR: hf or huggingface-cli not found.")
        print("Install with: pip install huggingface_hub")
        print("Then authenticate: hf auth login")
        sys.exit(1)

    print(f"Downloading models to {models_dir}")
    print(f"Total size: ~{sum(m['size_gb'] for m in MODELS):.1f} GB")
    print(f"Max retries per model: {MAX_RETRIES}")
    print(f"Initial timeout: {INITIAL_TIMEOUT}s (max {MAX_TIMEOUT}s)")
    print()

    success = 0
    failed = []
    for model in MODELS:
        if download_model(model, models_dir, hf_token):
            success += 1
        else:
            failed.append(model['name'])

    print(f"\n{'='*60}")
    print(f"SUMMARY: {success}/{len(MODELS)} models downloaded")
    if failed:
        print(f"Failed: {', '.join(failed)}")
        print("Re-run script to retry failed downloads.")
        sys.exit(1)
    print("All models downloaded successfully!")


if __name__ == "__main__":
    main()