---
name: amont-sujet
description: "Plays the upstream of the \u00ab treat a subject end to end \u00bb procedure (steps 1 to 3) for a code subject: scoping, questions, merge and split, evaluation against the fixed grid, closing, form check of the \u00ab deliverable to format skill \u00bb list, goal, goal check, success criteria with their hidden part, a stop before the counter-check by Fable, reconciliation. Each step is isolated, the three verification loops are bounded by the settings' ceiling, and the hidden part of the criteria never leaves its field. Triggers on \u00ab start the upstream of this subject \u00bb, \u00ab run steps 1 to 3 of the procedure \u00bb, \u00ab prepare the goal and the criteria of this subject \u00bb. Does not produce the deliverable, freezes nothing and never calls Fable \u2014 see the downstream tools of the harness."
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
