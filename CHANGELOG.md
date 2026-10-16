# Changelog

Notable changes to ix-recipes. Skills are versioned individually (semver in each skill's frontmatter); the plugin version lives in `dist/.claude-plugin/plugin.json`. Format inspired by [Keep a Changelog](https://keepachangelog.com).

## 2026-10-16 — plugin 2.12.0: the calculation check is specified and may re-read the source

### Recipes

- **Calculation check** (Amiel's decision 8 of 2026-10-16): the atom that recomputes every derived
  figure from the source values and reports the gaps is specified in
  [`docs/atome-verification-calcul.md`](docs/atome-verification-calcul.md). It belongs to ix-skills
  (`ix-skills:calc-check`), where it remains to be created. `fact-check` only checks that a figure is in
  the source.
- `ix-skills:calc-check` joins the closed list of the skills that may re-read the source
  (`VERIFICATION_SKILLS` in `scripts/parcours.py` and `build.py`). Until the atom exists, `requires`
  refuses it. The same change is to be carried over to ix-skills' copy of `build.py`.
- **Decision on a corpus** ([`docs/decision-corpus.md`](docs/decision-corpus.md)): separate the request
  (step 1 only, leak check) from the corpus (pieces a step consults when the recipe allows it). Decided,
  not coded: no code before the checks of its §8. Isolation tests recorded there: Claude refuses to read
  outside its step folder; Codex's read-only sandbox reads the whole disk (accepted, to be said in the page).

### Page

- **Page 1.1.1**: the designer is told only the checking skills the catalogue holds (`calc-check` is not
  announced before it exists).
- `suivi-parcours` 1.5.1 (its scripts).
- README: the install prompt names version 2.12.0.

## 2026-10-16 — plugin 2.11.0: domain skills rewritten after Anthropic's skill-writing guidance, merges, output format

- README: the install prompt names version 2.11.0.
- **Decisions** on the open questions of the 2026-10-16 review, recorded in `docs/revue-skills-metier.md`.
- **Merges**: `cgv-checker` is merged into `contrat-fournisseur` (2.0.0), which now reads supplier contracts, GTC / ToS
  and SaaS terms from a given position, with clause sets as annexes (`partials/clauses_cgv.md`,
  `clauses_contrat_fournisseur.md`, `clauses_saas_donnees.md`); `product-spec` is merged into `feature-spec` (2.0.0),
  which now covers screens, view states and the data model. `cgv-checker` and `product-spec` stay one version as
  hand-overs, so existing installs keep working.
- **Output format**: every rewritten skill gets a short default output skeleton (summary first, named table columns,
  facts / hypotheses / to-verify labels, actions with owner and date), because the bench showed form was the weak point.
- **Open reading lists**: every checklist now ends by checking what the document's subject calls for beyond the list
  (the bench showed a list makes models miss what they would see without it, e.g. the Data Act on SaaS terms).
- **Enriched**: `strategie-prix` 2.0.0 (pricing models, value metric, willingness to pay, break-even volume, pricing
  law; it prepares options and `decision` decides; category `research`), `mockup` 2.0.0 (fidelity levels, imposed
  brand guide, WCAG 2.2 AA baseline, French formats; adapted ideas from anthropics/skills `frontend-design`).
- `contrat-emploi` 1.3.0: labour law moved to `partials/droit_contrat_travail.md`; modes analyse, generation and
  revision defined. `people-review` 1.4.0: category `production`, no calibration session. `analyse-entretien` 1.2.0:
  annual and career-path interviews only.
- `tests/cas-skills/banc.py`: compares with no skill, across model and effort settings, with cost, form criteria
  and judges from several vendors (claude, codex, agy).

Same release, first part (developed as 2.9.0 on its branch, renumbered at merge):

- **Grid and analysis** (`docs/etat-de-l-art-skills.md`): Anthropic's skill-authoring guide, skill-creator and
  recent prompting guidance, compared with anthropics/knowledge-work-plugins (why its skills are longer, and
  when that length is knowledge or filler); one analysis line for each of the 47 domain skills; per-family
  rewrite sheets in `docs/fiches-reecriture/`.
- **46 domain skills rewritten** (minor version bump each): every rule carries its reason instead of a bare
  "do not"; domain knowledge the model would get wrong is added (formulas, default positions, French and EU
  law checked on Légifrance / EUR-Lex / CNIL and dated 2026-10-16, including 2026 changes); `.mystaffy.json`
  parameters are defined in the body; short examples where the form matters. Legal skills cite an article only
  when it is in their table or certain. `entretien-professionnel` is not rewritten here (its 2.0.1 came separately, in 2.10.1). Points that depend on an open question of the 2026-10-16 review are left as they were and listed.
- **New shared annexes** `partials/transverse_anti_biais.md` and `partials/transverse_debrief.md`: the text
  `interview-loop-planner` and `interview-guide-recruteur` used to copy inline (329 → 101 and 172 → 98 body lines).
- `contrat-fournisseur` no longer promises drafting (it analyses, buyer side); README aligned, as for
  `cgv-checker`, `compliance-checklist`, `lettre-cadrage-disciplinaire`, `offboarding-structure` and `org-design-brief`.
- `THIRD_PARTY.md`: the passages adapted from anthropics/knowledge-work-plugins (commit `33eeda1`), skill by skill.
- **Test cases** in `tests/cas-skills/` (one or more per skill) and a before/after bench, `tests/cas-skills/banc.py`,
  that plays each case several times per model and has each output graded blind.
## 2026-10-16 — plugin 2.10.1: entretien-professionnel follows law 2025-989

- `entretien-professionnel` 2.0.1: the professional interview becomes the *entretien de
  parcours professionnel* (law 2025-989 of 24 October 2025, Labor Code L6315-1 in force since
  31 December 2025): first year, every 4 years, 8-year review (7 years in some cases), who
  runs it and when (employer, line manager or management, during working hours), the 3,000 €
  top-up above 50 employees, sources with Légifrance links. Checked by an independent legal
  review against the texts in force: the 4- and 8-year periods counted from the last interview
  are the labour ministry's position (Q&A of 12 February 2026, question 2, Civil Code
  art. 2222), not the law's wording; below 50 employees damages require proof of harm
  (Cass. soc. 17 June 2026, 25-10.517).


## 2026-10-16 — plugin 2.10.0: a checking step may re-read the source (recipe format 2)

### Recipes

- **Recipe format 2** ([`docs/format-recette.md`](docs/format-recette.md) §1.10, §2ter): a step that checks
  may declare `reads_source: true` and then receives, besides its fields, the raw request exactly as
  the user gave it, to check the chain's output against it. Reserved to the checking skills
  (`ix-skills:fact-check`, `ix-skills:quality-check`, `ix-skills:controle-qualite`, a closed list);
  never step 1, never a producing step: `build.py`, the runner and the page refuse it with a plain
  message pointing to `verbatim`. `verbatim` fields stay the default.
- It is a format and not an optional field because a format-1 runner would ignore the key and run the
  check without the source, without saying so; at format 2 an older page refuses the recipe
  (« mettez la page à jour »). Format 1 recipes run unchanged; no recipe of the repository moves to
  format 2 (none uses it yet).
- Proof replayed on a real fact-check ([`docs/preuve-lecture-source/`](docs/preuve-lecture-source/README.md),
  2 Sonnet calls, $0.12): with an upstream analysis that miscopied a figure and dropped a line, the
  fact-check found 0 contradictions before and 4 after, and traced the error back to step 1.
- `concepteur-recette` 1.2.0 sets `reads_source` itself when it places a checking step after a
  producing one, and writes `format: 2` then.
- `build.py`: formats 1 and 2, and the `reads_source` checks. The same change is to be carried over to
  ix-skills' copy.

### Page

- **Page 1.1.0**: it reads format 2. The steps that re-read the request are shown on the cards
  (badge « Relit votre demande », « Votre demande » says who reads it), in the flowchart, in step
  details, on recipe lists and in a dossier's technical details. In the block builder, a checking skill
  dropped after another step comes ticked « Relit votre demande pour vérifier » (it can be unticked);
  writing the recipe then gives `format: 2`. The designer is told the rule and its proposals carry the
  field; a file written at `format: 1` with such a step is raised to 2; a missing setting is flagged as
  a departure from the proposal.
- Runner: `formats --json` adds `source_format`; `reads_source` per step in `recipes --json`,
  `status --json` and `plan --json`.
- `suivi-parcours` 1.5.0 (the page and its scripts).

## 2026-10-16 — plugin 2.9.0: the recipe format and the page get their own versions

### Recipes

- **Recipe format**: every recipe declares `format: 1` at the head of its `workflow` block
  ([`docs/format-recette.md`](docs/format-recette.md) §2bis: what the field means, when the format
  changes, how to move to format 2). `brief-client` 1.4.1 and `reponse-appel-offres` 1.6.1 declare it
  (no other change); `concepteur-recette` 1.1.1 writes it.
- A format the runner does not know, or a newer one, is refused with a plain message
  (« mettez la page à jour »). A recipe without the field is read as format 1, with a warning: every
  recipe written before it followed format 1's rules, and the absence will mean format 1 for good.
- Personal recipes created from the page get `format: 1` (blank model, blocks, copy of a supplied
  recipe, file written by the designer); an existing recipe of the recueil is never rewritten.
- `build.py`: `workflow.format` required, and a known one (1); an unknown or newer format stops the
  workflow checks with one error. The same change is to be carried over to ix-skills' copy.

### Page

- **Page 1.0.0**, the first numbered version of the tracking page (server, page and API), apart from
  the plugin's version: shown at the bottom of the page and at start-up, returned by `GET /api/version`
  (`{"version", "recipe_formats"}`) and under `page` in `/api/parcours` and `/api/recipes`.
- Creating a dossier with a personal recipe of a newer format answers 422 `recipe_refused` with the
  runner's message (it used to say « introuvable »); "My recipes" tells to update the page rather than
  to edit such a recipe.
- Runner: `parcours.py formats [--json]` lists the formats it plays; `recipes --json` gives `formats`
  and, per recipe, `format` and `warnings`; `recipe_format` in `state.json` and `status --json`.
- `suivi-parcours` 1.4.0 (the page and its scripts).

## 2026-10-15 — plugin 2.8.0: recipes shown as cards, built in blocks

- README: the install prompt names version 2.8.0.
- **Design in two stages**: the designer first returns a proposal (the chain of steps, as JSON
  shown step by step), which the user comments on per step or overall and sends back for
  revision; the recipe file is written only after "Validate the principle and write the recipe",
  and its departures from the validated proposal are flagged.
- **Recipes as standard flowcharts** (ISO 5807 shapes, top to bottom) wherever a recipe is shown;
  clicking a step shows its mission, inputs (their sources light up) and outputs, and in a proposal
  takes its comment. The Recipes page lists "Supplied recipes", "My recipes" and "Drafts"; a supplied
  recipe can be launched or copied ("Copy to modify", `recettes.py fork`) into a draft of one's own.
- **Cards and blocks**: recipes read as cards by default (the flowchart one click away), and are built
  like Scratch: a palette of the real catalogue, steps clicked or dragged into the chain, stops and
  optional steps dropped onto a step, inputs wired automatically (by hand in advanced settings);
  "Write the recipe" produces a valid file with no engine call (`recettes.py proposal`, `write-file`,
  `to-blocks`, `catalogue`).
- Designer: step 1 receives `brief` only (the designer is told so), and an unknown input says
  how to fix it (« replace it with brief »).
- `suivi-parcours` 1.3.0 (the page and its scripts).

## 2026-10-15 — plugin 2.7.0: your own recipes

- README: the install prompt names its version (2.7.0), updates an older install and
  reports the installed version first.
- **Personal recipes, outside the repository**, from the tracking page ("Recipes"): describe a
  recurring job; one fresh engine call plays `concepteur-recette` over the real catalogue (the
  current version of each installed plugin) and proposes a recipe, or says that one skill is
  enough ("Design a recipe anyway" asks again; or start from the blank model). Edit the file
  with a readable view of the steps and pauses; every save is checked with build.py's workflow
  rules (ported rule for rule, in French, compared with build.py by a test) plus: every skill in
  the catalogue, a free id. Test it on a real example in a test dossier kept apart, with the
  new free `simulation` engine by default (a real run only on request, after the plan and the
  cost ceiling). Validate it into the user's recueil, `~/.ix-recipes/recettes/<id>.md` (next to the
  `parcours` folder; inside the dossier folder when it has another name): it
  then shows in "New dossier" marked "Personal" and in `parcours.py recipes`, and runs like the
  others; an id used by the plugin or the catalogue is refused.
- **Propose to the repository**: a branch prepared in a separate working copy of a local clone
  (or of the repository, cloned once), `skills/<id>.md`, its `.mystaffy.json`, `dist/` rebuilt by
  build.py, a local commit and its diff shown; push and `gh pr create` only after the user
  confirms in the page. Missing git, build dependencies, git identity or write access are said
  plainly.
- `scripts/recettes.py` (new, standard library): `list`, `draft-new`, `design`, `show`, `save`,
  `check`, `template`, `promote`, `edit`, `personal`, `retire`, `delete-draft`, `essai-delete`,
  `contribute`. Bundled with the page in the plugin (`suivi-parcours` 1.2.0).
- `parcours.py`: a standard-library YAML reader (tested against pyyaml on every front matter of
  ix-recipes and ix-skills), used for personal recipes and as the fallback without pyyaml — the
  19 page tests that failed without pyyaml now pass; `recipe_sha256` / `recipe_origin` in the
  state, `recipe_current` in `status --json`; the `recettes` folder is never a dossier.
- Step ids and file names may hold underscores (`fiche_poste`).
- `build.py` unchanged.

## 2026-10-15 — plugin 2.6.0: a README you can try in one prompt, a hidden dossier folder

- README (FR and EN): it opens on a short description, a single prompt to paste into Claude
  Code that installs both plugins and opens the tracking page without a restart, and a sample
  client request to try the "Brief client" recipe; installation details, catalogue and
  contribution come after, for those who want them.
- The tracking page keeps its dossiers in `~/.ix-recipes/parcours` (hidden) instead of
  `~/Parcours`; an existing `~/Parcours` that holds dossiers stays in use until it is moved,
  and the page says so. `suivi-parcours` 1.1.1, `configuration-ix` 1.0.1.

## 2026-10-15 — plugin 2.5.0: Inflexion theme, many dossiers, setup

- Home: filter chips by recipe (with counts) once dossiers mix several recipes; the
  choice is remembered in the browser.
- `suivi-parcours` 1.1.0: a description that says plainly it starts a local page (an
  isolated Claude had taken "open the tracking page" for a claude.ai artifact); on a busy
  port it rebuilds the address of the running page from the folder's access key. The README
  recommends `/ix-recipes:suivi-parcours`, tested in an isolated Claude Code.
- The Inflexion theme ships with the page and is on by default (`themes/inflexion/`, bundled
  in the plugin; Archivo, Source Sans 3 and IBM Plex Mono under the SIL OFL 1.1, licences
  included); `--theme none` / `PARCOURS_THEME=none` for the neutral look.
- README: an install prompt to paste into Claude Code or Cowork, and a table of what gets
  deployed (plugins, tracking page, dossiers, theme). `configuration-ix` 1.0.0: checks the
  plugins (present, up to date, not duplicated), the page's prerequisites, the dossier
  folder, the theme and the optional engines; proposes each change, applies it once agreed.

- Many dossiers: what waits for you or runs is always shown; finished ones fold beyond
  the six most recent; a search field past 12 dossiers; `parcours.py archive` /
  `unarchive` / `archives` and the page's "Archive" and "Archived dossiers"; the list is
  cached by state.json date and size (300 dossiers listed in about 10 ms).

- `scripts/interface.py --theme <folder>` (or `PARCOURS_THEME`): a `theme.css` added after
  the page's styles, its fonts and images served under `/theme/`. The page stays neutral
  by default; a company's brand lives in its own folder, outside this public repository.

## 2026-10-15 — plugin 2.4.0: the tracking page becomes a product

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
  Dossiers in `~/Parcours` by default (`--parcours-dir`, `PARCOURS_DIR`), whatever the
  folder the page is launched from. README: the page is now the documented way to run a
  workflow outside a conversation.
- `scripts/parcours.py`: `recipes --json`, `new --title` / `new --json`, step `label`
  and `mission`, `title`, `recipe_label` and `max_budget_usd` in `status --json`,
  `output_document()`.
- Recipe format: optional French `label` per step, `context_labels` (the context sheet's
  headings for the reader) and `summary_fr` (one plain sentence for the "new dossier"
  screen), validated by `build.py` (both copies); `brief-client` 1.4.0 and
  `reponse-appel-offres` 1.6.0 carry them. The page holds no recipe-specific text any more:
  tested with a recipe written by an isolated Sonnet from the format alone, and by an
  invented recipe in the tests.
- Installable from the plugin alone: `suivi-parcours` 1.0.0 bundles the runner and the
  page (`scripts` field, copied by `build.py` into `dist/skills/suivi-parcours/scripts/`);
  each workflow recipe ships a `recipe.json` next to its SKILL.md; the bundled runner
  needs no `pyyaml` (tested with macOS's Python 3.9, `yaml` blocked). Ask Claude to
  "open the tracking page".
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
