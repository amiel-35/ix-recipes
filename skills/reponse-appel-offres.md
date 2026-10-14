---
id: reponse-appel-offres
label: Réponse à appel d'offres
version: 1.5.0
description_fr: "Conduit une réponse à appel d'offres de bout en bout — lecture du cahier des charges, questions à l'acheteur, go / no-go, stratégie de réponse, rédaction de l'offre, contrôle de conformité, mise en forme — chaque étape isolée, le dossier de consultation lu seulement par la première, une fiche de contexte validée par l'humain, et des pauses pour les réponses de l'acheteur et les décisions. Déclenche quand une consultation, un appel d'offres ou un cahier des charges reçu appelle une réponse complète. Déclenche sur \"on répond à cet appel d'offres\", \"prépare notre réponse à ce cahier des charges\", \"on y va ou pas sur cette consultation\", \"monte la réponse à cet AO\". Ne fait pas seulement l'analyse du cahier des charges — voir `analyse-cdc` — ni seulement l'offre — voir `offre-commerciale` ; pour une demande client informelle, voir `brief-client`."
description_en: "Runs a tender response end to end — reading the specification, questions to the buyer, go / no-go, response strategy, writing the offer, compliance check, formatting — each step isolated, the tender file read only by the first, a human-validated context sheet, and pauses for the buyer's answers and the decisions. Triggers when a consultation, call for tenders or received specification calls for a full response. Triggers on \"we're answering this call for tenders\", \"prepare our response to this specification\", \"should we bid on this consultation\", \"build the response to this tender\". Does not only analyse the specification — see `analyse-cdc` — nor only write the offer — see `offre-commerciale`; for an informal client request, see `brief-client`."
icon: ⇶
domain: sales
category: workflow
input_types:
- spec
- brief
- markdown
- reference
output_types:
- offre
- questions_acheteur
- decision_go_no_go
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
requires: [ix-recipes:analyse-cdc, ix-skills:questioning, ix-skills:decision, ix-skills:brief, ix-recipes:offre-commerciale, ix-skills:controle-qualite, ix-skills:deliver]
workflow:
  context_sheet: [buyer, objective, constraints, recipient, format, deadlines, named_solutions]
  steps:
    - id: analyse-cdc
      skill: ix-recipes:analyse-cdc
      mission: Read the tender file from the bidder's side — explicit and implicit requirements, evaluation criteria, submission rules, grey zones, blocking questions — and copy verbatim, item by item, every list the tender imposes (objectives, sequences and their sub-topics, exercises, deliverables, tools, documents to submit) and every sentence that prescribes what the response or the service must do (must, shall, is expected).
      receives: [brief]
      transmits: [requirements, imposed_items, evaluation_criteria, submission_rules, grey_zones, blocking_questions]
      verbatim: [imposed_items]     # copied word for word on purpose: exempt from the passage check, bounded in size
      produces_context_sheet: true
      pause: validate
      model: opus
    - id: questioning
      skill: ix-skills:questioning
      mission: Turn the grey zones and blocking questions into the questions to send the buyer within the consultation's question period, most blocking first. Do not question what the tender imposes (format, duration, the choice of a training, required deliverables) — the buyer decided it; ask only what is unclear or missing.
      receives: [context_sheet, analyse-cdc.grey_zones, analyse-cdc.blocking_questions]
      transmits: [buyer_questions]
      pause: answers
      model: sonnet
    - id: go-no-go
      skill: ix-skills:decision
      mission: "Recommend Go, Go with conditions or No-go against the requirements, the evaluation criteria and the buyer's answers, with visible trade-offs. Conditions are conditions to bid (eligibility, capacity, price risk, missing information), not choices of response design, which belong to the next step; without information on the bidder, say so instead of judging the fit."
      receives: [context_sheet, analyse-cdc.requirements, analyse-cdc.evaluation_criteria, answers]
      transmits: [go_no_go, conditions]
      pause: validate
      model: sonnet
    - id: strategie
      skill: ix-skills:brief
      mission: Write the response brief — angle, how each evaluation criterion and each imposed item will be met, proofs to provide, risks, what we will not propose. Imposed items are requirements to meet, never hypotheses or options to validate with the buyer.
      receives: [context_sheet, analyse-cdc.requirements, analyse-cdc.imposed_items, analyse-cdc.evaluation_criteria, answers, go-no-go.conditions]
      transmits: [response_brief]
      output_field: response_brief   # the step's whole output is this field
      pause: none
      model: sonnet
    - id: offre
      skill: ix-recipes:offre-commerciale
      mission: Write the content of the offer from the response brief, within the submission rules. Cover every imposed item explicitly and by its tender wording (place each objective and exercise in the schedule); imposed items are requirements, never hypotheses; never claim a placement or a coverage the text does not show. Leave unknown facts (prices, names, references, certifications) as visible placeholders.
      receives: [context_sheet, strategie.response_brief, analyse-cdc.imposed_items, analyse-cdc.submission_rules]
      transmits: [offer]
      output_field: offer   # the step's whole output is this field
      pause: none
      model: sonnet
    - id: conformite
      skill: ix-skills:controle-qualite
      mission: Check the offer against the tender's requirements, imposed items, evaluation criteria and submission rules — one line per requirement and per imposed item, met ones included, each with the exact passage of the offer. An imposed item missing from the offer is blocking (report it in the blocking section).
      receives: [offre.offer, analyse-cdc.requirements, analyse-cdc.imposed_items, analyse-cdc.evaluation_criteria, analyse-cdc.submission_rules]
      transmits: [compliance_verdicts]
      pause: validate
      model: sonnet
    - id: mise-en-forme
      skill: ix-skills:deliver
      mission: Format the offer for the buyer's evaluation committee, following the submission rules, without changing its substance. Remove internal annotations (hypothesis tags, legends, internal recaps) from the document handed over and list them in a separate note to the bidder; never delete a commitment or a sentence of substance, and never turn a condition into a commitment ("if they exist", "subject to" stay as written).
      receives: [context_sheet, offre.offer, analyse-cdc.submission_rules]
      transmits: [final_offer]
      output_field: final_offer   # the step's whole output is this field
      pause: none
      model: sonnet
---

# Role

You orchestrate the `reponse-appel-offres` recipe: a tender file goes in, a checked and formatted offer comes out, through seven steps. You run the steps; you never do a step's work yourself, and you never decide on substance — the steps do, and the human decides at the pauses, including whether to bid at all.

# Absolute rules

- **Isolation.** Run each step in a fresh sub-agent when the platform allows it (in Claude Code, the Agent tool). Give it only what its "Receives" column lists — never the conversation.
- **The tender file goes to step 1 only.** Later steps work from the requirements, criteria and rules step 1 extracted, and from the context sheet. The compliance step checks against those extracted requirements, not by rereading the file.
- **The context sheet replaces the tender file.** Step 1 produces it; the human validates it at the first pause; every later step that needs it receives it.
- **Handoff, not full outputs.** Each step ends its answer with a `## HANDOFF` block holding only the fields its "Transmits" column names.
- **No requalification.** A step never turns a hypothesis into a fact, nor drops a requirement, without saying so (`requalified: <reason>`).
- **The human decides go / no-go.** The step only recommends. On No-go, stop the run and give the trace.
- **Stop on a blocking signal.** If the compliance step finds a requirement unmet and blocking, stop before formatting and say which step to rerun.

# Context sheet

Produced at step 1, validated by the human. Facts from the tender file only, `not stated` when absent.

| Field | Content |
|---|---|
| `buyer` | the contracting organisation and the people or service named |
| `objective` | what the buyer wants to obtain, in their terms |
| `constraints` | budget ceiling, duration, location, imposed means, mandatory requirements |
| `recipient` | who evaluates the offer (committee, service), or `not stated` — never the end users or trainees |
| `format` | form of the offer: documents, templates, page limits, language |
| `deadlines` | question period, submission deadline, start date |
| `named_solutions` | means or methods the buyer mentions **without imposing them**, with their stated reason or "no reason given". Anything the tender imposes (deliverables, tools, sessions, format, the very choice of a training) is a requirement, listed in `imposed_items`, not a named solution |

# Steps

| # | Step | Skill | Mission | Receives | Transmits | Pause |
|---|---|---|---|---|---|---|
| 1 | analyse-cdc | `ix-recipes:analyse-cdc` | Read the tender file from the bidder's side | the tender file | requirements, imposed_items (verbatim lists), evaluation_criteria, submission_rules, grey_zones, blocking_questions **+ context sheet** | **validate** — the human checks the sheet and the reading |
| 2 | questioning | `ix-skills:questioning` | Questions to send the buyer, most blocking first | context sheet, grey_zones, blocking_questions | buyer_questions | **answers** — show the questions and stop; resume with the buyer's answers, or without them (points stay hypotheses) |
| 3 | go-no-go | `ix-skills:decision` | Recommend Go / Go with conditions / No-go | context sheet, requirements, evaluation_criteria, answers | go_no_go, conditions | **validate** — the human decides; No-go ends the run |
| 4 | strategie | `ix-skills:brief` | Response brief: angle, per-criterion and per-imposed-item answer, proofs, risks, exclusions | context sheet, requirements, imposed_items, evaluation_criteria, answers, conditions | response_brief | none |
| 5 | offre | `ix-recipes:offre-commerciale` | Content of the offer, every imposed item covered by its wording | context sheet, response_brief, imposed_items, submission_rules | offer | none |
| 6 | conformite | `ix-skills:controle-qualite` | One line per requirement and imposed item, with the passage; a missing imposed item blocks | offer, requirements, imposed_items, evaluation_criteria, submission_rules | compliance_verdicts | **validate** — the human reviews the verdicts; a blocking gap stops the run |
| 7 | mise-en-forme | `ix-skills:deliver` | Format for the evaluation committee, substance unchanged | context sheet, offer, submission_rules | final_offer | none |

Steps 2 and 4 reuse the pattern of `brief-client` (questions to a third party, then a brief), with the buyer instead of the client.

# Running a step

Send the sub-agent this message, filled in — and nothing else:

```
Use the skill `<skill>`.
Mission: <mission from the table>.
Context sheet:
<validated context sheet, or for step 1: none yet>
Input:
<only the fields listed in "Receives", each under its name; for step 1, the tender file verbatim>
The skill text is your method. Where its own output format and the HANDOFF below disagree, the HANDOFF wins: map your sections to these fields.
Stay strictly within the mission: do not produce later deliverables.
Write your full output to <trace file>, ending with:
## HANDOFF
### <field>        (one sub-section per field in "Transmits", nothing else)
## SUMMARY
<5 lines at most>
Reply to me with only the HANDOFF and SUMMARY blocks.
```

Launch the sub-agent with the step's model: Opus for step 1 (`analyse-cdc`) — it alone reads the raw input, and what it misses is lost for every later step — and Sonnet for the others, `go-no-go` included since the human decides right after it. For a high-stakes run, the human may ask for Opus on `go-no-go` too. If the platform cannot write files, the sub-agent returns its full output instead; keep it, but pass on only the HANDOFF fields.

For step 1, also ask: "Before the HANDOFF block, add a `## CONTEXT SHEET` block — a ```json code block — with the fields buyer, objective, constraints, recipient, format, deadlines, named_solutions — facts from the tender file only, `not stated` when absent." For step 3, give the three options explicitly: Go, Go with conditions, No-go. For step 6, the reference is the requirements, criteria and rules received — say so to the sub-agent.

After each step, show the human the sub-agent's summary. Do not load the full output into your own context unless the human asks for it; the trace file holds it. You need only light reasoning to orchestrate: when you can choose your own model, a light one (Sonnet) is enough.

# Pauses

- **After step 1 (validate).** Show the context sheet, the number of requirements and criteria found, and the main grey zones. Ask the human to correct anything before questions are prepared.
- **After step 2 (answers).** Show the buyer questions ready to send, most blocking first, and the question deadline from the context sheet. Stop. Resume with the buyer's answers, or with `answers: none — open points remain hypotheses` if the human says to go on.
- **After step 3 (validate).** Show the recommendation and its conditions. The human decides. On No-go, stop and output the trace.
- **After step 6 (validate).** Show unmet or partly met requirements first. If one is blocking, stop and say which step to rerun (usually `offre`, with the verdicts as extra input). Otherwise go on to formatting.

# Trace

If you can write files, save each full step output to `./parcours/appel-offres-<short-slug>/NN-<step>.md` and the context sheet to `00-context.md`. The tender file itself is only in step 1's input.

# Without sub-agents

If you cannot launch sub-agents, run the steps one after the other in the conversation. Open each step with a block containing only its inputs, and work from that block alone — not from the tender file above. Say at the top of the final output: "Steps run without isolation."

# Output

- The final offer (step 7 output, without its HANDOFF block), or the trace up to the stop if the run ended at No-go or on a blocking gap.
- A short trace: steps run, buyer answers received or not, go / no-go decision and its conditions, compliance verdicts still partial.

# Definition of done

- The tender file was read by step 1 only.
- The context sheet was validated before questions were prepared.
- The human took the go / no-go decision.
- Every requirement and every imposed item extracted at step 1 has a compliance line at step 6, met ones included.
- The trace says which steps ran and where the run stopped, if it did.
