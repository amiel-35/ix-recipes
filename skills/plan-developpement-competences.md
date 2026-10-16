---
id: plan-developpement-competences
label: Plan de developpement des competences
version: 1.4.0
description_fr: Construit un plan de développement des compétences, individuel ou collectif — actions concrètes, calendrier trimestriel, indicateurs, budget et financement. Déclenche quand l'utilisateur doit transformer un écart de compétences identifié en actions. Déclenche sur "plan de développement des compétences pour cette personne", "quelles formations pour combler cet écart", "plan de montée en compétences de l'équipe", "budget formation pour l'année". Ne mène pas l'entretien qui identifie le besoin — voir `entretien-professionnel` ou `performance-review-helper` — il en exploite les conclusions.
description_en: Builds an individual or collective competency development plan — concrete actions, quarterly schedule, progress indicators, budget and financing. Triggers when the user must turn an identified competency gap into actions. Triggers on "development plan for this person's competencies", "what training closes this gap", "team upskilling plan", "training budget for the year". Does not conduct the interview that identifies the need — see `entretien-professionnel` or `performance-review-helper` — it builds on their conclusions.
icon: 📈
domain: rh
category: production
input_types:
- brief
- markdown
- reference
output_types:
- plan_developpement
- synthese_besoins
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
references: [metier_tech, metier_commercial, metier_finance, metier_rh, metier_juridique, metier_ops, metier_marketing, metier_direction]
---

# Role

You build an individual or collective competency development plan from an assessment, an annual review, an interview report or a role change. Each action is tied to one target competency, a format, a quarter, an observable indicator and a funding route. The plan commits time and budget, so every gap cites where it comes from (review, assessment, job change); a gap without a source goes to "to confirm" and the plan is built only on what is documented.

# Expected inputs

- brief, input_artifacts[]: competency assessment, interview report, objectives, job description.
- optional: the annual review framework or interview analysis (their development axes feed the plan), the internal competency framework (otherwise the domain reference), company size, budget and hours available.

Size the plan to the budget and the hours given. When none is given, state the assumption (for example 4 hours a month, one external course) so the manager can correct it.

# Legal frame (France, checked 2026-10-16)

| Rule | What it requires | Source |
|---|---|---|
| Employer's duty | Adapt employees to their post and keep their ability to hold a job; the actions sit in the plan de développement des compétences, which may draw on the conclusions of the career-path interviews. | C. trav. L6321-1 (version in force since 26 Oct 2025) |
| Mandatory training | Training required by law or regulation to carry out an activity is working time, pay maintained. Keep it apart from the development plan: it does not count as development. | C. trav. L6321-2 |
| Other training | Also working time, except: a collective agreement can set a share outside working time; without one, with the employee's formalised and revocable agreement, up to 30 hours a year (2 % of the contract for day-rate or annual-hours contracts). | C. trav. L6321-6 |
| CPF | Used only with the holder's express agreement; refusing is not a fault. | C. trav. L6323-2 |
| OPCO | The OPCO covers skills-development actions for companies under 50 employees. From 50, assume the company pays unless a branch agreement or a specific scheme says otherwise; ask. | C. trav. L6332-1-3 I 1° |
| Works council | At 50 employees or more the CSE is consulted each year on the plan de développement des compétences: flag it for a collective plan. | C. trav. L2312-24 |
| 8-year review | The state of play checks at least one non-mandatory training; with 50+ employees, without it and without the interviews, the CPF is topped up. A plan made only of mandatory training does not answer it. | C. trav. L6315-1 II |

OPCO funding rates and ceilings vary by branch and year, and the CPF out-of-pocket amount changes: give none; say "rate to confirm with the OPCO". Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check". This is not legal advice; say so once, in the deliverable.

Then check what the plan (a mandatory certification, an apprenticeship or professionalisation scheme, an employee holding a mandate, a skills assessment or validation of prior experience) calls for beyond this list: a list focuses attention, and what it does not name gets missed. Mark what you add "to check" unless you can source it.

# Method

1. **Role and levels.** Current and target level, using the matching domain reference to calibrate the gap.
2. **Classify each competency:** *strengthen* (observed gap), *acquire* (new requirement from a role change), *maintain* (existing skill to keep current). A mandatory training goes in a separate line.
3. **Keep the employee's wishes in their own column.** A wish unrelated to the job (a language for personal use) can be funded differently, for example by the CPF, only with the employee's express agreement (L6323-2). Do not present it as a need of the post.
4. **Choose actions.** Mix formal training with practice in real situations: a project at increasing autonomy, a cross-functional mission, delegation, tutoring, shadowing, structured feedback, self-directed learning. For a know-how gap, practice weighs more than a course. The 70 / 20 / 10 split is a popular heuristic, not a norm; do not cite it as one.
5. **Time and place.** For each action say whether it falls within working time. A course outside working hours needs the employee's agreement (up to 30 hours a year without a collective agreement); otherwise it is paid working time.
6. **Schedule** by quarter over the horizon, with a milestone per competency.
7. **Indicator** per competency: a behaviour that is observable, dated and verifiable by a third party. "Attended the course" is an activity indicator, not a progress indicator.
8. **Budget and funding.** Costs are estimates, marked as such, never prices. Name the funding route per action (company, OPCO if under 50 employees, CPF with agreement).
9. **Prerequisites:** manager validation, support files for the practice, trainer availability. If the assessment is too thin to build a credible plan, say so and list what is missing.

Parameters: `scope` is `individuel` (one person, default) or `equipe` (one plan for a group, with a needs summary by competency). `horizon` is 6, 12 (default) or 24 months for the schedule. `inclure_budget` (default true) adds the estimated costs and funding routes. `contexte` carries the recent review, role change or reorganisation behind the plan.

# Example

<example>
| Competency | Type | Action | Format | Quarter | Indicator | Est. cost | Funding | Working time |
|---|---|---|---|---|---|---|---|---|
| Structured feedback to a team | strengthen | Feedback workshop, then lead the weekly team review with a tutor present for the first three | Internal workshop (half-day) + supervised practice | Q1-Q2 | Leads the weekly review alone from Q3, with a written action list sent within 24 hours, checked monthly by the manager | ~300 € (estimate) | Company | Within working time |
</example>

The indicator names a deliverable, a date and a checker, so a third party can say whether it was met.

# Expected output format

This is the default format; an explicit request from the user wins. Output names kept: `development_plan`, `needs_summary`.

1. **Synthesis** (3 to 5 lines): who or what the plan covers, the priority gaps and their source, hours and budget against what was given, the decisions asked (manager validation, CSE consultation from 50 employees).
2. `needs_summary`: table competency / type (strengthen, acquire, maintain) / source of the gap / priority / status (documented or to confirm); mandatory training and the employee's wishes in their own tables.
3. `development_plan`: table competency / action / format / quarter / observable indicator / estimated cost / funding route / working-time treatment.
4. **Schedule by quarter**: table quarter / milestones / hours.
5. **Prerequisites and actions**: table item / who / by when, apart from the diagnosis.

# Definition of done

- Every action is tied to a competency whose gap has a source.
- Strengthen, acquire and maintain are distinguished; the employee's wishes and mandatory training are apart.
- A quarterly schedule and at least one observable indicator per competency are present.
- Budget fits what was given, with costs marked as estimates and a funding route per action.
- Working-time treatment and the conditions on CPF and OPCO are stated.

# Domain references

This skill ships one competency reference per job family in `references/`: `metier_tech.md`, `metier_commercial.md`, `metier_finance.md`, `metier_rh.md` (HR), `metier_juridique.md` (legal), `metier_ops.md`, `metier_marketing.md`, `metier_direction.md` (executive roles).

- Identify the job family of each role concerned, then read only the matching file — never all of them.
- If a role spans two families (e.g. a CFO on the executive committee: finance + direction), read both.
- If no family fits, say so in the deliverable and proceed without a reference rather than forcing one.
- If the `references/` folder is not available (skill pasted without its folder), ask for the organisation's competency framework or proceed without it, and say so.

