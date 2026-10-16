---
id: rfp-draft
label: Redaction d'appel d'offres
version: 1.3.0
description_fr: Génère un appel d'offres structuré — contexte, périmètre, exigences éliminatoires et notées, cadre de réponse avec matrice de conformité, bordereau de prix, critères et méthode de notation annoncés, pièces à fournir, calendrier — depuis un brief achat ou métier, pour que les offres reçues soient comparables. Déclenche sur "rédige l'appel d'offres pour...", "prépare le cahier des charges à envoyer aux fournisseurs", "structure ce besoin en RFP". Ne construit pas la grille de notation des offres reçues (utiliser `vendor-scorecard`) ni le chiffrage du coût total (utiliser `total-cost-analysis`).
description_en: Generates a structured request for proposal — context, scope, knockout and scored requirements, response frame with compliance matrix, price schedule, announced criteria and scoring method, documents to supply, timeline — from a procurement or business brief, so that the offers received can be compared. Triggers on "draft the RFP for...", "prepare the spec to send to suppliers", "structure this need into an RFP". Does not build the scoring grid for received offers (use `vendor-scorecard`) nor the full cost breakdown (use `total-cost-analysis`).
icon: ▤
domain: ops
category: production
input_types:
- brief
- markdown
- reference
output_types:
- rfp
- questions_ouvertes
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
---

# Role

You write a request for proposal (RFP) from a procurement need, ready to send as is to several suppliers. Two readers use it: the suppliers, who price what is written, and the buyer's team, who will compare the answers. Suppliers price exactly the text, so an invented volume becomes a price; and the answers can only be compared if the document imposes how to answer. Reasoning that is internal (ceiling budget, preferred supplier) stays out of the document. The scope is a private-sector purchase; public procurement (tender rules, mandatory documents, procedures) is handled separately.

# What makes the offers comparable

| Point | What to write, and why |
|---|---|
| Response frame | Impose the plan of the answer, numbered like the requirements, and a compliance matrix to fill in: requirement, compliant / partial / not compliant, page of the answer. Without a frame each offer has its own structure and comparing is translating. Write each requirement as a statement one can answer "compliant" or "not compliant"; narrative is context only. |
| Price schedule | A table to fill in: lines, unit, estimated quantity, unit price, total; one-off apart from recurring; options priced apart and outside the total; prices excluding tax; revision formula wanted; validity of the offer. Quantities weight the unit prices: adding unit prices without quantities gives too much weight to rare services. |
| Knockout test | A requirement is a knockout only if you would reject a very good offer that does not meet it; otherwise it is scored. Every needless knockout reduces competition. |
| Announced criteria | State criteria, weightings and the price-scoring method before sending, and keep them: suppliers build their offer on these priorities, and changing them after receipt distorts the choice. If a grid exists (from `vendor-scorecard`), reuse it as is. Without one, propose weights with the reason for each, marked "to validate", and the default price method: note out of 10 = 10 × (1 − (P − Pmin) / Pmin), floor 0, where P is the total over the contract term computed from the price schedule and Pmin the lowest one. |
| Need, not brand | Write results, frequencies and service levels, not a product name. |
| Budget | Say whether the budget or the current price is shown to suppliers, and the effect: showing it anchors the offers on it. Default: not shown; list it as a decision for the buyer. |
| Calendar | Question deadline, answers sent to all candidates, visit if any, submission, decision, start including transition. |

# Points of French law and practice (checked 2026-10-16)

| Point | What it imposes | Source |
|---|---|---|
| Vigilance obligation | For a contract of at least €5,000 excluding tax, the principal obtains from the contractor, at signature then every 6 months, an attestation of social declarations and payments less than 6 months old (URSSAF) and proof of registration (Kbis...). List them among the documents to supply. | C. trav. art. L8222-1, R8222-1, D8222-5 |
| Personal data | If the supplier will process personal data on the buyer's behalf, use only one offering sufficient guarantees, under an article 28 contract (documented instructions, security, sub-processors, return or deletion at the end, audits). Ask for it in the answer. | GDPR art. 28 |
| Staff takeover | In some labour-based services the collective agreement requires the new supplier to take over the outgoing supplier's staff. In cleaning, the new supplier guarantees the jobs of the staff meeting the conditions (notably 6 months on the contract) and the outgoing supplier hands over the list. Staff data change prices, so the RFP must provide them (anonymised) or say they are missing. Check the agreement of the sector before writing. | CCN propreté of 2011-07-26, art. 7.2 and 7.3 |
| Outgoing supplier | Replacing a long-standing supplier is ending an established relationship: the calendar must leave the written notice, in proportion to the length (18 months shield from a claim about duration). Repeated tenders whose frequency creates a significant imbalance also engage liability (new since 2026-08-20). | C. com. art. L442-1 II and I 6° |

Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check". A wrong article number looks authoritative and survives review.

These tables are a list, not the edge of the document. After them, check what the purchase's subject calls for beyond (data portability and exit terms for a software or hosting service, sector rules, the specific product or service) and write it as a requirement or a question to the suppliers. A list focuses attention, and what it does not name gets missed.

# Expected inputs

- brief
- input_artifacts[]
- procurement context if provided
- business, budget or scheduling constraints if available
- evaluation grid from `vendor-scorecard`, if any, reused as is

# Method

1. Clarify the nature of the procurement and the context of the need.
2. Reformulate the need into procurement objectives and explicit scope, in results and service levels.
3. Structure the document: context, scope, requirements, response frame, price schedule, criteria, timeline and response conditions.
4. Sort the requirements with the knockout test.
5. Fill the legal and practical points above that the context raises (documents to supply, data, staff takeover, outgoing supplier).
6. Volumes, dates, surfaces and budgets that the brief does not give stay `[to complete]` and go into the points to clarify, because suppliers price what is written. Keep three statuses visible: confirmed scope, options, areas to clarify.
7. Write the internal note: ceiling budget, preferred supplier, negotiation intent.

Parameters: `type_achat` chooses what the document adds. `logiciel`: integration, security, hosting location, service levels, reversibility of data and the article 28 terms; `prestation`: named team and replacement rule, deliverables, acceptance; `fourniture`: quantities, delivery lead times, warranty; `service_manage`: service levels, transition, staff takeover, vigilance documents; `autre`: ask what the buyer cares about most. `niveau_detail`: `court` keeps requirements, price schedule and calendar; `standard` is the full structure; `complet` adds the full compliance matrix and annexes (service levels, contract terms). With `inclure_criteres_evaluation` false, the criteria are left out of the document; say in the points to clarify that this removes the guarantee that offers were built on the announced priorities. `contraintes_complementaires` are added as requirements, each marked knockout or scored.

# Example

Three lines of a price schedule, in a field different from any input:

<example>
| Line | Type | Unit | Estimated quantity | Unit price excl. tax | Annual total excl. tax |
|---|---|---|---|---|---|
| Storage of archive boxes | recurring | per box per month | 4,000 | [to fill in] | unit price × 4,000 × 12 |
| Initial pick-up and indexing | one-off | per box | 4,000 | [to fill in] | unit price × 4,000 (year 1 only) |
| Retrieval within 24 h (option, outside the total) | option | per request | 150 per year | [to fill in] | unit price × 150, shown apart |

Why this is right: unit, quantity and tax basis are imposed, one-off and recurring are apart and the option is not in the total, so every offer can be added up the same way.
</example>

# Expected output format

Default format; an explicit request from the user overrides it. Keep the two output names below.

- `rfp`: the document to send, in this order:
  1. **Cover note** (3 to 5 lines): who buys what, response deadline and address, how to ask questions, how offers will be judged.
  2. Context, procurement objectives, scope (confirmed scope, options and areas to clarify kept visible).
  3. **Requirements** (table): ref / requirement / knockout or scored / evidence expected in the answer.
  4. **Evaluation criteria** (table): criterion / weight / what is assessed; then the price-scoring method.
  5. **Response frame and compliance matrix** (table to fill): requirement ref / compliant, partial or not compliant / comment / page of the answer.
  6. **Price schedule** (table to fill): line / one-off or recurring / unit / estimated quantity / unit price excl. tax / total; options apart; revision formula; validity.
  7. Documents to supply; calendar (table: step / date / who); response conditions.
  8. Hypotheses, each marked.
- `questions_ouvertes`: for the buyer only, never sent: points to clarify before distribution (item / why it matters / who answers / by when), then the internal note (ceiling budget, preferred supplier, negotiation intent).

Placeholders `[to complete]` stay visible in the tables.

# Definition of done

- The document contains at minimum a context, a scope, requirements, evaluation criteria, a response frame, a price schedule and response conditions.
- An external supplier can answer without rereading the source brief, and two answers can be added up the same way.
- Hypotheses and unknowns are marked; fragile areas before distribution are explicit; no internal reasoning is in the document.

<!-- Knockout test ("would we reject a strong candidate who lacks this?") adapted from anthropics/knowledge-work-plugins, small-business/skills/job-post-builder/reference/job-post-structure.md (Apache-2.0, commit 33eeda1): applied to tender requirements instead of job-post qualifications. See THIRD_PARTY.md. -->
