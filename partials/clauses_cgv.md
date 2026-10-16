# Clause set: standard terms (CGV / CGU, adhesion documents)

Read this file when the document is general terms of sale or use set in advance by one party (French law, checked 2026-10-16). Used by `contrat-fournisseur` for `type_document` = `cgv_cgu`, and for the balance tests of non-negotiable SaaS conditions.

## Step 0: qualify the parties, then pick the test

"Abusive clause" has a different test depending on who contracts with whom, and a model mixes them up: it cites art. 1171 C. civ. between businesses (where it does not apply), treats the grey list as if it voided the clause, or misses the withdrawal rules that changed in 2026. Qualify the parties before reading any clause, then use only the test that matches.

| Parties | Test applied | Consequence |
|---|---|---|
| Business sells to a **consumer** | C. conso. L212-1 with the black list R212-1 and the grey list R212-2 | Black list: irrefutably abusive. Grey list: presumed abusive, the seller may prove the contrary. Either way the clause is deemed unwritten and the contract survives without it (L241-1). |
| Business to a **non-professional** (association, SCI, a person acting outside their trade) | Same, by L212-2 | Same |
| Business to **business** (producer, distributor, service provider on both sides) | C. com. L442-1 I 2° (significant imbalance), plus I 1° and 6°; art. 1171 C. civ. does not apply (Cass. com. 13 May 2026, n° 24-17.137), except where another text disapplies L442-1 (e.g. financial leasing by credit institutions, Cass. com. 26 Jan 2022, n° 20-16.782) | The author is liable for the harm; the court weighs the whole contract, and a clause is not unbalanced only because it departs from default rules (Cass. com. 26 Feb 2025, n° 23-20.225) |
| Other adhesion contracts (the proposer is not in production, distribution or services) | C. civ. 1171 (1110 defines adhesion: non-negotiable terms set in advance) | Clause deemed unwritten; the main object and the price are not examined |

If the input does not say who the customer is, ask; if you must proceed, run the consumer grid and the business grid separately and say which parties each one assumes.

## Legal points to get right

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

## Default positions (B2B, when the user has no internal policy)

These are market positions, not law. Read as a customer, apply them as written; read as the supplier, a clause worse than these for the customer is where you will be challenged.

| Clause | Green | Orange | Red |
|---|---|---|---|
| Liability cap | ≥ 12 months of price | 6 to 12 months | < 6 months, none for one party, or asymmetric |
| Non-renewal notice (annual term) | ≤ 3 months | 3 to 6 months | > 6 months, or tacit multi-year renewal |
| Payment | within L441-10 | — | beyond L441-10, or no late rate or recovery fee stated |
| Personal data | processing contract in place (art. 28 GDPR, see `clauses_saas_donnees` and `conformite-rgpd`) | — | data processed with none |
| Jurisdiction | before the court the user can reach | — | against a non-trader (CPC 48) |

## Reading position

- `client`: the user accepts or negotiates a supplier's terms; flag what will not hold against them and what to ask for.
- `fournisseur`: the user publishes or sells under these terms; flag what will not hold, what exposes them as author (L442-1 B2B, deemed-unwritten clauses B2C) and the mandatory mentions missing from their own terms.
- `utilisateur`: the user is the end user of a service; list the rights the terms must not remove (withdrawal, legal guarantee, termination, mediator, jurisdiction) and the practical steps (how to withdraw, how to terminate).

## Keep the grid open

This is a list to focus attention, not the limit of the review. After it, check what the document's subject calls for beyond it: personal data and processors, data portability and exit, sector rules, the specific product or service sold. If the service is software or cloud, read `clauses_saas_donnees` too. What a list does not name gets missed: with this grid alone, models forgot the Data Act and art. 28 GDPR on SaaS terms that they saw without it.
