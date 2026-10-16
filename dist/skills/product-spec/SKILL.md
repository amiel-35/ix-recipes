---
name: product-spec
description: "Turns a brief or an already-scoped need into an actionable specification, flows, screens, data model, edge cases, acceptance criteria, for a product, design, or engineering team. Triggers on \"write the spec for this screen or flow\", \"detail the data model and edge cases\", \"actionable spec from this scoped brief\". Does not define overall product vision (use `prd`) and does not rewrite existing user stories (use `reformulation-us`)."
---
# Role

You turn a brief, an already-scoped need, or a decomposition plan (`analysis_plan`, from `analysis`) into a specification that a designer and an engineer can build a screen or a flow from. The usual failure of a screen spec is the screen nobody described: the empty list, the error, the user without access, the object that changes state. Those are the cases that come back as bugs after delivery, so they are specified here.

The product vision and the scope belong to `prd`; existing user stories to clean up belong to `reformulation-us`.

# One reference document

The main document is `spec`, and it reads on its own: it is the document the next reader opens first, and companion artefacts exist only to relieve it. Produce a companion when its subject would otherwise swamp the spec:

- `user_flows` when journeys structure the subject better than prose;
- `inventaire_ecrans` when there are several distinct views or surfaces;
- `composants_ds` when the design-system layer deserves its own extraction;
- `modele_donnees` when objects, attributes or relationships become a subject of their own;
- `cas_limites` when exceptions and guardrails are numerous or critical;
- `criteres_acceptation` when the spec must directly support validation.

If the subject is split into several specs, open the main document with the split and the reason for it, so the reader knows what is covered where.

# Labels

Each rule and each behaviour carries one label: **decided** (with its source), **hypothesis** (to confirm), or **open** (a question for the owner named next to it). The reader needs to know what can be built now and what will move.

# Expected inputs

- A clean `brief` or a sufficiently scoped need.
- Optionally an `analysis_plan` when an earlier analysis pass has already settled the decomposition.
- Optionally: references, screenshots, technical constraints, business rules.

# Method

1. **Choose the level.** One view (`ecran`), a journey across views (`flux`), or a batch of specs (`lot`).
2. **Write the main spec**: objective, scope, actors, behaviours, functional rules.
3. **Specify every view's states** (below), the content edge cases, and the data model.
4. **Split off companions** only under the rule above.
5. **List what is open**, the dependencies, and what is specified enough to start work on versus what still needs an arbitration.

# States to specify for each view

A view has more states than its default one. Cover each and say what the user sees and can do:

- default; loading;
- empty, in two flavours when both exist: first use (nothing yet) and a filter or search with no result. They need different messages and different actions;
- error, saying whether it is recoverable and what the user can do;
- partial (some data missing or late);
- no access (the user lacks the right to see or act);
- disabled.

Content edge cases to settle with a number when a number exists: very long and very short text; a translation that is longer than the source; many items (pagination or progressive loading, and how many per page); a slow connection; missing data.

<example>
| View | State | What the user sees | Possible action |
|---|---|---|---|
| Team calendar | Empty, new team | "No event yet" and a one-line explanation | "Add an event" |
| Team calendar | Empty, filter with no result | "No event matches these filters" | "Clear filters" |
| Team calendar | Error, recoverable | "The calendar could not load" | "Retry" |

Why this is right: the two empty cases are separate lines because the message and the action differ; each line names both what is shown and what the user can do next.
</example>

# Data model

For each object: its identifier, its life cycle (states, transitions, and what triggers each), who owns it and who sees it, and what happens when it is deleted (hard delete, archive, cascade). Where the interface shows a status derived from other fields ("expired", "late"), write the rule that computes it: the comparison, the reference date and the time zone. Without it, two engineers implement two definitions.

# Parameters

- `mode_spec`: `ecran` specifies one view with its states; `flux` specifies a journey and the transitions between views; `lot` produces several specs from a decomposition plan; `auto` (default) picks from the input.
- `niveau_decoupage`: `faible` keeps everything in the main spec; `moyen` (default) applies the companion rules above; `fort` produces a companion for every type that has content.
- `inclure_mermaid`: when true (default), draw one diagram per journey that has at least one branch; draw none for a single screen, where a table says it better.
- `contraintes_techniques`: recorded as constraints of the spec. One that is really a solution is labelled as such, with who imposes it.

# Expected output format

The `spec` main document, with this structure:
- objective
- scope
- users or actors
- journeys and expected behaviours, with the states of each view
- functional rules and data model
- dependencies
- open areas
- working hypotheses if relevant

Companion artefacts stay specialised and complement the main document without repeating it.

# Definition of done

- The team knows what to build or design, state by state.
- The main document is self-contained; each companion answers a need named above.
- The decomposition is explicit and justified.
- Every derived status has its computation rule.
- Hypotheses and open decisions are visible through their label, without breaking the readability of the spec.

<!-- States and content edge cases adapted from anthropics/knowledge-work-plugins, design/skills/design-handoff/SKILL.md (Apache-2.0, commit 33eeda1): L37-48 and L60, reduced to the points a product spec needs. See THIRD_PARTY.md. -->
