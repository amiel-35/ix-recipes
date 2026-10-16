---
name: business-case-draft
description: "Structures an investment decision into a costed business case \u2014 costs, expected benefits, risks, explicit financial hypotheses. Triggers on \"draft the business case for...\", \"cost out this project\", \"is it worth investing in...\", \"justify this budget\", \"structure the investment file\". Requires numerical data, even if fragile; when none exists at all, points to `note-strategique` instead. Presents the ROI with its scenarios and break-even point, never as a certain figure."
---
# Role

You draft the business case an investment owner takes to a decision-maker (managing director, CFO, investment committee). That reader challenges assumptions, not layout, and rejects a case at the first question it cannot answer: where does this gain come from, what happens if we do nothing, how wrong can you be before it stops paying. A case built on gross gains or on one central scenario is either rejected on the spot or approved on a figure that does not hold.

Your job is a case whose figures survive that challenge. Each estimate carries its source or its assumption on the same line (a decision-maker can contest an assumption, not a bare number), and the recommendation rests on a break-even point calculated before it is written.

# How to calculate

| Item | Definition | Watch for |
|---|---|---|
| Baseline | Compare with the "do nothing" scenario, which has its own costs and losses (penalties, temporary staff, maintenance) that continue. Flows are the difference between project and baseline. | Costs already committed (sunk) are left out; counting them is the commonest error in investment files. |
| NPV | Σ over t = 0 to N of flow_t / (1 + r)^t. Investment at t = 0, flows at the end of each period unless the user says otherwise. | Decide on NPV. |
| IRR | The rate that makes NPV zero. | Several IRRs if flows change sign more than once; none if flows never change sign; it assumes reinvestment at the IRR, and it does not rank mutually exclusive projects of different size or timing. |
| Payback | First period where cumulative flows reach zero; simple or discounted (flows divided by (1 + r)^t). | Ignores everything after the payback, so it informs but does not decide. |
| ROI | The word is ambiguous: write the formula you use. Default: (cumulative net gains over N − investment) / investment, net of running costs, undiscounted. | A ROI computed on gross gains, without running costs, overstates the return. |
| Break-even | The value of the key assumption (annual net flow, adoption, price) that makes NPV zero. With a constant annual flow F over N years: F = investment / annuity factor, where the factor is Σ over t = 1 to N of 1/(1 + r)^t. | It tells the decision-maker how wrong the case can be. |
| Discount rate | The company's (cost of capital or hurdle rate given by finance). | If none is given, state your assumption and show the sensitivity. Flows and rate both nominal, or both real. |

**Cash and non-cash gains.** Freed time is a cash gain only if a spend disappears (a departure, an avoided hire, a stopped temp contract). Otherwise it is a non-cash gain. Calculate NPV with the cash gains alone and then with all gains, and state the gap: this is often the whole debate. It is common investment-file practice, taken here as the default position.

**Tax.** State whether the flows are before or after corporate income tax. Default before tax, as most requests are; after tax, depreciation is not a cash flow but lowers the tax.

| Rule | What it imposes | Source (checked 2026-10-16) |
|---|---|---|
| Corporate income tax rate | Normal rate 25 %; 15 % up to 42 500 € of profit per 12 months for companies with revenue of 10 M€ or less whose fully paid-up capital is held at least 75 % by individuals (or by a company meeting the same condition) | CGI art. 219 I (second paragraph and b); legifrance.gouv.fr, LEGIARTI000053542939, in force |

Cite a French tax article only if it is in this table or you are certain of it; otherwise state the rule without a number and mark it "to check".

# Expected inputs

- The project, opportunity or initiative and the decision to be made.
- Costs (one-off and recurring), expected gains, horizon, discount rate, options considered, constraints.
- If no figure at all exists, say so, list the data needed and point to `note-strategique` for the decision framing. If figures exist but are fragile, proceed and let the scenarios show it.

# Method

1. **Frame**: the decision, the baseline, the options (always including doing nothing).
2. **Inventory** one-off costs, running costs, gains and risks. Classify each gain as cash or non-cash. Give each figure its source (given, estimated, assumed).
3. **Build the flows** by period over the horizon, incremental to the baseline. Compute NPV, IRR, simple and discounted payback and the ROI with its formula, and recompute each from its inputs before writing.
4. **Scenarios**: at least three (low, central, high), each naming the assumption that moves. Calculate the break-even of the key assumption. This comes before the recommendation, because the recommendation depends on it.
5. **Recommend** with the condition that holds it ("go if the annual gain stays above X, which is Y % under the central case; the lever is Z"). Each risk says its effect on NPV or the scenario that expresses it.
6. **List the missing data** needed for a robust case, most consequential first.

# Parameters

- `horizon_analyse`: number of months counted (12, 24, 36 default, 60). Flows by year for 36 and 60 months; by quarter for 12 and 24, with the annual rate converted to (1 + r)^(1/4) − 1. If the asset or contract lasts less than the horizon, use its life. No value beyond the horizon, a conservative default; if you add one, show NPV without it.
- `inclure_options`: when true (default), give the same metrics for each option in one comparison table, with the baseline as reference; when false, project against baseline only.

# Example

<example>
Investment 90 000 € at t = 0, four years, rate 10 %, net annual flow (gains minus running costs) 30 000 € in the central case:

| Scenario | What moves | Net annual flow | NPV | IRR |
|---|---|---|---|---|
| Low | cash gains 40 % under plan | 18 000 € | −32 942 € | −8.4 % |
| Central | plan | 30 000 € | +5 096 € | 12.6 % |
| High | adoption faster, gains 25 % over plan | 37 500 € | +28 870 € | 24.1 % |

Break-even: annuity factor 3.1699, so NPV is zero at 90 000 / 3.1699 = 28 392 € a year, only 5.4 % under the central case.

Why this is right: the central NPV is positive but thin, and the break-even says so before anyone reads the IRR; the recommendation can then be conditional on holding the annual gain above 28 400 €.
</example>

# Expected output format

- `business_case`: context and decision, options and baseline, costs, gains (cash and non-cash), flows and metrics with formulas, scenarios and break-even, risks with their effect, recommendation with its condition, next steps, missing data.
- `financial_hypotheses`: each assumption, its source, and the scenario it moves.

# Definition of done

- Flows are incremental to the baseline, the horizon, rate and before / after tax basis are stated, and every metric was recomputed.
- NPV is shown for cash gains alone and for all gains when the case includes non-cash gains.
- Three scenarios and the break-even are in the document and the recommendation names its condition.
