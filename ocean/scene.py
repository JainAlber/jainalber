"""Scene composer: one cinematic SVG ocean, surface light to abyss.

Wide 16:9-ish canvas — jellyfish strip up top, dragon center stage,
cockpit resting on the seafloor, repo creatures patrolling both flanks.
"""

import random

from . import cockpit, creatures, dragon, jellyfish
from . import palette as P
from . import tiers

W, H = 1400, 790
MAX_REPOS = 10

STYLE = f"""
  text {{ font-family: {P.MONO}; }}
  .lbl   {{ font-size: 16px; fill: {P.TEXT}; letter-spacing: 1px; font-weight: bold; }}
  .sub   {{ font-size: 11px; fill: {P.TEXT_DIM}; letter-spacing: 1px; }}
  .jlbl  {{ font-size: 12px; fill: {P.TEXT}; letter-spacing: 1px; }}
  .plate {{ font-size: 21px; fill: {P.PEARL}; letter-spacing: 4px; font-weight: bold; }}
  .platesub {{ font-size: 11px; fill: {P.TEXT_DIM}; letter-spacing: 2px; }}
  .zone  {{ font-size: 13px; letter-spacing: 2px; font-weight: bold; }}
  .gval  {{ font-size: 18px; font-weight: bold; }}
  .glbl  {{ font-size: 10px; fill: {P.TEXT_DIM}; letter-spacing: 1.5px; }}
  .stamp {{ font-size: 10px; fill: {P.TEXT_DIM}; letter-spacing: 1px; }}
  .caption {{ font-size: 14px; fill: {P.TEXT}; letter-spacing: 6px; }}
  .dlabel  {{ font-size: 18px; fill: {P.TEXT}; letter-spacing: 4px; font-weight: bold; }}
  .dsub    {{ font-size: 12px; fill: {P.TEXT_DIM}; letter-spacing: 2px; }}

  .swim        {{ animation: swim 8s ease-in-out infinite; }}
  .drift       {{ animation: drift 7s ease-in-out infinite; }}
  .dragonfloat {{ animation: dfloat 11s ease-in-out infinite; }}
  .dragonswim  {{ animation: dswim 26s ease-in-out infinite alternate; }}
  .patrolS     {{ animation: patrolS 12s ease-in-out infinite alternate; }}
  .patrolM     {{ animation: patrolM 12s ease-in-out infinite alternate; }}
  .patrolL     {{ animation: patrolL 12s ease-in-out infinite alternate; }}
  .sway        {{ animation: sway 4.5s ease-in-out infinite; transform-origin: 0 0; }}
  .pulse       {{ animation: pulse 4s ease-in-out infinite; }}
  .jpulse      {{ animation: jpulse 3.8s ease-in-out infinite; transform-origin: 0 0; }}
  .flicker     {{ animation: flicker 2.2s steps(2, start) infinite; }}
  .gaugepulse  {{ animation: pulse 5s ease-in-out infinite; }}
  .bubble      {{ animation: rise 12s linear infinite; }}
  .ray         {{ animation: raypulse 11s ease-in-out infinite; }}
  .halopulse   {{ animation: halopulse 9s ease-in-out infinite; }}
  .snow        {{ animation: snowdrift 17s ease-in-out infinite alternate; }}
  .current     {{ animation: currentflow 1.6s linear infinite; }}
  .current2    {{ animation: currentflow 2.4s linear infinite reverse; }}

  @keyframes swim {{
    0%, 100% {{ transform: translate(0, 0) rotate(0deg); }}
    25%      {{ transform: translate(11px, -7px) rotate(1.6deg); }}
    55%      {{ transform: translate(20px, 2px) rotate(-1.2deg); }}
    80%      {{ transform: translate(7px, 7px) rotate(0.7deg); }}
  }}
  @keyframes patrolS {{ from {{ transform: translateX(-55px); }}  to {{ transform: translateX(55px); }} }}
  @keyframes patrolM {{ from {{ transform: translateX(-85px); }}  to {{ transform: translateX(85px); }} }}
  @keyframes patrolL {{ from {{ transform: translateX(-120px); }} to {{ transform: translateX(120px); }} }}
  @keyframes dswim   {{ from {{ transform: translateX(-45px); }}  to {{ transform: translateX(45px); }} }}
  @keyframes currentflow {{ from {{ stroke-dashoffset: 0; }} to {{ stroke-dashoffset: -54; }} }}
  @keyframes drift {{
    0%, 100% {{ transform: translate(0, 0); }}
    33%      {{ transform: translate(-7px, -13px); }}
    66%      {{ transform: translate(6px, -19px); }}
  }}
  @keyframes dfloat {{
    0%, 100% {{ transform: translate(0, 0) scale(1); }}
    50%      {{ transform: translate(0, -11px) scale(1.013); }}
  }}
  @keyframes sway   {{ 0%,100% {{ transform: rotate(0deg); }} 50% {{ transform: rotate(7deg); }} }}
  @keyframes pulse  {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.45; }} }}
  @keyframes jpulse {{
    0%, 100% {{ transform: scale(1, 1); }}
    45%      {{ transform: scale(1.10, 0.90) translate(0, 1px); }}
    60%      {{ transform: scale(0.97, 1.05) translate(0, -2px); }}
  }}
  @keyframes flicker {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.2; }} }}
  @keyframes rise   {{ 0% {{ transform: translateY(0); opacity: 0; }} 10% {{ opacity: 0.5; }}
                       90% {{ opacity: 0.4; }} 100% {{ transform: translateY(-320px); opacity: 0; }} }}
  @keyframes raypulse {{ 0%,100% {{ opacity: 0.04; }} 50% {{ opacity: 0.10; }} }}
  @keyframes halopulse {{ 0%,100% {{ opacity: 0.65; }} 50% {{ opacity: 1; }} }}
  @keyframes snowdrift {{ from {{ transform: translate(0, 0); }} to {{ transform: translate(-16px, 30px); }} }}
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
    for i in range(7):
        x = 80 + i * 200
        g += (f'<polygon points="{x},-40 {x + 42},-40 {x + 104},330 {x + 50},330" '
              f'fill="{P.TEAL_DIM}" class="ray" style="animation-delay:{i * 1.6}s" '
              f'opacity="0.07" filter="url(#blur6)"/>')
    # marine snow, drifting
    for i in range(80):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        g += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(0.5, 1.4):.1f}" fill="{P.SILVER}" '
              f'opacity="{rnd.uniform(0.05, 0.25):.2f}" class="snow" '
              f'style="animation-delay:-{rnd.uniform(0, 17):.1f}s"/>')
    # rising bubbles
    for i in range(14):
        x = rnd.uniform(30, W - 30)
        y = rnd.uniform(380, H - 60)
        g += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1.5, 3.5):.1f}" fill="none" '
              f'stroke="{P.TEAL_DIM}" stroke-width="0.7" class="bubble" '
              f'style="animation-delay:{i * 0.9:.1f}s"/>')
    # distant ambient fish schools — depth and life, not data
    for sx, sy, count, flip, dur in ((340, 268, 7, 1, 0), (1010, 510, 6, -1, 3),
                                     (560, 640, 5, 1, 6)):
        school = ""
        for j in range(count):
            fx = sx + (j % 4) * 26 + (j // 4) * 13
            fy = sy + (j % 3) * 11 - (j // 3) * 7
            school += (f'<path d="M {fx},{fy} q 5,-3 9,0 q -4,3 -9,0 l -4,-3 l 1,3 '
                       f'l -1,3 Z" fill="{P.SILVER}" opacity="0.14"'
                       + (f' transform="scale(-1,1) translate({-2 * fx},0)"' if flip == -1 else "")
                       + '/>')
        g += (f'<g><g class="swim" style="animation-delay:{dur}s;animation-duration:13s">'
              f'{school}</g></g>')
    # seafloor hint
    g += (f'<path d="M 0,{H - 26} Q {W * 0.25},{H - 52} {W * 0.5},{H - 30} '
          f'T {W},{H - 38} L {W},{H} L 0,{H} Z" fill="#01030a"/>')
    return g


def _repo_creatures(state) -> str:
    """Two flank lanes, newest near surface, oldest brushing the seafloor."""
    repos = sorted(state.repos, key=lambda r: r.pushed_at, reverse=True)[:MAX_REPOS]
    if not repos:
        return ""
    out = ""
    y0, y1 = 252, 686
    patrols = ("patrolM", "patrolL", "patrolS")
    for i, repo in enumerate(repos):
        t = i / max(len(repos) - 1, 1)
        y = y0 + (y1 - y0) * t
        x = 175 if i % 2 == 0 else W - 175
        facing = 1 if i % 2 == 0 else -1
        tier_r, tname = tiers.repo_tier(repo.commits)
        label = repo.name if len(repo.name) <= 22 else repo.name[:20] + "…"
        sub = f"{tname.upper()} · T{tier_r} · {repo.commits} COMMITS"
        out += creatures.render_creature(x, y, tier_r, label, sub,
                                         facing=facing, delay=i * 1.7,
                                         patrol=patrols[i % 3],
                                         duration=9.0 + (i * 2.3) % 8)
    return out


def build_svg(state) -> str:
    tier, tier_name, depth_zone = tiers.dragon_tier(state.total_commits)
    dragon_y = 388

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" aria-label="Living deep ocean ecosystem">',
        f'<defs>{DEFS}</defs>',
        f'<style>{STYLE}</style>',
        _background(),
        f'<text x="{W / 2}" y="42" class="caption" text-anchor="middle">T H E   L I V I N G   D E E P</text>',
        jellyfish.render_field(state.lang_age, state.tool_age, W, 88),
        f'<ellipse cx="{W / 2}" cy="{dragon_y}" rx="430" ry="165" fill="url(#dragonHalo)" class="halopulse"/>',
        f'<g class="dragonswim">{dragon.render_dragon(W / 2, dragon_y, state.total_commits, tier)}</g>',
        f'<text x="{W / 2}" y="{dragon_y + 158}" class="dlabel" text-anchor="middle">{tier_name.upper()}</text>',
        f'<text x="{W / 2}" y="{dragon_y + 176}" class="dsub" text-anchor="middle">'
        f'TIER {tier}/10 · {state.total_commits} TOTAL COMMITS</text>',
        cockpit.render_cockpit((W - 640) / 2, 582, 640, state, tier_name, depth_zone),
        _repo_creatures(state),
        '</svg>',
    ]
    return "\n".join(svg)
