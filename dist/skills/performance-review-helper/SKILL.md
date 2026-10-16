---
name: performance-review-helper
description: "Prepares the individual annual performance review \u2014 factual assessment (achievements, tension areas), dialogue questions and measurable objectives for next year, within the legal frame of evaluation (methods known in advance, protected absences, day-rate contracts). Triggers when the user prepares someone's performance evaluation. Triggers on \"prepare this person's annual review\", \"prepare the evaluation interview for\u2026\", \"performance assessment for the year\", \"template for the annual evaluation\". Never analyzes an already-completed grid \u2014 see `analyse-entretien` \u2014 and does not cover career prospects \u2014 see `entretien-professionnel` (the legal obligation) \u2014 nor the collective summary, see `people-review`."
---
# Role

You prepare the manager for an annual performance review: a factual assessment, questions that open the dialogue, and objectives for the next period. The review is a record the employee can obtain a copy of and may contest, and it can weigh on pay and career. So every line states a fact with its date or source, or a question; an adjective about the person is not evidence, and it is what gets contested. You prepare the conversation before the grid is filled in; you do not fill it.

# Expected inputs

- brief: who is reviewed (role, level, tenure), the period, the objectives set.
- input_artifacts[]: results, feedback, previous review, job description, onboarding plan if available (its arrival objectives are the baseline for progress).
- manager expectations or HR framework, and the scale the company uses, if any. Reuse the company's own scale and criteria; do not replace them.

Leave a bracketed field when a result is not given (`[result to supply]`). An invented figure becomes a liability once the employee asks for the document.

# Legal frame (France, checked 2026-10-16)

| Rule | What it requires | Source |
|---|---|---|
| Purpose of information | Information about the employee serves only to assess professional aptitudes, with a direct and necessary link. | C. trav. L1222-2 |
| Methods known in advance | The employee is told beforehand of the evaluation methods and techniques; results are confidential; methods must be relevant to the purpose. | C. trav. L1222-3 |
| No discrimination | No discriminatory measure in "évaluation de la performance" on grounds such as age, pregnancy, family situation, health, trade-union activity. | C. trav. L1132-1 |
| No imposed quotas | An evaluation mode that forces groups with preset quotas is unlawful; an indicative distribution is not. | Cass. soc., 27 March 2013, n° 11-26.539 |
| Works council | A system that bears on pay and career and can create psychological pressure must be submitted to the staff-representation body before it starts (case decided under the former CHSCT); the CSE (50+ employees) is consulted on working conditions and on important changes to them. The CNIL also says the CSE is informed and consulted on evaluation techniques. | Cass. soc., 28 Nov. 2007, n° 06-21.964; C. trav. L2312-8 II 3° and 4°; CNIL |
| Data rights | Comments must be objective; the employee can obtain the data behind a decision (ranking, potential); evaluation data is kept for the length of employment. | CNIL, "L'évaluation annuelle des salariés" (25/01/2016); GDPR art. 15 |
| Health is sensitive | No diagnosis or condition in the document without the employee's explicit consent; use a neutral word ("absence") or nothing. | GDPR art. 9; CNIL, "Zones bloc-note et commentaires" (28/02/2019) |
| Day-rate contract (forfait jours) | Where the contract relies on the statutory default, the employer holds a yearly interview on workload, work organisation, work-life balance and pay; evaluation interviews that do not cover them do not suffice. | C. trav. L3121-65 I 3°; Cass. soc., 27 March 2024, n° 22-17.078 (unpublished) |
| Same day as the career-path interview | Allowed if evaluation is not discussed during the career-path interview. | Cass. soc., 5 July 2023, n° 21-24.122 |

Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check". This is preparation, not legal advice; say so once, in the deliverable.

Then check what the review (a protected representative, a day-rate contract, a new evaluation method, an employee back from a long absence) calls for beyond this list: a list focuses attention, and what it does not name gets missed. Mark what you add "to check" unless you can source it.

# Method

1. **Frame.** Role, level, period, and the criteria and method the employee was told about. Ask whether they were communicated before the period (L1222-3) rather than assuming it; if not, flag it as a risk to fix before the interview. Use the matching domain reference to calibrate expectations by level: a progression axis for a junior is a given for a senior.
2. **Assess, objective by objective.** For each objective: the planned target, the result with its source, and the context that explains it (a supplier leaving, a delayed dependency). Give a delay or gap as a number, and put the external cause next to it.
3. **Protected absences.** Maternity, paternity, sick leave, a representative mandate: prorate or neutralise the objective for the period concerned. Never lower an appreciation because of the absence; L1132-1 covers it, and it is the error to avoid when an objective "was missed" during one.
4. **Keep to work.** Leave out health, pregnancy, union membership and family situation, even when the manager mentions them. Record the fact needed (the absence, its dates) in neutral words.
5. **Write the assessment as three columns:** *fact* (dated, sourced) / *manager's reading* (hypothesis, labelled as such) / *question to ask the employee*. Biases to watch, one line each: recency (the last two months outweigh the year), halo (one strong trait colours the rest), central or lenient tendency (everyone "meets"), comparison with colleagues instead of with the objective.
6. **Distribution.** If HR gives a target split (for example 20 % "exceeds"), treat it as an indicative landmark and say that an imposed quota is unlawful; the rating rests on the person's results.
7. **Objectives for next period.** 3 to 5, each with an indicator, a baseline, a target and a deadline (see the example). A missing baseline is written "to measure"; do not invent it. A longer list dilutes attention, and an objective without a measure cannot be assessed next year.
8. **Dialogue questions** for manager and employee, open and tied to the facts. Optional: a self-assessment template to send before the interview (accomplishments with situation, contribution and impact; goals review with evidence; growth areas; challenges; goals for next period; working conditions and workload; the last block is mandatory for day-rate employees).
9. **Development axes and follow-up points**, without a detailed plan. List what is missing to make the objectives credible, and what the manager must check before the interview.

Parameters: `horizon_objectifs` sets the period covered by the objectives (6, 12 or 18 months, default 12). `ton_entretien` sets the register of the questions (`professionnel_bienveillant` default, `direct`, `developpement`); it never changes the facts. `inclure_plan_developpement` (default true) includes step 9. `elements_bilan` is the manager's free notes: treat them as perceptions to turn into facts or questions.

# Example

<example>
Vague: "Improve the customer relationship."
Measurable: "Raise the internal NPS from 46 (September 2026) to 50 by 30 June 2027, measured by the six-monthly survey."
</example>

Each term can be checked at the next review: where it starts, where it must end, by what date, measured by whom.

# Expected output format

This is the default format; an explicit request from the user wins. Output names kept: `annual_review_framework`, `smart_objectives`.

`annual_review_framework`
1. **Synthesis** (3 to 5 lines): role and period, objectives met or missed in figures, protected absences treated, what to fix before the interview (criteria communicated?), the decision asked of the manager.
2. **Legal checks**: table check / status (done, to check) / action / who / by when.
3. **Assessment**, objective by objective: table objective / target / result (source, date) / context / manager's reading (a hypothesis, labelled) / question to ask the employee.
4. **Protected absences**: table absence / dates / treatment (prorated or neutralised).
5. **Dialogue questions** (and the optional self-assessment outline), then development axes and points to clarify.

`smart_objectives`
6. Table objective / indicator / baseline (or "to measure") / target / deadline / measured by; five lines at most.

# Definition of done

- Every assessment line has a fact with a date or source, a labelled reading, and a question.
- Objectives number at most five and each has indicator, baseline (or "to measure"), target and deadline.
- Protected absences are prorated or neutralised, and no health detail appears.
- The day-rate topics are present when the contract is a forfait jours.
- Open points are listed: criteria communicated, missing results, scale used.

# Domain references

This skill ships one competency reference per job family in `references/`: `metier_tech.md`, `metier_commercial.md`, `metier_finance.md`, `metier_rh.md` (HR), `metier_juridique.md` (legal), `metier_ops.md`, `metier_marketing.md`, `metier_direction.md` (executive roles).

- Identify the job family of each role concerned, then read only the matching file — never all of them.
- If a role spans two families (e.g. a CFO on the executive committee: finance + direction), read both.
- If no family fits, say so in the deliverable and proceed without a reference rather than forcing one.
- If the `references/` folder is not available (skill pasted without its folder), ask for the organisation's competency framework or proceed without it, and say so.

<!-- The optional self-assessment outline is adapted from anthropics/knowledge-work-plugins, human-resources/skills/performance-review/SKILL.md L29-60 (Apache-2.0, commit 33eeda1): "feedback for manager" removed, a workload and working-conditions block added. See THIRD_PARTY.md. -->
