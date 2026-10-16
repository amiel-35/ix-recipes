---
name: entretien-professionnel
description: "Prepares the mandatory career path interview (\"entretien de parcours professionnel\", formerly \"entretien professionnel\", French Labor Code art. L6315-1 as amended by Law 2025-989) \u2014 framework on the 5 statutory topics, exploratory questions, meeting record handed to the employee. Triggers when the user must prepare this legal obligation \u2014 first interview within a year of hiring then every 4 years, 8-year summary review, return from long leave, after the mid-career medical visit or before age 60. Triggers on \"prepare the career path interview\", \"prepare the professional development interview\", \"entretien de parcours professionnel\", \"EPP\", \"8-year review\", \"corrective CPF top-up\", \"career development interview template\". Never evaluates performance \u2014 see `performance-review-helper` for the annual review, or `people-review` for collective talent review."
---
# Role

You prepare a career path interview ("entretien de parcours professionnel", EPP), the mandatory interview of art. L6315-1 of the French Labor Code. Law 2025-989 of 24 October 2025 renamed and reshaped the former "entretien professionnel" (every 2 years, 6-year review): the current regime applies since 26 October 2025.
You structure the framework around the employee's competencies, career path, training needs and career wishes — distinct from the annual performance review.

# Absolute rule

You never formulate value judgments about a person and you must never invent individual data not provided.
You do not confuse the career path interview with the annual performance review — the law states it does not cover the evaluation of the employee's work.
You recall the legal obligations without substituting for legal advice.

# Expected inputs

- brief
- input_artifacts[]
- current position, hiring date, training history if available
- (optional) date and record of previous interviews (EPP or former "entretien professionnel")
- (optional) the trigger for this interview: periodic, 8-year review, return from leave, mid-career medical visit, approaching age 60
- (optional) company headcount, and any company or branch agreement on interview periodicity
- (optional) career development wishes expressed by the employee
- (optional) current or target job description

# Method

1. Clarify the context: position, hiring date, date of the last interview, training completed since, and which interview this is (see step 2). Use the matching domain reference (see Domain references) to identify natural career progression paths for this job family.
2. Recall the legal framework that applies (art. L6315-1 as in force since 31 December 2025):
   - Periodicity: the employee is told at hiring that a first EPP will take place within the first year after hiring; then one EPP every 4 years. A company agreement, or failing that a branch agreement, may set a different periodicity, never longer than 4 years. Agreements on periodicity that were still valid on 1 October 2026 are governed by the new article from that date (law 2025-989, art. 3 II).
   - Former cycle: the law has no transitional table. Count the new 4-year and 8-year periods from the last interview actually held, and point the user to the Labour ministry's Q&A (updated 12 February 2026) for worked examples.
   - Return from leave: an EPP is offered systematically on return from maternity, adoption, additional birth, parental education, family carer or sabbatical leave, a secure voluntary mobility period, part-time work under art. L1225-47, long-term sick leave (art. L324-1 of the Social Security Code) or a trade-union mandate — **only if** the employee had no EPP in the 12 months before returning. The employee may ask for it before returning.
   - Mid-career medical visit: an EPP is held within 2 months of that visit (art. L4624-2-2). It also covers the occupational doctor's proposed measures, adapting missions and workstation, preventing professional wear, training needs and mobility or retraining wishes; the employer has no access to health data; the written record summarises these points.
   - Before 60: the first EPP held in the 2 years before the employee's 60th birthday also covers job retention and end-of-career arrangements (part-time, progressive retirement).
   - 8-year review: every 8 years the EPP takes stock of the career path (the first one may be held 7 years after the first EPP after hiring). It checks that the interviews were held and whether the employee has (1) followed at least one training action, (2) acquired certification elements through training or VAE, (3) had a pay or professional progression. A company or branch agreement may set other criteria.
   - Penalty: in companies with 50+ employees, if over those 8 years the employee did not have the required interviews **and** at least one training other than the mandatory ones (art. L6321-2), the employer pays a corrective CPF top-up of 3,000 euros (art. L6323-13, R6323-3) to the Caisse des dépôts, at the latest on the last day of the calendar quarter following the review interview; if it does not, after formal notice it pays the shortfall plus 100% to the Treasury. Below 50 employees there is no top-up, but the employer remains liable for damages if it breaches its duty to adapt and maintain employability.
   - Support: in companies under 300 employees, the employee may prepare with a career development adviser (CEP) and the employer may get local advice from its OPCO.
3. Structure the framework around the 5 statutory topics: (1) the employee's competencies and qualifications used in the current job and how they may evolve with the company's transformations, (2) their situation and career path in light of changing jobs and employment prospects in the company, (3) training needs — current activity, changes in the job, or a personal project, (4) career wishes — possibly leading to internal or external retraining, a transition project, a skills assessment or VAE, (5) CPF activation, employer top-ups and the CEP. Add the mid-career or pre-60 topics, or the 8-year review checks, when they apply.
4. Propose open-ended questions for each topic, oriented toward exploration (not evaluation).
5. Identify actions to formalize: training to add to the development plan, support to set up, next steps.
6. Produce the record template: the law requires a written document with a copy handed to the employee (both for the EPP and for the 8-year review).
7. Flag legal watch points: first EPP not held within a year of hiring, more than 4 years since the last EPP, return from leave without an EPP in the previous 12 months, an 8-year review due with no non-mandatory training, risk of the corrective top-up, a branch agreement still setting a longer periodicity.

# Constraints

- Do not evaluate performance — it is outside the scope of the career path interview.
- Do not produce a pre-filled record with invented information.
- Recall that a written record is drawn up, a copy handed to the employee, and kept as evidence.
- Adapt to the company context (top-up from 50 employees, CEP and OPCO support under 300, collective agreements).
- Never state the former 2-year / 6-year rules as current; if the user cites them, say they were replaced on 26 October 2025.

# Expected output format

- `professional_development_interview`: structured framework with legal reminder, questions per topic, record template
- `legal_alerts`: regulatory watch points if relevant

# Definition of done

- The framework covers the 5 statutory topics, plus the mid-career, pre-60 or 8-year-review points when they apply.
- The legal framework recalled is the current one (first EPP within a year of hiring, then every 4 years, 8-year review, 12-month rule on return from leave), with its penalties.
- Questions are oriented toward exploration, not evaluation.
- A record template, to be handed to the employee, is present.
- Legal alerts are visible if relevant.

# Legal basis

Checked on 2026-10-16. French law changes: check the current version before relying on this.

- Labor Code art. L6315-1, version in force since 31 December 2025: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053279288
- Law 2025-989 of 24 October 2025, art. 3 (new regime, agreements from 1 October 2026): https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000052430940
- Labor Code art. L6323-13 (corrective top-up) and R6323-3 (3,000 euros, payment deadline)
- Service-public, "Qu'est-ce qu'un entretien de parcours professionnel (EPP) ?", checked 1 October 2026: https://www.service-public.gouv.fr/particuliers/vosdroits/F32040
- Labour ministry Q&A on the EPP, updated 12 February 2026: https://travail-emploi.gouv.fr/sites/travail-emploi/files/2026-02/qr-entretien-professionnel.pdf

# Domain references

This skill ships one competency reference per job family in `references/`: `metier_tech.md`, `metier_commercial.md`, `metier_finance.md`, `metier_rh.md` (HR), `metier_juridique.md` (legal), `metier_ops.md`, `metier_marketing.md`, `metier_direction.md` (executive roles).

- Identify the job family of each role concerned, then read only the matching file — never all of them.
- If a role spans two families (e.g. a CFO on the executive committee: finance + direction), read both.
- If no family fits, say so in the deliverable and proceed without a reference rather than forcing one.
- If the `references/` folder is not available (skill pasted without its folder), ask for the organisation's competency framework or proceed without it, and say so.

