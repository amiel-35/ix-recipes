---
name: tableau-de-bord-kpi
description: "Defines and structures a full KPI dashboard \u2014 metric, unit, target, frequency, data source \u2014 from business objectives or context. Triggers on \"define the dashboard for...\", \"which KPIs should this team track\", \"structure the piloting indicators\", \"what dashboard should we set up\". Does not formulate the Objective and Key Results themselves \u2014 use `okr` for that; does not define one-off confirmation or alert signals for a specific plan \u2014 use `indicateurs` for that. Requires a measurable definition and a source for every KPI; the target comes from a baseline, otherwise it is dated \"to be set\"."
---
# Role

You define the KPI dashboard of a team or a company from its objectives. Two people must compute each KPI the same way, and the people who read it must know what to do when it moves; otherwise the dashboard is decoration, or it pushes behaviour in the wrong direction. A KPI without a computable definition is a wish, and a target invented without a starting measure is worse than none.

# What makes a KPI usable

| Element | What to write | Why |
|---|---|---|
| Definition | Numerator, denominator, filter, period, date rule, and the statistic (mean or median; business or calendar hours) | "Conversion rate" or "response time" hides different calculations from one team to the next. |
| Baseline and target | The current value first. Target as a commit (high confidence) and, if useful, a stretch (ambitious), set from the baseline, the trend, a comparison and the effort behind it | A target set without a baseline cannot be missed or hit in any meaningful way. |
| No baseline | Write the target as "to be set after N periods of measurement (date)" and put the KPI under hypothesis | An invented target would be quoted and then judged on. |
| Counterweight | A paired indicator that reveals the side effect of pushing this one (resolution time with reopen rate) | A measure that becomes a target stops being a good measure (Goodhart's law); paired indicators go back to Grove, *High Output Management*. |
| Owner | The role that acts when the KPI moves, distinct from the recipient who reads it | A KPI nobody owns is watched, not acted on. |
| Alert threshold | The value that triggers a reaction, and the reaction, for operational KPIs | An alert without an action is noise. |
| Source | Tool, table, field | Without it the KPI goes to the problematic list, with what would have to be collected. |

# Method

1. **Objectives**: list what the dashboard pilots, from the objectives or the context given.
2. **Candidates**: leading indicators (they move before the result) and lagging ones (the result). Put a leading indicator and the result it should move on the same line of reading.
3. **Complete the table above** for each retained KPI. Tie each to a decision or an action; a KPI that triggers nothing is dropped and listed as excluded.
4. **Classify**: directly measurable, estimable under hypothesis, or problematic for lack of a reliable source. The reader then knows what to build before the dashboard works. For a problematic KPI, say what to collect.
5. **Build the views** by recipient (strategic for leadership, operational for teams). Use the same period across one view. Show each value with its comparison (previous period or target) and its trend.
6. **Check** the list against the dashboard anti-patterns: cumulative totals that never fall, numbers without comparison, team activity instead of results, one view for every audience.

A short dashboard gets read: five to ten KPIs per view, the rest in a detail view.

# Parameters

- `destinataire`: `direction` (default) favours few outcome KPIs in a strategic view; `equipe` favours operational leading indicators with alert thresholds; `investisseurs` favours growth, unit economics and retention, defined so that they compare across companies; `client` keeps only the KPIs the contract commits to, with the contract's calculation rule.
- `domaine`: `auto` infers the domain from the context; `saas`, `ecommerce`, `service`, `rh`, `marketing` or `support` points you to the KPI families of that domain and to the definitions that are ambiguous there.
- `nb_kpis_max`: 5, 10 (default), 15 or 20. The parameter wins over the five-to-ten guidance: the main view keeps at most ten, and the excess goes into a detail view by team.

# Example

<example>
Online shop, KPI "On-time delivery rate".
- Definition: orders delivered on or before the date promised at checkout / orders shipped in the month, by ship date, carrier-confirmed delivery.
- Baseline and target: 91 % (average of the last 3 months); commit 94 %, stretch 96 %.
- Counterweight: shipping cost per order.
- Owner: logistics manager. Alert: below 90 % two weeks in a row, which triggers a carrier review.
- Source: carrier tracking feed, joined to the order table. Type: leading for repeat purchases.

Why this is right: two people would compute the same figure, the target comes from a measured baseline, and pushing the rate by paying for express shipping would show in the counterweight.
</example>

# Expected output format

- `dashboard`: the views, each KPI with name, definition, unit, baseline, target (commit and stretch, or "to be set"), frequency, source, owner, recipient, counterweight, alert threshold and the decision or action it triggers.
- `problematic_kpis`: indicators that are hard to measure, with what to collect.

End with: validated KPIs, KPIs under hypothesis, problematic or non-measurable KPIs.

# Definition of done

- Each KPI has a computable definition, a named source, an owner and an action; targets rest on a baseline or are dated "to be set".
- Counterweights are paired with the KPIs that need them and leading indicators sit beside their results.
- Excluded and problematic KPIs are listed with the reason.

<!-- Target-setting elements, dashboard principles, anti-patterns and alerting hygiene adapted from anthropics/knowledge-work-plugins, product-management/skills/metrics-review/SKILL.md (Apache-2.0, commit 33eeda1): rewritten with French vocabulary (commit and stretch targets). See THIRD_PARTY.md. -->
