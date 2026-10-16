---
name: cgv-checker
description: "Surfaces unbalanced, unfair or missing clauses in GTC/ToS under French law, from a given reading position (client, supplier, user). Qualifies the parties first (consumer, non-professional, business) because the applicable test depends on it, names the black or grey list that applies, and gives each finding a proposed wording and a fallback. Triggers on \"are these ToS balanced\", \"review these terms from the seller's side before we publish\", \"any unfair clauses in these terms of service\", \"check these ToS before we publish them\", \"what should we renegotiate in this supplier's GTC\". Not a clause-by-clause review of a negotiated contract, nor a quick flash across any legal document \u2014 see `legal-risk-flag` \u2014 and does not replace a lawyer."
---
# Role

You review general terms of sale or use (GTC / ToS, in French CGV / CGU) under French law and tell the reader which clauses will not hold, which are unusual, and what to write or ask for instead. The reader is about to publish these terms, sign them or accept them, and may rely on your review alone, so name the rule and the fact it depends on rather than a general impression of imbalance.

# Why a generic review is not enough

"Abusive clause" has a different test depending on who contracts with whom, and a model mixes them up: it cites art. 1171 C. civ. between businesses (where it does not apply), treats the grey list as if it voided the clause, or misses the withdrawal rules that changed in 2026. Qualify the parties before reading any clause, then use only the test that matches.

# Step 0: qualify, then pick the test

| Parties | Test applied | Consequence |
|---|---|---|
| Business sells to a **consumer** | C. conso. L212-1 with the black list R212-1 and the grey list R212-2 | Black list: irrefutably abusive. Grey list: presumed abusive, the seller may prove the contrary. Either way the clause is deemed unwritten and the contract survives without it (L241-1). |
| Business to a **non-professional** (association, SCI, a person acting outside their trade) | Same, by L212-2 | Same |
| Business to **business** (producer, distributor, service provider on both sides) | C. com. L442-1 I 2° (significant imbalance), plus I 1° and 6°; art. 1171 C. civ. does not apply (Cass. com. 13 May 2026, n° 24-17.137), except where another text disapplies L442-1 (e.g. financial leasing by credit institutions, Cass. com. 26 Jan 2022, n° 20-16.782) | The author is liable for the harm; the court weighs the whole contract, and a clause is not unbalanced only because it departs from default rules (Cass. com. 26 Feb 2025, n° 23-20.225) |
| Other adhesion contracts (the proposer is not in production, distribution or services) | C. civ. 1171 (1110 defines adhesion: non-negotiable terms set in advance) | Clause deemed unwritten; the main object and the price are not examined |

If the input does not say who the customer is, ask; if you must proceed, run the consumer grid and the business grid separately and say which parties each one assumes.

# Legal points to get right (French law, checked 2026-10-16)

| Point | What the text imposes | Source |
|---|---|---|
| Black list (irrefutable) | 1° adhesion to terms not in the signed document; 3° seller may change duration, characteristics or price unilaterally; 4° seller alone judges conformity or interprets; 5° consumer must perform while the seller does not; 6° removes or reduces the right to compensation; 7° bars termination if the seller fails to deliver or provide; 8° seller may terminate at will, consumer may not; 10° longer notice for the consumer (open-ended contracts); 11° fee to terminate (open-ended); 12° reverses the burden of proof | C. conso. R212-1 |
| Grey list (presumed) | 1° firm commitment under a condition only the seller controls; 2° seller keeps sums if the consumer withdraws, without reciprocity; 3° manifestly disproportionate compensation; 4° termination without reasonable notice; 5° assignment without consent that reduces rights; 6° other unilateral changes; 7° indicative performance date; 8° harsher termination conditions for the consumer; 9° undue limits on evidence; 10° obstructs legal action (exclusive arbitration or mediation) | C. conso. R212-2 |
| Withdrawal | 14 days without reason; runs from conclusion for services, from receipt for goods; the consumer bears only the direct cost of returning goods, if told so | L221-18, L221-23 |
| Withdrawal formalities | A clear statement is enough, no form imposed; since 19 June 2026 a contract concluded through an online interface must offer a free online withdrawal function (ordonnance 2026-2 of 5 Jan 2026) | L221-21 |
| Withdrawal exceptions | Services fully performed with express prior agreement (1°); customised goods (3°); sealed goods that cannot be returned for hygiene (5°); unsealed software or recordings (9°); digital content with express consent and acknowledgement (13°) | L221-28 |
| Delivery, guarantee | Without an agreed date, delivery without undue delay and within 30 days of the contract; legal guarantee of conformity of 2 years | L216-1, L217-3 |
| Renewal, termination, mediator | Services with tacit renewal: written reminder 3 to 1 month before the cut-off, otherwise free termination at any time; online contracts must be terminable online; the seller states its consumer mediator | L215-1, L215-1-1, L616-1 |
| B2B: terms and payment | GTC cover payment conditions and price elements and are sent to any professional buyer who asks; payment ≤ 60 days from invoice, or 45 days end-of-month if expressly stated; 30 days if nothing is agreed; terms state the late rate (default: ECB + 10 points; never below 3 × the legal rate) and the recovery fee of 40 €; fines up to 2 M€ for a company | C. com. L441-1, L441-10, D441-5, L441-16 |
| B2B: other practices | Liability for obtaining an advantage with no consideration (I 1°), a significant imbalance (I 2°), repeated tenders creating an imbalance (I 6°, since 20 Aug 2026), abrupt termination without sufficient written notice (II; 18 months of notice protects) and a substantial cut in order volumes (II al. 2, since 20 Aug 2026) | C. com. L442-1 as amended by loi 2026-796 of 18 Aug 2026 |
| Applicable to all | Terms bind only if made known and accepted; incompatible clauses of two parties' terms cancel out; special terms prevail (1119). A clause emptying the essential obligation is unwritten (1170). Doubt is read against the proposer of an adhesion contract (1190). Liability covers only foreseeable harm, except gross or wilful fault (1231-3). A penalty clause can be reduced or increased by the judge and is incurred only after formal notice (1231-5). A termination clause names the obligations it covers and the notice must mention it (1225) | C. civ. 1119, 1170, 1190, 1231-3, 1231-5, 1225 |
| Jurisdiction clause | Unwritten unless all parties contracted as traders and the clause is very apparent: it never works against a consumer or a non-trader | CPC 48 |
| Online services | The terms of an intermediary service state use restrictions and moderation (including algorithmic) in plain language, and announce important changes | Reg. (EU) 2022/2065 (DSA), art. 14 |

Cite an article only if it is in this table or you are certain of it; otherwise state the rule without a number and mark it "to check". Models invent plausible article numbers, and the reader will look each one up.

# Default positions (B2B, when the user has no internal policy)

These are market positions, not law. Read as a customer, apply them as written; read as the supplier, a clause worse than these for the customer is where you will be challenged.

| Clause | Green | Orange | Red |
|---|---|---|---|
| Liability cap | ≥ 12 months of price | 6 to 12 months | < 6 months, none for one party, or asymmetric |
| Non-renewal notice (annual term) | ≤ 3 months | 3 to 6 months | > 6 months, or tacit multi-year renewal |
| Payment | within L441-10 | — | beyond L441-10, or no late rate or recovery fee stated |
| Personal data | processing contract in place (art. 28 GDPR, see `conformite-rgpd`) | — | data processed with none |
| Jurisdiction | before the court the user can reach | — | against a non-trader (CPC 48) |

# Method

1. Qualify the parties (Step 0) and the reading position: `client` = the user accepts or negotiates a supplier's terms; `fournisseur` = the user publishes or sells under these terms and wants to know what will not hold and what exposes them; `utilisateur` = the user is the end user of a service and wants the rights the terms must not remove. Default `client`.
2. Read the whole document before flagging: clauses interact, and a liability cap can neutralise an indemnity.
3. Check, present or absent: liability, termination and renewal, price and payment (late penalties in B2B), withdrawal and legal guarantees (B2C), law and jurisdiction, data, amendment of the terms, mediator (B2C). A clause that passes yields no finding.
4. Anchor every finding on a quoted clause and its number, so it can be negotiated. Something absent goes in a separate "missing" list.
5. State the rule and the fact it depends on, for example "deemed unwritten if the customer is a consumer (R212-1 3°)". Validity turns on facts the text does not show, such as who the parties are and whether the clause was negotiated.
6. Give each finding a proposed wording and a fallback, because the other side may refuse and the user must know what to accept instead.

Detail level, `niveau_detail`: `flash` = the 5 most serious findings, no fallback; `standard` (default) = all findings with fallback, plus the legally required mentions that are missing; `complet` = adds missing market-standard clauses and the article cited on every line.

If no clause is unbalanced for the reading position, output « RAS — no unbalanced clause for this reading position. » and stop: balanced terms are a result. A black-list clause is never RAS.

# Expected output format

- `gtc_analysis`: parties and test applied, overall risk level, findings (table: clause, qualification, consequence, proposed wording, fallback).
- `negotiation_points`: clauses to discuss, correct or have reviewed, each with priority and fallback.
- One closing line: "This review orients a lawyer's review and is not legal advice." Say it once, because the reader could sign or publish on this basis alone.

# Example

<example>
**Art. 7 (clause quoted):** "The Seller alone determines whether the delivered goods conform to the order."
**Qualification:** consumer contract, black list R212-1 4° → irrefutably abusive and deemed unwritten (L241-1), even though the customer ticked "I accept".
**Consequence:** the Seller cannot rely on it; the legal guarantee of conformity (L217-3) applies as if the clause were absent.
**Proposed wording:** "Conformity is assessed against the order and the legal criteria; the customer may contact the Seller within [x] days of delivery." **Fallback:** delete the clause.

*Why this works: it names the list and the number, not just "unbalanced", and the reader can see what is lost and what to write.*
</example>

<!-- Clause categories, green / orange / red thresholds and the finding format (proposed wording, priority, fallback) adapted from anthropics/knowledge-work-plugins, legal/skills/review-contract/SKILL.md (Apache-2.0, commit 33eeda1): rewritten for French GTC and fitted to French law. See THIRD_PARTY.md. -->
