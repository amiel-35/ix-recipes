---
name: negotiation-brief
description: "Prepares a procurement negotiation position before the meeting \u2014 objective, useful facts, levers, traded concessions, priced BATNA, red line derived from the BATNA, opening position and target, with the buyer-side guardrails of French law (payment periods, termination of an established relationship). Triggers on \"prep my negotiation with this supplier\", \"what leverage do we have with this vendor\", \"how far can we push on this renewal\", \"what's our BATNA on this contract\". Does not analyze the contract's clauses, see `contrat-fournisseur` \u2014 and does not compare several quotes against each other, see `offer-comparison`."
---
# Role

You prepare a buyer's negotiation brief from an offer, a supplier context or a renewal situation. The reader is the negotiator, who will read it in five minutes before the meeting and then use it live: a figure without a source becomes a commitment or a bluff at the table, so each one is labelled. The brief gives a clear position, identified levers and limits the negotiator owns because they are derived, not arbitrary.

# Format of every lever and figure

One line per lever: the lever, **the fact that supports it (with its source)**, **the assumption it rests on**, what is offered in exchange. Facts can be shown across the table; assumptions are not said out loud. A hypothetical room for manoeuvre is written as an assumption, never as a given.

# How to build the numbers

1. **One unit, one horizon.** Put every price position (opening, target, red line, supplier's offer, BATNA) in the same unit and over the same horizon (per year, per unit). Check what a percentage applies to: "−15 %" on the current price and on the new asking price are two different targets.
2. **Price the BATNA.** The best alternative over the same horizon and perimeter, switching costs included: the alternative's price over the horizon, plus the one-off costs (transition, double running, internal time, continuity risk). Reservation price per year = BATNA total / number of years. Illustration: an alternative at 60/year over 2 years plus 6 of one-off costs gives 126 over two years, so a reservation price of 63/year. An alternative that is only a plan (an untested quote, an in-house solution) is priced as such and its fragility is stated.
3. **The red line comes from the BATNA.** It is the price beyond which the BATNA is better. A risk-of-switching premium may be added if it is written and justified. A red line chosen without a calculation gets conceded at the table; one derived from the BATNA can be defended. Keep it to yourself.
4. **Estimate the supplier's floor and the ZOPA.** The zone between your red line and the supplier's presumed floor. Base the floor on the supplier's dependence on you (share of their revenue), spare capacity and cost structure, and mark it as an assumption. With no overlap, say so and prepare the exit or a different structure of the deal.
5. **Opening, target, red line.** Order for a buyer: opening < target < red line, in the same unit. Anchor with an ambitious opening that a fact can defend (competing quote, index, volume); an opening you cannot justify costs credibility for the rest of the meeting.
6. **Concessions are trades.** Write each as "if you..., then we...", in decreasing size. Look for what costs you little and is worth a lot to the supplier: commitment length, visibility on volumes, faster payment (within the legal limit), a reference.
7. **Tiers.** Tier 1: cannot proceed without it, no concession without escalation (service continuity, price cap, reversibility). Tier 2: strong preference, room to trade. Tier 3: currency for exchange. Concede from tier 3 to win tier 2.
8. **Failure risks.** Continuity, transition lead time and supplier dependence, whose other side is legal exposure (guardrails below). List blind spots when the offer or context is incomplete, and the open questions: past performance of the supplier, strength of the alternative, what the alternative quote covers.

# Guardrails of French law (checked 2026-10-16)

| Point | What the rule imposes | Source |
|---|---|---|
| Payment period | The agreed period is at most 60 days from the invoice date, or 45 days end of month if written in the contract. Fine up to €2 million for a company. A longer period is not a lever, and an earlier payment is a concession that is always allowed. | C. com. art. L441-10 I, L441-16 |
| Advantage without consideration, imbalance | Liability for obtaining or trying to obtain an advantage with no consideration or manifestly disproportionate (1°), or for imposing obligations creating a significant imbalance (2°). A price cut is asked for in exchange for something. | C. com. art. L442-1 I 1° and 2° |
| Repeated tenders | New since 2026-08-20 (law n° 2026-796 of 2026-08-18): submitting a partner to competitive tenders repeated in a way whose frequency or manner creates a significant imbalance engages liability (6°). One competing quote is a lawful lever; the risk is in repeating the pressure. | C. com. art. L442-1 I 6° |
| Ending an established relationship | Ending, even partly, an established relationship without written notice that takes its length into account engages liability; 18 months of notice shield from a claim about duration. New since 2026-08-20: a substantial reduction of order volumes during a negotiation can also engage it. A contract end date does not remove the issue: plan every exit threat with its notice. | C. com. art. L442-1 II |
| Good faith and bluff | Negotiations are free but must be in good faith. Not disclosing your own valuation is lawful; lying is not (a fake competing quote). Keeping your red line to yourself is allowed; inventing a competing offer is not. | C. civ. art. 1112, 1112-1 para. 2, 1137 |

Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check". The analysis of contract clauses belongs to `contrat-fournisseur`: the brief keeps these points to one line each because it must be read in five minutes.

# Expected inputs

- brief
- input_artifacts[]
- received offer or situation summary
- supplier context, relationship history or constraints if available

Parameters: `contexte_relation` sets the angle. `premier_achat`: no history, so no dependence lever and no established-relationship risk; `renouvellement`: performance history, volumes, the supplier's dependence, and the notice an exit requires; `mise_en_concurrence`: quotes as facts, with the repeated-tender caution above; `incident_qualite`: documented incidents are the lever, kept apart from price; `relation_strategique`: joint value, longer horizon, dependence on both sides. `pression_temps` (`faible`, `moyenne`, `forte`): the stronger the pressure, the shorter the brief, the more tier 1 comes first, and the more the BATNA's transition lead time weighs on the red line. With `inclure_batna` false, the red line is a limit supplied by the user: label it as such. `contraintes_negociation` (free text) are treated as tier 1 unless the user says otherwise.

# Expected output format

- `negotiation_brief`: structured sheet with objective, BATNA, levers, opening position, target and red line
- `open_questions`: points to clarify before entering negotiations

Recommended structure:
- objective
- negotiation-useful facts
- levers
- possible concessions
- expected counterparts
- opening position
- target
- red line
- BATNA
- main risks

# Example

<example>
- **Lever: volume visibility.** Fact: we will buy at least 4 000 units next year (forecast signed off by the plant, 2026-09). Assumption: the supplier values a 3-year volume commitment more than a lower unit price (their capacity is under-used). Trade: "if you move to 11.40, we commit to 3 years on the 4 000 units".

Why this is right: the fact can be shown across the table, the assumption stays in the brief, and the lever is paid for with something that costs us little.
</example>

# Definition of done

- The brief contains an opening position, a target and a red line, in the same unit, with the calculation of the red line.
- Each lever is linked to a fact and an assumption; hypothetical levers are marked.
- BATNA, switching costs and main risks are visible without rereading the source.
- Payment-period and legal guardrails are checked against what the brief proposes.

<!-- Priority tiers and the trade-off rule adapted from anthropics/knowledge-work-plugins, legal/skills/review-contract/SKILL.md (Apache-2.0, commit 33eeda1): rewritten for purchase negotiation with purchase examples instead of contract-clause examples. See THIRD_PARTY.md. -->
