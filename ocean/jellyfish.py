"""Tech-stack jellyfish: each detected language/tool drifts as a jelly.

Freshness buckets (days since any repo containing the tech was pushed):
  < 30   bright, near surface
  30-90  dimmed, mid-depth
  90+    faded silhouettes sinking into the background
"""

import math

from . import palette as P

MAX_LANGS = 6
MAX_TOOLS = 8


def _bucket(age_days: int) -> int:
    if age_days < 30:
        return 0
    if age_days < 90:
        return 1
    return 2

BUCKET_COLOR = (P.JELLY_BRIGHT, P.JELLY_MID, P.JELLY_FADED)
BUCKET_OPACITY = (0.95, 0.6, 0.32)
BUCKET_GLOW = ("url(#glowS)", "", "")


def _jelly(x, y, r, color, opacity, glow, label, delay) -> str:
    bell = (f'M {-r:.1f},0 A {r:.1f} {r:.1f} 0 0 1 {r:.1f},0 '
            f'Q {r * 0.8:.1f},{r * 0.45:.1f} {r * 0.45:.1f},{r * 0.35:.1f} '
            f'Q {r * 0.2:.1f},{r * 0.5:.1f} 0,{r * 0.35:.1f} '
            f'Q {-r * 0.2:.1f},{r * 0.5:.1f} {-r * 0.45:.1f},{r * 0.35:.1f} '
            f'Q {-r * 0.8:.1f},{r * 0.45:.1f} {-r:.1f},0 Z')
    g = (f'<g transform="translate({x:.0f},{y:.0f})">'
         f'<g class="drift" style="animation-delay:{delay:.1f}s">')
    glow_attr = f' filter="{glow}"' if glow else ""
    g += f'<path d="{bell}" fill="{color}" opacity="{opacity}"{glow_attr} class="jpulse"/>'
    g += f'<path d="{bell}" fill="none" stroke="{color}" stroke-width="0.8" opacity="{opacity * 0.5:.2f}" transform="scale(1.18)" />'
    for i in range(5):
        tx = -r * 0.7 + i * r * 0.35
        tl = r * (1.3 + 0.4 * math.sin(i * 2.4))
        g += (f'<path d="M {tx:.1f},{r * 0.35:.1f} q {3 * (1 if i % 2 else -1)},{tl * 0.5:.1f} '
              f'{-2 * (1 if i % 2 else -1)},{tl:.1f}" stroke="{color}" stroke-width="0.9" '
              f'fill="none" opacity="{opacity * 0.7:.2f}" class="sway"/>')
    g += f'<text x="0" y="{r * 2.1 + 10:.0f}" class="jlbl" text-anchor="middle" opacity="{max(opacity, 0.45)}">{label}</text>'
    g += '</g></g>'
    return g


def render_field(lang_age: dict, tool_age: dict, width: int, y_top: int) -> str:
    """Lay jellies out in three depth rows by freshness bucket."""
    langs = sorted(lang_age.items(), key=lambda kv: kv[1])[:MAX_LANGS]
    tools = sorted(tool_age.items(), key=lambda kv: kv[1])[:MAX_TOOLS]
    items = ([(n, a, True) for n, a in langs] + [(n, a, False) for n, a in tools])
    rows: dict[int, list] = {0: [], 1: [], 2: []}
    for name, age, is_lang in items:
        rows[_bucket(age)].append((name, is_lang))

    out = ""
    row_y = (y_top, y_top + 130, y_top + 250)
    for b, members in rows.items():
        if not members:
            continue
        n = len(members)
        for i, (name, is_lang) in enumerate(members):
            x = width * (i + 1) / (n + 1) + (18 if b == 1 else -12 if b == 2 else 0)
            y = row_y[b] + 22 * math.sin(i * 1.7)
            r = (15 if is_lang else 11) - b * 2
            out += _jelly(x, y, r, BUCKET_COLOR[b], BUCKET_OPACITY[b],
                          BUCKET_GLOW[b], name, delay=i * 0.7 + b * 0.3)
    return out
