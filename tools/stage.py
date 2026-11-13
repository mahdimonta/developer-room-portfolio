"""Shared staging canvas.

Every object is drawn on a canvas that uses the SAME origin as room-shell.png,
then cropped to its content. The crop offset is written to room-layout.json, so
PixiJS can place each sprite as an independent layer and still reproduce the
exact isometric composition. Nothing is flattened.
"""
import json
import os
from isolib import Sheet, crop_to_content

W, H = 824, 712
OX, OY = W // 2, 268

ROOT = os.path.join(os.path.dirname(__file__), "..")
ASSETS = os.path.join(ROOT, "public", "assets")
LAYOUT = {"meta": {"canvas": {"w": W, "h": H}, "origin": {"x": OX, "y": OY},
                   "tile": {"w": 64, "h": 32, "z": 32}},
          "sprites": {}, "anims": {}}


def canvas():
    return Sheet(W, H, OX, OY)


def emit(name, sheet, folder, sort=0, pad=0, hotspot=None, note=""):
    """Crop a staged sheet and register its placement."""
    img, (x, y) = crop_to_content(sheet.img, pad)
    if img.width == 0:
        raise ValueError(f"{name}: empty sprite")
    d = os.path.join(ASSETS, folder)
    os.makedirs(d, exist_ok=True)
    rel = f"assets/{folder}/{name}.png"
    img.save(os.path.join(d, f"{name}.png"))
    LAYOUT["sprites"][name] = {
        "src": rel, "x": x, "y": y, "w": img.width, "h": img.height,
        "sort": sort,
    }
    if hotspot:
        LAYOUT["sprites"][name]["hotspot"] = hotspot
    if note:
        LAYOUT["sprites"][name]["note"] = note
    return img


def emit_anim(name, frames, folder, sort=0, fps=8, loop=True, note=""):
    """Pack staged frames into one strip, cropped to the union bbox."""
    from PIL import Image
    boxes = [f.img.getbbox() for f in frames]
    boxes = [b for b in boxes if b]
    x0 = min(b[0] for b in boxes)
    y0 = min(b[1] for b in boxes)
    x1 = max(b[2] for b in boxes)
    y1 = max(b[3] for b in boxes)
    fw, fh = x1 - x0, y1 - y0
    strip = Image.new("RGBA", (fw * len(frames), fh), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        strip.alpha_composite(f.img.crop((x0, y0, x1, y1)), (i * fw, 0))
    d = os.path.join(ASSETS, folder)
    os.makedirs(d, exist_ok=True)
    strip.save(os.path.join(d, f"{name}.png"))
    LAYOUT["anims"][name] = {
        "src": f"assets/{folder}/{name}.png", "x": x0, "y": y0,
        "fw": fw, "fh": fh, "frames": len(frames), "fps": fps,
        "loop": loop, "sort": sort,
    }
    if note:
        LAYOUT["anims"][name]["note"] = note
    return strip


def emit_quad(name, pts, sort=0, kind="screen"):
    """Register a flat 4-point surface (e.g. a monitor screen) in stage space.

    Points are given in canvas pixels, order: top-left, top-right,
    bottom-right, bottom-left of the surface as seen on screen.
    """
    LAYOUT.setdefault("quads", {})[name] = {
        "kind": kind, "sort": sort,
        "points": [[round(p[0], 2), round(p[1], 2)] for p in pts],
    }


def write_layout():
    p = os.path.join(ASSETS, "room", "room-layout.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(LAYOUT, fh, indent=1)
    return p
