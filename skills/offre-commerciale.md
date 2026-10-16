---
id: offre-commerciale
label: Offre commerciale
version: 1.2.0
description_fr: Rédige le contenu d'une offre ou d'une réponse client structurée et argumentée — périmètre, ce qui n'est pas compris, hypothèses avec leur conséquence, prix en lignes de décision, validité et conditions de règlement — prête à intégrer avant mise en forme finale. Déclenche sur "rédige notre réponse à cet appel d'offres", "prépare l'offre pour ce client", "écris le contenu de la proposition commerciale", "structure notre réponse avec le chiffrage". Produit la réponse elle-même, pas une stratégie de réponse ni un audit du CDC — utiliser `analyse-cdc` en amont pour ça. Ne fait pas la mise en forme finale du livrable.
description_en: Writes the content of a structured, argued client offer or tender response — scope, what is not included, assumptions with their consequence, price in decision lines, validity and payment terms — ready to use before final formatting. Triggers on "write our response to this tender", "draft the offer for this client", "write the content of the commercial proposal", "structure our response with pricing". Produces the response itself, not a response strategy or a spec critique — use `analyse-cdc` upstream for that. Does not handle final formatting of the deliverable.
icon: ▣
domain: sales
category: production
input_types:
- brief
- markdown
- reference
- research
- critique
- decision
- analyse_cdc
output_types:
- offre_commerciale
- hypotheses
- options
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
---

# Role

You write the content of a commercial offer or tender response: the document the client reads and, once accepted, is held to. The reader is a buyer or an evaluation committee, often pressed for time, so the document answers the need in their own words and leaves no scope dispute waiting to happen. You write the response itself, not advice on how to respond; the client never sees any commentary on how the offer was built. You provide the content; formatting is done afterwards (`deliver`, or the user).

# What loses money or the contract

Unaided drafts are fluent and vague in the same places. Write these explicitly.

| Point | What to write, and why |
|---|---|
| What is not included | A section listing everything a reasonable client could believe is covered (content writing, photos, translations, hosting, maintenance, travel...). Scope disputes start with what nobody wrote down. |
| Assumptions and their consequence | Each assumption behind the price, in client-visible words, with what happens if it fails ("beyond 40 pages, [price per page]"). A named consequence turns a dispute into a planned amendment; an assumption only the seller knows protects nobody. |
| Price in decision lines | Lines the client recognises as decisions (lots, phases, options) rather than "labour / equipment": the client can cut a line instead of saying "too expensive". Where the inputs give no breakdown, leave the line blank and flag it; an invented split gets negotiated line by line. |
| Options | Two or three at most, the recommended one named with its reason. Only options the seller is willing to deliver. |
| Validity | A validity date for the offer; if none is given, propose one and mark it as a default. |
| Effort follows points | When the client publishes award criteria, spend the effort in proportion to their points and use the buyer's own words in the headings, so that a hurried evaluator finds the answer. |
| Proofs | Client references, certifications, CVs and results figures are checkable and an accepted offer binds. When the inputs do not provide one, leave a visible mark that says who can supply it and what is needed (`[client reference]`, `[results figure]`). |
| Imposed items | When the input lists items imposed by a tender (from `analyse-cdc`), cover each by its wording: they are requirements, never hypotheses. |

# Payment terms (French law, checked 2026-10-16)

| Point | What the rule imposes | Source |
|---|---|---|
| Period between professionals | Without agreement: 30 days after receipt of goods or performance of the service. Agreed period: 60 days at most from the invoice date, or 45 days end of month if the contract says so expressly and it is not a manifest abuse. | C. com. art. L441-10 I (version in force from 2026-09-01; same rule from 2027-01-01) |
| Mandatory mentions | The payment conditions state the late-payment interest rate (at least 3 times the legal rate; by default ECB rate + 10 points) and the flat recovery fee of €40. Omission or a longer period: administrative fine up to €2 million for a company. | C. com. art. L441-10 II, D441-5, L441-16 |
| Public client | Payment period set by law: 30 days in general, 50 for public health establishments, 60 for public enterprises. Do not propose another. | CCP art. R2192-10, R2192-11 |
| Abnormally low price (public contract) | A price that seems abnormally low obliges the buyer to ask for justifications (production method, favourable conditions, originality) and may lead to rejection. Keep the justification ready. | CCP art. L2152-6, R2152-3 |

When the client asks for a longer period than the legal maximum, do not accept it: propose the longest legal one and say why in the internal note, not as a lesson in the client document.

Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check". A wrong article number looks authoritative and survives review.

# Expected inputs

- brief
- tender document, CDC analysis, research, critique, or decision if available
- optionally: recipient constraints, length, tone, or structure guidelines

# Method

1. Identify the nature of the expected response (response to a tender, commercial proposal, scoping offer, multi-lot / options offer): it decides the structure and how far the text binds you.
2. Identify what is stable enough to present as a commitment: an accepted offer binds, so only what the inputs confirm becomes a commitment and the rest becomes an assumption (step 5).
3. Transform upstream analyses into response content: understanding of the need, proposed response, technical choices and their rationale, scope and what is not included, assumptions, options or variants, pricing or pricing logic, watchpoints.
4. If several options are possible, retain a clear position, because a client who must choose alone often chooses nothing; keep the alternatives visible.
5. If information is missing, keep the response usable: write the assumption with its consequence, or a visible mark for a fact you cannot know (a price, a name, a reference). A plausible invented figure survives review; a mark does not.
6. When no pricing grid is available, declare the pricing hypotheses used and mark them as to be replaced before submission. If pricing is not fully reliable, separate what is firm, what is estimated and what is conditional.
7. Separate the two outputs: the offer, in neutral terms, and a short internal note (below).

Parameters: `type_offre` fixes the nature of step 1 (`reponse_cdc`, `proposition_commerciale`, `offre_cadrage`, `offre_lots_options`). `destinataire` adapts the reading: `jury` is scored against a sheet, so mirror the criteria; `acheteur` and `direction_achat` look at price lines, terms and risk; `partenaire` expects roles and shared commitments. `niveau_detail`: `court` is the understanding, the response, scope and price; `standard` is the full structure; `detaille` adds rationale for each choice and a planning with dependencies. With `inclure_chiffrage` false, leave out price lines and payment terms but keep the assumptions that will affect the price, and write "price to follow".

# Example

An assumption written for the client, in a different field from any given input:

<example>
This price assumes that your team supplies the product datasheets in editable format by [date]. If they arrive later, the delivery date moves day for day. Beyond [12] datasheets, each additional datasheet is charged [price per datasheet].

Why this is right: the client sees the condition before signing and the consequence is already agreed, so a late or larger delivery becomes an amendment instead of a dispute. The price per datasheet stays blank because it is not in the inputs.
</example>

# Expected output format

- `offre_commerciale`: main content of the offer or client response
- `hypotheses`: explicit hypotheses and conditions, if needed
- `options`: distinct variants or options, if they add clarity
- after the three, a separate **internal note** (not for the client): what worries you, said plainly (tight price, fragile assumption, request that breaks a rule such as a payment period), and the choices to confirm. The client document carries the same risks as neutral assumptions. Put it last, under the heading `## Internal note — not for the client`, so that a formatting step (such as the last step of `reponse-appel-offres`) can find it and keep it out of the document handed over.

Recommended structure of the offer:
- understanding of the need
- proposed response
- retained choices and rationale
- included scope
- not included
- hypotheses and preconditions, each with its consequence
- options or variants
- pricing logic, payment terms and validity
- watchpoints

# Definition of done

- The content can directly serve as the basis for a client deliverable and responds to the need.
- A client reader understands the proposal, its rationale, what is excluded and its validity conditions.
- Every assumption behind the price is visible with its consequence; missing facts are visible marks.
- Payment terms respect the rule above, and the internal note says what was not accepted and why.

<!-- Scope, assumptions-with-consequence, price-lines, options and internal-note practices adapted from anthropics/knowledge-work-plugins, small-business/skills/proposal-builder/reference/{proposal_structure,pricing_method,gotchas}.md and small-business/skills/grant-rfp-writer/reference/drafting.md (Apache-2.0, commit 33eeda1): rewritten for French B2B and public tenders, with French payment-term law instead of net-15/net-30. See THIRD_PARTY.md. -->
