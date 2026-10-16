# Clause set: negotiated supplier or service contract

Read this file when the document is a supplier or service contract that the parties can negotiate (French law, checked 2026-10-16). Used by `contrat-fournisseur` for `type_document` = `contrat_negocie`. For software, cloud or hosting, read `clauses_saas_donnees` as well.

## Why a generic review is not enough

Three things go wrong without French-law knowledge: the buyer is told to ask for terms the law forbids (a payment term beyond 60 days), the buyer's own legal duties are missed (the URSSAF vigilance duty), and the imbalance is argued under the wrong text (art. 1171 C. civ. between businesses). Also compute: a cap "equal to three months of fees" means nothing until it is set against the annual price and the total commitment.

## Legal points to get right

| Point | What the text imposes | Source |
|---|---|---|
| Payment terms | Agreed term ≤ 60 days from invoice, or 45 days end-of-month if expressly stated; 30 days if nothing is agreed. An acceptance procedure lasts ≤ 30 days and does not move the start of the payment term unless the contract says so expressly and not abusively. A term within these limits is no finding; never propose a longer one: fines reach 2 M€ for a company. | C. com. L441-10, L441-16 |
| Buyer as author | The buyer is liable too for a significant imbalance imposed on the supplier (I 2°), repeated tenders (I 6°, since 20 Aug 2026), abrupt termination (II; 18 months of notice protects) and a substantial cut in volumes (II al. 2, since 20 Aug 2026). Counter-proposals must not fall into these. | C. com. L442-1 (loi 2026-796) |
| Imbalance between businesses | Argued under L442-1, not art. 1171 C. civ. | Cass. com. 13 May 2026, n° 24-17.137 |
| Vigilance duty | For any contract of at least 5 000 € HT, obtain at signature then every 6 months an URSSAF certificate under 6 months old (check its authenticity) and a Kbis or equivalent. Without them, the buyer is jointly liable for the taxes, contributions and wages owed if the supplier is found guilty of concealed work. | C. trav. L8222-1, R8222-1, D8222-5, L8222-2 |
| Vigilance, pending | Verification of accepted subcontractors (loi 75-1334 art. 3) added by loi 2026-534: in force on a date set by decree, no later than six months after promulgation (about late Dec 2026). Check the decree. | C. trav. L8222-1-1 |
| Cap and gross fault | A limitation does not work for gross or wilful fault. A clause that empties the essential obligation is unwritten. Whether a token service credit as "sole remedy" for an outage empties it is an interpretation: flag it, do not assert it. | C. civ. 1231-3, 1170 |
| Penalties | The judge can reduce or increase a manifestly excessive or derisory penalty, including one that protects the buyer. | C. civ. 1231-5 |
| Fixed term | A fixed-term contract runs to its end and nobody can demand renewal: a long fixed term with no early exit locks the buyer in. | C. civ. 1212 |
| Unforeseeable change | Renegotiation for excessive cost: check whether the contract waives it and who bears the risk. | C. civ. 1195 |

Cite an article only if it is in this table or you are certain of it; otherwise state the rule without a number and mark it "to check", because the reader will look each number up and models invent plausible ones.

## Default positions (buyer's side, when the user has no internal policy)

These are market positions, not law; say so. Read from the supplier's side, a clause worse than these for the buyer is where you will be challenged, and the buyer's legal duties above are the buyer's, not yours.

- **Liability cap** ≥ 12 months of price. Outside the cap or under a higher one: personal-data breach, confidentiality, infringement. State the cap as a share of the annual price and of the total commitment.
- **SLA**: availability measured per month, with its hours (downtime allowed per 30 days = (1 − target) × 720 h; 99.5 % is 3 h 36 min). Service credits are not the sole remedy; a right to terminate after N months below target.
- **Term**: renewal by one-year periods with notice ≤ 3 months; refuse tacit multi-year renewal. Compute the last date to give notice from the stated start date, and say if the start date is missing.
- **Price**: indexed on a named index and capped, not a free unilateral increase.
- **Exit**: reversibility in a structured, commonly used format, with assistance.

## Extra checks by `type_fournisseur`

- `logiciel`: exit and reversibility, licence scope, and the Data Act and GDPR points of `clauses_saas_donnees`.
- `maintenance`: response and restoration times, spare parts, what the penalty is worth against the loss it covers.
- `outsourcing`: staff transfer (L1224-1 C. trav. may apply when an activity moves; the answer turns on the facts, so refer it to a lawyer), audit rights, vigilance.
- `prestation`: deliverables and acceptance (≤ 30 days, L441-10 III).
- `autre`: the common checks only.

## Keep the grid open

This is a list to focus attention, not the limit of the review. After it, check what the contract's subject calls for beyond it: personal data and processors, data portability and exit, sector rules, the specific product or service bought. What a list does not name gets missed: with a grid, models forgot the Data Act and art. 28 GDPR on SaaS terms that they saw without it.
