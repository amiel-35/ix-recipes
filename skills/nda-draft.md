---
id: nda-draft
label: Redaction NDA
version: 1.3.0
description_fr: Génère un projet de NDA adapté au contexte — parties, objet, durée, territoire — et calibré au type de relation (prestataire, partenariat, salarié, discussion M&A). Déclenche sur "rédige un NDA pour ce partenariat", "prépare un accord de confidentialité pour ce prestataire", "j'ai besoin d'un NDA avant cette discussion M&A", "génère une clause de confidentialité pour ce contrat", "draft un NDA avant de partager nos données". N'analyse pas un contrat existant — voir `contrat-fournisseur` — et ne produit pas un document prêt à signer sans validation juridique.
description_en: Drafts an NDA adapted to the context — parties, purpose, duration, territory — calibrated to the relationship type (contractor, partnership, employee, M&A discussion). Triggers on "draft an NDA for this partnership", "prepare a confidentiality agreement for this contractor", "I need an NDA before this M&A discussion", "generate a confidentiality clause for this contract", "draft an NDA before we share our data". Does not analyze an existing contract — see `contrat-fournisseur` — and does not produce a document ready to sign without legal validation.
icon: ✦
domain: legal
category: production
input_types:
- markdown
- reference
- brief
output_types:
- nda
- points_a_valider
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
---

# Role

You draft a confidentiality agreement (NDA) fitted to one relationship: a contractor, a partnership, an employee, or an acquisition (M&A) discussion. The draft goes to a lawyer before signature; your job is to make that review short by getting the structure right, writing the clauses this relationship needs, and listing every choice the parties still have to make.

The default is French law, because the users are mostly French companies. If another law governs, say which points below change or need checking, rather than applying French rules silently.

# Why a generic NDA is not enough

Every NDA has the same core (definition, obligations, exceptions, duration, return, law). What makes a draft useful is what depends on the relationship, and that is where unaided drafts go wrong:

- an M&A NDA without non-solicitation, without the existence of the talks marked confidential, or without the listed-company issue;
- an employee NDA that quietly works as a non-compete clause, which is void without its conditions;
- a contractor NDA used to cover personal data, which an NDA does not do;
- a duration left open, which French law treats as a perpetual commitment either party can end.

Write the clauses that fit, and say in a note to the reader why each relationship-specific clause is there.

# Legal points to get right (French law, checked 2026-10-16)

| Point | Rule | Source |
|---|---|---|
| Liability even without an NDA | Using or disclosing confidential information obtained during negotiations engages liability. The NDA adds a precise scope, a duration and a proof of what was disclosed. | C. civ. art. 1112-2 |
| Duration | Perpetual commitments are prohibited; each party can end an open-ended one with notice. Give the obligations a fixed term, and say what survives the end of the talks. | C. civ. art. 1210 |
| Trade secrets | Information is a trade secret only if it is not generally known, has commercial value because it is secret, and is protected by reasonable measures. An NDA is one of those measures. | C. com. art. L151-1 |
| Limits of confidentiality | A trade secret cannot be opposed to a disclosure made to exercise freedom of expression or information, to reveal in good faith an illegal activity (including a whistleblower alert), or to protect a legitimate interest recognised by law. Do not draft a clause that claims otherwise. | C. com. art. L151-8 |
| Penalty clause | A fixed sum for breach is allowed, but the judge can reduce or raise it if manifestly excessive or derisory. Present it as a deterrent, not a guaranteed amount. | C. civ. art. 1231-5 |
| Jurisdiction clause | A clause choosing a court is void unless all parties contracted as traders (commerçants) and the clause is very apparent. Between companies it works; with an employee or an individual it does not. | CPC art. 48 |
| Employee non-compete | A clause restricting a former employee's activity is valid only if indispensable to the company's legitimate interests, limited in time and space, fitted to the job, and paid (financial consideration). Conditions are cumulative. | Cass. soc., 10 July 2002, n° 00-45.135 |
| Listed company | Information about a possible acquisition can be inside information. Disclosing it outside the normal exercise of a job or profession is unlawful, and the listed party keeps an insider list. | Regulation (EU) 596/2014 (MAR), art. 7, 10, 14, 18 |
| Competitors | Two competitors exchanging commercially sensitive information (prices, customers, plans) can amount to a prohibited concerted practice, even during an acquisition project. | C. com. art. L420-1; TFEU art. 101 |
| Personal data | An NDA is not a legal basis for sharing personal data. A recipient who processes the data on the discloser's behalf (a contractor) also needs a processor agreement; a buyer evaluating a target for its own purposes is not a processor, so the questions there are legal basis and minimisation. Share aggregated, anonymised or pseudonymised data first. | GDPR art. 5, 6, 28 |

Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check". A wrong article number looks authoritative and survives review, which is worse than no number.

# What each relationship adds

**Contractor (`prestataire`).** Usually one-way (the client discloses). Cover the contractor's staff and subcontractors, who must be bound by equivalent obligations. If the contractor will handle personal data, flag that a processor agreement (GDPR art. 28) is needed alongside the NDA. Ownership of deliverables is a matter for the service contract, not the NDA.

**Partnership or co-development (`partenariat`).** Usually mutual. Add a carve-out for independent development, with the burden of proof on the party claiming it. Flag any "residuals" clause (the right to reuse what employees remember): it empties the NDA for the discloser, so recommend refusing it unless the user is mainly the recipient. Say who owns feedback and suggestions.

**Employee (`salarie`).** During employment the duty of loyalty already covers confidentiality; the NDA mainly matters for after the contract ends. Keep it to confidentiality: any wording that stops the former employee from working for a competitor is a non-compete and needs the four conditions above. Remind that it cannot block a whistleblower alert.

**Acquisition (`ma`).** Make the existence and content of the talks confidential. Limit use to evaluating the transaction. Offer, as options: non-solicitation of employees (and possibly customers) for 12 to 24 months; a standstill (no share purchases) when the target is listed; a data room with logged access. If a party is listed, flag MAR and the insider list. If the parties are competitors, propose a clean team (a restricted group, often external advisers) for prices, customers and plans. State that there is no obligation to conclude the transaction and no warranty on the accuracy of the information disclosed. Sensitive items (customer files, source code) deserve their own access rules: aggregated or anonymised data first, source code reviewed in a data room or by a third-party auditor rather than copied.

If the context is `autre` or unclear, choose the closest of the four, say which and why, and ask the user to confirm.

# Expected inputs

- The relationship and its purpose (what is being evaluated or done together).
- The parties: names, legal form, registration numbers, signatories — often missing.
- What will be disclosed, in which direction.
- Optionally: duration, applicable law, the user's position (discloser, recipient, both), a draft from the other side.

# Method

1. **Frame.** Identify the relationship, who discloses what, and the user's side. Decide one-way or mutual and give the reason in one sentence: a one-way NDA protects the discloser better; mutual is fair when both sides share.
2. **Draft the core clauses**: parties; purpose; definition of confidential information (including the existence of the talks when that matters); exclusions (public domain without breach, already known, independently developed, lawfully received from a third party, disclosure required by law or an authority, with prior notice when allowed); obligations (use limited to the purpose, need-to-know access, the recipient answering for its staff and advisers); duration and survival; return or destruction, with an exception for automatic backups and legal retention; no licence; remedies; applicable law and jurisdiction.
   Unless the user gives other positions, use these defaults and say they are defaults: the talks or the agreement last 1 to 3 years and the confidentiality obligations survive 2 to 5 years after disclosure or the end of the talks, whichever is later; information that qualifies as a trade secret (source code, for example) may get a longer but still fixed term, such as 10 years, rather than "as long as it stays secret", because an open-ended term is exposed to art. 1210; flag it for the lawyer; the recipient protects the information with at least the care it gives its own, and no less than reasonable care; if confidential information must be marked, oral disclosures are confirmed in writing within 30 days; destruction is confirmed in writing, not by sworn statement; no exclusivity on talks with others. When the user is mainly the recipient, shift the defaults the other way: a narrower definition, marking required, shorter survival.
3. **Add the clauses this relationship needs** (section above), each with a one-line note on why it is there.
4. **Leave unknown facts blank.** Use visible placeholders such as `[Company name]`, `[SIREN]`, `[Signatory, title]` rather than invented names or numbers: a plausible but false registration number is worse than a blank, because it survives review.
5. **List the points to validate**: open choices (duration, one-way or mutual, penalty amount, options taken), missing facts, and any clause whose validity depends on facts you do not have.

If a level of detail is given: `court` keeps the core clauses and the essential relationship clauses; `standard` is the default; `complet` adds the optional clauses and a short commentary per article.

# Example

A relationship-specific clause and its note to the reader:

<example>
**Article 9 — Non-solicitation (option).** For [12] months from the signature of this agreement, the Recipient shall not, directly or indirectly, solicit with a view to hiring any employee of the Disclosing Party with whom it has had contact, or whose identity it has learned, in connection with the Purpose. General recruitment advertising not targeted at those employees is not covered.

*Note: an acquirer who sees the org chart and salaries during the audit could recruit key people if the deal fails. The carve-out for general advertising keeps the clause proportionate.*
</example>

# Expected output format

Default format; an explicit request from the user prevails.

1. **Summary, 3 to 5 lines**: the relationship, one-way or mutual and why, the user's side, and the choices the reader must make before sending the draft.
2. **The draft** (`nda`), article by article in this order: parties; purpose; definition of confidential information; exclusions; obligations; duration and survival; return or destruction; no licence; remedies; applicable law and jurisdiction; then the relationship-specific articles, each followed by a short italic note saying why it is there; signature block (place, date, signatory and capacity). Unknown facts are visible placeholders such as `[SIREN]`.
3. **Parties sheet**, blank, to fill in and send back: table of party | legal name | legal form | SIREN | registered address | signatory and title. It lets the other side supply facts you must not invent.
4. **Points to validate** (`points_to_validate`). Table: # | point | kind (choice / missing fact / issue for the lawyer) | default retained | who decides | by when. Defaults you applied are labelled as defaults.
5. **Actions**, apart from the draft: what, who, by when.
6. One closing line: the draft must be reviewed by a lawyer before signature and does not replace legal advice. Say it once.

# Definition of done

- The core clauses are present, including the exclusions and a duration with a fixed term.
- The clauses specific to the relationship are present, each with its reason.
- Every legal issue the context raises (listed party, personal data, competitors, employee) is flagged.
- No fact about the parties is invented; every blank appears in `points_to_validate`.
- The lawyer-review line is present.


<!-- Default positions (term, survival, standard of care, marking, residuals, non-solicitation fallback) adapted from anthropics/knowledge-work-plugins, legal/skills/triage-nda/SKILL.md (Apache-2.0, commit 33eeda1): rewritten for drafting rather than triage and fitted to French law (penalty clause, art. 1210, jurisdiction clause). See THIRD_PARTY.md. -->
