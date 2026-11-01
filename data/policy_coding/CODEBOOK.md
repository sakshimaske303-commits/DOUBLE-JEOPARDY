# Coastal policy coding: codebook

The unit is the jurisdiction that sets coastal building rules for each island group: Spain and, since 2023, the Canary Islands government (Canary Islands); the Government of India and the Union Territory administration (Lakshadweep); and the national governments of Seychelles, the Maldives and Fiji. Coding reflects rules in force in October 2026.

Files:

- `coastal_policy_coding.csv`: one row per jurisdiction and item, with the value, legal basis, source and verification level.
- `coastal_policy_timeline.csv`: dated changes to coastal and environmental rules, one row per change.

## Policy density (count of instruments, 0-6)

Density is the number of instrument types in force, following the distinction between policy density and policy intensity in Knill, Schulze and Tosun (2012). Each item is 1 if found in force and 0 if not found.

| Item | Coded 1 when | NATO type (Hood 1983) |
|---|---|---|
| D1_building_setback | a statutory minimum building distance from the shoreline applies to inhabited land | Authority |
| D2_statutory_coastal_zones | the law divides the coast into zones with different rules | Authority |
| D3_eia_law | an environmental impact assessment law covers coastal projects | Authority |
| D4_coastal_plan | a national coastal management or adaptation plan exists, binding or not | Nodality / Organisation |
| D5_dedicated_coastal_authority | a body with a coast-specific mandate administers the rules | Organisation |
| D6_climate_law_coastal | a climate framework law is in force | Authority |

## Policy intensity (setback stringency, 0-1)

Intensity measures how demanding the one instrument that decides where people may build is. Two items are coded in metres:

- `I1_setback_inhabited_m`: setback on land that is already built up or classified urban.
- `I2_setback_general_m`: setback on other coastal land.

Intensity = mean(I1, I2) / 100, using Spain's 100 m easement, the widest in the sample, as the reference. Jurisdictions without a setback score 0.

## Timeline direction

| Code | Meaning |
|---|---|
| expansion | a new instrument, or an existing one made stricter |
| dismantling | an instrument removed, relaxed or exempted (Bauer et al. 2012) |
| reallocation | competence moved between levels of government |
| reform | rules rewritten without a clear direction for coastal building |
| implementation | an implementing regulation without a substantive change |

## Verification levels

| Level | Meaning |
|---|---|
| primary | read in the official legal text |
| official | an official summary (FAOLEX/LEAP, ministry, gazette index) |
| secondary | a law-firm note, civil society statement or encyclopaedia |
| not_found | searched for and not found; coded 0 |

"Not found" is not proof of absence. The coding covers instruments that bear on building near the shore, not each country's whole environmental law.
