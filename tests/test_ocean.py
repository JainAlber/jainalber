import datetime as dt
import itertools
import xml.etree.ElementTree as ET

from ocean import detect, scene, tiers
from ocean import species as sp
from ocean.fetch import OceanState, RepoState


# ---------------------------------------------------------------- tiers

def test_dragon_tier_boundaries():
    assert tiers.dragon_tier(0)[0] == 1
    assert tiers.dragon_tier(15)[0] == 1
    assert tiers.dragon_tier(16)[0] == 2
    assert tiers.dragon_tier(400)[0] == 6
    assert tiers.dragon_tier(401)[0] == 7
    assert tiers.dragon_tier(1000)[0] == 9
    assert tiers.dragon_tier(1001)[0] == 10
    assert tiers.dragon_tier(50000)[0] == 10


def test_creature_stage_boundaries():
    assert tiers.creature_stage(0) == 1
    assert tiers.creature_stage(30) == 1
    assert tiers.creature_stage(31) == 2
    assert tiers.creature_stage(100) == 2
    assert tiers.creature_stage(101) == 3


# ---------------------------------------------------------------- species

def test_hybrid_table_covers_all_36_pairs():
    pairs = set(itertools.combinations(sp.CATEGORIES, 2))
    assert len(pairs) == 36
    for a, b in pairs:
        name, base, overlay = sp.HYBRIDS[frozenset({a, b})]
        assert base in (a, b) and overlay in (a, b) and base != overlay
        assert name


def test_resolve_pure_species_at_60_percent():
    name, base, overlay = sp.resolve_species({sp.PYTHON: 0.7, sp.JS: 0.3})
    assert (name, base, overlay) == ("Sea Krait", sp.PYTHON, None)


def test_resolve_hybrid_at_dual_30_percent():
    name, base, overlay = sp.resolve_species({sp.PYTHON: 0.45, sp.AI: 0.4, sp.CLI: 0.15})
    assert name == "Veiled Naga Ray"
    assert {base, overlay} == {sp.PYTHON, sp.AI}


def test_resolve_multi_everything_is_reef_shark():
    scores = {c: 1.0 for c in sp.CATEGORIES[:5]}
    name, base, overlay = sp.resolve_species(scores)
    assert name == "Reef Shark"
    assert base == sp.MULTI and overlay is None


def test_resolve_empty_scores_is_reef_shark():
    assert sp.resolve_species({})[0] == "Reef Shark"


# ---------------------------------------------------------------- detect

def test_package_json_deps():
    deps = detect.deps_from_package_json('{"dependencies": {"React": "^18", "next": "14"}}')
    assert deps == {"react", "next"}


def test_requirements_deps():
    deps = detect.deps_from_requirements("torch==2.1\n# comment\nflask[async]>=3\n")
    assert deps == {"torch", "flask"}


def test_scores_blend_langs_and_deps():
    scores = detect.category_scores(
        {"Python": 9000, "JavaScript": 1000},
        {"torch", "transformers"},
    )
    assert scores[sp.PYTHON] > scores[sp.JS]
    assert scores[sp.AI] > 0


def test_docker_bonus():
    scores = detect.category_scores({}, set(), has_docker=True)
    assert scores[sp.DEVOPS] > 0


# ---------------------------------------------------------------- scene

def _fixture_state() -> OceanState:
    now = dt.datetime.now(dt.timezone.utc)
    state = OceanState()
    state.repos = [
        RepoState("ml-thing", now, commits=120,
                  languages={"Python": 8000, "Jupyter Notebook": 4000},
                  deps={"torch", "pandas"}),
        RepoState("webapp", now - dt.timedelta(days=45), commits=55,
                  languages={"JavaScript": 5000, "CSS": 3000}, deps={"react"}),
        RepoState("dusty", now - dt.timedelta(days=400), commits=8,
                  languages={"Shell": 900}, deps=set()),
    ]
    state.total_commits = 183
    state.streak = 4
    state.open_prs = 2
    state.lang_age = {"Python": 0, "JavaScript": 45, "Shell": 400}
    state.tool_age = {"torch": 0, "react": 45}
    return state


def test_scene_renders_valid_xml_for_every_dragon_tier():
    state = _fixture_state()
    for commits in (0, 20, 60, 100, 200, 300, 500, 700, 900, 2000):
        state.total_commits = commits
        root = ET.fromstring(scene.build_svg(state))
        assert root.tag.endswith("svg")


def test_scene_contains_repo_labels_and_cockpit():
    svg = scene.build_svg(_fixture_state())
    assert "ml-thing" in svg and "webapp" in svg and "dusty" in svg
    assert "DSV JAIN PRASAD ALBER" in svg
    assert "183 TOTAL COMMITS" in svg


def test_every_hybrid_renders_valid_svg():
    """Force-render all 36 hybrids + 10 pure species at all 3 stages."""
    from ocean import creatures
    for pair, (name, base, overlay) in sp.HYBRIDS.items():
        for stage in (1, 2, 3):
            frag = creatures.render_creature(100, 100, base, overlay, stage,
                                             40, "repo", name)
            ET.fromstring(f'<svg xmlns="http://www.w3.org/2000/svg">{frag}</svg>')
    for cat in sp.PURE_SPECIES:
        for stage in (1, 2, 3):
            frag = creatures.render_creature(100, 100, cat, None, stage,
                                             40, "repo", "x")
            ET.fromstring(f'<svg xmlns="http://www.w3.org/2000/svg">{frag}</svg>')
