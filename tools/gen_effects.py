"""Ambient effects: coffee steam, dust motes, hotspot ring, screen glows."""
import math
from PIL import Image
from isolib import P, mix, radial_glow
from stage import canvas, emit, emit_anim, ASSETS
import os

DESK_H = 1.05


def steam(name, gx, gy, z, sort):
    """8-frame rising steam wisp over a mug."""
    frames = []
    n = 8
    for i in range(n):
        s = canvas()
        t = i / n
        for k in range(3):
            ph = t + k * 0.33
            rise = (ph % 1.0)
            a = int(130 * (1 - rise) ** 1.4)
            if a <= 2:
                continue
            wob = math.sin(rise * 6 + k * 2) * 3
            p = s.p(gx, gy, z + 0.12 + rise * 0.6)
            r = 2 + int(rise * 4)
            s.d.ellipse([p[0] - r + wob, p[1] - r, p[0] + r + wob, p[1] + r],
                        fill=(214, 228, 255, a))
        frames.append(s)
    emit_anim(name, frames, "effects", sort=sort, fps=7,
              note="coffee steam")


def dust():
    """Slow-drifting dust motes in the lamp light (one seamless loop)."""
    import random
    rnd = random.Random(5)
    n, w, h = 10, 220, 180
    motes = [(rnd.randrange(w), rnd.randrange(h), rnd.choice([1, 1, 2]),
              rnd.random()) for _ in range(34)]
    frames = []
    for i in range(n):
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        px = im.load()
        t = i / n
        for (x, y, sz, ph) in motes:
            yy = int((y - t * 26) % h)
            xx = int((x + math.sin((t + ph) * math.tau) * 5) % w)
            a = int(90 * (0.4 + 0.6 * abs(math.sin((t + ph) * math.pi))))
            for dx in range(sz):
                for dy in range(sz):
                    if xx + dx < w and yy + dy < h:
                        px[xx + dx, yy + dy] = (226, 238, 255, a)
        frames.append(im)
    strip = Image.new("RGBA", (w * n, h), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        strip.alpha_composite(f, (i * w, 0))
    d = os.path.join(ASSETS, "effects")
    os.makedirs(d, exist_ok=True)
    strip.save(os.path.join(d, "dust-sheet.png"))
    from stage import LAYOUT
    LAYOUT["anims"]["dust"] = {
        "src": "assets/effects/dust-sheet.png", "x": 150, "y": 150,
        "fw": w, "fh": h, "frames": n, "fps": 5, "loop": True, "sort": 40,
        "note": "dust motes drifting in the lamp light",
    }
    print("dust-sheet", strip.size)


def ui_bits():
    """Hotspot ring + glow blobs used by the interaction layer."""
    d = os.path.join(ASSETS, "ui")
    os.makedirs(d, exist_ok=True)
    # isometric hover ring (a flat diamond outline)
    im = Image.new("RGBA", (96, 56), (0, 0, 0, 0))
    dr = __import__("PIL.ImageDraw", fromlist=["ImageDraw"]).Draw(im)
    for inset, col in ((0, (70, 228, 224, 210)), (3, (70, 228, 224, 90))):
        dr.polygon([(48, 4 + inset), (92 - inset, 28), (48, 52 - inset),
                    (4 + inset, 28)], outline=col)
    im.save(os.path.join(d, "hotspot-ring.png"))
    # click indicator chevron
    ic = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    dc = __import__("PIL.ImageDraw", fromlist=["ImageDraw"]).Draw(ic)
    dc.polygon([(12, 3), (21, 14), (16, 14), (16, 21), (8, 21), (8, 14), (3, 14)],
               fill=(255, 179, 71, 235), outline=(16, 14, 32, 255))
    ic.save(os.path.join(d, "hotspot-arrow.png"))
    # reusable glows
    for nm, col, st in (("glow-cyan", "cyan", 0.5), ("glow-amber", "amber", 0.5),
                        ("glow-magenta", "magenta", 0.5),
                        ("glow-white", "white", 0.42)):
        radial_glow(128, 128, col, st, 2.1).save(os.path.join(d, f"{nm}.png"))
    print("ui bits ->", d)


def main():
    steam("steam-desk", 3.5 + 0.13, 0.25 + 1.15 + 0.13, DESK_H + 0.3, sort=27)
    steam("steam-machine", 7.9 + 1.1 + 0.13, 0.35 + 0.45 + 0.13, 1.8, sort=21)
    dust()
    ui_bits()
    print("effects done")


if __name__ == "__main__":
    main()
