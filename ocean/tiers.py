"""Tier math: dragon evolution (10 tiers) and per-repo creature stages (3)."""

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


def dragon_tier(total_commits: int) -> tuple[int, str, str]:
    """Return (tier, tier_name, depth_zone) for a total commit count."""
    tier = DRAGON_TIERS[0]
    for entry in DRAGON_TIERS:
        if total_commits >= entry[0]:
            tier = entry
    return tier[1], tier[2], tier[3]


def creature_stage(repo_commits: int) -> int:
    """Per-repo species stage: 1 (0-30), 2 (31-100), 3 (100+)."""
    if repo_commits > 100:
        return 3
    if repo_commits > 30:
        return 2
    return 1
