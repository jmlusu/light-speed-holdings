#!/usr/bin/env python3
"""Download optimized GGUF models for llama.cpp CPU inference.

Models selected for AMD Ryzen 7 PRO 5850U (8C/16T, 32GB RAM, CPU-only):
- q4_K_M quantization: Best speed/quality balance for 7-8B models
- q5_K_M quantization: Better quality for 9B+ models
"""

import subprocess
import sys
from pathlib import Path

MODELS = [
    {
        "name": "llama-3.1-8b-instruct-q4_K_M.gguf",
        "repo": "bartowski/Llama-3.1-8B-Instruct-GGUF",
        "file": "llama-3.1-8b-instruct-q4_K_M.gguf",
        "size_gb": 4.9,
        "description": "General purpose, balanced quality/speed",
    },
    {
        "name": "mistral-7b-instruct-v0.3-q4_K_M.gguf",
        "repo": "bartowski/Mistral-7B-Instruct-v0.3-GGUF",
        "file": "mistral-7b-instruct-v0.3-q4_K_M.gguf",
        "size_gb": 4.4,
        "description": "Fast general tasks, lower latency",
    },
    {
        "name": "gemma-2-9b-it-q5_K_M.gguf",
        "repo": "bartowski/gemma-2-9b-it-GGUF",
        "file": "gemma-2-9b-it-q5_K_M.gguf",
        "size_gb": 6.8,
        "description": "Higher quality general tasks (premium tier)",
    },
    {
        "name": "qwen2.5-coder-7b-instruct-q4_K_M.gguf",
        "repo": "bartowski/Qwen2.5-Coder-7B-Instruct-GGUF",
        "file": "qwen2.5-coder-7b-instruct-q4_K_M.gguf",
        "size_gb": 4.7,
        "description": "Coding specialist (30% workload)",
    },
    {
        "name": "deepseek-r1-distill-qwen-7b-q4_K_M.gguf",
        "repo": "bartowski/DeepSeek-R1-Distill-Qwen-7B-GGUF",
        "file": "deepseek-r1-distill-qwen-7b-q4_K_M.gguf",
        "size_gb": 4.7,
        "description": "Reasoning specialist (40% workload)",
    },
]


def check_huggingface_cli() -> bool:
    """Check if huggingface-cli is available."""
    try:
        subprocess.run(["huggingface-cli", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def download_model(model: dict, models_dir: Path) -> bool:
    """Download a single model using huggingface-cli."""
    output_path = models_dir / model["name"]
    if output_path.exists():
        print(f"✓ {model['name']} already exists, skipping")
        return True

    print(f"⬇ Downloading {model['name']} ({model['size_gb']} GB) - {model['description']}")
    try:
        subprocess.run(
            [
                "huggingface-cli",
                "download",
                model["repo"],
                model["file"],
                "--local-dir",
                str(models_dir),
                "--local-dir-use-symlinks",
                "False",
            ],
            check=True,
        )
        print(f"✓ Downloaded {model['name']}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to download {model['name']}: {e}")
        return False


def main():
    models_dir = Path(__file__).parent / "models"
    models_dir.mkdir(exist_ok=True)

    if not check_huggingface_cli():
        print("ERROR: huggingface-cli not found.")
        print("Install with: pip install huggingface_hub")
        print("Then authenticate: huggingface-cli login")
        sys.exit(1)

    print(f"Downloading models to {models_dir}")
    print(f"Total size: ~{sum(m['size_gb'] for m in MODELS):.1f} GB")
    print()

    success = 0
    for model in MODELS:
        if download_model(model, models_dir):
            success += 1
        print()

    print(f"Completed: {success}/{len(MODELS)} models downloaded")
    if success < len(MODELS):
        print("Some downloads failed. Re-run script to retry.")
        sys.exit(1)


if __name__ == "__main__":
    main()
