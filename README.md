<p align="center">
  <img src="docs/assets/banner.svg" alt="ix-recipes: domain recipes on top of ix-skills" width="100%">
</p>

<p align="center">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/amiel-35/ix-recipes?color=7f9a96"></a>
  <img alt="Plugin version" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Famiel-35%2Fix-recipes%2Fmain%2Fdist%2F.claude-plugin%2Fplugin.json&query=%24.version&label=plugin&color=7fc8bd">
  <img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-plugin-D97757">
  <img alt="Skills" src="https://img.shields.io/badge/skills-49-3d6b73">
  <a href="https://github.com/amiel-35/ix-skills"><img alt="requires ix-skills" src="https://img.shields.io/badge/requires-ix--skills-7fc8bd"></a>
  <img alt="Platforms" src="https://img.shields.io/badge/also-Codex%20%C2%B7%20GPT%20%C2%B7%20Gemini%20%C2%B7%20mystaffy-56707a">
</p>

<p align="center">
  <a href="#try-it-in-two-minutes"><b>Try it</b></a> ·
  <a href="#available-skills"><b>Catalog</b></a> ·
  <a href="#workflows"><b>Workflows</b></a> ·
  <a href="#contributing"><b>Contributing</b></a> ·
  <a href="README-fr.md"><b>Français</b></a>
</p>

---

<details>
<summary><b>Table of contents</b></summary>

- [Try it in two minutes](#try-it-in-two-minutes)
- [About](#about)
- [Detailed installation](#detailed-installation)
- [Corpus convention — the null output](#corpus-convention--the-null-output)
- [Available skills](#available-skills)
- [Workflows](#workflows)
- [Installation](#installation)
- [Structure](#structure)
- [Building](#building)
- [Sibling projects](#sibling-projects)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)

</details>

## Try it in two minutes

ix-recipes does the groundwork of consulting, HR, legal, finance and product jobs with Claude: answering a call for tenders, turning a vague client request into a brief, writing a job description, reviewing a contract… The bigger jobs are **recipes**: a series of steps you follow in a page on your computer, which stops whenever your judgement is needed.

**1. Paste this into Claude Code**, on your computer. That's all: Claude installs and opens the page. Prompt for version **2.10.0**:

```text
Install ix-recipes (version 2.10.0 or later) on this computer and open its tracking page so I can try it
(https://github.com/amiel-35/ix-recipes). Do everything yourself, without asking me to restart:
1. Add the amiel-35/plugins marketplace (if that fails for lack of a GitHub SSH key, use
   https://github.com/amiel-35/plugins.git), then install ix-skills@amiel-35 and
   ix-recipes@amiel-35. If they are already installed, update them; if they come from another
   marketplace, keep that one and create no duplicate. Check the installed ix-recipes version:
   if it is older than 2.10.0, update the marketplace and the plugin.
2. Check python3 (3.9 or later); if it is missing, tell me what to install and stop.
3. Start, in the background, the script skills/suivi-parcours/scripts/interface.py of the
   installed ix-recipes plugin (under ~/.claude/plugins/cache/, the latest version); it opens
   the page in the browser and prints its address.
Change nothing else without asking me. Answer in four lines: the installed ix-recipes version,
the page's address, where my dossiers are kept, how to stop the page.
```

**2. Try it.** In the page, pick the "Brief client" recipe, paste a client request, for example this one, and run:

```text
Hello, we'd like to redo our website: it looks dated and we get no quote requests online.
Budget to be discussed, ideally ready for the trade fair in March. Could you send us a
proposal? — Claire, sales director at a 40-person industrial joinery
```

Each step takes one to two minutes, and the page stops to show you the context sheet, then the questions to ask the client.

**Good to know.** You need Claude Code installed and signed in, and Python 3.9 or later (already there on macOS); not Cowork, since the page runs on your computer. Each step uses your Claude subscription or API credit: a full tender response cost $1 to $2 in our tests. Afterwards, in any Claude Code conversation, `/ix-recipes:suivi-parcours` reopens the page, and the skills trigger from an ordinary request ("write the job description for a senior product manager").

**Remove everything.** Trying it is installing it: everything comes off with this second prompt, also pasted into Claude Code. Nothing is deleted for good, and your dossiers go only with your agreement.

```text
Cleanly uninstall ix-recipes from this computer (https://github.com/amiel-35/ix-recipes).
1. Stop the tracking page if it runs (a python3 running suivi-parcours/scripts/interface.py).
2. Uninstall the ix-recipes then ix-skills plugins, whatever their marketplace. Before
   ix-skills, check that no other installed plugin uses it (ghost-council, for example); if
   one does, ask me whether to keep it.
3. Remove their marketplace (amiel-35, ix-recipes or ix-skills) only if no installed plugin
   comes from it any more, then move their copies in ~/.claude/plugins/cache/ to the trash.
4. My dossiers and recipes (~/.ix-recipes, and ~/Parcours if it exists): tell me how many there
   are and ask me whether to keep them or move them to the trash.
Delete nothing for good. End with what was removed and what remains.
```

---

*Everything below is for going further: what the repository holds, detailed installation, the full catalogue, other platforms and contributing.*

## About

Domain recipes on top of [ix-skills](https://github.com/amiel-35/ix-skills) — portable across Claude, GPT, Gemini, and mystaffy.

52 skills in 9 families, including 2 workflows, a workflow designer, the tracking page and its setup. ix-skills provides the ingredients: atomic cognitive moves (critique, decision, explorer, fact-check…) that apply to any content. ix-recipes provides the recipes:

- **domain skills** — they rely on domain knowledge that can be wrong or go stale (labour law, GDPR, HR practice, financial formulas, product methods), or produce an artefact a profession defines (PRD, NDA, job description, TCO);
- **workflows** — chains of ix-skills atoms for a recurring job, a designer for new ones, and a runner with a local tracking page (see [Workflows](#workflows)).

ix-recipes depends on ix-skills, never the other way round: a recipe may point to an atom, an atom never points to a recipe. The skills come from ix-skills, moved on 2026-10-14 with their git history.

---

## Detailed installation

### What gets deployed

| Piece | Role | Where it runs |
|---|---|---|
| **ix-skills** plugin | the cognitive atoms (scoping, decision, critique…) | wherever skills load (Claude Code, Cowork, Codex, Antigravity) |
| **ix-recipes** plugin | domain skills and the workflow recipes chaining the atoms | same |
| **tracking page** (`suivi-parcours`) | creates and follows a recipe's dossiers, step by step | Claude Code on your computer: a local server, Python 3.9+, the signed-in Claude CLI — not Cowork |
| **dossiers** | one folder per request handled: outputs, traces, state | `~/.ix-recipes/parcours`, hidden (or `$PARCOURS_DIR`); finished ones are archived in `.archives/` |
| **your recipes** | the workflow recipes you design in the page, kept outside the repository; drafts and their test dossiers alongside | `~/.ix-recipes/recettes`, next to the dossiers (see [Your own recipes](#your-own-recipes)) |
| **theme** | the page's look: the Inflexion brand by default (shipped with the page, fonts under the OFL), `none` for the neutral look, or another brand's folder | `$PARCOURS_THEME` or `--theme` |

For a team: everyone pastes the prompt from [Try it in two minutes](#try-it-in-two-minutes); another brand is shared as a theme folder (a `theme.css` and its fonts), turned on by `configuration-ix`.

### Command by command

Install both plugins in Claude Code — ix-recipes builds on ix-skills atoms:

```bash
claude plugin marketplace add amiel-35/ix-recipes
claude plugin install ix-recipes@ix-recipes
claude plugin marketplace add amiel-35/ix-skills
claude plugin install ix-skills@ix-skills
```

Or from the [amiel-35 catalogue](https://github.com/amiel-35/plugins), one marketplace for ix-skills, ix-recipes and ghost-council (install each plugin from one marketplace only):

```bash
claude plugin marketplace add amiel-35/plugins
claude plugin install ix-recipes@amiel-35
claude plugin install ix-skills@amiel-35
```

Restart Claude Code. Skills are namespaced (`fiche-poste` becomes `/ix-recipes:fiche-poste`), and Claude also picks them up from plain requests:

- *"Review this supplier contract before I sign."*
- *"Draft the job description for a senior product manager."*
- *"Estimate TAM, SAM and SOM for this market."*

Other platforms (Cowork, Codex CLI, Antigravity CLI, mystaffy, GPT, Gemini): see [Installation](#installation).

---

## Corpus convention — the null output

A skill that has nothing to produce opens its response with « RAS — » followed by the reason, and stops. The token is literal and identical across ix-skills and ix-recipes: that is what makes it greppable and testable.

---

## Available skills

Click a family to expand it.

<details>
<summary><b>👥 HR & People</b> — 14 skills</summary>

Tools for the full employee lifecycle — recruiting, onboarding, development, assessment, organization design, and employment law. French labor law context is embedded where relevant.

---

#### `fiche-poste` — Structured job description

**What it does:** Produces a structured, publishable job description from an HR brief or recruitment need. Distinguishes required from desirable criteria, identifies grey areas, and produces output that feeds the downstream recruiting workflow.

**Use when:** Starting a recruitment process. Output feeds `interview-loop-planner`.

---

#### `interview-loop-planner` — Full interview process design

**What it does:** Designs the complete interview loop for a recruitment — number of rounds, competencies per round, consolidated scorecard, and schedule. Produces round briefs that directly feed `interview-guide-recruteur`.

**Use when:** Before starting interviews for a significant hire. Ensures each round assesses different dimensions.

> Pipeline: `fiche-poste` → `interview-loop-planner` → `interview-guide-recruteur` (one per round).

---

#### `interview-guide-recruteur` — Recruiter-side interview guide

**What it does:** Produces a full recruiter or manager interview guide with STAR-structured questions, evaluation annotations, scenario-based questions, a weighted 1–4 scoring grid, graduated red flags, and a Go/No-go debrief sheet.

**Use when:** For a specific interview round. Best used downstream of `interview-loop-planner`, which defines the rounds and competencies.

---

#### `onboarding-plan` — 30-60-90 day integration plan

**What it does:** Builds a structured integration plan covering the first 30, 60, and 90 days — objectives, key relationships, deliverables, and success criteria per phase.

**Use when:** Before a new hire starts, to give both manager and employee a shared roadmap.

---

#### `entretien-professionnel` — Mandatory professional development interview

**What it does:** Prepares a mandatory professional development interview (French Labor Code, art. L6315-1) — required every 2 years for all employees. Produces a framework, questions, and a meeting record template compliant with legal requirements.

**What it doesn't do:** Not the same as an annual performance review. This is a legally required career development conversation, not a performance assessment.

**Use when:** Every 2 years per employee, or after specific events (return from parental leave, sick leave…) as required by French law.

---

#### `analyse-entretien` — The signals of an interview already held

**What it does:** Reads a filled interview grid or raw notes and extracts the signals: strengths, development areas, HR risks (disengagement, intention to leave, overload, conflict), expressed needs. Separates what was said from what is inferred, and reads the signals at the role's level using the job-family reference.

**What it doesn't do:** Does not prepare an upcoming interview (`performance-review-helper`, `entretien-professionnel`) and passes no judgement on the person.

**Use when:** After an annual review or a career-path interview, to turn it into an actionable summary for the manager or HR. Not for recruitment interview notes.

---

#### `performance-review-helper` — Annual review preparation

**What it does:** Prepares an annual performance review with a structured assessment of the past year and SMART objectives for the next. Supports both manager prep and employee self-assessment.

**What it doesn't do:** Not the mandatory professional development interview (`entretien-professionnel`). This is about performance — results, objectives, compensation context.

**Use when:** Ahead of annual review cycles.

---

#### `people-review` — Collective talent review

**What it does:** Structures a collective talent review with a positioning matrix (performance × potential), succession planning, retention and flight risk assessment, and priority actions per profile.

**Use when:** Annual or bi-annual talent reviews, before an organizational change, or when preparing a workforce plan.

---

#### `plan-developpement-competences` — Skills development plan

**What it does:** Builds an individual or collective skills development plan with training actions, schedule, success indicators, and budget. Links identified gaps to concrete development paths.

**Use when:** After a performance review, a people review, or a skills gap assessment.

---

#### `grille-remuneration` — Compensation grid

**What it does:** Structures a compensation grid by job family and seniority level — salary ranges, positioning criteria (internal equity, market benchmarks), and governance rules (who can offer what).

**Use when:** When scaling a team and needing consistent, defensible compensation decisions across hires and existing employees.

---

#### `contrat-emploi` — Employment contract

**What it does:** Three modes: analyse a contract received, draft a contract, offer letter or amendment, revise an existing draft clause by clause. Relies on French labour law as an annex (`droit_contrat_travail`: trial period, fixed-term contracts, day-rate, part-time, non-compete, mobility, offer or promise) and corrects requests that break it, saying why.

**What it doesn't do:** Does not provide legal advice. Requires validation by a labor lawyer before use.

**Use when:** Drafting a new contract, reviewing one received, correcting a draft, or preparing an amendment.

#### `lettre-cadrage-disciplinaire` — Disciplinary framing letter

**What it does:** Drafts a disciplinary letter (warning, reprimand, suspension…) from dated facts, after setting the sanction aimed at, the procedure it triggers and its deadlines. Calibrated to the sanction aimed at. Also covers the formal notice for job abandonment, which is not a sanction.

**What it doesn't do:** Does not draft the summons to the prior interview (it says when one is needed and what it contains). Must be validated by a labor lawyer before sending: under French law any letter that reproaches a fault is in principle a sanction, and the same facts cannot be sanctioned again.

**Use when:** Specific, dated misconduct calls for a sanction, before anything is sent to the employee.

---

#### `offboarding-structure` — Departure plan with continuity

**What it does:** Structures an offboarding plan covering knowledge handover, admin checklist, exit interview framework, and continuity risk mapping.

**Use when:** As soon as a departure is decided, whatever its form (resignation, mutual termination, dismissal, end of fixed-term contract). The earlier it starts, the better the knowledge transfer.

---

#### `org-design-brief` — Organizational redesign target

**What it does:** Formalizes an organizational target with a current state diagnosis, design rationale, human risks, and sequencing — before any announcement or implementation. Surfaces what the new structure solves, what new risks it creates, and how to phase the transition.

**Use when:** Before consulting the works council (CSE) and before announcing a reorganization. Also useful as pre-work before engaging a management team in the design.

</details>

<details>
<summary><b>⚖️ Legal & Contracts</b> — 6 skills</summary>

Pre-legal tools — all require professional validation before use. They orient reviews, surface risks, and produce drafts. None replace a lawyer.

---

#### `legal-risk-flag` — Fast red flag scan

**What it does:** Quickly reads a legal or contractual document and extracts priority risk signals with graduated severity levels (high / medium / low). Designed for speed — a flash assessment before deciding whether a deeper review is needed.

**What it doesn't do:** Does not perform a full analysis. Flags, does not conclude. Never replace a lawyer.

**Use when:** You receive a document and need to decide in minutes whether to escalate or which clauses to focus on.


---

#### `cgv-checker` — Merged into `contrat-fournisseur`

**Since 2.0.0:** hands over to `contrat-fournisseur`, position "client" or "supplier" and document type "GTC / ToS". The id stays for one version so existing installs keep working.

#### `conformite-rgpd` — GDPR compliance checklist

**What it does:** Produces a GDPR compliance checklist from a technical specification, product description, or data processing document. Distinguishes observed processing, inferred processing, and obligations to confirm.

**What it doesn't do:** Does not replace a DPO or qualified legal professional. Requires expert validation before operational use.

**Use when:** Before launching a product or feature that processes personal data. A structured first-pass self-assessment before the DPO review.

---

#### `compliance-checklist` — Legal compliance checklist

**What it does:** Generates a compliance checklist covering legal, contractual, and regulatory obligations — consumer, digital, accessibility, AI, cybersecurity, invoicing, sector-specific regulation — from a project context or document, each obligation with its application date and size exemption. GDPR is handed to `conformite-rgpd`.

**What it doesn't do:** Does not replace professional legal or regulatory advice. Always requires expert validation before operational use.

**Use when:** Before any product launch, contractualization, or operational change with legal implications. A structured pre-validation to orient the conversation with a lawyer, not replace it.

---

#### `nda-draft` — NDA draft adapted to context

**What it does:** Generates a confidentiality agreement draft adapted to the context — type of parties, subject of exchanges, duration. Produces a document ready for legal review, not for immediate signing.

**What it doesn't do:** Does not provide legal advice. Always requires lawyer validation before signing.

**Use when:** You need a starting point for NDA negotiations and don't want to start from a generic template.

---

#### `contrat-fournisseur` — Reading contracts and T&Cs

**What it does:** Reads a supplier or service contract, general terms (sales or use) or SaaS terms of service from a given position (client or buyer, supplier publishing its terms, user), under French law. Qualifies the parties first, then flags unbalanced, unfair or missing clauses ranked by priority, each with a proposed rewording and a fallback position. Reads the clause set of the document type as an annex (`clauses_cgv`, `clauses_contrat_fournisseur`, `clauses_saas_donnees`) and checks what the subject calls for beyond it (data, portability, sector). Absorbs `cgv-checker` since 2.0.0.

**What it doesn't do:** Does not draft a contract. Does not replace legal advice.

**Use when:** Before signing or accepting terms, before a negotiation, or to review your own T&Cs before publishing them.

</details>

<details>
<summary><b>💶 Finance & Pricing</b> — 4 skills</summary>

Quantify, explain and defend a money decision — budget variances, business case, financial narrative, pricing. Financial assumptions are always explicit.

---

#### `budget-variance-analysis` — Budget vs. actual diagnosis

**What it does:** Analyzes gaps between budget and actual figures. Identifies significant variances, qualifies them by nature (volume, price, mix, timing, operational), and produces corrective hypotheses and watch points.

**What it doesn't do:** Does not invent causes or figures. Does not make management decisions — produces a factual diagnosis.

**Use when:** Monthly or quarterly budget review, P&L analysis, or when you need to explain performance to a board or controller.

---

#### `business-case-draft` — Investment decision structure

**What it does:** Structures an investment decision with explicit costs, expected benefits, risk scenarios, and financial hypotheses. Distinguishes certain costs from estimated costs. Clearly marks what is a hypothesis vs a fact. If financial data is too fragile, says so and suggests `note-strategique` as an alternative.

**What it doesn't do:** Does not invent figures.

**Use when:** You have numbers to work with and need to frame a buy/build/invest decision. If you don't have numbers, use `note-strategique` instead.

---

#### `financial-narrative` — Numbers → executive story

**What it does:** Transforms raw financial figures (P&L, KPIs, reporting) into a clear, message-first narrative for an executive or board audience. Starts with key messages, contextualizes figures, connects variations to explanatory factors.

**What it doesn't do:** Does not invent numbers or trends. Does not reproduce the raw data. Does not distort figures to tell a better story.

**Use when:** Board presentations, investor updates, quarterly reviews — any time numbers need to be communicated to an audience that needs the "so what" before the detail.

---

#### `strategie-prix` — Pricing options and decision criteria

**What it does:** Prepares a pricing decision: links perceived value, segments and value metric; compares pricing models (subscription, usage, tiers, freemium…) with when each works; proposes ways to measure willingness to pay; computes the break-even volume of a price change; recalls French pricing law. It informs and suggests a lean without deciding: `decision` (ix-skills) decides next.

**What it doesn't do:** Does not set the price list and does not choose for the user.

**Use when:** Launch, repositioning, a move to another pricing model, or competitive pricing pressure.

</details>

<details>
<summary><b>🤝 Sales & Procurement</b> — 6 skills</summary>

Both sides of a tender: answering a specification and writing an offer, or running a call for tenders, comparing costs and scoring vendors.

---

#### `analyse-cdc` — Specification document analysis

**What it does:** Analyzes a received specification document (CDC) from the respondent's perspective. Surfaces explicit requirements, implicit requirements, grey areas, contradictions, and the blocking questions to ask before committing to a response.

**What it doesn't do:** Does not summarize the spec — it critiques it. Does not produce a response plan.

**Use when:** You receive a spec, RFP, or requirements document and need to understand what's really being asked before engaging. Output feeds a response strategy or clarification meeting.

---

#### `offre-commerciale` — Client offer content

**What it does:** Produces the structured content of a client offer — context understanding, proposed solution, value argument, pricing logic, and next steps. Focus is on content and argument, not final formatting.

**What it doesn't do:** Does not format the final document (use `deliver` for that). Does not negotiate.

**Use when:** Responding to an inbound request, after a discovery call, or when you need to structure a proposal before putting it into a deck or document.

---

#### `negotiation-brief` — Structured position before a negotiation

**What it does:** Prepares a complete negotiation position — objectives, non-negotiables, tradeable points, BATNA (best alternative if no agreement), and concession logic. Designed for preparation, not to hand to the other party.

**What it doesn't do:** Not a negotiation script. Not a template for the other party.

**Use when:** Before any high-stakes procurement negotiation — supplier, vendor, subcontractor. The clearer the position going in, the better the outcome.

---

#### `rfp-draft` — Request for proposal

**What it does:** Generates a structured request for proposal — context, scope, requirements, evaluation criteria, expected deliverables, and timeline.

**Use when:** You are the buyer and need to solicit structured offers from multiple vendors. Output feeds `offer-comparison` and `vendor-scorecard`.

---

#### `total-cost-analysis` — Full lifecycle cost (TCO)

**What it does:** Structures a Total Cost of Ownership analysis covering direct costs, hidden costs (implementation, training, integration, migration, exit), and financial risks over a given horizon. Distinguishes confirmed costs, estimated costs, and unquantified risks.

**What it doesn't do:** Does not look at the sticker price alone. Does not invent figures without marking them as hypotheses.

**Use when:** Before any significant purchase or vendor decision where the visible price doesn't capture the full economic impact. Pairs with `offer-comparison` and `vendor-scorecard`.

---

#### `vendor-scorecard` — Reusable vendor evaluation grid

**What it does:** Builds a weighted vendor scorecard from a procurement context — criteria, weightings, scoring scale, qualitative comment fields. Produces the scoring **tool**, not the decision.

**What it doesn't do:** Does not score vendors (that's `offer-comparison`). Does not invent weightings without justifying them.

**Use when:** Before a consultation process begins, to align stakeholders on evaluation criteria. Reusable for future consultations of the same type.

</details>

<details>
<summary><b>🧭 Product & UX</b> — 8 skills</summary>

From a scoped need to the document a product team expects — PRD, specs, user stories, personas, journeys, OKRs, market sizing. Upstream scoping (`cadrage`, `brief`, `analysis`) stays in ix-skills.

---

#### `prd` — Complete Product Requirements Document

**What it does:** Produces a full PRD — context, problem statement, goals, functional and non-functional requirements, out-of-scope items, success metrics, and open questions.

**Use when:** You need a comprehensive product document to align the team, communicate with engineering, or frame a significant investment.

---

#### `feature-spec` — Functional specification

**What it does:** Produces the spec of a feature or a screen: problem, scope and non-goals, user stories, MoSCoW requirements, acceptance criteria with a negative case, view states and content edge cases, data model, metrics with threshold and date. Splits into companion documents when the spec grows. Absorbs `product-spec` since 2.0.0.

**Use when:** A feature is approved and needs to be specified for engineering. More granular than a PRD.

> Hierarchy: `brief` → `prd` (the what and the why) → `feature-spec` (the how).

#### `product-spec` — Merged into `feature-spec`

**Since 2.0.0:** hands over to `feature-spec`, which also covers screens, flows, view states and the data model. The id stays for one version for existing installs.

#### `reformulation-us` — Rewrite poorly-written user stories

**What it does:** Rewrites existing user stories that are vague, developer-centric, or untestable into clean, testable user stories with proper structure and explicit acceptance criteria.

**Use when:** In backlog refinement, when stories are being pulled into a sprint but aren't ready, or after a discovery phase where stories were written informally.

---

#### `persona` — Structured user personas

**What it does:** Produces structured user personas from research data or a product brief — goals, frustrations, behaviors, context, and decision triggers. Designed to be actionable for product decisions, not just decorative.

**Use when:** At the start of a product initiative, or when the team has diverging assumptions about who they're building for.

---

#### `journey-map` — User journey with friction and opportunities

**What it does:** Produces a user journey map covering stages, actions, emotions, friction points, and improvement opportunities. Structured around the user's perspective, not the product's features.

**Use when:** Before redesigning an experience, identifying where to invest in UX improvement, or aligning a cross-functional team on how users actually experience the product.

---

#### `okr` — Review O/KR lines, or surface material to discuss

**What it does:** Two distinct modes. *Template*: reviews Objective/Key Result lines already written, line by line — conformity to the formula (O = action verb + what + intended impact; KR = measurement verb + what + from X to Y + deadline), task disguised as a KR, outcome or output, baseline sourced or missing, calibration profile (sandbagged / aspirational / stretch). *Material to discuss*: from a vague brief, produces candidate Objectives with what each one excludes, and families of Key Results with their traps and forcing mechanisms.

**What it doesn't do:** Never hands back a finished OKR on its own — the Objective is chosen by the person, the Key Results are discussed. Never invents a missing baseline: an absent X is declared « to be measured », never replaced by a plausible number. In template mode, does not rewrite the author's lines.

**Use when:** Quarterly planning, strategic alignment, or a contre-check on an OKR already drafted. Output feeds `tableau-de-bord-kpi` and `indicateurs`.

---

#### `tam-sam-som` — Market sizing with method

**What it does:** Estimates Total Addressable Market, Serviceable Addressable Market, and Serviceable Obtainable Market using top-down and bottom-up methods with explicit hypotheses. Surfaces the method, the figures, and the degree of uncertainty. Web search required in standard/deep mode.

**What it doesn't do:** Does not produce figures from memory without flagging it. TAM/SAM/SOM without hypotheses is a guess, not a sizing.

**Use when:** Preparing a pitch, validating a market opportunity, or building a business case.

</details>

<details>
<summary><b>💻 Tech</b> — 4 skills</summary>

Design and maintain software — architecture, tech debt, support triage, HTML mockup.

---

#### `system-design` — Technical architecture design

**What it does:** Designs a system or technical architecture — components, data flows, API contracts, storage, scalability decisions, and explicit trade-offs. Documents what was decided and why, including options rejected.

**Use when:** Before building a new system, when refactoring an existing architecture, or when a team needs a shared technical blueprint.

---

#### `tech-debt` — Technical debt audit with remediation plan

**What it does:** Identifies, categorizes (structural / code quality / dependency / documentation / test coverage), and prioritizes technical debt with a realistic remediation plan. Distinguishes quick wins from structural work.

**Use when:** Before a significant sprint, during quarterly engineering planning, when velocity has degraded, or before an acquisition due diligence.


---

#### `ticket-triage` — Support ticket categorization and routing

**What it does:** Categorizes an incoming support ticket, assigns a P1–P4 priority based on impact and urgency, identifies missing information needed for handling, and routes to the appropriate team or queue.

**Use when:** Processing incoming support or bug tickets, especially in high-volume contexts where consistent prioritization is needed.

---

#### `mockup` — Standalone HTML mockup

**What it does:** Produces a standalone, presentable HTML mockup from a brief, spec, or visual references, at the chosen fidelity (low, medium, high). Follows an imposed brand guide, shows states (empty, loading, error), marks what is provisional, applies an accessibility baseline (WCAG 2.2 AA) and French formats.

**What it doesn't do:** Not a functional prototype. Not production-ready code.

**Use when:** You need something visual to present to stakeholders, validate with users, or fix a layout before investing in design or engineering.

</details>

<details>
<summary><b>📊 Data & Market</b> — 3 skills</summary>

Read a market and a business model with numbers — competition, SaaS metrics, KPI dashboard.

---

#### `analyse-concurrentielle` — Competitive landscape with differentiation logic

**What it does:** Structures a competitive analysis around differentiation logic — not a list of players. Identifies market forces, compares players on a common framework, surfaces positioning risks and differentiation zones. Web search required in standard/deep mode.

**What it doesn't do:** Does not produce a bullet list of competitors. Does not make strategic recommendations — use `decision` for that.

**Use when:** Before a market entry, a positioning decision, or a fundraising narrative. Pairs with `note-strategique` or `decision` downstream.

---

#### `metriques-saas` — SaaS business model health

**What it does:** Reads SaaS key metrics together — CAC, LTV, NRR, churn, payback period — and interprets them as a system, not in isolation. Surfaces implications for business model health, growth sustainability, and piloting priorities.

**What it doesn't do:** Does not produce benchmarks from memory in standard/deep mode. Does not recommend actions — produces a diagnosis.

**Use when:** Board preparation, fundraising, operational review, or when metric trends are contradictory and you need to understand what they mean together.

---

#### `tableau-de-bord-kpi` — KPI dashboard structure

**What it does:** Defines and structures a KPI dashboard from business objectives, OKRs, or a business context. Distinguishes directly measurable KPIs, estimable KPIs (with stated hypotheses), and problematic KPIs (missing reliable source). Refuses vanity metrics.

**Use when:** After OKRs are set, or when you need to put a monitoring structure in place for a team, product, or business unit.

</details>

<details>
<summary><b>⇢ Workflows</b> — 5 skills</summary>

Recipes that chain several skills, each step isolated in its own context, with pauses where the human validates, answers or chooses. Format: [`docs/format-recette.md`](docs/format-recette.md).

---

#### `brief-client` — From a vague request to an actionable brief

**What it does:** Chains `cadrage` → `questioning` → the client's answers → [`explorer` → `decision`] → `brief`. Only the first step reads the raw request (email, notes, transcript); it produces a context sheet you validate, which travels with the rest. The recipe stops on the questions to send the client and resumes with their answers.

**What it doesn't do:** Does not write the offer (`offre-commerciale`) and does not read a formal tender specification (`reponse-appel-offres`, `analyse-cdc`).

**Use when:** A client request is too vague to price or produce as is.

---

#### `reponse-appel-offres` — Answer a tender end to end

**What it does:** Chains `analyse-cdc` → questions to the buyer → go / no-go → response strategy → `offre-commerciale` → compliance check (`controle-qualite`) → formatting (`deliver`). The tender file is read at step 1 only; the compliance check verifies the offer requirement by requirement against what step 1 extracted. You decide go / no-go.

**What it doesn't do:** Does not replace the decision to bid nor the final proofread; does not handle submission on a platform.

**Use when:** A received call for tenders or specification calls for a full response.

---

#### `concepteur-recette` — Design a workflow recipe, or advise against one

**What it does:** From a recurring job (ideally with a real example), first checks whether one existing skill or a manual sequence is enough; if a chain is justified, proposes the full recipe file in the ix-recipes format, its rationale and the questions to settle before running it. Works only from the real ix-skills and ix-recipes catalogue.

**What it doesn't do:** Does not run the recipe and writes no file: it proposes, you save. Never invents a skill.

**Use when:** You do the same multi-step job often and wonder whether it deserves a recipe.

---

#### `suivi-parcours` — Open the tracking page

**What it does:** Starts the local tracking page bundled in the plugin and gives you its address: create a dossier by pasting the request, review and validate each step, read the deliverable as a document; design, test and keep your own recipes. See [Running a workflow outside the conversation](#running-a-workflow-outside-the-conversation-the-tracking-page) and [Your own recipes](#your-own-recipes).

**What it doesn't do:** Runs no step and reads no dossier itself. Not from Cowork: the page runs on your computer.

**Use when:** You want to run a recipe step by step, with pauses, outside a conversation.

---

#### `configuration-ix` — Check and set up the installation

**What it does:** Checks the ix-skills and ix-recipes plugins (present, up to date, not duplicated), the tracking page's prerequisites, the dossier folder, the page's theme and the optional engines; proposes each change with its command and applies it once you agree.

**What it doesn't do:** Never handles credentials or subscriptions; runs no recipe.

**Use when:** After installing, after an update, or to turn a theme on.

</details>

<details>
<summary><b>📝 Recommendation</b> — 2 skills</summary>

Recommendation deliverables for a decision-maker. Once planned as workflows, they stay skills: a chain would buy no isolation, no human pause and no third party (decided 2026-10-15, after a benchmark of the recipe designer).

---

#### `note-strategique` — Strategic memo, conclusion first

**What it does:** Produces a structured, shareable strategic memo — for a decision-maker, board, or executive. Starts with the conclusion, then the argument, then the options, then the recommendation with explicit trade-offs. Two pages maximum without justification.

**What it doesn't do:** Does not start with context and bury the recommendation at the end. If you don't have a clear position yet, run `decision` first.

**Use when:** You have a recommendation to make and need to package it for a decision-maker. Output is directly shareable.

---

#### `offer-comparison` — Weighted comparison with recommendation

**What it does:** Compares already-received supplier offers on a normalized weighted grid and produces an argued recommendation. Makes the scoring method and uncertainty visible — does not hide trade-offs.

**What it doesn't do:** Does not evaluate offers you haven't received yet. If the proposals are too different in scope, manual normalization is required first.

**Use when:** After receiving multiple quotes for a significant purchase.

> Pipeline: `vendor-scorecard` → `offer-comparison` → `total-cost-analysis` → `decision`.

</details>

---

## Workflows

A workflow chains skills for a recurring job. Format: [`docs/format-recette.md`](docs/format-recette.md). Each step runs isolated (a sub-agent in Claude Code) and receives only what it needs; only the first reads the raw input; a human-validated context sheet replaces it afterwards; pauses let the human validate, answer (client, buyer) or choose. A trace of each step is written to `./parcours/` when possible.

Available: `brief-client`, `reponse-appel-offres` (see the catalog). Both tested end to end on real material (a client meeting transcript, a tender specification). `concepteur-recette` designs new ones.

### Running a workflow outside the conversation: the tracking page

In a conversation, the recipe orchestrates itself through sub-agents. For real isolation, a trace you can resume and no command line, use the tracking page: each step runs in a **fresh call** to an engine (Claude Code by default; Codex or Antigravity in technical mode) that receives only its inputs, and the page stops at every pause for you.

**With the plugins installed** (ix-recipes and ix-skills, in Claude Code on your computer), type `/ix-recipes:suivi-parcours` or ask *"start the ix-recipes tracking page"*. The `suivi-parcours` skill starts it from the plugin itself: Python 3.9+ and the signed-in Claude Code CLI are all it needs. **From a clone** of this repository (ix-skills cloned alongside, or installed as a plugin):

```bash
python3 scripts/interface.py
```

The page opens in your browser (local only, protected by a key in its address). Not from Cowork: the page runs on your computer, out of reach of a remote sandbox. There:

- **New dossier**: pick a recipe, paste the request (client email, notes, tender specification) or import a text file, then *Create and start*.
- **A dossier**: the steps on the left; at the top, the one thing expected from you (*Validate and continue*, *Send the answers and continue*, *Redo the step*…); in the middle, each step's output read as a formatted document, to copy, download or print to PDF. The context sheet, the only thing later steps know of your request, is checked and corrected field by field after step 1.
- **Technical details** (switch at the top): engine and model, cost per step, transmitted fields, raw outputs, exact messages received, log.
- **Recipes** (link at the top): your own recipes — see [Your own recipes](#your-own-recipes).

Dossiers live in `~/.ix-recipes/parcours` (`--parcours-dir` or `PARCOURS_DIR` to change it). Specs: [`docs/interface.md`](docs/interface.md), [`docs/executeur.md`](docs/executeur.md). Measured: a full tender response (7 steps, Claude) cost $0.86 to $1.53 depending on reruns.

The same runner works from the command line, for scripts:

```bash
python3 scripts/parcours.py new reponse-appel-offres --input cdc.md --slug ao --parcours-dir ~/.ix-recipes/parcours
python3 scripts/parcours.py next ao --parcours-dir ~/.ix-recipes/parcours        # runs until the next pause
```

### Your own recipes

Under **Recipes**, the page shows the supplied recipes and yours, each as cards (or as a standard flowchart, one click away; click a step for its mission, inputs and outputs); a supplied recipe can be launched, or copied to make your own version. It also makes recipes, outside the repository:

1. **Build it yourself in blocks**, Scratch-style: pick skills from a palette of the real catalogue, drop them into the chain, set the stops and the optional steps; *Write the recipe* produces the file at no cost. Or:
1. **New recipe**: describe the recurring job (what comes in, what must come out, who reads it). One fresh engine call plays `concepteur-recette` over the **real catalogue** of ix-skills and ix-recipes (the current versions installed), with your need and nothing else. It first returns a **proposal**: the chain of steps, shown step by step, that you comment on (per step or overall) and send back for revision as many times as needed; no file is written until you click *Validate the principle and write the recipe*. When it concludes that one skill or a manual sequence is enough, the page says so and shows its answer; *Design a recipe anyway* asks again, or start from the blank model.
2. **Edit**: the steps and pauses in a readable view, and the recipe file in an editor. Every save is checked like `build.py` checks a recipe of the repository (same rules, in plain French), plus: every skill exists in the catalogue, the id is free.
3. **Test**: play the draft on a real example in a **test dossier**, kept apart from your dossiers. The default `simulation` engine calls no model and costs nothing: each step names what it received and passes its fields on, so the chain, the context sheet and the pauses can be checked. A real run (Claude, Codex…) only when you pick it, after the page shows the steps and the cost ceiling. Test dossiers are deleted in one click.
4. **Keep**: *Validate into my recueil* copies the recipe to `~/.ix-recipes/recettes/<id>.md` (the `recettes` folder next to the `parcours` folder of the dossiers; inside it when the dossier folder has another name, such as an older `~/Parcours`). It then appears in *New dossier* marked *Personal* (and in `parcours.py recipes`), and runs like the others. An id already used by the plugin or the catalogue is refused.
5. **Propose to the repository**: the page prepares a branch from a local clone of ix-recipes (a separate working copy, your checkout is untouched) or from the repository address (cloned once into the recueil): `skills/<id>.md`, its `.mystaffy.json`, `dist/` rebuilt by `build.py` (which needs `pyyaml` and `jsonschema`), a commit. It shows the diff; **nothing leaves your computer before you confirm**. Then `git push` and, on GitHub with `gh` installed, the pull request. Without git, `gh` or write access, the page says what to do.

The same from the command line: `python3 scripts/recettes.py list | draft-new | design | save | promote | contribute …` (see [`docs/interface.md`](docs/interface.md) §9).

Coming next:

```
vendor selection      vendor-scorecard → weightings pause → rfp-draft → offers received → total-cost-analysis → offer-comparison
pre-send review       critique → fact-check → correction → fact-check → deliver → controle-qualite
```

Chains you can already run by hand:

```
research → analyse-concurrentielle → decision
brief    → prd → feature-spec
fiche-poste → interview-loop-planner → interview-guide-recruteur
```

---

## Installation

### Claude Code (plugin — recommended)

The repo is a Claude Code plugin marketplace (`.claude-plugin/marketplace.json` points at the `dist/` plugin root):

```bash
claude plugin marketplace add amiel-35/ix-recipes
claude plugin install ix-recipes@ix-recipes
claude plugin marketplace add amiel-35/ix-skills     # required: the atoms the recipes build on
claude plugin install ix-skills@ix-skills
```

To pick up updates later:

```bash
claude plugin marketplace update ix-recipes
claude plugin update ix-recipes
```

Then restart Claude Code. Releases resolve from the manifest version (`dist/.claude-plugin/plugin.json`), see `CHANGELOG.md`. In the Claude Code desktop app, the same steps go through the `/plugin` command.

**Alternative — the `amiel-35` catalogue.** [amiel-35/plugins](https://github.com/amiel-35/plugins) is a marketplace that lists ix-skills, ix-recipes and ghost-council, each pointing at the `dist/` folder of its own repo:

```bash
claude plugin marketplace add amiel-35/plugins
claude plugin install ix-recipes@amiel-35
claude plugin install ix-skills@amiel-35
```

Install a plugin from one marketplace only (`ix-recipes@ix-recipes` or `ix-recipes@amiel-35`, not both), otherwise it shows up twice; updates then go through `claude plugin marketplace update amiel-35`. Tested in Claude Code; not yet tested with Cowork's "Add from repository", so for Cowork keep the per-repo marketplace below.

The skills that list references (`partials/`, see [Structure](#structure): the 11 HR skills with job-family references, `contrat-emploi` with labour law, the two recruitment-interview skills with their annexes, `contrat-fournisseur` with its clause sets) receive their `references/` folder with the plugin: nothing more to do.

> Transition: until ix-skills 4.0.0, these skills also shipped inside ix-skills. Update ix-skills so they don't show up twice. ix-recipes 2.0.0 removes `code-review` and `contract-review` (see `CHANGELOG.md`).

**Manual fallback**: symlink or copy `dist/skills` into `~/.claude/skills/` — not `skills/`, whose canonical frontmatter is not a valid `SKILL.md`.

### Claude Cowork / claude.ai

**Option A — plugin**: **"Add from repository"** with `amiel-35/ix-recipes`, then again with `amiel-35/ix-skills` (the recipes build on its atoms). References are included.

**Option B — a single skill**: `dist/skills/<id>/` folders are valid Agent Skills; upload one as-is in **Cowork → Customize** (or the ChatGPT Skills editor). For the 11 HR skills that list references (`fiche-poste`, `entretien-professionnel`, `analyse-entretien`…), upload the whole folder, `references/` subfolder included; without it the skill asks for your organisation's competency framework. A single uploaded skill does not bring ix-skills atoms along.

### Codex CLI

Codex reads the same marketplace as Claude Code (tested with codex-cli 0.155.1). The recipes build on ix-skills atoms: add both.

```bash
codex plugin marketplace add amiel-35/ix-recipes
codex plugin add ix-recipes@ix-recipes
codex plugin marketplace add amiel-35/ix-skills
codex plugin add ix-skills@ix-skills
```

Plugins land in `~/.codex/plugins/cache/<marketplace>/<plugin>/<version>/skills/<id>/`, with the `references/` folders. To update, run `codex plugin marketplace upgrade` and re-add the plugin if needed (see `codex plugin --help`). To remove:

```bash
codex plugin remove ix-recipes@ix-recipes
codex plugin marketplace remove ix-recipes
```

**Name the skill in your request** ("use the fiche-poste skill from the ix-recipes plugin to…"). Codex then reads `SKILL.md` and only the reference file it needs. On a plain request that does not name the skill, Codex did not use it in our tests.

The `amiel-35/plugins` catalogue uses `git-subdir` sources and is **not tested with Codex**: for Codex, use the per-repo marketplaces above.

**Legacy installer** (copies into `~/.codex/skills/`, not re-tested on Codex 0.155):

```bash
git clone https://github.com/amiel-35/ix-recipes /tmp/ix-recipes
cd /tmp/ix-recipes
pip install -r requirements.txt
bash scripts/install-codex.sh                 # all skills
bash scripts/install-codex.sh fiche-poste     # one skill
bash scripts/install-codex.sh --dry-run       # preview without installing
```

Skills are installed to `~/.codex/skills/<id>/SKILL.md`, with their `references/` folder when they have one. Restart Codex to activate. Install ix-skills too, with `scripts/install-codex.sh` from its own repo.

### Antigravity CLI (agy, Gemini)

`agy` imports a Claude-format plugin folder (tested with agy 1.3.3). Import ix-recipes and its dependency ix-skills:

```bash
git clone https://github.com/amiel-35/ix-recipes
git clone https://github.com/amiel-35/ix-skills
agy plugin import ix-recipes/dist
agy plugin import ix-skills/dist
```

Skills are imported with their `references/` into `~/.gemini/config/plugins/<plugin>/`. Use `import`: `agy plugin validate` and `agy plugin install` expect a `plugin.json` at the root and do not accept this format. To import the plugins already installed in Claude Code instead (all of them): `agy plugin import claude`. To remove: `agy plugin uninstall ix-recipes`.

As with Codex, **name the skill in your request**: agy then reads `SKILL.md` and only the reference file it needs.

### mystaffy

```bash
python3 build.py --target mystaffy
python3 build.py --target ix-memory   # native ix-memory format
```

These targets carry `skill.md` and `manifest.json` only, not the `references/` folders: the HR skills then ask for the organisation's competency framework.

### GPT / Gemini / other LLMs (chat interfaces)

For plain chat UIs with no CLI: paste the content of `skills/<id>.md` as a system prompt. The YAML frontmatter is ignored harmlessly. For a skill that lists `references` in its frontmatter (the HR skills), also paste the matching `partials/metier_<family>.md` (`metier_tech`, `metier_rh`…), or the skill will ask for the organisation's competency framework. The two recruitment-interview skills also list `transverse_anti_biais` (and `transverse_debrief` for `interview-loop-planner`): paste them too, or the skills keep only their essential rules. Likewise, `contrat-emploi` lists `droit_contrat_travail`, and `contrat-fournisseur` the clause sets `clauses_cgv`, `clauses_contrat_fournisseur` and `clauses_saas_donnees` (paste the one for the document type).

---

## Structure

```
ix-recipes/
├── skills/                 ← canonical source (one .md + .mystaffy.json per skill)
├── partials/               ← job-family references (metier_*.md), interview annexes (transverse_*.md), labour law and clause sets, copied into references/ of the skills that list them
├── scripts/
│   └── install-codex.sh    ← Codex CLI installer
├── dist/                   ← plugin root, committed
│   ├── .claude-plugin/plugin.json   ← plugin manifest (hand-maintained, bump on each release)
│   └── skills/<id>/                 ← Agent Skills artifacts, generated by build.py
│       ├── SKILL.md
│       └── references/              ← only for skills that list references
├── .claude-plugin/
│   └── marketplace.json    ← marketplace manifest, points at ./dist
├── mystaffy-dist/, codex-dist/  ← mystaffy / Codex artifacts (gitignored)
├── build.py                ← multi-target packager, copied from ix-skills
├── requirements.txt        ← jsonschema, pyyaml
├── docs/                   ← banner and working notes
├── LICENSE                 ← MIT
├── LICENSES/               ← licence copies of third-party sources (Apache-2.0)
├── CHANGELOG.md            ← releases, by date
├── THIRD_PARTY.md          ← third-party sources and licences
└── CLAUDE.md               ← contribution guide
```

---

## Building

```bash
pip install -r requirements.txt         # jsonschema, pyyaml
python3 build.py --validate
python3 build.py
python3 build.py fiche-poste
python3 build.py --target agentskills   # dist/skills/<id>/SKILL.md — commit it
python3 build.py --target cowork        # validates dist/.claude-plugin/plugin.json
python3 build.py --target mystaffy --domain rh
python3 build.py --target codex
claude plugin validate dist
```

---

## Sibling projects

- [**ix-skills**](https://github.com/amiel-35/ix-skills) — the ingredients: atomic cognitive moves (critique, decision, explorer, fact-check…) and advisory postures (`dixieme-homme`, `red-team`, `contrarian`…). Required by ix-recipes.
- [**ghost-council**](https://github.com/amiel-35/ghost-council) — philosophers' reasoning methods encoded as skills (Popper, Kant, Pascal, Wittgenstein…), and `/council`, which has several independent angles deliberate on a decision.
- [**plugins**](https://github.com/amiel-35/plugins) — the `amiel-35` marketplace listing ix-skills, ix-recipes and ghost-council in one place.

---

## Contributing

Fork, edit, PR. Read [`CLAUDE.md`](CLAUDE.md) for the canonical skill format, the dependency rule with ix-skills and the checklists, and [`CHANGELOG.md`](CHANGELOG.md) for versions.

A skill that applies a reasoning move to any content belongs in ix-skills; a skill that needs domain know-how belongs here.

---

## Credits

Several skills draw on public sources. Each source taken from is listed in [`THIRD_PARTY.md`](THIRD_PARTY.md), with what was taken and under which licence.

---

## License

MIT, see [LICENSE](LICENSE).
