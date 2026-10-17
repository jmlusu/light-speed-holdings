import urllib.request

r = urllib.request.urlopen("http://127.0.0.1:1441/", timeout=5)
body = r.read().decode("utf-8", errors="replace")

# Look for lightspeed-specific content
ls_markers = ["lightspeed", "LIGHTSPEED", "Holdings", "logo", "nav", "header"]
for marker in ls_markers:
    if marker.lower() in body.lower():
        idx = body.lower().find(marker.lower())
        start = max(0, idx - 50)
        end = min(len(body), idx + 100)
        print(f'Found "{marker}" at position {idx}: ...{body[start:end]}...')
    else:
        print(f'Marker "{marker}" not found in body')

print("---")
print(f"Total body length: {len(body)}")
# Print first 2000 chars
print(f"First 2000 chars preview: {body[:2000]}")
