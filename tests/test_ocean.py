import datetime as dt
import xml.etree.ElementTree as ET

from ocean import creatures, detect, scene, tiers
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


def test_repo_tier_boundaries():
    assert tiers.repo_tier(0) == (1, "Abyssal Fry")
    assert tiers.repo_tier(15)[0] == 1
    assert tiers.repo_tier(16)[0] == 2
    assert tiers.repo_tier(80)[0] == 3
    assert tiers.repo_tier(81)[0] == 4
    assert tiers.repo_tier(600)[0] == 7
    assert tiers.repo_tier(601)[0] == 8
    assert tiers.repo_tier(1001) == (10, "Mythic Leviathan")


def test_repo_ladder_has_ten_distinct_creatures():
    assert len(tiers.REPO_TIERS) == 10
    names = {entry[2] for entry in tiers.REPO_TIERS}
    assert len(names) == 10
    assert set(creatures.RENDER) == set(range(1, 11))


# ---------------------------------------------------------------- detect

def test_package_json_deps():
    deps = detect.deps_from_package_json('{"dependencies": {"React": "^18", "next": "14"}}')
    assert deps == {"react", "next"}


def test_requirements_deps():
    deps = detect.deps_from_requirements("torch==2.1\n# comment\nflask[async]>=3\n")
    assert deps == {"torch", "flask"}


def test_detected_techs_filters_and_orders():
    langs, tools = detect.detected_techs(
        {"Python": 9000, "JavaScript": 1000, "Markdown": 500},
        {"torch", "react", "not-a-known-dep"},
    )
    assert langs == ["Python", "JavaScript"]
    assert tools == ["react", "torch"]


# ---------------------------------------------------------------- creatures

def test_every_evolution_tier_renders_valid_svg():
    for tier in range(1, 11):
        frag = creatures.render_creature(100, 100, tier, "repo", "sub text")
        ET.fromstring(f'<svg xmlns="http://www.w3.org/2000/svg">{frag}</svg>')


def test_creature_patrol_animation_present():
    frag = creatures.render_creature(0, 0, 5, "x", "y", patrol="patrolL", duration=11.5)
    assert 'class="patrolL"' in frag
    assert "animation-duration:11.5s" in frag


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


def test_scene_renders_valid_xml_for_every_repo_tier():
    state = _fixture_state()
    for commits in (0, 20, 60, 100, 200, 300, 500, 700, 900, 2000):
        state.repos[0].commits = commits
        root = ET.fromstring(scene.build_svg(state))
        assert root.tag.endswith("svg")


def test_scene_contains_repo_labels_and_cockpit():
    svg = scene.build_svg(_fixture_state())
    assert "ml-thing" in svg and "webapp" in svg and "dusty" in svg
    assert "CORAL HUNTER" in svg      # 120 commits -> tier 4
    assert "ABYSSAL FRY" in svg       # 8 commits -> tier 1
    assert "DSV JAIN PRASAD ALBER" in svg
    assert "183 TOTAL COMMITS" in svg


def test_scene_has_horizontal_patrol_keyframes():
    svg = scene.build_svg(_fixture_state())
    assert "@keyframes patrolM" in svg and "translateX" in svg
    assert "dswim" in svg             # the dragon patrols too
