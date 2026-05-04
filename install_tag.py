import os
import sys
import twc.dsmarshal as dsm
import builtins

args = sys.argv[1:]

if len(args) == 0:
    print(f"usage: {sys.argv[0]} path/to/install.py")
    exit(0)

with open(args[0], "r") as f:
    data = f.read()

im_a_coffee_achiever_sam = os.path.join(os.environ["RENDEREROOT"], "net", "media", "tags")
os.makedirs(im_a_coffee_achiever_sam, exist_ok=True)

def open_fix(path, mode):
    if mode == "w":
        mode = "wb"
    print("open fix ran on ", path, mode)
    return open(path, mode)

ns = {"PKG_ROOT": im_a_coffee_achiever_sam.replace("\\\\", "/").replace("\\", "/"), "dsm": dsm, "open": open_fix}
exec(data, ns, ns)