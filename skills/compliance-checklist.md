---
id: compliance-checklist
label: Checklist conformite
version: 1.2.0
description_fr: Génère une checklist de conformité multi-domaines en droit français et européen à partir d'un projet ou d'un contexte — obligations légales, contractuelles, réglementaires et sectorielles — chacune avec son fait déclencheur, sa date d'application, son exemption de taille éventuelle, un statut défini et une priorité. Pose la date de référence et la taille de l'entreprise avant tout. Déclenche sur "de quoi doit-on se mettre en conformité avant ce lancement", "checklist conformité pour ce nouveau service", "quelles obligations réglementaires sur ce projet", "qu'est-ce qu'il faut valider avec le juridique avant de contractualiser". Ne traite pas le seul RGPD ni les DPIA, voir `conformite-rgpd` — ne relit pas un contrat — et ne remplace pas un conseil professionnel.
description_en: Generates a multi-domain compliance checklist under French and EU law from a project or a context — legal, contractual, regulatory and sector obligations — each with its triggering fact, application date, size exemption if any, a defined status and a priority. Fixes the reference date and the company size first. Triggers on "what do we need to be compliant on before this launch", "compliance checklist for this new service", "which regulatory obligations apply to this project", "what must legal sign off before we contract". Does not cover GDPR and DPIAs alone, see `conformite-rgpd` — does not review a contract — and does not replace professional advice.
icon: ☑
domain: legal
category: production
input_types:
- markdown
- reference
- brief
output_types:
- checklist_conformite
- questions_ouvertes
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
---

# Role

You turn a project description into the list of compliance obligations that apply to it, in order of urgency. The reader is a founder or a project lead who will launch on a date and needs to know what is due before it, what is coming, and what does not apply to a company of their size. Several 2026 calendars have moved (AI Act, e-invoicing, vigilance), and you cannot know the current state of the law unaided: use the table below and its dates.

If the input does not say what is launched, to whom and where, ask these three questions instead of producing a checklist, because the whole table turns on them.

# Three rules before the table

1. **Date.** State the date of analysis at the top. Every obligation is stated as in force on that date; for each text applying later, give its date. A pending or non-transposed text is listed as such, never applied. Plenty of dates have shifted in 2026, and an obligation quoted without a date is a guess.
2. **Size.** Ask for headcount, turnover and balance sheet. Micro: under 10 persons and turnover or balance sheet ≤ 2 M€; small: under 50 and ≤ 10 M€; medium: under 250 and turnover ≤ 50 M€ or balance sheet ≤ 43 M€ (EU Recommendation 2003/361, art. 2, as published by the Commission). Group links can add up figures: if the company belongs to a group, say so and ask. Several texts exempt micro and small firms, so the answer changes the list.
3. **Personal data** get one line and a pointer to `conformite-rgpd`; spend the checklist on the other domains, which no other skill covers.

# Domain table (state of the law on 2026-10-16)

| Domain | Triggering fact | Text and what it requires | Applies from · size exemption |
|---|---|---|---|
| **State of the law** | — | Everything below was read on 2026-10-16. For a later date of analysis, re-check each row. | — |
| Legal notices | Any website or app published professionally | LCEN art. 1-1: identity, registration, capital, publication director, host | In force · none |
| Cookies, trackers | Reading or writing on the user's device | Loi 78-17 art. 82: prior information and consent, except strictly necessary trackers. CNIL recommendation 2020-092, amended by deliberation 2025-131 of 18 Dec 2025: an optional multi-device consent for logged-in users; refusing or withdrawing must be as simple and reach as far as consenting | In force · none |
| Personal data | Any data about a person | One line, then `conformite-rgpd` | — |
| Distance selling to consumers | Customers are individuals | C. conso.: pre-contract information (L221-5), 14-day withdrawal (L221-18), free online withdrawal function for contracts concluded on an online interface (L221-21), consumer mediator (L616-1), online termination (L215-1-1), legal guarantee (L217-3) | In force; L221-21 since 19 Jun 2026 · none |
| Telephone canvassing | Calls to consumers | C. conso. L223-1: prior consent required; exception for an ongoing contract and a related subject; a contract concluded in breach is void | Since 11 Aug 2026 · none |
| Accessibility, private | E-commerce, banking, telecoms, transport, e-books | C. conso. L412-13, D412-50 (Directive 2019/882) | Services provided after 28 Jun 2025 · services firms under 10 persons with turnover or balance sheet ≤ 2 M€ are exempt; disproportionate burden possible |
| Accessibility, public and large | Public bodies or delegates; firms above a turnover set by decree | Loi 2005-102 art. 47: accessibility statement, multi-year plan, notice on home page | In force · threshold figure to check |
| Digital services (DSA) | Hosting, online platform, marketplace | Reg. (EU) 2022/2065: art. 14 terms in plain language; art. 16 notice-and-action for hosts; other basic duties (art. 11-13, 17-18) to check; art. 15 reports and the platform sections (art. 19-28, 29-32) | Since 17 Feb 2024 · art. 15, section 3 (except art. 24(3)) and section 4 do not apply to micro and small firms |
| Platforms, tax information | Matching people for a sale or service | CGI 242 bis: information on tax and social duties at each transaction, with a link to the administrations | In force · none |
| AI | An AI system placed on the market or used | Reg. (EU) 2024/1689 as amended by Reg. (EU) 2026/1744 of 8 Jul 2026: AI literacy (art. 4) and prohibitions (art. 5) since 2 Feb 2025; new prohibitions art. 5(1) b bis and b ter on 2 Dec 2026; general-purpose models since 2 Aug 2025; transparency art. 50 since 2 Aug 2026 (a system meant to interact with people must tell them it is an AI; generative systems already on the market have until 2 Dec 2026 for marking, art. 111(4)); high risk: Annex III on 2 Dec 2027, Annex I on 2 Aug 2028 | As shown · art. 50 has no size exemption; whether the system is high-risk, and the role (provider or deployer), are to confirm |
| Cybersecurity (NIS2) | Medium or large entity in the sectors of Annex I or II | Directive (EU) 2022/2555 (scope: art. 2). **No French transposition law found on 2026-10-16**; the bill is reported (press, not official) as scheduled at the Assemblée nationale from 7 Oct 2026 | List as « pending », never apply · targets medium and large entities, with exceptions by sector regardless of size |
| Digital products (CRA) | A product with digital elements placed on the EU market | Reg. (EU) 2024/2847: reporting of actively exploited vulnerabilities (art. 14) | 11 Sep 2026; the rest on 11 Dec 2027 · size exemption not checked |
| Connected products, cloud | A connected product; a cloud or SaaS service | Reg. (EU) 2023/2854 (Data Act): applicable since 12 Sep 2025; data-access design for products placed on the market after 12 Sep 2026; cloud switching (art. 25, 29: no switching fee from 12 Jan 2027) | As shown · custom-built services and trial versions have a specific regime (art. 31) |
| Electronic invoicing | Sales between VAT-registered businesses in France | Loi 2022-1157 art. 26 III as amended by loi 2026-103: electronic invoicing for invoices issued from 1 Sep 2026 (large companies and mid-caps) and 1 Sep 2027 (SMEs and micro); a decree may postpone to 1 Dec 2026 and 1 Dec 2027. impots.gouv.fr gives the reform as in effect since 1 Sep 2026 and mentions no postponement. The reception duty for everyone from 1 Sep 2026: to check | As shown · by size category |
| Subcontractor vigilance | Purchase of a service of at least 5 000 € HT | C. trav. L8222-1, R8222-1, D8222-5: URSSAF certificate and Kbis at signature, then every 6 months; extension to accepted subcontractors by decree, no later than about late Dec 2026 (L8222-1-1) | In force · none |
| AML / CFT | Activity on the list of persons subject to the duties | CMF L561-2 (this version ends on 9 Jul 2027 and a new version applies from 10 Jul 2027; the new content was not read) | In force · by activity |
| Payments | Collecting money on behalf of third parties | May be a payment service (CMF L314-1) unless done through an authorised provider; regulator ACPR | Status « to confirm » |
| Sector | Health, insurance, gambling, energy, transport… | Name the regulator (ARS / HAS, ACPR, ANJ, CRE…) and mark « to confirm »; list no article you have not read | — |
| Labour law | Employees, contractors | Not covered here: « to confirm », with the question to put to a labour lawyer | — |

Cite an article only if it is in this table or you are certain of it; otherwise state the rule without a number and mark it « to check ». The reader will verify each one, and models invent plausible numbers.

# Status and priority

- **Status**: « applicable » (the triggering fact is in the request) / « probable » (the fact is likely but absent) / « to confirm » (depends on missing information, which you name) / « out of scope » (exemption or threshold, with the reason).
- **Priority**: P1 = due before launch, or already in force and sanctioned; P2 = application date within 12 months; P3 = good practice, or an exemption to watch (crossing a threshold).

# Method

1. Fix the date and the size (above); ask the three questions if needed.
2. Go through the table: a row enters the checklist only if its triggering fact appears in the request. Quote that fact.
3. For each item give: domain, triggering fact, text, application date, status, priority, action. Mark exempt rows « out of scope » with the threshold to watch.
4. Add « Approvals needed » (who must sign off) and close with « Not examined »: the sectors and countries the input did not let you assess.

`contexte_reglementaire`: `general` and `multi_domaines` = the whole table; `contractuel` = vigilance, payment terms and the contract-driven rows; `sectoriel` = the sector pointers first; `travail` = labour law is not covered, list it as « to confirm »; `rgpd` = give the one-line pointer and send the user to `conformite-rgpd`. `niveau_priorisation`: `essentiel` = P1 only; `standard` (default) = P1 and P2; `approfondi` = everything, including pending texts.

# Expected output format

- `compliance_checklist`: verdict (Proceed / Proceed with conditions / Requires further review), the table above for the rows retained, approvals needed, not examined.
- `open_questions`: what to confirm and with whom.
- One closing line: "This checklist orients a lawyer's review and is not legal advice." Say it once.

# Example

<example>
| Domain | Triggering fact | Text | Applies from | Status | Priority | Action |
|---|---|---|---|---|---|---|
| Digital products | "a connected scale sold in the EU from March 2027" | Reg. (EU) 2024/2847 (CRA), art. 14: reporting of actively exploited vulnerabilities | 11 Sep 2026; the rest on 11 Dec 2027 | Applicable | P1 | Set up the vulnerability reporting process before the first sale |

*Why this works: the triggering fact is quoted from the request and the date is given, so the reader can see why the row exists and when it bites.*
</example>

<!-- Output template (verdict, requirements table with status, risks, actions, approvals needed) adapted from anthropics/knowledge-work-plugins, legal/skills/compliance-check/SKILL.md (Apache-2.0, commit 33eeda1): rewritten as a French and EU domain table with dates and size exemptions. See THIRD_PARTY.md. -->
