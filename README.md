# ix-recipes

Domain recipes on top of [ix-skills](https://github.com/amiel-35/ix-skills): HR, legal, finance, procurement, product and tech deliverables, plus workflows that chain ix-skills atoms.

*[Version française](README-fr.md)*

## About

[ix-skills](https://github.com/amiel-35/ix-skills) holds the ingredients: atomic cognitive gestures (critique, decision, explorer, fact-check…) that apply to any content. ix-recipes holds the recipes:

- **domain skills**: they rely on domain knowledge that can be wrong or out of date (labour law, GDPR, HR practice, financial formulas, product methods), or they produce an artefact a profession defines (PRD, NDA, job description, TCO);
- **workflows**: chains of ix-skills atoms for a recurring job. The format is being designed; the first two candidates are listed below.

ix-recipes depends on ix-skills, never the other way round: a recipe may point to an ix-skills atom, an ix-skills atom never points to a recipe.

48 skills, moved from ix-skills on 2026-10-14 with their git history.

## Quick start

```bash
claude plugin marketplace add amiel-35/ix-recipes
claude plugin install ix-recipes@ix-recipes
```

Install [ix-skills](https://github.com/amiel-35/ix-skills) too: recipes and workflows refer to its atoms. Restart Claude Code. Skills are namespaced (`/ix-recipes:contract-review`), and Claude also picks them up from plain requests.

> Transition: until ix-skills 4.0.0, the same skills also ship inside ix-skills. If both plugins are installed, each of these skills appears twice.

**Cowork**: "Add from repository" with `amiel-35/ix-recipes`. **Codex CLI**: `bash scripts/install-codex.sh`.

## Corpus convention: the null output

A skill that has nothing to produce opens its response with « RAS — » followed by the reason, and stops. The token is literal and identical across ix-skills and ix-recipes, which makes it greppable and testable.

## Available skills

<details>
<summary><b>👥 HR</b> — 13 skills</summary>

| Skill | What it does |
|---|---|
| `contrat-emploi` | Analyzes or drafts an employment contract, job offer, or HR amendment, with watch points and the legal limit recalled |
| `entretien-professionnel` | Prepares the mandatory professional development interview (French labor code art. L6315-1) — 4-axis framework, exploratory questions, signable meeting record |
| `fiche-poste` | Produces a structured, publishable job description — mission, responsibilities, required/desirable competencies, success criteria |
| `grille-remuneration` | Structures a compensation grid by job family and level — salary ranges, positioning criteria, governance rules |
| `interview-guide-recruteur` | Prepares the recruiter-side interview guide for ONE round — STAR questions, recruiter annotations, scenarios, 1-4 scoring grid, graduated red flags, Go/No-go debrief sheet |
| `interview-loop-planner` | Designs the complete interview loop for a recruitment — number of rounds, competencies per round, consolidated scorecard, schedule, collective debrief protocol |
| `lettre-cadrage-disciplinaire` | Drafts a disciplinary letter (warning, formal notice, reprimand) from dated, documented facts, to be validated by a lawyer before sending |
| `offboarding-structure` | Structures an offboarding plan — knowledge and project handover, administrative checklist, exit interview, continuity risks |
| `onboarding-plan` | Builds a 30-60-90 day onboarding plan for a new employee — objectives, actions, meetings, deliverables and checkpoints per phase |
| `org-design-brief` | Formalizes an organizational target — current diagnosis, rationale, human risks, sequencing — before any announcement or implementation of a reorganization |
| `people-review` | Structures a collective talent review — positioning matrix, risks, succession plans, priority actions by category |
| `performance-review-helper` | Prepares the individual annual review — structured assessment (achievements, tension areas) and SMART objectives for next year |
| `plan-developpement-competences` | Builds an individual or collective competency development plan — concrete actions, quarterly schedule, progress indicators, budget and financing |

</details>

<details>
<summary><b>⚖️ Legal</b> — 7 skills</summary>

| Skill | What it does |
|---|---|
| `cgv-checker` | Surfaces unbalanced, unusual, or sensitive clauses in GTC/ToS from a given reading position (client, supplier, user) |
| `compliance-checklist` | Generates a multi-domain compliance checklist from a project or a context — legal, contractual, regulatory and sector obligations, each with a priority and a verification status |
| `conformite-rgpd` | Produces a GDPR compliance checklist from a technical spec or a description of personal-data processing — legal bases, DPIA, DPO, transfers outside the EU |
| `contract-review` | Analyzes a contract clause by clause — deviations from standard positions, GREEN/YELLOW/RED classification, priority redlines with fallback language |
| `contrat-fournisseur` | Analyzes or drafts a supplier contract from the buyer's side — SLA, penalties, termination, exclusivity, price, renewal — with renegotiation points ranked by impact |
| `legal-risk-flag` | Scans a legal or contractual document — contract, correspondence, any text — for priority red flags in one quick pass, with a graduated risk level (high/medium/low) and a recommended action |
| `nda-draft` | Drafts an NDA adapted to the context — parties, purpose, duration, territory — calibrated to the relationship type (contractor, partnership, employee, M&A discussion) |

</details>

<details>
<summary><b>💶 Finance & pricing</b> — 4 skills</summary>

| Skill | What it does |
|---|---|
| `budget-variance-analysis` | Analyzes budget-versus-actual variances line by line with probable causes, explicitly flagged hypotheses, and corrective actions |
| `business-case-draft` | Structures an investment decision into a costed business case — costs, expected benefits, risks, explicit financial hypotheses |
| `financial-narrative` | Transforms raw financial figures — results, budget, cash — into a clear, prioritized narrative for an executive or board audience |
| `strategie-prix` | Formulates a pricing recommendation linking perceived value, segmentation and candidate pricing models, with explicit trade-offs and owned critical assumptions |

</details>

<details>
<summary><b>🤝 Sales & procurement</b> — 6 skills</summary>

| Skill | What it does |
|---|---|
| `analyse-cdc` | Analyzes a received specification document from the respondent's side — explicit and implicit requirements, grey areas, contradictions, blocking questions before any commitment |
| `offre-commerciale` | Writes the content of a structured, argued client offer or tender response, ready to use before final formatting |
| `negotiation-brief` | Prepares a procurement negotiation position before the meeting — objective, useful facts, levers, possible concessions, BATNA, opening position, target and an owned red line |
| `rfp-draft` | Generates a structured request for proposal, context, scope, mandatory and desirable requirements, evaluation criteria, response conditions, from a procurement or business brief |
| `total-cost-analysis` | Structures a TCO, direct costs, hidden costs, hypotheses, risks, over a given horizon, distinguishing confirmed, estimated, and unquantified costs |
| `vendor-scorecard` | Builds a reusable vendor evaluation grid, weighted criteria, scoring scale, space for qualitative comments, the scoring tool, not the final decision |

</details>

<details>
<summary><b>🧭 Product & UX</b> — 8 skills</summary>

| Skill | What it does |
|---|---|
| `feature-spec` | Produces the complete functional spec of one feature, user stories, MoSCoW requirements, Given/When/Then acceptance criteria, success metrics |
| `journey-map` | Produces a user journey map, stages, actions, emotions, friction points, and opportunities, from the user's point of view, not the system's |
| `okr` | Reviews Objective/Key Result lines already written, or surfaces material to discuss from a vague brief |
| `persona` | Produces structured user personas from research data, interviews, or a product brief, distinguishing what is observed from what is assumed |
| `prd` | Produces a complete Product Requirements Document, problem, vision, target users, scope in and out, requirements, success metrics, the what and the why, never the how |
| `product-spec` | Turns a brief or an already-scoped need into an actionable specification, flows, screens, data model, edge cases, acceptance criteria, for a product, design, or engineering team |
| `reformulation-us` | Rewrites existing poorly-written user stories into clean, testable US with Given/When/Then acceptance criteria, staying faithful to the original intent |
| `tam-sam-som` | Estimates TAM, SAM, and SOM with top-down and bottom-up methods, explicit hypotheses, and owned reliability limits |

</details>

<details>
<summary><b>⚙️ Tech</b> — 5 skills</summary>

| Skill | What it does |
|---|---|
| `code-review` | Reviews code — diff, PR, files, or a pasted snippet — across four dimensions, security, performance, correctness, maintainability, with findings ranked critical vs suggestions and anchored to precise code references |
| `system-design` | Designs a system or technical architecture, components, data flows, API contracts, storage, with explicit trade-offs and owned scale hypotheses |
| `tech-debt` | Inventories technical debt, scores it on impact, risk and effort, and produces a remediation plan interleavable with feature work, every item justified by a business impact rather than a purely technical one |
| `ticket-triage` | Categorizes, prioritizes P1 through P4, and routes an incoming support ticket, with the information needed for immediate handling |
| `mockup` | Produces a standalone, presentable HTML mockup from a brief, spec, or visual references, a visual production deliverable, not a functional prototype |

</details>

<details>
<summary><b>📊 Data & market</b> — 3 skills</summary>

| Skill | What it does |
|---|---|
| `analyse-concurrentielle` | Builds a factual foundation on the competitive landscape — players, forces, differentiation, positioning |
| `metriques-saas` | Analyzes key SaaS metrics, CAC, LTV, NRR, churn, and produces a factual diagnosis of business model health, formulas and hypotheses included |
| `tableau-de-bord-kpi` | Defines and structures a full KPI dashboard — metric, unit, target, frequency, data source — from business objectives or context |

</details>

<details>
<summary><b>🔗 Upcoming workflows</b> — 2 skills</summary>

Still standalone skills, to be rewritten as chains of ix-skills atoms (`decision` → `deliver`; `vendor-scorecard` → `decision`).

| Skill | What it does |
|---|---|
| `note-strategique` | Produces a structured, argued strategic note that opens with the conclusion and makes trade-offs visible, for a decision-maker reader |
| `offer-comparison` | Compares already-normalized supplier offers on a weighted grid and closes with an argued recommendation, keeping fragile scores and non-comparable criteria visible |

</details>

## Repository layout

| Path | Role |
|---|---|
| `skills/` | Canonical source: one `.md` per skill + `.mystaffy.json` overrides |
| `dist/` | Plugin root, **committed**: `.claude-plugin/plugin.json` + `skills/<id>/SKILL.md` generated by `build.py` |
| `.claude-plugin/marketplace.json` | Marketplace manifest, points at `./dist` |
| `build.py` | Packaging (agentskills, cowork, mystaffy, ix-memory, codex), a copy of ix-skills' builder |

```bash
python3 build.py --validate                 # validate without writing
python3 build.py --target agentskills       # rebuild dist/skills/
claude plugin validate dist
```

## Credits

Several skills draw on public sources. They are listed in [THIRD_PARTY.md](THIRD_PARTY.md), with what was taken and under which licence.

## License

MIT, see [LICENSE](LICENSE).
