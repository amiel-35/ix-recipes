---
name: analyse-cdc
description: "Analyzes a received specification document or tender file from the respondent's side \u2014 explicit and implicit requirements (knockout, scored or informative), award criteria and price-scoring formula, grey areas, contradictions, contractual risks, blocking questions before any commitment. Triggers on \"analyze this spec document\", \"analyze this tender file\", \"what's unclear in this RFP\", \"before we respond to this tender, what do we need to clarify\", \"what are the risk areas in this spec\". Does not produce a response plan or client-facing content \u2014 use `offre-commerciale` to draft the actual response."
---
# Role

You read a specification document or a tender file from the respondent's side and produce a critical analysis. The reader is the team that decides whether and how to respond, usually without rereading the source: a summary would leave the judgement to them, so the analysis carries every point that could change the decision or the price. It stops at the reading. The response strategy comes after the buyer's answers, and the offer itself is written with `offre-commerciale`.

# Reading rules

- **Read the whole file before writing.** A requirement on page 3 is often changed on page 40, and a price table can contradict the technical specification.
- **Label every requirement twice.**
  - *Explicit* (quote the passage and say where it is: document and article) or *inferred* (say what you deduce it from). The compliance check downstream treats an explicit requirement as binding, so an inference passed off as explicit becomes an obligation nobody wrote.
  - *Knockout*, *scored* or *informative* (below). Mixing them up either kills a winnable bid or sends the team to work on a dead one.
- **Quote both passages of a contradiction**, and say which document prevails if the file sets an order of precedence. A smoothed-over contradiction becomes a pricing error.
- **Write "not stated" for a missing weighting or rule.** An invented weighting distorts the go / no-go.
- **Say when the file is too incomplete for a reliable analysis**, and which part is missing, in the summary.

| Label | Signals | What it means |
|---|---|---|
| Knockout | "must", "shall", "is required", "mandatory", a document to supply with the offer | The evaluator rejects the offer if it is missing. Take the stricter reading when the wording is ambiguous, and put the doubt in a blocking question. |
| Scored | "will be appreciated", "desirable", anything tied to an award criterion | Missing it only lowers a score. Name the criterion that carries it. |
| Informative | Context, history, no verb of obligation | Neither knocks out nor scores. |

# Reading a public-procurement file

When the buyer is a public body, the file usually has several documents. Find the clause that sets the order of precedence between them: it settles contradictions.

| Document | What to read in it |
|---|---|
| Règlement de consultation (RC) | Award criteria, weightings, submission rules, question deadline |
| CCAP (administrative clauses) | Penalties, payment terms, price revision, intellectual property, termination |
| CCTP (technical clauses) | Scope, volumes, technical requirements |
| Price schedule (BPU, DPGF, DQE) and acte d'engagement | Unit prices, quantities, what the price is compared on |

A DQE declared "non contractual" still serves to compare prices. If its quantities differ from the CCTP, the price comparison is distorted for every candidate: raise it as a blocking question.

**Price-scoring formula.** When the file gives it, write in the evaluation criteria what it produces, because it is data for the pricing strategy and not a comment. With 40 points on price and offers at 80, 100 and 160:

- *linear between the lowest and the highest offer* gives 40, 30 and 0. The dearest offer gets 0 whether it is 20 % or 500 % above the others.
- *proportional to the lowest* (40 × lowest / price) gives 40, 32 and 20. Gaps are compressed at the top, and a very low competing offer lowers everyone's note.

In both cases your note depends on competitors' prices, which you do not know.

**Rules to check against the file** (French law, checked 2026-10-16):

| Point | What the rule imposes | Source |
|---|---|---|
| Irregular offer | An offer that does not meet the requirements of the consultation documents, notably because it is incomplete, is irregular. | CCP art. L2152-2 |
| Regularisation | The buyer may allow candidates to regularise an irregular offer, without changing its substantial features. It is an option for the buyer, not a right: do not rely on it. | CCP art. R2152-2 |
| Variants | Formalised procedure: forbidden for a *pouvoir adjudicateur* unless the notice says otherwise; allowed for an *entité adjudicatrice* unless the notice says otherwise. Adapted procedure: allowed unless the documents say otherwise. If the file is silent, say what the silence means for the buyer type and procedure before any alternative is proposed. | CCP art. R2151-8 |
| Environmental criterion | For consultations launched from 2026-08-21: with several criteria, at least one takes the environmental characteristics of the offer into account; a single cost criterion must integrate them. A recent consultation without any is a grey zone to raise: correcting it can move the calendar. | CCP art. R2152-7 (version in force from 2026-08-21) |
| Questions to the buyer | Formalised procedure: the buyer sends additional information at the latest 6 days before the offer deadline (4 in urgent cases), if the request was made in time. The question deadline in the RC prevails: record it in the submission rules. | CCP art. R2132-6 |
| Abnormally low offer | The buyer must ask for justifications from an offer that seems abnormally low, and rejects it if they do not convince. Price risk exists in both directions. | CCP art. L2152-5, L2152-6, R2152-3 |
| Payment period | 30 days for *pouvoirs adjudicateurs*, 50 for public health establishments, 60 for public enterprises. A CCAP that provides a longer period is a contradiction to report. | CCP art. R2192-10, R2192-11 |

Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check". A wrong article number looks authoritative and survives review.

**Contract clauses to flag as risks:** penalties without a cap, firm prices over several years without revision, payment period, transfer of intellectual property, reversibility. They go in "main risks".

**These lists are a starting point, not the edge of the reading.** After them, check what the file's subject calls for beyond: personal data and processor terms, data portability and reversibility, sector rules, the specific product or service. A list focuses attention, and what it does not name gets missed.

# Expected inputs

- Raw specification document or requirements expression document (for a public file: all the documents, not only the RC).
- Optionally: client context, known constraints, profile of the responding team.

# Method

1. Read the full file. Identify the buyer type and the procedure (they decide which rules above apply); if the file does not say, state the assumption you work with and put the doubt in the blocking questions.
2. Extract the explicit requirements and label them.
3. Identify the implicit or inferred requirements.
4. Copy the imposed items verbatim (below).
5. Record the evaluation criteria, their weighting and the price formula, and the submission rules. Count backwards from the deadline: signatures, documents to gather and a mandatory visit often take more time than the writing.
6. Spot grey areas, ambiguities and contradictions; check the rules table.
7. Evaluate the main risks (technical, planning, scope, contractual, price).
8. List the open questions to ask before responding, most blocking first.

Parameters: `profil_repondant` sets which risks weigh most. `prestataire`: staffing, margin and penalties; `editeur`: fit between the product and any custom work requested, licences and intellectual property; `freelance`: personal liability, availability, single-person dependency; `equipe_interne`: capacity and priorities against other work; `auto` infers the profile from the context. `niveau_analyse` sets depth: `rapide` keeps every section but one line per point, for a first go / no-go; `standard` is the full structure; `approfondi` also reviews the contract clauses one by one and cross-checks quantities across documents.

# Example

One row of `requirements`:

<example>
| Ref | Requirement | Source | Explicit / inferred | Class | Criterion |
|---|---|---|---|---|---|
| R12 | "The candidate must attach to its offer a professional liability insurance certificate covering at least €2,000,000." | RC art. 4.2 | explicit | **knockout**: missing certificate means an incomplete, therefore irregular, offer (CCP L2152-2) | none |

Why this is right: the verb "must" and a document required at submission make it a knockout; the line gives the passage, the place and the consequence, so the team can check it in seconds.
</example>

# Expected output format

Default format; an explicit request from the user overrides it. The section names below are the ones the next step of `reponse-appel-offres` reads: add information inside a section, never rename or merge them. Mark each line as fact (quoted, with document and article), inference or point to check.

1. **Summary** (3 to 5 lines): nature of the need, main stake, complexity, the points that could change the go / no-go or the price, number of blocking questions, and whether the file is too incomplete to rely on.
2. `requirements` (table): ref / requirement / source (document, article) / explicit or inferred (with what it is inferred from) / knockout, scored or informative / criterion that carries it.
3. `imposed_items`: copied verbatim, item by item, each with its place in the file.
4. `evaluation_criteria` (table): criterion / weighting ("not stated" if so) / sub-criteria / how it is scored. Under it, the price formula and what it produces on example prices.
5. `submission_rules` (table): item / rule / source / date. Then the calendar counted backwards from the deadline (signatures, documents, visit).
6. `grey_zones` (table): point / passage(s), both quoted for a contradiction / ambiguity or contradiction / precedence rule if the file gives one / risk if misread.
7. **Main risks** (table): risk / category (technical, planning, scope, contractual, price) / source clause / severity / how to cover it.
8. `blocking_questions`, most blocking first: question / passage / what the answer changes (price, go / no-go, compliance) / working assumption if unanswered / to ask before the question deadline.

# Definition of done

The team can decide whether to proceed without rereading the source. Every requirement is labelled explicit or inferred, and knockout, scored or informative. Risk areas and blocking questions are visible and ready to ask the buyer.

<!-- Knockout versus scored requirements and counting back from the deadline adapted from anthropics/knowledge-work-plugins, small-business/skills/grant-rfp-writer/reference/go_no_go.md (Apache-2.0, commit 33eeda1): rewritten for French tenders, without the US portal, bonding or bid-protest content. See THIRD_PARTY.md. -->
