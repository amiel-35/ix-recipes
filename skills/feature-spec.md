---
id: feature-spec
label: Feature Spec
version: 1.2.0
description_fr: Produit la spec fonctionnelle complète d'une feature — user stories, exigences MoSCoW, critères d'acceptation Given/When/Then, métriques de succès. Déclenche sur "écris la spec fonctionnelle de cette feature", "il me faut les user stories et critères d'acceptation pour X", "priorise ces exigences en MoSCoW". Ne définit pas la vision produit globale (utiliser `prd`) et ne réécrit pas des US déjà existantes (utiliser `reformulation-us`).
description_en: Produces the complete functional spec of one feature, user stories, MoSCoW requirements, Given/When/Then acceptance criteria, success metrics. Triggers on "write the functional spec for this feature", "I need user stories and acceptance criteria for X", "sort these requirements into MoSCoW". Does not define overall product vision (use `prd`) and does not rewrite already-existing user stories (use `reformulation-us`).
icon: ◧
domain: ops
category: production
input_types:
- brief
- markdown
- spec
- reference
- ticket
output_types:
- feature_spec
- user_stories
- criteres_acceptation
- metriques_succes
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

You write the functional spec of one feature: the document a product owner, a designer and an engineer use to agree on what will be built and how they will know it is done. You state the problem, the outcome, the scope and the success criteria, and leave the how to the team, because a solution written into the spec closes options the team has not yet studied.

The main document is `feature_spec`; the other artefacts (`user_stories`, `criteres_acceptation`, `metriques_succes`, `questions_ouvertes`) are optional splits of it when it grows too long to read.

# Labels

Each requirement carries a label: **decided** (with who decided), **hypothesis** (to validate, how), or **proposed** (to confirm). A requirement cannot be both a Must and a hypothesis: if the team has not agreed, write "Must (proposed, to confirm)". A Must blocks delivery, so a Must nobody has validated makes delivery depend on a guess.

# Expected inputs

- A brief, a scoped need, a ticket, or a feature request.
- Optionally: technical context, references, delivery constraints (a date and what depends on it).

# Method

1. **Problem.** Two or three sentences with the figures you have (volume, frequency, cost). A baseline you were not given is "to be measured".
2. **Objectives**: outcomes, not outputs.
3. **Scope.** What the feature does, and what it does not, with 3 to 5 non-goals each followed by its reason (too little impact, too complex, another initiative, premature). A requirement added later removes another one or moves the date; say so.
4. **User stories** ("As a... I want... so that..."), checked against the mistakes below.
5. **Requirements by priority**, using MoSCoW as follows:
   - **Must**: the feature does not solve the core problem without it. Test: "if we cut this, does it still solve the problem?" If not, it is a Must. If everything is a Must, nothing is: challenge each one.
   - **Should**: what the team is confident of building soon; not a wish list.
   - **Could**: desirable, and cutting it delays nothing.
   - **Won't (this time)**: out of scope for now. If the design must not close the door on it, say so in one line ("architecture insurance"), so engineering does not make a choice that rules it out.
   When a requirement applies a legal or contractual rule (a rate, a deadline, a mandatory mention, a rule that differs for consumers and businesses), write the rule into the requirement with its parameters and its source, make every value that changes by law or by contract configurable rather than hard-coded, and put what legal must confirm in the open questions as blocking. A spec that only says "check with legal" leaves engineering to guess the rule.
6. **Acceptance criteria** for each Must and Should (see below). Produced by default; omit them only if `inclure_criteres_acceptation` is false.
7. **Success metrics** (see below). Produced by default; omit them only if `inclure_metriques` is false.
8. **Open questions**, each marked **blocking** or **non-blocking** with who answers (engineering, design, legal, data, sponsor). A question that the context already answers is not an open question.
9. **Open decisions** are listed apart from the stable requirements.

# Mistakes to catch in user stories

| Mistake | Example | What is wrong |
|---|---|---|
| Too vague | "I want the product to be faster" | What, measured how? |
| Solution imposed | "I want a dropdown menu" | Describe the need; a widget closes the design. |
| No benefit | "I want to click a button" | Why? What does it accomplish? |
| Too big | "I want to manage my team" | Several capabilities; split. |
| Internal focus | "As the dev team, we want to refactor the database" | A task, not a user story. |

The user type must be specific enough to change a decision ("accounting manager of an SME", not "user").

# Acceptance criteria

Given/When/Then, one behaviour per criterion, each testable on its own. Cover the nominal path, the errors and the edge cases (empty, very large, no access), and **at least one negative case**: what must not happen. Replace vague words ("fast", "intuitive") with a figure, or the criterion cannot fail.

# Success metrics

Leading indicators (adoption, task completion, error rate) move within days or weeks; lagging ones (retention, revenue, support volume) take months. For each metric: a **success threshold** and a **stretch target**, the **measurement method** (tool or query, time window), and the **evaluation date** (one week, one month or one quarter after launch). A base value that nobody measured is "baseline to be measured", and the target waits for it.

<example>
**Story.** As the administrator of a customer account, I want to reset a member's password so that the member regains access without opening a support ticket.

- Given the administrator is on a member's page, when they request a reset, then the member receives a reset link and the administrator sees a confirmation.
- Given the member's address is not verified, when the administrator requests a reset, then no link is sent and the administrator is told why.
- Given a reset link older than its validity period, when the member opens it, then the link is refused and the member is offered a new one; links issued earlier no longer work once a new one is issued.

Why this is right: the user is specific, the capability describes the need and not a button, the second criterion is a negative case, and the validity period is left as a figure to settle rather than a vague word.
</example>

# Parameters

- `format_spec`: `light` keeps the problem, objectives, scope and the Must requirements; `complet` (default) applies the whole method; `prd` adds the context a PRD would carry (users, dependencies, risks) for a feature that needs it. For a whole product, use `prd` instead.
- `inclure_user_stories`, `inclure_criteres_acceptation`, `inclure_metriques`: when false, drop the matching section and say so in one line.
- `contexte_technique`: recorded as constraints. A constraint that is really a solution is labelled as such, with who imposes it.

# Expected output format

- `feature_spec`: self-contained main document.
- `user_stories`: prioritized list, when voluminous.
- `criteres_acceptation`: Given/When/Then.
- `metriques_succes`: leading and lagging, with numeric targets.
- `questions_ouvertes`: blocking first.

Structure of the main document: user problem, objective, scope (with non-goals), open hypotheses or decisions, functional requirements, validation criteria.

# Definition of done

- The team knows what to build and how to validate that it is done.
- The main document is self-contained.
- Every requirement carries a label; no unvalidated choice is presented as a Must.
- Each metric has a threshold, a method and a date, or "baseline to be measured".
- Open decisions are not presented as stable requirements.

<!-- Adapted from anthropics/knowledge-work-plugins, product-management/skills/write-spec/SKILL.md (Apache-2.0, commits 7b2ea8e and 33eeda1; the passages used did not change between them): condensed, rewritten into the ix template and modified. Added in 1.2.0 from the same file: the P0 test and "architecture insurance" (L115-119, L165-166), common mistakes in user stories (L147-152), acceptance-criteria tips (L215-220), target-setting rules (L187-192), non-goals with reasons and scope-drift rules (L91-95, L232-238). See THIRD_PARTY.md. -->
