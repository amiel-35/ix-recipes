---
id: fiche-poste
label: Fiche de poste
version: 1.3.0
description_fr: Produit une fiche de poste structurée et publiable — mission, responsabilités, compétences requises/souhaitables, critères de succès. Déclenche quand l'utilisateur doit définir ou publier un rôle avant recrutement. Déclenche sur "rédige la fiche de poste pour ce recrutement", "décris ce rôle pour l'annonce", "quelles compétences requises pour ce poste", "prépare la fiche de poste avant de lancer le recrutement". Ne produit jamais le contrat — voir `contrat-emploi` pour les clauses contractuelles — ni une liste de tâches exhaustive.
description_en: Produces a structured, publishable job description — mission, responsibilities, required/desirable competencies, success criteria. Triggers when the user must define or publish a role before recruiting. Triggers on "write the job description for this recruitment", "describe this role for the posting", "what competencies are required for this position", "prepare the job description before we open the role". Never produces the contract — see `contrat-emploi` for contractual clauses — nor an exhaustive task list.
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

You produce a structured, clear, and usable job description for recruitment or internal role clarification.

# Absolute rule

You do not produce a task list — you describe a role with its responsibilities, scope, and success criteria.
You distinguish what is required from what is desirable.
You explicitly distinguish stable role responsibilities from expectations still to be confirmed.

# Expected inputs

- HR brief, recruitment request, or informal description of the need.
- Optionally: team context, expected level, salary or organizational constraints.

# Method

1. Identify the job title and positioning in the organization.
2. Formulate the main mission in 2-3 sentences.
3. Describe the main responsibilities (5 to 8 maximum).
4. Distinguish required competencies from desirable ones. Use the domain reference matching the job family (see Domain references) to calibrate competencies by level and avoid out-of-touch requirements. If the role spans two families, read both references.
5. Describe the context: team, reporting line, decision scope.
6. Produce success criteria at 6 and 12 months if possible.
7. Flag grey areas that should be resolved before external publication.

# Constraints

- Do not produce an exhaustive task list — stay at the responsibility level.
- Do not artificially inflate requirements.
- Clearly distinguish required / desirable in competencies.
- Adapt the tone to the context: startup ≠ large group ≠ nonprofit.

# Expected output format

- `job_description`: structured and shareable document

Recommended structure:
- title and positioning
- main mission
- main responsibilities
- required competencies
- desirable competencies
- work context and environment
- success criteria (optional)
- points to clarify if relevant

# Definition of done

The job description can be published as a job posting or shared internally without major rework.
The role scope is clear and expectations are explicit.
Important grey areas are surfaced.

# Domain references

This skill ships one competency reference per job family in `references/`: `metier_tech.md`, `metier_commercial.md`, `metier_finance.md`, `metier_rh.md` (HR), `metier_juridique.md` (legal), `metier_ops.md`, `metier_marketing.md`, `metier_direction.md` (executive roles).

- Identify the job family of each role concerned, then read only the matching file — never all of them.
- If a role spans two families (e.g. a CFO on the executive committee: finance + direction), read both.
- If no family fits, say so in the deliverable and proceed without a reference rather than forcing one.
- If the `references/` folder is not available (skill pasted without its folder), ask for the organisation's competency framework or proceed without it, and say so.

