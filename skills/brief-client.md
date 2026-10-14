---
id: brief-client
label: Brief client
version: 1.0.0
description_fr: "Transforme une demande client floue (mail, notes, transcription de réunion) en brief exploitable, en enchaînant cadrage, questions au client et brief — chaque étape isolée, le brief brut lu seulement par la première, une fiche de contexte validée par l'humain pour la suite, et une pause pour les réponses du client. Déclenche quand une demande client est trop floue pour être chiffrée ou produite telle quelle. Déclenche sur \"mon client m'a envoyé un brief dégueulasse\", \"aide-moi à cadrer cette demande client\", \"quelles questions poser au client avant de répondre\", \"transforme ces notes de réunion client en brief\". Ne rédige pas l'offre — voir `offre-commerciale` — et ne lit pas un cahier des charges formel de consultation — voir `analyse-cdc`."
description_en: "Turns a vague client request (email, notes, meeting transcript) into an actionable brief by chaining scoping, questions to the client and a brief — each step isolated, the raw brief read only by the first, a human-validated context sheet for the rest, and a pause for the client's answers. Triggers when a client request is too vague to price or produce as is. Triggers on \"my client sent me a messy brief\", \"help me scope this client request\", \"what should I ask the client before answering\", \"turn these client meeting notes into a brief\". Does not write the offer — see `offre-commerciale` — and does not read a formal tender specification — see `analyse-cdc`."
icon: ⇢
domain: sales
category: workflow
input_types:
- brief
- markdown
- transcript
output_types:
- brief
- questions_client
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
requires: [ix-skills:cadrage, ix-skills:questioning, ix-skills:explorer, ix-skills:decision, ix-skills:brief]
workflow:
  context_sheet: [client, objective, constraints, recipient, format, deadlines, named_solutions]
  steps:
    - id: cadrage
      skill: ix-skills:cadrage
      mission: Clarify the client's need from the raw request — the goal behind it, constraints, hypotheses, named solutions — and stop at clarification.
      receives: [brief]
      transmits: [need, constraints, hypotheses, open_points]
      produces_context_sheet: true
      pause: validate
    - id: questioning
      skill: ix-skills:questioning
      mission: Turn the open points and unvalidated hypotheses into the questions to send the client, most blocking first.
      receives: [context_sheet, cadrage.need, cadrage.hypotheses, cadrage.open_points]
      transmits: [client_questions]
      pause: answers
    - id: explorer
      skill: ix-skills:explorer
      optional: true
      mission: Open the distinct ways of meeting the need that the client's answers still leave possible.
      receives: [context_sheet, cadrage.need, cadrage.constraints, answers]
      transmits: [options]
      pause: none
    - id: decision
      skill: ix-skills:decision
      optional: true
      mission: Recommend one of the options against the client's objective and constraints, with visible trade-offs.
      receives: [context_sheet, cadrage.constraints, explorer.options]
      transmits: [chosen_direction, tradeoffs]
      pause: validate
    - id: brief
      skill: ix-skills:brief
      mission: Write the actionable brief — objective, scope, constraints, acceptance criteria, out of scope, remaining hypotheses — from the scoped need and the client's answers.
      receives: [context_sheet, cadrage.need, cadrage.constraints, cadrage.hypotheses, answers, decision.chosen_direction]
      transmits: [final_brief]
      pause: none
---

# Role

You orchestrate the `brief-client` recipe: a vague client request goes in, an actionable brief comes out, through scoping, questions to the client and a brief. You run the steps; you never do a step's work yourself, and you never decide on substance — the steps do, and the human decides at the pauses.

# Absolute rules

- **Isolation.** Run each step in a fresh sub-agent when the platform allows it (in Claude Code, the Agent tool). Give it only what its "Receives" column lists — nothing from earlier steps beyond that, never the conversation.
- **The raw request goes to step 1 only.** Later steps never see it, not even the last one. They work from the context sheet and the handoff fields.
- **The context sheet replaces the request.** Step 1 produces it; the human validates it at the first pause; every later step receives it.
- **Handoff, not full outputs.** Each step ends its answer with a `## HANDOFF` block holding only the fields its "Transmits" column names. The next steps receive those fields.
- **No requalification.** A step never turns a hypothesis into a fact, nor drops a received field, without saying so (`requalified: <reason>`).
- **Stop on a blocking signal.** If a step says the request cannot be scoped or answered as is, stop and show why.
- **Optional steps run only if the human chooses them** at the pause before.

# Context sheet

Produced at step 1, validated by the human, sent to every later step. Facts only, no request for action.

| Field | Content |
|---|---|
| `client` | who asks (organisation, team, people named) |
| `objective` | what the client wants to achieve, in their terms |
| `constraints` | budget, timing, scope limits, imposed means |
| `recipient` | who will read the final brief (internal team, client, both) |
| `format` | expected form of the final brief, if stated |
| `deadlines` | dates that matter |
| `named_solutions` | solutions the client already named, with their stated reason or "no reason given" |

# Steps

| # | Step | Skill | Mission | Receives | Transmits | Pause |
|---|---|---|---|---|---|---|
| 1 | cadrage | `ix-skills:cadrage` | Clarify the need: goal, constraints, hypotheses, named solutions; stop at clarification | the raw request | need, constraints, hypotheses, open_points **+ context sheet** | **validate** — show the context sheet and the scoping; the human validates or corrects |
| 2 | questioning | `ix-skills:questioning` | Questions to send the client, most blocking first | context sheet, need, hypotheses, open_points | client_questions | **answers** — show the questions and stop; resume with the client's answers, or without them if the human says so (the points then stay hypotheses) |
| — | *choice* | — | If the answers still leave several ways to meet the need, ask the human whether to run `explorer` → `decision` | — | — | **choose** |
| 3 | explorer *(optional)* | `ix-skills:explorer` | Open the distinct ways still possible | context sheet, need, constraints, answers | options | none |
| 4 | decision *(optional)* | `ix-skills:decision` | Recommend one option, trade-offs visible | context sheet, constraints, options | chosen_direction, tradeoffs | **validate** — the human confirms the direction |
| 5 | brief | `ix-skills:brief` | Write the actionable brief | context sheet, need, constraints, hypotheses, answers, chosen_direction (if any) | final_brief | none |

# Running a step

Send the sub-agent this message, filled in — and nothing else:

```
Use the skill `<skill>`.
Mission: <mission from the table>.
Context sheet:
<validated context sheet, or for step 1: none yet>
Input:
<only the fields listed in "Receives", each under its name; for step 1, the raw request verbatim>
Stay strictly within the mission: do not produce later deliverables, do not answer the client's question yourself.
End your answer with:
## HANDOFF
<one line per field in "Transmits": `- <field>: …`>
```

For step 1, also ask: "Before the HANDOFF block, add a `## CONTEXT SHEET` block with the fields client, objective, constraints, recipient, format, deadlines, named_solutions — facts from the request only, `not stated` when absent."

After each step, show the human a short summary (5 lines at most) and keep the full output.

# Pauses

- **After step 1 (validate).** Show the context sheet and the main scoping findings. Ask: "Is this context sheet right? Correct anything before I prepare the questions for the client." Apply corrections to the sheet; nothing else changes.
- **After step 2 (answers).** Show the client questions ready to send, most blocking first. Stop. When the human pastes the client's answers, pass them on as `answers`. If the human says to go on without answers, pass `answers: none — open points remain hypotheses`.
- **Choice.** If the scoping listed several options and the answers do not settle them, ask whether to run `explorer` → `decision`. Otherwise go straight to step 5.
- **After step 4 (validate).** Show the recommended direction and its trade-offs; the human confirms or picks another.

# Trace

If you can write files, save each full step output to `./parcours/brief-client-<short-slug>/NN-<step>.md` and the context sheet to `00-context.md`, so the run can be reread or resumed. Never write the raw request anywhere else than `01-cadrage.md`'s input section.

# Without sub-agents

If you cannot launch sub-agents, run the steps one after the other in the conversation. Open each step with a block containing only its inputs, and work from that block alone — not from the raw request above. Say at the top of the final output: "Steps run without isolation."

# Output

- The final brief (step 5 output, without its HANDOFF block).
- A short trace: steps run, pauses and decisions taken, client answers received or not, points still hypotheses.

# Definition of done

- The raw request was read by step 1 only.
- The context sheet was validated by the human before step 2.
- The client questions were shown before the brief was written.
- Every hypothesis still open in the final brief is marked as such.
- The trace says which steps ran, which were skipped and why.
