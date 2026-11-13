"""Generate the room cat: idle, walk, sit, sleep, stretch, look.

The cat is drawn small (a real cat next to 2-metre furniture) and keeps the
same outline style and light direction as everything else. Walk frames are
drawn in place; cat.js moves the sprite along a path.
"""
import math
from isolib import P, mix
from stage import canvas, emit_anim

HOME = dict(gx=4.6, gy=6.4)      # the cat's rug spot
BODY = "cat"


def _cat_base(s, gx, gy, z, bl=0.52, bh=0.3, lift=0.0):
    """Rounded body block. Returns key pixel anchors for head/tail."""
    a = s.p(gx, gy, z + lift)
    b = s.p(gx + bl, gy + bl * 0.6, z + lift)
    x0, y0 = min(a[0], b[0]), min(a[1], b[1])
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    h = int(bh * 32)
    s.d.rounded_rectangle([x0 - 10, y0 - h, x1 + 4, y1 + 2], radius=7,
                          fill=P[BODY], outline=mix(BODY, "ink", 0.45))
    # lit back
    s.d.rounded_rectangle([x0 - 8, y0 - h + 2, x1 - 2, y0 - h // 3], radius=5,
                          fill=mix("cat_lit", BODY, 0.4))
    # two stripes
    for k in (0.35, 0.6):
        sx = int(x0 - 8 + (x1 - x0 + 10) * k)
        s.line([(sx, y0 - h + 2), (sx + 2, y0 - 1)], mix(BODY, "ink", 0.3))
    return dict(front=(x0 - 9, y0 - h // 2), back=(x1 + 3, y0 - h // 2),
                top=((x0 + x1) // 2, y0 - h), bottom=((x0 + x1) // 2, y1))


def _cat_head(s, cx, cy, turn=0.0, blink=False, up=0.0):
    tx = int(turn * 4)
    cy = int(cy - up * 4)
    s.d.rounded_rectangle([cx - 8 + tx, cy - 8, cx + 6 + tx, cy + 5], radius=5,
                          fill=mix(BODY, "white", 0.06),
                          outline=mix(BODY, "ink", 0.45))
    # ears
    for ex in (-7, 1):
        s.d.polygon([(cx + ex + tx, cy - 6), (cx + ex + 3 + tx, cy - 13),
                     (cx + ex + 6 + tx, cy - 5)],
                    fill=mix(BODY, "white", 0.02),
                    outline=mix(BODY, "ink", 0.4))
        s.d.polygon([(cx + ex + 2 + tx, cy - 7), (cx + ex + 3 + tx, cy - 11),
                     (cx + ex + 5 + tx, cy - 6)], fill=P["cat_dark"])
    # muzzle + eyes (only when facing the camera-ish)
    if turn > -0.5:
        s.d.ellipse([cx - 6 + tx, cy - 2, cx + 4 + tx, cy + 5],
                    fill=mix("cat_pale", BODY, 0.45))
        if not blink:
            s.px(cx - 4 + tx, cy - 1, P["amber"])
            s.px(cx + 2 + tx, cy - 1, P["amber"])
        else:
            s.line([(cx - 5 + tx, cy - 1), (cx - 3 + tx, cy - 1)],
                   mix(BODY, "ink", 0.3))
            s.line([(cx + 1 + tx, cy - 1), (cx + 3 + tx, cy - 1)],
                   mix(BODY, "ink", 0.3))
        s.px(cx - 1 + tx, cy + 2, P["magenta"])
    return (cx + tx, cy)


def _tail(s, bx, by, phase=0.0, curl=0.0):
    """Tail as a short chain of segments, swaying with phase."""
    x, y = bx, by + 2
    pts = [(x, y)]
    for i in range(4):
        t = (i + 1) / 4
        # curl=0 -> a low, lazy S behind the body; curl=1 -> wrapped around
        x += 3.4 - curl * 3.0 * t
        y += 1.2 - 3.4 * t * (1 - curl * 0.75) + math.sin(phase + i * 0.8) * 1.6
        pts.append((int(round(x)), int(round(y))))
    s.line(pts, mix(BODY, "ink", 0.2), w=4)
    s.line(pts[2:], mix(BODY, "ink", 0.3), w=3)
    s.d.ellipse([pts[-1][0] - 2, pts[-1][1] - 2, pts[-1][0] + 2, pts[-1][1] + 2],
                fill=mix("cat_pale", BODY, 0.45))


def _legs(s, anchor, swing=0.0, tuck=False):
    bx, by = anchor["bottom"]
    if tuck:
        s.d.ellipse([bx - 11, by - 3, bx + 5, by + 3],
                    fill=mix(BODY, "ink", 0.25))
        return
    for i, (dx, ph) in enumerate(((-9, 0.0), (-5, 0.5), (1, 0.25), (5, 0.75))):
        o = int(math.sin((swing + ph) * math.tau) * 2.5)
        s.line([(bx + dx, by - 4), (bx + dx + o, by + 4)],
               mix(BODY, "ink", 0.2 if i < 2 else 0.3), w=3)
        s.px(bx + dx + o, by + 4, mix("cat_pale", BODY, 0.5))


# ----------------------------------------------------------- states ---------
def anim_idle():
    """Standing idle: tail sways, occasional blink."""
    frames = []
    n = 12
    for i in range(n):
        s = canvas()
        t = i / n * math.tau
        a = _cat_base(s, HOME["gx"], HOME["gy"], 0.0, lift=0.004 * math.sin(t))
        _legs(s, a)
        _tail(s, *a["back"], phase=t)
        _cat_head(s, *a["front"], turn=0.15 * math.sin(t / 2),
                  blink=(i == 7))
        frames.append(s)
    emit_anim("cat-idle", frames, "cat", sort=35, fps=6, note="cat idle")


def anim_walk():
    frames = []
    n = 8
    for i in range(n):
        s = canvas()
        t = i / n
        a = _cat_base(s, HOME["gx"], HOME["gy"], 0.0,
                      lift=0.01 * abs(math.sin(t * math.tau)))
        _legs(s, a, swing=t)
        _tail(s, *a["back"], phase=t * math.tau * 2, curl=0.4)
        _cat_head(s, *a["front"], turn=0.3)
        frames.append(s)
    emit_anim("cat-walk", frames, "cat", sort=35, fps=9,
              note="cat walk cycle, in place")


def anim_sit():
    frames = []
    n = 10
    for i in range(n):
        s = canvas()
        t = i / n * math.tau
        a = _cat_base(s, HOME["gx"], HOME["gy"], 0.0, bl=0.4, bh=0.36)
        _legs(s, a, tuck=True)
        _tail(s, *a["back"], phase=t * 0.6, curl=1.0)
        _cat_head(s, a["front"][0], a["front"][1] - 5,
                  turn=0.2 * math.sin(t / 3), blink=(i == 6), up=0.4)
        frames.append(s)
    emit_anim("cat-sit", frames, "cat", sort=35, fps=5, note="cat sitting")


def anim_sleep():
    frames = []
    n = 10
    for i in range(n):
        s = canvas()
        t = i / n * math.tau
        a = _cat_base(s, HOME["gx"], HOME["gy"], 0.0, bl=0.6, bh=0.17,
                      lift=0.004 * math.sin(t))
        _legs(s, a, tuck=True)
        _tail(s, *a["back"], phase=t * 0.3, curl=1.6)
        hx, hy = a["front"]
        _cat_head(s, hx + 2, hy + 3, turn=-0.7, blink=True)
        # "z z z" above the head, drifting
        for k in range(3):
            zx = hx - 6 + k * 5
            zy = hy - 14 - k * 5 - int(2 * math.sin(t + k))
            sz = 2 + (2 - k)
            s.line([(zx, zy), (zx + sz, zy)], P["cyan_pale"])
            s.line([(zx + sz, zy), (zx, zy + sz)], P["cyan_pale"])
            s.line([(zx, zy + sz), (zx + sz, zy + sz)], P["cyan_pale"])
        frames.append(s)
    emit_anim("cat-sleep", frames, "cat", sort=35, fps=4, note="cat sleeping")


def anim_stretch():
    frames = []
    shape = [(0.40, 0.32), (0.46, 0.30), (0.58, 0.26), (0.70, 0.21),
             (0.76, 0.19), (0.70, 0.22), (0.56, 0.27), (0.44, 0.31)]
    for i, (bl, bh) in enumerate(shape):
        s = canvas()
        t = i / len(shape)
        a = _cat_base(s, HOME["gx"], HOME["gy"], 0.0, bl=bl, bh=bh)
        _legs(s, a, swing=t * 0.5)
        _tail(s, *a["back"], phase=t * math.tau, curl=-0.6)
        _cat_head(s, a["front"][0] - int(t * 3), a["front"][1],
                  turn=-0.2, blink=(2 <= i <= 4), up=0.2)
        frames.append(s)
    emit_anim("cat-stretch", frames, "cat", sort=35, fps=6, loop=False,
              note="cat stretching")


def anim_look():
    """Cat tracks the mouse pointer: 5 head directions, picked at runtime."""
    frames = []
    for turn in (-0.9, -0.45, 0.0, 0.45, 0.9):
        s = canvas()
        a = _cat_base(s, HOME["gx"], HOME["gy"], 0.0, bl=0.4, bh=0.36)
        _legs(s, a, tuck=True)
        _tail(s, *a["back"], phase=0.0, curl=1.0)
        _cat_head(s, a["front"][0], a["front"][1] - 5, turn=turn, up=0.5)
        frames.append(s)
    emit_anim("cat-look", frames, "cat", sort=35, fps=1, loop=False,
              note="5 head directions; frame chosen by pointer position")


def main():
    anim_idle()
    anim_walk()
    anim_sit()
    anim_sleep()
    anim_stretch()
    anim_look()
    print("cat anims done")


if __name__ == "__main__":
    main()
