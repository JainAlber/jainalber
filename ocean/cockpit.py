"""Submersible telemetry cockpit: riveted dark panel, glowing gauges."""

from . import palette as P


def _gauge(x, y, label, value, accent) -> str:
    """Arc gauge with value readout."""
    g = (f'<g transform="translate({x},{y})">'
         f'<path d="M -26,8 A 27 27 0 0 1 26,8" fill="none" stroke="{P.PANEL_EDGE}" stroke-width="5" stroke-linecap="round"/>'
         f'<path d="M -26,8 A 27 27 0 0 1 26,8" fill="none" stroke="{accent}" stroke-width="5" '
         f'stroke-linecap="round" stroke-dasharray="60 95" class="gaugepulse"/>'
         f'<text x="0" y="4" class="gval" text-anchor="middle" fill="{accent}">{value}</text>'
         f'<text x="0" y="26" class="glbl" text-anchor="middle">{label}</text>'
         f'</g>')
    return g


def _fmt(v) -> str:
    return "—" if v is None else str(v)


def render_cockpit(x, y, w, state, tier_name, depth_zone) -> str:
    h = 190
    g = f'<g transform="translate({x},{y})">'
    # hull panel
    g += (f'<rect x="0" y="0" width="{w}" height="{h}" rx="14" fill="{P.PANEL}" '
          f'stroke="{P.PANEL_EDGE}" stroke-width="2"/>')
    g += f'<rect x="6" y="6" width="{w - 12}" height="{h - 12}" rx="10" fill="none" stroke="{P.PANEL_EDGE}" stroke-width="0.7" opacity="0.6"/>'
    # rivets
    for rx in (16, w - 16):
        for ry in (16, h - 16):
            g += f'<circle cx="{rx}" cy="{ry}" r="2.4" fill="{P.PANEL_EDGE}"/>'
    # nameplate
    g += (f'<text x="{w / 2}" y="30" class="plate" text-anchor="middle">DSV JAIN PRASAD ALBER</text>'
          f'<text x="{w / 2}" y="46" class="platesub" text-anchor="middle">CYBERSECURITY × AI · B.E. CS @ BITS PILANI DUBAI</text>')
    g += f'<line x1="20" y1="56" x2="{w - 20}" y2="56" stroke="{P.PANEL_EDGE}" stroke-width="1"/>'
    # depth zone banner
    g += (f'<text x="{w / 2}" y="78" class="zone" text-anchor="middle" fill="{P.EMERALD}">'
          f'DEPTH ZONE · {depth_zone.upper()} — {tier_name.upper()}</text>')
    # gauges
    cols = 4
    items = [
        ("COMMITS", _fmt(state.total_commits), P.TEAL),
        ("STREAK", _fmt(state.streak) + ("d" if state.streak is not None else ""), P.EMERALD),
        ("OPEN PRS", _fmt(state.open_prs), P.GOLD),
        ("VESSELS", str(len(state.repos)), P.INDIGO),
    ]
    for i, (label, value, accent) in enumerate(items):
        gx = w * (i + 0.5) / cols
        g += _gauge(gx, 122, label, value, accent)
    # sync stamp + blinking status LED
    stamp = state.generated.strftime("%Y-%m-%d %H:%M UTC")
    g += (f'<circle cx="24" cy="{h - 16}" r="3" fill="{P.EMERALD}" class="flicker"/>'
          f'<text x="34" y="{h - 12}" class="stamp">SYSTEMS NOMINAL · LAST SONAR SWEEP {stamp}</text>')
    g += '</g>'
    return g
