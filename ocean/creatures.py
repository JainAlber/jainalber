"""The universal evolution ladder: every repo climbs the same 10 tiers,
from a translucent larval fry to the Mythic Leviathan.

Each tier is a hand-built creature drawn facing +x, centered on the
origin. ``s`` is the half-length scale; SIZES gives each tier a
presence proportional to its rank.
"""

import math

from . import palette as P

SIZES = {1: 22, 2: 27, 3: 32, 4: 38, 5: 50, 6: 56, 7: 48, 8: 60, 9: 62, 10: 78}


def _sine_path(s, waves, amp, n=36, y0=0.0):
    pts = []
    for i in range(n):
        t = i / (n - 1)
        x = -s + 2 * s * t
        y = y0 + amp * math.sin(waves * math.tau * t)
        pts.append(f"{x:.1f},{y:.1f}")
    return "M " + " L ".join(pts)


# ---------------------------------------------------------------- tiers

def _t1_abyssal_fry(s) -> str:
    """Tiny translucent larva — barely there, all eye and tail filament."""
    g = (f'<ellipse cx="0" cy="0" rx="{s:.0f}" ry="{s * 0.32:.0f}" fill="{P.PALE}" '
         f'opacity="0.30"/>')
    g += (f'<ellipse cx="0" cy="0" rx="{s * 1.25:.0f}" ry="{s * 0.45:.0f}" fill="{P.PALE}" '
          f'opacity="0.12" filter="url(#blur2)"/>')
    # visible gut speck — the only solid thing in it
    g += f'<circle cx="{-s * 0.15:.0f}" cy="{s * 0.05:.0f}" r="{s * 0.12:.1f}" fill="{P.SILVER}" opacity="0.5"/>'
    # oversized larval eye
    g += (f'<circle cx="{s * 0.55:.0f}" cy="{-s * 0.05:.0f}" r="{s * 0.18:.1f}" fill="#0a0f1e" opacity="0.85"/>'
          f'<circle cx="{s * 0.60:.0f}" cy="{-s * 0.10:.0f}" r="{s * 0.06:.1f}" fill="{P.PEARL}"/>')
    # tail filament
    g += (f'<path d="M {-s:.0f},0 q {-s * 0.5:.0f},{-s * 0.18:.0f} {-s * 0.95:.0f},{s * 0.05:.0f}" '
          f'stroke="{P.PALE}" stroke-width="0.8" fill="none" opacity="0.45" class="sway"/>')
    return g


def _t2_reef_guppy(s) -> str:
    """Small swift fish — basic form, one clean colour."""
    body = (f'M {-s * 0.7:.0f},0 Q {-s * 0.2:.0f},{-s * 0.42:.0f} {s * 0.55:.0f},{-s * 0.18:.0f} '
            f'Q {s * 0.95:.0f},0 {s * 0.55:.0f},{s * 0.18:.0f} '
            f'Q {-s * 0.2:.0f},{s * 0.42:.0f} {-s * 0.7:.0f},0 Z')
    g = f'<path d="{body}" fill="{P.TEAL_DIM}" opacity="0.95"/>'
    # fan tail
    g += (f'<path d="M {-s * 0.65:.0f},0 L {-s * 1.15:.0f},{-s * 0.38:.0f} '
          f'Q {-s * 1.0:.0f},0 {-s * 1.15:.0f},{s * 0.38:.0f} Z" '
          f'fill="{P.TEAL_DIM}" opacity="0.8" class="sway"/>')
    # dorsal bump + pectoral
    g += (f'<path d="M {-s * 0.1:.0f},{-s * 0.34:.0f} q {s * 0.22:.0f},{-s * 0.3:.0f} {s * 0.4:.0f},{-s * 0.02:.0f} Z" '
          f'fill="{P.TEAL_DIM}" opacity="0.75"/>')
    g += (f'<path d="M {s * 0.1:.0f},{s * 0.1:.0f} q {-s * 0.18:.0f},{s * 0.3:.0f} {-s * 0.34:.0f},{s * 0.16:.0f}" '
          f'stroke="{P.TEAL_DIM}" stroke-width="2" fill="none" opacity="0.7" class="sway"/>')
    # lateral glint + eye
    g += (f'<path d="M {-s * 0.5:.0f},0 Q 0,{-s * 0.1:.0f} {s * 0.5:.0f},{-s * 0.05:.0f}" '
          f'stroke="{P.SILVER}" stroke-width="1" fill="none" opacity="0.5"/>')
    g += (f'<circle cx="{s * 0.62:.0f}" cy="{-s * 0.08:.0f}" r="{s * 0.09:.1f}" fill="#0a0f1e"/>'
          f'<circle cx="{s * 0.65:.0f}" cy="{-s * 0.11:.0f}" r="{s * 0.03:.1f}" fill="{P.PEARL}"/>')
    return g


def _t3_neon_tang(s) -> str:
    """Disc-bodied tang with razor neon fins."""
    body = (f'M {-s * 0.75:.0f},0 Q {-s * 0.3:.0f},{-s * 0.62:.0f} {s * 0.35:.0f},{-s * 0.5:.0f} '
            f'Q {s * 0.92:.0f},{-s * 0.12:.0f} {s * 0.92:.0f},{s * 0.05:.0f} '
            f'Q {s * 0.4:.0f},{s * 0.55:.0f} {-s * 0.3:.0f},{s * 0.55:.0f} '
            f'Q {-s * 0.65:.0f},{s * 0.3:.0f} {-s * 0.75:.0f},0 Z')
    g = f'<path d="{body}" fill="{P.INDIGO}" opacity="0.92"/>'
    # glowing dorsal + anal fin blades
    g += (f'<path d="M {-s * 0.35:.0f},{-s * 0.52:.0f} Q {s * 0.05:.0f},{-s * 0.95:.0f} {s * 0.42:.0f},{-s * 0.46:.0f}" '
          f'stroke="{P.EMERALD}" stroke-width="2.4" fill="none" filter="url(#glowS)" class="pulse"/>')
    g += (f'<path d="M {-s * 0.3:.0f},{s * 0.5:.0f} Q {s * 0.1:.0f},{s * 0.85:.0f} {s * 0.45:.0f},{s * 0.42:.0f}" '
          f'stroke="{P.EMERALD}" stroke-width="2" fill="none" filter="url(#glowS)" class="pulse"/>')
    # sharp tail
    g += (f'<path d="M {-s * 0.7:.0f},0 L {-s * 1.2:.0f},{-s * 0.3:.0f} L {-s * 1.05:.0f},0 '
          f'L {-s * 1.2:.0f},{s * 0.3:.0f} Z" fill="{P.EMERALD}" opacity="0.85" class="sway"/>')
    # vivid accent sweep + eye
    g += (f'<path d="M {-s * 0.45:.0f},{s * 0.15:.0f} Q {s * 0.1:.0f},{s * 0.05:.0f} {s * 0.6:.0f},{-s * 0.15:.0f}" '
          f'stroke="{P.TEAL}" stroke-width="2.2" fill="none" opacity="0.9"/>')
    g += (f'<circle cx="{s * 0.55:.0f}" cy="{-s * 0.18:.0f}" r="{s * 0.1:.1f}" fill="#0a0f1e"/>'
          f'<circle cx="{s * 0.58:.0f}" cy="{-s * 0.21:.0f}" r="{s * 0.035:.1f}" fill="{P.PEARL}"/>')
    return g


def _t4_coral_hunter(s) -> str:
    """Angular triggerfish — patterned, confident, built to bite coral."""
    body = (f'M {-s * 0.7:.0f},0 L {-s * 0.1:.0f},{-s * 0.52:.0f} L {s * 0.55:.0f},{-s * 0.3:.0f} '
            f'Q {s:.0f},{-s * 0.05:.0f} {s * 0.92:.0f},{s * 0.12:.0f} '
            f'L {s * 0.45:.0f},{s * 0.38:.0f} L {-s * 0.15:.0f},{s * 0.5:.0f} Z')
    g = f'<path d="{body}" fill="#2a3848"/>'
    # gold war-paint diagonals
    for k in range(3):
        x0 = -s * 0.35 + k * s * 0.32
        g += (f'<path d="M {x0:.0f},{-s * 0.42:.0f} L {x0 + s * 0.22:.0f},{s * 0.42:.0f}" '
              f'stroke="{P.GOLD}" stroke-width="2.6" opacity="{0.85 - k * 0.15:.2f}"/>')
    # trigger spike + crescent tail
    g += (f'<path d="M {s * 0.05:.0f},{-s * 0.45:.0f} l {-s * 0.08:.0f},{-s * 0.42:.0f} '
          f'l {s * 0.2:.0f},{s * 0.3:.0f} Z" fill="{P.GOLD}" opacity="0.9"/>')
    g += (f'<path d="M {-s * 0.65:.0f},0 L {-s * 1.18:.0f},{-s * 0.42:.0f} Q {-s * 0.92:.0f},0 '
          f'{-s * 1.18:.0f},{s * 0.42:.0f} Z" fill="#2a3848" stroke="{P.GOLD}" '
          f'stroke-width="1.4" class="sway"/>')
    # set-back hunter eye with gold ring
    g += (f'<circle cx="{s * 0.32:.0f}" cy="{-s * 0.12:.0f}" r="{s * 0.13:.1f}" fill="none" '
          f'stroke="{P.GOLD}" stroke-width="1.4"/>'
          f'<circle cx="{s * 0.32:.0f}" cy="{-s * 0.12:.0f}" r="{s * 0.07:.1f}" fill="#0a0f1e"/>')
    # tight predator mouth
    g += (f'<path d="M {s * 0.88:.0f},{s * 0.04:.0f} l {s * 0.14:.0f},{s * 0.02:.0f}" '
          f'stroke="{P.PEARL}" stroke-width="1.6" stroke-linecap="round"/>')
    return g


def _t5_electric_eel(s) -> str:
    """Long body with bioluminescent current tracking along it."""
    spine = _sine_path(s, 1.6, s * 0.22)
    g = f'<path d="{spine}" stroke="#1d2a44" stroke-width="{s * 0.2:.1f}" fill="none" stroke-linecap="round"/>'
    # glow underlay + twin currents chasing along the body
    g += (f'<path d="{spine}" stroke="{P.TEAL}" stroke-width="{s * 0.3:.1f}" fill="none" '
          f'opacity="0.22" filter="url(#blur4)" class="pulse"/>')
    g += (f'<path d="{spine}" stroke="{P.TEAL}" stroke-width="1.6" fill="none" '
          f'stroke-dasharray="7 11" class="current"/>')
    g += (f'<path d="{_sine_path(s, 1.6, s * 0.22, y0=s * 0.07)}" stroke="{P.EMERALD}" '
          f'stroke-width="1.1" fill="none" stroke-dasharray="4 14" opacity="0.8" class="current2"/>')
    # blunt eel head + eye
    g += f'<circle cx="{s:.0f}" cy="0" r="{s * 0.13:.1f}" fill="#1d2a44"/>'
    g += (f'<circle cx="{s * 1.04:.0f}" cy="{-s * 0.04:.0f}" r="{s * 0.045:.1f}" fill="{P.TEAL}" '
          f'filter="url(#glowS)" class="pulse"/>')
    # ribbon fin under the tail half
    g += (f'<path d="M {-s:.0f},{s * 0.12:.0f} Q {-s * 0.4:.0f},{s * 0.42:.0f} {s * 0.2:.0f},{s * 0.22:.0f}" '
          f'stroke="#1d2a44" stroke-width="2" fill="none" opacity="0.6" class="sway"/>')
    return g


def _t6_barracuda(s) -> str:
    """Streamlined torpedo — pure speed with an underbite."""
    body = (f'M {-s * 0.95:.0f},0 Q {-s * 0.3:.0f},{-s * 0.2:.0f} {s * 0.55:.0f},{-s * 0.14:.0f} '
            f'L {s * 1.05:.0f},{-s * 0.02:.0f} L {s * 0.6:.0f},{s * 0.14:.0f} '
            f'Q {-s * 0.3:.0f},{s * 0.2:.0f} {-s * 0.95:.0f},0 Z')
    g = f'<path d="{body}" fill="url(#tunaGrad)"/>'
    # underbite jaw
    g += (f'<path d="M {s * 0.55:.0f},{s * 0.1:.0f} L {s * 1.12:.0f},{s * 0.05:.0f}" '
          f'stroke="{P.SILVER}" stroke-width="2.2" stroke-linecap="round"/>')
    # dark lateral stripe + flank dashes
    g += (f'<path d="M {-s * 0.85:.0f},0 L {s * 0.7:.0f},{-s * 0.02:.0f}" stroke="#22303e" '
          f'stroke-width="2.4" opacity="0.8"/>')
    for k in range(4):
        g += (f'<path d="M {-s * 0.5 + k * s * 0.3:.0f},{-s * 0.09:.0f} l {s * 0.07:.0f},{s * 0.05:.0f}" '
              f'stroke="#22303e" stroke-width="1.6" opacity="0.6"/>')
    # far-back dorsal + forked tail
    g += (f'<path d="M {-s * 0.45:.0f},{-s * 0.16:.0f} l {s * 0.12:.0f},{-s * 0.22:.0f} '
          f'l {s * 0.16:.0f},{s * 0.2:.0f} Z" fill="#3d5266"/>')
    g += (f'<path d="M {-s * 0.9:.0f},0 L {-s * 1.3:.0f},{-s * 0.3:.0f} L {-s * 1.12:.0f},0 '
          f'L {-s * 1.3:.0f},{s * 0.3:.0f} Z" fill="#3d5266" class="sway"/>')
    # speed streaks trailing the tail
    for k, dy in enumerate((-s * 0.12, 0, s * 0.12)):
        g += (f'<path d="M {-s * 1.35:.0f},{dy:.0f} l {-s * 0.5:.0f},0" stroke="{P.SILVER}" '
              f'stroke-width="1.1" opacity="0.3" class="pulse" '
              f'style="animation-delay:{k * 0.5:.1f}s"/>')
    g += (f'<circle cx="{s * 0.72:.0f}" cy="{-s * 0.05:.0f}" r="{s * 0.07:.1f}" fill="#0a0f1e"/>'
          f'<circle cx="{s * 0.74:.0f}" cy="{-s * 0.07:.0f}" r="{s * 0.025:.1f}" fill="{P.PEARL}"/>')
    return g


def _t7_deep_sea_angler(s) -> str:
    """Round-bodied lurker with an observability lure burning ahead of it."""
    # lure halo first so the body overlaps it
    lx, ly = s * 0.95, -s * 0.72
    g = f'<circle cx="{lx:.0f}" cy="{ly:.0f}" r="{s * 0.55:.0f}" fill="url(#lureHalo)" class="pulse"/>'
    body = (f'M {-s * 0.8:.0f},{-s * 0.05:.0f} Q {-s * 0.45:.0f},{-s * 0.62:.0f} {s * 0.25:.0f},{-s * 0.55:.0f} '
            f'Q {s * 0.85:.0f},{-s * 0.35:.0f} {s * 0.8:.0f},{s * 0.1:.0f} '
            f'Q {s * 0.6:.0f},{s * 0.55:.0f} {-s * 0.3:.0f},{s * 0.5:.0f} '
            f'Q {-s * 0.75:.0f},{s * 0.3:.0f} {-s * 0.8:.0f},{-s * 0.05:.0f} Z')
    g += f'<path d="{body}" fill="#141a2c"/>'
    g += f'<path d="{body}" fill="none" stroke="{P.INDIGO_DEEP}" stroke-width="1.2" opacity="0.8"/>'
    # gaping jaw with needle teeth
    g += (f'<path d="M {s * 0.78:.0f},{-s * 0.02:.0f} Q {s * 0.45:.0f},{s * 0.18:.0f} {s * 0.15:.0f},{s * 0.12:.0f}" '
          f'stroke="#060a16" stroke-width="{s * 0.16:.1f}" fill="none" stroke-linecap="round"/>')
    teeth = ""
    for k in range(5):
        tx = s * 0.7 - k * s * 0.13
        teeth += f'M {tx:.0f},{s * 0.02 + k * s * 0.012:.1f} l {-s * 0.025:.1f},{s * 0.1:.1f} l {-s * 0.04:.1f},{-s * 0.09:.1f} '
    g += f'<path d="{teeth}" stroke="{P.PEARL}" stroke-width="0.9" fill="none" opacity="0.9"/>'
    # lure stalk + burning bulb
    g += (f'<path d="M {s * 0.25:.0f},{-s * 0.52:.0f} Q {s * 0.55:.0f},{-s * 0.95:.0f} {lx:.0f},{ly:.0f}" '
          f'stroke="{P.SILVER}" stroke-width="1.3" fill="none" opacity="0.7" class="sway"/>')
    g += (f'<circle cx="{lx:.0f}" cy="{ly:.0f}" r="{s * 0.11:.1f}" fill="{P.TEAL}" '
          f'filter="url(#glowS)" class="pulse"/>')
    # small glowing eye, ragged fins, photophore specks
    g += f'<circle cx="{s * 0.4:.0f}" cy="{-s * 0.2:.0f}" r="{s * 0.06:.1f}" fill="{P.TEAL}" class="pulse"/>'
    g += (f'<path d="M {-s * 0.75:.0f},0 L {-s * 1.15:.0f},{-s * 0.28:.0f} L {-s * 1.05:.0f},{s * 0.05:.0f} '
          f'L {-s * 1.18:.0f},{s * 0.3:.0f} Z" fill="#141a2c" stroke="{P.INDIGO_DEEP}" '
          f'stroke-width="1" class="sway"/>')
    for k in range(6):
        px = -s * 0.5 + k * s * 0.2
        py = s * 0.3 * math.sin(k * 1.9) - s * 0.05
        g += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="1.1" fill="{P.TEAL}" opacity="0.55" class="pulse"/>'
    return g


def _t8_apex_mako(s) -> str:
    """High-velocity shark — pressure wake peeling off behind it."""
    body = (f'M {-s * 0.9:.0f},0 Q {-s * 0.2:.0f},{-s * 0.3:.0f} {s * 0.5:.0f},{-s * 0.22:.0f} '
            f'Q {s * 1.08:.0f},{-s * 0.06:.0f} {s * 1.12:.0f},{s * 0.02:.0f} '
            f'Q {s * 0.5:.0f},{s * 0.26:.0f} {-s * 0.9:.0f},0 Z')
    g = f'<path d="{body}" fill="url(#sharkGrad)"/>'
    # pale underside
    g += (f'<path d="M {-s * 0.6:.0f},{s * 0.08:.0f} Q {s * 0.3:.0f},{s * 0.22:.0f} {s * 0.95:.0f},{s * 0.04:.0f}" '
          f'stroke="{P.SILVER}" stroke-width="2.5" fill="none" opacity="0.35"/>')
    # tall dorsal, pectoral, crescent caudal
    g += (f'<path d="M {-s * 0.12:.0f},{-s * 0.26:.0f} Q {s * 0.0:.0f},{-s * 0.75:.0f} {s * 0.22:.0f},{-s * 0.28:.0f} Z" '
          f'fill="#2a3848"/>')
    g += (f'<path d="M {s * 0.25:.0f},{s * 0.12:.0f} L {s * 0.05:.0f},{s * 0.5:.0f} L {s * 0.42:.0f},{s * 0.2:.0f} Z" '
          f'fill="#2a3848"/>')
    g += (f'<path d="M {-s * 0.88:.0f},0 Q {-s * 1.25:.0f},{-s * 0.5:.0f} {-s * 1.32:.0f},{-s * 0.55:.0f} '
          f'L {-s * 1.18:.0f},0 Q {-s * 1.28:.0f},{s * 0.4:.0f} {-s * 1.24:.0f},{s * 0.45:.0f} Z" '
          f'fill="#2a3848" class="sway"/>')
    # gill slits
    for k in range(5):
        gx = s * 0.42 + k * s * 0.06
        g += (f'<path d="M {gx:.0f},{-s * 0.1:.0f} q {-s * 0.03:.1f},{s * 0.1:.1f} 0,{s * 0.18:.1f}" '
              f'stroke="#16202e" stroke-width="1.3" fill="none"/>')
    # black eye + pressure wake
    g += f'<circle cx="{s * 0.82:.0f}" cy="{-s * 0.08:.0f}" r="{s * 0.05:.1f}" fill="#05080f"/>'
    for k in range(3):
        wy = -s * 0.18 + k * s * 0.18
        g += (f'<path d="M {-s * 1.4:.0f},{wy:.0f} q {-s * 0.3:.0f},{s * 0.05:.0f} {-s * 0.6:.0f},{-s * 0.02:.0f}" '
              f'stroke="{P.TEAL_DIM}" stroke-width="1.2" fill="none" opacity="0.3" '
              f'class="pulse" style="animation-delay:{k * 0.6:.1f}s"/>')
    return g


def _t9_shadow_kraken(s) -> str:
    """Multi-tentacled dark mass — it manages this depth layer now."""
    g = (f'<ellipse cx="0" cy="0" rx="{s * 1.3:.0f}" ry="{s * 0.9:.0f}" fill="{P.INDIGO_DEEP}" '
         f'opacity="0.3" filter="url(#blur6)"/>')
    # mantle
    mantle = (f'M {-s * 0.15:.0f},{-s * 0.85:.0f} Q {s * 0.5:.0f},{-s * 0.75:.0f} {s * 0.55:.0f},{-s * 0.05:.0f} '
              f'Q {s * 0.55:.0f},{s * 0.35:.0f} {s * 0.1:.0f},{s * 0.4:.0f} '
              f'L {-s * 0.5:.0f},{s * 0.35:.0f} Q {-s * 0.7:.0f},{-s * 0.3:.0f} {-s * 0.15:.0f},{-s * 0.85:.0f} Z')
    g += f'<path d="{mantle}" fill="#0d1226"/>'
    g += f'<path d="{mantle}" fill="none" stroke="{P.INDIGO}" stroke-width="1.4" opacity="0.65"/>'
    # eight tentacles fanning down-back
    for k in range(8):
        bx = -s * 0.45 + k * s * 0.13
        ln = s * (0.9 + 0.35 * math.sin(k * 2.1))
        curve = 1 if k % 2 else -1
        g += (f'<path d="M {bx:.0f},{s * 0.35:.0f} q {curve * s * 0.18:.0f},{ln * 0.5:.0f} '
              f'{-curve * s * 0.22 - s * 0.12:.0f},{ln:.0f}" stroke="#0d1226" '
              f'stroke-width="{max(s * 0.09 - k * 0.15, 1.6):.1f}" fill="none" stroke-linecap="round" '
              f'class="sway" style="animation-delay:{k * 0.35:.1f}s"/>')
    # sucker glints on two front tentacles
    for k in range(4):
        g += (f'<circle cx="{-s * 0.3 + k * s * 0.05:.0f}" cy="{s * 0.55 + k * s * 0.18:.0f}" r="1.2" '
              f'fill="{P.INDIGO}" opacity="0.55"/>')
    # vast emerald eyes
    for ex in (s * 0.18, s * 0.42):
        g += (f'<circle cx="{ex:.0f}" cy="{-s * 0.15:.0f}" r="{s * 0.13:.1f}" fill="#05080f"/>'
              f'<circle cx="{ex:.0f}" cy="{-s * 0.15:.0f}" r="{s * 0.08:.1f}" fill="{P.EMERALD}" '
              f'filter="url(#glowS)" class="pulse"/>')
    return g


def _t10_mythic_leviathan(s) -> str:
    """Ancient armored deity — indigo and emerald, absolute presence."""
    g = (f'<ellipse cx="0" cy="0" rx="{s * 1.6:.0f}" ry="{s * 0.8:.0f}" fill="{P.INDIGO_DEEP}" '
         f'opacity="0.25" filter="url(#blur6)" class="pulse"/>')
    for k, r in enumerate((1.25, 1.5)):
        g += (f'<ellipse cx="0" cy="0" rx="{s * r:.0f}" ry="{s * r * 0.45:.0f}" fill="none" '
              f'stroke="{P.EMERALD}" stroke-width="0.8" opacity="{0.16 - k * 0.05:.2f}" class="pulse"/>')
    # serpentine bulk
    body = (f'M {-s * 1.1:.0f},{s * 0.1:.0f} Q {-s * 0.6:.0f},{-s * 0.42:.0f} {s * 0.1:.0f},{-s * 0.38:.0f} '
            f'Q {s * 0.8:.0f},{-s * 0.32:.0f} {s * 1.1:.0f},{-s * 0.02:.0f} '
            f'Q {s * 0.85:.0f},{s * 0.3:.0f} {s * 0.1:.0f},{s * 0.34:.0f} '
            f'Q {-s * 0.7:.0f},{s * 0.38:.0f} {-s * 1.1:.0f},{s * 0.1:.0f} Z')
    g += f'<path d="{body}" fill="{P.INK}"/>'
    # armor plates along the back
    plates = ""
    for k in range(7):
        px = -s * 0.85 + k * s * 0.28
        py = -s * 0.36 + s * 0.05 * math.sin(k * 1.2)
        pw = s * 0.16
        plates += f'M {px:.0f},{py:.0f} a {pw:.0f} {pw:.0f} 0 0 1 {pw * 1.6:.0f},0 '
    g += (f'<path d="{plates}" fill="#1a2560" stroke="{P.INDIGO}" stroke-width="1.3" '
          f'opacity="0.95"/>')
    # emerald biolume line + gold rune dots
    g += (f'<path d="M {-s * 1.0:.0f},{s * 0.18:.0f} Q 0,{s * 0.3:.0f} {s * 0.95:.0f},{s * 0.08:.0f}" '
          f'stroke="{P.EMERALD}" stroke-width="1.8" fill="none" opacity="0.8" class="pulse"/>')
    for k in range(6):
        gx = -s * 0.75 + k * s * 0.3
        g += (f'<circle cx="{gx:.0f}" cy="{-s * 0.08 + s * 0.06 * math.sin(k * 2.2):.0f}" r="2.2" '
              f'fill="{P.GOLD}" class="pulse" style="animation-delay:{k * 0.4:.1f}s"/>')
    # great head: brow, jaw, burning eye
    g += (f'<path d="M {s * 0.75:.0f},{-s * 0.3:.0f} Q {s * 1.25:.0f},{-s * 0.22:.0f} {s * 1.35:.0f},{-s * 0.02:.0f} '
          f'L {s * 1.2:.0f},{s * 0.12:.0f} Q {s * 0.9:.0f},{s * 0.22:.0f} {s * 0.75:.0f},{s * 0.1:.0f} Z" '
          f'fill="{P.INK}" stroke="{P.INDIGO}" stroke-width="1"/>')
    g += (f'<path d="M {s * 1.08:.0f},{s * 0.06:.0f} L {s * 1.38:.0f},{s * 0.1:.0f}" '
          f'stroke="{P.EMERALD}" stroke-width="1.4" opacity="0.7"/>')
    g += (f'<circle cx="{s * 1.05:.0f}" cy="{-s * 0.12:.0f}" r="{s * 0.07:.1f}" fill="{P.EMERALD}" '
          f'filter="url(#glowS)" class="pulse"/>'
          f'<circle cx="{s * 1.05:.0f}" cy="{-s * 0.12:.0f}" r="{s * 0.11:.1f}" fill="none" '
          f'stroke="{P.GOLD}" stroke-width="1" opacity="0.8"/>')
    # ancient fins + tail flukes
    g += (f'<path d="M {s * 0.2:.0f},{s * 0.32:.0f} Q {s * 0.05:.0f},{s * 0.75:.0f} {-s * 0.15:.0f},{s * 0.8:.0f} '
          f'Q 0,{s * 0.5:.0f} {-s * 0.05:.0f},{s * 0.34:.0f} Z" fill="#1a2560" '
          f'stroke="{P.INDIGO}" stroke-width="1" class="sway"/>')
    g += (f'<path d="M {-s * 1.05:.0f},{s * 0.08:.0f} L {-s * 1.5:.0f},{-s * 0.32:.0f} '
          f'L {-s * 1.32:.0f},{s * 0.08:.0f} L {-s * 1.5:.0f},{s * 0.42:.0f} Z" fill="{P.INK}" '
          f'stroke="{P.INDIGO}" stroke-width="1.2" class="sway"/>')
    return g


RENDER = {
    1: _t1_abyssal_fry, 2: _t2_reef_guppy, 3: _t3_neon_tang,
    4: _t4_coral_hunter, 5: _t5_electric_eel, 6: _t6_barracuda,
    7: _t7_deep_sea_angler, 8: _t8_apex_mako, 9: _t9_shadow_kraken,
    10: _t10_mythic_leviathan,
}


def render_creature(x, y, tier, label, sub, facing=1, delay=0.0,
                    patrol="patrolM", duration=10.0) -> str:
    """Creature group at scene coords: patrols its lane horizontally,
    bobs as it swims, carries its labels with it."""
    s = SIZES[tier]
    body = RENDER[tier](s)
    flip = f' transform="scale({facing},1)"' if facing == -1 else ""
    # animated classes sit on nested groups: CSS transform animations
    # would otherwise stomp the positioning transform attribute
    return (
        f'<g transform="translate({x:.0f},{y:.0f})">'
        f'<g class="{patrol}" style="animation-duration:{duration:.1f}s;animation-delay:-{delay:.1f}s">'
        f'<g class="swim" style="animation-delay:{delay:.1f}s">'
        f'<g{flip}>{body}</g>'
        f'<text x="0" y="{s * 0.95 + 24:.0f}" class="lbl" text-anchor="middle">{label}</text>'
        f'<text x="0" y="{s * 0.95 + 42:.0f}" class="sub" text-anchor="middle">{sub}</text>'
        f'</g></g></g>'
    )
