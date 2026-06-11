"""Entry point: fetch GitHub state, render the ocean, write README assets.

Usage: python -m ocean.generate
Requires GITHUB_TOKEN for streak data; degrades gracefully without it.
"""

import os
import pathlib
import sys
import xml.etree.ElementTree as ET

from . import fetch, scene

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# Served from Vercel (connected to the ocean-asset repo) so the SVG's CSS
# animations survive — GitHub freezes styles on repo-hosted SVGs.
SVG_URL = os.environ.get(
    "OCEAN_SVG_URL", "https://jainalber-ocean.vercel.app/ocean.svg")

README = f"""<div align="center">

<img src="{SVG_URL}" alt="A living deep ocean ecosystem: an evolving eastern dragon, repositories swimming as sea creatures, tech-stack jellyfish, and a submersible telemetry cockpit." width="100%" />

<sub>🌊 A living ecosystem — the dragon grows with every commit, repos swim at their
depth, jellyfish glow while their tech stays warm. Regenerated every Sunday by
<a href=".github/workflows/ocean-sync.yml">ocean-sync</a>.</sub>

</div>
"""


def main() -> int:
    if "--offline" in sys.argv:
        state = fetch.load_state(str(ASSETS / "ocean-state.json"))
    else:
        state = fetch.fetch_ocean()
    if not state.repos:
        print("ERROR: no repos fetched — aborting without touching files", file=sys.stderr)
        return 1

    svg = scene.build_svg(state)

    # never ship a malformed scene
    try:
        ET.fromstring(svg)
    except ET.ParseError as e:
        print(f"ERROR: generated SVG is not valid XML: {e}", file=sys.stderr)
        return 1

    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "ocean.svg").write_text(svg, encoding="utf-8")
    fetch.save_state(state, str(ASSETS / "ocean-state.json"))
    (ROOT / "README.md").write_text(README, encoding="utf-8")

    print(f"ocean rendered: {len(state.repos)} repos, "
          f"{state.total_commits} commits, streak={state.streak}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
