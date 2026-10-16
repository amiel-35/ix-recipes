---
skill: metriques-saas
famille: finance
ecrit: 2026-10-16
---

# Cas 1 — diagnostic trimestriel avant un board

## Demande

> Voilà nos chiffres du T3 2026 (B2B SaaS, abonnements mensuels). Fais-moi un diagnostic de la santé du modèle : NRR, churn, CAC, LTV, payback, burn multiple. Le board est dans 10 jours.
>
> - MRR au 1er juillet : 200 000 €
> - Nouveau MRR (T3) : 30 000 €
> - Expansion : 12 000 € ; contraction : 4 000 € ; MRR perdu (churn) : 10 000 €
> - MRR au 30 septembre : 228 000 €
> - Clients : 400 au 1er juillet, 50 nouveaux, 20 perdus, 430 au 30 septembre
> - Dépenses sales & marketing T3 : 450 000 €
> - Marge brute : 78 %
> - Burn net T3 : 600 000 € ; trésorerie au 30 septembre : 4,2 M€

## Valeurs de référence (calculées à la main)

| Métrique | Formule | Valeur |
|---|---|---|
| NRR trimestriel | (MRR début + expansion − contraction − churn) / MRR début | 198 / 200 = **99 %** (annualisé par composition ≈ 96 %) |
| GRR trimestriel | (MRR début − contraction − churn) / MRR début | 186 / 200 = **93 %** (≈ 75 % annualisé) |
| Churn clients | perdus / clients début | 20 / 400 = **5 %** sur le trimestre (≈ 1,7 %/mois) |
| CAC mixte | dépenses S&M / nouveaux clients | 450 000 / 50 = **9 000 €** |
| MRR moyen d'un nouveau client | nouveau MRR / nouveaux clients | 600 € |
| Payback CAC (marge brute) | CAC / (MRR nouveau client × marge brute) | 9 000 / 468 ≈ **19 mois** (≈ 15 mois sans la marge) |
| LTV | ARPA × marge brute / churn mensuel | ≈ 530 × 0,78 / 0,0167 ≈ **25 k€** (hypothèses à dire) ; LTV/CAC ≈ 2,8 |
| Net new ARR | (MRR fin − MRR début) × 12 | 336 000 € |
| Burn multiple | burn net / net new ARR | 600 / 336 ≈ **1,8** |
| Runway | trésorerie / burn mensuel | 4,2 M€ / 200 k€ ≈ **21 mois** |

## Une bonne sortie contient

1. La formule de chaque métrique donnée, pas seulement le résultat.
2. Un NRR de 99 % sur le trimestre, sans y inclure le nouveau MRR (erreur fréquente : 228 / 200 = 114 %), et un GRR de 93 %.
3. La période de chaque taux (trimestriel, mensuel ou annualisé), et l'annualisation faite par composition ou signalée comme approximative.
4. Un CAC de 9 000 €, dit « mixte » (toutes dépenses S&M, sans distinguer les canaux) avec le décalage entre dépense et signature signalé.
5. Un payback calculé sur la marge brute (≈ 19 mois), ou bien les deux versions avec la différence expliquée.
6. Une LTV dont les hypothèses sont écrites (ARPA retenu, churn retenu, marge), avec sa fragilité dite : un seul trimestre de churn.
7. Un burn multiple ≈ 1,8 et la runway ≈ 21 mois.
8. La distinction mesuré (mouvements de MRR) / dérivé (NRR, CAC, burn multiple) / estimé (LTV).
9. Les trous de données : cohortes, ventilation du CAC par canal, part annuel / mensuel, définition du churn (date de résiliation ou de fin de contrat).
10. Aucun repère de marché présenté comme une norme sans source ni contexte.
11. Des implications pour les décisions du board (ce que ces chiffres permettent ou non de trancher), sans plan d'action choisi à la place du board.

## Une mauvaise sortie

- NRR à 114 %, ou NRR et GRR confondus.
- Payback ou LTV sans hypothèse écrite.
- « Un bon NRR est supérieur à 120 % » posé comme règle.

## Résultats

Notation à l'aveugle par un juge Opus (sorties anonymisées et mélangées), banc `claude -p` avec le seul skill en invite système, outil Lecture seulement.

| Date | Version | Modèle | Critères tenus (sur 11) | Note |
|---|---|---|---|---|
| 2026-10-16 | 1.1.0 | Sonnet 5.5 | 9 | Pas de ventilation du CAC par canal ni de définition du churn ; « implications » réduites à des questions, sans dire ce que les chiffres permettent de trancher. 0 erreur. |
| 2026-10-16 | 1.2.0 | Sonnet 5.5 | **11** | 0 erreur ; tous les calculs vérifiés. |
| 2026-10-16 | 1.1.0 | Haiku 5.5 | 1 | NRR par une formule fausse, burn multiple à 20x (au lieu de 1,8), pas de GRR ; 4 erreurs. |
| 2026-10-16 | 1.2.0 | Haiku 5.5 | 8 | Formules et périodes justes, mais 6 erreurs d'arithmétique ou d'interprétation (quick ratio, NRR et GRR mêlés dans un commentaire), repères non sourcés, plan d'action choisi. |

# Cas 2 — données incomplètes avant une levée (cas de contrôle)

## Demande

> On prépare notre levée. Calcule notre LTV/CAC et dis-moi si on est bons. ARR au 31/12/2025 : 1,2 M€ ; ARR au 30/09/2026 : 1,5 M€ (contrats annuels). Cette année on a signé 22 nouveaux clients. Budget marketing sur les 9 mois : 380 k€, plus 2 commerciaux à 70 k€ chargés par an chacun. Sur les 60 clients qu'on avait en janvier, 3 sont partis. On ne suit pas notre marge brute.

## Valeurs de référence

- Coût d'acquisition sur 9 mois : 380 k€ + 2 × 70 k€ × 9/12 = 485 k€ ; CAC ≈ 22 000 € (22 045 €).
- Churn clients : 3 / 60 = 5 % sur 9 mois (≈ 6,6 % sur 12 mois par composition).
- Croissance d'ARR : + 25 % sur 9 mois.

## Une bonne sortie contient

1. Le CAC qui inclut les salaires commerciaux au prorata des 9 mois (≈ 22 k€), avec la formule.
2. Le churn rapporté à sa période (9 mois), annualisé par composition ou signalé comme approximatif.
3. Le constat que sans marge brute, la LTV et le payback ne peuvent pas être calculés sur la marge : soit une hypothèse de marge écrite et signalée, soit un calcul sur le revenu étiqueté comme tel, soit les deux.
4. Le constat que le NRR ne peut pas être calculé (ni expansion ni contraction connues), sans l'inventer.
5. Une LTV/CAC présentée avec ses hypothèses et sa fragilité (un seul exercice partiel, 3 départs).
6. Pas de « vous êtes bons » sans base : des repères seulement avec source, ou marqués comme non sourcés.
7. La liste des données à réunir avant la levée (marge brute, cohortes, MRR mensuel, expansion).

## Résultats

| Date | Version | Modèle | Critères tenus (sur 7) | Note |
|---|---|---|---|---|
| 2026-10-16 | 1.1.0 | Sonnet 5.5 | 7 | 0 erreur. |
| 2026-10-16 | 1.2.0 | Sonnet 5.5 | 7 | 0 erreur ; NRR déclaré non calculable, « je ne peux pas dire si vous êtes bons ». |
| 2026-10-16 | 1.1.0 | Haiku 5.5 | 3 | NRR inventé, « vous êtes bons » sur repères non sourcés, faits inventés (montant de levée) ; 5 erreurs. |
| 2026-10-16 | 1.2.0 | Haiku 5.5 | 4 | NRR calculé en supposant l'expansion nulle (raisonnement circulaire), fragilité du churn niée ; 4 erreurs. |
