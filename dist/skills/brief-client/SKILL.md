---
name: brief-client
description: "Turns a vague client request (email, notes, meeting transcript) into an actionable brief by chaining scoping, questions to the client and a brief \u2014 each step isolated, the raw brief read only by the first, a human-validated context sheet for the rest, and a pause for the client's answers. Triggers when a client request is too vague to price or produce as is. Triggers on \"my client sent me a messy brief\", \"help me scope this client request\", \"what should I ask the client before answering\", \"turn these client meeting notes into a brief\". Does not write the offer \u2014 see `offre-commerciale` \u2014 and does not read a formal tender specification \u2014 see `analyse-cdc`."
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
The skill text is your method. Where its own output format and the HANDOFF below disagree, the HANDOFF wins: map your sections to these fields.
Stay strictly within the mission: do not produce later deliverables, do not answer the client's question yourself.
Write your full output to <trace file>, ending with:
## HANDOFF
### <field>        (one sub-section per field in "Transmits", nothing else)
## SUMMARY
<5 lines at most>
Reply to me with only the HANDOFF and SUMMARY blocks.
```

Launch the sub-agent with the step's model: Opus for step 1 (`cadrage`) — it alone reads the raw input, and what it misses is lost for every later step — and Sonnet for the others, `decision` included since the human decides right after it. For a high-stakes run, the human may ask for Opus on `decision` too. If the platform cannot write files, the sub-agent returns its full output instead; keep it, but pass on only the HANDOFF fields.

For step 1, also ask: "Before the HANDOFF block, add a `## CONTEXT SHEET` block — a ```json code block — with the fields client, objective, constraints, recipient, format, deadlines, named_solutions — facts from the request only, `not stated` when absent."

After each step, show the human the sub-agent's summary. Do not load the full output into your own context unless the human asks for it; the trace file holds it. You need only light reasoning to orchestrate: when you can choose your own model, a light one (Sonnet) is enough.

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
