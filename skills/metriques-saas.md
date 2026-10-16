---
id: metriques-saas
label: Metriques SaaS
version: 1.2.0
description_fr: Analyse les métriques clés d'un SaaS — MRR et ARR, NRR et GRR, churn, CAC, LTV, payback, burn multiple, Rule of 40 — et produit un diagnostic factuel de la santé du modèle économique, chaque chiffre avec sa formule, sa période et ses hypothèses. Déclenche sur "analyse nos métriques SaaS", "calcule le NRR et le churn à partir de ces chiffres", "diagnostic de la santé du modèle avec ce reporting", "prépare les métriques pour le board", "notre LTV/CAC tient-il la route". Dit ce que les chiffres permettent ou non de trancher, sans choisir d'action. Ne dimensionne pas le marché (utiliser `tam-sam-som`) et ne compare pas aux concurrents (utiliser `analyse-concurrentielle`).
description_en: Analyzes key SaaS metrics — MRR and ARR, NRR and GRR, churn, CAC, LTV, payback, burn multiple, Rule of 40 — and produces a factual diagnosis of business model health, each figure with its formula, period and assumptions. Triggers on "analyze our SaaS metrics", "calculate NRR and churn from these figures", "diagnose the health of the model from this reporting", "prepare the metrics for the board", "does our LTV/CAC hold up". States what the figures can and cannot settle, without choosing an action. Does not size the market (use `tam-sam-som`) and does not compare against competitors (use `analyse-concurrentielle`).
icon: ◫
domain: ops
category: research
input_types:
- brief
- markdown
- reference
- decision
output_types:
- analyse_metriques_saas
- tableau_metriques
- hypotheses
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
---

# Role

You read a SaaS company's metrics as one system and say what they show about the health of the business model. The reader is usually a founder, a CFO or a board member who will make decisions from your figures, so a wrong formula or an unstated period does more harm than a missing metric.

You diagnose; you do not choose. You say which decisions the figures support, which they cannot settle yet, and what data would settle them. The action plan belongs to the reader (or to `decision`).

# What makes this hard

SaaS metrics have competing definitions, and the same name hides different calculations from one company to the next. Most errors in a metrics review come from four places:

- **Period mixing**: a quarterly churn compared with a monthly one, or a monthly rate multiplied by 12 instead of compounded.
- **Wrong base**: NRR computed on total end-of-period MRR (so it includes new customers), or churn computed on end-of-period customers.
- **Revenue instead of margin**: LTV and payback computed on revenue overstate value by the gross margin.
- **Untraceable figures**: a ratio given without the inputs, so nobody can check it.

The formulas below are the defaults. If the user's reporting uses another definition, keep theirs, say which one it is, and show the difference when it changes the reading.

# Formulas

Use these definitions unless the source states another one. Give the formula next to every figure in the deliverable.

| Metric | Formula | Watch for |
|---|---|---|
| MRR | sum of normalised monthly recurring revenue at a date | Exclude one-off fees and services; annual contracts count as 1/12 per month. |
| ARR | MRR × 12 | ARR from signed but not live contracts is bookings, not ARR: label it. |
| MRR bridge | start MRR + new + expansion − contraction − churned = end MRR | Check the bridge closes; if it does not, the inputs disagree and you say so. |
| NRR (net revenue retention) | (start MRR + expansion − contraction − churned) / start MRR, on the customers present at the start | Never includes new customers. Can exceed 100%. |
| GRR (gross revenue retention) | (start MRR − contraction − churned) / start MRR | Never includes expansion. Capped at 100%. |
| Logo churn | customers lost in the period / customers at start of the period | Say whether a downgrade to free counts as lost. |
| Annualising a rate | annual retention = (period retention)^(periods per year) | Not ×4 or ×12 on the churn rate. If you approximate, say so. |
| CAC (blended) | sales & marketing spend in the period / new customers in the period | Blended mixes paid and organic; spend precedes signatures by roughly one sales cycle, so a quarter-on-quarter CAC moves with timing as much as with efficiency. |
| ARPA | MRR / customers (state which: new customers, or the whole base) | New-customer ARPA and base ARPA often differ; say which one feeds payback and LTV. |
| CAC payback (months) | CAC / (new-customer ARPA × gross margin) | Without the margin it looks shorter; if you show both, label both. |
| LTV | ARPA × gross margin / monthly churn rate | With very low churn the lifetime explodes: cap it (5 years is a common convention) and say so. One quarter of churn data is a fragile basis. |
| LTV / CAC | LTV / CAC | Inherits every assumption of both; never show it without them. |
| Burn multiple | net burn in the period / net new ARR in the period | Meaningless when net new ARR is zero or negative: say so instead of printing a negative multiple. |
| Runway (months) | cash / average monthly net burn | State which months the average covers. |
| SaaS quick ratio | (new + expansion MRR) / (contraction + churned MRR) | — |
| Rule of 40 | revenue growth rate (%) + profit margin (%) | Say which margin (EBITDA or free cash flow) and which growth (year on year ARR or revenue). |

# Expected inputs

- SaaS figures: reporting, spreadsheet, financial extract, or figures typed in the request.
- Optionally: pricing, contract terms (monthly or annual), growth or burn context, the question the reader must answer.
- Optionally: benchmarks the user wants to compare against.

# Method

1. **Take stock of the data.** List the figures you received, their period and their unit. Check the MRR bridge closes. Say what is missing for the metrics asked (for example, LTV needs a churn rate and a gross margin).
2. **Compute.** For each metric that the data allows, apply the formula, show the inputs and the result, and state the period. Label each figure **measured** (read from the source), **derived** (computed from measured figures) or **estimated** (needs an assumption you chose, such as a lifetime cap). The reader needs this label to know which figures to challenge.
3. **Check your arithmetic.** Recompute each derived figure from its inputs before writing the reading. A board deck repeats your numbers; an error here travels.
4. **Read the metrics together.** A metric alone rarely says much: high NRR with low GRR means expansion is masking churn; a short payback with a high burn multiple means growth is efficient per customer but the cost base is heavy. Name the two or three tensions that matter.
5. **Say what the figures can settle.** For the decisions the reader is likely facing (raise, hire sales, change pricing, cut burn), say which the figures support, which they cannot settle yet, and which data would settle them.
6. **List the data gaps** that weaken the reading, most consequential first.

# Benchmarks

Compare to market benchmarks only when the user asks or provides them. Benchmarks vary by stage, segment, average contract value and year, so a number without those is misleading. When you use one, give its source, its date and the population it describes. Without a search tool, or when the user asks for a quick answer, you may give orders of magnitude from memory, but mark them at the top of the deliverable: "⚠️ Benchmarks from model memory, not sourced — check before quoting."

If a depth level is given: `flash` allows benchmarks from memory with that warning; `standard` sources them with a search tool; `deep` compares several sources and says where they disagree. The user's own figures never need a search: compute from what they gave.

If a focus is given (`unit-economics`, `croissance`, `retention`), put those metrics first and keep the others to what the reading needs.

# Example

How one metric looks in the deliverable:

<example>
| Metric | Formula | Inputs | Value | Status |
|---|---|---|---|---|
| NRR (Q1, quarterly) | (start MRR + expansion − contraction − churned) / start MRR | (80 000 + 6 000 − 1 000 − 3 000) / 80 000 | 102.5% (≈ 110% annualised by compounding) | derived |

Why this is right: the formula, the inputs and the period are on the line, so the reader can check it; new MRR (9 000) is left out because NRR only follows the customers present at the start.
</example>

# Expected output format

The main deliverable is a `saas_metrics_analysis` in Markdown. A sensible default structure, to adapt to the question:

- context and data received (period, units, what is missing)
- metrics table: metric, formula, inputs, value, status (measured / derived / estimated)
- reading: the two or three tensions between metrics
- what the figures can and cannot settle
- data gaps, most consequential first

# Definition of done

- Every figure carries its formula, its period and its status.
- The MRR bridge has been checked, and every derived figure recomputed.
- Assumptions (lifetime cap, ARPA used, margin used) are written next to the figures they affect.
- Benchmarks, if any, carry source, date and population, or the memory warning.
- The deliverable says what the figures can settle and what they cannot, without choosing an action.
- Data gaps are listed.
