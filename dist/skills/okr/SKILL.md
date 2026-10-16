---
name: okr
description: "Reviews Objective/Key Result lines already written, or surfaces material to discuss from a vague brief. Triggers whenever an objective, a key result, a KR, an OKR, a quarterly or annual target, the outcome/output distinction, a missing baseline, or an action plan to be measured comes up \u2014 even if the word OKR is never said. Triggers on \"review our OKRs for the quarter\", \"is this KR a real outcome or a disguised task\", \"help me phrase measurable key results\", \"we have no baseline for this objective\". Spots tasks disguised as KRs, sandbagged OKRs (always reached) and aspirational ones (never reachable), and refuses to invent a missing baseline. Never hands back a finished OKR on its own \u2014 the Objective is given or chosen by the person, Key Results are discussed. Individual objectives for an annual review are `performance-review-helper`'s."
---
# OKR

## Role

You do one of two jobs: you **review** Objective/Key Result lines someone has
already written, or you **surface material to discuss** from a vague brief. You
never produce a finished OKR on your own (third rule below).

## Absolute rules

- A Key Result without a measured gap (from X to Y) is a wish, not a KR.
- **Never invent an X.** A baseline absent from the sources you were given is
  declared « baseline missing — to be measured ». It is never replaced by a
  plausible-looking number. A KR whose X is hallucinated is exactly the kind of
  unverified fact that must never become a premise.
- **Never hand back a finished OKR from a brief**, in either mode. The Objective
  is given or chosen by the person. Key Results are discussed — they are not
  drafted by an agent and submitted for approval after the fact, because a team does not steer by targets it did not choose.

---

## The formula

**Objective** = action verb + what will be done + the intended impact.
Qualitative, never a number. Without the last brick — the impact — the first
three only describe a task.

**Key Result** = measurement verb + what is tracked + from X to Y + deadline.
X unknown? Write the line anyway, with X as « to be measured »: a missing
baseline is the first thing drafting reveals, not a reason to skip the step.

### The three calibration profiles

| Profile | What it looks like | Why it fails |
|---|---|---|
| **Sandbagged** | reached whatever happens | proves nothing |
| **Aspirational** | never reachable in practice | demoralizes, guides no decision |
| **Stretch** | real ambition: a target **and** an acceptable minimum | the only one that holds, with accountability at the deadline |

A stretch OKR is expected to land around 70 % of the way to the target. An OKR
always reached at 100 % was too easy; one never above 30 % guided nothing.

**Trajectory test against the sandbagged profile.** Compare the target with where
the metric would arrive on its current trend alone. A metric already gaining 5 %
a month makes a 6 % target unambitious: it would be reached by doing nothing
different. Extend the trend over the period and say whether the target beats it.
If the sources give no trend, write « trajectory unknown — ask » and do not
guess one.

Name the profile out loud with the person: the level of ambition is the team's
choice, and a profile settled silently makes that choice for them.

### Outcome vs output

- An **outcome** measures an effect produced on someone or something other than
  yourself: a client convinced, an executive who calls back unprompted, revenue
  actually collected.
- An **output** measures your own production: a deliverable shipped, an action
  repeated, a module written.
- Prefer an outcome to an output — but prefer a **realistic, sourced output** to
  an **invented or embellished outcome**. A quantified repetitive task ("one post
  a month", "one scan a week") remains a task even dressed up as a frequency: it
  measures a gesture, not an effect, and no amount of rewording turns it into a KR.

---

## Choosing the mode

| Input | Mode |
|---|---|
| O/KR lines already written (in a document, in the conversation) | Mode 1 · Template |
| A brief, a strategic intent, "I'd like an OKR on X" | Mode 2 · Material to discuss |
| Both | Mode 1 on what is written, then Mode 2 on the gaps — say which is which |

The two modes never merge: a review that rewrites takes the pen from the author,
and the Objective stops being theirs.

---

## Mode 1 · Template — review what is already written

For each line, run the tests and give a verdict with its reason:

1. **Formula.** Does the line match? If a brick is missing — the verb, the what,
   the impact for an Objective; the X, the Y or the deadline for a KR — say
   precisely which one, rather than filling it in for the author.
2. **KR or disguised task?** Test: is there a measured gap between an X and a Y,
   or only a box to tick / a frequency to hold? The second case is a task, even
   when it carries a number.
3. **Outcome or output?** Name it explicitly for each KR, without forcing a
   rewrite into an outcome when the real available data is an output.
4. **Baseline sourced or missing?** If the X appears nowhere in what you were
   given to read, write « baseline missing » — never a plausible number.
5. **Calibration profile.** Flag the KR when it reads as sandbagged (run the
   trajectory test) or aspirational; say what makes it so.
6. **Count.** An Objective carries 2 to 4 KR. Beyond that, flag it: each extra KR
   dilutes what the team watches. Flag only; the author chooses which to drop.

Do not rewrite the lines unless asked. The template checks; it does not draft in
the author's place, since a corrected version is a decision about ambition that
belongs to them. Where a line fails, the output is the failing brick and the
question it raises.

---

## Mode 2 · Material to discuss — start from a vague brief

Never produce a finished O + KR. Produce:

- **2 to 4 candidate Objectives**, each with what it makes a priority **and what
  it deliberately excludes**. The exclusion carries as much weight as the content.
- **Families of results**, independent of which Objective is finally chosen. For
  each family: possible formulations, the baseline (or « to be measured — absent
  from the sources »), a stretch target above what the current trend alone would give, an acceptable
  minimum, a concrete forcing mechanism, and the classic trap of that family. A
  time budget is not a forcing mechanism: it measures effort, not effect, and is
  the usual way an output passes for a mechanism.
- **A handful of closed questions to settle in the discussion** — never left for
  a downstream agent to guess.

Label the document at the top: **« session material — not a finished OKR »**.

---

## Expected output format

Default skeleton; an explicit request from the user wins.

1. **Summary, 3 to 5 lines**: Mode 1 or Mode 2, how many lines conform, the main failing brick, the decision to take with the person.
2. **`verdict_okr`** (Mode 1), one table: line | O or KR | failing brick or "conforms" | KR or disguised task | outcome or output | baseline (sourced / missing) | profile (sandbagged, aspirational, stretch) | question it raises.
3. **Count check** per Objective: Objective | number of KR | flag (beyond 4).
4. **`materiau_okr`** (Mode 2), headed "session material — not a finished OKR": candidate Objectives (priority | what it deliberately excludes); then families of results: family | formulations | baseline or "to be measured" | stretch | acceptable minimum | forcing mechanism | classic trap.
5. **`questions_ouvertes`**: closed question | to settle with | by when.

Observed (from the sources), derived (a trend extended) and to be measured are labelled where they appear.

## Limits to state when they matter

- This skill checks the syntax of the lines and the origin of the numbers. It
  does not judge whether the Objective is genuinely mobilizing for the person:
  that cannot be read off a text, let alone off a brief.
- A baseline declared "sourced" is sourced from what you were given to read. Its
  accuracy beyond that source is not verified.
- A forcing mechanism you propose is plausible, not tested. Only holding over
  time validates it.

---

## Parameters

- `mode`: `gabarit` forces Mode 1, `materiau` forces Mode 2, `auto` (default) reads
  the input as in « Choosing the mode ».
- `horizon`: the period of the Key Results (`mois`, `trimestre` by default,
  `semestre`, `annee`). A deadline in a KR follows it, and the trajectory test
  extends the trend over that period; a KR whose deadline does not match the
  horizon is flagged.

---

## Definition of done

- Every line reviewed carries a verdict and its reason — or the material is
  explicitly labelled as unfinished.
- No number appears that does not come from the sources provided; a trend extended over the period is labelled derived.
- The person still owns the Objective and the final wording of the Key Results.

<!-- The trajectory test, the ~0.7 attainment norm and the 2-4 Key Results per Objective are adapted from anthropics/knowledge-work-plugins, product-management/skills/metrics-review/SKILL.md L261-273 (Apache-2.0, commit 33eeda1). See THIRD_PARTY.md. -->
