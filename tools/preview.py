"""Compose a flat preview of the staged layers (QA only, not shipped).

The real site keeps every layer separate; this only proves the alignment
and the visual consistency of the generated sprites.
"""
import json
import os
import sys
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..")
ASSETS = os.path.join(ROOT, "public", "assets")
LAYOUT = json.load(open(os.path.join(ASSETS, "room", "room-layout.json"),
                        encoding="utf-8"))


def compose(out="docs/_preview_room.png", scale=1, show_quads=False):
    m = LAYOUT["meta"]["canvas"]
    base = Image.new("RGBA", (m["w"], m["h"]), (10, 10, 24, 255))
    shell = Image.open(os.path.join(ASSETS, "room", "room-shell.png"))
    base.alpha_composite(shell, (0, 0))

    # window view goes behind the frame layers
    q = LAYOUT.get("quads", {}).get("window-glass")
    if q:
        pts = q["points"]
        city = Image.open(os.path.join(ASSETS, "room", "city-night.png"))
        x0 = int(min(p[0] for p in pts))
        y0 = int(min(p[1] for p in pts))
        x1 = int(max(p[0] for p in pts))
        y1 = int(max(p[1] for p in pts))
        base.alpha_composite(city.resize((x1 - x0, y1 - y0)), (x0, y0))

    items = []
    for name, s in LAYOUT["sprites"].items():
        items.append((s["sort"], name, s, False))
    for name, a in LAYOUT["anims"].items():
        items.append((a["sort"], name, a, True))
    items.sort(key=lambda t: (t[0], t[1]))

    for sort, name, s, is_anim in items:
        if is_anim:
            # show only resting idle frames so anim layers don't stack
            if name.startswith("char-") and name != "char-idle":
                continue
            if name.startswith("cat-") and name != "cat-sleep":
                continue
        p = os.path.join(ROOT, "public", s["src"])
        if not os.path.exists(p):
            print("MISSING", p)
            continue
        im = Image.open(p).convert("RGBA")
        if is_anim:
            im = im.crop((0, 0, s["fw"], s["fh"]))
        base.alpha_composite(im, (s["x"], s["y"]))

    if scale != 1:
        base = base.resize((base.width * scale, base.height * scale),
                           Image.NEAREST)
    dst = os.path.join(ROOT, out)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    base.convert("RGB").save(dst)
    print("preview ->", dst, base.size, f"{len(items)} layers")


if __name__ == "__main__":
    compose(*(sys.argv[1:] or []))
