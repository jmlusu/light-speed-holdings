import os

candidates = [
    r"C:\Users\jmlus\light-speed-holdings\lightspeed-main-site",
    r"C:\Users\jmlus\light-speed-holdings\website",
]
for c in candidates:
    exists = os.path.exists(c)
    if exists:
        print(c, "exists")
    else:
        print(c, "not exists")
