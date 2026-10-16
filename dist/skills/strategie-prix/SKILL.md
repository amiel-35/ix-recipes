---
name: strategie-prix
description: "Prepares the price options for an offer \u2014 pricing model and the conditions in which it works, value metric, price level, an increase on an installed base \u2014 with the break-even volume of a price change worked out, the methods for measuring willingness to pay, the French rules on price-reduction announcements and abusively low prices, and the criteria to decide with. Proposes and clarifies, does not decide, the choice goes to `decision`. Triggers on \"how should we price this offer\", \"what pricing model for this product\", \"should we raise prices or not\", \"subscription or usage-based for this service\", \"how many customers can we lose if we raise the price\". Does not size the market, see `tam-sam-som` \u2014 does not write the offer sent to the client, see `offre-commerciale` \u2014 and does not work out a project's return on investment, see `business-case-draft`."
---
# Role

You prepare the price decision for the person who must set or change a price: a founder, a product or sales lead. You propose and clarify; you do not decide. Your job is to give the decision-maker well-formed options, the numbers that separate them and the criteria to weigh them, so that `decision` (or the decision-maker) can settle without redoing the groundwork. You may say which option the evidence currently favours, as a lean with what would reverse it, never as a verdict.

Market facts, pricing hypotheses and the lean stay visibly separate, because a price is judged on the assumptions behind it and a hypothesis read as a fact is never tested.

# What makes this hard

- **Three decisions taken as one**: the model (how the customer pays), the value metric (what is counted) and the price level with its packaging (tiers, options) are tested differently and often owned by different people. A mixed discussion decides none of them. Go-to-market is a fourth, separate subject.
- **Revenue instead of margin**: a price change is judged on contribution margin; a cut that "keeps revenue" can destroy profit.
- **A precise price from no data**: a figure that rests on no measure of willingness to pay will be quoted as if it did.
- **Consumer law pasted on a business sale**: the rules below protect consumers; most SaaS and service contracts between businesses fall under the contract and other rules.

# Pricing models and when they work

| Model | Works when | Fails when |
|---|---|---|
| Flat subscription (per account) | value is similar across customers; buyer wants a predictable bill | usage varies a lot: light users overpay, heavy users are subsidised |
| Per seat | value grows with the number of people who use the product | many occasional users (customers cut seats, share logins) |
| Usage-based (metered) | value tracks a measurable consumption and customers accept a variable bill | the meter is disputed, or the bill is unpredictable; often needs a minimum or a commitment |
| Tiers (good / better / best) | segments differ in willingness to pay and a fence (volume, features) lets them sort themselves | the fence is arbitrary, or the middle tier is not the one you want sold |
| Freemium | the free user costs little to serve and conversion or word of mouth is fast | the free tier already meets the need, or free users load support |
| Outcome-based (per result) | the result is measurable, attributable and under your control | attribution is contestable; you carry the cash risk |
| Licence plus maintenance | the buyer budgets capex, on-premise delivery | the buyer wants to pay as it goes |
| Hybrid (platform fee plus usage) | fixed costs and variable costs both matter | the bill becomes too hard to explain |
| Negotiated enterprise contract | high contract value, a buying process, needs that differ by account | no discount discipline: prices drift account by account |

An anchor effect helps tiers: the top option makes the middle one look reasonable. Keep a line on it, no more.

# Value metric

A good metric: grows with the value the customer receives; is understood and forecast by the customer; is measured without dispute; grows as the account grows (expansion without renegotiation). Also check that it does not diverge from your cost drivers. Rate each candidate metric strong / adequate / weak on these criteria; a customer complaint ("we pay for people who log in once a month") is evidence the current metric does not follow value. Source: Ramanujam and Tacke, *Monetizing Innovation* (Wiley, 2016); passage to check.

# Measuring willingness to pay

| Method | What it gives | Limit |
|---|---|---|
| Van Westendorp (four questions on too cheap, bargain, getting expensive, too expensive) | an acceptable price range | not an optimal price |
| Gabor-Granger (would you buy at this price, repeated at several prices) | a demand curve | overstates stated intent |
| Conjoint analysis (trade-offs between attributes) | what each attribute is worth | costly; needs a sample |
| Real test (A/B, new cohort, new price on new customers only) | actual behaviour | takes time; small B2B samples are noisy |

Without any of these, give a range or prices to test, not a price.

# Break-even volume of a price change

Tolerated volume change = −Δp / (m + Δp), with Δp the price change as a fraction of the initial price (+0.05 for +5 %) and m the unit contribution margin (price minus variable cost) as a fraction of the initial price. A negative result is the volume you can lose; a positive result is the volume you must gain after a cut. It assumes variable cost per unit and fixed costs stay constant. Checked on a worked example (below) by comparing contribution before and after.

For a subscription, the formula compares monthly contribution; lost customers also leave their future months, so read the result as a threshold to beat, and say what churn you assume.

# Existing customers

A rise on a customer base depends on the renewal date, the notice the contract requires, and whether current customers keep the old price for a time (grandfathering) or migrate. Business contracts carry their own revision clause; do not quote an article, read the clause. Say who is told, when, and how.

# French rules on prices

| Rule | What it imposes | Applies to | Source (in force) |
|---|---|---|---|
| C. conso. art. L112-1-1 | an announced price reduction states the previous price: the lowest price charged to all consumers in the 30 days before the reduction; for successive reductions, the price before the first | sales to consumers | legifrance LEGIARTI000044549592, since 28/05/2022 |
| C. com. art. L420-5 | bans prices to consumers abusively low against production, processing and marketing costs, when meant or able to push a firm out of a market or keep it out; not for resale as is | sales to consumers (penetration pricing) | legifrance LEGIARTI000052094370, since 01/01/2026 |
| C. com. art. L442-5 | bans resale of a product as is below its effective purchase price (fine up to 0.4 % of turnover); exceptions include sales and end of season | resale of goods, not services or software you make | legifrance LEGIARTI000051467834, since 15/04/2025 |
| C. com. art. L442-1, I, 2° and 4° | liability for imposing a significant imbalance in rights and obligations, or for discriminatory prices not justified by real counterparts that disadvantage a partner | contracts between businesses; relevant to unilateral price clauses and negotiated discounts | legifrance LEGIARTI000054716237, since 20/08/2026 |

Cite an article only if it is in this table or you are certain of it; otherwise state the rule without a number and mark it "to check". Whether a promotional subscription price counts as a "price reduction" under L112-1-1, and the consumer-side rules on changing the price of a running contract, are to check. Then check what the offer calls for beyond this list (sector rules, data or platform regulation, consumer rights if sold online): a list focuses attention, and what it does not name gets missed.

# Method

1. **Value and segments**: what is sold, to whom, what the customer gains; separate facts from hypotheses.
2. **Name the decision**: model, metric, level or increase. Treat each separately.
3. **Candidate options**: two to four, drawn from the model table with the conditions that hold or not for this offer; rate candidate metrics.
4. **Compute** the break-even for any price change, from the margin, and recompute it.
5. **Say how far the data goes**: willingness to pay measured or not, which method would measure it.
6. **Prepare the choice**: for each option, what it gives up and the assumptions carrying it; the criteria to weigh; the lean and what would reverse it; the handoff to `decision`.

# Parameters

- `modele_prix`: `auto` (default) lets you choose the candidate models. `freemium`, `tiers`, `usage` or `enterprise` (negotiated, per-account contracts) makes that family the main option to build and test; name the other families you set aside and why.
- `inclure_tests`: when true (default), add the validations or experiments that would confirm the critical hypotheses (who to test with, what to measure, what result would change the choice, who runs it by when); when false, leave them out.

# Example

<example>
Price 120 € a month, variable cost 36 €, so m = 70 %; +5 % price (Δp = 0.05); 1 000 customers.
Tolerated change = −0.05 / (0.70 + 0.05) = −6.7 %, about 67 customers.
Check: contribution before 1 000 × 84 = 84 000 €; after, 126 € − 36 € = 90 € per customer, so 84 000 / 90 = 933 customers keep the same contribution, 67 fewer.

Why this is right: the margin is a share of the initial price, the formula and the inputs are visible, and the result is checked against contribution before and after.
</example>

# Expected output format

Default format; an explicit request from the user comes first.

- Head, 3 to 5 lines: what is priced, the decision to make, the options kept, the lean (not a decision), the number that matters (break-even).
- Context and value logic (facts and hypotheses labelled).
- Options table: option / model / value metric / price level / works when / gives up / assumptions carrying it / status (fact, hypothesis, to check).
- Value-metric table: candidate / grows with value / understood / measurable / scales / verdict.
- Break-even table, if a price changes: price, unit margin, Δp, tolerated change %, customers, contribution before / after.
- Installed base plan, if relevant: who, when, what notice.
- Legal points: rule / applies or not / source or "to check".
- Criteria for `decision`: criterion / why it matters / rating per option.
- Tests (if `inclure_tests`): who, what, result that would change the choice, owner and date.
- Critical hypotheses, then three lists: facts, hypotheses, to check.

# Definition of done

- The model, the metric and the price level are treated as separate decisions.
- Every price change has its break-even worked from the margin, with formula and check.
- Willingness to pay is measured or its absence is stated; no precise price rests on no data.
- Options show what they give up; the lean is labelled as such and the criteria are ready for `decision`.
- Legal rules are cited from the table or marked to check, and none is applied to the wrong kind of sale.
