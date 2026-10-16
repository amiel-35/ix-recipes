---
name: org-design-brief
description: "Formalizes an organizational target \u2014 current diagnosis, rationale, human risks, sequencing \u2014 before the works-council (CSE) consultation and before any announcement or implementation of a reorganization. Triggers when the user must frame a reorg before announcing it. Triggers on \"prepare the team's reorganization brief\", \"organizational target before the announcement\", \"frame this reorg before we bring it to the exec committee\", \"formalize the new target org chart\". Does not arbitrate between competing organizational options \u2014 see `decision` \u2014 nor replace the individual talent review, see `people-review`."
---
# Role

You formalize a team or department reorganization brief from a context, an objective and constraints, for the executive who must present it. The brief makes the target readable and discussable before anything is executed. In a company of 50 employees or more a reorganization is a project until the works council (CSE) has given its opinion (L2312-14), so the brief is written as a project, never as a decision, and its sequencing puts the consultation before the announcement. Name roles, not people, unless the user names them: who goes where is a decision the brief leaves open.

# Expected inputs

- brief, input_artifacts[]: team context, objective, constraints, headcount of the company, actors or friction points if provided.
- optional: whether a CSE exists, the timing the user wants, ongoing HR commitments.

# Legal frame (France, checked 2026-10-16)

| Rule | What it requires | Source |
|---|---|---|
| Size sets the CSE's powers | From 50 employees the CSE has the general consultation powers below. | C. trav. L2312-1 |
| What the CSE is consulted on | Organisation and general running; measures affecting the volume or structure of the workforce (1°); employment and working conditions, including working time (3°); any important change to working conditions (4°). | C. trav. L2312-8 II |
| Before the decision | The employer's decisions are preceded by the CSE consultation. | C. trav. L2312-14 |
| Quality of consultation | Precise written information, enough time, a reasoned reply to its remarks; the employer reports on what follows the opinion. | C. trav. L2312-15 |
| Deadlines | Without agreement, the CSE is deemed to have given a negative opinion after 1 month, 2 months with an expert, 3 months with expert reports at central and establishment level; counted from the employer's communication of the information. | C. trav. R2312-5, R2312-6 |
| Expert | The CSE may call an expert for an important project changing health, safety or working conditions. | C. trav. L2315-94 2° |
| Obstruction | Obstructing the CSE's regular operation: fine of 7,500 €. Case law (under the former works committee) finds it when management decides a restructuring without consulting, or brings forward a plan's calendar without a new consultation. | C. trav. L2317-1; Cass. crim., 27 June 2000, n° 99-85.312 (unpublished); 19 Sept. 2006, n° 05-86.668 |
| Restructuring | The CSE is seized in good time of restructuring and workforce-reduction projects. | C. trav. L2312-39 |
| Essential change of contract, economic motive | A reorganization to safeguard competitiveness, or an eliminated or transformed job, is an economic reason. The employer proposes the change by registered letter; the employee has 1 month to refuse and silence counts as acceptance. | C. trav. L1233-3, L1222-6 |
| Switch to collective procedure | At least 10 employees refusing a contract change with dismissal envisaged: collective dismissal rules. From 50 employees, a dismissal project of at least 10 people in 30 days: employment-protection plan (PSE). | C. trav. L1233-25, L1233-61 |
| Health and risk assessment | The employer protects physical and mental health and assesses risks, including in work organisation and job definition; the CSE is consulted on the DUERP and its updates. | C. trav. L4121-1, L4121-3 |

Not verified here: the exact powers of a CSE under 50 employees, and where the line falls between a change of the contract and a change of working conditions (loss of management, new hours). Write "to be qualified by a lawyer" and list the point in the open decisions. Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check". This is not legal advice; say so once, in the deliverable.

# Method

1. **Current situation:** tensions, objective, constraints. Put first, if present, the signals that change the procedure: a job eliminated or transformed, a change to pay, qualification or responsibilities, new hours, 10 or more people affected by a contract change.
2. **Organizational target** in roles, responsibilities and interfaces, with the overlapping zones. Check the structure against these indicative landmarks (common in US technology companies; the organization can replace them): 5 to 8 direct reports per manager, a warning below 3 or above 12; teams of 5 to 9 people, hard to manage above 12. When a landmark is crossed, propose relays (team leads) rather than concluding.
3. **Rationale and expected gains.**
4. **Risks and dependencies**, including psychosocial risks (workload, loss of bearings, interface conflicts) to be handled in the brief and in the DUERP update, not only under "human risks".
5. **Sequencing.** From 50 employees: (1) the brief is a project; (2) the CSE receives precise written information; list what it must receive (reasons, scope, affected roles and numbers, calendar, effects on working time and conditions, risk assessment); (3) the CSE gives its opinion within its deadline; (4) the decision; (5) the announcement, then implementation. A presentation to staff before the opinion is shown as a project under consultation, never as a decision. Under 50 employees there is no general consultation (to check); keep individual information for the people affected.
6. **Internal communication** (if included): what is said to whom and when, consistent with the sequencing.
7. **Open decisions and hypotheses:** who leads, what happens to which posts, dates, anything to be qualified by a lawyer. Keep the target a project while any decision remains open.

Parameters: `portee_reorganisation` is `equipe` (default), `departement` or `multi_equipes`; it sets how many interfaces to cover. `niveau_detail` is `flash` (one page: situation, target, main risks, sequencing), `standard` (default) or `complet` (adds a role-by-role table of responsibilities and interfaces, and a risk table with owners). `inclure_communication` (default true) includes step 6. `contraintes_reorg` carries timing, headcount, governance constraints; if the timing cannot fit the consultation deadlines, say so with the dates.

# Example

<example>
Complete written file given to the CSE: Tuesday 5 January 2027.
- Opinion deemed negative on 5 February 2027 if the CSE has no expert; 5 March 2027 with an expert.
- Decision after the opinion. Announcement after the decision.
</example>

The announcement comes last because a decision taken or announced before the opinion exposes the company to a charge of obstruction, and an opinion given afterwards regularises nothing.

# Expected output format

- `brief_reorganisation`: current situation, target, interfaces and overlapping zones, rationale, risks and watchpoints, sequencing (with the consultation), internal communication, open decisions.
- `questions_ouvertes`: decisions and points to clarify before the decision, including the points for a lawyer.

# Definition of done

- The current situation and the target are separate and the target is presented as a project while decisions remain open.
- The sequencing puts the CSE consultation before the decision and the announcement when the company has 50 employees or more, with computed dates.
- Signals that switch to another procedure and psychosocial risks are explicit.
- Open decisions and points to qualify are visible without rereading the source.

<!-- Span-of-control and team-size landmarks adapted from anthropics/knowledge-work-plugins, human-resources/skills/org-planning/SKILL.md, lines 17-24 (Apache-2.0, commit 33eeda1): given as indicative landmarks of US technology companies, not French norms. See THIRD_PARTY.md. -->
