"""Generate the room shell: floor, walls, skirting, window, rug, light pools.

Grid: 10 x 10 cells of 48x24 px, wall height 7 cells.
Origin is placed so the whole room fits the canvas.
"""
import os
from PIL import Image
from isolib import (Sheet, P, HX, HY, TH, ZH, mix, off, dither,
                    radial_glow, crop_to_content)

OUT = os.path.join(os.path.dirname(__file__), "..", "public", "assets", "room")
GW = GD = 11          # grid width / depth in cells
WALL = 7              # wall height in cells
W, H = 824, 712
OX, OY = W // 2, 268


def sheet():
    return Sheet(W, H, OX, OY)


def draw_floor(s):
    for gy in range(GD):
        for gx in range(GW):
            far = (gx + gy) / (GW + GD - 2)
            base = mix("floor", "floor_dark", 0.3 * (1 - far))
            # soft light pool toward the desk corner (upper-left light)
            lit = max(0.0, 1.0 - ((gx - 2.0) ** 2 + (gy - 3.0) ** 2) / 34.0)
            base = mix(base, "floor_lit", 0.6 * lit)
            if (gx + gy) % 2 == 0:
                base = mix(base, "white", 0.03)
            pts = s.tile(gx, gy, base)
            s.poly(pts, None, outline=mix(base, "ink", 0.3))
    # plank seams every 2 cells for texture
    for gx in range(0, GW + 1, 2):
        a, b = s.p(gx, 0), s.p(gx, GD)
        s.line([a, b], mix("floor_line", "ink", 0.2))


def draw_rug(s):
    cx, cy, r = 3.3, 4.6, 2.0
    pts = []
    import math
    for i in range(44):
        t = i / 44 * math.tau
        gx = cx + math.cos(t) * r
        gy = cy + math.sin(t) * r * 0.95
        pts.append(s.p(gx, gy))
    s.poly(pts, P["rug"], outline=mix("rug", "ink", 0.4))
    inner = []
    for i in range(44):
        t = i / 44 * math.tau
        inner.append(s.p(cx + math.cos(t) * (r - 0.55),
                         cy + math.sin(t) * (r - 0.55) * 0.95))
    s.poly(inner, mix("rug", "rug_lit", 0.55), outline=mix("rug", "ink", 0.2))
    dither(s, inner, "violet", density=3, alpha=36)


def draw_walls(s):
    top = WALL
    # ---- back-left wall (the gy = 0 plane, faces +y / viewer-right)
    for gx in range(GW):
        shade_t = 0.12 + 0.05 * (gx / GW)
        col = mix("wall", "wall_lit", 0.45 - shade_t)
        a, b = s.p(gx, 0, top), s.p(gx + 1, 0, top)
        c, d = s.p(gx + 1, 0, 0), s.p(gx, 0, 0)
        s.quad(a, b, c, d, col, outline=mix(col, "ink", 0.22))
    # ---- back-right wall (the gx = 0 plane, faces +x / viewer-left) darker
    for gy in range(GD):
        col = mix("wall_dark", "wall", 0.42 - 0.04 * (gy / GD))
        a, b = s.p(0, gy, top), s.p(0, gy + 1, top)
        c, d = s.p(0, gy + 1, 0), s.p(0, gy, 0)
        s.quad(a, b, c, d, col, outline=mix(col, "ink", 0.26))
    # ---- top trim
    s.line([s.p(0, 0, top), s.p(GW, 0, top)], P["wall_edge"])
    s.line([s.p(0, 0, top), s.p(0, GD, top)], mix("wall_edge", "ink", 0.3))
    # ---- skirting boards
    for gx in range(GW):
        a, b = s.p(gx, 0, 0.3), s.p(gx + 1, 0, 0.3)
        c, d = s.p(gx + 1, 0, 0), s.p(gx, 0, 0)
        s.quad(a, b, c, d, P["skirt"], outline=mix("skirt", "ink", 0.3))
    for gy in range(GD):
        a, b = s.p(0, gy, 0.3), s.p(0, gy + 1, 0.3)
        c, d = s.p(0, gy + 1, 0), s.p(0, gy, 0)
        s.quad(a, b, c, d, mix("skirt", "ink", 0.2),
               outline=mix("skirt", "ink", 0.4))
    # corner seam
    s.line([s.p(0, 0, top), s.p(0, 0, 0)], mix("wall_dark", "ink", 0.25))


def main():
    os.makedirs(OUT, exist_ok=True)
    s = sheet()
    draw_walls(s)
    draw_floor(s)
    draw_rug(s)
    s.img.save(os.path.join(OUT, "room-shell.png"))
    print("room-shell", s.img.size)


if __name__ == "__main__":
    main()
