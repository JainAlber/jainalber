"""Species registry: 10 pure species, 36 hybrids, and resolution rules.

Pure species map 1:1 to tech categories. A hybrid is rendered as the
*base* parent's body carrying the *overlay* parent's signature trait,
so every combination stays visually legible at small sizes.
"""

# Tech category keys
PYTHON = "python"
JS = "js"
AI = "ai"
DEVOPS = "devops"
FRONTEND = "frontend"
CLI = "cli"
DATA = "data"
MOBILE = "mobile"
DOCS = "docs"
MULTI = "multi"

CATEGORIES = [PYTHON, JS, AI, DEVOPS, FRONTEND, CLI, DATA, MOBILE, DOCS]

PURE_SPECIES = {
    PYTHON:   "Sea Krait",
    JS:       "Yellowfin Tuna",
    AI:       "Manta Ray",
    DEVOPS:   "Mantis Shrimp",
    FRONTEND: "Lionfish",
    CLI:      "Moray Eel",
    DATA:     "Anglerfish",
    MOBILE:   "Flying Fish",
    DOCS:     "Nautilus",
    MULTI:    "Reef Shark",
}

# Signature trait each species can lend to a hybrid (see creatures.py overlays)
TRAITS = {
    PYTHON:   "bands",       # black/white krait banding
    JS:       "streaks",     # yellow fins + motion streaks
    AI:       "circuits",    # neural circuit bioluminescence
    DEVOPS:   "armor",       # rainbow segmented carapace
    FRONTEND: "plumes",      # flowing venomous fin rays, glowing tips
    CLI:      "spots",       # jet-black skin, green biolum spots
    DATA:     "lure",        # blazing teal angler lure
    MOBILE:   "wings",       # iridescent glide wings
    DOCS:     "spiral",      # golden-ratio shell glow
}

# 36 hybrids. Key: frozenset of the two categories.
# Value: (display name, base-body category, overlay-trait category)
HYBRIDS = {
    frozenset({PYTHON, JS}):       ("Bandtail Barracuda", JS, PYTHON),
    frozenset({PYTHON, AI}):       ("Veiled Naga Ray", AI, PYTHON),
    frozenset({PYTHON, DEVOPS}):   ("Pistol Krait", PYTHON, DEVOPS),
    frozenset({PYTHON, FRONTEND}): ("Silk-Finned Serpent", PYTHON, FRONTEND),
    frozenset({PYTHON, CLI}):      ("Shadow Krait", PYTHON, CLI),
    frozenset({PYTHON, DATA}):     ("Lantern Asp", PYTHON, DATA),
    frozenset({PYTHON, MOBILE}):   ("Glidewing Krait", PYTHON, MOBILE),
    frozenset({PYTHON, DOCS}):     ("Scribe Serpent", PYTHON, DOCS),
    frozenset({JS, AI}):           ("Circuit Sailfin", JS, AI),
    frozenset({JS, DEVOPS}):       ("Gauntlet Tuna", JS, DEVOPS),
    frozenset({JS, FRONTEND}):     ("Regal Firetail", JS, FRONTEND),
    frozenset({JS, CLI}):          ("Nightrunner Eel", CLI, JS),
    frozenset({JS, DATA}):         ("Beacon Darter", JS, DATA),
    frozenset({JS, MOBILE}):       ("Skipjack Skimmer", JS, MOBILE),
    frozenset({JS, DOCS}):         ("Chambered Charger", JS, DOCS),
    frozenset({AI, DEVOPS}):       ("Forgeback Ray", AI, DEVOPS),
    frozenset({AI, FRONTEND}):     ("Plume Ray", AI, FRONTEND),
    frozenset({AI, CLI}):          ("Abyss Glider", AI, CLI),
    frozenset({AI, DATA}):         ("Oracle Ray", AI, DATA),
    frozenset({AI, MOBILE}):       ("Stratos Ray", AI, MOBILE),
    frozenset({AI, DOCS}):         ("Archivist Ray", AI, DOCS),
    frozenset({DEVOPS, FRONTEND}): ("Harlequin Duelist", DEVOPS, FRONTEND),
    frozenset({DEVOPS, CLI}):      ("Trench Reaver", DEVOPS, CLI),
    frozenset({DEVOPS, DATA}):     ("Forge Lantern", DEVOPS, DATA),
    frozenset({DEVOPS, MOBILE}):   ("Rocket Prawn", DEVOPS, MOBILE),
    frozenset({DEVOPS, DOCS}):     ("Keeper of the Shell", DEVOPS, DOCS),
    frozenset({FRONTEND, CLI}):    ("Duskfire Eel", CLI, FRONTEND),
    frozenset({FRONTEND, DATA}):   ("Gala Angler", DATA, FRONTEND),
    frozenset({FRONTEND, MOBILE}): ("Aurora Skimmer", MOBILE, FRONTEND),
    frozenset({FRONTEND, DOCS}):   ("Ornate Whorl", DOCS, FRONTEND),
    frozenset({CLI, DATA}):        ("Pit Lantern", CLI, DATA),
    frozenset({CLI, MOBILE}):      ("Riftwing Eel", CLI, MOBILE),
    frozenset({CLI, DOCS}):        ("Hollow Whisperer", CLI, DOCS),
    frozenset({DATA, MOBILE}):     ("Comet Angler", DATA, MOBILE),
    frozenset({DATA, DOCS}):       ("Lore Lantern", DOCS, DATA),
    frozenset({MOBILE, DOCS}):     ("Spiral Skimmer", MOBILE, DOCS),
}


def resolve_species(scores: dict[str, float]) -> tuple[str, str, str | None]:
    """Resolve category scores into a creature.

    Returns (display_name, base_category, overlay_category_or_None).

    Rules:
      - one category at >=60% of total -> pure species
      - top two categories both >=30%  -> hybrid
      - otherwise                      -> Reef Shark (multi-language)
    """
    total = sum(scores.values())
    if total <= 0:
        return PURE_SPECIES[MULTI], MULTI, None
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    top_cat, top_score = ranked[0]
    if top_score / total >= 0.6 or len(ranked) == 1:
        return PURE_SPECIES[top_cat], top_cat, None
    second_cat, second_score = ranked[1]
    if top_score / total >= 0.3 and second_score / total >= 0.3:
        name, base, overlay = HYBRIDS[frozenset({top_cat, second_cat})]
        return name, base, overlay
    return PURE_SPECIES[MULTI], MULTI, None
