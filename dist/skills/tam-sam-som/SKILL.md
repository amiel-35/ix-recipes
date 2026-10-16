---
name: tam-sam-som
description: "Estimates TAM, SAM, and SOM with top-down and bottom-up methods, explicit hypotheses, and owned reliability limits. Triggers on \"what's the size of the addressable market\", \"calculate TAM SAM SOM before the investor pitch\", \"size the market for this segment\", \"a market order of magnitude for the pitch\". Does not compare against competitors (use `analyse-concurrentielle`) and does not read internal retention metrics (use `metriques-saas`), a factual sizing base, not the strategy."
---
# Role

You build a TAM, SAM and SOM estimate that an investor or a board member can challenge factor by factor. They contest a factor (how many customers, at what price), not a total, so every figure shows the factors that produce it, and the uncertainty is a range with the factor that moves it.

# What makes this hard

- **Anchoring**: a top-down figure computed first pulls the bottom-up one toward it. Compute the bottom-up first.
- **Borrowed scope**: a published market report almost always covers a wider scope (whole software category, all of Europe, hardware included). Taking it as the TAM overstates the market.
- **Share as a plan**: "1 % of the market" is a wish, not an estimate. A SOM needs a reason: sales capacity or observed shares.
- **Mixed units**: annual recurring revenue against cumulative revenue, or different years.

# Definitions

Always in euros per year (recurring), with the reference year. The default positions below are venture practice, not a norm.

| Level | Meaning | Built from |
|---|---|---|
| TAM | Yearly spend on the need within the geography, if every possible customer bought | number of customers × annual price (or basket × frequency) |
| SAM | The part your model can serve: segments, geography, channel, technical or regulatory constraints | TAM minus what your offer cannot reach, each filter justified |
| SOM | What is realistic to capture by a dated horizon, given competition and sales capacity | capacity (below) or shares observed on comparable players |

# Method

1. **Define the scope**: need, geography, customer segment, horizon, year of reference.
2. **Bottom-up first**: target customers × annual price, every factor sourced or labelled as an assumption. This gives the TAM, then the SAM by filtering.
3. **Top-down second**: a published market figure × scope filters, each filter justified. Say how the report's scope differs from yours.
4. **Compare**: if the two estimates differ by more than a factor of about 2 (a proposed rule of thumb, not a sourced one), explain the gap by scope or by an assumption; do not average them.
5. **SOM by capacity**: salespeople × signatures per person per month × months, net of ramp-up time for new hires and of churn, × annual price; or a share compared with players actually observed. Show the ARR at the horizon.
6. **Check**: SOM ≤ SAM ≤ TAM; same unit and year throughout; SOM consistent with the commercial plan. Give a low and a high figure for each level, naming the factor that moves it.
7. **List what to verify** before the figures are quoted, with a public source to check each.

Public sources to propose for French markets: INSEE (Sirene establishment register, business statistics by size and sector), Eurostat (structural business statistics), and the statistics of professional orders or ministries for regulated sectors (for example DREES for health professions). Give the year of every figure.

# Depth and sources

Figures given by the user never need a search and never trigger the warning below: use them as given and label them "provided".

If a depth level is given: `flash` allows market figures from memory, with this line at the top of the deliverable: "⚠️ Flash mode — data from model memory. Potentially outdated."; `standard` sources market figures with a search tool (URL, date); `deep` uses several sources per key figure and states where they disagree. Without a level, use `standard` if a search tool exists, otherwise `flash` with the warning. Memory is not a source for market figures outside flash mode, because market data can be a year or more out of date.

# Parameters

- `methode_principale`: `mixte` (default) presents both estimates side by side; `top-down` or `bottom-up` makes that method the headline figure and the other the control. The bottom-up is still computed first, and the cross-check is still done when the data allows.

# Example

<example>
Illustrative figures, not real data. A planning tool for veterinary clinics in France:

12 000 target clinics (Sirene, activity code and size filter, 2025) × 90 €/month × 12 = 12 960 000 €/year, so a TAM of 13.0 M€/year. Filter: 55 % have no planning module they would keep (assumption, to check by survey) gives a SAM of 7.1 M€/year.

Why this is right: every factor has a source or a label, the unit is euros per year with the year, and the SAM filter is a stated assumption a reader can change.
</example>

# Expected output format

The main deliverable is a `tam_sam_som` in Markdown: scope, bottom-up, top-down, comparison of the two, TAM / SAM / SOM with ranges, hypotheses, limits, implications, points to verify.

# Definition of done

- Every figure shows its factors; units are euros per year with a reference year.
- The SOM rests on a capacity or an observed share, and SOM ≤ SAM ≤ TAM holds.
- The gap between the two methods is explained, the ranges name their driving factor, and the points to verify carry a source.
