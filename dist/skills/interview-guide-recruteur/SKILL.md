---
name: interview-guide-recruteur
description: "Prepares the recruiter-side interview guide for ONE round \u2014 STAR questions, recruiter annotations, scenarios, weighted 1-4 scoring grid, graduated red flags, Go/No-go debrief sheet, legal frame for questions. Reads the `round_brief` produced by `interview-loop-planner` or derives competencies from the job description. Triggers when the user must run a specific, well-equipped interview. Triggers on \"prepare the interview guide for this role\", \"STAR questions for the technical round\", \"scoring grid for this interview\", \"what red flags to watch for in this interview\", \"here is the round 3 brief, prepare the guide\". Does not design the full recruitment loop \u2014 see `interview-loop-planner`, which produces the briefs feeding this guide round by round."
---
# Role

You prepare the guide that one interviewer (or a pair) will use for one interview round. The interviewer reads it before the meeting and takes notes in it during the meeting; a colleague who interviews the next candidate must be able to score the same answer the same way. The guide serves that comparability: the same questions, the same evidence sought, the same scale, scored before the debrief.

The guide is written before any candidate is met, so write it about the role and assume nothing about a person; this keeps the interviewer from arriving with a prior (confirmation bias).

# Expected inputs

- **`round_brief`** produced by `interview-loop-planner` (preferred), in this format:
  ```
  round_brief: round_number, round_name, objective, target_competencies, round_coefficient,
  format, duration_minutes, interviewer_profile, position_level, specific_context
  ```
- Otherwise: the job description or the recruitment need, with the expected level.

Parameters, when the form supplies them: `role_title`, `level` (junior / confirmed / senior / director: calibrates depth and the behaviours in the scoring grid), `round_focus` (main dimension of the round: technical, behavioural, leadership, collaboration, culture fit, scenario), `competencies` (target competencies; if empty, take them from the brief or the job description), `fiche_poste_file` (job description or `round_brief`).

**With a `round_brief`:** evaluate **only** its `target_competencies`; reuse its `round_coefficient` and `duration_minutes`; shape the questions to its `format` (a 60-minute scenario is not a 30-minute screening call) and anchor them in its `specific_context`. The loop planner has spread the competencies across rounds so that none is assessed twice or forgotten; a guide that evaluates everything again breaks that split and gives a competency double weight without anyone deciding it. **Without it:** pick 2 to 4 competencies from the job description (beyond four, an interviewer cannot collect evidence on each) and say that you chose them. If a competency is vague ("team player", "dynamic"), propose an observable reformulation before writing questions on it.

# References

This skill ships its reference files in `references/`. Read them as follows, and only these:

- **Competencies by job family**: `metier_tech.md`, `metier_commercial.md`, `metier_finance.md`, `metier_rh.md`, `metier_juridique.md`, `metier_ops.md`, `metier_marketing.md`, `metier_direction.md`. Identify the job family and read only the matching file (two if the role spans two families, saying which competency comes from which). It gives the coefficient of each competency (x3 core, x2 secondary, x1 complementary) and the behaviours per level.
- **`transverse_anti_biais.md`**: read it when you write the recruiter instructions and the checklists; the instructions point to it.

If `references/` is not available (skill pasted without its folder), ask for the organisation's competency framework or work from the job description, and say so. Keep in any case: each interviewer notes alone, with written evidence, before the debrief; a gap of more than 1.5 points between two interviewers on the same competency is discussed with evidence; watch for affinity, halo, confirmation, attribution, cultural and pedigree bias.

# Legal frame (France, checked 2026-10-16)

| Rule | What it imposes on the guide | Source |
|---|---|---|
| C. trav. L1221-6 | Information asked of a candidate serves only to assess their ability to do the job; it must have a direct and necessary link with the job. Tie each question to one target competency. | Légifrance |
| C. trav. L1221-8 | The candidate is told in advance of the methods and techniques used to assess them, which must be relevant; results are confidential. Provide a line to tell the candidate the format beforehand (scenario, exercise, case). | Légifrance |
| C. trav. L1132-1 | Grounds of exclusion: origin, sex, age, family situation, pregnancy, health, disability, sexual orientation, beliefs, union activity, appearance, surname, place of residence, and others. | Légifrance |
| C. trav. L1225-2 | A woman candidate is not required to disclose a pregnancy. | Légifrance |
| CNIL, HR retention referential (published 2 April 2026, updated 20 May 2026), recruitment section | Unsuccessful candidate: file kept in the active base for the length of the procedure, then up to 5 years from the date the post is filled, as evidence against a discrimination claim (art. L1134-5); talent pool: up to 2 years from the last contact, unless the candidate objects. Interview notes follow the same rule. | cnil.fr |

**Questions not to ask:** children or plans for children, pregnancy, marital status, age, origin, nationality of parents, religion, health, address, bank domiciliation, union or political activity. If the job has a real constraint (travel, hours, on-call duty), **describe the requirement and ask every candidate whether they can meet it**, in the same words; never ask about family life to guess whether they can. When a manager asks for such a question, refuse it in the guide, give the rule, and put the compliant version in its place.

Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check".

Then check what the role calls for beyond this list (a regulated condition of access, a safety-sensitive post, a job exposed to minors or to customers' data): a requirement that is legitimate for the job is put to every candidate in the same words and tied to a competency. A list focuses attention, and what it does not name gets missed. Mark what you add "to check" unless you can source it.

# Method

1. **Frame the round.** Role, level, target competencies and their coefficients, format, duration. Identify whether the role involves management or cross-team exposure; this adds a competency only if the brief includes it.
2. **Group the questions by target competency**, not by a fixed list of dimensions. A round evaluates two to four of them.
3. **Write the questions.** For each competency, open behavioural questions built for STAR evidence (Situation, Task, Action, Result), each with 2 to 3 follow-up probes. Default probes when the candidate stays vague: "What did you do yourself?" and "What was the measurable result?". Recall the STAR method at the top of the guide.
   - Give each question a **recruiter note** ("What we are probing: ..."), separate from the probes. It lets a second interviewer score the same answer the same way.
   - Ask one question at a time and do not lead ("We value collaboration, how collaborative are you?" tells the candidate the answer). Use a situational question ("What would you do if...") only for a domain in which the candidate has no experience.
   - Anchor each question in the role's context (`specific_context` or the job description), because a generic question produces generic answers.
4. **Scenarios** in proportion to the format and duration: a screening call needs none; a scenario round is built around one. Each scenario has the situation in 3 to 4 lines, what to observe, positive signals and red flags. Warn the candidate beforehand (L1221-8).
5. **Scoring grid, 1 to 4**, aligned with `interview-loop-planner`:
   - a behavioural descriptor per level (1 insufficient, 2 partial, 3 solid, 4 excellent) for each competency, each level distinguished by a **behaviour**, not an adjective;
   - coefficients x3 / x2 / x1 taken from the reference or the `round_brief`, not reinvented;
   - weighted average = Σ(coefficient × score) / Σ coefficients; give the arithmetic for this round's coefficients (for 3 + 3 + 2 = 8, the total is between 8 and 32);
   - default bands on the weighted average: below 2.0 insufficient (less than "partial"), 2.0 to 2.74 to investigate, 2.75 to 3.49 solid (around level 3), 3.5 and above excellent (mostly 4s); express them also as totals for this round. The user may change them, before the first candidate;
   - **floor**: a score below 2 on an x3 competency means No-go unless the interviewer documents in writing why not, because a high average can hide a disqualifying gap.
   - the round's `round_coefficient` is given to the consolidated scorecard of the loop; it does not enter the computation here.
6. **Red flags** at two levels: red (disqualifying alone, or with another red) and orange (to investigate, not eliminatory alone). Write each as an **observable behaviour** and what it probably reveals: "attributed every team result to themselves when asked who did what" can be checked and discussed; "arrogant" cannot.
7. **Note-taking template**: a block per competency with space for facts and quotes, the score, and a separate line for gut feelings; mark what was observed directly, what is a weak signal, and what needs checking in a later round.
8. **Culture or fit, only if the round has it as a target competency.** An unstructured fit conversation is where the forbidden grounds enter. Keep it only with observable criteria tied to the job ("has arbitrated between speed and quality in front of a client and explains how"); otherwise leave it out and say why. Note the candidate's own questions, but score them only if they are part of a target competency.
9. **Expected response profile**: 5 to 6 lines describing what a good candidate shows for this round, the interviewer's reference point.
10. **Recruiter instructions** at the top: leave silences; do not feed answers; present the job in detail after the questions, not before, because describing it first tells the candidate what to answer; note facts and quotes; score the same day, alone, before the debrief. Point to `transverse_anti_biais.md` and its checklists. The guide stays with the interviewers and is not sent to the candidate, since the notes reveal what is scored.

The `debrief_sheet` is **individual** (one interviewer, one round). The collective debrief follows the protocol of `interview-loop-planner`.

<example>
Competency: giving feedback to a peer (x2).
Question: "Tell me about a time you had to tell a colleague that their work did not meet the standard." Probes: "What exactly did you say?", "What happened next?"
What we are probing: whether the feedback was specific and delivered directly, and whether the candidate followed up.
1 insufficient: avoided the conversation, or reports only the colleague's faults.
2 partial: raised it, in general terms ("it wasn't great"), no follow-up.
3 solid: named the gap with a concrete example and agreed a change with the colleague.
4 excellent: as 3, then checked the result and adjusted their own approach afterwards.
Why it is right: each level differs by something the candidate did, so two interviewers hearing the same answer land on the same score.
</example>

# Expected output format

This is the default format; an explicit request from the user wins. Output names kept (the guide is a form for the interviewers, so the sheets are left blank for them).

1. **Synthesis** (3 to 5 lines): the round, target competencies with coefficients, format and duration, what the interviewer decides at the end and the floor.
2. `recruiter_instructions`: posture, STAR reminder, legal reminders, pointer to the anti-bias reference.
3. `interview_structure`: table block / minutes / competency / format; the total equals the round's `duration_minutes`.
4. `recruiter_interview_guide`, by competency: table question / probes / recruiter note (what we are probing) / competency. Then the **scoring grid in a separate table**: competency / coefficient / 1 / 2 / 3 / 4, each cell a behaviour. Scenarios on their own sheet (situation, what to observe, positive signals, red flags).
5. **Note-taking template**: per competency, facts and quotes / score / what was observed, weak signal, to check later; a separate line for gut feeling.
6. `watch_points`: table level (red or orange) / observable behaviour / what it probably reveals.
7. `expected_response_profile` (5 to 6 lines).
8. `debrief_sheet`, blank and individual: score per competency, weighted average and band, floor check, 3 strengths, 3 watch points, red flags, Go / Conditional Go / No-go, conditions of success, retention note.

# Definition of done

- Every target competency of this round is covered, and nothing else is evaluated.
- Each question is tied to one competency, has a recruiter note and at least two probes.
- The scoring grid has behavioural descriptors, coefficients inherited from the brief or reference, weighted-average bands whose arithmetic matches the round's coefficients, and the floor.
- The schedule fits the round's duration; scenarios are proportionate to the format.
- Red flags are observable behaviours.
- No question touches a ground of L1132-1; any constraint is asked of all candidates in the same words.
- The candidate is told of the format in advance; the guide stays with the interviewers.

<!-- Behavioural anchors by level, and the question-writing tips (no leading question, one question at a time, situational questions only without domain experience), adapted from anthropics/knowledge-work-plugins, small-business/skills/job-post-builder/reference/interview-guide-structure.md (L69-75, L87-93) (Apache-2.0, commit 33eeda1): rewritten on a 1-4 scale and fitted to French law (L1221-6, L1221-8, L1132-1). See THIRD_PARTY.md. -->
