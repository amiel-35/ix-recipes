# Changelog

Notable changes to ix-recipes. Skills are versioned individually (semver in each skill's frontmatter); the plugin version lives in `dist/.claude-plugin/plugin.json`. Format inspired by [Keep a Changelog](https://keepachangelog.com).

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
