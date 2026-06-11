"""Parametric sea creature renderers.

Every species is a body generator drawn in local coords: origin at the
creature's center, facing +x, body spanning roughly x in [-s, s].
Hybrids = base species body + the overlay parent's signature trait,
so all 36 combinations render without 36 hand-drawn artworks.

Stage (1-3) scales size, detail and bioluminescence.
"""

import math

from . import palette as P
from . import species as sp


def _path(pts, close=False) -> str:
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return d + (" Z" if close else "")


def _smooth(pts, close=False) -> str:
    """Catmull-Rom-ish smooth path through points using quadratic segments."""
    if len(pts) < 3:
        return _path(pts, close)
    d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(1, len(pts) - 1):
        mx = (pts[i][0] + pts[i + 1][0]) / 2
        my = (pts[i][1] + pts[i + 1][1]) / 2
        d += f" Q {pts[i][0]:.1f},{pts[i][1]:.1f} {mx:.1f},{my:.1f}"
    d += f" T {pts[-1][0]:.1f},{pts[-1][1]:.1f}"
    return d + (" Z" if close else "")


def _sine_spine(s: float, waves: float, amp: float, n: int = 24):
    """Points along a horizontal sine, head at +s, tail at -s."""
    return [(-s + 2 * s * t / (n - 1),
             amp * math.sin(waves * math.tau * t / (n - 1)))
            for t in range(n)]


# ---------------------------------------------------------------- bodies

def body_python(s, stage):
    """Sea Krait: banded serpent. Stage1 thin+pale, 3 muscular + venom shimmer."""
    w = (1.5, 3.2, 5.5)[stage - 1]
    spine = _sine_spine(s, 1.6, s * 0.22)
    body_col = ("#7d8a8f", "#1c2530", "#10161f")[stage - 1]
    band_col = (P.PALE, "#e8edf0", "#f4f8f9")[stage - 1]
    g = f'<path d="{_smooth(spine)}" fill="none" stroke="{body_col}" stroke-width="{w}" stroke-linecap="round"/>'
    if stage >= 2:  # vivid banding via dashed overlay
        g += (f'<path d="{_smooth(spine)}" fill="none" stroke="{band_col}" '
              f'stroke-width="{w * 0.92}" stroke-dasharray="{w * 1.3} {w * 1.7}" stroke-linecap="butt"/>')
    hx, hy = spine[-1]
    g += f'<circle cx="{hx + 2:.1f}" cy="{hy:.1f}" r="{w * 0.75:.1f}" fill="{body_col}"/>'
    eye = ("#3a4750", "#cfd8dc", "#ffe066")[stage - 1]
    g += f'<circle cx="{hx + 2.5:.1f}" cy="{hy - w * 0.25:.1f}" r="{max(0.8, w * 0.2):.1f}" fill="{eye}"/>'
    if stage >= 2:  # flickering tongue
        g += (f'<path d="M {hx + w * 0.8:.1f},{hy:.1f} l 5,-1.5 m -5,1.5 l 5,1.5" stroke="{P.BLOOD}" '
              f'stroke-width="0.8" fill="none" class="flicker"/>')
    if stage == 3:  # venom shimmer
        g += f'<circle cx="{hx + 4:.1f}" cy="{hy + 1:.1f}" r="6" fill="{P.EMERALD}" opacity="0.25" filter="url(#blur2)" class="pulse"/>'
    return g


def body_js(s, stage):
    """Yellowfin Tuna: silver torpedo, yellow fins, speed."""
    h = s * (0.28, 0.34, 0.4)[stage - 1]
    body = _smooth([(-s, 0), (-s * 0.55, -h * 0.7), (s * 0.25, -h), (s * 0.8, -h * 0.35),
                    (s, 0), (s * 0.8, h * 0.35), (s * 0.25, h), (-s * 0.55, h * 0.7)], close=True)
    g = f'<path d="{body}" fill="url(#tunaGrad)"/>'
    g += f'<path d="{_path([(-s, 0), (-s * 1.28, -h * 1.1), (-s * 1.12, 0), (-s * 1.28, h * 1.1)], close=True)}" fill="url(#tunaGrad)"/>'
    if stage >= 2:  # yellow fins + finlets
        g += f'<path d="{_path([(s * 0.1, -h), (s * 0.0, -h * 1.8), (-s * 0.25, -h * 0.85)], close=True)}" fill="{P.GOLD}"/>'
        g += f'<path d="{_path([(s * 0.05, h * 0.9), (-s * 0.1, h * 1.6), (-s * 0.3, h * 0.8)], close=True)}" fill="{P.GOLD}"/>'
        for i in range(4):
            x = -s * 0.35 - i * s * 0.13
            g += f'<path d="M {x:.1f},{-h * 0.62:.1f} l -4,-4 l -2,4 Z" fill="{P.GOLD}" opacity="0.9"/>'
    g += f'<circle cx="{s * 0.78:.1f}" cy="{-h * 0.18:.1f}" r="{max(1.2, h * 0.14):.1f}" fill="#0a0f14"/>'
    if stage == 3:  # motion blur
        for i, op in enumerate((0.5, 0.3, 0.15)):
            g += (f'<line x1="{-s * 1.4 - i * 14}" y1="{(i - 1) * h * 0.45:.1f}" x2="{-s * 2.4 - i * 18}" '
                  f'y2="{(i - 1) * h * 0.45:.1f}" stroke="{P.GOLD}" stroke-width="2" opacity="{op}" stroke-linecap="round"/>')
    return g


def body_ai(s, stage):
    """Manta Ray: gliding wings, neural circuit glow."""
    w = s * (0.8, 1.15, 1.5)[stage - 1]
    fill = ("#5a6b78", "#33408f", "#1d2666")[stage - 1]
    wing = _smooth([(-s * 0.55, 0), (-s * 0.1, -w * 0.55), (s * 0.45, -w),
                    (s * 0.5, -w * 0.2), (s * 0.7, 0),
                    (s * 0.5, w * 0.2), (s * 0.45, w), (-s * 0.1, w * 0.55)], close=True)
    g = f'<path d="{wing}" fill="{fill}" opacity="{0.75 if stage == 1 else 1}"/>'
    g += f'<path d="M {-s * 0.55:.1f},0 L {-s * 1.25:.1f},2" stroke="{fill}" stroke-width="2" fill="none"/>'
    g += (f'<path d="M {s * 0.62:.1f},-4 q 8,-5 12,-1 M {s * 0.62:.1f},4 q 8,5 12,1" '
          f'stroke="{fill}" stroke-width="2.4" fill="none"/>')  # cephalic fins
    if stage >= 2:
        g += trait_circuits(s * 0.9, strong=(stage == 3))
    return g


def body_devops(s, stage):
    """Mantis Shrimp: segmented armor, raptorial claws, rainbow at stage 3."""
    n = (4, 5, 6)[stage - 1]
    seg_w = s * 1.5 / n
    rainbow = ["#ff5d5d", "#ffb347", "#ffe066", "#2eff9e", "#14e0c8", "#4f5fd5"]
    g = ""
    for i in range(n):
        x = s * 0.6 - i * seg_w
        col = "#5d6d75" if stage == 1 else rainbow[i % 6] if stage == 3 else ("#7a8c94" if i % 2 else "#b06a4f")
        g += (f'<ellipse cx="{x:.1f}" cy="0" rx="{seg_w * 0.62:.1f}" ry="{s * 0.22:.1f}" '
              f'fill="{col}" opacity="{0.85 if stage < 3 else 1}"/>')
    g += f'<path d="{_path([(-s * 0.95, 0), (-s * 1.25, -s * 0.22), (-s * 1.25, s * 0.22)], close=True)}" fill="{"#5d6d75" if stage == 1 else P.TEAL_DIM}"/>'
    g += (f'<line x1="{s * 0.72:.1f}" y1="-3" x2="{s * 0.95:.1f}" y2="-8" stroke="#9fb3ba" stroke-width="1.5"/>'
          f'<circle cx="{s * 0.97:.1f}" cy="-9" r="2.4" fill="{P.EMERALD if stage == 3 else "#324a52"}"/>'
          f'<line x1="{s * 0.72:.1f}" y1="3" x2="{s * 0.95:.1f}" y2="8" stroke="#9fb3ba" stroke-width="1.5"/>'
          f'<circle cx="{s * 0.97:.1f}" cy="9" r="2.4" fill="{P.EMERALD if stage == 3 else "#324a52"}"/>')
    if stage >= 2:  # claws
        claw = "#ffb347" if stage == 3 else "#7a8c94"
        g += (f'<path d="M {s * 0.55:.1f},{s * 0.2:.1f} q 10,4 14,12 q 2,5 -3,6" stroke="{claw}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
              f'<path d="M {s * 0.45:.1f},{s * 0.24:.1f} q 8,6 10,13" stroke="{claw}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    if stage == 3:  # crackling energy
        g += (f'<path d="M {s * 0.72:.1f},{s * 0.55:.1f} l 4,-3 l -1,4 l 5,-2" stroke="{P.TEAL}" '
              f'stroke-width="1.2" fill="none" class="flicker"/>')
    return g


def body_frontend(s, stage):
    """Lionfish: flowing venomous fin rays, striped, glowing tips."""
    h = s * 0.42
    rays = (5, 9, 14)[stage - 1]
    spread = (0.5, 0.85, 1.25)[stage - 1]
    g = ""
    for i in range(rays):  # fin fan first (behind body)
        a = math.pi * (0.55 + spread * (i / max(rays - 1, 1) - 0.5))
        L = s * (1.0, 1.45, 2.0)[stage - 1] * (0.75 + 0.25 * math.sin(i * 2.1))
        tx, ty = -math.cos(a) * L, -math.sin(a) * L
        col = P.BLOOD if i % 2 else "#e8edf0"
        g += (f'<path d="M 0,0 Q {tx * 0.5:.1f},{ty * 0.5 - 6:.1f} {tx:.1f},{ty:.1f}" stroke="{col}" '
              f'stroke-width="{1.0 + stage * 0.4:.1f}" fill="none" opacity="0.85" class="sway"/>')
        if stage == 3:
            g += f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="2" fill="{P.EMERALD}" class="pulse" filter="url(#glowS)"/>'
    body = _smooth([(-s * 0.7, 0), (-s * 0.2, -h), (s * 0.55, -h * 0.55), (s * 0.75, 0),
                    (s * 0.55, h * 0.55), (-s * 0.2, h)], close=True)
    g += f'<path d="{body}" fill="#d8dde0"/>'
    for i in range(stage + 2):  # stripes
        x = s * 0.5 - i * s * 0.26
        g += f'<path d="M {x:.1f},{-h:.1f} q -6,{h:.1f} 0,{h * 2:.1f}" stroke="{P.BLOOD}" stroke-width="{3 + stage}" fill="none" opacity="0.9"/>'
    g += f'<circle cx="{s * 0.55:.1f}" cy="{-h * 0.2:.1f}" r="1.8" fill="#0a0f14"/>'
    return g


def body_cli(s, stage):
    """Moray Eel: lurker. Stage1 = eyes in shadow; 3 = black + green spots + second jaw."""
    if stage == 1:
        return (f'<ellipse cx="0" cy="0" rx="{s * 0.8:.1f}" ry="{s * 0.3:.1f}" fill="#05080d" opacity="0.85"/>'
                f'<circle cx="{s * 0.35:.1f}" cy="-2" r="1.6" fill="{P.EMERALD}" class="pulse"/>'
                f'<circle cx="{s * 0.5:.1f}" cy="-2" r="1.6" fill="{P.EMERALD}" class="pulse"/>')
    w = (0, 5.0, 8.5)[stage - 1]
    spine = _sine_spine(s, 1.3, s * 0.18)
    g = f'<path d="{_smooth(spine)}" fill="none" stroke="#0a0f12" stroke-width="{w}" stroke-linecap="round"/>'
    g += trait_spots(s, strong=(stage == 3))
    hx, hy = spine[-1]
    g += (f'<path d="M {hx:.1f},{hy:.1f} l 8,-2 m -8,2 l 7,3" stroke="#0a0f12" stroke-width="{w * 0.5:.1f}" stroke-linecap="round"/>'
          f'<circle cx="{hx + 1:.1f}" cy="{hy - w * 0.3:.1f}" r="1.7" fill="{P.EMERALD}"/>')
    if stage == 3:  # pharyngeal second jaw
        g += (f'<path d="M {hx + 3:.1f},{hy + 1:.1f} l 3,-1.5 l 1.5,2 l 2,-2" stroke="{P.PEARL}" '
              f'stroke-width="1.1" fill="none" opacity="0.9"/>')
    return g


def body_data(s, stage):
    """Anglerfish: nightmare jaw + blazing lure that lights the abyss."""
    r = s * (0.42, 0.55, 0.72)[stage - 1]
    lure_r = (1.8, 3.2, 5.5)[stage - 1]
    lure_x, lure_y = r * 0.9, -r * 1.6
    g = ""
    if stage == 3:  # lure illuminates surroundings
        g += f'<circle cx="{lure_x:.1f}" cy="{lure_y:.1f}" r="{r * 2.6:.1f}" fill="url(#lureHalo)" class="pulse"/>'
    g += f'<circle cx="0" cy="0" r="{r:.1f}" fill="#0d1117"/>'
    g += f'<path d="M {r * 0.2:.1f},{-r * 0.95:.1f} Q {r * 0.8:.1f},{lure_y:.1f} {lure_x:.1f},{lure_y:.1f}" stroke="#2a3540" stroke-width="1.4" fill="none"/>'
    g += f'<circle cx="{lure_x:.1f}" cy="{lure_y:.1f}" r="{lure_r:.1f}" fill="{P.TEAL}" filter="url(#glowS)" class="pulse"/>'
    if stage >= 2:  # teeth
        jaw_y = r * 0.25
        teeth = "".join(
            f'M {r * 0.85 - i * r * 0.3:.1f},{jaw_y:.1f} l -2.4,{4 + stage} l -2.4,{-4 - stage} '
            for i in range(stage + 2))
        g += f'<path d="{teeth}" stroke="{P.PEARL}" stroke-width="1.1" fill="none"/>'
        g += f'<path d="M {r * 0.95:.1f},{jaw_y:.1f} q {-r:.1f},{r * 0.9:.1f} {-r * 1.9:.1f},{r * 0.35:.1f}" stroke="#0d1117" stroke-width="3" fill="none"/>'
    g += f'<circle cx="{r * 0.45:.1f}" cy="{-r * 0.3:.1f}" r="{1.5 + stage * 0.5:.1f}" fill="{P.TEAL_DIM}" opacity="0.9"/>'
    g += f'<path d="{_path([(-r, 0), (-r * 1.6, -r * 0.5), (-r * 1.6, r * 0.5)], close=True)}" fill="#0d1117"/>'
    return g


def body_mobile(s, stage):
    """Flying Fish: wings grow until fully airborne."""
    h = s * 0.22
    body = _smooth([(-s * 0.8, 0), (-s * 0.3, -h), (s * 0.6, -h * 0.6), (s * 0.85, 0),
                    (s * 0.6, h * 0.6), (-s * 0.3, h)], close=True)
    g = f'<path d="{body}" fill="url(#flyGrad)"/>'
    g += f'<path d="{_path([(-s * 0.8, 0), (-s * 1.1, -h * 1.6), (-s * 0.95, 0), (-s * 1.05, h * 1.2)], close=True)}" fill="url(#flyGrad)"/>'
    wing = (0.5, 1.1, 1.9)[stage - 1]
    for sign in (-1, 1):
        g += (f'<path d="M {-s * 0.1:.1f},{sign * h * 0.4:.1f} Q {s * 0.2:.1f},{sign * s * wing * 0.7:.1f} '
              f'{s * 0.75:.1f},{sign * s * wing:.1f} Q {s * 0.05:.1f},{sign * s * wing * 0.75:.1f} {-s * 0.35:.1f},{sign * h * 0.4:.1f} Z" '
              f'fill="url(#iridGrad)" opacity="{0.5 + stage * 0.16:.2f}" class="sway"/>')
    g += f'<circle cx="{s * 0.62:.1f}" cy="{-h * 0.25:.1f}" r="1.6" fill="#0a0f14"/>'
    return g


def body_docs(s, stage):
    """Nautilus: living spiral; golden ratio glows at stage 3."""
    g = ""
    r = s * 0.55
    if stage >= 2:
        g += f'<circle cx="0" cy="0" r="{r * 1.05:.1f}" fill="{P.AMBER}" opacity="{0.12 * stage:.2f}" filter="url(#blur4)" class="pulse"/>'
    g += f'<circle cx="0" cy="0" r="{r:.1f}" fill="#caa46a"/>'
    # logarithmic spiral
    pts, a, b = [], r * 0.16, 0.21
    for i in range(40):
        t = i * 0.35
        rr = min(a * math.exp(b * t), r)
        pts.append((rr * math.cos(t), rr * math.sin(t)))
    stroke = P.GOLD if stage == 3 else "#8a6a3a"
    g += f'<path d="{_smooth(pts)}" stroke="{stroke}" stroke-width="{1.2 + stage * 0.5:.1f}" fill="none" opacity="0.95"/>'
    if stage >= 2:  # chamber walls
        for i in range(2, 2 + stage * 2):
            t = i * 0.8
            rr = min(a * math.exp(b * t), r * 0.95)
            g += (f'<line x1="0" y1="0" x2="{rr * math.cos(t):.1f}" y2="{rr * math.sin(t):.1f}" '
                  f'stroke="#8a6a3a" stroke-width="0.8" opacity="0.7"/>')
    tn = stage + 2
    for i in range(tn):  # tentacles out the aperture
        ang = math.pi * (0.92 + 0.16 * i / tn)
        g += (f'<path d="M {r * math.cos(ang) * 0.9:.1f},{r * math.sin(ang) * 0.9:.1f} '
              f'q {-8 - stage * 3},{4} {-12 - stage * 4},{10}" stroke="#b58a55" stroke-width="1.6" fill="none" class="sway"/>')
    g += f'<circle cx="{-r * 0.72:.1f}" cy="{r * 0.28:.1f}" r="2" fill="#0a0f14"/>'
    return g


def body_multi(s, stage):
    """Reef Shark: the apex generalist."""
    h = s * 0.3
    body = _smooth([(-s, 0), (-s * 0.45, -h * 0.75), (s * 0.3, -h), (s * 0.85, -h * 0.3),
                    (s * 1.05, 0), (s * 0.85, h * 0.3), (s * 0.3, h * 0.8), (-s * 0.45, h * 0.7)], close=True)
    g = f'<path d="{body}" fill="url(#sharkGrad)"/>'
    g += f'<path d="{_path([(-s * 0.05, -h * 0.95), (s * 0.12, -h * 1.9), (s * 0.3, -h * 0.9)], close=True)}" fill="url(#sharkGrad)"/>'
    g += f'<path d="{_path([(-s, 0), (-s * 1.35, -h * 1.5), (-s * 1.15, 0), (-s * 1.3, h * 0.9)], close=True)}" fill="url(#sharkGrad)"/>'
    g += f'<path d="M {s * 0.25:.1f},{h * 0.75:.1f} l {-h * 0.6:.1f},{h * 0.9:.1f} l {-h * 0.7:.1f},{-h * 0.55:.1f} Z" fill="url(#sharkGrad)"/>'
    g += f'<circle cx="{s * 0.8:.1f}" cy="{-h * 0.25:.1f}" r="{max(1.4, h * 0.13):.1f}" fill="#05080d"/>'
    g += f'<path d="M {s * 0.95:.1f},{h * 0.22:.1f} q {-s * 0.25:.1f},{h * 0.5:.1f} {-s * 0.55:.1f},{h * 0.42:.1f}" stroke="#05080d" stroke-width="1.6" fill="none"/>'
    if stage >= 2:  # scars
        for i in range(stage):
            g += f'<line x1="{s * 0.15 - i * 9:.1f}" y1="{-h * 0.4:.1f}" x2="{s * 0.28 - i * 9:.1f}" y2="{-h * 0.05:.1f}" stroke="#7d8a8f" stroke-width="1" opacity="0.7"/>'
    if stage == 3:  # pressure wake
        g += (f'<path d="M {-s * 1.45:.1f},-4 q -14,4 -26,0 M {-s * 1.45:.1f},5 q -16,3 -30,-2" '
              f'stroke="{P.TEAL_DIM}" stroke-width="1.4" fill="none" opacity="0.5"/>')
    return g


BODIES = {
    sp.PYTHON: body_python, sp.JS: body_js, sp.AI: body_ai,
    sp.DEVOPS: body_devops, sp.FRONTEND: body_frontend, sp.CLI: body_cli,
    sp.DATA: body_data, sp.MOBILE: body_mobile, sp.DOCS: body_docs,
    sp.MULTI: body_multi,
}


# ---------------------------------------------------------------- trait overlays

def trait_bands(s, strong=True):
    g = ""
    for i in range(4):
        x = -s * 0.55 + i * s * 0.33
        g += f'<rect x="{x:.1f}" y="{-s * 0.3:.1f}" width="{s * 0.1:.1f}" height="{s * 0.6:.1f}" rx="2" fill="#eef3f5" opacity="{0.75 if strong else 0.5}"/>'
    return g


def trait_streaks(s, strong=True):
    g = ""
    for i, op in enumerate((0.55, 0.35, 0.2)):
        g += (f'<line x1="{-s * 1.2 - i * 12:.1f}" y1="{(i - 1) * 7}" x2="{-s * 2.0 - i * 16:.1f}" y2="{(i - 1) * 7}" '
              f'stroke="{P.GOLD}" stroke-width="2" opacity="{op}" stroke-linecap="round"/>')
    return g


def trait_circuits(s, strong=True):
    col = P.TEAL if strong else P.TEAL_DIM
    op = 0.9 if strong else 0.45
    g = ""
    nodes = [(-s * 0.3, -s * 0.25), (0, -s * 0.4), (s * 0.25, -s * 0.15),
             (-s * 0.15, s * 0.2), (s * 0.2, s * 0.3), (0, 0)]
    for i in range(len(nodes) - 1):
        x1, y1 = nodes[i]
        x2, y2 = nodes[i + 1]
        g += f'<path d="M {x1:.1f},{y1:.1f} L {x1:.1f},{y2:.1f} L {x2:.1f},{y2:.1f}" stroke="{col}" stroke-width="1" fill="none" opacity="{op}"/>'
    for x, y in nodes:
        g += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.5" fill="{col}" opacity="{op}" class="pulse"/>'
    return g


def trait_armor(s, strong=True):
    rainbow = ["#ff5d5d", "#ffb347", "#ffe066", "#2eff9e", "#14e0c8"]
    g = ""
    for i in range(5):
        x = s * 0.45 - i * s * 0.24
        g += (f'<path d="M {x:.1f},{-s * 0.3:.1f} a {s * 0.13:.1f} {s * 0.13:.1f} 0 0 0 {-s * 0.2:.1f},0" '
              f'stroke="{rainbow[i]}" stroke-width="3" fill="none" opacity="{0.95 if strong else 0.6}"/>')
    return g


def trait_plumes(s, strong=True):
    g = ""
    n = 7 if strong else 5
    for i in range(n):
        a = math.pi * (0.6 + 0.5 * (i / (n - 1) - 0.5))
        L = s * (1.3 if strong else 0.9)
        tx, ty = -math.cos(a) * L, -abs(math.sin(a)) * L
        col = P.BLOOD if i % 2 else "#e8edf0"
        g += f'<path d="M 0,{-s * 0.15:.1f} Q {tx * 0.5:.1f},{ty * 0.6:.1f} {tx:.1f},{ty:.1f}" stroke="{col}" stroke-width="1.3" fill="none" opacity="0.8" class="sway"/>'
        if strong:
            g += f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="1.6" fill="{P.EMERALD}" class="pulse"/>'
    return g


def trait_spots(s, strong=True):
    g = ""
    import random
    rnd = random.Random(7)
    for _ in range(10 if strong else 6):
        x = rnd.uniform(-s * 0.85, s * 0.85)
        y = rnd.uniform(-s * 0.2, s * 0.2)
        g += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(1, 2.2):.1f}" fill="{P.EMERALD}" opacity="{0.85 if strong else 0.5}" class="pulse"/>'
    return g


def trait_lure(s, strong=True):
    lx, ly = s * 0.7, -s * 0.75
    g = f'<path d="M {s * 0.4:.1f},{-s * 0.25:.1f} Q {s * 0.6:.1f},{ly:.1f} {lx:.1f},{ly:.1f}" stroke="#2a3540" stroke-width="1.3" fill="none"/>'
    g += f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="{4 if strong else 2.6}" fill="{P.TEAL}" filter="url(#glowS)" class="pulse"/>'
    return g


def trait_wings(s, strong=True):
    g = ""
    for sign in (-1, 1):
        L = s * (1.2 if strong else 0.8)
        g += (f'<path d="M 0,{sign * s * 0.12:.1f} Q {s * 0.3:.1f},{sign * L * 0.7:.1f} {s * 0.7:.1f},{sign * L:.1f} '
              f'Q {s * 0.1:.1f},{sign * L * 0.7:.1f} {-s * 0.25:.1f},{sign * s * 0.12:.1f} Z" '
              f'fill="url(#iridGrad)" opacity="0.6" class="sway"/>')
    return g


def trait_spiral(s, strong=True):
    pts, a, b = [], s * 0.06, 0.22
    for i in range(34):
        t = i * 0.35
        rr = min(a * math.exp(b * t), s * 0.38)
        pts.append((rr * math.cos(t) - s * 0.1, rr * math.sin(t)))
    return (f'<path d="{_smooth(pts)}" stroke="{P.GOLD}" stroke-width="1.2" fill="none" '
            f'opacity="{0.85 if strong else 0.5}" class="pulse"/>')


TRAIT_FNS = {
    "bands": trait_bands, "streaks": trait_streaks, "circuits": trait_circuits,
    "armor": trait_armor, "plumes": trait_plumes, "spots": trait_spots,
    "lure": trait_lure, "wings": trait_wings, "spiral": trait_spiral,
}


# ---------------------------------------------------------------- composition

def render_creature(x, y, base_cat, overlay_cat, stage, size, label, sub,
                    facing=1, delay=0.0) -> str:
    """Full creature group at scene coords with swim animation + label."""
    body = BODIES[base_cat](size, stage)
    if overlay_cat:
        body += TRAIT_FNS[sp.TRAITS[overlay_cat]](size, strong=(stage >= 2))
    flip = f" scale({facing},1)" if facing == -1 else ""
    # animation class lives on an inner group: CSS transform animations
    # would otherwise stomp the positioning transform attribute
    return (
        f'<g transform="translate({x:.0f},{y:.0f})">'
        f'<g class="swim" style="animation-delay:{delay:.1f}s">'
        f'<g transform="scale(1){flip}">{body}</g>'
        f'<text x="0" y="{size * 0.85 + 16:.0f}" class="lbl" text-anchor="middle">{label}</text>'
        f'<text x="0" y="{size * 0.85 + 28:.0f}" class="sub" text-anchor="middle">{sub}</text>'
        f'</g></g>'
    )
