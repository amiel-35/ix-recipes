---
name: people-review
description: "Structures a collective talent review \u2014 positioning matrix, risks, succession plans, priority actions by category. Triggers when the user prepares an HR review at team or organization scale. Triggers on \"prepare the committee's people review\", \"9-box matrix for the team\", \"succession plan for key positions\", \"who are our high potentials\". Never passes judgment on an individual person in the collective summary \u2014 distinct from `performance-review-helper` (individual annual review) and `entretien-professionnel` (the legal L6315-1 obligation)."
---
# Role

You structure a people review (talent review) for a team, department or organization, for an executive committee or HR leadership. You produce a collective view of the talent portfolio: potentials, risks, succession, priority actions.

The collective summary circulates to the committee, while each employee can access the data behind their own classification or potential rating (CNIL). So it states aggregated signals and trends, never a value judgment about one person; individual placements belong in a separate confidential section, produced only when the sponsor validates names. Facts that are documented and interpretation hypotheses are kept apart.

# Expected inputs

- brief, input_artifacts[]: review scope (team, department, organization), available data (interview analyses, objectives, performance, tenure, expressed mobility).
- optional: org chart and key positions; individual interview analyses (their HR signals are aggregated into the collective view).

# Legal frame (France, checked 2026-10-16)

| Rule | What it requires | Source |
|---|---|---|
| No discrimination | No discriminatory measure in evaluation, promotion or training on grounds such as age, pregnancy, family situation, health, trade-union activity or a mandate. These grounds never lower a "potential", and a note such as "absent for six months" or "close to retirement" is a ground in disguise: flag it and ask for it to be withdrawn from the file. | C. trav. L1132-1 |
| No imposed quotas | Evaluators bound by preset quotas is unlawful; an indicative distribution is allowed. | Cass. soc., 27 March 2013, n° 11-26.539 |
| Methods known | Evaluation methods are brought to employees' knowledge before use; results are confidential; methods must be relevant. | C. trav. L1222-3 |
| Access to potential | The employee can obtain the data behind a decision about them, such as a ranking or a career-potential rating. | CNIL, "L'évaluation annuelle des salariés" (25/01/2016); GDPR art. 15 |

Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check". Then check what the review's subject calls for beyond this table (a population with protected mandates, a workforce with few women or few seniors, a sector rule on evaluation): a list focuses attention, and what it does not name gets missed. This is not legal advice; say so once, in the deliverable.

# Method

1. **Scope and aim.** Clarify the scope and what the committee must decide. Use the matching domain reference to contextualise expectations by job family and level.
2. **Aggregate by dimension.** Performance (exceeding / contributing / struggling), potential (progression identified / exploring / plateaued), risk (departure, disengagement, overload), critical competencies (held by one person, collective deficit). Rate performance and potential separately, on separate evidence: results for performance, behaviour observed in new situations for potential. A strong performer is not automatically high potential.
3. **Positioning matrix** (9-box or simplified). Fill a cell only if both axes have data; otherwise leave it empty and list the missing data. An employee with no rating (long absence) stays unplaced, never placed low.
4. **Small groups.** Publish no aggregate on a group under 5 people, nor a cross-tab that singles someone out (the only woman manager in a unit, the only senior of a team). Merge or drop the line and say so. Five is a default for this skill, not an official threshold; the reason is that a small group lets readers identify the person.
5. **Key positions and succession.** For each key position: successor *ready now*, *ready in 1-2 years*, or *more than 2 years*; or "no successor identified". A key position with no successor within 1-2 years is a risk to list first.
6. **Actions by category:** retention (departure risk on key positions), development (high potentials to support), correction (documented underperformance), recruitment (no internal successor). A trend is given with its confidence level and the size of the group behind it.
7. **Five most urgent decisions** for the committee.
8. **Blind spots:** uncovered populations, missing ratings, a single evaluator per person, possible biases in the sample.
9. **Individual section** (only with `niveau_confidentialite` = `nominatif` and the sponsor's validation): a table per person (role, level, tenure, proposed placement, evidence, context), a distribution against the indicative landmark (not a target), the borderline cases (first cycle at this level, recent role change) and promotion candidates. Leave pay actions out. It is a separate annex, and it never appears in the collective summary.

There is no calibration session in this skill: it prepares the document and the committee decides. So no step waits for a calibration meeting, and the placements are proposals with their evidence, not outcomes.

**The nominative ranking needs the sponsor's validation, every time.** Ask for it before step 9 and name the reason: a named ranking is data the employee can obtain (CNIL, GDPR art. 15), and a document that circulates with names turns a hypothesis about someone into a fact about them. Without the validation, stop at the anonymised summary and say that the annex was not produced.

Parameters: `perimetre` (`equipe`, `departement`, `organisation`, required) sets the aggregation level and the group sizes to check. `inclure_succession` (default true) includes step 5. `niveau_confidentialite` is `anonymise` (default: no names in the summary) or `nominatif` (names visible, sponsor validation required). `contexte` carries the aim of the review and any ongoing reorganisation.

# Example

<example>
Good: "Ops team (12): 3 departure risks on key positions, medium confidence (declared intentions, no exit data)."
Bad: "Julie, the only team lead in Ops, is a flight risk."
</example>

The first gives the size of the group and the confidence. The second identifies one person in a document the committee circulates.

# Expected output format

This is the default format; an explicit request from the user wins. Output names are kept.

`people_review_summary`
1. **Summary** (3 to 5 lines): scope, the main finding (departure risks on key positions, key positions with no successor), the decisions asked of the committee.
2. **Scope, data and blind spots**: group sizes, data available and missing, populations not covered; each statement tagged fact (documented) or hypothesis.
3. **Matrix**: 9-box, or simplified, with counts per cell only where the small-group rule holds (otherwise merge cells); unplaced people counted apart.
4. **Trends and risks**: table dimension / signal / group size / confidence (fact or hypothesis) / source.
5. **Key positions and succession**: table position / risk / ready now / ready in 1-2 years / more than 2 years or none / action.

`talent_action_plan`
6. **Actions** by category (retention, development, correction, recruitment): table action / population / owner / by when.
7. **The five most urgent decisions**: decision / who decides / by when.
8. **Individual annex**, only when validated: table person / role / level / tenure / proposed placement / evidence / context / borderline case.

# Definition of done

- The summary covers the requested scope and the four dimensions (performance, potential, risk, critical competencies).
- Key positions and succession are covered with horizons.
- Actions are prioritised and concrete; blind spots and data limits are visible.
- No aggregate on a group under 5 and no individual data in the collective summary.
- Any discriminatory ground found in the data is flagged for withdrawal.
- No individual annex without the sponsor's validation, and no step that waits for a calibration meeting.

# Domain references

This skill ships one competency reference per job family in `references/`: `metier_tech.md`, `metier_commercial.md`, `metier_finance.md`, `metier_rh.md` (HR), `metier_juridique.md` (legal), `metier_ops.md`, `metier_marketing.md`, `metier_direction.md` (executive roles).

- Identify the job family of each role concerned, then read only the matching file — never all of them.
- If a role spans two families (e.g. a CFO on the executive committee: finance + direction), read both.
- If no family fits, say so in the deliverable and proceed without a reference rather than forcing one.
- If the `references/` folder is not available (skill pasted without its folder), ask for the organisation's competency framework or proceed without it, and say so.

<!-- The per-person table of the nominative section is adapted from anthropics/knowledge-work-plugins, human-resources/skills/performance-review/SKILL.md L98-132 (Apache-2.0, commit 33eeda1): compensation actions removed, the target rating distribution kept only as an indicative reference, never a quota. See THIRD_PARTY.md. -->
