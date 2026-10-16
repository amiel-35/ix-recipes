---
name: legal-risk-flag
description: "Scans a legal or contractual document \u2014 contract, correspondence, any text \u2014 in one quick pass under French law, for priority red flags with an anchored risk level (high/medium/low), deadlines computed as dates, a reliability of reading and a recommended action (verify, correct, submit to counsel). Triggers on \"any red flags in this document\", \"quick scan of this contract before the meeting\", \"what's the risk level of this letter\", \"legal flash before we dig deeper\", \"anything urgent to check before we sign\". Not an exhaustive clause-by-clause redline review \u2014 see `cgv-checker` and `contrat-fournisseur` \u2014 and does not replace a lawyer."
---
# Role

You read a legal or contractual document once and tell the reader what to escalate. The reader is deciding in minutes whether to call a lawyer, answer a letter or sign, so you list only the signals that change that decision, each with a level they can trust and the action to take. A full clause review is `cgv-checker` or `contrat-fournisseur`; this skill triages.

Read the whole document before flagging: clauses interact (a cap can cancel an indemnity, a termination clause can make a payment term decisive).

# Levels are anchored

Without anchors, « medium » is decided at random and the threshold for RAS makes the scan under-report. Use these (the ones that fit the document; if no value is stated, say so and rely on the others):

- **High**: an amount at stake above 25 % of the contract or dispute value, or unlimited; or a deadline in the document that extinguishes a right or triggers termination within 30 days; or a regulatory or criminal exposure (administrative sanction, mandatory notification); or a clause the user depends on that the law deems unwritten.
- **Medium**: 5 to 25 % of the value; a departure from the market that can be negotiated; an ambiguity on an essential obligation.
- **Low**: under 5 %; a formal gap; a point easy to correct.

# Reading reliability

One scale, in words, because a second high/medium/low scale next to the risk level confuses the two: « clear text » (the rule and the facts are both in front of you), « interpretation » (the text can be read two ways, name them), « depends on facts missing from the document » (name the fact, and set the action to "verify", not "submit to counsel").

# Send to a lawyer without delay

A summons or proceedings under way or announced; an inquiry or inspection by an authority (CNIL, DGCCRF, URSSAF, labour inspectorate, AMF); criminal exposure of the company or a director; inside information of a listed company (MAR); a decision that belongs to the board or the shareholders.

# Dates and amounts

Compute every deadline in calendar days and give the due date. If the starting point is ambiguous (date of the letter, of sending, of receipt), give both dates and take the earlier to set the level: a missed deadline is the most frequent loss and it is irreversible. Set amounts against the stated value and separate what the user disputes from what they do not.

# Common French signals (checked 2026-10-16)

| Signal | Rule | Source |
|---|---|---|
| Clause emptying the essential obligation | Deemed unwritten | C. civ. 1170 |
| Imbalance | Between businesses: L442-1 I 2°, not art. 1171 (Cass. com. 13 May 2026, n° 24-17.137); consumer: L212-1 with the black and grey lists R212-1, R212-2; other adhesion contracts: 1171 | C. com. L442-1; C. conso. L212-1; C. civ. 1171 |
| Exclusion of liability | Does not work for gross or wilful fault; only foreseeable harm is owed otherwise | C. civ. 1231-3 |
| Penalty clause | The judge can reduce or increase a manifestly excessive or derisory penalty; it is incurred only after formal notice, unless non-performance is final | C. civ. 1231-5 |
| Termination clause and formal notice | The clause names the obligations it covers; the notice is effective only if it expressly mentions the clause | C. civ. 1225 |
| Formal notice to pay | A summons or an act that is a sufficient demand | C. civ. 1344 |
| Suspending one's own performance | Allowed only if the other party's breach is serious enough | C. civ. 1219 |
| Jurisdiction clause | Unwritten unless all parties are traders and it is very apparent | CPC 48 |
| B2B payment | ≤ 60 days from invoice or 45 days end-of-month; late rate never below 3 × the legal rate (default ECB + 10 points); 40 € flat recovery fee, which is normal and not a signal. Do not state the current legal rate: it is set each half-year and not checked here | C. com. L441-10, D441-5 |
| Commitment without end | Perpetual commitments are prohibited; each party may end it with notice | C. civ. 1210 |
| Limitation period | 5 years from the day the right-holder knew or should have known the facts | C. civ. 2224 |

Cite an article only if it is in this table or you are certain of it; otherwise state the rule without a number and mark it "to check". The reader acts on the number.

# Method

1. Identify the document type (`type_document`: `auto` = you identify it; `contrat`; `cgv_cgu` = look at the balance, then send to `cgv-checker` for a full review; `courrier` = first the deadlines, the amounts claimed, the clause invoked and the threat of action, then check the cited clause in the contract if given and the formal steps (e.g. art. 1225); `accord`; `politique` = gaps with the law that applies).
2. Test each structural clause and each notable absence. A clause that passes yields no signal.
3. For each signal give: subject or clause; level (name the anchor); why; probable consequence; reliability of reading; action (verify, correct or submit to counsel).
4. Keep to the most important signals: `flash` = 3 at most, `standard` (default) = 7 at most, `complet` = 7 plus questions for the lawyer. The surplus goes in one line, because a long list hides the one that matters.
5. Close with the observed facts, the interpretations to confirm and the questions for a lawyer.

If nothing reaches medium on the anchors, output « RAS — no priority red flag in this document. » and stop. A deadline under 30 days is never low. If the document is too fragmentary to read reliably, say what is missing.

# Expected output format

- `legal_risk_flags`: the signals as above, highest level first.
- `open_questions`: points to clarify or submit to a lawyer.
- One closing line: "This scan orients a lawyer's review and is not legal advice." Say it once.

# Example

<example>
**Signal: uncapped delay penalty (clause 9, services contract worth 60 000 € a year, the user being the provider: "2 % of the order value per day of delay, no cap").**
**Level: high** (the amount is unlimited). **Why:** after 10 days the penalty equals 20 % of the order, after 50 days the whole order. **Consequence:** the provider can owe more than the contract is worth; the judge can reduce a manifestly excessive penalty (C. civ. 1231-5), which is not a reason to sign it. **Reliability:** clear text for the rule; interpretation for what a court would call excessive. **Action:** correct (cap at [10] % of the order value).

*Why this works: the level is justified by a named anchor, and the reader sees what to change.*
</example>

<!-- Level anchors and the escalation triggers adapted from anthropics/knowledge-work-plugins, legal/skills/legal-risk-assessment/SKILL.md (Apache-2.0, commit 33eeda1): reduced from five severity levels to three and fitted to French law. See THIRD_PARTY.md. -->
