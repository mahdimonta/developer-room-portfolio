"""Generate every room prop as an independent, correctly-aligned layer.

Layout (grid cells, 11x11 room, wall height 7):
  gy = 0 plane  -> upper-right wall  (desk, project shelf, window, poster)
  gx = 0 plane  -> upper-left wall   (bookshelf, posters, wall lamp)
Depth sort key is roughly (gx + gy) so near objects draw over far ones.
"""
import math
from isolib import P, mix, off, dither, radial_glow, outline_sprite
from stage import canvas, emit, emit_anim, emit_quad, write_layout

# ---------------------------------------------------------------- desk ------
DESK = dict(gx=1.6, gy=0.25, sx=5.4, sy=1.7, h=1.05)


def desk():
    s = canvas()
    d = DESK
    # back panel / modesty board
    s.box_mat(d["gx"], d["gy"], 0.0, d["sx"], 0.12, d["h"] - 0.08, "wood_dark")
    # legs
    for lx in (d["gx"] + 0.08, d["gx"] + d["sx"] - 0.3):
        for ly in (d["gy"] + 0.15, d["gy"] + d["sy"] - 0.35):
            s.box_mat(lx, ly, 0.0, 0.22, 0.2, d["h"] - 0.1, "metal_dark")
    # cable tray
    s.box_mat(d["gx"] + 0.8, d["gy"] + 0.55, d["h"] - 0.42, d["sx"] - 1.6, 0.5,
              0.1, "metal_dark")
    # top slab
    t = s.box(d["gx"], d["gy"], d["h"] - 0.1, d["sx"], d["sy"], 0.12,
              top=mix("wood", "white", 0.3),
              left=mix("wood", "ink", 0.42),
              right=mix("wood", "ink", 0.16),
              outline=mix("wood", "ink", 0.5))
    # top wood grain
    for i in range(1, 7):
        gy = d["gy"] + d["sy"] * i / 7
        a = s.p(d["gx"], gy, d["h"] + 0.02)
        b = s.p(d["gx"] + d["sx"], gy, d["h"] + 0.02)
        s.line([a, b], mix("wood", "wood_lit", 0.5 if i % 2 else 0.2))
    # front edge highlight
    s.line([t["t_s"], t["t_w"]], mix("wood_edge", "white", 0.15))
    s.line([t["t_e"], t["t_s"]], mix("wood_edge", "white", 0.05))
    emit("desk", s, "furniture", sort=22, note="main computer desk")


# --------------------------------------------------------------- drawers ----
def drawers():
    s = canvas()
    gx, gy = DESK["gx"] + 4.05, DESK["gy"] + 0.25
    s.box_mat(gx, gy, 0.0, 1.2, 1.2, DESK["h"] - 0.12, "plastic")
    for i in range(3):
        z = 0.12 + i * 0.29
        f = s.box(gx + 0.02, gy + 0.02, z, 1.16, 1.16, 0.24,
                  top=mix("plastic_lit", "ink", 0.1),
                  left=mix("plastic", "ink", 0.18),
                  right=mix("plastic_lit", "ink", 0.02),
                  outline=mix("plastic_dark", "ink", 0.3))
        mid = ((f["t_w"][0] + f["b_s"][0]) // 2, (f["t_w"][1] + f["b_s"][1]) // 2)
        s.rect(mid[0] - 7, mid[1] - 1, mid[0] + 7, mid[1] + 1,
               mix("metal_lit", "white", 0.2))
    emit("drawers", s, "furniture", sort=21, note="desk drawer unit")


# ---------------------------------------------------------------- chair -----
CHAIR = dict(gx=3.1, gy=2.1)


def chair():
    """Ergonomic gaming desk chair facing the desk.
    
    Both chair-back and chair-front are sorted behind the character (sort 26 and 28),
    so the character sits naturally ON the seat, never covered or sliced by the chair.
    When the character stands up, the chair remains intact and clean at the desk.
    """
    s = canvas()
    gx, gy = CHAIR["gx"], CHAIR["gy"]
    
    # --- Chair backrest: positioned behind the seated developer, facing the desk
    # Rear ergonomic shell visible from the isometric perspective
    for dz, inset in [(0.65, 0.0), (1.15, 0.04)]:
        s.box(gx + 0.08 + inset, gy + 0.82, dz, 0.94 - inset * 2, 0.18, 0.52,
              top=mix("plastic_lit", "white", 0.08),
              left=mix("plastic", "ink", 0.30),
              right=mix("plastic_lit", "ink", 0.10),
              outline=mix("plastic_dark", "ink", 0.40))
    # Vertical cyber racing stripes on the rear shell
    for k in (0.33, 0.67):
        s.line([s.p(gx + 0.08 + 0.94 * k, gy + 0.98, 0.68),
                s.p(gx + 0.08 + 0.94 * k, gy + 0.98, 1.66)], P["orange"], w=2)
    # Headrest cushion at the top
    s.box_mat(gx + 0.22, gy + 0.80, 1.68, 0.66, 0.20, 0.24, "plastic_dark")
    emit("chair-back", s, "furniture", sort=26,
         note="chair backrest — draws behind the character")

    s = canvas()
    # 5-caster star base centered under the seat
    cx, cy = gx + 0.55, gy + 0.45
    base_z = 0.04
    for dx, dy in ((-0.45, -0.15), (0.45, -0.15), (-0.35, 0.40), (0.35, 0.40), (0.0, 0.48)):
        ex, ey = cx + dx, cy + dy
        s.line([s.p(cx, cy, base_z), s.p(ex, ey, base_z)],
               mix("metal_dark", "white", 0.10), w=3)
        f = s.p(ex, ey, base_z)
        s.d.ellipse([f[0] - 3, f[1] - 2, f[0] + 3, f[1] + 2],
                    fill=mix("plastic_dark", "ink", 0.20),
                    outline=mix("ink", "plastic_dark", 0.35))
    # Heavy-duty hydraulic cylinder
    s.box_mat(cx - 0.09, cy - 0.09, base_z, 0.18, 0.18, 0.44, "metal")
    # Padded seat pan facing the desk
    seat = s.box(gx + 0.04, gy + 0.08, 0.46, 1.02, 0.85, 0.18,
                 top=mix("plastic_lit", "ink", 0.05),
                 left=mix("plastic", "ink", 0.28),
                 right=mix("plastic", "ink", 0.08),
                 outline=mix("plastic_dark", "ink", 0.35))
    dither(s, [seat["t_n"], seat["t_e"], seat["t_s"], seat["t_w"]],
           "orange", density=4, alpha=40)
    # Streamlined armrests on left and right
    for ax in (gx - 0.04, gx + 0.98):
        s.box_mat(ax, gy + 0.22, 0.62, 0.14, 0.52, 0.08, "plastic_dark")
        s.box_mat(ax + 0.02, gy + 0.38, 0.50, 0.10, 0.10, 0.12, "metal_dark")
    emit("chair-front", s, "furniture", sort=28,
         note="chair seat, base and armrests — sorted behind character so boy sits cleanly on top")


# ------------------------------------------------------- project shelf ------
SHELF = dict(gx=1.9, gy=0.02, z=3.25, sx=4.8, slots=6)


def project_shelf():
    s = canvas()
    h = SHELF
    # floating shelf board + brackets
    for bx in (h["gx"] + 0.4, h["gx"] + h["sx"] - 0.6):
        s.box_mat(bx, h["gy"] + 0.05, h["z"] - 0.34, 0.16, 0.5, 0.34,
                  "metal_dark")
    b = s.box(h["gx"], h["gy"], h["z"], h["sx"], 0.75, 0.16,
              top=mix("wood", "white", 0.26),
              left=mix("wood", "ink", 0.44),
              right=mix("wood", "ink", 0.18),
              outline=mix("wood", "ink", 0.52))
    s.line([b["t_s"], b["t_w"]], mix("wood_edge", "white", 0.2))
    # LED strip under the shelf
    a0 = s.p(h["gx"] + 0.1, h["gy"] + 0.72, h["z"] - 0.02)
    a1 = s.p(h["gx"] + h["sx"] - 0.1, h["gy"] + 0.72, h["z"] - 0.02)
    s.line([a0, a1], P["cyan_dim"], w=2)
    emit("project-shelf", s, "furniture", sort=10, note="shelf board for projects")

    # second (upper) shelf for books / trophies
    s2 = canvas()
    for bx in (h["gx"] + 0.8, h["gx"] + h["sx"] - 1.0):
        s2.box_mat(bx, h["gy"] + 0.05, h["z"] + 1.26, 0.14, 0.42, 0.3,
                   "metal_dark")
    s2.box(h["gx"] + 0.35, h["gy"], h["z"] + 1.56, h["sx"] - 0.7, 0.62, 0.14,
           top=mix("wood", "white", 0.2),
           left=mix("wood", "ink", 0.46),
           right=mix("wood", "ink", 0.2),
           outline=mix("wood", "ink", 0.52))
    emit("upper-shelf", s2, "furniture", sort=9, note="upper decorative shelf")


# ------------------------------------------------------------ bookshelf -----
def bookshelf():
    s = canvas()
    gx, gy, w, d, h = 0.1, 5.6, 1.0, 2.9, 3.6
    s.box_mat(gx, gy, 0.0, w, d, h, "wood_dark", lift=0.0)
    # inner back
    s.box(gx + 0.1, gy + 0.08, 0.1, w - 0.2, d - 0.16, h - 0.2,
          top=mix("wood_dark", "ink", 0.3),
          left=mix("wood_dark", "ink", 0.52),
          right=mix("wood_dark", "ink", 0.3), top_only=True)
    shelves = [0.25, 1.05, 1.85, 2.65]
    for z in shelves:
        s.box(gx + 0.08, gy + 0.08, z, w - 0.16, d - 0.16, 0.08,
              top=mix("wood", "white", 0.1),
              left=mix("wood", "ink", 0.45),
              right=mix("wood", "ink", 0.2))
        # books standing on each shelf
        colors = ["cyan_dim", "magenta", "amber", "green_dim", "violet",
                  "blue_dim", "orange"]
        by = gy + 0.2
        i = 0
        while by < gy + d - 0.45:
            bw = 0.1 + (i % 3) * 0.035
            bh = 0.5 + ((i * 7) % 4) * 0.055
            c = colors[(i + int(z * 7)) % len(colors)]
            s.box_mat(gx + 0.18, by, z + 0.08, w - 0.42, bw, bh, c, lift=0.05)
            by += bw + 0.045
            i += 1
    emit("bookshelf", s, "furniture", sort=14, note="bookshelf with books")


# ------------------------------------------------------------- monitors -----
def monitor(name, gx, gy, z, w, h, sort, tilt=0, accent="cyan"):
    s = canvas()
    # stand
    s.box_mat(gx + w / 2 - 0.12, gy + 0.18, z, 0.24, 0.3, 0.34, "metal_dark")
    foot = s.box(gx + w / 2 - 0.5, gy + 0.05, z, 1.0, 0.62, 0.08,
                 top=mix("metal", "white", 0.1),
                 left=mix("metal", "ink", 0.4),
                 right=mix("metal", "ink", 0.18))
    # bezel slab
    zz = z + 0.34
    body = s.box(gx, gy + 0.22, zz, w, 0.14, h,
                 top=mix("plastic_lit", "ink", 0.08),
                 left=mix("plastic", "ink", 0.3),
                 right=mix("plastic", "ink", 0.1),
                 outline=mix("plastic_dark", "ink", 0.4))
    # screen surface = the left face (faces the camera) inset
    pad = 0.1
    a = s.p(gx + pad, gy + 0.22, zz + h - pad * 0.6)
    b = s.p(gx + w - pad, gy + 0.22, zz + h - pad * 0.6)
    c = s.p(gx + w - pad, gy + 0.22, zz + pad * 0.6)
    dd = s.p(gx + pad, gy + 0.22, zz + pad * 0.6)
    s.quad(a, b, c, dd, P["screen"], outline=mix("screen", "ink", 0.4))
    emit_quad(f"{name}-screen", [a, b, c, dd], sort=sort + 1)
    # accent glow bar at the bottom edge of the bezel
    s.line([s.p(gx + pad, gy + 0.2, zz + 0.04),
            s.p(gx + w - pad, gy + 0.2, zz + 0.04)], P[accent], w=2)
    emit(name, s, "computer", sort=sort,
         note="monitor frame; its screen is a separate live layer")
    return [a, b, c, dd]


def monitors():
    monitor("monitor-main", DESK["gx"] + 1.35, DESK["gy"] + 0.3, DESK["h"] + 0.02,
            2.3, 1.35, sort=24, accent="cyan")
    monitor("monitor-side", DESK["gx"] + 3.75, DESK["gy"] + 0.34, DESK["h"] + 0.02,
            1.5, 1.0, sort=24, accent="magenta")


# ------------------------------------------------------------- pc tower -----
def tower():
    """PC tower tucked under the desk, so the desk slab draws over it."""
    s = canvas()
    gx, gy, h = DESK["gx"] + 0.45, DESK["gy"] + 0.3, 0.9
    s.box_mat(gx, gy, 0.0, 0.62, 1.0, h, "plastic", lift=0.02)
    # glass side panel (the +y face, toward the camera)
    a = s.p(gx + 0.06, gy + 1.0, h - 0.08)
    b = s.p(gx + 0.56, gy + 1.0, h - 0.08)
    c = s.p(gx + 0.56, gy + 1.0, 0.1)
    d = s.p(gx + 0.06, gy + 1.0, 0.1)
    s.quad(a, b, c, d, mix("screen", "blue_dim", 0.3),
           outline=mix("metal_dark", "ink", 0.2))
    # internals: GPU bar + two RGB fan rings
    s.quad(s.p(gx + 0.1, gy + 0.99, 0.52), s.p(gx + 0.52, gy + 0.99, 0.52),
           s.p(gx + 0.52, gy + 0.99, 0.42), s.p(gx + 0.1, gy + 0.99, 0.42),
           mix("metal_dark", "white", 0.06))
    for k, col in ((0.22, "cyan"), (0.68, "magenta")):
        f = s.p(gx + 0.31, gy + 0.98, 0.1 + k * (h - 0.2))
        s.d.ellipse([f[0] - 7, f[1] - 6, f[0] + 7, f[1] + 6],
                    outline=P[col], width=2)
    emit("pc-tower", s, "computer", sort=19,
         note="desktop tower under the desk")


# ------------------------------------------------- keyboard / mouse / pad ---
def peripherals():
    s = canvas()
    kx, ky = DESK["gx"] + 1.5, DESK["gy"] + 1.0
    # mouse pad
    pad = s.box(kx - 0.3, ky - 0.1, DESK["h"] + 0.02, 3.1, 0.95, 0.02,
                top=mix("plastic_dark", "violet", 0.12),
                left=mix("plastic_dark", "ink", 0.2),
                right=mix("plastic_dark", "ink", 0.1))
    dither(s, [pad["t_n"], pad["t_e"], pad["t_s"], pad["t_w"]],
           "violet", density=3, alpha=30)
    # keyboard body
    kb = s.box(kx, ky, DESK["h"] + 0.04, 2.0, 0.72, 0.1,
               top=mix("plastic_lit", "ink", 0.12),
               left=mix("plastic", "ink", 0.32),
               right=mix("plastic", "ink", 0.12),
               outline=mix("plastic_dark", "ink", 0.4))
    # keycaps grid, per-key RGB tint
    keys = ["cyan", "blue", "violet", "magenta", "amber"]
    for r in range(4):
        for c in range(13):
            gxx = kx + 0.1 + c * 0.142
            gyy = ky + 0.1 + r * 0.13
            col = mix(keys[(c + r) % len(keys)], "plastic_dark", 0.55)
            s.box(gxx, gyy, DESK["h"] + 0.14, 0.11, 0.1, 0.03,
                  top=col, left=mix(col, "ink", 0.3), right=mix(col, "ink", 0.15))
    emit("keyboard", s, "computer", sort=26, note="RGB keyboard and desk pad")

    m = canvas()
    mx, my = kx + 2.25, ky + 0.2
    m.box_mat(mx, my, DESK["h"] + 0.04, 0.3, 0.42, 0.1, "plastic", lift=0.1)
    m.box_mat(mx + 0.04, my + 0.06, DESK["h"] + 0.13, 0.22, 0.3, 0.04,
              "plastic_lit", lift=0.1)
    mp = m.p(mx + 0.15, my + 0.2, DESK["h"] + 0.18)
    m.px(mp[0], mp[1], P["cyan"])
    emit("mouse", m, "computer", sort=26, note="mouse")


# -------------------------------------------------------------- laptop ------
LAPTOP = dict(gx=DESK["gx"] + 4.25, gy=DESK["gy"] + 0.55)


def laptop():
    s = canvas()
    gx, gy = LAPTOP["gx"], LAPTOP["gy"]
    z = DESK["h"] + 0.02
    # base
    base = s.box(gx, gy, z, 1.1, 0.78, 0.07,
                 top=mix("metal", "white", 0.12),
                 left=mix("metal", "ink", 0.38),
                 right=mix("metal", "ink", 0.14),
                 outline=mix("metal_dark", "ink", 0.35))
    # keyboard deck
    s.box(gx + 0.08, gy + 0.08, z + 0.07, 0.94, 0.62, 0.01,
          top=mix("plastic_dark", "ink", 0.08),
          left=mix("plastic_dark", "ink", 0.3),
          right=mix("plastic_dark", "ink", 0.15))
    # lid, standing up on the far edge
    lid = s.box(gx, gy - 0.04, z + 0.07, 1.1, 0.08, 0.78,
                top=mix("metal", "white", 0.08),
                left=mix("metal", "ink", 0.42),
                right=mix("metal", "ink", 0.18),
                outline=mix("metal_dark", "ink", 0.4))
    pad = 0.08
    a = s.p(gx + pad, gy + 0.04, z + 0.78)
    b = s.p(gx + 1.1 - pad, gy + 0.04, z + 0.78)
    c = s.p(gx + 1.1 - pad, gy + 0.04, z + 0.14)
    d = s.p(gx + pad, gy + 0.04, z + 0.14)
    s.quad(a, b, c, d, P["screen"], outline=mix("screen", "ink", 0.4))
    emit_quad("laptop-screen", [a, b, c, d], sort=26)
    emit("laptop", s, "computer", sort=25,
         hotspot="contact", note="laptop — contact & resume hotspot")


# -------------------------------------------------------------- window ------
def window():
    s = canvas()
    gx, z, w, h = 7.0, 3.0, 3.4, 2.8
    # recess / frame on the gy=0 wall
    fr = s.box(gx - 0.18, 0.0, z - 0.18, w + 0.36, 0.1, h + 0.36,
               top=mix("wood_dark", "white", 0.1),
               left=mix("wood_dark", "ink", 0.3),
               right=mix("wood_dark", "ink", 0.1),
               outline=mix("wood_dark", "ink", 0.5))
    # the glass opening — left transparent here; the city view layer fills it
    a = s.p(gx, 0.02, z + h)
    b = s.p(gx + w, 0.02, z + h)
    c = s.p(gx + w, 0.02, z)
    d = s.p(gx, 0.02, z)
    emit_quad("window-glass", [a, b, c, d], sort=3, kind="window")
    emit("window-frame", s, "room", sort=2, note="window frame on the back wall")
    return [a, b, c, d]

    # mullions drawn as a separate layer ON TOP of the city view
    m = canvas()
    for k in (1 / 2,):
        m.line([m.p(gx + w * k, 0.01, z), m.p(gx + w * k, 0.01, z + h)],
               mix("wood_dark", "white", 0.06), w=3)
    m.line([m.p(gx, 0.01, z + h * 0.52), m.p(gx + w, 0.01, z + h * 0.52)],
           mix("wood_dark", "white", 0.06), w=3)
    # sill
    m.box(gx - 0.22, 0.0, z - 0.3, w + 0.44, 0.42, 0.12,
          top=mix("wood", "white", 0.2),
          left=mix("wood", "ink", 0.42),
          right=mix("wood", "ink", 0.18),
          outline=mix("wood", "ink", 0.5))
    emit("window-mullions", m, "room", sort=6,
         note="window bars + sill, drawn over the city view")


def _path(folder, name):
    import os
    d = os.path.join(os.path.dirname(__file__), "..", "public", "assets", folder)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, name)


# ------------------------------------------------------- daytime sunny city -
def city(quad=None):
    from isolib import Sheet, radial_glow, mix
    import random
    rnd = random.Random(42)
    if quad:
        w = int(max(p[0] for p in quad) - min(p[0] for p in quad))
        h = int(max(p[1] for p in quad) - min(p[1] for p in quad))
    else:
        w, h = 240, 190
    s = Sheet(w, h, 0, 0)
    for y in range(h):
        t = y / h
        sky_col = (int(58 + 42 * t), int(135 + 55 * t), int(235 + 18 * (1 - t)))
        s.line([(0, y), (w, y)], sky_col)
    s.img.alpha_composite(radial_glow(90, 90, "amber", 0.45, 1.8), (140, 4))
    for cx, cy, cr in [(35, 26, 16), (58, 22, 20), (80, 26, 15), (160, 40, 18), (185, 36, 22)]:
        s.d.ellipse([cx - cr, cy - int(cr * 0.55), cx + cr, cy + int(cr * 0.55)], fill=(255, 255, 255, 170))
    bands = [(0.42, 0.38, 26, 56), (0.64, 0.58, 20, 78), (0.88, 0.82, 14, 105)]
    for depth, ytop, step, maxh in bands:
        x = -6
        while x < w + 6:
            bw = step + rnd.randint(-4, 8)
            bh = rnd.randint(int(maxh * 0.45), maxh)
            y0 = int(h * ytop) - bh
            b_col = (int(70 + 45 * depth), int(95 + 50 * depth), int(140 + 60 * depth))
            s.rect(x, y0, x + bw, h, b_col)
            s.line([(x, y0), (x + bw, y0)], (220, 235, 255))
            for wy in range(y0 + 5, h - 4, 7):
                for wx in range(x + 3, x + bw - 2, 5):
                    if rnd.random() < 0.65:
                        s.rect(wx, wy, wx + 2, wy + 3, (180, 225, 255, 200))
            x += bw + rnd.randint(2, 6)
    if quad:
        from PIL import Image, ImageDraw
        x0 = int(min(p[0] for p in quad))
        y0 = int(min(p[1] for p in quad))
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).polygon([(p[0] - x0, p[1] - y0) for p in quad], fill=255)
        s.img.putalpha(mask)
        from stage import LAYOUT
        s.img.save(_path("room", "city-night.png"))
        LAYOUT["sprites"]["city-night"] = {
            "src": "assets/room/city-night.png", "x": x0, "y": y0,
            "w": w, "h": h, "sort": 3,
            "note": "sunny daytime city seen through the window",
        }
    else:
        s.img.save(_path("room", "city-night.png"))
    print("city-daytime", s.img.size)

def rain_frames(quad=None):
    pass



# ------------------------------------------------------- side cabinet -------
CAB = dict(gx=7.9, gy=0.35, sx=2.0, sy=1.5, h=1.5)


def cabinet():
    s = canvas()
    c = CAB
    s.box_mat(c["gx"], c["gy"], 0.0, c["sx"], c["sy"], c["h"], "wood_dark",
              lift=0.04)
    for i in range(2):
        s.box(c["gx"] + 0.06, c["gy"] + c["sy"] - 0.04, 0.12 + i * 0.68,
              c["sx"] - 0.12, 0.04, 0.6,
              top=mix("wood", "ink", 0.2),
              left=mix("wood", "ink", 0.3),
              right=mix("wood", "ink", 0.15),
              outline=mix("wood", "ink", 0.5))
    emit("cabinet", s, "furniture", sort=18, note="side cabinet for the coffee corner")


# ---------------------------------------------------- coffee machine --------
def coffee_machine():
    s = canvas()
    gx, gy = CAB["gx"] + 0.3, CAB["gy"] + 0.3
    z = CAB["h"]
    s.box_mat(gx, gy, z, 0.8, 0.75, 0.95, "metal_dark", lift=0.06)
    # drip area recess
    s.box(gx + 0.12, gy + 0.1, z + 0.05, 0.56, 0.6, 0.3,
          top=mix("ink", "metal_dark", 0.4),
          left=mix("ink", "metal_dark", 0.2),
          right=mix("ink", "metal_dark", 0.3))
    # spout
    s.box_mat(gx + 0.3, gy + 0.3, z + 0.52, 0.18, 0.18, 0.1, "metal")
    # display + button
    p0 = s.p(gx + 0.1, gy + 0.72, z + 0.82)
    s.rect(p0[0] - 1, p0[1] - 5, p0[0] + 14, p0[1] - 1, P["screen_lit"])
    s.px(p0[0] + 18, p0[1] - 3, P["amber"])
    emit("coffee-machine", s, "furniture", sort=19, note="coffee machine")


# ------------------------------------------------------------ mugs ----------
def mug(name, gx, gy, z, sort, color="cyan"):
    s = canvas()
    s.box_mat(gx, gy, z, 0.26, 0.26, 0.3, "white", lift=0.0)
    top = s.box(gx + 0.02, gy + 0.02, z + 0.3, 0.22, 0.22, 0.01,
                top=mix("ink", color, 0.25), left="#000", right="#000",
                top_only=True)
    # handle
    h0 = s.p(gx + 0.26, gy + 0.13, z + 0.22)
    s.d.arc([h0[0] - 2, h0[1] - 6, h0[0] + 5, h0[1] + 3], 300, 70,
            fill=mix("white", "ink", 0.15), width=2)
    emit(name, s, "furniture", sort=sort, note="coffee mug")


# ----------------------------------------------------------- plants ---------
def plant(name, gx, gy, z, scale, sort, pot="orange"):
    s = canvas()
    import random
    rnd = random.Random(hash(name) % 9999)
    pw = 0.44 * scale
    s.box_mat(gx, gy, z, pw, pw, 0.34 * scale, pot, lift=0.08)
    s.box(gx + 0.03, gy + 0.03, z + 0.3 * scale, pw - 0.06, pw - 0.06, 0.04,
          top=mix("wood_dark", "ink", 0.3), left="#000", right="#000",
          top_only=True)
    cx, cy = gx + pw / 2, gy + pw / 2
    base_z = z + 0.34 * scale
    for i in range(13):
        t = i / 13 * math.tau + rnd.random()
        ln = (0.5 + rnd.random() * 0.75) * scale
        tipz = base_z + ln
        ex = cx + math.cos(t) * 0.32 * scale * (0.5 + rnd.random())
        ey = cy + math.sin(t) * 0.32 * scale * (0.5 + rnd.random())
        col = mix("leaf" if i % 2 else "leaf_dark", "cyan", 0.08 * rnd.random())
        s.line([s.p(cx, cy, base_z), s.p(ex, ey, tipz)], col, w=2)
        tip = s.p(ex, ey, tipz)
        s.d.ellipse([tip[0] - 3, tip[1] - 3, tip[0] + 3, tip[1] + 3],
                    fill=mix(col, "white", 0.12))
    emit(name, s, "furniture", sort=sort, note="potted plant")


# --------------------------------------------------------------- bed -------
BED = dict(gx=7.3, gy=5.7, sx=1.9, sy=4.1)  # single-bed footprint


def bed():
    s = canvas()
    b = BED
    # frame
    s.box_mat(b["gx"], b["gy"], 0.0, b["sx"], b["sy"], 0.46, "wood_dark",
              lift=0.02)
    # headboard at the far (-y) end
    s.box_mat(b["gx"], b["gy"] - 0.22, 0.0, b["sx"], 0.22, 1.5, "wood",
              lift=0.06)
    # mattress
    s.box(b["gx"] + 0.06, b["gy"] + 0.04, 0.46, b["sx"] - 0.12, b["sy"] - 0.1,
          0.3, top=mix("gray", "night", 0.45),
          left=mix("gray", "ink", 0.52), right=mix("gray", "ink", 0.35),
          outline=mix("night", "ink", 0.3))
    # duvet (covers the lower two thirds)
    duv = s.box(b["gx"] + 0.02, b["gy"] + 1.3, 0.72, b["sx"] - 0.04,
                b["sy"] - 1.36, 0.22,
                top=mix("violet", "night", 0.3),
                left=mix("violet", "ink", 0.5),
                right=mix("violet", "ink", 0.3),
                outline=mix("violet", "ink", 0.6))
    dither(s, [duv["t_n"], duv["t_e"], duv["t_s"], duv["t_w"]],
           "cyan", density=4, alpha=26)
    # a single pillow, centred
    px = b["gx"] + (b["sx"] - 1.26) / 2
    pl = s.box(px, b["gy"] + 0.25, 0.76, 1.26, 0.72, 0.18,
               top=mix("white", "night", 0.22),
               left=mix("white", "ink", 0.52),
               right=mix("white", "ink", 0.36),
               outline=mix("night", "ink", 0.35))
    dither(s, [pl["t_n"], pl["t_e"], pl["t_s"], pl["t_w"]],
           "blue", density=3, alpha=30)
    emit("bed", s, "furniture", sort=28, note="single bed with duvet and one pillow")


# ------------------------------------------------------- floor clutter ------
def floor_props():
    s = canvas()
    # stack of books next to the bookshelf
    for i in range(4):
        c = ["magenta", "cyan_dim", "amber", "green_dim"][i]
        s.box_mat(1.35 + i * 0.03, 8.3 + i * 0.04, i * 0.13, 0.95, 0.72, 0.13,
                  c, lift=0.08)
    # a backpack leaning on the bookshelf
    s.box_mat(1.25, 6.2, 0.0, 0.8, 0.95, 1.0, "blue_dim", lift=0.04)
    s.box_mat(1.3, 6.35, 0.3, 0.7, 0.3, 0.4, "blue", lift=0.1)
    s.line([s.p(1.3, 6.3, 1.0), s.p(1.75, 6.5, 1.25)],
           mix("plastic_dark", "ink", 0.1), w=3)
    emit("floor-props", s, "furniture", sort=33,
         note="book stack and backpack on the floor")


# ----------------------------------------------------------- posters --------
def poster(name, gx, z, w, h, kind, sort):
    """Wall poster on the gy=0 wall."""
    s = canvas()
    fr = mix("wood_dark", "ink", 0.2)
    s.quad(s.p(gx - 0.06, 0.02, z + h + 0.06), s.p(gx + w + 0.06, 0.02, z + h + 0.06),
           s.p(gx + w + 0.06, 0.02, z - 0.06), s.p(gx - 0.06, 0.02, z - 0.06), fr)
    a = s.p(gx, 0.01, z + h)
    b = s.p(gx + w, 0.01, z + h)
    c = s.p(gx + w, 0.01, z)
    d = s.p(gx, 0.01, z)
    if kind == "grid":
        s.quad(a, b, c, d, mix("night", "violet", 0.22))
        for k in range(1, 7):
            t = k / 7
            s.line([(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t),
                    (d[0] + (c[0] - d[0]) * t, d[1] + (c[1] - d[1]) * t)],
                   mix("violet", "cyan", 0.4))
        # a neon sun arc
        mid = ((a[0] + c[0]) // 2, (a[1] + c[1]) // 2)
        s.d.arc([mid[0] - 16, mid[1] - 14, mid[0] + 16, mid[1] + 10], 180, 360,
                fill=P["magenta"], width=2)
    elif kind == "code":
        s.quad(a, b, c, d, mix("screen", "blue_dim", 0.18))
        for r in range(9):
            t = (r + 1) / 11
            y0 = a[1] + (d[1] - a[1]) * t
            y1 = b[1] + (c[1] - b[1]) * t
            ln = 0.28 + ((r * 37) % 60) / 100
            s.line([(a[0] + 4, y0), (a[0] + 4 + (b[0] - a[0] - 8) * ln,
                                     y0 + (y1 - y0) * ln)],
                   mix("cyan" if r % 3 else "magenta", "screen", 0.25))
    else:  # chart / blueprint
        s.quad(a, b, c, d, mix("night", "cyan", 0.1))
        pts = []
        for k in range(9):
            t = k / 8
            x = a[0] + (b[0] - a[0]) * t
            y = a[1] + (b[1] - a[1]) * t + 26 - 22 * math.sin(t * 3.1) ** 2
            pts.append((x, y))
        s.line(pts, P["amber"], w=2)
    emit(name, s, "room", sort=sort, note="wall poster")


# ------------------------------------------------------ left wall decor -----
def left_wall_decor():
    """Whiteboard + pin board + LED strip on the gx=0 wall."""
    s = canvas()

    def wall_quad(gy0, gy1, z0, z1, fill, outline=None):
        s.quad(s.p(0.01, gy0, z1), s.p(0.01, gy1, z1),
               s.p(0.01, gy1, z0), s.p(0.01, gy0, z0), fill, outline)

    # --- whiteboard with a flow diagram
    gy0, gy1, z0, z1 = 1.3, 4.1, 3.5, 5.6
    wall_quad(gy0 - 0.08, gy1 + 0.08, z0 - 0.08, z1 + 0.08,
              mix("metal_dark", "ink", 0.15))
    wall_quad(gy0, gy1, z0, z1, mix("gray_dark", "night", 0.52))
    nodes = [(1.75, 5.0), (2.6, 5.0), (2.6, 4.25), (3.45, 4.25), (1.75, 4.25)]
    for i, (ny, nz) in enumerate(nodes):
        a = s.p(0.0, ny - 0.3, nz + 0.22)
        b = s.p(0.0, ny + 0.3, nz + 0.22)
        c = s.p(0.0, ny + 0.3, nz - 0.22)
        d = s.p(0.0, ny - 0.3, nz - 0.22)
        col = ["cyan_dim", "magenta", "amber_dim", "green_dim", "blue_dim"][i]
        s.quad(a, b, c, d, mix(col, "white", 0.1), outline=mix(col, "ink", 0.4))
    # connectors
    for (ay, az), (by, bz) in [(nodes[0], nodes[1]), (nodes[1], nodes[2]),
                               (nodes[2], nodes[3]), (nodes[0], nodes[4])]:
        s.line([s.p(0.0, ay, az), s.p(0.0, by, bz)],
               mix("gray_dark", "ink", 0.2), w=2)
    # marker tray
    s.box(0.0, gy0 + 0.2, z0 - 0.26, 0.26, 1.2, 0.08,
          top=mix("metal", "white", 0.1), left=mix("metal", "ink", 0.4),
          right=mix("metal", "ink", 0.2))

    # --- cork pin board with notes
    gy0, gy1, z0, z1 = 4.7, 6.8, 3.9, 5.5
    wall_quad(gy0 - 0.09, gy1 + 0.09, z0 - 0.09, z1 + 0.09,
              mix("wood_dark", "ink", 0.1))
    wall_quad(gy0, gy1, z0, z1, mix("wood", "amber_dim", 0.3))
    notes = [(5.1, 5.1, "cyan"), (5.8, 5.15, "magenta"), (6.4, 5.0, "amber"),
             (5.3, 4.4, "green"), (6.1, 4.3, "violet")]
    for ny, nz, col in notes:
        a = s.p(0.0, ny - 0.26, nz + 0.26)
        b = s.p(0.0, ny + 0.26, nz + 0.26)
        c = s.p(0.0, ny + 0.26, nz - 0.26)
        d = s.p(0.0, ny - 0.26, nz - 0.26)
        s.quad(a, b, c, d, mix(col, "white", 0.42), outline=mix(col, "ink", 0.3))
        for k in range(3):
            t = 0.3 + k * 0.2
            s.line([(a[0] + 3, a[1] + (d[1] - a[1]) * t),
                    (b[0] - 3, b[1] + (c[1] - b[1]) * t)],
                   mix(col, "ink", 0.4))

    # --- LED strip running along the top of the left wall
    s.line([s.p(0.03, 0.4, 6.55), s.p(0.03, 8.4, 6.55)], P["violet"], w=2)
    for k in range(9):
        gy = 0.8 + k * 0.9
        pos = s.p(0.03, gy, 6.5)
        s.img.alpha_composite(
            radial_glow(58, 58, "violet" if k % 2 else "blue", 0.1, 2.6),
            (pos[0] - 29, pos[1] - 29))
    emit("wall-decor-left", s, "room", sort=5,
         note="whiteboard, pin board and LED strip on the left wall")


# ------------------------------------------------------------- lamps --------
def wall_lamp():
    s = canvas()
    gx, z = 0.05, 7.5
    s.box_mat(gx, 7.4, z, 0.1, 0.5, 0.12, "metal_dark")
    s.box_mat(gx + 0.02, 7.5, z - 0.3, 0.3, 0.3, 0.3, "metal")
    g = radial_glow(130, 130, "amber", 0.26, 2.2)
    pos = s.p(gx + 0.16, 7.65, z - 0.25)
    s.img.alpha_composite(g, (pos[0] - 65, pos[1] - 65))
    emit("wall-lamp", s, "effects", sort=8, note="wall lamp with baked glow")


def desk_lamp():
    s = canvas()
    gx, gy = DESK["gx"] + 0.15, DESK["gy"] + 0.3
    z = DESK["h"] + 0.02
    s.box_mat(gx, gy, z, 0.42, 0.42, 0.06, "metal_dark")
    s.line([s.p(gx + 0.2, gy + 0.2, z + 0.06), s.p(gx + 0.26, gy + 0.2, z + 1.1)],
           P["metal"], w=3)
    s.line([s.p(gx + 0.26, gy + 0.2, z + 1.1), s.p(gx + 0.9, gy + 0.3, z + 0.95)],
           P["metal"], w=3)
    head = s.p(gx + 0.95, gy + 0.32, z + 0.9)
    s.poly([off(head, -7, -5), off(head, 9, -8), off(head, 12, 4),
            off(head, -4, 6)], mix("metal", "white", 0.1),
           outline=mix("metal_dark", "ink", 0.3))
    s.img.alpha_composite(radial_glow(190, 190, "amber", 0.3, 2.2),
                          (head[0] - 90, head[1] - 70))
    emit("desk-lamp", s, "effects", sort=27, note="desk lamp with baked glow")


# -------------------------------------------------------- headphones --------
def headphones():
    s = canvas()
    gx, gy = DESK["gx"] + 0.35, DESK["gy"] + 1.15
    z = DESK["h"] + 0.04
    st = s.p(gx, gy, z)
    s.d.arc([st[0] - 13, st[1] - 20, st[0] + 13, st[1] + 2], 190, 350,
            fill=mix("plastic_lit", "white", 0.1), width=4)
    for dx in (-13, 11):
        s.d.ellipse([st[0] + dx - 4, st[1] - 7, st[0] + dx + 4, st[1] + 5],
                    fill=mix("plastic", "ink", 0.1),
                    outline=mix("plastic_dark", "ink", 0.3))
        s.d.ellipse([st[0] + dx - 2, st[1] - 4, st[0] + dx + 2, st[1] + 2],
                    fill=P["cyan_dim"])
    emit("headphones", s, "furniture", sort=26, note="headphones on the desk")


# --------------------------------------------- project objects on the shelf --
def shelf_slot(i):
    """Grid position of shelf slot i (0-based, left to right)."""
    span = SHELF["sx"] - 0.9
    gx = SHELF["gx"] + 0.45 + span * (i / max(1, SHELF["slots"] - 1))
    return gx, SHELF["gy"] + 0.26, SHELF["z"] + 0.16


def proj_store(s, gx, gy, z):
    """Tiny shop / marketplace kiosk — HamrahMadrese."""
    s.box_mat(gx, gy, z, 0.5, 0.42, 0.3, "wood", lift=0.1)
    s.box_mat(gx + 0.05, gy + 0.05, z + 0.3, 0.4, 0.32, 0.26, "amber", lift=0.12)
    # striped awning
    for k in range(5):
        t = k / 5
        a = s.p(gx + 0.5 * t, gy + 0.44, z + 0.56)
        b = s.p(gx + 0.5 * (t + 0.2), gy + 0.44, z + 0.56)
        c = s.p(gx + 0.5 * (t + 0.2), gy + 0.58, z + 0.46)
        d = s.p(gx + 0.5 * t, gy + 0.58, z + 0.46)
        s.quad(a, b, c, d, P["magenta"] if k % 2 else P["white"])
    s.box_mat(gx + 0.16, gy + 0.46, z + 0.3, 0.18, 0.06, 0.2, "cyan", lift=0.2)


def proj_phone(s, gx, gy, z):
    """Phone standing upright — Focus Leaf."""
    s.box_mat(gx + 0.1, gy + 0.08, z, 0.3, 0.2, 0.06, "metal_dark")
    s.box_mat(gx + 0.12, gy + 0.14, z + 0.06, 0.26, 0.06, 0.52, "plastic_dark")
    a = s.p(gx + 0.15, gy + 0.14, z + 0.54)
    b = s.p(gx + 0.35, gy + 0.14, z + 0.54)
    c = s.p(gx + 0.35, gy + 0.14, z + 0.1)
    d = s.p(gx + 0.15, gy + 0.14, z + 0.1)
    s.quad(a, b, c, d, mix("screen", "green_dim", 0.3))
    mid = ((a[0] + c[0]) // 2, (a[1] + c[1]) // 2)
    s.d.ellipse([mid[0] - 5, mid[1] - 5, mid[0] + 5, mid[1] + 5],
                outline=P["green"], width=2)


def proj_robot(s, gx, gy, z):
    """Small competition robot — FIRST Global."""
    s.box_mat(gx + 0.04, gy + 0.04, z, 0.48, 0.4, 0.22, "metal", lift=0.1)
    for wx in (gx + 0.02, gx + 0.44):
        for wy in (gy + 0.04, gy + 0.3):
            s.box_mat(wx, wy, z, 0.1, 0.12, 0.14, "plastic_dark")
    s.box_mat(gx + 0.12, gy + 0.12, z + 0.22, 0.3, 0.24, 0.22, "orange", lift=0.1)
    # arm
    s.line([s.p(gx + 0.42, gy + 0.2, z + 0.42), s.p(gx + 0.66, gy + 0.2, z + 0.62)],
           P["metal_lit"], w=3)
    eye = s.p(gx + 0.2, gy + 0.3, z + 0.4)
    s.px(eye[0], eye[1], P["cyan"])
    s.px(eye[0] + 4, eye[1], P["cyan"])


def proj_tower(s, gx, gy, z):
    """Sensor tower with a dish — PyroGuard."""
    s.box_mat(gx + 0.12, gy + 0.1, z, 0.28, 0.26, 0.08, "plastic_dark")
    for k in range(4):
        zz = z + 0.08 + k * 0.14
        w = 0.2 - k * 0.035
        s.box_mat(gx + 0.26 - w / 2, gy + 0.23 - w / 2, zz, w, w, 0.13,
                  "metal_dark", lift=0.06)
    top = s.p(gx + 0.26, gy + 0.23, z + 0.66)
    s.d.ellipse([top[0] - 7, top[1] - 5, top[0] + 7, top[1] + 5],
                fill=mix("metal_lit", "white", 0.1),
                outline=mix("metal_dark", "ink", 0.3))
    s.px(top[0], top[1] - 1, P["orange"])
    for r in (10, 15):
        s.d.arc([top[0] - r, top[1] - r - 3, top[0] + r, top[1] + r - 3],
                200, 340, fill=P["amber_dim"], width=1)


def proj_dashboard(s, gx, gy, z):
    """Chart panel on a stand — Simorgh."""
    s.box_mat(gx + 0.14, gy + 0.12, z, 0.24, 0.2, 0.08, "metal_dark")
    s.box_mat(gx + 0.08, gy + 0.18, z + 0.08, 0.38, 0.06, 0.42, "plastic_dark")
    a = s.p(gx + 0.1, gy + 0.18, z + 0.48)
    b = s.p(gx + 0.44, gy + 0.18, z + 0.48)
    c = s.p(gx + 0.44, gy + 0.18, z + 0.12)
    d = s.p(gx + 0.1, gy + 0.18, z + 0.12)
    s.quad(a, b, c, d, mix("screen", "green_dim", 0.2))
    for k in range(4):
        t = 0.15 + k * 0.22
        x = a[0] + (b[0] - a[0]) * t
        y = a[1] + (b[1] - a[1]) * t
        hh = 6 + (k * 5) % 14
        s.line([(x, y + 22), (x, y + 22 - hh)],
               P["green"] if k % 2 else P["cyan"], w=2)


def proj_apps(s, gx, gy, z):
    """A small stack of app cards — the extra Android apps."""
    for k in range(3):
        c = ["green_dim", "cyan_dim", "violet"][k]
        s.box_mat(gx + 0.08 + k * 0.03, gy + 0.08 + k * 0.05, z + k * 0.1,
                  0.34, 0.26, 0.1, c, lift=0.12)
    tp = s.p(gx + 0.25, gy + 0.2, z + 0.3)
    s.px(tp[0], tp[1], P["white"])


PROJECT_MODELS = {
    "store": proj_store, "phone": proj_phone, "robot": proj_robot,
    "tower": proj_tower, "dashboard": proj_dashboard, "apps": proj_apps,
}


def project_objects():
    """One sprite per shelf model, each its own interactive layer."""
    for i, (key, fn) in enumerate(PROJECT_MODELS.items()):
        gx, gy, z = shelf_slot(i)
        s = canvas()
        fn(s, gx, gy, z)
        emit(f"proj-{key}", s, "projects", sort=12 + i,
             hotspot="project", note=f"shelf model '{key}' (slot {i})")


# ------------------------------------------------- upper-shelf decoration ---
def trophies():
    s = canvas()
    # three medals / trophies for the three international awards
    for i, c in enumerate(["cyan_pale", "cyan_pale", "cyan_pale"]):
        gx = SHELF["gx"] + 0.9 + i * 0.55
        gy = SHELF["gy"] + 0.22
        z = SHELF["z"] + 1.7
        s.box_mat(gx, gy, z, 0.2, 0.18, 0.1, "wood_dark")
        cup = s.p(gx + 0.1, gy + 0.09, z + 0.1)
        s.d.polygon([(cup[0] - 5, cup[1] - 12), (cup[0] + 5, cup[1] - 12),
                     (cup[0] + 3, cup[1] - 2), (cup[0] - 3, cup[1] - 2)],
                    fill=mix(c, "gray", 0.25), outline=mix("gray_dark", "ink", 0.2))
        s.d.arc([cup[0] - 10, cup[1] - 12, cup[0] - 2, cup[1] - 4], 90, 270,
                fill=mix(c, "gray", 0.4), width=1)
        s.d.arc([cup[0] + 2, cup[1] - 12, cup[0] + 10, cup[1] - 4], 270, 90,
                fill=mix(c, "gray", 0.4), width=1)
    # a couple of leaning books
    for i in range(3):
        gx = SHELF["gx"] + 3.1 + i * 0.16
        s.box_mat(gx, SHELF["gy"] + 0.2, SHELF["z"] + 1.7, 0.42, 0.13, 0.5,
                  ["magenta", "amber", "blue_dim"][i], lift=0.06)
    emit("shelf-decor", s, "furniture", sort=11, note="trophies and books on the upper shelf")


# ------------------------------------------------------- RGB ambient rim ----
def rgb_lighting():
    """Cozy-cyberpunk RGB strip lighting along the floor/wall seams.

    Baked glow blobs (same technique as wall-lamp/desk-lamp) rather than
    runtime filters, so the effect costs nothing at render time. Colours
    alternate cyan / magenta / violet to read as an RGB LED strip without
    competing with the amber practical lights.
    """
    s = canvas()
    colors = ["cyan", "magenta", "violet"]
    # along the floor/back-right wall seam (gx=0 plane)
    for i, gy in enumerate([x * 0.9 for x in range(1, 10)]):
        pos = s.p(0.04, gy, 0.12)
        col = colors[i % len(colors)]
        s.img.alpha_composite(radial_glow(46, 30, col, 0.16, 2.6),
                              (pos[0] - 23, pos[1] - 15))
    # along the floor/back-left wall seam (gy=0 plane)
    for i, gx in enumerate([x * 0.9 for x in range(1, 10)]):
        pos = s.p(gx, 0.04, 0.12)
        col = colors[(i + 1) % len(colors)]
        s.img.alpha_composite(radial_glow(46, 30, col, 0.16, 2.6),
                              (pos[0] - 23, pos[1] - 15))
    # thin strip lines right at the seams for a crisper "LED strip" read
    s.line([s.p(0.02, 0.3, 0.08), s.p(0.02, 8.6, 0.08)], P["cyan"], w=1)
    s.line([s.p(0.3, 0.02, 0.08), s.p(8.6, 0.02, 0.08)], P["magenta"], w=1)
    # Roof / ceiling RGB light strip along the top wall trim (z=6.9)
    s.line([s.p(0.02, 0.3, 6.9), s.p(0.02, 9.2, 6.9)], P["cyan"], w=3)
    s.line([s.p(0.3, 0.02, 6.9), s.p(9.2, 0.02, 6.9)], P["magenta"], w=3)
    emit("rgb-strip", s, "effects", sort=7,
         note="baked RGB LED strip glow along the floor/wall seams")


def pet_bed():
    """Soft plush cat bed on the floor where the cat rests."""
    s = canvas()
    cx, cy = 4.7, 6.5
    pts = []
    for i in range(32):
        t = i / 32 * math.tau
        gx = cx + math.cos(t) * 0.82
        gy = cy + math.sin(t) * 0.82 * 0.95
        pts.append(s.p(gx, gy, 0.0))
    s.poly(pts, mix("violet", "ink", 0.3), outline=mix("violet", "ink", 0.5))
    inner = []
    for i in range(32):
        t = i / 32 * math.tau
        inner.append(s.p(cx + math.cos(t) * 0.58,
                         cy + math.sin(t) * 0.58 * 0.95, 0.06))
    s.poly(inner, mix("violet", "white", 0.35), outline=mix("violet", "ink", 0.3))
    emit("pet-bed", s, "furniture", sort=33, note="soft pet cushion on the floor for the cat")


# --------------------------------------------------------------- runner -----
def main():
    desk()
    drawers()
    chair()
    project_shelf()
    bookshelf()
    monitors()
    tower()
    peripherals()
    laptop()
    glass = window()
    city(glass)
    # rain_frames(glass) disabled for clear day
    cabinet()
    coffee_machine()
    mug("mug-desk", DESK["gx"] + 3.5, DESK["gy"] + 1.15, DESK["h"] + 0.04,
        sort=26, color="cyan")
    mug("mug-machine", CAB["gx"] + 1.1, CAB["gy"] + 0.45, CAB["h"], sort=20,
        color="amber")
    plant("plant-floor", 2.9, 9.4, 0.0, 1.5, sort=37, pot="green_dim")
    # Removed per user request: bed(), floor_props(), and the 3 wall posters
    # Replaced with a sleek pet cushion on the floor for the cat
    pet_bed()
    left_wall_decor()
    wall_lamp()
    desk_lamp()
    headphones()
    project_objects()
    trophies()
    rgb_lighting()
    p = write_layout()
    print("layout ->", p)


if __name__ == "__main__":
    main()
