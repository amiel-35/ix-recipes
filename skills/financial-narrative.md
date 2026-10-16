---
id: financial-narrative
label: Narrative financiere
version: 1.3.0
description_fr: Transforme des chiffres financiers bruts (résultats, budget, trésorerie) en récit clair et hiérarchisé pour une direction ou un board. Déclenche sur "raconte ces chiffres au board", "prépare le narratif financier du comité", "transforme ce tableau de résultats en note pour la direction", "qu'est-ce qu'on retient de ces chiffres trimestriels". Se limite aux chiffres financiers pour une audience exécutive ; pour définir les indicateurs à suivre, utiliser `tableau-de-bord-kpi`.
description_en: Transforms raw financial figures — results, budget, cash — into a clear, prioritized narrative for an executive or board audience. Triggers on "tell the board what these numbers mean", "draft the financial narrative for the committee", "turn this P&L into a note for leadership", "what should we take away from this quarter's figures". Limited to financial figures for an executive audience; to define which metrics to track use `tableau-de-bord-kpi`.
icon: ◈
domain: finance
category: production
input_types:
- markdown
- reference
- brief
output_types:
- narrative_financiere
- messages_cles
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
---

# Role

You turn financial tables into the narrative an executive team or a board reads before a meeting. The reader sees the first lines, repeats the message to others and rarely goes back to the table, so the order of the messages and the honesty of the lead matter more than completeness. A board that finds a hidden variance on its own stops believing the rest of the document.

Each key message carries four things: the source figure, the comparison, the proposed reading and a confidence level (confirmed, probable, hypothesis). A reader then knows what to repeat as fact and what to ask about.

# What makes this hard

- **Wrong comparison**: revenue up on last year and below budget is two different stories; telling only one misleads.
- **Percent of a percent**: a margin falling from 42 % to 40 % is −2 points, not −4.8 %; the second is read as a revenue drop.
- **Exceptional items**: the board knows that "one-off" items tend to return, so a restated figure alone looks like window dressing.
- **Profit and cash told as one story** when they diverge.
- **A table read aloud**: the reader has the table; the narrative must add the order of importance and the why.

# Rules for reading the figures

- **Comparisons**: budget measures performance, forecast measures steering, last year shows the trend. Say which you use. When they point in different directions (above last year, below budget), both go into the main message.
- **Rates in points**: write margin and rate changes in points (or basis points), never as a percentage of the rate.
- **Margin variance**: when revenue and the margin rate are given, split the margin variance into a volume effect (revenue variance × budget rate) and a rate effect (rate variance × actual revenue). The two add up to the total margin variance exactly; recompute before writing. If the data does not allow it, say so.
- **Non-recurring items**: show the published figure and the restated figure side by side, name and quantify the item removed, and label the restated one "restated". Do not open on the restated figure alone.
- **Profit versus cash**: when EBITDA and the change in cash diverge, quantify the gap and give the explanation the source supports (working capital, investment, tax, debt service). If the source does not explain it, say the gap is unexplained and name the items to ask for.
- **Offsetting items**: a headline variance read without what offsets it points to the wrong cause. If costs are under budget while the result is short, say so.
- **Undocumented variations**: write "cause not documented in the source", with the question and who to ask, instead of an explanation of your own.

# Method

1. **Choose the messages.** Take the variance that changes a decision first. If it is a deterioration, it opens the narrative, quantified; at most three messages lead.
2. **Fix the comparisons** and compute the variances and the rates in points; recompute each derived figure.
3. **Write each key message** with its four parts. Mark every reading that is not in the source as an interpretation or a hypothesis.
4. **Explain** variations with documented causes first, then list the undocumented ones as questions.
5. **Situate** the outlook only from what the source gives (guidance, pipeline, committed costs); otherwise label it a hypothesis.
6. **List** the areas where the figures lack context.

# Parameters

- `audience`: `direction` (default) reads for a management team that knows the business; `board` uses shorter messages, avoids operational vocabulary and states the decisions or risks that concern directors; `codir` adds function-level detail; `managerial` focuses on the reader's own lines, causes and actions.
- `longueur`: `flash` gives the key messages only, as a spoken update; `standard` (default) adds a short narrative (situation, evolution, factors, outlook); `detaillee` adds line detail, the margin decomposition and an annex of source figures.

# Example

<example>
Q2 revenue 6.0 M€, budget 6.3, last year 5.5. Gross margin 55 % against 57 % budget.

Weak: "Revenue grows by 9 %."

Better: "Revenue is 6.0 M€: 0.3 M€ (4.8 %) under budget, although up 9.1 % on last year. Gross margin is 2 points under budget at 55 %: of the 0.29 M€ margin shortfall, 0.17 M€ comes from lower revenue (−0.3 × 57 %) and 0.12 M€ from the lower rate (−2 points × 6.0). The source does not say why the rate fell; question for the sales director (discounting, product mix?). Figures confirmed, reading hypothesis."

Why this is right: it opens on the variance that matters for a board, gives both comparisons, states margin in points, splits the shortfall into two parts that add up (0.171 + 0.120 = 0.291), and does not invent the cause.
</example>

# Expected output format

Default format; an explicit request from the user comes first.

- Head, 3 to 5 lines: the verdict against budget and against last year, the main variance quantified, the decision or question put to the reader.
- Key messages, three at most: message / source figure / comparison / proposed reading / confidence.
- Figures table: line / actual / budget / last year / variance vs budget (amount, %) / variance vs last year (amount, %) / rates in points.
- Published and restated figures side by side, the non-recurring item named and quantified.
- Narrative: situation, evolution, explanatory factors, outlook; messages before details.
- Margin variance split into volume and rate effects, with the check that they add up, when the data allows.
- Questions to ask: undocumented variation / question / who answers.
- Closing lists: established facts, proposed interpretations, areas without enough context.

Output names: `financial_narrative` (the text) and `key_messages` (the messages table).

# Definition of done

- The narrative leads with at most three messages, the main variance first and quantified, whether favorable or not.
- Comparisons are named, rates are in points, non-recurring items are shown both ways, a divergence between profit and cash is addressed.
- Each reading beyond the source is marked, and the closing lists are filled.

<!-- Narrative elements, anti-patterns and comparison guidance adapted from anthropics/knowledge-work-plugins, finance/skills/variance-analysis/SKILL.md (Apache-2.0, commit 33eeda1), and the basis-point convention from finance/skills/financial-statements/SKILL.md: rewritten and checked on numerical examples; the margin decomposition is derived and verified here. See THIRD_PARTY.md. -->
