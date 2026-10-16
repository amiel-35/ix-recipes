---
id: product-spec
label: Spec
version: 2.0.0
description_fr: Fusionné dans feature-spec — utiliser feature-spec. Déclenche encore sur "écris la spec de cet écran ou de ce parcours", "détaille le modèle de données et les cas limites", "spec exploitable à partir de ce brief cadré", pour renvoyer vers `feature-spec`, qui couvre désormais les écrans, les parcours, les états et le modèle de données.
description_en: Merged into feature-spec, use feature-spec. Still triggers on "write the spec for this screen or flow", "detail the data model and edge cases", "actionable spec from this scoped brief", to point to `feature-spec`, which now covers screens, flows, states and the data model.
icon: ▣
domain: ops
category: production
input_types:
- brief
- markdown
- reference
- analysis_plan
output_types:
- spec
- user_flows
- inventaire_ecrans
- composants_ds
- modele_donnees
- cas_limites
- criteres_acceptation
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
---

# Merged into `feature-spec`

Use `feature-spec` for what this skill did: specifying a screen (`mode_spec: ecran`), a journey (`flux`) or a batch of specs (`lot`), with the states of every view, the content edge cases, the data model with the computation rules of derived statuses, and the companion artefacts (`user_flows`, `inventaire_ecrans`, `composants_ds`, `modele_donnees`, `cas_limites`).

The two skills are merged because a screen spec and a feature spec share most of their method (labels, requirements, acceptance criteria, open questions): kept apart, each improvement had to be written twice, and a user had to guess which of two near-identical skills to call. The id `feature-spec` is kept; `product-spec` stays for one version as a pointer.

Run `feature-spec` on the request. If a brief arrives here with an `analysis_plan`, `feature-spec` accepts it as input.
