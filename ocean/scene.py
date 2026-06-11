"""Scene composer: one continuous SVG ocean, surface light to abyss."""

import math
import random

from . import cockpit, creatures, dragon, jellyfish
from . import palette as P
from . import species as sp
from . import tiers

W, H = 900, 1750
MAX_REPOS = 10

STYLE = f"""
  text {{ font-family: {P.MONO}; }}
  .lbl   {{ font-size: 12px; fill: {P.TEXT}; letter-spacing: 1px; }}
  .sub   {{ font-size: 9px;  fill: {P.TEXT_DIM}; letter-spacing: 1px; }}
  .jlbl  {{ font-size: 10px; fill: {P.TEXT}; letter-spacing: 1px; }}
  .plate {{ font-size: 17px; fill: {P.PEARL}; letter-spacing: 4px; font-weight: bold; }}
  .platesub {{ font-size: 9px; fill: {P.TEXT_DIM}; letter-spacing: 2px; }}
  .zone  {{ font-size: 11px; letter-spacing: 2px; }}
  .gval  {{ font-size: 15px; font-weight: bold; }}
  .glbl  {{ font-size: 8px; fill: {P.TEXT_DIM}; letter-spacing: 1.5px; }}
  .stamp {{ font-size: 8px; fill: {P.TEXT_DIM}; letter-spacing: 1px; }}
  .caption {{ font-size: 11px; fill: {P.TEXT_DIM}; letter-spacing: 5px; }}
  .dlabel  {{ font-size: 13px; fill: {P.TEXT}; letter-spacing: 3px; }}
  .dsub    {{ font-size: 10px; fill: {P.TEXT_DIM}; letter-spacing: 2px; }}

  .swim        {{ animation: swim 9s ease-in-out infinite; }}
  .drift       {{ animation: drift 7s ease-in-out infinite; }}
  .dragonfloat {{ animation: dfloat 12s ease-in-out infinite; }}
  .sway        {{ animation: sway 5s ease-in-out infinite; transform-origin: 0 0; }}
  .pulse       {{ animation: pulse 4s ease-in-out infinite; }}
  .jpulse      {{ animation: jpulse 4.5s ease-in-out infinite; transform-origin: 0 0; }}
  .flicker     {{ animation: flicker 2.2s steps(2, start) infinite; }}
  .gaugepulse  {{ animation: pulse 5s ease-in-out infinite; }}
  .bubble      {{ animation: rise 14s linear infinite; }}
  .ray         {{ animation: raypulse 11s ease-in-out infinite; }}

  @keyframes swim   {{ 0%,100% {{ transform: translate(0,0); }} 50% {{ transform: translate(14px,-7px); }} }}
  @keyframes drift  {{ 0%,100% {{ transform: translate(0,0); }} 50% {{ transform: translate(-8px,-16px); }} }}
  @keyframes dfloat {{ 0%,100% {{ transform: translate(0,0); }} 50% {{ transform: translate(0,-14px); }} }}
  @keyframes sway   {{ 0%,100% {{ transform: rotate(0deg); }} 50% {{ transform: rotate(6deg); }} }}
  @keyframes pulse  {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.45; }} }}
  @keyframes jpulse {{ 0%,100% {{ transform: scale(1,1); }} 50% {{ transform: scale(1.08,0.92); }} }}
  @keyframes flicker {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.2; }} }}
  @keyframes rise   {{ 0% {{ transform: translateY(0); opacity: 0; }} 8% {{ opacity: 0.5; }}
                       92% {{ opacity: 0.4; }} 100% {{ transform: translateY(-520px); opacity: 0; }} }}
  @keyframes raypulse {{ 0%,100% {{ opacity: 0.04; }} 50% {{ opacity: 0.10; }} }}
"""

DEFS = f"""
<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{P.SURFACE}"/>
  <stop offset="0.18" stop-color="{P.SHALLOW}"/>
  <stop offset="0.45" stop-color="{P.MID}"/>
  <stop offset="0.75" stop-color="{P.DEEP}"/>
  <stop offset="1" stop-color="{P.ABYSS}"/>
</linearGradient>
<linearGradient id="tunaGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#5a7184"/><stop offset="0.55" stop-color="{P.SILVER}"/>
  <stop offset="1" stop-color="#7d96a8"/>
</linearGradient>
<linearGradient id="sharkGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#3a4654"/><stop offset="0.6" stop-color="#2a3848"/>
  <stop offset="1" stop-color="#1d2a44"/>
</linearGradient>
<linearGradient id="flyGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#7d96a8"/><stop offset="1" stop-color="#aebfd0"/>
</linearGradient>
<linearGradient id="iridGrad" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{P.TEAL}"/><stop offset="0.5" stop-color="{P.INDIGO}"/>
  <stop offset="1" stop-color="{P.SILVER}"/>
</linearGradient>
<radialGradient id="lureHalo">
  <stop offset="0" stop-color="{P.TEAL}" stop-opacity="0.5"/>
  <stop offset="1" stop-color="{P.TEAL}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="dragonHalo">
  <stop offset="0" stop-color="{P.INDIGO_DEEP}" stop-opacity="0.35"/>
  <stop offset="1" stop-color="{P.INDIGO_DEEP}" stop-opacity="0"/>
</radialGradient>
<filter id="blur2"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="blur4"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="blur6"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="glowS" x="-80%" y="-80%" width="260%" height="260%">
  <feGaussianBlur stdDeviation="2.2" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
"""


def _background() -> str:
    rnd = random.Random(42)
    g = f'<rect width="{W}" height="{H}" fill="url(#sea)"/>'
    # surface light rays — heavily blurred so they read as light, not bars
    for i in range(5):
        x = 90 + i * 180
        g += (f'<polygon points="{x},-40 {x + 46},-40 {x + 120},430 {x + 58},430" '
              f'fill="{P.TEAL_DIM}" class="ray" style="animation-delay:{i * 1.8}s" '
              f'opacity="0.07" filter="url(#blur6)"/>')
    # marine snow
    for _ in range(70):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        g += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(0.5, 1.4):.1f}" fill="{P.SILVER}" '
              f'opacity="{rnd.uniform(0.05, 0.25):.2f}"/>')
    # rising bubbles
    for i in range(12):
        x = rnd.uniform(30, W - 30)
        y = rnd.uniform(500, H - 60)
        g += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1.5, 3.5):.1f}" fill="none" '
              f'stroke="{P.TEAL_DIM}" stroke-width="0.7" class="bubble" '
              f'style="animation-delay:{i * 1.1:.1f}s"/>')
    # seafloor hint
    g += (f'<path d="M 0,{H - 26} Q {W * 0.25},{H - 52} {W * 0.5},{H - 30} '
          f'T {W},{H - 38} L {W},{H} L 0,{H} Z" fill="#01030a"/>')
    return g


def _repo_creatures(state) -> str:
    repos = sorted(state.repos, key=lambda r: r.pushed_at, reverse=True)[:MAX_REPOS]
    if not repos:
        return ""
    out = ""
    # free water between the jellyfish field, the dragon and the cockpit
    segments = [(300, 430), (760, 850), (1120, 1640)]
    total = sum(b - a for a, b in segments)

    def slot(t: float) -> float:
        d = t * total
        for a, b in segments:
            if d <= b - a:
                return a + d
            d -= b - a
        return segments[-1][1]

    for i, repo in enumerate(repos):
        t = i / max(len(repos) - 1, 1)
        y = slot(t)
        x = 165 if i % 2 == 0 else W - 165
        facing = 1 if i % 2 == 0 else -1
        stage = tiers.creature_stage(repo.commits)
        name, base, overlay = sp.resolve_species(repo.scores)
        size = 34 + stage * 9
        sub = f"{name} · st{stage} · {repo.commits} commits"
        out += creatures.render_creature(x, y, base, overlay, stage, size,
                                         repo.name, sub, facing=facing,
                                         delay=i * 0.9)
    return out


def build_svg(state) -> str:
    tier, tier_name, depth_zone = tiers.dragon_tier(state.total_commits)
    dragon_y = 575

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" aria-label="Living deep ocean ecosystem">',
        f'<defs>{DEFS}</defs>',
        f'<style>{STYLE}</style>',
        _background(),
        f'<text x="{W / 2}" y="58" class="caption" text-anchor="middle">T H E   L I V I N G   D E E P</text>',
        jellyfish.render_field(state.lang_age, state.tool_age, W, 140),
        f'<ellipse cx="{W / 2}" cy="{dragon_y}" rx="430" ry="190" fill="url(#dragonHalo)"/>',
        dragon.render_dragon(W / 2, dragon_y, state.total_commits, tier),
        f'<text x="{W / 2}" y="{dragon_y + 215}" class="dlabel" text-anchor="middle">{tier_name.upper()}</text>',
        f'<text x="{W / 2}" y="{dragon_y + 233}" class="dsub" text-anchor="middle">'
        f'TIER {tier}/10 · {state.total_commits} TOTAL COMMITS</text>',
        cockpit.render_cockpit((W - 640) / 2, 880, 640, state, tier_name, depth_zone),
        _repo_creatures(state),
        '</svg>',
    ]
    return "\n".join(svg)
