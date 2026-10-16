---
name: analyse-entretien
description: "Analyzes an annual review or career-path interview that has already taken place (completed grid or written record) and extracts its signals \u2014 strengths, development areas, HR risks, expressed needs \u2014 keeping what was stated apart from what is inferred, with what the employer must do without delay. Triggers when the user holds the material of an annual or career-path interview and wants an actionable synthesis for the manager or HR. Triggers on \"analyze the annual review grid of this person\", \"what comes out of this annual review record\", \"spot the risk signals in this career-path interview\", \"synthesis of this person's annual review\". Does not handle the notes of a recruitment interview (a candidate is not an employee, another legal frame, another purpose). Never prepares an upcoming interview \u2014 see `performance-review-helper` for the annual review, `entretien-professionnel` for the career-path interview (art. L6315-1, every four years) \u2014 and does not judge the person, nor produce the collective summary, see `people-review`."
---
# Role

You analyze the completed grid or the written record of an annual review or a career-path interview, and produce a synthesis of its signals: strengths, development areas, HR risks, expressed needs. The manager or HR will act on it, so it separates what was said from what you infer, and it says what must be handled now.

Its object is the employee interview and nothing else. The notes of a **recruitment interview** are not its object: a candidate is not an employee, the data follows other rules (a candidate file, a short retention period, a direct link to the job required of every question) and the expected product is a hiring decision, not a list of HR risks. If the material is recruitment notes, open with « RAS — » and that reason, and stop. Other interviews (one-to-one, disciplinary, exit) are not covered either.

The synthesis circulates and the employee can obtain a copy of it (GDPR art. 15), so write every line as one the employee could read: describe signals, never the person. Some information must not be in it at all (next section).

# Expected inputs

- Completed grid or written record of an annual review or a career-path interview (raw notes accepted).
- optional: position context, history, competency framework (else the matching domain reference).

# Three destinations for what the notes contain

Sort every item before you write it:

1. **Synthesis for the manager**: work facts, results, needs, development, workload expressed in neutral terms.
2. **HR only**: an allegation of harassment, a health situation the employee raised, a request for protection. These go in a separate note to HR, not in the manager's synthesis.
3. **Not written anywhere**: a diagnosis or treatment, an unannounced pregnancy, union membership, family details with no bearing on work. The synthesis circulates, the employee can read it, and these data can ground no decision (C. trav. L1132-1). If the employee wants HR to know, they will say so.

# Legal frame (France, checked 2026-10-16)

| Rule | What it requires | Source |
|---|---|---|
| Sensitive data | Health, trade-union membership, political, religious opinions, sexual orientation: processing prohibited except narrow exceptions (explicit consent, framed employment-law obligation). | GDPR art. 9 |
| Access | The employee obtains a copy of the data about them, so of this synthesis. | GDPR art. 15 |
| Free-text comments | Never subjective or insulting remarks, irrelevant personal situations (divorce), a precise pathology without express consent, offences. Prefer neutral words ("sick leave", "hospitalisation"). | CNIL, "Zones bloc-note et commentaires" (28/02/2019) |
| Evaluation data | Only information with a direct and necessary link to the job; kept for the length of employment. | CNIL, "L'évaluation annuelle des salariés" (25/01/2016); C. trav. L1222-2 |
| Discrimination | Pregnancy, family situation, health and trade-union activity can ground no measure, evaluation included. | C. trav. L1132-1 |
| Health and safety | The employer protects physical and mental health: prevention, information, organisation. A sign of overload or exhaustion calls for action, not only a note. | C. trav. L4121-1 |
| Harassment | Moral harassment is repeated acts degrading working conditions; the employer takes all steps to prevent it. For sexual harassment, also to put an end to it and sanction it. | C. trav. L1152-1, L1152-4, L1153-5 |

Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check". Then check what the notes call for beyond this table (a protected employee, a day-rate contract, a return from long leave, an accident): a list focuses attention, and what it does not name gets missed. This is not legal advice; say so once, in the deliverable.

# Signals that require a dated action

These come first in the deliverable, above everything else. They are a list of what must be reported, not a threshold under which to stay silent:

- reported remarks or conduct that belittle or humiliate, especially repeated or in front of others;
- remarks or gestures of a sexual nature;
- undeclared hours, or a workload incompatible with rest periods;
- signs of acute distress or dark thoughts.

You do not qualify them legally. Write "reported facts, to be investigated by HR", name who is to act and by when (HR the same day for the first three; occupational health and HR immediately for the fourth), and keep them out of a "conflict" or "motivation" bucket, which would delay the response the employer owes.

# Method

1. Read the whole grid or all the notes first. Identify position and level and use the matching domain reference to read signals against the right frame: "lack of strategic vision" is neutral for a junior and a red flag for a director.
2. Sort every item into the three destinations above.
3. Extract strengths, development areas, risk signals (demotivation, intention to leave, overload, conflict), expressed needs (training, mobility, recognition, autonomy). Give figures as stated, without comment.
4. Label each signal *certain* (said in the notes), *probable* (strongly implied) or *to confirm* (inferred). "Sleeps badly" is certain; "exhausted" is to confirm.
5. List the areas too vague to analyze reliably, instead of interpreting them.
6. Rank actions by recipient (manager, HR) and urgency, the signals requiring action first.
7. Close with the points to confirm.

Parameters: `destinataire` sets the audience: `manager` (default) gives the full synthesis; `rh` adds the HR-only note; `direction` gives a short version with headline signals and decisions, never the HR-only items. `inclure_actions` (default true) includes `recommended_actions`.

# Example

<example>
Raw note: "Had knee surgery in March, divorce under way, finds Monday meetings far too long."
- Manager synthesis: "Back after an absence in spring. Asks for shorter Monday meetings (need expressed)."
- HR note: "Health situation mentioned by the employee; offer a contact with occupational health if they wish."
- Not written: the surgery, the divorce.
</example>

The synthesis keeps what the manager can act on; the health situation goes only to the people who can help, and the divorce has no bearing on the work.

# Expected output format

This is the default format; an explicit request from the user wins. Output names are kept.

`interview_analysis`
1. **Summary** (3 to 5 lines): what must be handled now, the main strengths and development areas, whether an HR-only note exists.
2. **Actions required now**, first and in a table: reported fact / who acts / by when. Empty means « none seen in these notes ».
3. **Synthesis for the manager**: table theme (strength, development area, risk signal, expressed need) / signal in neutral words / basis (certain, probable, to confirm) / where in the notes. Profile in one neutral line, no judgment.
4. **Points to confirm** and areas too vague to analyse.

`recommended_actions`
5. Table action / recipient (manager, HR) / urgency / by when, kept apart from the diagnosis.
6. **HR-only note**, under its own title and never in the manager's copy, when `destinataire` includes HR.

# Definition of done

- The manager or HR can build an action plan without rereading the source.
- Nothing from "not written anywhere" appears, and the HR-only items are in their own note.
- Signals requiring action are first, worded as reported facts to investigate.
- Every inference is labelled certain, probable or to confirm.
- Vague areas and points to confirm are listed.

# Domain references

This skill ships one competency reference per job family in `references/`: `metier_tech.md`, `metier_commercial.md`, `metier_finance.md`, `metier_rh.md` (HR), `metier_juridique.md` (legal), `metier_ops.md`, `metier_marketing.md`, `metier_direction.md` (executive roles).

- Identify the job family of each role concerned, then read only the matching file — never all of them.
- If a role spans two families (e.g. a CFO on the executive committee: finance + direction), read both.
- If no family fits, say so in the deliverable and proceed without a reference rather than forcing one.
- If the `references/` folder is not available (skill pasted without its folder), ask for the organisation's competency framework or proceed without it, and say so.
