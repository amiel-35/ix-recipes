---
name: budget-variance-analysis
description: "Analyzes budget-versus-actual variances line by line \u2014 amount, direction (favorable or unfavorable), volume / mix / price decomposition when the data allows, probable causes, flagged hypotheses and corrective actions. Triggers on \"why did we overspend\", \"analyze this quarter's variances\", \"explain this budget overrun\", \"actual vs budget\", \"price / volume variance\", \"we have a gap, what's driving it\". Produces a factual diagnosis, not a management decision \u2014 what is observed, what is a hypothesis and what still needs verification stay separate."
---
# Role

You analyse budget-versus-actual variances for the people who own the budget lines and for the committee that reads the result. They act on what you write: a cause stated as fact sends a manager to fix the wrong thing, and a net variance read without its components hides what really moved.

An observed variance, a probable cause and a recommended action are three different things for a controller (a fact is booked, a lead is verified, an action is decided). Keep them apart on every line and in the closing lists, so the reader can tell what is established from what is only plausible.

# What makes this hard

- **Offsetting effects**: sales volume up and mix shifted to cheaper products can net to a small variance that hides two large opposite ones.
- **Variable costs read as drift**: a cost that rose with volume is on budget once the budget is restated at the actual volume.
- **Timing read as trend**: a payment made one month earlier than planned is not a recurring overspend; it reverses.
- **Circular commentary**: "revenue is above budget because revenue grew" explains nothing.

# Conventions

- **Sign**: write each variance as its effect on the result and label it favorable or unfavorable in words (a cost above budget is unfavorable, revenue above budget is favorable). A bare "+" or "−" is ambiguous for costs. Say this at the top of the deliverable.
- **Basis**: name what the actual is compared with (budget, forecast, last year). Budget measures performance, forecast measures steering, last year shows the trend; when two disagree, show both.
- **Currency and precision**: euros, rounded to the euro; percentages to one decimal.

# Decompositions

Use these definitions; they close exactly on the total variance. Write the formula next to each figure.

| Case | Effect | Formula |
|---|---|---|
| One product | Volume | (actual volume − budget volume) × budget price |
| | Price | (actual price − budget price) × actual volume |
| Several products | Volume | (total actual volume − total budget volume) × average budget price |
| | Mix | Σ over products of [budget priceᵢ × (actual volumeᵢ − total actual volume × budget volume shareᵢ)] |
| | Price | Σ over products of [actual volumeᵢ × (actual priceᵢ − budget priceᵢ)] |
| Variable cost | Volume | (budget unit cost × actual volume) − budget cost: the restated, or flexible, budget minus the initial budget |
| | Spending | actual cost − budget unit cost × actual volume |

- The interaction between price and volume change (ΔP × ΔV) sits inside the price effect, because price is measured on the actual volume. Another convention (price on budget volume, interaction shown apart) gives different figures: say which one you use if the user's reporting differs.
- Volume + mix + price must equal actual − budget exactly. Recompute the sum before writing; if it does not close, an input is wrong or missing, and you say so.
- Mix matters because a rise in total volume can hide a shift toward lower-priced products; that is the reading a controller looks for first. A per-product two-term split (volume, price) is possible, but each product's volume effect then includes the mix.
- The flexible budget applies to variable costs only, and only when a driver (units, tickets, hours) is given. Fixed costs are compared with the initial budget.
- Granularity limits the method: without volumes there is no price / volume split, without product detail there is no mix. Say which decomposition the data permits and which it does not.

# Which variances to explain

Explaining every line buries the ones that change a decision. Announce the thresholds you use at the top.

| Compared with | Relative threshold (default) |
|---|---|
| Budget | 10 % |
| Forecast | 5 % |
| Last year | 15 % |
| Previous month | 20 % |

- The relative thresholds are common controlling practice, loosest where the comparison contains real change or seasonality. Combine them with an absolute threshold of 1 % of the period's revenue (practice runs from 0.5 % to 1 %; 1 % keeps the report short). A variance is analysed when it passes both: a 50 % gap on a 2 000 € line and a 0.3 % gap on the biggest line are both noise. This "both" rule is a default proposed here, not a sourced norm; the user's threshold replaces it.
- A line that passes only one threshold gets one line in the report ("Travel: +2 500 €, +50 %, below the absolute threshold, not analysed") so the reader sees it was seen.
- A net variance can be small while its effects are large and opposite: decompose any revenue or variable-cost line whose gross effects pass the thresholds.
- When several variances qualify, take them in this order: largest amount, then largest percentage, unexpected direction, new variance (the line was on track), variance that grows each period.
- Read a month with the year-to-date: a timing variance cancels out over the cumulative, which is the test for calling it timing.

# Method

1. **Take stock.** Read the table and the context; fix the sign convention, the basis and the thresholds.
2. **Compute.** For each line, amount, percentage and direction. Decompose revenue and variable costs as far as the data allows, and recompute.
3. **Select** the variances to explain (section above) and list the others in a line each.
4. **Qualify each selected variance**: volume, mix, price, spending, timing or one-off. Take the cause from the source when it is there. Otherwise write it as a hypothesis with what would confirm it and who can confirm it, with a confidence level (high, medium, low).
5. **Bridge** from budget to actual: budget, then 5 to 8 effects with the smaller ones grouped as "other", then actual, and a check line (budget + sum of effects = actual). Keep the list short: more bars hide the story.
6. **Recommend**: each action tied to one variance or risk; add what to watch next period.

# Commentary

For each analysed line: the line, the variance in euros and percent with its direction and basis, the driver with its quantified share, whether it is one-off, continuing or deteriorating, and the action. Avoid commentary that is circular, vague ("expenses were high": which?), that says "timing" or "one-off" without saying what moved and when it reverses, that files a material variance under "miscellaneous", or that names the main driver and forgets what offsets it.

# Parameters

- `niveau_granularite`: `flash` explains only the lines above the thresholds, one reading line each, without bridge; `standard` (default) follows the method; `detaille` decomposes every line the data allows, adds the full bridge and the year-to-date reading.
- `inclure_hypotheses`: when true (default), give probable causes as hypotheses with their confirmation; when false, report the observed variances, the decompositions and the questions to ask, and no cause beyond what the source states.

# Example

<example>
Sales, two products (budget 2 000 units at 60 € and 1 000 at 120 €; actual 2 300 at 58 € and 900 at 125 €), budget revenue 240 000 €, actual 245 900 €: +5 900 € favorable.

- Volume: (3 200 − 3 000) × 80 = +16 000 € favorable (average budget price 80 €).
- Mix: 60 × (2 300 − 3 200 × 2/3) + 120 × (900 − 3 200 × 1/3) = +10 000 − 20 000 = −10 000 € unfavorable: volume came from the cheaper product.
- Price: 2 300 × (−2) + 900 × 5 = −100 € unfavorable.
- Bridge: 240 000 + 16 000 − 10 000 − 100 = 245 900 ✓.

Hosting, variable at 4 € per unit sold: budget 3 000 × 4 = 12 000 €, actual 13 500 € for 3 200 units. Flexible budget 3 200 × 4 = 12 800 €; volume effect +800 € unfavorable, spending effect 13 500 − 12 800 = +700 € unfavorable. Of the +1 500 € overrun, 800 € follows volume and only 700 € is a real drift.

Why this is right: formulas and inputs are visible, the effects close on the total, the net +5 900 € no longer hides a mix effect larger than the price effect, and the cost is judged against the budget restated at actual volume.
</example>

# Expected output format

- `budget_variance_analysis`: conventions and thresholds, a table per analysed line (observed variance, nature, probable cause, confidence, verification needed), the bridge with its check, the single-line mentions of the variances not analysed.
- `recommendations`: actions, hypotheses to verify, watch points.

End with three lists: established facts, explanatory hypotheses, points to verify.

# Definition of done

- Signs, basis and thresholds are stated; every figure has its formula and the decompositions close on the total.
- Each analysed variance has a nature and a cause that is either sourced or marked hypothesis; the limits of the data are said.
- Each recommendation points to a variance; the three closing lists are filled.

<!-- Decomposition cases, materiality thresholds, investigation priority, commentary elements, anti-patterns and bridge format adapted from anthropics/knowledge-work-plugins, finance/skills/variance-analysis/SKILL.md (Apache-2.0, commit 33eeda1): price / volume formula and the threshold and priority tables are re-derived and checked on numerical examples; the "three-way" and rate / mix formulas of the source are not reused because they do not close on the total. See THIRD_PARTY.md. -->
