---
id: onboarding-plan
label: Plan d'onboarding
version: 1.3.0
description_fr: Construit un plan d'intégration 30-60-90 jours pour un nouveau collaborateur — objectifs, actions, réunions, livrables et points de contrôle par phase, plus les formalités légales d'arrivée datées (DPAE, document d'information, visite médicale) et le point de décision sur la période d'essai. Déclenche quand l'utilisateur doit préparer l'arrivée d'une recrue. Déclenche sur "plan d'onboarding 30-60-90 jours", "prépare l'intégration du nouveau développeur", "checkpoints pour les 90 premiers jours", "que doit-on préparer avant son arrivée". Ne traite pas un départ — voir `offboarding-structure` — et ne conçoit pas la boucle d'entretien qui a précédé le recrutement, voir `interview-loop-planner`.
description_en: Builds a 30-60-90 day onboarding plan for a new employee — objectives, actions, meetings, deliverables and checkpoints per phase, plus the dated legal formalities of arrival (hiring declaration, information document, medical visit) and the decision point on the trial period. Triggers when the user must prepare a new hire's arrival. Triggers on "30-60-90 day onboarding plan", "prepare the new developer's integration", "checkpoints for the first 90 days", "what should we prepare before they start". Does not handle a departure — see `offboarding-structure` — nor the interview loop that preceded the hire, see `interview-loop-planner`.
icon: ◫
domain: rh
category: production
input_types:
- brief
- markdown
- reference
output_types:
- plan_onboarding
- pre_requis_onboarding
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

You build the onboarding plan of one new hire: three phases over 90 days, the formalities the employer owes at arrival, and the date by which the manager must decide on the trial period. The plan is shared between the manager, HR and the new hire, so it must be concrete, progressive and written about the role, never about the person's weaknesses.

A plan that thinks only of equipment and rituals leaves out what exposes the employer: legal deadlines at arrival, and a mid-term review placed too late to inform the trial-period decision. The legal table below is there because that is what is usually forgotten.

# Expected inputs

- brief, `input_artifacts[]`: role, team context, work environment, start date, contract type, trial period length, goals or constraints.
- Optionally: the Go / No-go interview summary (post-hire success conditions, competencies to strengthen, sponsor) and the consolidated scorecard.
- Dates of absence of the manager and the buddy if known; if not, ask.

Parameters, when the form supplies them: `seniorite_poste` (junior / intermediate / senior / management: sets the pace and the autonomy expected), `mode_travail` (on site / hybrid / remote: changes the meetings, the equipment and the on-site days), `inclure_checkpoints` (default yes: include a checkpoint per phase), `contexte_equipe` (team, key contacts, constraints).

# References

This skill ships one competency reference per job family in `references/`: `metier_tech.md`, `metier_commercial.md`, `metier_finance.md`, `metier_rh.md` (HR), `metier_juridique.md` (legal), `metier_ops.md`, `metier_marketing.md`, `metier_direction.md` (executive roles).

Identify the job family and read only the matching file: it says what "autonomy" means concretely for this family and level, which calibrates the pace of the three phases. If the role spans two families, read both. If no family fits, say so and proceed without a reference. If `references/` is not available (skill pasted without its folder), ask for the organisation's competency framework or proceed without it, and say so. Take the pace from the level and state it as an assumption.

# Legal frame: arrival and trial period (France, checked 2026-10-16)

| Rule | What it imposes | Source |
|---|---|---|
| C. trav. L1221-10; R1221-4; R1221-5 (version of 28 Dec. 2025) | The hiring can only take place after the hiring declaration (DPAE); sent at the earliest in the 8 days before the expected hire date; made electronically, otherwise by registered letter sent at the latest on the last working day before the hire. | Légifrance |
| C. trav. L1221-5-1; R1221-35 | Written main information (identity, workplace, job, hire date, trial period, pay, working time): at the latest the **7th calendar day** from the hire date; the rest within one month. The signed contract covers it if it contains these items. | Légifrance |
| C. trav. L1221-13 | Entry in the single staff register at the time of hiring. | Légifrance |
| C. trav. L4141-2 | Practical safety training for every worker hired. | Légifrance |
| C. trav. R4624-10 | Information and prevention visit within **3 months** of actually taking up the post. | Légifrance |
| C. trav. R4624-18; R4624-24 | Night workers and workers under 18: the visit takes place **before** assignment. Posts under reinforced individual follow-up: a medical fitness examination **before** assignment, in place of the visit. | Légifrance |
| CSS L911-7 | Compulsory collective health cover, financed at least half by the employer: plan the enrolment at hiring; some employees may waive it on their own initiative (short fixed-term contracts, for example): collect the waiver, the form of which is to check. | Légifrance |
| C. trav. L1221-19, L1221-21, L1221-25 | Trial period: 4 months for a cadre (renewal only if an extended branch agreement allows it and the contract says so); the employer's notice is one month after 3 months of presence and does not extend the trial. | Légifrance |
| C. trav. L3121-64, II | Days forfait: the authorising agreement sets the follow-up of the workload and the periodic exchange with the employee. | Légifrance |

Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check".

# Method

1. **Frame.** Role, context, expectations for 90 days; calibrate with the reference. If the interview summary or scorecard is provided, extract the competencies to strengthen (scored partial), the success conditions and the sponsor.
2. **Compute the dates** when the start date and the trial length are known (otherwise ask): DPAE window, written information deadline, safety training, visit deadline, **end of trial period** and **last date to decide**. The latter is the trial end minus the employer's notice that applies at the notification date (one month once 3 months of presence are reached). A mid-term review placed after it cannot inform the decision, so make the 60-90 day checkpoint the **decision point on the trial period**. For a four-month trial, a termination is notified about a month before the end, around day 90.
3. **Prerequisites table** (`onboarding_prerequisites`): "Before day 1 / first week / first three months", with item, deadline (a date, not "before arrival"), owner, legal basis. A computed date can be checked and planned, "before arrival" cannot. Add the practical items: accounts, equipment, welcome message, calendar, desk or remote set-up, buddy.
4. **Three phases** (discovery, skill-building, autonomy). Each has an objective that prepares the next, concrete actions that serve it, the people the new hire meets, deliverables, and at least one checkpoint. Name a buddy who is not the manager, since the manager cannot be the only person the hire dares to ask.
5. **Day 1 and week 1** with a light first day (set-up, introductions, role expectations); deep work starts in week 2, because a loaded first day is retained by no one. Add the key-contacts table (manager, buddy, IT, HR: who for what).
6. **Absences.** Place the checkpoints around the manager's and buddy's absences, or name a relay.
7. **Working mode.** For hybrid or remote: which meetings happen on site, the equipment, how isolation is avoided. For a days forfait, plan a first workload discussion.
8. **Confidentiality of the scorecard.** The plan is shared with the new hire: turn a partial score into a **development objective stated on the role** ("lead a mentoring pairing by day 60") and never quote the verdict, the score or the interviewers' words. The hire would read an interview assessment out of context, and interview notes are restricted data.
9. **Unknowns.** What depends on a team context you were not given (tools, projects, people) is a question for the manager, not something to invent: an invented need or weakness reads as a judgment of the person.

<example>
| Item | Deadline | Owner | Legal basis |
|---|---|---|---|
| Written key information (identity, job, hire date, trial, pay, working time), unless the signed contract carries it | Start Monday 11 Jan. 2027: by the 7th calendar day, Sunday 17 Jan., so deliver by Friday 15 Jan. | HR | L1221-5-1, R1221-35 |
| Information and prevention visit | Book at hiring; must take place within 3 months of 11 Jan.: by Friday 9 Apr. 2027 (11 Apr. is a Sunday) | HR with occupational health | R4624-10 |

Why it works: each deadline is computed from the start date and adjusted to a working day, so the owner can put it in a calendar; "within the first weeks" would not have prevented a miss.
</example>

# Expected output format

- `onboarding_plan`: 30 / 60 / 90 days with objectives, actions, meetings, deliverables, checkpoints, the trial decision point, key contacts, questions to the manager.
- `onboarding_prerequisites`: the dated table (before day 1, first week, first three months) with legal basis.

# Definition of done

- The plan covers D1-D30, D30-D60 and D60-D90, each with objectives, actions and at least one checkpoint.
- The prerequisites table has computed dates, owners and legal bases, including the hiring declaration, the information document, the visit and health cover.
- The end of the trial period and the last date to decide are stated (or asked for), and the decision point is placed before it.
- Nothing taken from the scorecard is quoted; weak points appear as role-based objectives.
- Absences of the manager and the buddy are handled; what is unknown is listed as questions.

<!-- Pre-start checklist, day-1 and week-1 programme, key-contacts table and the advice not to overload day 1 and to assign a buddy other than the manager adapted from anthropics/knowledge-work-plugins, human-resources/skills/onboarding/SKILL.md (L33-79, L100-104) (Apache-2.0, commit 33eeda1): rewritten and completed with the French legal formalities and the trial-period decision point. See THIRD_PARTY.md. -->
