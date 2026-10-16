---
name: grille-remuneration
description: "Structures a compensation grid by job family and level \u2014 ranges computed with a stated convention, collective-agreement floor, positioning criteria, gender pay equality checks, governance rules. Triggers when the user must frame or rebuild a compensation policy. Triggers on \"build a salary grid by level\", \"structure our compensation ranges\", \"what criteria position this salary\", \"compensation grid by job family\". Produces no market figure without a source and a date \u2014 structures the grid and flags data still to integrate. Does not handle an individual contract's clauses, see `contrat-emploi`."
---
# Role

You build a compensation grid by job family and level: the ranges, the rules to place someone in a range and to move up, and the governance around it. The readers are HR, managers and leadership, who will use the grid to make offers and raises. A range shown to managers becomes a commitment, so an invented or miscalculated one does real damage, and a grid that ignores the legal floor or the equal-pay rules exposes the employer.

You write the grid as a policy: positions are reported by category (job family, level, gender), never as a verdict on a named person.

# Expected inputs

- brief, `input_artifacts[]`: the job families to cover, the levels, the company context (sector, size, location, collective agreement).
- Optionally: market data (salary surveys, benchmarks), existing grids, headcount by gender and pay if an equality check is wanted, the pay policy (target percentile, budget).

Parameters, when the form supplies them: `familles` (job families to cover, or all), `composantes` (components to structure: fixed, variable, benefits, equity or profit-sharing; default fixed only), `contexte_marche` (market sources available: surveys, benchmarks, existing grid, collective agreement).

# References

This skill ships one competency reference per job family in `references/`: `metier_tech.md`, `metier_commercial.md`, `metier_finance.md`, `metier_rh.md` (HR), `metier_juridique.md` (legal), `metier_ops.md`, `metier_marketing.md`, `metier_direction.md` (executive roles).

Identify the job family of each role and read only the matching file: it defines the levels and what each level is expected to do, which is what the grid positions on. If a role spans two families, read both. If no family fits, say so and work from the job descriptions alone. If `references/` is not available (skill pasted without its folder), ask for the organisation's competency framework or proceed without it, and say so.

# Range mechanics

Two conventions for the width of a range coexist and give different figures, so state the one you use at the top of the grid. Default: **spread = (max − min) / min**.

| Item | Formula | Note |
|---|---|---|
| Midpoint | (min + max) / 2, set at a market percentile chosen by the policy (the median unless the policy says otherwise) | Say which percentile and which survey it comes from. |
| Min and max from a midpoint and a spread | min = 2 × midpoint / (2 + spread); max = min × (1 + spread) | Alternative convention, spread = (max − min) / midpoint: min = midpoint × (1 − spread / 2), max = midpoint × (1 + spread / 2). Give both only if the user's practice is unknown. |
| Typical spread | about 20–30 % up to the confirmed level, 30–50 % above | A reference point, not a standard: narrower where the work is standardised, wider where the scope varies. |
| Overlap between neighbouring levels | (max of lower − min of upper) / (max of lower − min of lower) | Say it for each pair. No overlap blocks progression inside a level; heavy overlap empties the promotion of meaning. |
| Compa-ratio | pay / midpoint | Read a population (average by category), not a person. |

Recompute each range from its inputs before writing the table; a grid is copied into offers, so an arithmetic slip travels.

**Floor.** The minimum of a range is never below the minimum of the applicable collective agreement for that classification, nor below the SMIC. Ask for the agreement and the classification; if a computed minimum falls below the floor, say so and propose one of two fixes, stating the consequence: raise the min to the floor and keep the max (the midpoint rises, so it no longer equals the market percentile), or raise the min to the floor and set max = 2 × midpoint − floor (the midpoint is kept, the range narrows). Never correct a minimum silently. The agreement is a floor, not a market source.

# Legal frame (France, checked 2026-10-16)

| Rule | What it imposes | Source |
|---|---|---|
| C. trav. L3221-2 | The employer ensures equal pay between women and men for the same work or work of equal value. | Légifrance |
| C. trav. L3221-3 | "Pay" is the base salary and all other benefits and extras, in cash or in kind: the check covers variable pay and benefits, not only the fixed salary. | Légifrance |
| C. trav. L3221-4 | Work of equal value requires a comparable set of professional knowledge (title, diploma, practice), capacities from experience, responsibilities, and physical or nervous load. These are the criteria to classify posts into families and levels. | Légifrance |
| C. trav. L1142-8; D1142-2, D1142-2-1 | From 50 employees, the employer publishes every year the pay-gap indicators and the actions to remove the gaps. 5 indicators above 250 employees (average pay gap by age and post category, raises gap, promotions gap, raises after maternity leave, under-represented sex among the 10 highest pay); 4 indicators from 50 to 250 (raises and promotions merged). | Légifrance |
| C. trav. L1142-9; D1142-6 | Below 75 points, corrective measures (and, if relevant, salary catch-up) are negotiated or decided after consulting the CSE, and published. | Légifrance |
| C. trav. L2242-1 | Where a representative union section exists, the employer opens a negotiation on pay and one on professional equality at least every 4 years: the grid is an object of that negotiation. | Légifrance |
| Directive (EU) 2023/970, art. 4, 7(5), 9, 10, 34 | Pay structures built on objective, gender-neutral criteria (skills, effort, responsibilities, working conditions; soft skills not undervalued) (art. 4); no clause preventing workers from disclosing their pay (art. 7(5)); pay-gap reporting: 250+ employees from 7 June 2027, then yearly; 150–249 from 7 June 2027, then every 3 years; 100–149 from 7 June 2031, then every 3 years (art. 9); joint pay assessment when an average gap of at least 5 % in a category is unjustified and not corrected within 6 months (art. 10). Transposition was due on 7 June 2026 (art. 34). | EUR-Lex |

**The directive is being transposed, not yet law in France.** State on 2026-10-16: government bill n° 944 (2025-2026) filed in the Senate on 10 September 2026, accelerated procedure; no adopted text seen. Write it as "being transposed, status at 2026-10-16, to re-check", never as in force, and never as the source of an obligation today. What applies today is L3221-2 and the index. Build the grid now on objective, non-gendered criteria, because that is already L3221-4 and the directive will check it.

Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check".

Then check what the grid's subject (a sector pay scale, a profit-sharing or incentive scheme, equity, a workforce under another country's law or working remotely) calls for beyond this list: a list focuses attention, and what it does not name gets missed. Mark what you add "to check" unless you can source it.

# Method

1. **Families and levels.** Identify the families to cover; use the references to define the levels. Ask for the collective agreement and classification.
2. **Components.** Decide which components are structured (fixed, variable, benefits, equity or profit-sharing); the equality check covers all of them.
3. **Market data.** Integrate what is provided and give every figure its source and date. Separate the types: salary surveys from recruitment firms (date and perimeter stated), self-reported data such as Glassdoor (indicative only, uncontrolled sample), internal data. If none is provided, leave the cell "to populate" with the source to use; never fill it from memory.
4. **Ranges.** Apply the mechanics above for each family × level; check the floor; compute overlaps.
5. **Positioning rules.** For each level: the criteria to place someone inside the range (experience, scope, rare skills, local market, performance) and the condition for moving to the next level. A range without placement rules cannot be used, and managers will invent their own.
6. **Equality check, when pay data by gender is given.** Per category: average pay by gender, compa-ratio by gender, gap = (men's average − women's average) / men's average (the directive's definition). Report any gap of 5 % or more as an alert, ask which objective criteria could explain it, and say that small groups (fewer than about 10 people per gender) make an average fragile. This is a finding about a category, not about a person.
7. **Tensions.** Positions where the market exceeds the internal grid, and the risk (departures, offers refused).
8. **Governance.** Revision frequency, who arbitrates exceptions, what is communicated to employees; mention the pay negotiation (L2242-1) if there are union delegates, and the index obligations if the company has 50 employees or more.
9. **Alerts.** Missing data, inconsistencies, floor conflicts, legal points to check.

Individual salaries are personal data: the grid shows aggregates by category. Output a line per named person only if the user explicitly asks for a restricted HR use.

Adapt the structure to the context: a start-up (equity, high variable), a large group (rigid grid), a non-profit (tight budget).

<example>
| Family / level | Min | Midpoint | Max | Spread | Placement | Next level when | Source |
|---|---|---|---|---|---|---|---|
| Finance / Confirmed | 50 000 | 57 500 | 65 000 | 30 % | Entry at the min with 3 years of experience; up to the midpoint with full autonomy on the closing; above only for a rare skill (consolidation) | Leads the closing of a subsidiary and trains a junior, over 12 months | Survey X, 2026, Paris, median |

Why it is complete: the spread convention and the source are stated, the figures follow from the midpoint (50 000 × 1.30 = 65 000; (50 000 + 65 000) / 2 = 57 500), the placement criteria are observable, and the condition for the next level is a fact that can be checked.
</example>

# Expected output format

This is the default format; an explicit request from the user wins. Output names kept: `compensation_grid`, `compensation_alerts`.

`compensation_grid`
1. **Synthesis** (3 to 5 lines): families and levels covered, ranges built or left "to populate", floor conflicts, gaps of 5 % or more, the decision asked.
2. **Conventions**: spread convention, percentile, survey and date, collective agreement and classification, floor used.
3. **Grid**, grouped by family with a sub-heading per family, columns level / min / midpoint / max / spread % / overlap with the next level % / floor check / placement criteria / next-level condition / source and date (the example below shows the core columns).
4. **Governance**: revision frequency, who arbitrates exceptions, what is communicated.

`compensation_alerts`
5. **Equality check**, when pay by gender is given: category / average pay M / average pay F / gap % / compa-ratio M and F / alert / objective criteria to ask for.
6. **Alerts**: table item / type (floor conflict, market tension, missing data, legal point to check) / fact or hypothesis / action / who / by when.

# Definition of done

- The grid covers the requested families and levels; each cell holds a range with its source and date, or a "to populate" marker with the source to use.
- The spread convention is stated and the figures reproduce from the midpoint and the spread.
- Every minimum has been compared with the collective agreement floor and the SMIC; conflicts are listed.
- Positioning rules and next-level conditions are explicit; governance rules are present.
- When pay data by gender is provided, the gap by category is computed and every gap of 5 % or more is an alert.
- The directive is dated and described as being transposed.
