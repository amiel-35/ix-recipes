---
id: total-cost-analysis
label: Analyse cout total (TCO)
version: 1.3.0
description_fr: Structure un TCO — coûts directs, coûts cachés, hypothèses, risques — sur un horizon donné, en distinguant coûts confirmés, estimés et non chiffrés, avec la révision de prix au plafond, les coûts internes, le double run, la sortie et le seuil de bascule qui inverserait le classement. Déclenche sur "calcule le coût total de possession", "au-delà du prix affiché, quel est le vrai coût sur trois ans", "compare le TCO entre ces deux offres". Compare les coûts, ne recommande pas. Ne construit pas la grille de notation qualitative des fournisseurs (utiliser `vendor-scorecard`) ni le document d'appel d'offres (utiliser `rfp-draft`).
description_en: Structures a TCO — direct costs, hidden costs, hypotheses, risks — over a given horizon, distinguishing confirmed, estimated and unquantified costs, with price revision at the cap, internal costs, double running, exit costs and the tipping value that would reverse the ranking. Triggers on "calculate the total cost of ownership", "beyond the sticker price, what's the real cost over three years", "compare TCO between these two offers". Compares costs, does not recommend. Does not build the qualitative vendor scoring grid (use `vendor-scorecard`) nor the tender document itself (use `rfp-draft`).
icon: ∑
domain: ops
category: research
input_types:
- brief
- markdown
- reference
- decision
output_types:
- analyse_tco
- comparatif_tco
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
---

# Role

You structure a total cost of ownership across the whole life of a purchase, so that options compare beyond the sticker price. The reader decides on the confirmed costs and negotiates the rest, so each line says which kind it is: **confirmed** (in an offer or contract), **estimated** (a calculation on a stated hypothesis) or **unquantified** (a risk or cost with no figure yet). You compare costs; the choice between offers belongs to `offer-comparison` or `decision`.

# Rules of the calculation

| Point | How to treat it | Why |
|---|---|---|
| Tax basis | State it at the top. Compare excluding VAT when the buyer recovers it; including VAT when it does not (non-taxable association, some exempt activities, part of the public sector). | The same offers rank differently on the wrong basis. Cite no VAT article: the deduction rule of the CGI is repealed on 2027-01-01 and recodified, and the new article numbers are not verified. |
| Price revision | Compute a revision clause (an index such as Syntec) at its cap for the worst case and at 0 % for the best case; show the range. | Ignoring the clause understates the cost of the offer that carries it. |
| Introductory prices | Cost the later years at the normal price when the first year is discounted. | A launch price is a first-year price. |
| Volumes | Apply the same growth in volumes, and the price tiers, to every option. | An option costed on today's volumes against another on tomorrow's is not a comparison. |
| Internal costs | Staff time (administration, training, acceptance), at the loaded cost supplied, or marked unquantified. | It is real cost that offers never show. |
| Double running | The period when the old and the new run together is a cost. If it is the same for all options it does not change the ranking: say so. | Prevents a neutral cost from looking decisive, or from being forgotten. |
| Exit and reversibility | Cost of recovering data and of terminating. When personal data is processed, its return or deletion at the end is a term of the article 28 contract (GDPR art. 28.3 g): request it, do not assume it is free. | Exit costs arrive after the decision is made. |
| Horizon | The same for all options, aligned on the commitment period or the asset's life. A firm commitment longer than the need is an exit cost. | Otherwise annual costs and commitments are compared across different lengths. |
| Discounting | Stay in current euros by default. Discount only if payment schedules differ a lot (cash purchase against subscription) or the horizon exceeds 3 years, at a rate supplied by the user, never invented. | A rate you chose silently changes the ranking. |
| Life-cycle cost | Useful grid of lines: acquisition; use (energy, resources); maintenance; end of life; and quantifiable environmental externalities where they apply (CCP art. R2152-9 definition, checked 2026-10-16, used here only as a grid of lines). | Prevents forgetting a phase. |
| Tipping value | For each hypothesis that can reverse the ranking, give the value at which it reverses. | It tells the reader which unknown to settle first. |

Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check".

# Expected inputs

- brief
- input_artifacts[]
- offer, contract or economic summary
- usage, implementation or operation hypotheses if available

# Method

1. Identify the cost lines across the life cycle: direct, implementation, operation, exit.
2. Document hypotheses of volume, duration, resources and contract terms; the same for every option.
3. Compute each line per year, then the total; recompute each total from its lines before writing, because a total repeated in a decision is hard to correct later.
4. Add hidden costs and risks when plausible, marked confirmed, estimated or unquantified. Say for each unquantified cost that could change the decision which amount would reverse the ranking.
5. Produce the quantified summary and, if several options, the comparison.
6. Surface the hypotheses that would change the conclusion, with their tipping value.

Parameters: `horizon_analyse` (12, 24, 36 or 60 months) is the common horizon, 36 by default. `devise` sets the currency of the figures; offers in another currency are converted at a rate the user gives, never an assumed one. With `inclure_comparatif` false, analyse a single option and skip the comparison section. `hypotheses_couts` (free text) holds volumes, usage and internal resources, and takes precedence over defaults.

# Example

<example>
| Line | Nature | Value | Hypothesis | Sensitivity |
|---|---|---|---|---|
| Service fee, 3 years | estimated | 90,000 to 92,727 | €30,000 per year; revision capped at 3 % from year 2 (30,900 then 31,827) | medium |

Tipping value: an offer B quoted at 91,500 is cheaper than A once the average annual revision exceeds about 1.7 %, and dearer below.

Why this is right: the range shows the clause at both ends, and the tipping line tells the reader exactly which assumption decides.
</example>

# Expected output format

Default format; an explicit request from the user overrides it. Keep the two output names below.

- `tco_analysis`:
  1. **Summary** (3 to 5 lines): tax basis and horizon, total per option as a range, the structural gap between options, the hypothesis that reverses the ranking, the first thing to settle.
  2. **Hypotheses** (table): hypothesis / value / source / applied to every option.
  3. **Breakdown per option** (table, grouped by phase: acquisition, implementation, operation, internal costs, double running, exit): line / nature (confirmed, estimated, unquantified) / year 1 to N / total / calculation hypothesis / sensitivity (low, medium, high). Total row as a range (revision at 0 % and at its cap), recomputed from its lines.
  4. **Unquantified costs** (table): cost / why it could matter / amount that would change the decision.
- `tco_comparison`, if several options:
  5. **Comparison** (table): option / total low / total high / gap to the cheapest / unquantified costs left out.
  6. **Tipping values** (table): hypothesis / base value / value at which the ranking reverses / which option then leads.
  7. **Points to verify** (table): point / who / by when.

Confirmed, estimated and unquantified stay visibly labelled everywhere a figure appears.

# Definition of done

- The tax basis is stated, and the breakdown covers acquisition, implementation, operation, internal costs and end of life.
- Each line is confirmed, estimated or unquantified; every total has been recomputed from its lines.
- Revision, discounts, volumes and commitments are treated the same way for all options.
- The most sensitive lines and the tipping values are identifiable without rereading the reasoning.

<!-- The cost-category coverage (total cost, implementation, training, support, exit costs) draws on anthropics/knowledge-work-plugins, operations/skills/vendor-review/SKILL.md (Apache-2.0, commit 33eeda1), rewritten with the French tax basis, price revision and tipping-value rules. See THIRD_PARTY.md. -->
