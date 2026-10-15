# Changelog

Notable changes to ix-recipes. Skills are versioned individually (semver in each skill's frontmatter); the plugin version lives in `dist/.claude-plugin/plugin.json`. Format inspired by [Keep a Changelog](https://keepachangelog.com).

## Unreleased (branch `ihm-produit`) — the tracking page becomes a product

- `scripts/interface.html` rewritten: "Your dossiers" grouped by what they wait for,
  a "New dossier" screen (pick a recipe, paste or import the request, create and
  start), and a dossier screen with the steps on the left, one action card ("Validate
  and continue", "Send the answers and continue", "Redo the step", "Resume", "Stop"),
  and each step's output read as a formatted document (no HANDOFF / SUMMARY blocks,
  copy, download, print to PDF). The context sheet is a readable table, editable field
  by field when it is validated. Engines, per-step cost, transmitted fields, raw
  outputs, exact messages and the log sit behind a "Technical details" switch. Dark
  mode and phone layout.
- `scripts/interface.py`: `GET /api/recipes`, `POST /api/parcours` (create from the
  page, request on stdin), `GET …/document/<file>`; titles and step labels in the list.
- `scripts/parcours.py`: `recipes --json`, `new --title` / `new --json`, step `label`
  and `mission`, `title`, `recipe_label` and `max_budget_usd` in `status --json`,
  `output_document()`.
- Recipe format: optional French `label` per step, `context_labels` (the context sheet's
  headings for the reader) and `summary_fr` (one plain sentence for the "new dossier"
  screen), validated by `build.py` (both copies); `brief-client` 1.4.0 and
  `reponse-appel-offres` 1.6.0 carry them. The page holds no recipe-specific text any more:
  tested with a recipe written by an isolated Sonnet from the format alone, and by an
  invented recipe in the tests.
- Markdown renderer: line breaks kept, `http(s)` links (new tab, no referrer),
  strikethrough, task lists, ordered list start, HTML comments dropped; headings start
  at h2.

## 2026-10-15 — plugin 2.3.0: the runner, the tracking page, the recipe designer

### Added
- `scripts/parcours.py` (spec: `docs/executeur.md`): plays a recipe step by step,
  each step in a fresh call to Claude Code, Codex or Antigravity that receives only
  its inputs, isolated from the user's own configuration. State in
  `./parcours/<slug>/state.json`, the exact message and the full output of each step
  kept, pauses (`validate`, `answers`, `choose`), corrections (`rerun`, `retry`,
  `handoff --file`), a lock, cost per step. From step 2 on, any message or recorded
  field that carries a passage of the raw request is refused, naming the fragment
  and the remedy.
- `scripts/interface.py` + `interface.html` (spec: `docs/interface.md`): a local page
  (127.0.0.1, token in the URL fragment, Host check, CSP) to follow the runs, read
  the outputs, answer the pauses and launch the next step; it only calls
  `parcours.py`.
- `concepteur-recette` 1.1.0: designs a recipe from a recurring job, after checking
  that a single skill or a manual sequence is not enough (the usual conclusion).
- Recipe format: `verbatim` fields on step 1 (lists the source imposes, copied word
  for word, checked line by line, at most 85% of the source; what they quote may be
  re-quoted downstream), `output_field` (a step whose deliverable is a document
  passes its whole output on instead of a summary of it), and the context sheet
  definitions of the recipe body sent to step 1.

### Changed
- `reponse-appel-offres` 1.5.0, `analyse-cdc` 1.3.0: imposed items, evaluation
  criteria and submission rules extracted at step 1 and carried to the offer and the
  compliance check; imposed items are requirements, never hypotheses nor "named
  solutions"; the compliance check reports a missing imposed item as blocking; the
  formatting keeps every commitment and condition as written.
- `brief-client` 1.3.0: the final brief is the step's whole output.
- Blocking signal: only when a later step cannot do its job; reservations go in the
  output.

### Measured
Full tender response on a real specification, Claude engine: $0.86 for the first
run, $1.53 for the corrected one with its reruns. A drift judge counted 113 imposed
items: 90 verbatim in the final offer, 14 shortened, 9 under another label, none
missing; no invented fact (prices, names, references stay placeholders).

## 2026-10-14 — plugin 2.2.0: lean orchestration, a model per step

- `brief-client` 1.1.0, `reponse-appel-offres` 1.1.0: each sub-agent writes its
  full output to the trace file and returns only its HANDOFF block and a
  5-line summary, so the orchestrator no longer accumulates outputs (in the
  first test, the orchestrator's growing context made 78% of the cost). Each
  step names its model: **Opus for step 1**, the only one reading the raw input,
  **Sonnet for the others**, decisions included since the human decides right
  after them. Measured: tender step 1 went from $0.73 to $0.52 with a Sonnet
  orchestrator; in a blind comparison, the Opus scoping of a real meeting kept
  what later steps need (the existing specification as a constraint, the need
  separated from the training already named) where the Sonnet one lost it.
- `docs/format-recette.md`: `model` field per step and the lean-orchestrator rule;
  `build.py` validates `model`.

## 2026-10-14 — plugin 2.1.0: first workflow recipes

### Added — workflow format and two recipes

- `docs/format-recette.md`: the format of a workflow recipe — each step isolated
  (sub-agent in Claude Code), raw input to step 1 only, a human-validated
  context sheet for the rest, named handoff fields, pauses (`validate`,
  `answers`, `choose`), a trace in `./parcours/`. `build.py` checks the
  `workflow` block mechanically.
- `brief-client` 1.0.0: `cadrage` → `questioning` → client answers →
  [`explorer` → `decision`] → `brief`. Tested end to end in Claude Code on a
  real client meeting transcript: five isolated steps, three pauses, the raw
  transcript seen by step 1 only.
- `reponse-appel-offres` 1.0.0: `analyse-cdc` → buyer questions → go / no-go →
  response strategy → `offre-commerciale` → compliance check → formatting.
  Tested in Claude Code on a real tender specification up to the buyer
  questions; step 2 received no line of the specification.

## 2026-10-14 — plugin 2.0.0

### Removed (breaking)

- `code-review` and `contract-review`: condensed adaptations of Anthropic's
  knowledge-work-plugins, where the source is far richer (2,345 words against
  264 for contract review); Claude Code also ships a built-in `/code-review`.
  For a clause-by-clause contract review, use Anthropic's `legal` plugin; this
  repo keeps `legal-risk-flag`, `cgv-checker` and `contrat-fournisseur`.

### Added — third-party credits

`THIRD_PARTY.md` filled from a skill-by-skill provenance check:
anthropics/knowledge-work-plugins (Apache-2.0, licence copy in
`LICENSES/Apache-2.0.txt`) for `feature-spec`, `system-design`, `tech-debt`,
`ticket-triage`; wshobson/agents and davila7/claude-code-templates (MIT) for
six skills inspired by them. The four Apache-derived skills carry a
modification notice at the end of their body.

### Added — domain references for the HR recipes

The eight job-family competency annexes (`metier_tech`, `metier_commercial`,
`metier_finance`, `metier_rh`, `metier_juridique`, `metier_ops`,
`metier_marketing`, `metier_direction`) come back from the ix-memory project,
translated into English, in `partials/`. Ten HR recipes (eleven with `analyse-entretien`, below) declare them in a new
`references` frontmatter field; `build.py` copies them into
`dist/skills/<id>/references/`, and each skill reads only the file of the job
family at hand instead of carrying eight empty "Domain calibration" lines.
Tested headless: a senior data engineer job description read
`metier_tech.md` and nothing else. Minor bumps: `entretien-professionnel`,
`grille-remuneration`, `offboarding-structure`, `onboarding-plan`,
`plan-developpement-competences`, `people-review`, `interview-loop-planner`
1.2.0; `fiche-poste`, `performance-review-helper`, `interview-guide-recruteur`
1.3.0. The Codex installer now copies `references/` too.

### Added — `analyse-entretien` 1.0.0

Migrated from ix-memory, where it never reached ix-skills: reads a filled
interview grid or raw notes and extracts strengths, development areas, HR
risk signals and expressed needs, separating what was said from what is
inferred, with the job-family references. 47 skills.

### Fixed

- `conformite-rgpd` 1.3.0: the art. 5 principles were mis-stated
  (lawfulness, fairness and transparency split in three) and accountability
  (art. 5(2)) was missing; processors (art. 28), breaches (arts. 33–34),
  rights (arts. 12–22), record exemption limits (art. 30(5)), DPO cases
  (art. 37(1)) and transfers (arts. 44–49) added, every obligation tied to its
  article, checked against the text in force. Reviewed twice independently
  (a first legal review, then a deep adversarial one): no error of law, and
  the gaps a team without a lawyer would pay for are now covered — the
  organisation's role (controller or processor) and who owns which
  obligation, the record required in practice whatever the headcount,
  art. 46 LIL on offence data, the art. 28(3) contract content, art. 34
  high-risk communication and its exceptions, US transfers limited to
  Data Privacy Framework recipients, ePrivacy and electronic marketing
  flagged, and pending omnibus proposals never applied as if in force.

### Changed

- Pointers to the removed skills dropped: `cgv-checker` 1.2.1,
  `compliance-checklist` 1.1.1, `contrat-fournisseur` 1.2.1,
  `legal-risk-flag` 1.2.1, `nda-draft` 1.1.1, `system-design` 1.1.1,
  `tech-debt` 1.2.1.
- `feature-spec` 1.1.1, `ticket-triage` 1.1.2: modification notice added.
- README: 47 skills.

## 2026-10-14 — plugin 1.0.0

### Added — repository created from ix-skills

48 skills moved from [ix-skills](https://github.com/amiel-35/ix-skills) (commit `9229d48`) with their git history: HR, legal, finance, sales and procurement, product, tech, data. `note-strategique` and `offer-comparison` come along as standalone skills, to be rewritten as workflows chaining ix-skills atoms.

### Changed

- `financial-narrative` 1.1.1: no longer points to `data-storytelling`, which is not carried over.
- `ticket-triage` 1.1.1: no longer points to `retrospective`, which is not carried over.
