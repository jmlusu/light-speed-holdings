#!/usr/bin/env python3
import os
import subprocess
import time
import urllib.request
import urllib.error

os.chdir(r"C:\Users\jmlus\light-speed-holdings")

vite_bin = r"C:\Users\jmlus\light-speed-holdings\node_modules\.bin\vite.cmd"

# Start Vite dev server on port 1441
env = os.environ.copy()
env["PORT"] = "1441"
env["VITE_TURNSTILE_SITE_KEY"] = "0x4AAAAAAE404z2CBA0ZUph1"

print("=" * 60)
print("Starting Vite development server (port 1441)...")
print("=" * 60)

dev_proc = subprocess.Popen(
    [vite_bin, "--mode", "development"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    env=env,
    text=True,
    bufsize=1,
)

# Read output until "ready in" appears
output_line = ""
for line in dev_proc.stdout:
    print(line, end="")
    if "ready in" in line:
        break

# Wait a bit for server to fully start
time.sleep(3)

print("\n" + "=" * 60)
print("Testing Vite dev server connectivity...")
print("=" * 60)

# Test 127.0.0.1
try:
    r = urllib.request.urlopen("http://127.0.0.1:1441/", timeout=5)
    body = r.read().decode("utf-8", errors="replace")
    print(f"\n✓ 127.0.0.1:1441 connected! Status: {r.status}")
    print(f"  Body length: {len(body)} chars")
except urllib.error.URLError as e:
    print(f"\n✗ 127.0.0.1:1441 FAILED: {e}")

# Test localhost
try:
    r = urllib.request.urlopen("http://localhost:1441/", timeout=5)
    body = r.read().decode("utf-8", errors="replace")
    print(f"\n✓ localhost:1441 connected! Status: {r.status}")
    print(f"  Body length: {len(body)} chars")
except urllib.error.URLError as e:
    print(f"\n✗ localhost:1441 FAILED: {e}")

# Test network addresses
for addr in ["192.168.1.136", "192.168.80.1", "172.19.48.1"]:
    try:
        r = urllib.request.urlopen(f"http://{addr}:1441/", timeout=5)
        body = r.read().decode("utf-8", errors="replace")
        print(f"\n✓ {addr}:1441 connected! Status: {r.status}")
    except urllib.error.URLError as e:
        print(f"\n✗ {addr}:1441 FAILED: {e}")

print("\n" + "=" * 60)
print("Starting Vite preview server (port 1440)...")
print("=" * 60)

# Start Vite preview server on port 1440
preview_env = env.copy()
preview_env["PORT"] = "1440"

preview_proc = subprocess.Popen(
    [vite_bin, "--mode", "development"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    env=preview_env,
    text=True,
    bufsize=1,
)

# Override preview port by setting VITE_PREVIEW_PORT or modifying config
# Actually, vite preview uses port 1440 by default from config
# Let's just test the default

time.sleep(3)

print("\n" + "=" * 60)
print("Testing Vite preview server connectivity (port 1440)...")
print("=" * 60)

# Test 127.0.0.1:1440
try:
    r = urllib.request.urlopen("http://127.0.0.1:1440/", timeout=5)
    body = r.read().decode("utf-8", errors="replace")
    print(f"\n✓ 127.0.0.1:1440 connected! Status: {r.status}")
except urllib.error.URLError as e:
    print(f"\n✗ 127.0.0.1:1440 FAILED: {e}")

# Test localhost:1440
try:
    r = urllib.request.urlopen("http://localhost:1440/", timeout=5)
    body = r.read().decode("utf-8", errors="replace")
    print(f"\n✓ localhost:1440 connected! Status: {r.status}")
except urllib.error.URLError as e:
    print(f"\n✗ localhost:1440 FAILED: {e}")

# Terminate processes
print("\n" + "=" * 60)
print("Terminating servers...")
print("=" * 60)
dev_proc.terminate()
preview_proc.terminate()
dev_proc.wait()
preview_proc.wait()
print("Done.")
