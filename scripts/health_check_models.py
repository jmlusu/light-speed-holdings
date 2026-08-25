#!/usr/bin/env python3
"""Health check for all llama-server model instances.

Probes each configured model port and reports status.
Exit code 0 = all healthy, 1 = any unhealthy.
"""

import sys
import time
from pathlib import Path

import httpx
import yaml

MODELS_DIR = Path(__file__).parent.parent / "models"


def load_model_config() -> dict:
    """Load llamacpp provider config from company/models.yaml."""
    config_path = Path(__file__).parent.parent / "company" / "models.yaml"
    with open(config_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["providers"]["llamacpp"]


def probe_health(host: str, port: int, api_key: str = "", timeout: float = 5.0) -> dict:
    """Probe a single llama-server health endpoint."""
    headers = {"X-API-Key": api_key} if api_key else {}
    url = f"http://{host}:{port}/health"
    try:
        start = time.time()
        resp = httpx.get(url, timeout=timeout, headers=headers)
        latency_ms = (time.time() - start) * 1000
        return {
            "status": "healthy" if resp.status_code == 200 else f"http_{resp.status_code}",
            "latency_ms": round(latency_ms, 1),
            "body": resp.json() if resp.status_code == 200 else None,
        }
    except httpx.ConnectError:
        return {"status": "unreachable", "latency_ms": None, "body": None}
    except httpx.TimeoutException:
        return {"status": "timeout", "latency_ms": None, "body": None}
    except OSError as e:
        return {"status": f"error: {e}", "latency_ms": None, "body": None}


def main() -> int:
    config = load_model_config()
    host = config["server"]["host"]
    api_key = config["server"].get("api_key", "")
    ports = config["server"]["ports"]

    print(f"{'Model':<28} {'Port':<6} {'Status':<12} {'Latency':>10}")
    print("-" * 60)

    all_healthy = True
    for model_name, port in sorted(ports.items(), key=lambda x: x[1]):
        result = probe_health(host, port, api_key)
        status = result["status"]
        latency = f"{result['latency_ms']}ms" if result["latency_ms"] is not None else "-"
        healthy = status == "healthy"
        if not healthy:
            all_healthy = False
        marker = "+" if healthy else "X"
        print(f"  [{marker}] {model_name:<24} {port:<6} {status:<12} {latency:>10}")

    print()
    if all_healthy:
        print(f"All {len(ports)} model servers healthy.")
    else:
        print("Some model servers are unhealthy.")

    return 0 if all_healthy else 1


if __name__ == "__main__":
    sys.exit(main())
