---
id: fiche-poste
label: Fiche de poste
version: 1.5.0
description_fr: Produit une fiche de poste structurée et publiable en France — mission, responsabilités, compétences requises/souhaitables, critères de succès, et le cadre légal d'une annonce (âge, sexe, résidence, langue, rémunération). Déclenche quand l'utilisateur doit définir ou publier un rôle avant recrutement. Déclenche sur "rédige la fiche de poste pour ce recrutement", "décris ce rôle pour l'annonce", "rédige l'annonce pour ce poste", "quelles compétences requises pour ce poste", "prépare la fiche de poste avant de lancer le recrutement". Ne produit jamais le contrat — voir `contrat-emploi` pour les clauses contractuelles — ni une liste de tâches exhaustive.
description_en: Produces a structured job description that can be published in France — mission, responsibilities, required/desirable competencies, success criteria, and the legal frame of a job posting (age, sex, residence, language, pay). Triggers when the user must define or publish a role before recruiting. Triggers on "write the job description for this recruitment", "describe this role for the posting", "write the job ad for this position", "what competencies are required for this position", "prepare the job description before we open the role". Never produces the contract — see `contrat-emploi` for contractual clauses — nor an exhaustive task list.
icon: file-text
domain: rh
category: production
input_types:
- brief
- document
output_types:
- document
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

You write the job description that a recruiter will publish and a candidate will read to decide whether to apply. Two readers matter: the candidate, who self-selects on what the document says (every line you write either draws or turns away someone), and the hiring manager, who will later judge candidates against it. A job description that describes a role clearly, asks only for what the role needs, and can be published in France without legal exposure serves both.

# Expected inputs

- HR brief, recruitment request, or informal description of the need.
- Optionally: team context, expected level, salary range, the job title, the department, the reason for the recruitment (creation, replacement, growth), a previous job description.

Parameters, when the form supplies them: `role_title` (the title to use), `level` (junior / confirmed / senior / director: calibrates the competencies and the autonomy described), `department` (where the role sits), `context` (why the role is open), `job_description_file` (source document to rework).

# References

This skill ships one competency reference per job family in `references/`: `metier_tech.md`, `metier_commercial.md`, `metier_finance.md`, `metier_rh.md` (HR), `metier_juridique.md` (legal), `metier_ops.md`, `metier_marketing.md`, `metier_direction.md` (executive roles).

Identify the job family and read only the matching file: it holds the competencies and level expectations you need, and loading the others would only add noise. If the role spans two families (a CFO on the executive committee: finance and direction), read both and say which competency comes from which. If no family fits, say so in the deliverable and work from the brief alone rather than forcing one. If `references/` is not available (skill pasted without its folder), ask for the organisation's competency framework or proceed without it, and say so.

# Legal frame: publishing in France (checked 2026-10-16)

Read this section whenever the job description is meant to be published or sent to a job board. A posting is a public statement by the employer, so the rules apply to the wording itself.

| Rule | What it imposes on the posting | Source |
|---|---|---|
| C. trav. L1132-1 | No one may be set aside from a recruitment procedure because of origin, sex, age, family situation, pregnancy, health, disability, physical appearance, surname, **place of residence**, bank domiciliation, or ability to express oneself in a language other than French (among other listed grounds). | Légifrance |
| C. trav. L1133-1 | A difference of treatment is allowed only for an essential and determining occupational requirement, with a legitimate aim and a proportionate requirement. This is the test every "required" line must pass. | Légifrance |
| C. trav. L1142-1, 1° | A job offer may not mention the sex or the family situation of the candidate sought, in any form of advertising. | Légifrance |
| C. trav. L5331-2 | No upper age limit in a publicly distributed offer, unless the law itself sets an age condition. | Légifrance |
| C. trav. L5331-3 | No false or misleading statement in a publicly distributed offer, in particular on the job itself, the **pay and fringe benefits**, or the workplace. | Légifrance |
| C. trav. L5331-4 | A publicly distributed offer for work performed in France is written in French, even if good command of a foreign language is a condition of the job. A job title that has no French equivalent is described in French. A medium that itself publishes in a foreign language may receive offers in that language. | Légifrance |
| Directive (EU) 2023/970, art. 5 and 34 | Candidates are entitled to the initial pay or its range before the interview (a posting is one way); employers do not ask for pay history; postings and job titles must be non-gendered. Transposition was due on 7 June 2026. **State on 2026-10-16: not yet in French law** (government bill n° 944 filed in the Senate on 10 September 2026, accelerated procedure). Present it as "being transposed" and re-check. | EUR-Lex; Sénat |

Consequences for the writing:

- A pay range in the posting is **recommended** and will probably become compulsory; today it is not. Do not write that it is already required. Never ask for the candidate's current salary in a posting or an application form (art. 5(2) logic).
- Write the title and the text so they do not point to a sex (an epicene title, "your", the infinitive). "(H/F)" after a title is a usual way to show the offer is open to all; treat it as a custom, not as a legal requirement.
- Replace any residence requirement ("lives in Lyon") by what the job really needs: the area of intervention, the travel expected, the on-site days.
- If the user wants an English posting for a job in France, write the French text and offer an English version alongside it; whether a given platform falls under the last paragraph of art. L5331-4 is for the user to check.
- When a "required" line comes from a manager's preference (age bracket, sex, "young", residence), do not carry it over. Say which line you dropped and which article makes it risky.

Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check". A wrong article number looks authoritative and survives review.

Then check what the role (a regulated profession or a legal condition of access, night or safety-sensitive work, a posting on behalf of a client, an apprenticeship or a fixed-term contract) calls for beyond this list: a list focuses attention, and what it does not name gets missed. Mark what you add "to check" unless you can source it.

# Method

1. **Title and position.** Take the title from the brief; place the role in the organisation (team, reporting line).
2. **Mission** in 2 to 3 sentences: the outcome the role exists to produce.
3. **Responsibilities**: 5 to 8, written as outcomes the person owns ("owns the monthly closing and its quality"), not as tasks. A task list hides what matters and is out of date at the first reorganisation.
4. **Required and desirable competencies.** Use the domain reference to calibrate by level. Apply two tests to each line:
   - *Rejection test*: would we turn down a strong candidate who lacks it? If not, it is desirable. Each required line filters people out; an unjustified one can also be discriminatory (L1133-1). A degree is required only if experience cannot replace it.
   - *Checkable test*: can it be checked on a CV or in an interview? "Strong leader" cannot; "has led a team of three or more" can. Rewrite or cut the vague ones.
5. **Context**: team, reporting line, decision scope, working mode, location and travel (stated as requirements of the job, not of the person).
6. **Pay**, if the brief gives it: reproduce the figures given, fixed and variable separately, and the conditions of the variable ("up to" a ceiling that depends on targets is said so, L5331-3). Without figures, omit the section: "competitive" or "depending on profile" is not a range and informs no one. Never invent a figure.
7. **Success criteria** at 6 and 12 months if the brief allows.
8. **Points to clarify** before publication: separate what is stable in the role from what is still to be confirmed with the manager, and list the legal changes you made to the manager's wishes.

Defaults: 400 to 700 words for a posting (shorter reads thin, longer loses candidates); avoid "rockstar", "ninja" and similar words that signal a culture rather than a job; match the tone to the organisation (start-up, large group, non-profit) in a few words.

<example>
Manager's line: "autonomous and rigorous".
Rewritten as desirable: "has run a monthly closing alone, with reconciliations checked by a second person".
Why it works: it can be verified on a CV or by one interview question, and it describes a behaviour rather than a personality trait, so it does not filter on temperament.
</example>

# Expected output format

This is the default format; an explicit request from the user wins. Output name kept: `job_description`.

1. **Synthesis for the hiring manager** (3 to 5 lines, not published): the role in one sentence, the lines changed for legal reasons, what is still to confirm, the decision asked.
2. **Publishable part**, in this order: title (epicene) and positioning (team, reporting line) / mission (2 to 3 sentences) / responsibilities (5 to 8 outcomes) / competencies as a table, columns competency / required or desirable / how it is checked (CV or interview) / work context (mode, location, travel) / pay (figures given, fixed and variable apart, or the section omitted) / success criteria at 6 and 12 months.
3. **Not published**, after a separator: table of points to clarify, columns point / fact or to confirm / who decides / by when; table of lines changed, columns manager's line / change / rule behind it.
4. A field the brief does not give stays in brackets (`[to confirm]`), so that the manager fills it in rather than the model inventing it.

# Definition of done

- The document can be published in France as it stands: no line points to an age, a sex, a residence or a family situation, the language is French, and no pay statement is invented or misleading.
- Every required line passes the rejection test and the checkable test.
- Responsibilities are 5 to 8 outcomes, not a task list.
- Stable expectations and expectations still to be confirmed are told apart, and the grey areas are listed.

<!-- Rejection test for "required" lines, "checkable on a resume" rule, "pay is a number or a band, otherwise omit the section", length and wording hygiene adapted from anthropics/knowledge-work-plugins, small-business/skills/job-post-builder/SKILL.md (L99-103) and reference/job-post-structure.md (L32-40, L53-59) (Apache-2.0, commit 33eeda1): rewritten and fitted to French law (L1133-1, L5331-3, L5331-4, epicene wording). See THIRD_PARTY.md. -->
