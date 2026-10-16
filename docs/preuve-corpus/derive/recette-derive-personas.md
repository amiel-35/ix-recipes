---
id: derive-personas
label: Personas à partir de notes de terrain
version: 0.1.0
description_fr: "Essai du test de dérive (decision-corpus.md §8) : regroupement des notes de terrain, puis personas."
description_en: "Drift test (decision-corpus.md §8): grouping field notes, then personas."
icon: ⇢
domain: ops
category: workflow
input_types: [markdown]
output_types: [markdown]
compatible: [claude-code]
requires: [ix-skills:affinity-mapping, ix-recipes:persona]
workflow:
  format: 1
  context_sheet: [entities, objective, constraints, recipient, format, deadlines, named_solutions]
  steps:
    - id: regroupement
      label: "Regroupement des notes"
      skill: ix-skills:affinity-mapping
      mission: Group the field notes into segments of passengers who behave alike towards the service (who they are and what they do, not the topic of the question). For each group give its name, the note ids (N001…) it rests on, the number of interviews when the notes state one, and its key behaviours and frustrations, each with its note ids. Form at most 4 groups, since the request asks for 4 personas at most; notes that fit none stay apart. Do not write personas.
      receives: [brief]
      transmits: [groups]
      produces_context_sheet: true
      pause: validate
      model: opus
    - id: personas
      label: "Personas"
      skill: ix-recipes:persona
      mission: "Write one persona per group received in `regroupement.groups`. Do not regroup the participants: the groups are decided. Quote and detail from what you receive (and from the corpus when it is available), never form new groups."
      receives: [context_sheet, regroupement.groups]
      transmits: [personas]
      output_field: personas
      pause: none
      model: sonnet
---
Recette d'essai, hors du dépôt.
