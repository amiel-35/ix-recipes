---
id: amont-sujet
label: Amont d'un sujet
version: 1.0.0
description_fr: "Joue l'amont de la procédure « traiter un sujet de bout en bout » (étapes 1 à 3) pour un sujet de code : cadrage, questions, fusion et découpage, évaluation contre la grille fixe, clôture, vérification de forme de la liste « livrable vers skill de format », goal, vérification du goal, critères de réussite avec leur part cachée, arrêt avant la contre-vérification par Fable, réconciliation. Chaque étape est isolée, les trois boucles de vérification sont bornées par le plafond des réglages, et la part cachée des critères ne sort jamais de son champ. Déclenche sur « lance l'amont de ce sujet », « fais l'étape 1 à 3 de la procédure », « prépare le goal et les critères de ce sujet ». Ne produit pas le livrable, ne gèle rien et n'appelle jamais Fable — voir les outils de l'aval du harnais."
description_en: "Plays the upstream of the « treat a subject end to end » procedure (steps 1 to 3) for a code subject: scoping, questions, merge and split, evaluation against the fixed grid, closing, form check of the « deliverable to format skill » list, goal, goal check, success criteria with their hidden part, a stop before the counter-check by Fable, reconciliation. Each step is isolated, the three verification loops are bounded by the settings' ceiling, and the hidden part of the criteria never leaves its field. Triggers on « start the upstream of this subject », « run steps 1 to 3 of the procedure », « prepare the goal and the criteria of this subject ». Does not produce the deliverable, freezes nothing and never calls Fable — see the downstream tools of the harness."
summary_fr: "L'amont d'un sujet de code : cadrage clos, goal et critères de réussite, jusqu'au gel, avec des boucles bornées et un arrêt avant Fable."
icon: ⇉
domain: ops
category: workflow
input_types:
- brief
- markdown
output_types:
- cadrage_clos
- goal
- criteres
compatible:
- claude-code
requires: [ix-skills:cadrage, ix-skills:questioning, ix-skills:decomposer, ix-skills:controle-qualite, ix-skills:goal-writing, ix-skills:critique, ix-skills:criteres-reussite]
workflow:
  format: 4
  context_sheet: [subject, objective, constraints, readers, deliverables, named_solutions, deadlines]
  context_labels:
    subject: "Sujet"
    objective: "But"
    constraints: "Contraintes"
    readers: "Lecteurs"
    deliverables: "Livrables"
    named_solutions: "Solutions déjà nommées"
    deadlines: "Échéances"
  steps:
    - id: cadrage
      label: "1a. Cadrage de la demande"
      stage: "1a"
      role: cadrage_et_criteres
      skill: ix-skills:cadrage
      mission: Clarify the need from the raw request in its default mode, not the closing mode — the goal behind it (a goal, not an artefact), the facts, the constraints each with its reason, the named solutions treated as hypotheses, the options — and stop at clarification.
      receives: [brief]
      transmits: [need, constraints, hypotheses, open_points]
      produces_context_sheet: true
      pause: validate
      model: opus
    - id: questions
      label: "1b. Questions qui débloquent"
      stage: "1b"
      role: cadrage_et_criteres
      skill: ix-skills:questioning
      mission: Generate the questions that unblock the subject and expose its blind spots, most blocking first, from the scoped need and its open points. Questions only, no answers.
      receives: [context_sheet, cadrage.need, cadrage.constraints, cadrage.hypotheses, cadrage.open_points]
      transmits: [questions]
      pause: none
      model: opus
    - id: fusion
      label: "1c. Fusion et découpage"
      stage: "1c"
      role: cadrage_et_criteres
      skill: ix-skills:decomposer
      mission: "Merge the questions of the previous step with the open points of the scoping, without duplicates on the named solutions, each blocking question with a default answer. Then apply the four splitting tests one by one with a verdict and its reason (parts accepted separately with their own users; one grid no longer replayed in about an hour; a part depending on an undecided decision; stakeholders with conflicting interests to arbitrate apart), and say which part starts now if one is true. The complete output is the submitted scoping: intent, audience and situation of use, decisions to take, constraints with reasons, scope and out of scope, stakeholders, deliverables with their reader and the documentation, remaining assumptions with their risk, splitting tests. If a verdict of the evaluation is given as an input, correct only the defects it names and keep the rest."
      receives: [context_sheet, cadrage.need, cadrage.constraints, cadrage.hypotheses, cadrage.open_points, questions.questions]
      transmits: [cadrage]
      output_field: cadrage
      pause: none
      model: opus
    - id: evaluation
      label: "1d. Évaluation du cadrage"
      stage: "1d"
      role: evaluation_cadrage
      skill: ix-skills:controle-qualite
      mission: "Judge the submitted scoping against the fixed grid of the scoping (the piece named A5 in the dossier's corpus) in verdict mode: the grid is the reference, the scoping is the deliverable, one verdict per point, never one on the whole. Before the pause only G1, G2, G4 to G8 apply; G3 and G9 are noted as waiting for pause 1, without a verdict. In every verdict separate what waits for the pause from a defect that can be corrected now. The first line of the verdict field is OK when no point is a correctable breach, REPRENDRE otherwise; then one line per point. In the other field, list the blocking questions the pilot must answer at pause 1, each with its default answer."
      receives: [fusion.cadrage, corpus]
      transmits: [verdict, attente_pause_1]
      verdict_field: verdict
      loop: {to: fusion, ceiling: passes_verification_max}
      pause: answers
      model: opus
    - id: cloture
      label: "1e. Clôture du cadrage"
      stage: "1e"
      role: cadrage_et_criteres
      skill: ix-skills:cadrage
      mission: "Apply the closing mode of the skill, asked explicitly: close the submitted scoping with the pilot's answers as decisions that quote them, a default accepted without remark marked as such and recalled to the decider, a blocking question left unanswered turned into the residual question. Write to hold the fixed grid (the piece named A5 in the corpus): nothing marked to confirm in a closed scoping, a recall instead. In the second field write the list « deliverable to format skill » of the subject's type, computed from the settings (the piece named A4 in the corpus, key skills_de_format of the type), one line per deliverable: the form expected, not who produces it."
      receives: [context_sheet, fusion.cadrage, evaluation.attente_pause_1, answers, corpus]
      transmits: [cadrage_clos, liste_skills_de_format]
      output_field: cadrage_clos
      pause: none
      model: opus
    - id: verif_livrables
      label: "Vérification de forme de la liste des skills de format"
      stage: "1e"
      role: verification_mecanique
      skill: ix-skills:controle-qualite
      mission: "Compare, mechanically and read-only, the list « deliverable to format skill » of the closing step with the association of the settings (the piece named A4 in the corpus, key skills_de_format of the subject's type): every deliverable of the closed scoping that has a line there, no skill added, none dropped, none renamed. The first line of the verdict field is OK when the list matches, REPRENDRE otherwise; then the differences, one per line. Do not correct the list."
      receives: [cloture.liste_skills_de_format, cloture.cadrage_clos, corpus]
      transmits: [verdict]
      verdict_field: verdict
      pause: none
      model: haiku
    - id: goal
      label: "2A. Rédaction du goal"
      stage: "2A"
      role: redaction_goal
      skill: ix-skills:goal-writing
      mission: "Write the goal of the autonomous agent that will produce the deliverables, from the closed scoping, the settings (the piece named A4 in the corpus: turn ceiling, model of each role, limits of the sub-agents, suites offered at a ceiling, freezing) and the list « deliverable to format skill ». You receive no success criteria and no grid, and you write for none. The complete goal goes in the first field, the writer's notes in the second, never in the goal. If a verdict of the verification is given as an input, correct only the defects it names."
      receives: [context_sheet, cloture.cadrage_clos, cloture.liste_skills_de_format, corpus]
      transmits: [goal, notes_redacteur]
      pause: none
      model: sonnet
    - id: verif_goal
      label: "2A. Vérification du goal"
      stage: "2A"
      role: verification_goal
      skill: ix-skills:critique
      mission: "Critique the goal under exactly four imposed angles: ambiguities, testability, implicit assumptions, open questions left without an answer. The first line of the verdict field is OK when none of the four angles shows a defect that must be corrected before the production, REPRENDRE otherwise; then the defects, each with the passage and the angle. Never propose the correction."
      receives: [goal.goal, goal.notes_redacteur, cloture.cadrage_clos]
      transmits: [verdict]
      verdict_field: verdict
      loop: {to: goal, ceiling: passes_verification_max}
      pause: none
      model: opus
    - id: criteres
      label: "2B. Critères de réussite"
      stage: "2B"
      role: cadrage_et_criteres
      skill: ix-skills:criteres-reussite
      mission: "Write the success criteria from the closed scoping alone — you see neither the goal nor any producer's work — with the domain annexes the settings name for the subject's type (the piece named A4 in the corpus, key annexes_criteres). Put the visible grid (mechanical part, review part) in the first field, the open questions of the grid in the third. The HIDDEN part, known to the judge alone, goes into the second field and nowhere else: not in your document, not in a summary, not in any other field, not even its titles or the names of its parts. If a verdict of the counter-check is given as an input, correct only the defects it names, hidden part included."
      receives: [context_sheet, cloture.cadrage_clos, corpus]
      transmits: [grille_visible, part_cachee, questions_ouvertes]
      hidden: [part_cachee]
      pause: none
      model: opus
    - id: contre_verif
      label: "2B. Contre-vérification (à part, après accord)"
      stage: "2B"
      skill: ix-skills:critique
      mission: "Counter-check the grid of criteria, hidden part included, with the angles of the verification of the goal and the question « what would pass and still be wrong? ». The first line of the verdict field is OK when nothing must be reworked, REPRENDRE otherwise; then the defects. This step is not played by the runner: the pilot calls the other model after giving their agreement, and hands the output back."
      receives: [criteres.grille_visible, criteres.part_cachee, cloture.cadrage_clos]
      transmits: [verdict]
      verdict_field: verdict
      loop: {to: criteres, ceiling: passes_verification_max}
      external: true
    - id: reconciliation
      label: "3. Réconciliation"
      stage: "3"
      role: reconciliation
      skill: ix-skills:controle-qualite
      mission: "Reconcile, in verdict mode, the goal, the visible grid and the closed scoping: the stopping condition of the goal points to the mechanical part of the grid by its slot and says nothing of what it checks; each criterion of the visible grid points to an element of the closed scoping; nothing in the goal contradicts the closed scoping. List the gaps, one per line, each with the passages. Do not correct."
      receives: [goal.goal, criteres.grille_visible, cloture.cadrage_clos]
      transmits: [ecarts]
      pause: validate
      model: sonnet
---

# Role

You orchestrate the upstream of the procedure « treat a subject end to end » for a subject of code: steps 1 to 3, up to the pilot's second pause. You never do the work of a step, and you never decide on substance. This recipe is a **format 4** recipe: it is played by the runner (`scripts/parcours.py`), never in a conversation, because its loops, its hidden field and its stop before an external step need the runner to hold them. The downstream (freezing, production, judgement, correction) is not part of it: the tools of the harness do it.

# Absolute rules

- Every step runs in a fresh context and receives only what its line lists. The raw request goes to the first step alone; a human-validated context sheet replaces it afterwards.
- The goal (2A) and the criteria (2B) are written apart: the step that writes the goal never receives the criteria, the step that writes the criteria never receives the goal.
- The hidden part of the criteria lives in its own field. No later step receives it, the external counter-check apart; the runner keeps it outside the dossier, in the sealed place given at run time.
- The three verification loops (the evaluation of the scoping, the check of the goal, the counter-check of the criteria) are bounded by the ceiling of the settings (`plafonds.passes_verification_max`). At the ceiling the runner stops, writes down the failure and offers exactly the suites the settings define for it; only the pilot chooses.
- Fable is never called here. The recipe stops before the counter-check; the pilot calls the other model after agreeing, and hands the output back, which counts as a pass of the loop.
- Every call carries the model of its role in the settings (`role`).

# Context sheet

| `field` | definition |
|---|---|
| `subject` | the subject in one line: what it is about, and its type (the type of subject of the settings) |
| `objective` | what must become true once the subject is treated, as a goal and not as an artefact to produce |
| `constraints` | what limits the answer, each with its reason when the request gives it |
| `readers` | who receives or uses each result, and in which situation |
| `deliverables` | what the subject must deliver, documentation included, each with its reader |
| `named_solutions` | solutions, tools or artefacts the request already names, kept apart from the need |
| `deadlines` | dates or delays the request states |

# Steps

| Step | Skill | Mission | Receives | Transmits | Pause |
|---|---|---|---|---|---|
| `cadrage` | `ix-skills:cadrage` | scope the need from the raw request | brief | need, constraints, hypotheses, open_points | validate |
| `questions` | `ix-skills:questioning` | the questions that unblock | context sheet, scoping | questions | none |
| `fusion` | `ix-skills:decomposer` | merge, apply the splitting tests, write the submitted scoping | scoping, questions | cadrage | none |
| `evaluation` | `ix-skills:controle-qualite` | judge the scoping against the fixed grid | submitted scoping, corpus | verdict, attente_pause_1 | answers (pause 1) |
| `cloture` | `ix-skills:cadrage` | close the scoping, write the list of format skills | submitted scoping, answers, corpus | cadrage_clos, liste_skills_de_format | none |
| `verif_livrables` | `ix-skills:controle-qualite` | check the list against the settings | the list, corpus | verdict | none |
| `goal` | `ix-skills:goal-writing` | write the goal | closed scoping, list, corpus | goal, notes_redacteur | none |
| `verif_goal` | `ix-skills:critique` | critique the goal under four angles | goal, writer's notes, closed scoping | verdict | none |
| `criteres` | `ix-skills:criteres-reussite` | write the criteria, visible and hidden | closed scoping, corpus | grille_visible, part_cachee, questions_ouvertes | none |
| `contre_verif` | `ix-skills:critique` | counter-check the criteria (external, after agreement) | grid, hidden part, closed scoping | verdict | stop |
| `reconciliation` | `ix-skills:controle-qualite` | reconcile goal, grid and scoping | goal, grid, closed scoping | ecarts | validate (pause 2) |

The `corpus` of the dossier holds the settings (A4) and the fixed grid of the scoping (A5): the harness copies them there when it creates the parcours.

# Running a step

The runner builds each message itself: the text of the skill, the mission, the context sheet, exactly the fields the step receives, and the closing blocks (`## HANDOFF` with one `### field` per transmitted field, then `## SUMMARY`). A verification step starts its verdict field with `OK` or `REPRENDRE`. On `REPRENDRE` the runner sends the parcours back to the step named by the loop, giving it the verdict as an extra input, and plays the steps again from there, until the ceiling.

# Pauses

- `cadrage` ends with the validation of the context sheet.
- `evaluation` ends with pause 1: the pilot answers the blocking questions (or does not, and the default is kept and recalled at the closing).
- `contre_verif` is the stop before the counter-check: the pilot decides, calls the other model, hands the output back.
- `reconciliation` ends with pause 2: the pilot answers the open questions of the grid and may read the hidden part. Freezing follows, by the tools of the harness.

# Trace

The runner writes every output in `./parcours/<slug>/NN-<step>.md`; a hidden field leaves a mark there. The harness builds the trace of the subject (format A3) from the state of the parcours.

# Without sub-agents

There is no fallback: a recipe of format 4 is refused by anything that does not play its format, instead of being played by halves.

# Output

The closed scoping, the goal, the visible grid and the reconciliation, each in its step's output; the hidden part sits in the sealed place.

# Definition of done

The reconciliation is validated by the pilot at pause 2, no ceiling is reached without a suite chosen, and no file of the dossier holds the hidden part.
