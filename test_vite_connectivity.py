#!/usr/bin/env python3
import os
import socket
import subprocess
import time
import urllib.error
import urllib.request

os.chdir(r"C:\Users\jmlus\light-speed-holdings")

VITE_CMD = r".\node_modules\.bin\vite.cmd"
PORT = 1441


def start_vite_dev_server():
    """Start Vite development server on specified port."""
    env = os.environ.copy()
    env["PORT"] = str(PORT)
    env["VITE_TURNSTILE_SITE_KEY"] = "0x4AAAAAAE404z2CBA0ZUph1"

    print(f"Starting Vite dev server on port {PORT}...")
    proc = subprocess.Popen(
        [VITE_CMD, "--mode", "development"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        text=True,
        bufsize=1,
    )

    # Wait for server to be ready
    for line in proc.stdout:
        print(line, end="")
        if "ready in" in line:
            break

    # Wait additional time for server to stabilize
    time.sleep(3)
    return proc


def test_connectivity(addr, port, label):
    """Test HTTP connectivity to a given address:port."""
    url = f"http://{addr}:{port}/"
    try:
        r = urllib.request.urlopen(url, timeout=5)
        body = r.read().decode("utf-8", errors="replace")[:200]
        status = r.status
        print(f"  [OK] {label} ({url}) - Status {status}, {len(body)} chars")
        return True, body
    except urllib.error.URLError as e:
        err_str = str(e).lower()
        if "timed out" in err_str:
            print(f"  [TIMEOUT] {label} ({url}) - connection established but no response within 5s")
        else:
            print(f"  [FAIL] {label} ({url}) - {type(e).__name__}: {str(e)[:100]}")
        return False, None


def is_port_open(port):
    """Check if a port is open on localhost."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    result = s.connect_ex(("127.0.0.1", port))
    s.close()
    return result == 0


# Main test
print("=" * 60)
print("LIGHTSPEED HOLDINGS: Vite Server Connectivity Investigation")
print("=" * 60)

# Check initial state
print("\n--- Initial State ---")
print(f"Port 1441 open: {is_port_open(1441)}")
print(f"Port 1440 open: {is_port_open(1440)}")

# Start Vite dev server
print("\n--- Starting Vite Dev Server ---")
dev_proc = start_vite_dev_server()

print("\n--- Connectivity Tests ---")
print(f"\n127.0.0.1:{PORT}:")
test_connectivity("127.0.0.1", PORT, "127.0.0.1")

print(f"\nlocalhost:{PORT}:")
test_connectivity("localhost", PORT, "localhost")

print(f"\n192.168.1.136:{PORT}:")
test_connectivity("192.168.1.136", PORT, "192.168.1.136")

print(f"\n192.168.80.1:{PORT}:")
test_connectivity("192.168.80.1", PORT, "192.168.80.1")

print(f"\n172.19.48.1:{PORT}:")
test_connectivity("172.19.48.1", PORT, "172.19.48.1")

# Also check port 1440
print("\n\nPort 1440 (preview) connectivity:")
print("  127.0.0.1:1440:")
test_connectivity("127.0.0.1", 1440, "127.0.0.1")
print("  localhost:1440:")
test_connectivity("localhost", 1440, "localhost")
print("  192.168.1.136:1440:")
test_connectivity("192.168.1.136", 1440, "192.168.1.136")

# Cleanup
print("\n--- Cleanup ---")
dev_proc.terminate()
try:
    dev_proc.wait(timeout=5)
except Exception as e:
    dev_proc.kill()

print("\n" + "=" * 60)
print("Test complete.")
print("=" * 60)
