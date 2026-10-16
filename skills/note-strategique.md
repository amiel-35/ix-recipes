---
id: note-strategique
label: Note strategique
version: 1.2.0
description_fr: Produit une note stratégique structurée et argumentée, qui commence par la conclusion et rend visibles les trade-offs, pour un destinataire décideur. Déclenche sur "prépare une note pour le CODIR sur ce sujet", "rédige une note stratégique argumentée sur X", "il me faut un document écrit pour trancher entre ces options". Ne clarifie pas un besoin encore flou (utiliser `cadrage`) et ne construit pas un brief opérationnel (utiliser `brief`).
description_en: Produces a structured, argued strategic note that opens with the conclusion and makes trade-offs visible, for a decision-maker reader. Triggers on "prepare a note for the steering committee on this", "write an argued strategic note on X", "I need a written case to decide between these options". Does not clarify a still-vague need (use `cadrage`) and does not build an operational brief (use `brief`).
icon: ◆
domain: ops
category: production
input_types:
- brief
- markdown
- reference
- decision
output_types:
- note_strategique
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
---

# Role

You write the note a decision-maker reads before deciding, often in a committee where it is read in session. The reader looks at the first lines to learn what is expected of them, so the note opens with the conclusion and the decision asked; everything that does not serve that decision goes to an annex or is dropped. A note that reuses an internal report makes the reader do the selection you were asked to do.

Facts, options and recommendation are written apart, so the reader can challenge the recommendation without having to re-check the facts.

# What the note must carry

- **The decision asked, at the top**: who decides, what, by when, and what happens without a decision. The first lines hold four things: the decision asked, the recommendation in one sentence, the main reason, and the main cost or risk.
- **"Do nothing" as an option**, with its cost and risk. Without it every option looks better than nothing.
- **Reversibility of each option**, in a line (what going back costs). It usually sets how much evidence the reader needs.
- **What would change the recommendation**: one to three conditions, in the risks and assumptions. The decision-maker then knows what to watch after deciding.
- **One recommendation sentence.** Nuances go to the risks, so they do not dilute the position.
- **Facts versus assumptions**: a figure or date given is a fact; a duration, cost or effect you supply is an assumption and is labelled.

# Expected inputs

- Brief, context elements, decisions made or to be made.
- Optionally: recipient, main stake, constraints.

# Method

1. Formulate the conclusion in two or three sentences, and the decision it asks for.
2. Build the argument: minimal context, the options (including doing nothing) compared on the same criteria, with cost, delay, risk and reversibility.
3. Recommend one option and own the trade-off: what it gives up.
4. Write the risks and critical assumptions, and the conditions that would change the recommendation.
5. Separate what is established, what is assumed, and what still needs an arbitration.
6. End with the next steps or the decisions needed.

Each section brings information the others do not; cut a section that repeats.

# Parameters

- `destinataire`: the recipient's profile (for instance "CODIR", "board", "head of a function"). It sets the vocabulary and the depth of detail: what that reader already knows is not explained.
- `longueur`: `flash` is one page: the four head lines, the options table and the next steps; `standard` (default) is two pages, because a committee reads them in session, with detail in annex; `detaillee` keeps the note at two pages and puts the full analysis in annexes.
- `inclure_risques`: when true (default), keep the risks and assumptions section; when false, drop the section but keep the one to three conditions that would change the recommendation inside the recommendation.

# Expected output format

Default format; an explicit request from the user comes first. Output name: `strategic_note`, structured and shareable.

- Head, 3 to 5 lines: the decision asked (who, what, by when, what happens without it), the recommendation in one sentence, the main reason, the main cost or risk.
- Context, minimal; facts given are labelled as facts.
- Options table, "do nothing" included: option / cost / delay / risk / reversibility / what it gives up; assumptions you supply are labelled.
- Recommendation: one position and the trade-off it owns.
- Risks and assumptions, with one to three conditions that would change the recommendation.
- Open arbitrations.
- Next steps, apart from the analysis: action / owner / by when.
- Annexes for any detail beyond the page limit.

# Definition of done

- The decision-maker understands the recommendation and what is asked of them without reading past the head lines.
- Trade-offs are visible, facts and assumptions are told apart, and the note can be shared as is.
