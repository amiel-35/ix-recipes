---
name: vendor-scorecard
description: "Builds a vendor evaluation grid to be fixed before the offers are received \u2014 knockouts outside the weighting, weighted criteria with their reason, anchored scale, price-scoring formula and its effects \u2014 the scoring tool, not the final decision. Triggers on \"build the vendor scoring grid\", \"how will we score the offers we are going to receive\", \"grid to validate before sending the specification\", \"weighted grid to compare suppliers\". Does not score offers already received (use `offer-comparison`), does not draft the tender document sent to suppliers (use `rfp-draft`) nor the full cost breakdown (use `total-cost-analysis`)."
---
# Role

You build the scoring grid for a private-sector purchase before the offers arrive. Two readers will defend it: the business owner, who must explain the weights to management, and the procurement lead, who must justify the choice to a supplier that lost. So each weight carries what it reflects of the need, and the grid is fixed before any offer is read. Public procurement has its own rules for criteria, weighting and scoring, to be handled separately.

# What the grid must contain

1. **Knockouts outside the weighting.** Legal or vital requirements are yes / no conditions checked before any score: a weight would let a good score elsewhere offset a disqualifying gap. Typical ones:

   | Condition | When | Source (checked 2026-10-16) |
   |---|---|---|
   | Supplier can sign an article 28 processing contract | The supplier processes personal data for you | GDPR art. 28 |
   | Vigilance documents supplied (URSSAF attestation under 6 months, registration proof) | Contract of €5,000 excluding tax or more | C. trav. art. L8222-1, R8222-1, D8222-5 |
   | Ability to start on the required date | Always, if the date is fixed | — |
   | Legal requirement specific to the object | e.g. a payroll tool must produce the *déclaration sociale nominative* | CSS art. L133-5-3 |

   Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check".

2. **Dimensions by purchase type** (a default to adapt, not a standard):

   | Type | Dimensions |
   |---|---|
   | Software, SaaS | Functional coverage; integration (API, SSO, existing tools); security and data; reversibility (export, formats, help at the end); deployment support; support and service levels; vendor solidity; total cost |
   | Intellectual service | Understanding of the need; method; named team (and replacement rule); comparable references; planning; price |
   | Supplies | Technical conformity; price on quantities; delivery lead time and reliability; quality (non-conformities); warranty and after-sales; security of supply (single source); environmental impact |
   | Recurring labour-based service (cleaning, maintenance, managed IT) | Resources; service levels and penalties; transition and reversibility plan; social conditions (vigilance, staff takeover); price |

   When the purchase is critical, add concentration risk and business continuity.

   This table is a start, not the edge of the grid. Then check what the purchase's subject calls for beyond it (personal data and processor terms, data portability and exit, sector rules, the specific product or service) and add it as a knockout or a criterion now, while the grid is still open: a list focuses attention, and what it does not name gets missed.

3. **Weight of price**, a practitioner's default, unsourced, to give as adjustable: commodity purchase, price at 50 % or more; standard service, 30 to 40 %; strategic software or intellectual service, 20 to 30 %.

4. **Fixed before the offers.** Fix criteria, weights, scale and price formula before receiving offers, give them to the suppliers (with `rfp-draft`), and leave them. After reading, weights drift towards the offer already preferred; suppliers built their offers on the announced priorities; and the choice must be defensible to the losers and internally. A change after opening is a labelled sensitivity (see `offer-comparison`), never the grid.

5. **Anchored scale.** 0 to 4 or 0 to 5 with an observable descriptor per level and per criterion (0 absent or non-compliant, 1 insufficient, 2 partial, 3 compliant, 4 beyond, with proof). Without anchors two evaluators do not score the same thing. An even scale avoids the refuge in the middle.

6. **Technical threshold** (optional): offers below a minimum technical score are set aside before the price is read. State the threshold and why.

7. **Number of criteria.** 5 to 8 by default. A criterion under 5 % hardly ever separates offers (at most 0.5 point out of 10): merge it. Weights total 100.

# Price-scoring formulas

Marks out of 10; P is the price of the offer, computed on the full cost over the same horizon (`total-cost-analysis`); Pmin and Pmax the lowest and highest offers received. Example with offers at 200, 220, 260 and 300:

| Formula | Marks | Effect |
|---|---|---|
| Proportional to the lowest: `10 × Pmin / P` | 10; 9.09; 7.69; 6.67 | A curve, not a line: 10 % above the lowest costs about 0.9 point at the top, less for dear offers. Each mark depends on the lowest offer: a very low outlier compresses all the others' marks and can reverse a ranking between two offers that did not move. |
| Linear between lowest and highest: `10 × (Pmax − P) / (Pmax − Pmin)` | 10; 8; 4; 0 | The dearest gets 0 whatever the gap (100 against 101 gives 10 and 0), and a small gap is stretched over the whole scale. With a heavy price weight it eliminates the dearest outright. |
| Relative gap to the lowest: `10 × (1 − k × (P − Pmin) / Pmin)`, floor 0 | 10; 9; 7; 5 with k = 1 | Each percent above the lowest costs k × 0.1 point; the mark reaches 0 at Pmin × (1 + 1/k). Choose k and announce it. The lowest offer still sets the scale: a very low outlier stretches every gap. |

Proposed default: the third, with k announced, or the first, stating its dependence on the lowest offer. The second only if its effects are accepted. Whatever the formula, each mark depends on offers you do not control: check by recomputing the ranking without the lowest offer. Example: price weight 40 %, quality 60 %; offer X at 220 with quality 6.5, offer Y at 260 with quality 7.3. With the lowest offer at 200 the proportional formula gives X 7.54, Y 7.46. If a third offer comes in at 150, the same formula gives X 6.63, Y 6.69: the ranking flips although neither offer changed.

**Exchange rate between criteria.** Write what each weight trades. With a price weight w (in %) and a proportional mark, an offer r above the lowest loses 10 × w/100 × (1 − 1/(1 + r)) points out of 10. At w = 30 % and r = 10 %, that is 0.27 point, as much as one point of mark on a criterion weighted 27 %. This is the sentence management validates, more than the percentage.

# Method

1. Identify the purchase type, the stakes and the priorities given; if there are none, say what you assumed.
2. List the knockouts, then choose the scored dimensions and turn them into 5 to 8 criteria, each with its weight and the reason for it.
3. Anchor the scale for each criterion and name the evidence expected in the offer.
4. Choose the price formula, give its exchange rate, and simulate it on fictional prices when the user asks to see how it behaves.
5. Flag the criteria that need an internal definition before use, the sensitive weights, and what is a number against what needs a comment.
6. Recompute the weights total and the simulated marks before writing them.

Parameters: `type_achat` selects the starting dimensions (`logiciel`, `prestation`, `fourniture`); `multi_lots` gives one grid per lot with the shared knockouts written once, weights that may differ by lot, and a rule on whether one supplier may win several lots; `autre` starts from the closest type and says which. `nb_criteres_max` (5, 8, 10, 12) caps the scored criteria, knockouts not counted; above 8, the average weight falls below 12.5 %. With `inclure_risque_conformite` false, the risk dimension (solidity, continuity, security) is left out of the scored criteria, but legal knockouts stay because they are conditions. `priorites_achat` (free text): each priority receives a weight with the reason.

# Example

<example>
**Criterion: delivery reliability** (supplies). Weight 15 %: late delivery stops our line, and the volumes are steady enough to measure it. Evidence: on-time delivery report over 12 months, for two comparable customers.
- 0: no data supplied, or under 80 % on time
- 1: 80 to 90 %
- 2: 90 to 95 %
- 3: 95 % or more, shown by the report
- 4: 98 % or more, shown, and backed by a penalty commitment
Comment space: [justification of the mark].

Why this is right: each level is observable, so two evaluators reading the same report give the same mark.
</example>

# Expected output format

Default format; an explicit request from the user overrides it. Keep the two output names below.

- `vendor_scorecard`:
  1. **Summary** (3 to 5 lines): purchase type, number of knockouts and scored criteria, weight of price and formula, the weights to validate first, and the decision asked (validate, then freeze before the specification goes out).
  2. **Knockouts** (table): condition / why it is a knockout / evidence required with the offer / source.
  3. **Weighted criteria, grouped by family** (table): family / criterion / weight % / measurement mode (what evidence, which source) / reason for the weight. One subtotal row per family and a final row at **100 %**; recompute them before writing.
  4. **Scale** (separate table): level / meaning, 0 to 4; then the per-criterion anchors: criterion / 0 / 1 / 2 / 3 / 4, each level observable.
  5. **Price**: formula, its parameter, exchange rate between price and quality, simulation on fictional prices, ranking test without the lowest offer. Technical threshold if any.
  6. **Blank scoring sheet**, one per evaluator, whenever a committee will use the grid: offer and evaluator / knockouts met yes or no / rows criterion, weight, mark 0 to 4, weighted mark, justification and page of the offer / total / date and signature. Each evaluator fills it alone before the joint meeting, so that the first voice does not anchor the others.
- `framing_notes`: how to use the grid, the freeze rule, sensitive weights, criteria needing an internal definition, who validates and by when. Facts, assumptions and points to check labelled apart.

# Definition of done

- Knockouts are separate from the scored criteria; criteria are grouped by family with a subtotal each, every one has a weight with its reason, and the weights total 100.
- Each scale is anchored and reusable; the price formula, its exchange rate and its dependence on the other offers are written.
- The freeze rule is stated, and no weight is presented as a standard without a source.
- A blank scoring sheet is attached when a committee will score.
- The grid can be shared as is with the business and procurement teams.
