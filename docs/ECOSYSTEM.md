# The Living Deep — Ecosystem Field Guide

How the ocean reads the profile and decides what swims there.

## The Evolution Ladder (per repo, by that repo's commit count)

Every repository climbs the same ladder. No species, no hybrids — just
growth: each tier is a distinct creature, and the progression tells the
story of a repo growing from a larval speck into a deity of the deep.

| Tier | Commits | Creature | The form |
|---|---|---|---|
| 1 | 0–15 | **Abyssal Fry** | tiny translucent larva, ghostly pale, all eye and tail filament |
| 2 | 16–40 | **Reef Guppy** | basic form gained — small swift fish, one clean colour |
| 3 | 41–80 | **Neon Tang** | disc body, razor neon fins glowing emerald, clearly structured |
| 4 | 81–150 | **Coral Hunter** | angular triggerfish, gold war-paint diagonals, confident |
| 5 | 151–250 | **Electric Eel** | long sinuous body, bioluminescent currents chasing along it |
| 6 | 251–400 | **Barracuda Build** | streamlined torpedo with an underbite, built for speed |
| 7 | 401–600 | **Deep-Sea Angler** | needle teeth, observability lure burning on its forehead |
| 8 | 601–800 | **Apex Mako** | high-velocity shark, pressure wake peeling off behind it |
| 9 | 801–1000 | **Shadow Kraken** | eight tentacles, emerald eyes — it manages this depth layer |
| 10 | 1000+ | **Mythic Leviathan** | ancient armored deity in indigo and emerald, absolute presence |

Repos are placed by recency: newest near the surface, oldest brushing
the seafloor. Each creature patrols its depth lane horizontally at its
own speed and phase.

## The Dragon (profile-wide, total commits)

| Tier | Commits | Form | Zone |
|---|---|---|---|
| 1 | 0–15 | Sea Serpent Hatchling — thin pale white-blue, ghostly | Sunlit |
| 2 | 16–40 | River Snake — faint scales, dim blue tint | Sunlit |
| 3 | 41–80 | Deep Eel — spine fins emerge, soft teal glow | Twilight |
| 4 | 81–150 | Scaled Wyrm — proper scales, horn nubs, indigo emerging | Twilight |
| 5 | 151–250 | Sea Wyrm — whiskers, claw fins, bioluminescent underbelly | Midnight |
| 6 | 251–400 | Ocean Drake — antlers, four limbs, glowing blue eyes | Midnight |
| 7 | 401–600 | Abyssal Drake — flowing fin mane, glowing spine ridges | Abyssal |
| 8 | 601–800 | Ancient Lung — full eastern dragon, pearl under chin | Abyssal |
| 9 | 801–1000 | Sovereign of Depths — crown antlers, every scale glowing | Hadal |
| 10 | 1000+ | Primordial Shenlong — emerald and gold biolume, the ocean bends around it | Hadal |

## Jellyfish (tech stack)

Max 6 languages + 8 tools, one compact strip. Freshness = days since any
repo containing the tech was pushed: **<30d** bright and high ·
**30–90d** dimmer, a step lower · **90+d** faded silhouettes.

## Serving

GitHub freezes CSS animation on repo-hosted SVGs, so `ocean-sync`
publishes the scene to the `ocean-asset` repo; Vercel redeploys on every
push and the profile README embeds the Vercel URL — everything swims.
