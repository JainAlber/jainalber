"""Tier math: dragon evolution (profile-wide) and per-repo creature
evolution — both climb the same 10-step commit ladder."""

DRAGON_TIERS = [
    # (min_commits, tier, name, depth_zone)
    (0,    1,  "Sea Serpent Hatchling",  "Sunlit Zone"),
    (16,   2,  "River Snake",            "Sunlit Zone"),
    (41,   3,  "Deep Eel",               "Twilight Zone"),
    (81,   4,  "Scaled Wyrm",            "Twilight Zone"),
    (151,  5,  "Sea Wyrm",               "Midnight Zone"),
    (251,  6,  "Ocean Drake",            "Midnight Zone"),
    (401,  7,  "Abyssal Drake",          "Abyssal Zone"),
    (601,  8,  "Ancient Lung",           "Abyssal Zone"),
    (801,  9,  "Sovereign of Depths",    "Hadal Zone"),
    (1001, 10, "Primordial Shenlong",    "Hadal Zone"),
]

REPO_TIERS = [
    # (min_commits, tier, name)
    (0,    1,  "Abyssal Fry"),
    (16,   2,  "Reef Guppy"),
    (41,   3,  "Neon Tang"),
    (81,   4,  "Coral Hunter"),
    (151,  5,  "Electric Eel"),
    (251,  6,  "Barracuda Build"),
    (401,  7,  "Deep-Sea Angler"),
    (601,  8,  "Apex Mako"),
    (801,  9,  "Shadow Kraken"),
    (1001, 10, "Mythic Leviathan"),
]


def dragon_tier(total_commits: int) -> tuple[int, str, str]:
    """Return (tier, tier_name, depth_zone) for a total commit count."""
    tier = DRAGON_TIERS[0]
    for entry in DRAGON_TIERS:
        if total_commits >= entry[0]:
            tier = entry
    return tier[1], tier[2], tier[3]


def repo_tier(repo_commits: int) -> tuple[int, str]:
    """Return (tier, creature_name) for a single repo's commit count."""
    tier = REPO_TIERS[0]
    for entry in REPO_TIERS:
        if repo_commits >= entry[0]:
            tier = entry
    return tier[1], tier[2]
