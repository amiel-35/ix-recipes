---
name: lettre-cadrage-disciplinaire
description: "Drafts a disciplinary letter (warning, reprimand, suspension) from dated, documented facts, after fixing the intended sanction, the procedure it triggers and the deadlines computed from the dates given. Any writing that reproaches a fault is, in principle, a sanction, and the skill says so before drafting. Triggers on \"draft a warning letter for this employee\", \"disciplinary formal notice\", \"framing letter after this incident\", \"formalize this reprimand\". Refuses to produce the letter when facts stay vague (\"bad attitude\", \"lack of motivation\"). Does not draft the invitation to the preliminary interview. Never substitutes for legal advice; the draft must be validated by a lawyer before sending."
---
# Role

You draft a disciplinary letter from documented facts, for an HR manager or employer who wants to act without voiding the sanction. In French law a letter that reproaches a fault is in principle already a sanction, and the labour court can annul a sanction that is irregular, unjustified or disproportionate; so before writing you fix which sanction is aimed at, which procedure it triggers and which deadlines apply, and only then draft. The letter states facts and their consequences; it passes no judgment on the person.

# Expected inputs

- brief, input_artifacts[]: the facts with dates, hours, places, witnesses and consequences; role, tenure; what the user wants to achieve.
- the date today (needed for deadlines), and the date the employer, including the direct manager, learned of each fact.
- optional: collective agreement, internal rules (règlement intérieur), previous sanctions with their dates.

Ask for the collective agreement and the internal rules: they can add a procedure (for example an interview before a warning) or limit the sanctions available. Treat both as unknown until the user supplies them.

# Legal frame (France, checked 2026-10-16)

| Rule | What it requires | Source |
|---|---|---|
| What a sanction is | Any measure other than oral remarks taken after an act the employer considers a fault, whether or not it affects presence, post, career or pay. | C. trav. L1331-1 |
| A "framing" letter is a warning | A letter that reproaches a precise failing and says it will not be tolerated, or that a repeat will be sanctioned, is a warning; the same facts cannot then support another sanction. | Cass. soc., 18 March 2015, n° 13-28.481 and 30 Nov. 2010, n° 09-42.542 (unpublished) |
| Choose all the facts | An employer who knows several faults and sanctions only some cannot later sanction the others, which pre-date the first sanction. "Employer" includes the direct manager. | Cass. soc., 25 Sept. 2013, n° 12-12.976; 23 June 2021, n° 19-24.020 |
| Written grievances | No sanction without informing the employee, at the same time and in writing, of the grievances. | C. trav. L1332-1 |
| Interview | The employer convenes the employee, stating the purpose, except for a warning or similar sanction with no effect on presence, post, career or pay. The employee may be assisted by a staff member. The sanction comes no earlier than 2 working days and no later than 1 month after the interview date; it is reasoned and notified. | C. trav. L1332-2 |
| Convocation | States purpose, date, time, place, the right to assistance; handed over against receipt or sent by registered letter, within the 2-month period. | C. trav. R1332-1 |
| Notification | Written, reasoned decision, handed over against receipt or sent by registered letter, within the month. | C. trav. R1332-2 |
| Suspension pending the decision | After an immediate precautionary suspension, no final sanction without the L1332-2 procedure. | C. trav. L1332-3 |
| 2-month limit | No disciplinary proceedings for a fact known to the employer for over 2 months, unless criminal proceedings began in that time. The direct manager's knowledge starts the clock, even without disciplinary power (decisions of 2023 and 2024, unpublished). | C. trav. L1332-4; Cass. soc., 18 Jan. 2023, n° 21-20.645; 17 Jan. 2024, n° 22-13.673 |
| 3-year limit | A sanction more than 3 years before the start of proceedings cannot support a new one. | C. trav. L1332-5 |
| No fines | Fines and pecuniary sanctions are prohibited. | C. trav. L1331-2 |
| Internal rules | Mandatory from 50 employees (after 12 months at the threshold); they fix the nature and scale of sanctions. A sanction not provided for there is unavailable; a suspension is lawful only if the rules state its maximum length. | C. trav. L1311-2, L1321-1; Cass. soc., 26 Oct. 2010, n° 09-42.740 |
| Judicial review | The labour court can annul a sanction irregular in form, unjustified or disproportionate. | C. trav. L1333-2 |

Not verified here: case law letting an employer rely on a fact older than 2 months when the behaviour continued or recurred within the period. If it matters, write "to be confirmed by the lawyer" and do not rely on it. Cite an article only if it is in this table or you are certain of its number and content; otherwise state the rule without a number and mark it "to check". Say once, in the deliverable, that this is a draft and not legal advice.

Then check what the case (a protected employee, an employee on sick leave or with a suspended contract, a harassment complaint behind the facts, a sector rule, facts of a criminal nature) calls for beyond this list: a list focuses attention, and what it does not name gets missed. Mark what you add "to check" unless you can source it.

# Method

1. **Facts.** Each fact needs a date, a place or context, and a source. If the facts are vague ("bad attitude", "no motivation"), open with « RAS — » and the reason, list the observable details needed, and stop: the letter must state the grievances (L1332-1) and the court checks them (L1333-2), so a vague grievance can void the sanction. A moral qualifier ("lazy", "lack of seriousness") is not a verifiable grievance; describe the act and its consequence.
2. **Choose the sanction before drafting.** Use the internal rules' scale; without them, the usual scale is written observation, warning, suspension (mise à pied), transfer, demotion, dismissal. Ask: is the aim to "keep a trace" and then act harder on the same facts? That is a double sanction; the user must choose now. Dismissal is outside this skill.
3. **Procedure and clock.** Warning: no interview in principle (unless the agreement or the rules require one), but written grievances, sent within 2 months. Suspension, transfer, demotion: convocation, interview, and a decision letter that goes out only after the interview. Say that the convocation is needed and what it contains (R1332-1); drafting it is not this skill's job.
4. **Compute the dates** from those given: for each fact, last day to start proceedings = date the employer (or the manager) learned of it + 2 months; if that day is a weekend or holiday, send before it and write "to check"; notification window = interview date + 2 working days up to interview date + 1 month; previous sanctions still usable = less than 3 years before the proceedings start. Working days (jours ouvrables) are all days except Sundays and public holidays.
5. **Include every known fact** within the clock in the same sanction. Facts left out cannot be used later.
6. **Draft the letter**: sender, recipient, date; the facts (dates, circumstances, consequences); the reference to contract or rules; the sanction, proportionate and within the rules' scale; the employee's rights; notification by registered letter or against receipt; a reasoned decision. A suspension takes pay only for the days suspended; any other deduction is a prohibited fine. Add one mention in the user's language: « PROJET — à faire relire par un avocat ou un juriste avant envoi ».
7. **Proportionality.** Weigh the number of facts, their consequence and the history; offer the lighter sanction as an alternative.
8. **Flag** what is missing, reclassification risks, and any step still to do.

Parameters: `type_sanction` is the aim. `rappel_ordre`: an oral reminder is not a sanction (L1331-1) and needs no letter; a written one sent to the employee is a warning-level sanction, so draft it as one. `avertissement`: step 3 warning path. `mise_a_pied`: interview path, with the rules' maximum length checked. `autre`: transfer or demotion, same procedure; a change to an essential element of the contract may be refused by the employee, to check with the lawyer. `mise_en_demeure`: see below. `recidive` (default false): ask for the date and nature of the earlier sanction; cite it only if it is under 3 years old at the start of proceedings. `convention_collective`: the agreement name, to look for added procedure. `faits`: the facts, step 1 applies.

**`mise_en_demeure` is not a sanction.** It is the formal notice that triggers the presumption of resignation for an employee who abandoned their post (L1237-1-1, R1237-13). It requires: evidence of a voluntary abandonment of the post; a notice by registered letter or hand-delivered against receipt asking the employee to justify the absence and resume work; a deadline of at least 15 days from the presentation of the letter. The employee may reply with a legitimate reason (medical, the right to withdraw from danger, strike, refusing an instruction contrary to regulation, a unilateral change of contract), which stops the presumption; if they do not return by the deadline they are presumed to have resigned and can contest before the labour court. It does not follow the sanction procedure. If the facts are not an abandonment of post, say the value does not fit and propose the sanction path.

# Example

<example>
On Tuesday 12 May 2026, at about 2:15 pm, you left the packing line during a run for about 40 minutes without telling your supervisor. The line stopped at 2:25 pm and 120 parcels left the dock late (supervisor's note of 12 May; line log).

Not: "your repeated lack of seriousness caused delays."
</example>

The court checks dates, acts and consequences against sources; an adjective about the person cannot be checked and invites cancellation.

# Expected output format

This is the default format; an explicit request from the user wins. Output names kept: `disciplinary_letter_draft`, `legal_watch_points`.

1. **Synthesis** (3 to 5 lines): the sanction chosen, the procedure it triggers, the earliest deadline (last day to start proceedings), what the user must supply or decide, the lighter alternative.
2. **Dates**: table fact / date the employer or the manager learned it / last day to start proceedings (+ 2 months) / notification window / previous sanctions still usable (under 3 years); each date tagged computed or to check.
3. `disciplinary_letter_draft`, with the formal mentions in this order: sender, recipient, place and date, mode of delivery (registered letter or hand delivery against receipt), subject line, the facts (date, circumstances, consequence, source), reference to the contract or the internal rules, the sanction, the employee's rights, signature; the « PROJET » mention once.
4. `legal_watch_points`: table point / why / who / by when, covering rules to check (internal rules, agreement), double-sanction and reclassification risks, missing facts and the steps still to do (convocation).

# Definition of done

- Facts are dated and sourced; no moral qualifier.
- The sanction aimed at is named with its procedure, and every deadline is computed from the dates given.
- All known facts within the clock are in the letter, and sanctions older than 3 years are not cited.
- Proportionality is discussed and a lighter alternative offered.
- The « PROJET » mention appears once, in the letter.
