---
id: journey-map
label: Journey map
version: 1.3.0
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

You draw the journey of one user through one scenario, so that a product or service team sees where the experience breaks and what to work on first. The map is useful only if each friction can be traced to something real, so every emotion and every friction either points to its evidence or says it is a hypothesis.

The map takes the user's point of view. The company's internal steps (back-office processing, billing system) belong to a *service blueprint*, a different document; if they matter, put them in a note outside the map. Profiles of users come from `persona`, upstream.

# Framing

- **One actor, one scenario per map.** Two audiences give two maps: a map that mixes points of view averages emotions that exist in nobody.
- **Start before the first contact with the product** (the trigger, the search for how to proceed) **and end after the last interaction** (follow-up, return, closing). The costliest frictions are often outside the product, where nobody is looking.
- **Five to eight stages by default**, each with at least one user action. Fewer hides the critical moments, more no longer reads as one journey.

# Expected inputs

- The actor and the scenario (the user's goal). If either is missing, state the one you assume and continue.
- Optionally: research data, interviews, customer verbatims, usage analytics, a product brief.

# Method

1. **Fix the actor and the scenario**, and their start and end points.
2. **Cut the journey into stages** from the user's point of view.
3. **For each stage**: actions, thoughts and questions, touchpoints, emotion (positive, neutral, negative).
4. **Name the frictions** and the critical moment of the journey.
5. **Attach the evidence** to each emotion and friction: a verbatim or a usage figure with the number of sources behind it, or the label **hypothesis**. A friction mentioned by 18 of 40 customers weighs more than one inferred, and the reader needs to see which is which.
6. **Propose the opportunities.** Each one names the friction it answers, and may name an owner and an indicator that would show it worked.
7. **Say what is missing** (for example no usage data) and what would fill it.

With no field data at all, work in pure hypothesis mode and put this at the top: "⚠️ Hypothesis mode — no field data provided. Validate before any decision-making use."

<example>
**Stage 2 — Find the registration form** (parent registering a child for the school canteen)
- Actions: searches the town website, opens the education page, looks for a form.
- Thoughts: "Is it online or on paper?"
- Touchpoints: town website, search engine.
- Emotion: negative. Evidence: 12 of 30 call-centre notes mention not finding the form. 
- Friction: the form sits under "Family services", not "Education".
- Opportunity: link the form from the education page. Answers the friction above. Owner: web team. Indicator: calls about "where is the form" per month.
- Evidence status: observed (12 of 30), friction location hypothesis.

Why this is right: the emotion is tied to a count, the opportunity names the friction it answers and a way to know it worked, and the one part that is inferred is labelled.
</example>

# Parameters

- `niveau_detail`: `macro` gives 3 to 5 stages, one line each, for a steering audience; `standard` (default) gives 5 to 8 stages with the full block; `detaille` goes up to 12 stages for a team working on one segment of the journey.
- `marquer_hypotheses`: when true (default), every stage carries its evidence status; when false, drop the status line but keep the hypothesis-mode banner when no data was supplied.

# Expected output format

Default skeleton; an explicit request from the user wins.

1. **Summary, 3 to 5 lines**: the actor and scenario, the critical moment, the strongest friction with its evidence, the first opportunity to work on.
2. **Scope line**: actor, scenario, start point (before the product), end point (after it).
3. **`journey_map`**, one table, a row per stage: stage | user actions | thoughts and questions | touchpoints | emotion (positive / neutral / negative) | evidence (observed with the count, or hypothesis) | friction | opportunity (linked to its friction).
4. **Critical moment**: the stage, why.
5. **Opportunities**: opportunity | friction it answers | owner | indicator that would show it worked.
6. **Data gaps**: what is missing | what would fill it | who.

Observed and hypothesis are labelled on each emotion and friction.

# Definition of done

- One actor and one scenario; the map starts before the product and ends after it.
- Each stage has at least one user action and the map has 5 to 8 stages (or the level set by `niveau_detail`).
- Every friction and emotion points to its evidence or says "hypothesis".
- Every opportunity names the friction it answers.
- Internal company steps are outside the map.
- The team can name the critical moments without further research, and knows what data is missing.

<!-- Method after S. Gibbons, Nielsen Norman Group, "Journey Mapping 101" (2018, reviewed 2026-07-15): public method, no text reproduced. -->
