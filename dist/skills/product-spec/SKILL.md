---
name: product-spec
description: "Merged into feature-spec, use feature-spec. Still triggers on \"write the spec for this screen or flow\", \"detail the data model and edge cases\", \"actionable spec from this scoped brief\", to point to `feature-spec`, which now covers screens, flows, states and the data model."
---
# Merged into `feature-spec`

Use `feature-spec` for what this skill did: specifying a screen (`mode_spec: ecran`), a journey (`flux`) or a batch of specs (`lot`), with the states of every view, the content edge cases, the data model with the computation rules of derived statuses, and the companion artefacts (`user_flows`, `inventaire_ecrans`, `composants_ds`, `modele_donnees`, `cas_limites`).

The two skills are merged because a screen spec and a feature spec share most of their method (labels, requirements, acceptance criteria, open questions): kept apart, each improvement had to be written twice, and a user had to guess which of two near-identical skills to call. The id `feature-spec` is kept; `product-spec` stays for one version as a pointer.

Run `feature-spec` on the request. If a brief arrives here with an `analysis_plan`, `feature-spec` accepts it as input.
