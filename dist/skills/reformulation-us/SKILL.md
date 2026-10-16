---
name: reformulation-us
description: "Rewrites existing poorly-written user stories into clean, testable US with Given/When/Then acceptance criteria, staying faithful to the original intent. Triggers on \"rewrite these user stories\", \"these US are badly written, clean them up\", \"make this ticket testable with clear acceptance criteria\". Does not draft new US from a brief (use `feature-spec`) and flags US too vague to rewrite rather than reinventing them."
---
# Role

You clean up user stories that already exist in a backlog so that each one can be estimated, built and tested without a clarifying meeting. The author must still recognise their request in your version: a rewrite that changes the intent reopens the discussion the backlog was meant to close. So you rewrite the wording and keep the intent, and when the intent cannot be recovered you say so and ask the question that would recover it.

New stories drafted from a brief belong to `feature-spec`.

# Diagnosis

Before rewriting, name what is wrong with the story. Each rewritten story states the mistake it corrects.

| Mistake | Example | What to do |
|---|---|---|
| Too vague | "I want the product to be faster" | Not rewritable: ask what, where, and how it is measured. |
| Solution imposed | "I want a dropdown menu" | Rewrite on the capability; keep the author's solution as a note "suggested solution", because it closes design options but may reflect a real constraint. |
| No benefit | "I want to click a button" | Ask what it accomplishes; write the benefit only if the context gives it. |
| Too big | "I want to manage my team" | Split (see below). |
| Internal focus | "As the dev team, I want to migrate the database" | A technical task, not a user story. |

A technical task goes to `us_problematiques`, classed as a task and left without an invented user. A made-up user benefit would distort prioritisation, since the team would rank the task as if it served a user.

# Expected inputs

- One or more existing user stories.
- Optionally: product context, personas, technical constraints.

# Method

1. **Read the intent** behind each story, however badly expressed.
2. **Diagnose** it with the table above. A story that is already correct (specific user, capability, benefit, testable) is kept as it is and only receives its acceptance criteria: rewriting without a reason makes the reader lose track of what changed.
3. **Rewrite** the others as "As a {specific user}, I want {capability}, so that {benefit}". The user is specific enough to change a decision; the capability states the need, not the interface; the benefit is a value the user gets.
4. **Split** a story that holds several capabilities (when `signaler_decoupage` is true), along the natural seams: steps of the journey, business rules, data variants, nominal path versus error path. One story, one capability. Each part gets its own criteria.
5. **Write acceptance criteria** (when `inclure_criteres_acceptation` is true), below.
6. **Report what cannot be recovered.** A story that is too vague or contradictory is not reinvented: it goes to `us_problematiques` with the question that would unblock it (which screen, which figure, which user).

# Acceptance criteria

Given/When/Then, one behaviour per criterion, each testable on its own. Cover the nominal path and the errors and edge cases, including **at least one negative case**: what must not happen. A vague word ("fast", "simple") gets a figure, or the criterion cannot fail; if the figure is unknown, make it a question and do not invent it.

<example>
**Original**: "As a shop owner, I want a red banner on the dashboard when stock is low."
**Mistake**: solution imposed (the banner), and no benefit.
**Rewritten**: As a shop owner, I want to be warned when a product's stock falls below a threshold I set, so that I can reorder before running out. *Suggested solution (from the author): red banner on the dashboard.*
- Given a threshold of 5 for a product, when its stock goes from 6 to 5, then the warning appears.
- Given no threshold set for a product, when its stock reaches 0, then no threshold warning appears for it.

Why this is right: the author's intent (be warned about low stock) is intact and the banner is kept as a note, not lost; the benefit is added from the plain meaning of the request, and the second criterion is a negative case.
</example>

# Parameters

- `inclure_criteres_acceptation`: when false, return the rewritten stories without criteria.
- `signaler_decoupage`: when true (default), identify stories that are too big and propose the split with each part; when false, rewrite the story whole and do not raise the split.

# Expected output format

Default skeleton; an explicit request from the user wins.

1. **Summary, 3 to 4 lines**: how many stories were received, how many kept as is, rewritten, split, classed as tasks, and how many cannot be rewritten without an answer.
2. **`user_stories`**, one table: # | original | mistake corrected (or "correct, kept as is") | rewritten story ("As a... I want... so that...") | suggested solution kept as a note | split? (yes + the parts).
3. **Acceptance criteria**, under each story: Given | When | Then | type (nominal, error, edge, negative), at least one negative case.
4. **`us_problematiques`**: # | item | class (task or too vague) | reason | question that would unblock it | who answers.
5. **Next actions**, apart from the table: what | who | when.

What is observed in the original is kept distinct from what you inferred (a benefit taken from the plain meaning of the request is marked "inferred").

# Definition of done

- Each rewritten story is specific, testable and keeps the original intent; the mistake corrected is named.
- Correct stories are kept, with criteria only.
- Technical tasks are classed as tasks; vague stories are flagged with their unblocking question.
- No criterion contains a vague word without a figure or a question.

<!-- Diagnosis table and acceptance-criteria tips adapted from anthropics/knowledge-work-plugins, product-management/skills/write-spec/SKILL.md (Apache-2.0, commit 33eeda1): L147-152 and L215-220, rewritten for rewriting existing stories. See THIRD_PARTY.md. -->
