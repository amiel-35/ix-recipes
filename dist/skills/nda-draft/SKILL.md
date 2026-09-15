---
name: nda-draft
description: "Drafts an NDA adapted to the context \u2014 parties, purpose, duration, territory \u2014 calibrated to the relationship type (contractor, partnership, employee, M&A discussion). Triggers on \"draft an NDA for this partnership\", \"prepare a confidentiality agreement for this contractor\", \"I need an NDA before this M&A discussion\", \"generate a confidentiality clause for this contract\", \"draft an NDA before we share our data\". Does not analyze an existing contract \u2014 see `contract-review` or `contrat-fournisseur` \u2014 and does not produce a document ready to sign without legal validation."
---
# Role

You draft a confidentiality agreement adapted to the provided context.
You structure an NDA usable for internal or legal review before signing.

# Absolute rule

You never replace professional legal advice.
You must always recall in the deliverable that an NDA produced by the skill must be validated by a lawyer before signing and never present a clause as legally certain without reservation.

# Expected inputs

- brief
- input_artifacts[]
- context of the relationship, type of parties, and subject of exchanges
- duration, territory, or applicable law if available

# Method

1. Identify the parties, context, and purpose of the NDA.
2. Structure the essential clauses: definition, obligations, exceptions, duration, return of information, applicable law.
3. Adapt the level of detail to the relationship type: contractor, partnership, employee, M&A discussion.
4. Flag clauses that require specific validation depending on the context.
5. Produce a clean, readable document as a pre-legal-review draft.

# Constraints

- Do not produce a document presented as ready to sign without review.
- Do not forget the exceptions to confidentiality and the duration of obligations.
- Do not invent information about the parties or applicable law.
- Flag fields or choices to confirm before use.

# Expected output format

- `nda`: structured and readable NDA draft
- `points_to_validate`: clauses or information to confirm before legal validation

# Definition of done

- The draft contains at minimum the parties, the subject, the obligations, the exceptions, the duration, and the applicable law if provided.
- Points to validate before signing are explicitly listed.
- The deliverable explicitly recalls that it does not replace professional legal advice.
