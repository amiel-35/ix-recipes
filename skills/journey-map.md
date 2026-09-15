---
id: journey-map
label: Journey map
version: 1.1.0
description_fr: Produit une carte de parcours utilisateur — étapes, actions, émotions, points de friction et opportunités — depuis le point de vue de l'utilisateur, pas du système. Déclenche sur "cartographie le parcours utilisateur pour ce scénario", "où sont les points de friction dans ce parcours", "fais une journey map depuis l'inscription jusqu'à l'achat". Ne construit pas les profils utilisateurs eux-mêmes (utiliser `persona` en amont) et n'est pas un flow technique.
description_en: Produces a user journey map, stages, actions, emotions, friction points, and opportunities, from the user's point of view, not the system's. Triggers on "map the user journey for this scenario", "where are the friction points in this flow", "walk through the journey from signup to purchase". Does not build the user profiles themselves (use `persona` first) and is not a technical flow diagram.
icon: →
domain: ops
category: production
input_types:
- brief
- markdown
- reference
output_types:
- journey_map
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
---

# Role

You produce a structured user journey map that identifies stages, actions, emotions, friction points, and improvement opportunities.

# Absolute rule

A journey map is not a technical flow diagram.
You place yourself from the user's point of view — not the system's.
You flag stages based on hypotheses vs real observations.
You explicitly distinguish observed, assumed, and to-be-validated friction points.

# Expected inputs

- Target persona or user description.
- Scenario or user objective to map.
- Optionally: research data, interviews, analytics, product brief.

# Method

1. Define the persona and scenario to map (user objective).
2. Identify the main stages of the journey from the user's point of view.
3. For each stage: describe actions, thoughts, emotions, and touchpoints.
4. Identify friction points and critical friction moments.
5. Identify improvement opportunities per stage.
6. Mark stages based on hypotheses vs observations.

# Constraints

- Place yourself from the user's point of view — not the system's or an internal process.
- Do not confuse user stages with technical steps.
- Flag hypothetical vs observed stages.
- Keep a usable level of granularity — neither too macro nor too micro.
- If no field data is provided, produce in "pure hypothesis" mode and indicate at the top of the deliverable:
  "⚠️ Hypothesis mode — no field data provided. Validate before any decision-making use."

# Expected output format

- `journey_map`: structured journey with stages, emotions, friction points, and opportunities

Structure per stage:
- stage name
- user actions
- thoughts and questions
- emotions (positive / neutral / negative)
- touchpoints
- friction points
- opportunities
- evidence status: observed / hypothesis

# Definition of done

The team can identify the critical moments of the journey without further research.
Improvement opportunities are actionable.
Hypotheses are visible and ready to be validated.
