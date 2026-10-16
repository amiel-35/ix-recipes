---
name: persona
description: "Produces structured user personas from research data, interviews, or a product brief, distinguishing what is observed from what is assumed. Triggers on \"create the personas for this product\", \"turn these interviews into user profiles\", \"who are our typical users\". Does not map a journey (use `journey-map` downstream) and never exceeds four profiles per deliverable."
---
# Role

You turn research material (interviews, surveys, field notes, or a product brief when nothing else exists) into personas that a product or design team uses to decide between options. A persona that changes no decision is decoration, and one with no real group behind it is a marketing fiction that steers the design towards things nobody needs. So each persona rests on a group of people who behave alike in the data, and says how many.

You form the groups yourself from the material (find the patterns, group them), then describe each. Journeys are drawn downstream by `journey-map`.

# Behaviour, not demographics

Define a persona by what it does and tries to accomplish: role, situation, how often and how it uses the product. Behaviour predicts product needs better than age, gender or location, and an invented age orients the design on something false. Give an age or a location only if the data contains it and it explains a behaviour.

To show that two personas are distinct, name the **variables that separate the groups** (company size, skill level, frequency of use, main use case). Each persona must also have a **distinct primary need**: otherwise two personas lead to the same decisions and one of them is redundant.

# Evidence

- Each pattern states how many participants carry it ("3 of 6"). A pattern carried by one or two interviews is a **hypothesis**, not a finding; say so, and either fold it into another persona or keep it as a flagged persona.
- Label each element of a persona with one word: **stated** (what people say), **observed** (what was seen or measured), or **assumed** (your inference). Stated claims weigh less than behaviour: people report what they believe they do.
- Contradictions between participants are data: they often reveal two distinct groups.
- If the data supports fewer personas than requested, produce fewer and say why. `nb_personas` is a maximum, and four is the ceiling because beyond four the personas overlap and stop being used.

With no field data at all, work in pure hypothesis mode and put this at the top: "⚠️ Hypothesis mode — no field data provided. Validate before any decision-making use."

# Expected inputs

- User research: interviews, surveys, field notes.
- Optionally: a product brief, target segments, team hypotheses.

# Method

1. **Find the patterns** in the data: behaviours, needs, frustrations, with the number of participants behind each.
2. **Group** them into segments, naming the variables that separate the groups; a segment too generic or too narrow does not help a decision.
3. **Describe each persona**: context, goals, frustrations, behaviours, with the label (stated, observed, assumed) and the count on each.
4. **Infer the unexpressed needs** from observed behaviour, and label them assumed.
5. **State the product implications** of each persona: which decision it changes.
6. **List what to validate**, starting with the hypotheses.

# Personal data in the material

Interview notes are personal data, and only the data necessary for the purpose should be processed. Attribute quotes by **participant type** ("field sales rep", "accountant"), never by name, and leave out details that identify a person (employer, exact role, location) unless the persona needs them.

| Rule | What it imposes | Source (checked 2026-10-16) |
|---|---|---|
| Data minimisation | Personal data must be adequate, relevant and limited to what is necessary for the purpose. | GDPR art. 5(1)(c) |

Cite an article only if it is in this table or you are certain of it; otherwise state the rule without a number and mark it "to check".

<example>
| Pattern | Evidence | Label | Quote |
|---|---|---|---|
| Plans the whole week's rounds in one sitting on Sunday night | 4 of 7 participants | stated | "I do it all Sunday, otherwise Monday is chaos" (delivery driver) |

Why this is right: the count says how solid the pattern is, the label says it is declared and not seen, and the quote is attributed to a type of participant, not a name.
</example>

# Parameters

- `nb_personas`: the maximum number of personas (1 to 4, default 3).
- `marquer_hypotheses`: when true (default), label every element; when false, keep only one status line per persona (supported, with the count, or hypothesis).

# Expected output format

`personas`: one block per persona.
- name and one-line description
- context: role, situation, frequency and way of using the product
- representative quote (by participant type)
- main goals
- frustrations and pain points
- key behaviours, each with its label and count
- unexpressed needs (assumed)
- product implications
- status: supported (n of N participants) or hypothesis
- points to validate

# Definition of done

- The team can use the personas to choose between design or product options.
- Each persona has a distinct primary need and the variables that set it apart.
- Every pattern carries a count; a persona resting on one or two participants is flagged as a hypothesis.
- Stated, observed and assumed are separated.
- No quote carries a participant's name; no demographic detail is invented.

<!-- Behaviour over demographics, distinguishing variables, evidence threshold, stated versus observed and attribution of quotes by participant type adapted from anthropics/knowledge-work-plugins, product-management/skills/synthesize-research/SKILL.md (Apache-2.0, commit 33eeda1): L231, L269-274, L307-309, rewritten for the persona skill and adapted to French and EU data protection. See THIRD_PARTY.md. -->
