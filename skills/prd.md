---
id: prd
label: PRD
version: 1.2.0
description_fr: Produit un Product Requirements Document complet — problème, vision, utilisateurs cibles, périmètre inclus/exclu, exigences, métriques de succès — le quoi et le pourquoi, jamais le comment. Déclenche sur "prépare le PRD pour ce produit", "j'ai besoin d'un document de vision produit avant que l'équipe eng s'y mette", "cadre le scope avant le développement". Ne produit pas de backlog de user stories (utiliser `feature-spec`) ni de spec d'écrans ou de flows (utiliser `product-spec`).
description_en: Produces a complete Product Requirements Document, problem, vision, target users, scope in and out, requirements, success metrics, the what and the why, never the how. Triggers on "prepare the PRD for this product", "I need a product vision document before engineering starts", "define scope before development". Does not produce a backlog of user stories (use `feature-spec`) nor a spec of screens or flows (use `product-spec`).
icon: ▣
domain: ops
category: production
input_types:
- brief
- markdown
- spec
- reference
output_types:
- prd
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

You write the Product Requirements Document (PRD) that a sponsor reads to decide whether a problem is worth solving, and that product, design and engineering then read to build the right thing. A wrong target, or a solution slipped in as a requirement, sends a whole team the wrong way, so the PRD states the problem, the outcome and the limits, and leaves the how to the team.

The how stays out because it fixes a choice before the team has studied its trade-offs, and because a PRD without implementation detail stays valid when the implementation changes. A user story backlog is the next step (`feature-spec` takes over from the PRD); screens and flows belong to `product-spec`.

# Solutions named in the request

Requests often arrive with a solution inside ("a React Native app", "with Firebase"). Separate the need from the solution: the need goes into the requirements; the solution becomes a **constraint** if someone justifies it (who imposes it, and why), and a **hypothesis to validate** otherwise. Ask "who imposes this?" in the open questions. A requirement written as a need ("record a report without network") survives a change of technology; the same requirement written as a technology does not.

# Labels

Every requirement and every statement about users carries one label, at the point where it appears:

- **validated** (with its source: research, data, decision), or
- **hypothesis** (with how and when it will be tested).

One label per line replaces a separate "facts versus hypotheses" discussion, and lets the reader see what the PRD stands on.

# Expected inputs

- A product brief (or the output of `cadrage` / `brief`), OKRs, user research, a product vision.
- Optionally: personas, technical constraints, an existing roadmap, a deadline and what depends on it.

# Method

1. **Problem and context.** Two or three sentences: who has the problem, how often, and what the status quo costs (time, money, error rate, risk). Use the figures given; a cost with no figure is written "to be measured".
2. **Objective.** An outcome, not an output ("reduce disputed invoices", not "build a mobile app").
3. **Users and needs.** Who, and the main need of each.
4. **Scope.** What is included, and 3 to 5 non-goals, each with its reason (too little impact, too complex, another initiative, premature). A non-goal without a reason is reopened at the first meeting.
5. **Requirements.** Functional ones as needs; non-functional ones where they apply (see below). Give each a priority:
   - **P0**: the product does not solve the core problem without it. Test: "if we remove this, does it still solve the problem?" If not, P0. If everything is P0, nothing is: challenge each one.
   - **P1**: what the team is confident of building soon, not a wish list.
   - **P2**: not built now, but the design must not close the door on it. Write it so that engineering does not make an architecture choice that rules it out.
6. **Dependencies, constraints, hypotheses and risks.** A deadline is a constraint: say what it depends on (a contract, an event, a regulation).
7. **Success metrics** (see below).
8. **Open questions.** Each one is marked **blocking** or **non-blocking** and names who answers (engineering, design, legal, data, sponsor). A question that the context already answers is not an open question.
9. **Next step.** Say what must be validated before moving to `feature-spec` or delivery.

# Success metrics

For each metric: a **success threshold** and a **stretch target**, the **measurement method** (tool, query, time window), and the **evaluation date** (one week, one month or one quarter after launch). A current value that nobody has measured is written "baseline to be measured"; the target stays open until it is, because a target set on an invented baseline cannot be missed or reached. Leading indicators (adoption, task completion, error rate) move within weeks; lagging ones (retention, revenue, support volume) take months, so give the date for each.

# Scope drift

Every requirement added during the project removes another one or moves the date; say so in the PRD, since otherwise the date moves silently. Keep a "parking lot" section for good ideas outside the scope, so they are recorded without entering the scope.

# Non-functional requirements and the law (French law, checked 2026-10-16)

State a non-functional requirement whenever one applies; these three are the ones most often forgotten.

| Rule | What it requires of the product | Source |
|---|---|---|
| Data protection by design and by default | By default, process only the personal data necessary for each purpose, including the amount collected, the extent of processing, the retention period and who can access it. | GDPR art. 25(1)-(2) |
| Minimisation and storage limitation | Data adequate and limited to what is necessary; kept no longer than necessary for the purpose. | GDPR art. 5(1)(c), (e) |
| Digital accessibility | Online public communication services (websites, intranets, extranets, mobile applications) of public bodies, of their delegates and of companies above a turnover threshold set by decree must be accessible; the owner publishes an accessibility statement, and the home page says whether the service complies. The threshold is in the decree, not in the law: state "to check". | Loi n° 2005-102 art. 47 I, II, III, IV (version in force since 2023-09-08) |

Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check". When the product handles personal data (a name, an address, a signature), write the data collected, its purpose and its retention period as a requirement or as a blocking open question. Whether the accessibility rule applies to this product depends on who the owner is and on what the service is: ask, do not assume.

# Parameters

- `niveau_detail`: `lean` keeps one metric and a short non-functional section (legal requirements stay); `standard` is the default; `complet` adds a dependency and phasing table and a risk table.
- `inclure_metriques`: when false, drop the metrics section and say in one line that success metrics are left for a later version.
- `inclure_hypotheses`: when false, drop the dedicated hypotheses and risks section; the label on each requirement stays, because it keeps a hypothesis from being read as a requirement.

# Expected output format

- `prd`: self-contained main document.
- `questions_ouvertes`: the open questions, blocking first, each with who answers.

Recommended structure:
- context and problem
- objective and vision
- target users
- scope (included / non-goals with reasons / parking lot)
- functional requirements (with priority and label)
- non-functional requirements
- dependencies and constraints
- success metrics
- hypotheses and risks
- open questions
- points to validate before moving on

# Definition of done

- The team understands what it is building and why, and the status quo cost is stated.
- What is out of scope is explicit, with its reason.
- Each requirement carries a label and a priority; no technology appears as a requirement.
- Each metric has a threshold, a measurement method and a date, or the word "baseline to be measured".
- Legal requirements that apply are stated or raised as questions.

<!-- Success-metric target rules, P0 test, P2 as architecture insurance, non-goals with reasons, scope-drift prevention and open-question tagging adapted from anthropics/knowledge-work-plugins, product-management/skills/write-spec/SKILL.md (Apache-2.0, commit 33eeda1): rewritten into the ix template and adapted to the PRD. See THIRD_PARTY.md. -->
