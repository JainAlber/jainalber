# The Living Deep — Ecosystem Field Guide

How the ocean reads a repository and decides what swims there.

## Resolution Rules

A repo's tech categories are scored from language bytes (60%), recognized
dependencies (40%), and a DevOps bonus for Dockerfiles.

| Condition | Result |
|---|---|
| One category ≥ 60% of total score | Pure species |
| Top two categories each ≥ 30% | Hybrid (larger share = body, smaller = trait) |
| Anything else | Reef Shark |

Per-repo evolution stages: **1** (0–30 commits) · **2** (31–100) · **3** (100+).

## The 10 Pure Species

| Category | Species | Signature trait it lends to hybrids |
|---|---|---|
| Python | Sea Krait | black/white banding |
| JS/TS | Yellowfin Tuna | yellow fins + speed streaks |
| AI/ML | Manta Ray | neural circuit bioluminescence |
| DevOps/Infra | Mantis Shrimp | rainbow segmented armor |
| Frontend/UI | Lionfish | flowing venomous fin plumes, glowing tips |
| CLI/Tools | Moray Eel | jet-black skin, emerald spots |
| Data/Analytics | Anglerfish | blazing teal lure |
| Mobile | Flying Fish | iridescent glide wings |
| Docs/Misc | Nautilus | golden-ratio spiral glow |
| Multi-language | Reef Shark | — (apex fallback) |

## The 36 Hybrids

Body = the parent whose anatomy carries the creature; trait = the other
parent's signature, layered over it.

| Parents | Hybrid | Body | Trait | The creature |
|---|---|---|---|---|
| Python × JS | **Bandtail Barracuda** | Tuna | bands | torpedo speedster wearing krait war-paint down its tail |
| Python × AI | **Veiled Naga Ray** | Manta | bands | serpent-marked wings, neural glow flickering between the bands |
| Python × DevOps | **Pistol Krait** | Krait | armor | banded serpent with rainbow carapace plates at the neck |
| Python × Frontend | **Silk-Finned Serpent** | Krait | plumes | a sea snake trailing a lionfish's silk fan, glowing at every tip |
| Python × CLI | **Shadow Krait** | Krait | spots | bands fading into jet black, emerald spots where light dies |
| Python × Data | **Lantern Asp** | Krait | lure | a serpent that carries its own abyssal lamp above its brow |
| Python × Mobile | **Glidewing Krait** | Krait | wings | iridescent wings mid-coil; leaps between depth layers |
| Python × Docs | **Scribe Serpent** | Krait | spiral | a golden spiral glows along its coil, like marginalia |
| JS × AI | **Circuit Sailfin** | Tuna | circuits | speed and inference; circuitry tracing the lateral line |
| JS × DevOps | **Gauntlet Tuna** | Tuna | armor | rainbow-plated forehead, built to ram pipelines through |
| JS × Frontend | **Regal Firetail** | Tuna | plumes | the fastest beautiful thing in the water |
| JS × CLI | **Nightrunner Eel** | Moray | streaks | a lurker that bolts — gold streaks in the dark |
| JS × Data | **Beacon Darter** | Tuna | lure | headlamp tuna, illuminating its own speed |
| JS × Mobile | **Skipjack Skimmer** | Tuna | wings | perpetually breaching, silver-blue and gold |
| JS × Docs | **Chambered Charger** | Tuna | spiral | a golden spiral etched on the flank like a service record |
| AI × DevOps | **Forgeback Ray** | Manta | armor | wings plated with rainbow segments; the foundry glider |
| AI × Frontend | **Plume Ray** | Manta | plumes | wingtips fraying into venomous silk |
| AI × CLI | **Abyss Glider** | Manta | spots | dark wings, green constellation, mid-depth silence |
| AI × Data | **Oracle Ray** | Manta | lure | the all-seeing one: a lure feeding light into its circuits |
| AI × Mobile | **Stratos Ray** | Manta | wings | wings over wings; it has somewhere to be |
| AI × Docs | **Archivist Ray** | Manta | spiral | a golden ratio glowing across its back, stately glide |
| DevOps × Frontend | **Harlequin Duelist** | Mantis | plumes | armored shrimp fanning lionfish silks from its carapace |
| DevOps × CLI | **Trench Reaver** | Mantis | spots | black armor, green spots, claws in the dark |
| DevOps × Data | **Forge Lantern** | Mantis | lure | a miner's headlamp on rainbow armor |
| DevOps × Mobile | **Rocket Prawn** | Mantis | wings | launches between depths, segments streaking like boosters |
| DevOps × Docs | **Keeper of the Shell** | Mantis | spiral | hermit mantis guarding a glowing spiral home |
| Frontend × CLI | **Duskfire Eel** | Moray | plumes | a moray wearing a fin mane that glows as it fades aft |
| Frontend × Data | **Gala Angler** | Angler | plumes | nightmare jaw under gorgeous plumage — beauty and horror |
| Frontend × Mobile | **Aurora Skimmer** | Flying Fish | plumes | striped silk wings drawing light trails when it leaps |
| Frontend × Docs | **Ornate Whorl** | Nautilus | plumes | fin rays fanning from the shell aperture like a crown |
| CLI × Data | **Pit Lantern** | Moray | lure | only the lure, the spots and two eyes are visible. good luck |
| CLI × Mobile | **Riftwing Eel** | Moray | wings | a black eel that flies; wrong on every level, gloriously |
| CLI × Docs | **Hollow Whisperer** | Moray | spiral | coiled through shell chambers, amber-green glow inside |
| Data × Mobile | **Comet Angler** | Angler | wings | its lure streams behind it like a comet tail between layers |
| Data × Docs | **Lore Lantern** | Nautilus | lure | a teal lamp extending from an amber shell; the library light |
| Mobile × Docs | **Spiral Skimmer** | Flying Fish | spiral | golden spiral patterning across iridescent wings |

## The Dragon (profile-wide, total commits)

| Tier | Commits | Form | Zone |
|---|---|---|---|
| 1 | 0–15 | Sea Serpent Hatchling | Sunlit |
| 2 | 16–40 | River Snake | Sunlit |
| 3 | 41–80 | Deep Eel | Twilight |
| 4 | 81–150 | Scaled Wyrm | Twilight |
| 5 | 151–250 | Sea Wyrm | Midnight |
| 6 | 251–400 | Ocean Drake | Midnight |
| 7 | 401–600 | Abyssal Drake | Abyssal |
| 8 | 601–800 | Ancient Lung | Abyssal |
| 9 | 801–1000 | Sovereign of Depths | Hadal |
| 10 | 1000+ | Primordial Shenlong | Hadal |

## Jellyfish (tech stack)

Max 6 languages + 8 tools. Freshness = days since any repo containing the
tech was pushed: **<30d** bright near surface · **30–90d** dim mid-depth ·
**90+d** faded silhouettes in the deep.
