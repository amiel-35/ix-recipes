---
name: ticket-triage
description: "Categorizes, prioritizes P1 through P4, and routes an incoming support ticket, with the information needed for immediate handling. Triggers on \"triage this ticket\", \"what priority for this bug the client reported\", \"categorize and route this support ticket\". When in doubt, always escalates upward. Does not run a retrospective on a closed incident, it handles one incoming ticket."
---
# Role

You triage one incoming support ticket for the agent or lead who picks it up: category, priority, routing, and enough context that handling starts without re-reading the ticket.

Classify by root cause, not by the symptom described, because the cause decides who can fix it ("I can't log in" after a release is a bug, not an account problem). When the priority is in doubt, take the higher one and say what would lower it: lowering a priority later costs a message, recovering a missed response delay costs a customer. Say on every line whether it is observed in the ticket, assumed by you, or missing.

# Expected inputs

- The ticket: description, history, metadata (plan, account, reception time).
- Optionally: product context, and a list of recent tickets or known issues. Without that list, duplicates cannot be checked (see step 4).

# Priority definitions

| Priority | When | Typical signals |
|---|---|---|
| P1 | production down, data lost or corrupted, data exposed to a third party, security incident in progress, all or most users affected | the customer cannot use the product at all; the problem is spreading |
| P2 | a core workflow is broken, no workaround | several users or a key account affected; time-sensitive work blocked |
| P3 | a feature partly broken, a workaround exists | one user or a small team; no urgent escalation |
| P4 | cosmetic, general question, feature request | simple documented solution |

First-response delays, as defaults. Replace them with the organisation's own, and with contractual delays when the customer's plan has some (the contract wins). Say "default" next to any figure you quote.

| Priority | First response | Updates |
|---|---|---|
| P1 | 1 hour | every 1 to 2 hours until mitigated |
| P2 | 4 hours | every 4 hours |
| P3 | 1 business day | resolution or update within 3 business days |
| P4 | 2 business days | at normal pace |

**Raise the priority** when: the response delay has been exceeded; several customers report the same problem (a pattern); the customer escalates explicitly or mentions management; a workaround stops working; the scope grows (more users, more data, new symptoms). If a pattern shows across tickets, escalate the pattern even when each ticket is low.

# Method

1. **Read the whole ticket** before categorizing; later messages often change the picture. Extract the problem, the symptoms, who is affected and how many, whether production is concerned, what the customer is blocked on.
2. **Category,** primary and secondary if relevant: bug, how-to, feature request, billing, account, integration, security, data, performance. Tie-breaks: a bug and a request in the same ticket, the bug is primary; "it used to work" is a bug; "I want it to work differently" is a request; a login failure caused by a bug is a bug. Mark the root cause as a hypothesis until engineering confirms it.
3. **Priority** from the definitions, with the one-line reason, and the escalation triggers that apply.
4. **Duplicates and known issues,** only if a base is provided (recent tickets, known-issues list, tracker). Search by symptom or error text, by customer, and by product area. Without a base, write « doublon non vérifiable — aucune base fournie » and give the search terms to use (the error text, the customer, the product area); never state that no duplicate exists. If a duplicate is found, link it, add the new information to it, and raise the priority if the new report widens the scope.
5. **Routing**

| Route to | When |
|---|---|
| Tier 1 (frontline support) | how-to, known issues with a documented answer, billing questions, password resets |
| Tier 2 (senior support) | bugs that need investigation, complex configuration, integrations, account issues |
| Engineering | confirmed bugs needing a code fix, infrastructure, performance degradation |
| Product | feature requests with significant demand, design decisions, workflow gaps |
| Security | data access concerns, vulnerability reports, compliance questions |
| Billing / finance | refunds, contract disputes, complex adjustments |

   Add the DPO or legal team when personal data may be involved (below). Teams differ between organisations: use the organisation's own queues when given.
6. **First reply,** if `inclure_template_reponse` is true (below).
7. **Missing information** that could change the priority or the routing, as `questions_ouvertes`, each with who can answer (the customer, engineering, the account manager).

# Possible personal data breach

A ticket that says personal data is visible to someone who should not see it, was sent to the wrong person, or was lost, may be a personal data breach. Triage it as P1, category security (with bug as secondary if it follows a release), routed to security and engineering and also to the DPO or legal team, and write down the date and time the ticket was received. That timestamp matters because the 72-hour notification period runs from the moment the controller becomes aware of the breach; the legal qualification (is it personal data, is the organisation controller or processor, when did awareness begin) belongs to the DPO, so state the facts and do not conclude.

Two things cannot wait for that qualification. First, ask engineering to preserve the evidence (access logs, the release and configuration in place, the cache state) before any rollback or purge: the DPO, and the CNIL if it is notified, will need to establish what was exposed, to whom and since when. Second, when the product hosts its customers' data (payroll, HR, school or health software used by client organisations), the organisation is usually the customers' processor: each affected customer, as controller, has its own 72 hours, so it must be told without undue delay; prepare that message in the routing note instead of counting 72 hours on your own side.

Checked 2026-10-16 on the text of Regulation (EU) 2016/679 (GDPR), EUR-Lex (CELEX 32016R0679):

| Rule | What it imposes | Source |
|---|---|---|
| Notification by the controller | Notify the supervisory authority (the CNIL in France) without undue delay and, where feasible, no later than 72 hours after becoming aware, unless the breach is unlikely to result in a risk to individuals; if later than 72 hours, give the reasons for the delay. The wording counts hours, not business days: a weekend counts. | GDPR art. 33(1) |
| Processor | A processor notifies the controller without undue delay after becoming aware. If the organisation processes its customers' data on their behalf, the customer may be the controller and must be told without undue delay; the DPO confirms the roles. | GDPR art. 33(2) |
| Documentation | Every breach is documented: facts, effects, remedial action. Keep the ticket as the first trace. | GDPR art. 33(5) |
| Individuals | Where the breach is likely to result in a high risk, the controller informs the persons concerned without undue delay. | GDPR art. 34(1) |

Cite an article only if it is in this table or you are certain of it; otherwise state the rule without a number and mark it "to check". In the customer reply, do not call the event a breach, do not admit liability and do not guess at the cause. Do not ask the customer for screenshots or copies of the exposed data, which would spread it; ask them not to share or download it, and, if they already hold a capture, to keep it without forwarding it until security asks for it.

# First-reply templates

Written in the ticket's language. In French, use « vous », no filler praise, and no promise you cannot keep. State what the customer reported, what happens next and when they will hear back; leave out any hypothesis about the cause. Fill the delay from the priority table (or the organisation's).

<example>
Bug:
"Thank you for reporting this. You describe [the symptom in the customer's terms], which stops you from [their impact]. We have logged it as priority [P_] and our team is investigating. [If a workaround exists: In the meantime, you can [workaround].] We will come back to you within [delay] with an update."

Security:
"Thank you for flagging this. We have passed it to our security team, who are looking at it now. We will come back to you within [delay]. [If protective action is useful: In the meantime, please [action, e.g. do not share or download the documents concerned].]"
</example>

Both state the next step and the delay, and neither names a cause or accepts blame.

# Parameters

- `contexte_produit`: the product or scope concerned; use it for the product area and the routing.
- `inclure_template_reponse`: when true (default), add a first reply matched to the category; when false, omit it.

# Expected output format

- `triage`: reported symptom; probable root cause (labelled hypothesis); category; retained priority with its reason and the delay (default or organisation's); product area; routing; duplicate status; missing elements; next action; internal notes (what is already checked, escalation triggers to watch, reproduction hints for a bug, whether a rollback should be considered when a release is the suspected cause); the first reply when requested.
- `questions_ouvertes`: points to clarify for a finer handling, each with who can answer.

# Definition of done

- Handling can start without re-reading the source ticket.
- The priority is justified and the routing unambiguous.
- Duplicate status says either what was checked or that no base was provided.
- A possible personal data breach is flagged, with the reception time and the question left to the DPO.
- Gaps that weaken the triage are visible.

<!-- Adapted from anthropics/knowledge-work-plugins, customer-support/skills/ticket-triage/SKILL.md (Apache-2.0, commit 7b2ea8e): condensed, rewritten into the ix template and modified. The default response delays, the escalation triggers, the category tie-break tips, the routing table and the Bug and Security first-reply templates are adapted from the same file at commit 33eeda1 (unchanged since 7b2ea8e), rewritten and adapted to French business usage. The personal data breach rules (GDPR) and the duplicate-check condition are original. See THIRD_PARTY.md. -->
