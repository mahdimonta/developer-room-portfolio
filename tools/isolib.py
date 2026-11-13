"""Isometric pixel-art drawing toolkit (2:1 projection).

All sprites in THE DEVELOPER'S ROOM are generated with this library so that
every asset shares one palette, one isometric angle (2:1), one light direction
(upper-left) and one outline style. Output is nearest-neighbour friendly.
"""
from PIL import Image, ImageDraw

# --- projection ------------------------------------------------------------
TW, TH, ZH = 64, 32, 32          # cell width, cell depth, cell height in px
HX, HY = TW // 2, TH // 2


def iso(gx, gy, gz=0.0):
    """Grid cell coords -> screen px (relative to grid origin)."""
    return ((gx - gy) * HX, (gx + gy) * HY - gz * ZH)


def off(p, dx, dy):
    return (p[0] + dx, p[1] + dy)


# --- palette ---------------------------------------------------------------
P = {
    "void":       (8, 8, 20),
    "night":      (12, 16, 38),
    "wall":       (40, 46, 88),
    "wall_lit":   (54, 62, 112),
    "wall_dark":  (27, 32, 64),
    "wall_edge":  (68, 78, 136),
    "skirt":      (32, 29, 60),
    "floor":      (70, 52, 86),
    "floor_lit":  (86, 64, 104),
    "floor_dark": (54, 40, 68),
    "floor_line": (37, 27, 48),
    "rug":        (46, 32, 74),
    "rug_lit":    (62, 44, 98),
    "rug_dark":   (34, 23, 56),
    "wood":       (76, 56, 94),
    "wood_lit":   (95, 71, 116),
    "wood_dark":  (54, 39, 68),
    "wood_edge":  (112, 86, 134),
    "metal":      (62, 70, 104),
    "metal_lit":  (88, 98, 139),
    "metal_dark": (41, 47, 74),
    "plastic":    (33, 37, 60),
    "plastic_lit": (50, 56, 88),
    "plastic_dark": (21, 24, 41),
    "screen":     (12, 20, 40),
    "screen_lit": (20, 34, 66),
    "cyan":       (70, 228, 224),
    "cyan_dim":   (38, 140, 148),
    "cyan_pale":  (168, 247, 245),
    "blue":       (74, 125, 255),
    "blue_dim":   (44, 73, 160),
    "violet":     (150, 112, 255),
    "magenta":    (255, 77, 157),
    "amber":      (255, 179, 71),
    "amber_dim":  (176, 114, 38),
    "orange":     (255, 122, 61),
    "green":      (116, 214, 128),
    "green_dim":  (62, 128, 76),
    "leaf":       (74, 170, 112),
    "leaf_dark":  (44, 112, 76),
    "white":      (232, 236, 255),
    "gray":       (138, 147, 194),
    "gray_dark":  (84, 90, 128),
    "ink":        (16, 14, 32),
    "skin":       (214, 158, 122),
    "skin_dark":  (170, 118, 90),
    "hair":       (36, 28, 46),
    "hair_lit":   (58, 46, 72),
    "hood":       (44, 52, 96),
    "hood_lit":   (62, 74, 130),
    "hood_dark":  (28, 33, 64),
    "cat":        (74, 70, 96),
    "cat_lit":    (102, 97, 128),
    "cat_dark":   (50, 47, 68),
    "cat_pale":   (196, 190, 216),
}


def rgba(key, a=255):
    if isinstance(key, tuple):
        return key if len(key) == 4 else key + (a,)
    c = P[key]
    return (c[0], c[1], c[2], a)


def mix(a, b, t):
    ca, cb = P[a] if isinstance(a, str) else a, P[b] if isinstance(b, str) else b
    return tuple(int(round(ca[i] + (cb[i] - ca[i]) * t)) for i in range(3))


def shade(key, t):
    """t<0 darken toward ink, t>0 lighten toward white."""
    return mix(key, "ink" if t < 0 else "white", abs(t))


# --- canvas ----------------------------------------------------------------
class Sheet:
    """A transparent pixel canvas with isometric helpers."""

    def __init__(self, w, h, ox=None, oy=0):
        self.img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)
        self.ox = w // 2 if ox is None else ox
        self.oy = oy

    # ---- coordinate helpers
    def p(self, gx, gy, gz=0.0):
        x, y = iso(gx, gy, gz)
        return (int(round(x + self.ox)), int(round(y + self.oy)))

    def poly(self, pts, fill, outline=None):
        self.d.polygon(pts, fill=fill, outline=outline)

    def line(self, pts, fill, w=1):
        self.d.line(pts, fill=fill, width=w)

    def px(self, x, y, fill):
        self.d.point((x, y), fill=fill)

    def rect(self, x0, y0, x1, y1, fill, outline=None):
        self.d.rectangle([x0, y0, x1, y1], fill=fill, outline=outline)

    # ---- isometric primitives
    def tile(self, gx, gy, fill, gz=0.0, outline=None):
        """One flat diamond at grid cell (gx, gy)."""
        t = self.p(gx, gy, gz)
        pts = [off(t, 0, 0), off(t, HX, HY), off(t, 0, TH), off(t, -HX, HY)]
        self.poly(pts, fill, outline)
        return pts

    def quad(self, a, b, c, d, fill, outline=None):
        self.poly([a, b, c, d], fill, outline)

    def box(self, gx, gy, gz, sx, sy, sz, top, left, right,
            outline=None, top_only=False):
        """Axis-aligned isometric box. (gx,gy,gz) = near-left-bottom corner.

        Faces: top (up), left (toward -x screen, the +y side), right (+x side).
        Drawn back-to-front so a later box occludes an earlier one correctly.
        """
        z0, z1 = gz, gz + sz
        # top face corners
        t_n = self.p(gx, gy, z1)
        t_e = self.p(gx + sx, gy, z1)
        t_s = self.p(gx + sx, gy + sy, z1)
        t_w = self.p(gx, gy + sy, z1)
        # bottom corners for the two visible side faces
        b_e = self.p(gx + sx, gy, z0)
        b_s = self.p(gx + sx, gy + sy, z0)
        b_w = self.p(gx, gy + sy, z0)
        if not top_only:
            # right face (+x): t_e t_s b_s b_e
            self.quad(t_e, t_s, b_s, b_e, right, outline)
            # left face (+y): t_w t_s b_s b_w
            self.quad(t_w, t_s, b_s, b_w, left, outline)
        self.quad(t_n, t_e, t_s, t_w, top, outline)
        return dict(t_n=t_n, t_e=t_e, t_s=t_s, t_w=t_w, b_e=b_e, b_s=b_s, b_w=b_w)

    def box_mat(self, gx, gy, gz, sx, sy, sz, mat, outline=None, lift=0.12):
        """Box shaded from one palette key with the project's light direction."""
        base = P[mat] if isinstance(mat, str) else mat
        return self.box(gx, gy, gz, sx, sy, sz,
                        top=mix(base, "white", 0.18 + lift),
                        left=mix(base, "ink", 0.34),
                        right=mix(base, "ink", 0.12),
                        outline=outline)

    def save(self, path):
        self.img.save(path)
        return path


def new_sheet(w, h, ox=None, oy=0):
    return Sheet(w, h, ox, oy)


def paste(dst: Sheet, src: Sheet, x=0, y=0):
    dst.img.alpha_composite(src.img, (x, y))


def outline_sprite(img, color=(10, 10, 24, 190), diagonals=False):
    """Add a 1px dark outline around opaque pixels (classic pixel-art look)."""
    w, h = img.size
    a = img.load()
    out = img.copy()
    o = out.load()
    nb = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if diagonals:
        nb += [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    for y in range(h):
        for x in range(w):
            if a[x, y][3] != 0:
                continue
            for dx, dy in nb:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and a[nx, ny][3] > 128:
                    o[x, y] = color
                    break
    return out


def radial_glow(w, h, color, strength=0.75, power=2.2):
    """Soft additive-looking glow blob, pre-baked (no runtime filters needed)."""
    g = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = g.load()
    cx, cy = (w - 1) / 2, (h - 1) / 2
    r = max(cx, cy)
    c = P[color] if isinstance(color, str) else color
    for y in range(h):
        for x in range(w):
            dx, dy = (x - cx) / r, (y - cy) / r
            d = (dx * dx + dy * dy) ** 0.5
            if d >= 1:
                continue
            a = int(255 * strength * (1 - d) ** power)
            if a > 0:
                px[x, y] = (c[0], c[1], c[2], a)
    return g


def dither(sheet: Sheet, pts, color, density=2, alpha=70):
    """Checkerboard dither inside a polygon's bounding box, clipped by mask."""
    mask = Image.new("L", sheet.img.size, 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    layer = Image.new("RGBA", sheet.img.size, (0, 0, 0, 0))
    lp = layer.load()
    c = P[color] if isinstance(color, str) else color
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    for y in range(max(0, int(min(ys))), min(sheet.img.height, int(max(ys)) + 1)):
        for x in range(max(0, int(min(xs))), min(sheet.img.width, int(max(xs)) + 1)):
            if (x + y) % density == 0:
                lp[x, y] = (c[0], c[1], c[2], alpha)
    layer.putalpha(Image.composite(layer.getchannel("A"),
                                   Image.new("L", layer.size, 0), mask))
    sheet.img.alpha_composite(layer)


def pack_strip(frames, path, json_path=None, name="anim"):
    """Pack equal-size frames into a horizontal strip + optional atlas JSON."""
    import json
    w = max(f.width for f in frames)
    h = max(f.height for f in frames)
    sheet = Image.new("RGBA", (w * len(frames), h), (0, 0, 0, 0))
    meta = {"frames": {}, "meta": {"image": path.split("/")[-1],
                                   "format": "RGBA8888",
                                   "size": {"w": w * len(frames), "h": h},
                                   "scale": "1"}}
    for i, f in enumerate(frames):
        sheet.alpha_composite(f, (i * w, 0))
        meta["frames"][f"{name}_{i}"] = {
            "frame": {"x": i * w, "y": 0, "w": w, "h": h},
            "rotated": False, "trimmed": False,
            "spriteSourceSize": {"x": 0, "y": 0, "w": w, "h": h},
            "sourceSize": {"w": w, "h": h},
        }
    sheet.save(path)
    if json_path:
        meta["animations"] = {name: [f"{name}_{i}" for i in range(len(frames))]}
        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(meta, fh, indent=1)
    return path, (w, h, len(frames))


def crop_to_content(img, pad=0):
    bb = img.getbbox()
    if bb is None:
        return img, (0, 0)
    x0, y0, x1, y1 = bb
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(img.width, x1 + pad), min(img.height, y1 + pad)
    return img.crop((x0, y0, x1, y1)), (x0, y0)
