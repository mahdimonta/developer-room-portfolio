"""Generate the anonymous developer character.

Seen from behind / rear three-quarter: the face is never drawn, so the
character stays anonymous while still reading as a person.
States: idle, typing, look-around, stand, walk, sit-down, coffee.
"""
import math
from isolib import P, mix, off
from stage import canvas, emit_anim

# the seat the character occupies (matches CHAIR in gen_props)
SEAT = dict(gx=3.1, gy=2.3)
SIT_Z = 0.70


def _head(s, gx, gy, z, lean=0.0, turn=0.0):
    """Back of the head: hair mass, nape, headphones. No face, ever."""
    c = s.p(gx + lean * 0.1, gy, z)
    tx = int(turn * 3)
    # nape of the neck (drawn first, mostly hidden by the hair)
    s.d.rectangle([c[0] - 4, c[1] + 4, c[0] + 4, c[1] + 12], fill=P["skin_dark"])
    # hair mass — a wide rounded block, pixel-art chunky
    s.d.rounded_rectangle([c[0] - 13 + tx, c[1] - 14, c[0] + 13 + tx, c[1] + 8],
                          radius=9, fill=P["hair"],
                          outline=mix("hair", "ink", 0.45))
    # lit crown, light from the upper left
    s.d.rounded_rectangle([c[0] - 10 + tx, c[1] - 12, c[0] + 5 + tx, c[1] - 1],
                          radius=6, fill=mix("hair_lit", "hair", 0.3))
    # hair tuft at the back of the crown
    s.d.polygon([(c[0] + 6 + tx, c[1] - 13), (c[0] + 13 + tx, c[1] - 17),
                 (c[0] + 11 + tx, c[1] - 8)], fill=mix("hair", "white", 0.1))
    # a sliver of ear only when the head is turned — still no face
    if abs(turn) > 0.45:
        ex = c[0] + tx + int(12 * (1 if turn > 0 else -1))
        s.d.ellipse([ex - 2, c[1] - 2, ex + 2, c[1] + 4], fill=P["skin"])
    # headphones over the hair
    s.d.arc([c[0] - 15 + tx, c[1] - 19, c[0] + 15 + tx, c[1] + 3], 185, 355,
            fill=mix("plastic_lit", "white", 0.15), width=3)
    for dx in (-15, 10):
        s.d.rounded_rectangle([c[0] + dx + tx, c[1] - 6,
                               c[0] + dx + 6 + tx, c[1] + 4],
                              radius=3, fill=mix("plastic", "ink", 0.05),
                              outline=mix("plastic_dark", "ink", 0.3))
        s.px(c[0] + dx + 3 + tx, c[1] - 1, P["cyan"])
    return c


def _torso(s, gx, gy, z, lean=0.0, w=0.86, h=0.66):
    """Hoodie seen from behind: broad shoulders, hood bunched at the nape."""
    px = s.p(gx + lean * 0.08, gy, z)
    top = s.p(gx + lean * 0.08, gy, z + h)
    hw = int(w * 19)          # half-width in px
    # body block
    s.d.polygon([(top[0] - hw + 2, top[1] + 2), (top[0] + hw - 2, top[1] + 2),
                 (px[0] + hw + 2, px[1]), (px[0] - hw - 2, px[1])],
                fill=P["hood"], outline=mix("hood_dark", "ink", 0.45))
    # left side catches the light
    s.d.polygon([(top[0] - hw + 3, top[1] + 3), (top[0] - 2, top[1] + 3),
                 (px[0] - 2, px[1] - 1), (px[0] - hw, px[1] - 1)],
                fill=mix("hood_lit", "hood", 0.45))
    # shoulder line
    s.line([(top[0] - hw + 2, top[1] + 3), (top[0] + hw - 2, top[1] + 3)],
           mix("hood_lit", "white", 0.1))
    # hood bunched behind the neck
    s.d.rounded_rectangle([top[0] - 13, top[1] - 3, top[0] + 13, top[1] + 11],
                          radius=6, fill=mix("hood_dark", "hood", 0.4),
                          outline=mix("hood_dark", "ink", 0.35))
    s.d.arc([top[0] - 11, top[1] - 1, top[0] + 11, top[1] + 13], 200, 340,
            fill=mix("hood_lit", "hood", 0.3), width=2)
    # drawstrings + a cyan back print
    s.line([(top[0] - 6, top[1] + 10), (top[0] - 5, top[1] + 19)], P["cyan_dim"])
    s.line([(top[0] + 6, top[1] + 10), (top[0] + 5, top[1] + 19)], P["cyan_dim"])
    mid = ((top[0] + px[0]) // 2, (top[1] + px[1]) // 2 + 4)
    s.d.rectangle([mid[0] - 6, mid[1] - 2, mid[0] + 6, mid[1] + 1],
                  fill=mix("cyan_dim", "hood", 0.4))
    return dict(top=top, bottom=px, hw=hw)


def _arm(s, sx, sy, sz, ex, ey, ez, sleeve="hood", lit=False):
    """Upper + fore arm as two chunky segments, with a visible hand."""
    mx, my, mz = (sx + ex) / 2, (sy + ey) / 2 - 0.1, (sz + ez) / 2 + 0.08
    base = mix(sleeve, "white", 0.12) if lit else mix(sleeve, "ink", 0.16)
    s.line([s.p(sx, sy, sz), s.p(mx, my, mz)], base, w=8)
    s.line([s.p(mx, my, mz), s.p(ex, ey, ez)], mix(base, "ink", 0.16), w=7)
    # cuff
    cf = s.p(ex, ey, ez)
    el = s.p(mx, my, mz)
    s.d.ellipse([el[0] - 4, el[1] - 4, el[0] + 4, el[1] + 4], fill=base)
    s.d.ellipse([cf[0] - 4, cf[1] - 4, cf[0] + 4, cf[1] + 4],
                fill=mix(sleeve, "ink", 0.3))
    # hand
    s.d.ellipse([cf[0] - 4, cf[1] - 1, cf[0] + 4, cf[1] + 6], fill=P["skin"],
                outline=mix("skin_dark", "ink", 0.3))
    s.d.ellipse([cf[0] - 3, cf[1], cf[0] + 1, cf[1] + 3],
                fill=mix("skin", "white", 0.15))


JEANS = (46, 54, 104)
JEANS_LIT = (62, 72, 132)
SHOE = (28, 32, 54)


def _shoe(s, gx, gy, z, lit=False):
    f = s.p(gx, gy, z)
    s.d.rounded_rectangle([f[0] - 7, f[1] - 4, f[0] + 7, f[1] + 5], radius=3,
                          fill=mix(SHOE, "white", 0.12 if lit else 0.0),
                          outline=mix(SHOE, "ink", 0.5))
    s.line([(f[0] - 6, f[1] + 4), (f[0] + 6, f[1] + 4)], P["cyan_dim"])


def _legs_sitting(s, gx, gy, z):
    """Thighs forward towards the desk, shins dropping to the floor under the desk."""
    for side, lit in ((-1, True), (1, False)):
        hx = gx + side * 0.18
        col = JEANS_LIT if lit else JEANS
        hip = s.p(hx, gy + 0.05, z)
        knee = s.p(hx, gy - 0.50, z - 0.08)
        foot = s.p(hx, gy - 0.52, z - 0.66)
        s.line([hip, knee], col, w=11)
        s.line([knee, foot], mix(col, "ink", 0.18), w=9)
        _shoe(s, hx, gy - 0.56, z - 0.70, lit)


def _legs_standing(s, gx, gy, z, stride=0.0):
    for side, lit in ((-1, True), (1, False)):
        hx = gx + side * 0.17
        fy = gy + stride * side * 0.45
        col = JEANS_LIT if lit else JEANS
        s.line([s.p(hx, gy, z), s.p(hx, fy, z - 0.55)], col, w=11)
        s.line([s.p(hx, fy, z - 0.55), s.p(hx, fy + 0.05, z - 1.05)],
               mix(col, "ink", 0.18), w=9)
        _shoe(s, hx, fy + 0.14, z - 1.08, lit)


# ------------------------------------------------------------ states --------
def frame_sitting(breath=0.0, hand_l=0.0, hand_r=0.0, turn=0.0, lean=0.0):
    """One seated frame. breath/hand/turn are small animation offsets."""
    s = canvas()
    gx, gy = SEAT["gx"] + 0.55, SEAT["gy"] + 0.55
    z = SIT_Z
    _legs_sitting(s, gx, gy, z)
    _torso(s, gx, gy, z + 0.04 + breath * 0.02, lean=lean)
    # arms reach forward and down to the keyboard
    for side, hoff, lit in ((-1, hand_l, True), (1, hand_r, False)):
        _arm(s, gx + side * 0.3, gy - 0.02, z + 0.56,
             gx + side * 0.26, gy - 0.86, z + 0.3 - hoff * 0.06, lit=lit)
    _head(s, gx, gy - 0.1, z + 1.22 + breath * 0.03, lean=lean, turn=turn)
    return s


def frame_standing(gx, gy, stride=0.0, bob=0.0, arm=0.0, turn=0.0, mug=False):
    s = canvas()
    z = 1.14 + bob * 0.03
    _legs_standing(s, gx, gy, z, stride)
    _torso(s, gx, gy, z, w=0.82, h=0.7)
    # swinging arms, opposite phase to the legs
    _arm(s, gx - 0.3, gy - 0.02, z + 0.6,
         gx - 0.34, gy + 0.26 - arm * 0.32, z + 0.04, lit=True)
    if mug:
        _arm(s, gx + 0.3, gy - 0.02, z + 0.6,
             gx + 0.34, gy - 0.4, z + 0.38)
        m = s.p(gx + 0.38, gy - 0.46, z + 0.42)
        s.d.rounded_rectangle([m[0] - 5, m[1] - 6, m[0] + 5, m[1] + 4],
                              radius=2, fill=mix("white", "night", 0.12),
                              outline=mix("gray_dark", "ink", 0.2))
        s.line([(m[0] - 4, m[1] - 5), (m[0] + 4, m[1] - 5)], P["amber_dim"])
    else:
        _arm(s, gx + 0.3, gy - 0.02, z + 0.6,
             gx + 0.34, gy + 0.26 + arm * 0.32, z + 0.04)
    _head(s, gx, gy - 0.06, z + 1.26 + bob * 0.02, turn=turn)
    return s


def anim_idle():
    """Seated idle: slow breathing, hands resting, occasional micro-lean."""
    frames = []
    n = 12
    for i in range(n):
        t = i / n * math.tau
        frames.append(frame_sitting(breath=math.sin(t),
                                    hand_l=0.1 * math.sin(t),
                                    hand_r=0.1 * math.sin(t + 0.6),
                                    lean=0.08 * math.sin(t / 2)))
    emit_anim("char-idle", frames, "character", sort=30, fps=7,
              note="seated idle, breathing")


def anim_typing():
    """Hands alternate fast; shoulders dip slightly on each stroke."""
    frames = []
    n = 8
    for i in range(n):
        t = i / n * math.tau
        frames.append(frame_sitting(breath=0.3 * math.sin(t * 2),
                                    hand_l=1.0 if i % 2 == 0 else 0.0,
                                    hand_r=0.0 if i % 2 == 0 else 1.0,
                                    lean=0.12))
    emit_anim("char-typing", frames, "character", sort=30, fps=11,
              note="seated typing")


def anim_look_around():
    """Head turns left, holds, returns, turns right, returns."""
    turns = [0, .35, .7, .9, .9, .7, .3, 0, -.35, -.75, -.9, -.6, -.2, 0]
    frames = [frame_sitting(breath=0.4, turn=t, lean=0.05 * t) for t in turns]
    emit_anim("char-look", frames, "character", sort=30, fps=6, loop=False,
              note="seated, looking around")


def anim_sit_down():
    """Stand -> sit transition, played forward to sit and reversed to stand."""
    frames = []
    steps = 7
    for i in range(steps):
        t = i / (steps - 1)
        gx = SEAT["gx"] + 0.55
        gy = SEAT["gy"] + 1.5 - t * 0.9
        s = canvas()
        z = 1.14 - t * 0.44
        if t < 0.8:
            _legs_standing(s, gx, gy, z, stride=0.14 * (1 - t))
        else:
            _legs_sitting(s, gx, gy, z)
        _torso(s, gx, gy, z, w=0.82 + t * 0.04, h=0.7 - t * 0.04)
        for side in (-1, 1):
            _arm(s, gx + side * 0.3, gy - 0.02, z + 0.58,
                 gx + side * 0.28, gy + 0.24 - t * 1.0, z + 0.06 + t * 0.26,
                 lit=(side < 0))
        _head(s, gx, gy - 0.08, z + 1.24, lean=t * 0.22)
        frames.append(s)
    emit_anim("char-sit", frames, "character", sort=30, fps=9, loop=False,
              note="sitting down (reverse for standing up)")


def anim_walk():
    """Walk cycle used for the coffee trip, between the desk and the cabinet."""
    frames = []
    n = 8
    for i in range(n):
        t = i / n * math.tau
        frames.append(frame_standing(SEAT["gx"] + 0.55, SEAT["gy"] + 1.2,
                                     stride=0.5 * math.sin(t),
                                     bob=abs(math.cos(t)),
                                     arm=math.sin(t)))
    emit_anim("char-walk", frames, "character", sort=30, fps=10,
              note="walk cycle, in place (moved by code)")


def anim_coffee():
    """Standing at the machine: reaches, waits, lifts the mug."""
    frames = []
    for i, (arm, mug) in enumerate([(0.0, False), (0.5, False), (0.9, False),
                                    (0.9, False), (0.5, True), (0.1, True),
                                    (0.0, True), (0.0, True)]):
        frames.append(frame_standing(SEAT["gx"] + 0.55, SEAT["gy"] + 1.2,
                                     arm=-arm, bob=0.2 * math.sin(i),
                                     turn=0.5, mug=mug))
    emit_anim("char-coffee", frames, "character", sort=30, fps=6, loop=False,
              note="making coffee at the machine")


def main():
    anim_idle()
    anim_typing()
    anim_look_around()
    anim_sit_down()
    anim_walk()
    anim_coffee()
    print("character anims done")


if __name__ == "__main__":
    main()
