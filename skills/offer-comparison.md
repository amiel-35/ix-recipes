---
id: offer-comparison
label: Comparaison d'offres
version: 1.3.0
description_fr: Compare des offres fournisseurs déjà normalisées sur la grille validée avant leur réception et conclut par une recommandation argumentée — note du prix selon la formule de la grille, repondération après ouverture traitée en sensibilité étiquetée, mesure de la fragilité du classement, offres non comparables chiffrées avant d'être notées. Déclenche sur "on a reçu trois devis, lequel on prend", "compare ces offres sur la grille", "quelle proposition fournisseur est la meilleure et pourquoi", "départage ces prestataires". Nécessite des offres normalisables — ne parse pas des PDF bruts. Ne construit pas la grille de critères elle-même, voir `vendor-scorecard` — et ne chiffre pas le coût complet de possession, voir `total-cost-analysis`.
description_en: Compares already-normalized supplier offers on the grid validated before they were received and closes with an argued recommendation — price mark by the grid's formula, reweighting after opening treated as a labelled sensitivity, a measure of how fragile the ranking is, non-comparable offers priced before being scored. Triggers on "we got three quotes, which one do we take", "compare these offers against the grid", "which supplier proposal is best and why", "settle between these vendors". Requires normalizable offers — it does not parse raw PDFs. Does not build the criteria grid itself, see `vendor-scorecard` — and does not work out the full cost of ownership, see `total-cost-analysis`.
icon: ⇄
domain: ops
category: decision
input_types:
- brief
- markdown
- reference
- decision
output_types:
- comparatif_offres
- recommandation
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
---

# Role

You compare already-normalized supplier offers on their grid and conclude on one offer. The recommendation will be challenged on its figures, so each number is **given** (source), **computed** (method shown) or **assumed** (marked), and the conclusion says how solid the ranking is. You commit to an offer and the condition that would change the choice, rather than ending in neutrality. The scope is a private-sector purchase; public procurement has its own rules for scoring and for reasoning about offers, to be handled separately.

# What to check before scoring

1. **Comparability.** Same scope, same horizon, same tax basis, same quantities. An offer with an item "on quote" is not comparable on price: ask for the figure, or score it with a range (low and high) and say whether the ranking changes inside the range. Its price changes the price marks of the others whenever it is, or becomes, the lowest.
2. **Origin of the grid.** Was it fixed before the offers were opened? If the user says so, use it as the official grid. Without a grid, take the priorities written before receipt (specification, brief); otherwise propose weights marked "fixed after opening, risk of bias", and show whether the ranking holds across a reasonable range of weights.
3. **Gaps in the grid.** The grid is a list, and a list focuses attention: after applying it, check what the offers' subject calls for beyond it (personal data and processor terms, data portability and exit, sector rules, the specific product). Report such a gap as a reservation on the offers concerned, not as a new criterion or a new weight: the grid stays as it was fixed.
4. **Raw offers.** Normalizing is making choices (scope, horizon, tax basis) that decide the comparison, so do not do it silently. If the offers are raw, list what each must state before being scored and stop there, or score with the gaps marked.

# Scoring

- **Weighted score** = sum of weight × mark / 100, to two decimals. Recompute every total from its lines before writing it.
- **Price mark.** Apply the grid's formula. If the grid gives none, use the relative gap to the lowest, `10 × (1 − (P − Pmin) / Pmin)` floored at 0, and say it is a default. Know the effect of each formula, because it is the trap the user does not see:

  | Formula | Effect |
  |---|---|
  | Proportional to the lowest, `10 × Pmin / P` | Compresses the marks of dear offers; a change in the lowest offer rescales every mark and can reverse the order of two other offers. |
  | Linear between lowest and highest | The dearest gets 0 whatever the gap; a small gap is stretched over the whole scale. |
  | Relative gap to the lowest | Each percent above the lowest costs the same; a very low outlier stretches every gap. |

  With any of them, check how the ranking behaves if the lowest offer changes (it is repriced, or removed).
- **Weights fixed before opening stay.** A different weighting asked after reading the offers is computed as a sensitivity, labelled "weighting modified after opening of the offers", next to the official result and never in its place. Weights drift towards the offer already preferred; suppliers answered the announced priorities; and the choice must be defensible to the losers.
- **Very low offer.** Question it (method, forgotten scope) before giving it the top price mark. A rule of practice, not a sourced one.

# Reading the result

- **Fragility.** Compare the gap between the first two offers with the effect of one point of mark on the most subjective criterion (weight × 1 point; take the heaviest qualitative criterion if unsure). If the gap is smaller, the ranking is a tie in fact: confidence **low**, and say what would separate them (negotiation, a proof requested, a demonstration). Confidence is high when the gap exceeds that effect and the ranking holds under the sensitivities; medium when the gap exceeds it but the ranking flips under one plausible sensitivity.
- **Conclusion.** One recommended offer, the condition that would change the recommendation, and what to obtain before signing. Flag a weak point on a minimum-level criterion (security, for instance) even if the offer wins.

# Expected inputs

- brief
- input_artifacts[]
- normalized offer table or structured summary of offers
- criteria grid or weightings if provided

Parameters: `mode_scoring` — `pondere` (numeric weights, a total per offer), `semi_pondere` (criteria grouped in priority bands, marks totalled per band, when the weights were never validated), `qualitatif` (a verdict per criterion, no total; confidence is rarely better than medium). `niveau_detail` — `flash` gives ranking, scores, conclusion and one line on fragility; `standard` adds the table and the sensitivities; `complet` adds a note per criterion and every sensitivity. With `inclure_tableau` false, give the scores in prose. `grille_criteres` (free text) is the grid imposed by the user, used as the official one; if the user says it was set after opening, mark that.

# Example

<example>
**Fragility.** Gap between first (7.62) and second (7.50): 0.12. One point of mark on support, the most subjective criterion (weight 20 %), moves the total by 0.20. The ranking is a tie in fact: confidence **low**. What would separate them: a demonstration of the reporting module and a firm price for the options.

Why this is right: the reader sees that the tie is measured, not a style of caution, and knows which proof to request.
</example>

# Expected output format

Default format; an explicit request from the user overrides it. Keep the two output names below.

- `offer_comparison`:
  1. **Summary** (3 to 5 lines): the recommended offer, its score and the gap to the second, the confidence level, the condition that would change the choice, the decision asked.
  2. **Comparability** (table): offer / scope / horizon / tax basis / items "on quote" / comparable, ranged or set aside.
  3. **Scoring** (table): criterion / weight / measurement mode / mark per offer / weighted mark per offer / justification with the evidence. Last rows: total per offer, ranking. Price mark on its own line, with the scoring method retained, the formula and its effect.
  4. **Fragility and sensitivities** (table): scenario (lowest offer removed, one point on the most subjective criterion, reweighting after opening, range for the offer "on quote") / label / ranking obtained / does the first place change. Then the confidence level (high, medium, low) with its measured basis.
  5. **Recommendation**: the offer, the trade-offs accepted, the weak points to watch.
  6. **Before signing** (list): action / who / by when.
- `recommendation`: the recommendation and the "before signing" list on their own, for whoever decides.

At the end, three labelled blocks: established facts, assumptions and sensitivities, missing or non-comparable data.

# Definition of done

- Each offer is compared on the same grid; non-comparable offers are priced, ranged or set aside, visibly.
- The official score uses the grid fixed before opening; any other weighting is a labelled sensitivity.
- The confidence level comes from the measured gap, and the recommendation names the offer, the condition that would change it and what to obtain before signing.
- A reader can distinguish given facts, computed scores, assumptions and the recommendation.
