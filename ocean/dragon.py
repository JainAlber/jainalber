"""The Dragon: a parametric eastern dragon that grows through 10 tiers,
from a pale sea-serpent hatchling to the Primordial Shenlong.

The body is a serpentine ribbon: a sine centerline swept with a width
profile that tapers head -> tail. Every tier unlocks anatomy.
"""

import math

from . import palette as P

# tier -> (length, waves, amplitude, head_width, body_color, accent)
TIER_GEO = {
    1:  (130, 1.1, 14,  4.0, "#b9c6cb", "#d7e2e5"),
    2:  (190, 1.4, 20,  5.5, "#9fb3ba", "#c4d4d8"),
    3:  (260, 1.6, 28,  7.5, "#5f7d85", "#14e0c8"),
    4:  (330, 1.8, 36, 10.0, "#46568f", "#6c7fd8"),
    5:  (410, 2.0, 44, 12.5, "#3a4d9e", "#14e0c8"),
    6:  (500, 2.2, 54, 15.0, "#32429c", "#2eff9e"),
    7:  (580, 2.4, 64, 17.5, "#2a3a8f", "#14e0c8"),
    8:  (650, 2.6, 74, 20.0, "#223078", "#00ff9c"),
    9:  (720, 2.9, 88, 23.0, "#1a2560", "#ffd166"),
    10: (780, 3.2, 98, 26.0, "#11142e", "#00ff9c"),
}


def _spine(length, waves, amp, n=64):
    """Centerline, head at +x end, with a gentle vertical drift."""
    pts = []
    for i in range(n):
        t = i / (n - 1)
        x = -length / 2 + length * t
        y = amp * math.sin(waves * math.tau * t) * (0.45 + 0.55 * t)
        pts.append((x, y))
    return pts


def _normals(pts):
    out = []
    for i, (x, y) in enumerate(pts):
        x0, y0 = pts[max(i - 1, 0)]
        x1, y1 = pts[min(i + 1, len(pts) - 1)]
        dx, dy = x1 - x0, y1 - y0
        d = math.hypot(dx, dy) or 1
        out.append((-dy / d, dx / d))
    return out


def _ribbon(pts, norms, w_head, taper=0.18):
    """Closed body outline: head end is widest, tail tapers to a point."""
    top, bot = [], []
    n = len(pts)
    for i, ((x, y), (nx, ny)) in enumerate(zip(pts, norms)):
        t = i / (n - 1)                      # 0 = tail, 1 = head
        w = w_head * (taper + (1 - taper) * t ** 0.7)
        top.append((x + nx * w, y + ny * w))
        bot.append((x - nx * w, y - ny * w))
    pts_all = top + bot[::-1]
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts_all) + " Z"
    return d


def _head(hx, hy, w, tier, body, accent):
    """Stylized eastern dragon head pointing +x."""
    g = ""
    snout = w * (2.6 if tier >= 6 else 2.0)
    # skull + snout wedge
    g += (f'<path d="M {hx - w:.1f},{hy - w:.1f} Q {hx + w:.1f},{hy - w * 1.5:.1f} {hx + snout:.1f},{hy - w * 0.3:.1f} '
          f'L {hx + snout * 1.08:.1f},{hy + w * 0.15:.1f} Q {hx + w:.1f},{hy + w * 1.3:.1f} {hx - w:.1f},{hy + w:.1f} Z" '
          f'fill="{body}"/>')
    if tier >= 5:  # open jaw
        g += (f'<path d="M {hx + w * 0.8:.1f},{hy + w * 0.5:.1f} Q {hx + snout * 0.9:.1f},{hy + w * 1.4:.1f} '
              f'{hx + snout * 1.15:.1f},{hy + w * 0.9:.1f}" stroke="{body}" stroke-width="{w * 0.55:.1f}" '
              f'fill="none" stroke-linecap="round"/>')
    # eye
    er = max(1.2, w * 0.28)
    eye_col = "#3a4750" if tier <= 2 else accent
    halo = f' filter="url(#glowS)"' if tier >= 3 else ""
    g += f'<circle cx="{hx + w * 0.7:.1f}" cy="{hy - w * 0.35:.1f}" r="{er:.1f}" fill="{eye_col}"{halo} class="pulse"/>'
    # horn nubs (t4) -> antlers (t6) -> crown (t9)
    if tier >= 4:
        hl = w * (0.9 if tier < 6 else 2.2 if tier < 9 else 3.2)
        for sign, dx in ((-1, -0.2), (1, 0.35)):
            bx, by = hx - w * 0.3 + w * dx, hy - w * 0.95
            if tier < 6:
                g += f'<path d="M {bx:.1f},{by:.1f} l {hl * 0.4:.1f},{-hl:.1f}" stroke="{body}" stroke-width="{w * 0.35:.1f}" stroke-linecap="round"/>'
            else:
                branch = (f'<path d="M {bx:.1f},{by:.1f} q {hl * 0.25:.1f},{-hl * 0.6:.1f} {hl * 0.15:.1f},{-hl:.1f} '
                          f'M {bx + hl * 0.1:.1f},{by - hl * 0.45:.1f} l {hl * 0.4:.1f},{-hl * 0.35:.1f}')
                if tier >= 9:
                    branch += f' M {bx + hl * 0.05:.1f},{by - hl * 0.75:.1f} l {-hl * 0.3:.1f},{-hl * 0.3:.1f}'
                g += branch + f'" stroke="{P.GOLD if tier >= 9 else body}" stroke-width="{w * 0.3:.1f}" fill="none" stroke-linecap="round"/>'
    # whiskers (t5 short, t6+ full flowing)
    if tier >= 5:
        wl = w * (3 if tier == 5 else 6)
        for sign in (-1, 1):
            g += (f'<path d="M {hx + snout * 0.95:.1f},{hy + sign * w * 0.2:.1f} '
                  f'q {wl * 0.6:.1f},{sign * wl * 0.25:.1f} {wl * 0.2:.1f},{sign * wl * 0.55:.1f} '
                  f'q {-wl * 0.3:.1f},{sign * wl * 0.3:.1f} {-wl * 0.55:.1f},{sign * wl * 0.22:.1f}" '
                  f'stroke="{accent}" stroke-width="1.4" fill="none" opacity="0.9" class="sway"/>')
    # pearl under chin (t8+)
    if tier >= 8:
        g += (f'<circle cx="{hx + w * 1.2:.1f}" cy="{hy + w * 2.2:.1f}" r="{w * 0.55:.1f}" '
              f'fill="{P.PEARL}" filter="url(#glowS)" class="pulse"/>')
    return g


def render_dragon(cx, cy, total_commits, tier) -> str:
    length, waves, amp, w, body, accent = TIER_GEO[tier]
    pts = _spine(length, waves, amp)
    norms = _normals(pts)
    hx, hy = pts[-1]

    g = f'<g transform="translate({cx:.0f},{cy:.0f})"><g class="dragonfloat">'

    # tier 10: the ocean bends around it
    if tier == 10:
        for i, rr in enumerate((amp * 2.6, amp * 3.4, amp * 4.4)):
            g += (f'<ellipse cx="0" cy="0" rx="{length * 0.62 + i * 30:.0f}" ry="{rr:.0f}" fill="none" '
                  f'stroke="{P.EMERALD}" stroke-width="0.8" opacity="{0.18 - i * 0.05:.2f}" class="pulse"/>')

    # ambient body glow (t3 soft -> t8 full)
    if tier >= 3:
        blur = "url(#blur6)" if tier >= 8 else "url(#blur4)"
        op = min(0.18 + tier * 0.05, 0.62)
        g += f'<path d="{_ribbon(pts, norms, w * 1.7)}" fill="{accent}" opacity="{op:.2f}" filter="{blur}" class="pulse"/>'

    # body ribbon
    g += f'<path d="{_ribbon(pts, norms, w)}" fill="{body}"/>'

    # scales: faint at t2, proper at t4+
    if tier >= 2:
        sc_op = 0.25 if tier < 4 else 0.5
        sc = ""
        step = 3 if tier >= 6 else 4
        for i in range(8, len(pts) - 4, step):
            x, y = pts[i]
            nx, ny = norms[i]
            t = i / (len(pts) - 1)
            sw = w * (0.18 + 0.82 * t ** 0.7) * 0.8
            sc += (f'M {x - nx * sw:.1f},{y - ny * sw:.1f} '
                   f'A {sw:.1f} {sw:.1f} 0 0 1 {x + nx * sw:.1f},{y + ny * sw:.1f} ')
        g += f'<path d="{sc}" stroke="{accent}" stroke-width="0.7" fill="none" opacity="{sc_op}"/>'

    # spine fins (t3) -> flowing fin mane (t7+)
    if tier >= 3:
        fins = ""
        step = 4 if tier < 7 else 3
        fl = w * (0.9 if tier < 7 else 1.8)
        for i in range(10, len(pts) - 6, step):
            x, y = pts[i]
            nx, ny = norms[i]
            t = i / (len(pts) - 1)
            ww = w * (0.18 + 0.82 * t ** 0.7)
            bx, by = x + nx * ww, y + ny * ww
            if tier < 7:
                fins += f'M {bx:.1f},{by:.1f} l {nx * fl - 3:.1f},{ny * fl:.1f} l {3:.1f},{2:.1f} Z '
            else:
                fins += (f'M {bx:.1f},{by:.1f} q {nx * fl - 6:.1f},{ny * fl - 4:.1f} '
                         f'{nx * fl * 1.3 - 10:.1f},{ny * fl * 1.3:.1f} ')
        style = (f'fill="{accent}" opacity="0.55"' if tier < 7
                 else f'fill="none" stroke="{accent}" stroke-width="1.6" opacity="0.75" class="sway"')
        g += f'<path d="{fins}" {style}/>'

    # glowing spine ridge dots (t7+)
    if tier >= 7:
        for i in range(8, len(pts) - 4, 5):
            x, y = pts[i]
            g += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.6" fill="{accent}" class="pulse" opacity="0.9"/>'

    # bioluminescent underbelly (t5+)
    if tier >= 5:
        belly = []
        for i, ((x, y), (nx, ny)) in enumerate(zip(pts, norms)):
            t = i / (len(pts) - 1)
            ww = w * (0.18 + 0.82 * t ** 0.7)
            belly.append((x - nx * ww * 0.85, y - ny * ww * 0.85))
        d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in belly[6:])
        g += f'<path d="{d}" stroke="{P.TEAL}" stroke-width="1.8" fill="none" opacity="0.65" class="pulse"/>'

    # limbs: claw fins at t5 (2), four true limbs t6+
    if tier >= 5:
        idxs = [int(len(pts) * 0.35), int(len(pts) * 0.72)]
        if tier >= 6:
            idxs += [int(len(pts) * 0.2), int(len(pts) * 0.55)]
        for k, i in enumerate(idxs):
            x, y = pts[i]
            nx, ny = norms[i]
            sign = 1 if k % 2 else -1
            ll = w * (1.1 if tier == 5 else 1.8)
            claw = "" if tier == 5 else (f'l {3:.0f},{sign * 4:.0f} m -3,{-sign * 4:.0f} '
                                         f'l {-2:.0f},{sign * 5:.0f} m 2,{-sign * 5:.0f} l {-5:.0f},{sign * 3:.0f}')
            g += (f'<path d="M {x:.1f},{y:.1f} q {-nx * ll * sign * 0.5 - 4:.1f},{ll * 0.8:.1f} '
                  f'{-nx * ll * sign - 2:.1f},{ll * 1.4:.1f} {claw}" stroke="{body}" '
                  f'stroke-width="{w * 0.4:.1f}" fill="none" stroke-linecap="round"/>')

    # gold accents along body for the Primordial (t10)
    if tier == 10:
        for i in range(12, len(pts) - 6, 9):
            x, y = pts[i]
            g += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.1" fill="{P.GOLD}" class="pulse" opacity="0.85"/>'

    g += _head(hx, hy, w, tier, body, accent)
    g += "</g></g>"
    return g
