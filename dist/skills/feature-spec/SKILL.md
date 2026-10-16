---
name: feature-spec
description: "Produces the functional spec of a feature, a screen or a flow, user stories, MoSCoW requirements, Given/When/Then acceptance criteria, the states of every view, content edge cases, data model and status-computation rules, success metrics. Triggers on \"write the functional spec for this feature\", \"I need user stories and acceptance criteria for X\", \"sort these requirements into MoSCoW\", \"write the spec for this screen or flow\", \"detail the data model and edge cases\", \"actionable spec from this scoped brief\". Replaces `product-spec`. Does not define overall product vision (use `prd`), does not rewrite already-existing user stories (use `reformulation-us`) and does not draw the interface (use `mockup`)."
---
# Role

You write the functional spec of one feature, one screen or one flow: the document a product owner, a designer and an engineer use to agree on what will be built and how they will know it is done. You state the problem, the outcome, the scope and the success criteria, and leave the how to the team, because a solution written into the spec closes options the team has not yet studied.

A spec of a screen fails in a known way: the screen nobody described (the empty list, the error, the user without access, the object that changes state). Those cases come back as bugs after delivery, so they are specified here, state by state.

This skill replaces `product-spec` (merged, 2.0.0), which covered screens, flows and data models; the vision of the whole product belongs to `prd`, existing stories to clean up to `reformulation-us`, the look of the interface to `mockup`.

# One reference document

The main document is `feature_spec`, and it reads on its own: it is the one the next reader opens first, and companion artefacts exist only to relieve it. Produce a companion when its subject would otherwise swamp the main document:

- `user_stories` when the list is long;
- `criteres_acceptation` when the spec must directly support validation;
- `metriques_succes` when the metrics need their own table;
- `questions_ouvertes` when open points are numerous;
- `user_flows` when journeys structure the subject better than prose;
- `inventaire_ecrans` when there are several distinct views or surfaces;
- `composants_ds` when the design-system layer deserves its own extraction;
- `modele_donnees` when objects, attributes or relationships become a subject of their own;
- `cas_limites` when exceptions and guardrails are numerous or critical.

If the subject is split into several specs, open the main document with the split and the reason for it, so the reader knows what is covered where.

# Labels

Each requirement, rule and behaviour carries a label: **decided** (with who decided, or its source), **hypothesis** (to validate, how), or **proposed** (to confirm, by whom). A requirement cannot be both a Must and a hypothesis: if the team has not agreed, write "Must (proposed, to confirm)". A Must blocks delivery, so a Must nobody has validated makes delivery depend on a guess. The reader needs to see what can be built now and what will move.

# Expected inputs

- A brief, a scoped need, a ticket, or a feature request; or an `analysis_plan` (from `analysis`) when an earlier pass has already settled the decomposition.
- Optionally: technical context, references, screenshots, business rules, delivery constraints (a date and what depends on it).

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
8. **Views, states and data** (below), when the subject has screens, a flow or objects. Choose the level first: one view (`ecran`), a journey across views (`flux`), or a batch of specs from a decomposition plan (`lot`).
9. **Open questions**, each marked **blocking** or **non-blocking** with who answers (engineering, design, legal, data, sponsor). A question that the context already answers is not an open question.
10. **Open decisions** are listed apart from the stable requirements.
11. **Split off companions** only under the rule above.

# Mistakes to catch in user stories

| Mistake | Example | What is wrong |
|---|---|---|
| Too vague | "I want the product to be faster" | What, measured how? |
| Solution imposed | "I want a dropdown menu" | Describe the need; a widget closes the design. |
| No benefit | "I want to click a button" | Why? What does it accomplish? |
| Too big | "I want to manage my team" | Several capabilities; split. |
| Internal focus | "As the dev team, we want to refactor the database" | A task, not a user story. |

The user type must be specific enough to change a decision ("accounting manager of an SME", not "user").

# States to specify for each view

A view has more states than its default one. Cover each and say what the user sees and can do:

- default; loading;
- empty, in two flavours when both exist: first use (nothing yet) and a filter or search with no result. They need different messages and different actions;
- error, saying whether it is recoverable and what the user can do;
- partial (some data missing or late);
- no access (the user lacks the right to see or act);
- disabled.

Content edge cases to settle with a number when a number exists: very long and very short text; a translation that is longer than the source; many items (pagination or progressive loading, and how many per page); a slow connection; missing data.

This list focuses attention on what a view usually forgets. Then check what this feature's subject calls for beyond it (personal data shown or exported, accessibility, a sector rule, the specific product): what the list does not name gets missed.

# Data model and derived statuses

For each object: its identifier, its life cycle (states, transitions, and what triggers each), who owns it and who sees it, and what happens when it is deleted (hard delete, archive, cascade). Where the interface shows a status derived from other fields ("expired", "late"), write the rule that computes it: the comparison, the reference date and the time zone. Without it, two engineers implement two definitions.

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

- `format_spec`: `light` keeps the problem, objectives, scope and the Must requirements; `complet` (default) applies the whole method; `contexte_produit` adds the context a PRD would carry (users, dependencies, risks) for a feature that needs it. That value was called `prd` before 2.0.0, a name that collided with the skill `prd`; for a whole product, use that skill.
- `mode_spec`: `ecran` specifies one view with its states; `flux` specifies a journey and the transitions between views; `lot` produces several specs from a decomposition plan; `auto` (default) specifies the feature and adds the view, state and data-model sections when the input speaks of screens, flows or objects.
- `niveau_decoupage`: `faible` keeps everything in the main document; `moyen` (default) applies the companion rule above; `fort` produces a companion for every type that has content.
- `inclure_mermaid`: when true (default), draw one diagram per journey that has at least one branch; draw none for a single screen, where a table says it better.
- `inclure_user_stories`, `inclure_criteres_acceptation`, `inclure_metriques`: when false, drop the matching section and say so in one line.
- `contexte_technique`: recorded as constraints (stack, integrations, delivery). A constraint that is really a solution is labelled as such, with who imposes it.

# Expected output format

Default skeleton; an explicit request from the user wins. `feature_spec` is self-contained; the companions of the rule above complement it without repeating it.

1. **Summary, 3 to 5 lines**: what is built, for whom, how many Musts, what blocks (number of blocking questions), the decision asked.
2. **Problem and objectives**, with figures or "to be measured".
3. **Scope**: in; non-goals, each with its reason.
4. **Users and stories**; specific user, need, benefit.
5. **Requirements** table: ID | requirement | MoSCoW | label (decided / hypothesis / proposed) | source or owner.
6. **Acceptance criteria** table: requirement ID | Given | When | Then | type (nominal, error, edge, negative).
7. **Views and states** table (if there are screens): view | state | what the user sees | possible action.
8. **Data model and rules** (if there are objects): object | life cycle | owner and visibility | deletion | derived status and its computation rule.
9. **Success metrics** table: metric | leading or lagging | baseline | threshold | stretch | method | evaluation date.
10. **Open questions and decisions**: question | blocking or not | who answers | by when; decisions apart from the stable requirements.
11. **Next actions**, apart from the diagnosis: what | who | when.

Facts, hypotheses and points to check are labelled where they appear. Sections 7 and 8 are dropped, in one line, when the subject has no view or no object.

# Definition of done

- The team knows what to build and how to validate that it is done.
- The main document is self-contained.
- Every requirement carries a label; no unvalidated choice is presented as a Must.
- Each metric has a threshold, a method and a date, or "baseline to be measured".
- Open decisions are not presented as stable requirements.
- Every view states its states (empty in both flavours, error, no access) and every derived status has its computation rule.
- Companions answer a need named above; a split into several specs is explained.

<!-- Adapted from anthropics/knowledge-work-plugins, product-management/skills/write-spec/SKILL.md (Apache-2.0, commits 7b2ea8e and 33eeda1; the passages used did not change between them): condensed, rewritten into the ix template and modified. Added in 1.2.0 from the same file: the P0 test and "architecture insurance" (L115-119, L165-166), common mistakes in user stories (L147-152), acceptance-criteria tips (L215-220), target-setting rules (L187-192), non-goals with reasons and scope-drift rules (L91-95, L232-238). See THIRD_PARTY.md. Added in 2.0.0 (merge of `product-spec`): states and content edge cases adapted from design/skills/design-handoff/SKILL.md (Apache-2.0, commit 33eeda1), L37-48 and L60. -->
