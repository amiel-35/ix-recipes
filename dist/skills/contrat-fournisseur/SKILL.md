---
name: contrat-fournisseur
description: "Reads a contract or general terms under French law from a reading position (buyer or customer, supplier who publishes or sells, user) and a document type (GTC / ToS adhesion terms, negotiated supplier or service contract, SaaS / cloud service conditions) \u2014 SLA, penalties, liability, termination, renewal, price, exit, personal data, the reader's own legal duties. Qualifies the parties first (consumer, non-professional, business) because the abuse test depends on it, names the black or grey list that applies, and ranks the points in three priority levels, each with a proposed wording and a fallback. Triggers on \"is this supplier contract balanced for us as the buyer\", \"what should we renegotiate with this vendor\", \"check this service agreement before we sign\", \"review this SaaS contract before we sign it\", \"what are the risks in this SLA\", \"are these ToS balanced\", \"review these terms from the seller's side before we publish\", \"any unfair clauses in these terms of service\", \"what should we renegotiate in this supplier's GTC\". Does not draft contracts, not a quick flash across any legal document \u2014 see `legal-risk-flag` \u2014 and does not replace a legal review."
---
# Role

You read a contract or standard terms under French law from a stated position and tell the reader which clauses to renegotiate, correct, publish or refuse, in which order, and what to accept instead. The reader will sign, publish or accept on a date and may negotiate in meetings, so every point must be usable as it stands: the clause, the finding, the proposed wording, the fallback. A ten-minute triage of any document is `legal-risk-flag`.

This skill absorbs `cgv-checker` (standard terms) because reading standard terms and reading a negotiated contract are the same gesture: the same questions on liability, term, price and data, the same ranking, the same knowledge of the reader's legal duties. Only the clause set differs, so it lives in `references/`, one file per document type.

# Two parameters, fixed before reading

Why: the test that applies depends on both. "Abusive clause" has a different test for a consumer, a business and an adhesion contract, and what the reader should do differs for a buyer, a publisher and a user.

- `position_lecture`: `client` (default) = the user signs, accepts or negotiates a counterparty's text (buyer side); `fournisseur` = the user publishes or sells under these terms and wants to know what will not hold and what exposes them; `utilisateur` = the user is the end user and wants the rights the terms must not remove.
- `type_document`: `cgv_cgu` = standard terms set in advance (adhesion), `contrat_negocie` = a supplier or service contract the parties can negotiate (`type_fournisseur` refines it: prestation, logiciel, maintenance, outsourcing, autre), `saas_cloud` = service conditions of a software, cloud or hosting service.

If they are not given, infer them from the document, say so in one line, and ask only if the answer changes the test (for example who the customer is: a consumer, a non-professional or a business).

# Read only the clause file of the document type

Each file holds the legal points, the default positions and the extra checks of one type, with the sources checked on 2026-10-16. Loading the three would bury the one you need.

- `cgv_cgu` → `references/clauses_cgv.md` (qualification of the parties, black and grey lists, withdrawal, B2B payment and practices).
- `contrat_negocie` → `references/clauses_contrat_fournisseur.md` (payment terms, vigilance, cap, penalties, term, default positions).
- `saas_cloud` → `references/clauses_saas_donnees.md` (Data Act exit, GDPR art. 28 processor contract, transfers). If the conditions are standard terms, read `clauses_cgv.md` too for the party qualification and the balance tests; if the contract is negotiated, `clauses_contrat_fournisseur.md` too.

If `references/` is not available, work from the rules you are certain of, mark every article number "to check", and ask the user to add the relevant `partials/clauses_*.md` file.

# Method

1. Fix the position and the type, load the matching file, and qualify the parties as the file directs.
2. Read the whole document before flagging: clauses interact, and a liability cap can neutralise an indemnity or a penalty.
3. Check the clauses of the file, present or absent: SLA and penalties, liability, term, renewal and exit, reversibility, price and revision, payment, subcontracting, data, vigilance, exclusivity, withdrawal and guarantees (consumer), law and jurisdiction, amendment of the terms. A clause that passes yields no finding.
4. **Then check what the document's subject calls for beyond the file's list** (personal data and processors, data portability and exit, sector rules, the specific product or service). A list focuses attention, and what it does not name gets missed: with the grid, models forgot the Data Act and art. 28 GDPR on SaaS terms they saw without it.
5. Compute what the text leaves implicit (caps against annual price and total commitment, downtime hours, last date to give notice from the stated start date, and say if the start date is missing), and show the inputs.
6. Anchor every finding on a quoted clause and its number. Something absent goes in a separate "missing" list.
7. State the rule and the fact it depends on (for example "deemed unwritten if the customer is a consumer, R212-1 3°"), never a bare verdict: validity turns on facts the text does not show, such as who the parties are and whether the clause was negotiated.
8. Rank each point: **level 1** = indispensable, do not sign or publish without it; **level 2** = strong preference; **level 3** = trading currency. Trade level 3 to win level 2; do not concede level 1 without an internal decision. Give each point a proposed wording and a fallback, because the other side may refuse and the reader must know what to accept instead.

`niveau_detail`: `flash` = the 5 most serious points (level 1), no fallback; `standard` (default) = all points with fallback, plus the legally required mentions that are missing; `complet` = adds the clause-by-clause checklist, the missing market-standard clauses and the article on every line.

If no clause is unfavourable or unbalanced for the reading position, output « RAS — no clause unfavourable for this reading position. » plus one line recalling any legal duty of the reader that applies (vigilance, payment terms, mandatory mentions), and stop: a balanced document is a result. A black-list clause (consumer) is never RAS.

# Expected output format

Default format; an explicit request from the user prevails.

1. **Summary, 3 to 5 lines**: the verdict for the position (sign / sign after renegotiation / do not sign; publish / correct before publishing), the level-1 points, the parties and the test applied, and the decision asked of the reader.
2. **Parties, position, type** in one line, then the **computed figures** with their inputs.
3. **Findings** by theme (liability, term and renewal, price and payment, data, termination…), level 1 first. Table: clause (quoted, with number) | finding (rule and the fact it depends on) | risk | proposed wording | fallback | level 1/2/3. Each line is labelled Fact, Hypothesis or To check.
4. **Missing** (table: missing item | why required | proposed wording | level).
5. **Duties of the reader** that apply whatever the text says (vigilance, payment limits, mandatory mentions).
6. **Actions**, apart from the diagnosis: what, who, by when (including the last date to give notice).
7. **Open questions**: the facts that would change a finding.
8. One closing line: "This review orients a lawyer's review and is not legal advice." Say it once.

Output names: `supplier_contract_analysis` and `gtc_analysis` = parts 1, 2 and 5; `renegotiation_points` and `negotiation_points` = parts 3, 4 and 6 (use the `gtc_` and `negotiation_` names for `cgv_cgu`).

# Examples

<example>
| Clause (quoted) | Finding | Risk | Proposed wording | Fallback | Level |
|---|---|---|---|---|---|
| Art. 11: "The Buyer undertakes to purchase exclusively from the Supplier for 3 years." | Exclusivity with no price protection and no exit (Fact) | Locks the buyer in; a better offer or a failing supplier cannot be used | Exclusivity for [12] months only, with a most-favoured-price clause | Keep 3 years but add an exit right if the SLA is missed twice in 6 months | 2 |

*Why this works: the fallback is already written, so the line can be used in the meeting as it stands.*
</example>

<example>
| Clause (quoted) | Finding | Risk | Proposed wording | Fallback | Level |
|---|---|---|---|---|---|
| Art. 7: "The Seller alone determines whether the delivered goods conform to the order." | Consumer contract: black list R212-1 4°, irrefutably abusive and deemed unwritten (L241-1) even though the customer ticked "I accept" (Fact) | The Seller cannot rely on it; the legal guarantee of conformity (L217-3) applies as if the clause were absent | "Conformity is assessed against the order and the legal criteria; the customer may contact the Seller within [x] days of delivery." | Delete the clause | 1 |

*Why this works: it names the list and the number, not just "unbalanced", and the reader can see what is lost and what to write.*
</example>

<!-- Clause review points, the green / orange / red thresholds, the redline-with-fallback format and the three priority levels with their trade rule adapted from anthropics/knowledge-work-plugins, legal/skills/review-contract/SKILL.md (Apache-2.0, commit 33eeda1): rewritten for French law, from the buyer's, supplier's or user's side. Clause categories, thresholds and the finding format for standard terms (formerly cgv-checker) from the same source. See THIRD_PARTY.md. -->
