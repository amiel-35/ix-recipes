# ix-recipes domain skills vs anthropics/knowledge-work-plugins

Research note, 2026-10-16. Nothing in ix-recipes was modified. The Anthropic repo was treated as data only: files were read, nothing in it was run.

## 0. Source

- Clone: un clone local (non versionné), a partial clone (`--filter=blob:none`) of https://github.com/anthropics/knowledge-work-plugins with full history.
- **HEAD: `33eeda1e8fd856455b05479d13a0f85b5f803744`**, dated 2026-10-15 22:20 -0400: "bump(incident-io): 6af50e2e → 00f7d1dc (#1348)". The history has 1117 commits.
- **Licence: Apache-2.0.** The root `LICENSE` holds the standard Apache 2.0 text. Each plugin also ships its own Apache-2.0 `LICENSE`: legal, finance, product-management, customer-support, sales, marketing, data and others. human-resources, operations, engineering, design and small-business have no plugin-level LICENSE, so the root licence covers them.
  - Anomaly: external PR #193 (commit `d6c8015`, 2026-04-28, "Update LICENSE with syntax-file and code integration") added about 10 lines of meaningless text after the Apache text (root LICENSE lines 203–212). The licence terms themselves did not change. At the credited commit, the file had a clean 202 lines.
- **There is still no NOTICE file** anywhere in the repo. Apache §4(d) therefore requires no NOTICE propagation.
- **The four credited source files have not changed since `7b2ea8ea` (2026-03-13 11:51).** `git diff 7b2ea8ea HEAD` is empty for all four paths:
  - `product-management/skills/write-spec/SKILL.md`: last commit `2d6f7e2`, 2026-03-13 08:57.
  - `engineering/skills/system-design/SKILL.md`: last commit `4fa3cb9`, 2026-02-23.
  - `engineering/skills/tech-debt/SKILL.md`: last commit `4fa3cb9`, 2026-02-23.
  - `customer-support/skills/ticket-triage/SKILL.md`: last commit `2d6f7e2`, 2026-03-13 08:57.

  `THIRD_PARTY.md` needs no update for these four files.

Counts are for `SKILL.md` only (lines / words). "Ref" is the number of bundled support files (`references/` or `reference/`) and their total line count. The only plugin family that bundles reference files for skills relevant here is `small-business` (folder `reference/`, singular). The HR, legal, finance, PM, ops, engineering and support plugins ship a single SKILL.md each.

## 1. The 47 skills and their closest equivalents

ix counts are for the whole `skills/<id>.md`, frontmatter included. "P" = partial overlap only.

| # | ix skill | ix L/W | Closest KWP skill(s) | KWP L/W | Ref |
|---|---|---|---|---|---|
| 1 | analyse-entretien | 86/711 | none. P: `human-resources/skills/interview-prep` (debrief template only) | 37/196 | 0 |
| 2 | contrat-emploi | 71/513 | `human-resources/skills/draft-offer`; P: `small-business/skills/job-post-builder` (`reference/offer-letter-template.md`, US at-will) | 82/364; 204/1645 | 0; 8 files/672 L |
| 3 | entretien-professionnel | 85/719 | none (French statutory interview) | — | — |
| 4 | fiche-poste | 85/607 | `small-business/skills/job-post-builder` | 204/1645 | 8 files/672 L |
| 5 | grille-remuneration | 83/702 | `human-resources/skills/comp-analysis` | 92/485 | 0 |
| 6 | interview-guide-recruteur | 196/1753 | `human-resources/skills/interview-prep`; `job-post-builder/reference/interview-guide-structure.md` | 37/196; 93 L | 0 |
| 7 | interview-loop-planner | 354/2645 | P: `interview-prep`, `job-post-builder/reference/role-intake.md` (default stage maps), `human-resources/skills/recruiting-pipeline` | 37/196; 73 L; 31/177 | 0 |
| 8 | lettre-cadrage-disciplinaire | 74/651 | none | — | — |
| 9 | offboarding-structure | 84/701 | none | — | — |
| 10 | onboarding-plan | 84/686 | `human-resources/skills/onboarding` | 104/555 | 0 |
| 11 | org-design-brief | 80/500 | `human-resources/skills/org-planning` | 28/197 | 0 |
| 12 | people-review | 87/735 | P: `human-resources/skills/performance-review` (calibration mode), `human-resources/skills/people-report` | 149/699; 99/405 | 0 |
| 13 | performance-review-helper | 84/659 | `human-resources/skills/performance-review` | 149/699 | 0 |
| 14 | plan-developpement-competences | 83/698 | none. P: development-plan table in `performance-review` (L89–92) | — | — |
| 15 | cgv-checker | 71/526 | `legal/skills/review-contract`; `small-business/skills/contract-review` | 358/2345; 158/1734 | 0; 5 files/324 L |
| 16 | compliance-checklist | 69/473 | `legal/skills/compliance-check`; `operations/skills/compliance-tracking` | 274/2109; 44/224 | 0 |
| 17 | conformite-rgpd | 89/2012 | `legal/skills/compliance-check` (GDPR, DPA art. 28 and DSR sections, L66–240) | 274/2109 | 0 |
| 18 | contrat-fournisseur | 69/436 | `legal/skills/review-contract`; `small-business/skills/contract-review`; P: `legal/skills/vendor-check` (agreement status only) | 358/2345; 158/1734; 159/857 | 0; 5/324 L; 0 |
| 19 | legal-risk-flag | 87/639 | `legal/skills/legal-risk-assessment` | 265/1787 | 0 |
| 20 | nda-draft | 67/482 | `legal/skills/triage-nda` (triage, not drafting) | 262/2122 | 0 |
| 21 | budget-variance-analysis | 84/489 | `finance/skills/variance-analysis` | 266/1634 | 0 |
| 22 | business-case-draft | 84/504 | none for internal investment. P: `sales/skills/close-plan` (customer-facing ROI case) | 106/1378 | 0 |
| 23 | financial-narrative | 81/505 | `finance/skills/variance-analysis` (narrative part); `finance/skills/financial-statements` | 266/1634; 335/1865 | 0 |
| 24 | metriques-saas | 79/442 | P: `product-management/skills/metrics-review`; `marketing/skills/performance-report` (CAC, payback, L226–240). No SaaS unit-economics skill | 388/2805; 392/2978 | 0 |
| 25 | tableau-de-bord-kpi | 83/534 | `product-management/skills/metrics-review` (dashboard design, L319–375); P: `data/skills/build-dashboard` (HTML build) | 388/2805; 924/2705 | 0 |
| 26 | tam-sam-som | 80/462 | none | — | — |
| 27 | total-cost-analysis | 90/542 | `operations/skills/vendor-review` (TCO section) | 104/460 | 0 |
| 28 | analyse-cdc | 80/537 | P: `small-business/skills/grant-rfp-writer` (go/no-go on solicitations) | 162/2102 | 5 files/605 L |
| 29 | analyse-concurrentielle | 79/443 | `product-management/skills/competitive-brief`; `marketing/skills/competitive-brief`; `sales/skills/competitive-intelligence` | 302/2169; 331/1999; 102/1340 | 0 |
| 30 | negotiation-brief | 83/507 | none on the buy side. P: `legal/skills/meeting-briefing`, negotiation tiers in `review-contract` (L281–306) | 220/1334 | 0 |
| 31 | offer-comparison | 90/578 | `operations/skills/vendor-review` (comparison matrix) | 104/460 | 0 |
| 32 | offre-commerciale | 110/680 | `small-business/skills/proposal-builder`; P: `sales/skills/create-an-asset` | 168/2514; 105/1337 | 5 files/695 L; 0 |
| 33 | rfp-draft | 81/483 | none (no buyer-side RFP skill) | — | — |
| 34 | strategie-prix | 77/439 | none. P: pricing-model mention in PM `competitive-brief` | — | — |
| 35 | vendor-scorecard | 77/449 | `operations/skills/vendor-review` | 104/460 | 0 |
| 36 | note-strategique | 76/433 | none. P: `product-management/skills/stakeholder-update`, `engineering/skills/architecture` (ADR) | 352/2328; 85/355 | 0 |
| 37 | feature-spec | 91/528 | `product-management/skills/write-spec` (credited source) | 250/1985 | 0 |
| 38 | journey-map | 78/474 | none. P: one line in `design/skills/user-research` | 41/265 | 0 |
| 39 | mockup | 70/409 | none. P: `design/skills/design-handoff`, `design-critique` | 131/584; 118/595 | 0 |
| 40 | okr | 162/1341 | P: `product-management/skills/metrics-review` (OKR section, L235–273); `roadmap-update` | 388/2805; 266/1924 | 0 |
| 41 | persona | 76/455 | `product-management/skills/synthesize-research` (persona section, L225+); `design/skills/research-synthesis` | 312/2363; 92/432 | 0 |
| 42 | prd | 85/497 | `product-management/skills/write-spec` | 250/1985 | 0 |
| 43 | product-spec | 104/588 | `write-spec`; P: `design/skills/design-handoff` | 250/1985; 131/584 | 0 |
| 44 | reformulation-us | 75/464 | P: `write-spec` (user stories and acceptance criteria, L137–152, L194–220) | 250/1985 | 0 |
| 45 | system-design | 75/452 | `engineering/skills/system-design` (credited); `engineering/skills/architecture` | **42/191**; 85/355 | 0 |
| 46 | tech-debt | 76/574 | `engineering/skills/tech-debt` (credited) | **32/223** | 0 |
| 47 | ticket-triage | 80/442 | `customer-support/skills/ticket-triage` (credited) | 275/1734 | 0 |

How long the Anthropic skills are depends on the plugin:

- **HR, operations, engineering and design are as short as ix or shorter.** Examples: HR `org-planning` 28 lines, `interview-prep` 37, `recruiting-pipeline` 31; engineering `tech-debt` 32, `system-design` 42; `operations/vendor-review` 104.
- **Legal, finance, customer-support and product-management run 250–450 lines.**
- **Sales and small-business run about 100–200 lines but 1,300–2,800 words each**, plus `reference/` folders. Their length is mostly connector plumbing.
- **No KWP equivalent at all for 11 ix skills:** entretien-professionnel, lettre-cadrage-disciplinaire, offboarding-structure, plan-developpement-competences, tam-sam-som, strategie-prix, rfp-draft, negotiation-brief, journey-map, mockup, note-strategique. Several more have only partial matches.
- **The ix skills that use `references: [metier_*]` (12 HR skills) load 427–898 words of a competency partial on top of the body.** The Anthropic HR skills have nothing comparable.

## 2. What the extra length is made of: 9 pairs read in full

Categories:

- **K**: domain knowledge Claude would plausibly get wrong or omit (thresholds, legal rules, formulas, definitions, checklists).
- **W**: worked examples or templates of the output.
- **P**: process or workflow steps.
- **C**: connector or tool instructions specific to Claude products.
- **F**: filler, meaning things Claude already knows, generic advice or repetition.

Shares are rough estimates by line count.

### 2.1 Support: `ticket-triage` (ix 80 L) vs `customer-support/skills/ticket-triage` (275 L, credited source)

**Share: K ≈ 35%, W ≈ 33%, P ≈ 16%, C ≈ 7%, F ≈ 9%.**

- **K:**
  - Category taxonomy with signal words (L103–117).
  - Category tips, e.g. "root cause drives the category" (L119–126).
  - P1–P4 criteria **with SLA expectations** (1 h, 4 h, 1 business day, 2 business days; L128–168).
  - Triggers for bumping priority up (L170–177).
  - Routing table by tier (L179–190).
- **W:**
  - Triage output template (L61–91).
  - Five first-response templates, one per category (L207–265).
- **P:** workflow (L25–59), duplicate-detection steps (L192–205).
- **C:** `~~support platform`, `~~knowledge base`, `/customer-escalation` (L9, L49–51, L93–99).
- **F:** usage examples (L13–23); "best practices" (L267–275) mostly repeat the workflow.

ix kept the four one-line priority definitions and the "escalate when in doubt" rule (ix L54–58). Everything else was condensed away.

**Real gains for ix:**
- SLA per priority as a stated default to replace with the organisation's own (L138, 148, 158, 168).
- Priority bump triggers (L170–177).
- Category tips (L119–126).
- Routing table (L179–190).
- First-response templates (L207–265, especially the Bug and Security ones).

### 2.2 HR: `performance-review-helper` (ix 84 L + metier partial) vs `human-resources/skills/performance-review` (149 L)

**Share: W ≈ 70%, F ≈ 10%, C ≈ 8%, P ≈ 7%, K ≈ 3%.**

- **W:** three full templates: self-assessment (L29–60), manager review (L62–96), calibration prep (L98–132).
- **K:** only the target rating distribution, about 15–20% / 60–70% / 10–15% (L109–114). That is a US forced-distribution norm, so treat it with care.
- **C:** `~~HRIS`, `~~project tracker` (L134–142).
- **F:** four tips (L144–149), e.g. "be specific", "behaviours not personality".

ix already covers this through its method and the `metier_*` level grids, which Anthropic does not have.

**Possible gain:**
- The self-assessment template (L31–60) as an optional second deliverable.
- The calibration-prep table (L100–132), which `people-review` lacks.

### 2.3 Legal: `nda-draft` (ix 67 L) vs `legal/skills/triage-nda` (262 L)

**Share: K ≈ 63%, W ≈ 15%, P ≈ 13%, F ≈ 6%, C ≈ 2%.** This is the densest knowledge file of the nine.

- **K:**
  - Default positions when no playbook is configured: mutual; 2–3 years, up to 5 for trade secrets; the 4–5 standard carve-outs; no non-solicit, non-compete or residuals (L45–54).
  - A 10-section screening checklist covering definition scope, oral-disclosure marking (30 days), standard of care, carve-outs, permitted disclosures, term and survival (1–3 / 2–5 years), return and destruction with a retention exception, remedies, problematic provisions, and governing law (L56–119).
  - GREEN/YELLOW/RED criteria (L121–175).
  - Five "common issue → standard position → redline approach" entries: overbroad definition, missing independent-development carve-out, non-solicit (fallback: targeted solicitation only, 12 months), residuals, perpetual term (L235–256).
- **W:** triage report template (L179–218).
- **P:** intake, playbook loading, routing table with timelines (L23–34, L220–233).

The ix skill has **no** domain content. It names the clause headings and adds the lawyer disclaimer.

**Real gains:**
- Default positions (L45–54).
- Carve-out list (L77–83).
- Problematic-provisions list (L107–114).
- Standard positions with redline approach (L235–256).

These suit both `nda-draft` and `legal-risk-flag`.

**Caveat, common-law flavour:**
- "No liquidated damages" (L104, L169) does not translate to France, where a clause pénale (art. 1231-5 C. civ.) is common and can be moderated by the judge.
- "Injunctive relief" maps to référé.
- "No mandatory arbitration" (L119) is a US preference.

Adapt these items before borrowing them; do not copy them as is.

### 2.4 Legal: `legal-risk-flag` (ix 87 L) vs `legal/skills/legal-risk-assessment` (265 L)

**Share: K ≈ 45%, W ≈ 28%, F ≈ 22%, P ≈ 5%, C 0.**

- **K:**
  - 5-level severity scale **anchored in % of deal value**: <1%, 1–5%, 5–25%, >25% (L18–26).
  - 5-level likelihood scale (L28–36).
  - Score = S×L with bands 1–4, 5–9, 10–15, 16–25 (L38–47).
  - Concrete examples at each level (L78–81, 98–102, 120–125, 145–151).
  - Outside-counsel triggers: mandatory, strongly recommended, consider (L230–254).
- **W:** 5×5 matrix (L49–61), risk memo template (L155–208), risk-register fields (L210–228).
- **F:** the "recommended actions" lists per colour (L72–76, 90–96, 111–118, 134–143) are generic management advice; "selecting outside counsel" (L256–265) is generic.

ix uses high/medium/low with no anchor.

**Real gains:**
- Severity anchors (L20–26).
- Examples per level (as above).
- Mandatory-escalation triggers (L234–239).

### 2.5 Legal: `contrat-fournisseur` + `cgv-checker` (ix 69 + 71 L) vs `legal/skills/review-contract` (358 L)

**Share: K ≈ 46%, P ≈ 24%, W ≈ 14%, F ≈ 11%, C ≈ 4%.**

- **K:**
  - Table of 12 clause categories with review points (L71–86).
  - Per-clause "elements to review / common issues" for limitation of liability, indemnification, IP, data protection (72 h, SCCs), term and termination (auto-renewal notice windows), and governing law (L90–192).
  - GREEN/YELLOW/RED with **numeric examples**, e.g. cap at 6 vs 12 months of fees, 60 vs 90-day renewal notice (L198–240).
  - 3-tier negotiation priorities with the rule "trade Tier 3 to secure Tier 2, never concede Tier 1 without escalation" (L281–306).
- **W:** redline format with **Fallback** and Priority fields (L261–271); review summary template (L317–352).
- **P:** context questions: which side, deadline, focus, deal (L34–43); review order: read the whole contract first, because clauses interact (L61–69).
- **C:** CLM routing via MCP (L308–315).
- **F:** redline "best practices" (L250–259) are partly generic; disclaimers.

**Real gains:**
- Clause guidance (L90–192), split by reading side.
- Numeric GREEN/YELLOW examples (L202–216).
- Negotiation tiers (L281–306), also usable by `negotiation-brief`.
- Redline format with fallback (L263–271).

**Neither side has the French rules a French CGV or supplier review needs:**
- Mandatory CGV content and pénalités de retard (C. com. L441-1, L441-10, with the €40 flat indemnity).
- Payment terms of 60 days, or 45 days end of month (L441-10).
- Déséquilibre significatif (L442-1).
- The B2C blacklist and greylist (C. conso. R212-1/-2).
- Brutal termination of an established relationship (L442-1 II).

That knowledge has to be written for ix. KWP does not supply it.

### 2.6 Finance: `budget-variance-analysis` (ix 84 L) vs `finance/skills/variance-analysis` (266 L)

**Share: K ≈ 64%, W ≈ 26%, F ≈ 8%, P ≈ 2%, C 0.**

- **K:**
  - Price/volume decomposition formula with a worked example (L15–44).
  - Rate/mix with a margin example (L46–60).
  - Headcount/compensation decomposition into headcount, rate, mix, timing and attrition (L62–75).
  - OpEx decomposition by cost behaviour (L77–91).
  - Materiality: 1–5% of a benchmark; trigger table of 10% vs budget, 15% vs prior, 5% vs forecast, 20% MoM; 0.5–1% of revenue in absolute terms (L93–113).
  - Investigation priority order (L115–123).
  - When to compare against budget, forecast or prior (L233–239).
  - Forecast accuracy and MAPE (L241–256).
  - How to read variance trends, e.g. sandbagging (L258–266).
- **W:**
  - Per-variance narrative template (L127–139).
  - Narrative quality checklist and **anti-patterns** (L141–159).
  - Text waterfall (L177–196) and bridge reconciliation table (L198–212).
  - Three-way comparison table (L225–231).

ix names the variance types (volume, price, mix, timing) but has no formula, threshold or narrative standard.

**Real gains:** two-way decomposition (L19–29, L38–44), headcount decomposition (L66–75), materiality table (L104–113), narrative anti-patterns (L152–159), waterfall with the reconciliation check (L169–175, L198–212). These also fit `financial-narrative`.

**Caveat, a defect in the source:** the "three-way decomposition" formulas (L31–36) do not reconcile. For a single product they leave out the (ΔP×ΔV) interaction term. Do not copy them.

### 2.7 Procurement: `vendor-scorecard` + `total-cost-analysis` (ix 77 + 90 L) vs `operations/skills/vendor-review` (104 L)

**Share: W ≈ 38%, F ≈ 25%, P ≈ 15%, K ≈ 10%, C ≈ 10%.**

- **W:** output template with cost table (Year 1 / 3-year), risk table, recommendation and negotiation points (L51–88).
- **K/F:** checklists for TCO, risk and performance (L27–46) that Claude mostly knows. The only items arguably worth adding are concentration risk and BCP/DR (L37, L39).
- **C:** `~~knowledge base`, `~~procurement` (L90–98).

The ix pair is already more rigorous: confirmed/estimated/unquantified costs, sensitivity, and hypotheses that invert the ranking. **No meaningful gap.**

### 2.8 Product: `prd` + `feature-spec` (ix 85 + 91 L) vs `product-management/skills/write-spec` (250 L, credited source)

**Share: F ≈ 43%, P ≈ 24%, K ≈ 20%, C ≈ 7%, W ≈ 6%.** This is the filler-heaviest of the nine.

- **F:**
  - Section-by-section PRD guidance that restates the section list (L77–136).
  - INVEST (L137–145), MoSCoW (L154–160) and the Given/When/Then definition (L196–201). Claude knows all of these well.
  - Closing tips (L240–250).
- **P:** conversational intake (L19–37), review loop (L70–75).
- **C:** `~~project tracker`, `~~knowledge base`, `~~design` (L39–55).
- **K:**
  - The P0 test question (L115).
  - P2 framed as "architectural insurance" (L119, L166).
  - User-story anti-patterns (L147–152).
  - Lists of leading and lagging indicators (L168–185).
  - **Target-setting rules**: success threshold plus stretch, measurement method, evaluation date (L187–192).
  - Acceptance-criteria tips, including negative cases and banned vague words (L215–220).
  - Scope-creep signals and countermeasures, e.g. "every addition comes with a removal" (L222–238).
- **W:** the SSO user stories and acceptance-criteria examples (L108–111, L203–213).

**Real gains:**
- Target-setting rules (L187–192) for `feature-spec`, `prd` and `okr`.
- User-story anti-patterns (L147–152) for `reformulation-us`.
- Acceptance-criteria tips (L215–220).
- Scope-creep countermeasures (L232–238).

### 2.9 HR recruiting: `fiche-poste` + `interview-guide-recruteur` (ix 85 + 196 L) vs `small-business/skills/job-post-builder` (204 L + `reference/` 672 L) and `human-resources/skills/interview-prep` (37 L)

**Share in `job-post-builder` SKILL.md: C ≈ 35%, P ≈ 30%, K ≈ 12%, F/safety ≈ 13%, W ≈ 10%.**

- **C:** DocuSign browser flow, Drive/M365 search, the docx skill, house artifact style, closing-offer router, build-connector (L38–52, L65–86, L153–171, L179–205).
- **K (SKILL.md):**
  - Every required line must be checkable from a résumé; pay is a band or the section is omitted (L96–103).
  - Each competency belongs to one stage; 1/3/5 anchors written per role; separate résumé-screening rubric weighted to 100 (L118–130).
- **Reference files** (the K/W lives here):
  - `job-post-structure.md`: 7-part structure, the required-line test "would we reject a strong candidate without this?" (L34–35), 400–700-word target (L59).
  - `interview-guide-structure.md`: stage map, 1/3/5 anchor example (L69–75), debrief rule "scores shared before discussion" (L79).
  - `role-intake.md`: default stage maps for companies under 25 people and for larger ones (L56–73).
  - `gotchas.md`, mostly connector-related.
  - `offer-letter-template.md`: US at-will and 401(k) terms.
  - `examples/worked-example.md`.
- `interview-prep` (37 L) is a thin outline. ix `interview-guide-recruteur` is far richer: STAR, weighted 1–4 grid with thresholds, graduated red flags, anti-bias partial.

**Real gains for `fiche-poste`:**
- The required-qualification test (`job-post-structure.md` L34–35) plus "checkable from a résumé" (SKILL.md L100–101).
- The length target (L59).
- The rule that pay is a figure or nothing (SKILL.md L102–103).

**Gap on both sides:** French recruitment law. Questions must have a direct link to the job (C. trav. L1221-6) and discrimination criteria are banned (L1132-1).

### 2.10 Other pairs, not read in full but checked

**Tech** (`engineering/system-design` 42 L, `engineering/tech-debt` 32 L): ix is the superset.

- ix `tech-debt` keeps the formula (Impact+Risk)×(6−Effort) and adds horizon thresholds (≥28 / 15–27 / <15).
- It drops only the category→risk column (KWP L12–19).

**`product-management/metrics-review`**, for `okr` and `tableau-de-bord-kpi`:

- OKR grading 0–0.3 / 0.4–0.6 / 0.7–1.0 and 70% as the stretch norm (L260–266).
- Target-setting inputs: baseline, benchmark, trajectory, effort, confidence (L268–273).
- Dashboard design principles, layout and **anti-patterns** (L319–362).
- Alert hygiene (L363–375).
- North Star and L1/L2 hierarchy (L109–174).
- DAU/MAU stickiness thresholds of >0.5 and <0.2 (L186).

**`legal/compliance-check`:**

- DPA art. 28 checklist (L118–172), useful for `contrat-fournisseur`.
- DSR timelines table (L208–216). It says "30 days" for GDPR where art. 12(3) says one month, extendable by two.
- ix `conformite-rgpd` (2,012 words, article-level) is already denser on GDPR than KWP.

**`metriques-saas`:** no KWP skill gives the SaaS unit-economics formulas or benchmarks (NRR/GRR, LTV variants, CAC payback, Rule of 40). Only `marketing/performance-report` L234–235 defines CAC and payback in one line each. ix promises "formulas included" (L34, L68) but contains none, so this K has to come from elsewhere.

### Summary of the length question

| Plugin family | Where the length goes |
|---|---|
| legal, finance, customer-support | Mostly **K + W** (60–90%). Real reference content: default positions, thresholds, formulas, colour criteria with examples, templates. |
| product-management | A mix: **F** ≈ 40% (frameworks Claude knows), K ≈ 20%, P/C ≈ 30%. |
| HR, operations, engineering, design | **Short, W-heavy or thin.** ix is already as rich or richer, especially with the `metier_*` partials. |
| sales, small-business | Mostly **C** (CRM, DocuSign, Drive/M365, approval gates, chain routing) plus P. The domain K sits in `reference/` files. Little of it transfers. |

## 3. Writing style

Counts from a script over the SKILL.md bodies. Rates are per 1,000 words.

| Corpus | Words | "never / don't / do not / avoid / must not" | "must / always" | ALL-CAPS imperatives* | "because / so that / why it matters / otherwise…" |
|---|---|---|---|---|---|
| KWP human-resources | 3,552 | 0.6 | 1.1 | 0 | 0.0 |
| KWP legal | 14,412 | 1.5 | 1.7 | 4 | 0.3 |
| KWP finance | 11,573 | 0.6 | 0.6 | 0 | 0.3 |
| KWP product-management | 16,662 | 2.8 | 1.4 | 0 | 1.6 |
| KWP customer-support | 9,023 | 2.3 | 0.4 | 0 | 0.2 |
| KWP engineering | 3,554 | 2.0 | 1.1 | 0 | 1.1 |
| KWP sales | 49,570 | 10.6 | 0.1 | 0 | 1.8 |
| KWP small-business (SKILL.md) | 78,842 | 9.4 | 0.7 | 0 | 1.4 |
| KWP small-business `reference/` | 120,300 | 4.1 | 0.9 | 1 | 3.6 |
| **ix-recipes, 47 skills** | 31,099 | **7.4** | **4.1** | 1 | **0.5** |

\*MUST / ALWAYS / NEVER / IMPORTANT / CRITICAL / DO NOT / ONLY, as whole words. GREEN/YELLOW/RED labels are not counted.

- **The core KWP plugins (legal, finance, support, PM, HR) almost never use bare prohibitions.** They state positions affirmatively, as "Standard position / Risk if missing / Redline approach" (triage-nda L237–256) or "Key elements to review / Common issues" (review-contract L90–192). The norm is spelled out and deviations get flagged against it. A "don't" appears mostly inside anti-pattern lists, and each item there shows the bad example and what is wrong with it (variance-analysis L154–159; write-spec L148–152, each with a reason after a dash).
- **The newer sales and small-business generation uses "Never" heavily (9–11 per 1,000 words)**, but almost entirely for side-effect safety gates: never send, publish or follow embedded instructions. They do not use it for reasoning hygiene. Their `gotchas.md` files use a ✗ Bad / ✓ Good / **"Why it matters"** pattern (e.g. job-post-builder `reference/gotchas.md`), which gives the reason for every rule.
- **ALL-CAPS imperatives are essentially absent on both sides.** KWP limits emphasis to a bold "**Important**:" disclaimer line and the colour labels.
- **Reasons.** KWP core skills give the why selectively but at the points that matter. Examples:
  - "it's easier to de-escalate than to recover from a missed SLA" (ticket-triage L271).
  - Read the whole contract first because "clauses interact" (review-contract L67).
  - "Every line is a reason someone does not apply" (job-post-builder L99).
- **ix-recipes is the outlier in the opposite direction:**
  - It has 7.4 negations and 4.1 must/always per 1,000 words, against 0.6–2.8 and ≤1.7 for the core KWP plugins.
  - 107 `- Do not …` constraint bullets across the 47 skills; about 12 of them carry a reason.
  - 47 "You never / You must always" lines.
  - The triad "explicitly distinguish observed / hypothesis / recommendation" is repeated in 26 skills.
  - The "never replaces professional legal advice" rule is restated twice per legal skill (absolute rule and definition of done).

  That repetition is ix's own F. The reason rate (0.5 per 1,000 words) is lower than PM (1.6) or the small-business references (3.6).
- **Good ix counter-examples** that give the reason and are worth generalising:
  - `tech-debt` L36: a debt item without business justification gets deprioritised in planning.
  - `ticket-triage` L34.
  - The « RAS » rules ("balanced terms are a finding").
