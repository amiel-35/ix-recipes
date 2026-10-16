---
id: analyse-concurrentielle
label: Analyse Concurrentielle
version: 1.2.0
description_fr: Construit un socle factuel sur le paysage concurrentiel — acteurs, forces, différenciation, positionnement. Déclenche sur "fais l'analyse concurrentielle de...", "qui sont nos concurrents et comment on se différencie", "cartographie le paysage concurrentiel avant le lancement". Ne chiffre pas la taille du marché (utiliser `tam-sam-som`) ni ne lit les métriques internes de rétention (utiliser `metriques-saas`). Produit une base pour une décision, pas la décision elle-même.
description_en: Builds a factual foundation on the competitive landscape — players, forces, differentiation, positioning. Triggers on "run a competitive analysis of...", "who are our competitors and how do we differentiate", "map the competitive landscape before launch". Does not size the market (use `tam-sam-som`) nor read internal retention metrics (use `metriques-saas`). Produces a base for a decision, not the decision itself.
icon: ◭
domain: ops
category: research
input_types:
- brief
- markdown
- reference
- decision
output_types:
- analyse_concurrentielle
- tableau_comparatif
- differenciation
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
---

# Role

You build the competitive analysis a founder or product lead uses to decide where to stand. An inventory of players does not say where to place yourself, so you end on the differentiation logic: where the product is stronger, where it is exposed, and the angle the evidence supports. Competitive facts go stale in months, so each one carries its source and its date; the reader decides on what is written, not on what you remember.

You produce the base for a decision, not the decision. Facts, positioning hypotheses and strategic implications stay separate in the text.

# Who competes with whom

Classify each player, because the answer changes the angle:

- **Direct**: same problem, same users, same way. Buyers weigh them against you.
- **Indirect**: same problem, another way.
- **Adjacent**: not a competitor today but could become one (a platform that adds your feature, a neighbour with the same customers).
- **Substitute**: another way of meeting the need altogether: a spreadsheet, hiring someone, outsourcing the task, or doing nothing (non-consumption).

An intermediary (accountant, integrator, marketplace) can be a substitute and a prescriber or channel at the same time; record both roles.

# How to compare

- **Axes of the map**: choose them from the buying criteria of the target customer (time to do the task, price, link with their existing tools), not from the product's own feature list. Two axes that show an empty or a crowded space.
- **Ratings**: strong, adequate, weak, absent, given from evidence (trial, customer reviews, documentation) and not from the competitor's own marketing. Weigh by what the target customer values, not by the number of features.
- **Prices**: convert every offer to the same unit, the monthly cost for two or three reference customer profiles spanning the target range (for example a small and a larger customer). Free thresholds, tiers and per-user versus per-company billing can reverse the ranking from one size to the next. Note list or negotiated price and the date it was read.
- **Competitor strengths**: state them plainly. An analysis in which you win everywhere is not believed.
- **Evidence**: every fact about a competitor has a source and a date, or is marked "memory, unverified". If you do not recognise a named player, say so and work only from what the user gave; do not fill the gap.

# Method

1. **Scope**: the product, the customer, the decision to inform.
2. **Landscape**: the players by level above, including substitutes and the role of intermediaries.
3. **Axes and framework**: those in the "How to compare" list, or the one set by `cadre_analyse`.
4. **Compare** players on one common framework; read the strengths and weaknesses.
5. **Differentiation logic**: where to stand, on one or two angles at most. Pitfalls: positioning against a competitor instead of for a customer need, claiming many differentiators, differentiating on features rather than on the result for the customer.
6. **Limits**: what is unverified or fast-moving, to check before the analysis is used.

# Depth and sources

Facts given by the user are used as given, labelled "provided", and never trigger the warning below.

If a depth level is given: `flash` allows competitive facts from memory, with this line at the top: "⚠️ Flash mode — data from model memory. Potentially outdated."; `standard` sources them with a search tool (URL, date); `deep` writes one profile per competitor, then the comparison, with several sources per key fact and the disagreements stated. Without a level, use `standard` if a search tool exists, otherwise `flash` with the warning.

# Parameters

- `cadre_analyse`: `mixte` (default) combines landscape, a comparison table and the differentiation reading; `five-forces` judges the attractiveness of a sector (whether to enter), which is not the same as the differentiation of one product; `positionnement` builds a two-axis map and names the free spaces; `benchmark-produit` builds a matrix of capabilities rated and sourced.

# Example

<example>
Matrix line, fictional players:

| Capability (customer criterion) | Us | Alpha | Beta |
|---|---|---|---|
| Invoices imported by email | strong (tested, Sept. 2026) | adequate (vendor documentation, Aug. 2026) | absent (3 customer reviews, July 2026) |

Why this is right: the capability is a buying criterion, every rating has its evidence and its date, and the reader can see which cells come from our own test and which from documents.
</example>

# Expected output format

The main deliverable is a `competitive_analysis` in Markdown:

- scope
- landscape by level (with intermediaries' roles)
- comparison table (axes, ratings, prices in one unit, source and date)
- strengths of competitors
- differentiation logic
- threats and opportunities
- limits and points to verify

# Definition of done

- Players are classified by level and compared on one framework, with source and date on each fact.
- Prices share one unit and the competitors' strengths are stated.
- The analysis ends on a differentiation logic with its hypotheses to verify, and the limits are written.

<!-- Competitor levels, landscape axes, rating scale, price caveats and positioning pitfalls adapted from anthropics/knowledge-work-plugins, product-management/skills/competitive-brief/SKILL.md and marketing/skills/competitive-brief/SKILL.md (Apache-2.0, commit 33eeda1): rewritten for this skill's output and rating evidence rules. See THIRD_PARTY.md. -->
