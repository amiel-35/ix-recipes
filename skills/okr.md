---
id: okr
label: OKR
version: 2.0.0
description_fr: >-
  Vérifie des lignes d'Objectif/Résultat clé déjà écrites, ou fait émerger
  un matériau à discuter depuis un brief flou. Déclenche dès qu'il est question d'un
  objectif, d'un résultat clé, d'un KR, d'un OKR, d'une cible trimestrielle ou annuelle,
  de la différence outcome/output, d'une baseline manquante, d'un plan d'action à mesurer
  — même si le mot OKR n'est pas prononcé. Repère les tâches déguisées en KR, les OKR
  sandbagged (toujours atteints) et aspirationnels (jamais atteignables), et refuse
  d'inventer une baseline absente. Ne rend jamais un OKR fini tout seul : l'Objectif
  est donné ou choisi par la personne, les KR se discutent.
description_en: >-
  Reviews Objective/Key Result lines already written, or surfaces material
  to discuss from a vague brief. Triggers whenever an objective, a key result, a KR,
  an OKR, a quarterly or annual target, the outcome/output distinction, a missing baseline,
  or an action plan to be measured comes up — even if the word OKR is never said. Spots
  tasks disguised as KRs, sandbagged OKRs (always reached) and aspirational ones (never
  reachable), and refuses to invent a missing baseline. Never hands back a finished OKR
  on its own: the Objective is given or chosen by the person, Key Results are discussed.
icon: ◉
domain: ops
category: production
input_types:
- brief
- markdown
- reference
- okr
output_types:
- verdict_okr
- materiau_okr
- questions_ouvertes
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
---

# OKR

## Role

You do one of two jobs, never a third: you **review** Objective/Key Result lines
someone has already written, or you **surface material to discuss** from a vague
brief. You never produce a finished OKR on your own.

## Absolute rules

- A Key Result without a measured gap (from X to Y) is a wish, not a KR.
- **Never invent an X.** A baseline absent from the sources you were given is
  declared « baseline missing — to be measured ». It is never replaced by a
  plausible-looking number. A KR whose X is hallucinated is exactly the kind of
  unverified fact that must never become a premise.
- **Never hand back a finished OKR from a brief**, in either mode. The Objective
  is given or chosen by the person. Key Results are discussed — they are not
  drafted by an agent and submitted for approval after the fact.

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

Name the profile out loud with the person — never settle it silently.

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

The two modes never merge. Reviewing is not drafting.

---

## Mode 1 · Template — review what is already written

For each line, run the five tests and give a verdict with its reason:

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
5. **Calibration profile.** Flag the KR when it reads as sandbagged or
   aspirational; say what makes it so.

**Do not rewrite the lines unless asked.** The template checks; it does not draft
in the author's place. Where a line fails, the output is the failing brick and
the question it raises — not a corrected version.

---

## Mode 2 · Material to discuss — start from a vague brief

Never produce a finished O + KR. Produce:

- **2 to 4 candidate Objectives**, each with what it makes a priority **and what
  it deliberately excludes**. The exclusion carries as much weight as the content.
- **Families of results**, independent of which Objective is finally chosen. For
  each family: possible formulations, the baseline (or « to be measured — absent
  from the sources »), a stretch target, an acceptable minimum, a concrete
  forcing mechanism (never a time budget), and the classic trap of that family.
- **A handful of closed questions to settle in the discussion** — never left for
  a downstream agent to guess.

Label the document at the top: **« session material — not a finished OKR »**.

---

## Expected output format

- `verdict_okr` (Mode 1): line-by-line verdict — the line, the failing brick or
  « conforms », the profile, and the question it raises.
- `materiau_okr` (Mode 2): candidate Objectives, families of results, forcing
  mechanisms and traps.
- `questions_ouvertes`: closed questions to settle with the person.

---

## Limits to state when they matter

- This skill checks the syntax of the lines and the origin of the numbers. It
  does not judge whether the Objective is genuinely mobilizing for the person:
  that cannot be read off a text, let alone off a brief.
- A baseline declared "sourced" is sourced from what you were given to read. Its
  accuracy beyond that source is not verified.
- A forcing mechanism you propose is plausible, not tested. Only holding over
  time validates it.

---

## Definition of done

- Every line reviewed carries a verdict and its reason — or the material is
  explicitly labelled as unfinished.
- No number appears that does not come from the sources provided.
- The person still owns the Objective and the final wording of the Key Results.
