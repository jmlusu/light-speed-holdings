import os

base = r"C:\Users\jmlus\light-speed-holdings\docs\pharos\linkedin-series"
posts = ["post-04", "post-05", "post-06", "post-07", "post-08", "post-09", "post-10", "post-11"]
images = ["hero", "carousel-1", "carousel-2", "carousel-3", "carousel-4", "carousel-5"]

print("=" * 70)
print("PHAROS LINKEDIN SERIES VISUAL PRODUCTION - AUDIT REPORT")
print("=" * 70)
print()

print("-" * 70)
print("DIRECTORY STRUCTURE")
print("-" * 70)

for post in posts:
    post_dir = os.path.join(base, post, "visuals")
    files = os.listdir(post_dir)
    image_files = [f for f in files if f.endswith(".png")]
    desc_files = [f for f in files if f.endswith("-description.md")]
    print()
    print(f"{post}/visuals/")
    print(f"  PNG files: {len(image_files)}")
    for f in sorted(image_files):
        fpath = os.path.join(post_dir, f)
        size = os.path.getsize(fpath)
        print(f"    - {f} ({size} bytes)")
    print(f"  Description files: {len(desc_files)}")
    for f in sorted(desc_files):
        print(f"    - {f}")

print()
print("-" * 70)
print("SUMMARY COUNTS")
print("-" * 70)
total_png = 0
total_desc = 0
for post in posts:
    post_dir = os.path.join(base, post, "visuals")
    image_files = [f for f in os.listdir(post_dir) if f.endswith(".png")]
    desc_files = [f for f in os.listdir(post_dir) if f.endswith("-description.md")]
    total_png += len(image_files)
    total_desc += len(desc_files)

print(f"Total PNG image files: {total_png}")
print(f"Total description (.md) files: {total_desc}")
print(f"Total files created: {total_png + total_desc}")
print(
    f"Expected: {len(posts) * 6} PNG images + {len(posts) * 6} description files = {len(posts) * 12} total files"
)
if total_png == len(posts) * 6 and total_desc == len(posts) * 6:
    print("Status: COMPLETE")
else:
    print(
        f"Status: PARTIAL - {len(posts) * 6 - total_png} PNG images or {len(posts) * 6 - total_desc} description files missing"
    )
