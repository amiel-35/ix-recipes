---
skill: budget-variance-analysis
famille: finance
ecrit: 2026-10-16
---

# Cas 1 — clôture de septembre avant un comité

## Demande

> Clôture de septembre, on a un écart sur le trimestre. Analyse-moi ça pour le comité de lundi.
>
> Chiffre d'affaires T3 :
> - Produit Pro : budget 1 000 unités à 200 € ; réel 900 unités à 210 €
> - Produit Lite : budget 2 000 unités à 50 € ; réel 2 600 unités à 48 €
>
> Charges T3 (budget / réel) :
> - Marketing : 40 000 / 52 000 € (l'acompte de 10 000 € du salon de novembre a été payé en septembre)
> - Hébergement : 20 000 / 21 500 €
> - Salaires : 150 000 / 147 000 €
> - Déplacements : 5 000 / 7 500 €

## Valeurs de référence (calculées à la main, 2026-10-16)

| Élément | Valeur |
|---|---|
| CA budget / réel / écart | 300 000 / 313 800 / **+13 800 € favorable** |
| Effet volume (total, au prix moyen budget de 100 €) | (3 500 − 3 000) × 100 = **+50 000** |
| Effet mix | Pro : (900 − 1 166,7) × 200 = −53 333 ; Lite : (2 600 − 2 333,3) × 50 = +13 333 ; **−40 000** |
| Effet prix | 900 × 10 + 2 600 × (−2) = **+3 800** |
| Bouclage | 50 000 − 40 000 + 3 800 = 13 800 |
| Par produit (deux termes) | Pro : volume −20 000, prix +9 000 (−11 000) ; Lite : volume +30 000, prix −5 200 (+24 800) |
| Seuil absolu à 1 % du CA réel | ≈ 3 138 € |
| Marketing | +12 000 (+30 %), défavorable, significatif ; dont 10 000 de calendrier (salon de novembre), 2 000 non expliqués |
| Hébergement | +1 500 (+7,5 %), sous les deux seuils |
| Salaires | −3 000 (−2 %), favorable, sous le seuil relatif |
| Déplacements | +2 500 (+50 %) : au-dessus du seuil relatif, sous l'absolu ; une ligne, sans analyse de cause, avec la règle annoncée |

## Une bonne sortie contient

1. Un écart de CA de +13 800 € décomposé en volume, mix et prix dont la somme boucle, avec les formules.
2. L'effet mix nommé (≈ −40 000 €) : le volume total monte mais se déplace vers Lite, moins cher.
3. La convention retenue pour l'interaction prix × volume (rangée dans l'effet prix, ou séparée et nommée).
4. Le seuil de matérialité annoncé avec sa raison, et le traitement des déplacements cohérent avec ce seuil (une ligne, sans analyse).
5. Le marketing ventilé : 10 000 € de calendrier (le salon, qui se compensera en novembre) et 2 000 € non expliqués, marqués à vérifier.
6. Les sens favorable / défavorable corrects sur les charges (dépassement = défavorable), la convention dite en tête.
7. Aucune cause inventée à la baisse de volume de Pro ni à la baisse de prix de Lite : hypothèses marquées, ou questions aux responsables.
8. Un pont budget → réel qui boucle, avec la ligne de contrôle écrite.
9. Aucun commentaire circulaire ou « divers » sur un écart significatif.
10. Chaque action reliée à un écart ; faits établis, hypothèses et points à vérifier en listes séparées.

## Une mauvaise sortie

- Une décomposition « volume / prix » qui ne boucle pas, ou qui ignore le mix.
- « Marketing en dépassement de 12 000 € » sans voir que 10 000 € sont du calendrier.
- Hébergement ou salaires commentés longuement alors qu'ils sont sous le seuil.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 10) | Note |
|---|---|---|---|---|
| 2026-10-16 | 1.1.0 | Sonnet 5.5 | 4.3 (4–5) | banc 3 passages, moyenne (min–max) ; erreurs relevées 0.0 (0–0) |
| 2026-10-16 | 1.2.0 | Sonnet 5.5 | **8.7 (8–9)** | banc 3 passages ; erreurs 1.3 (0–4) |
| 2026-10-16 | 1.1.0 | Haiku 5.5 | 3.0 (2–4) | banc 3 passages, moyenne (min–max) ; erreurs relevées 7.0 (4–9) |
| 2026-10-16 | 1.2.0 | Haiku 5.5 | **7.0 (6–8)** | banc 3 passages ; erreurs 4.7 (2–7) |

# Cas 3 — Écarts du troisième trimestre d'un fabricant (contrôle indépendant)

Écrit le 2026-10-16 sans voir le corps du skill, à partir de sa seule description.

## Demande

> On est un fabricant de mobilier de jardin en aluminium (PME, 45 salariés). Le comité de direction veut comprendre pourquoi le résultat du T3 2026 (juillet à septembre) est sous le budget alors que « les charges sont tenues ». Voici le budget et le réalisé du trimestre, en euros HT :
>
> | Ligne | Budget T3 | Réel T3 |
> |---|---|---|
> | Unités vendues | 10 000 | 9 000 |
> | Chiffre d'affaires | 1 200 000 | 1 147 500 |
> | Achats matières (aluminium, quincaillerie) | 480 000 | 459 000 |
> | Transport sur ventes | 60 000 | 63 000 |
> | Personnel | 300 000 | 318 000 |
> | Loyer | 45 000 | 45 000 |
> | Marketing | 40 000 | 22 000 |
> | Honoraires | 15 000 | 27 000 |
> | Résultat | 260 000 | 213 500 |
>
> Ce que je sais : on a augmenté nos prix de vente de 7,50 € par unité au 1er juillet pour répercuter la hausse de l'aluminium. Le salon professionnel prévu en septembre a été reporté à la mi-octobre. Dans les honoraires, il y a une facture d'avocat de 12 000 € pour le litige avec un distributeur. Pour le personnel et le transport, je n'ai pas d'explication. Le budget a été construit avec 120 € de prix de vente, 48 € de matières et 6 € de transport par unité.

## Valeurs de référence

| Ligne | Budget | Réel | Écart | Budget flexible (9 000 u.) | Écart réel / flexible |
|---|---|---|---|---|---|
| Chiffre d'affaires | 1 200 000 | 1 147 500 | −52 500 (−4,4 %) | 1 080 000 | +67 500 (effet prix) |
| Matières | 480 000 | 459 000 | −21 000 | 432 000 | +27 000 défavorable |
| Transport | 60 000 | 63 000 | +3 000 | 54 000 | +9 000 défavorable |
| Personnel | 300 000 | 318 000 | +18 000 | 300 000 | +18 000 défavorable |
| Loyer | 45 000 | 45 000 | 0 | 45 000 | 0 |
| Marketing | 40 000 | 22 000 | −18 000 | 40 000 | −18 000 (décalage) |
| Honoraires | 15 000 | 27 000 | +12 000 | 15 000 | +12 000 défavorable |
| Total charges | 940 000 | 934 000 | −6 000 | 886 000 | +48 000 défavorable |
| Résultat | 260 000 | 213 500 | −46 500 | 194 000 | +19 500 |

- Prix unitaires réels : vente 1 147 500 / 9 000 = 127,50 € (+6,25 %) ; matières 459 000 / 9 000 = 51 € (+6,25 %) ; transport 63 000 / 9 000 = 7 € (+16,7 %). Volume : −10 %.
- Chiffre d'affaires : effet volume (9 000 − 10 000) × 120 = −120 000 ; effet prix (127,50 − 120) × 9 000 = +67 500 ; total −52 500.
- Matières : effet volume −1 000 × 48 = −48 000 (favorable) ; effet prix (51 − 48) × 9 000 = +27 000 (défavorable) ; total −21 000.
- Taux de marge sur matières inchangé : 60 % au budget (720 000 / 1 200 000) comme au réel (688 500 / 1 147 500) ; marge unitaire 72 € → 76,50 €.
- Pont du résultat : 260 000 → effet volume −66 000 (1 000 u. × marge sur coûts variables budgétée de 120 − 48 − 6 = 66 €) → 194 000 → écarts de prix et de coûts +19 500 (+67 500 prix de vente, −27 000 matières, −9 000 transport, −18 000 personnel, +18 000 marketing, −12 000 honoraires) → 213 500.
- Résultat hors décalage du salon : 213 500 − 18 000 = 195 500 ; hors décalage et hors honoraires d'avocat ponctuels : 207 500.

## Une bonne sortie contient

1. Donne l'écart de chaque ligne en euros et en pourcentage, avec une convention de signe annoncée (une charge sous le budget est favorable, un produit sous le budget est défavorable).
2. Décompose l'écart de chiffre d'affaires en effet volume (−120 000 €) et effet prix (+67 500 €).
3. Décompose l'écart matières en effet volume (−48 000 €, favorable) et effet prix (+27 000 €, défavorable), et constate que la hausse du coût matière (+6,25 %) est exactement répercutée dans le prix de vente (+6,25 %), le taux de marge restant à 60 %.
4. Montre que « les charges sont tenues » est trompeur : à 9 000 unités, le budget flexible des charges est de 886 000 €, le réel de 934 000 €, soit 48 000 € de dépassement au lieu des 6 000 € d'économie apparents.
5. Construit le pont du résultat de 260 000 € à 213 500 € : effet volume −66 000 € (1 000 unités × 66 € de marge sur coûts variables), écarts de prix et de coûts +19 500 €, et identifie la baisse de volume comme première cause de l'écart.
6. Traite les −18 000 € de marketing comme un décalage dans le temps (salon reporté en octobre) et non comme une économie, en indiquant que le T4 les supportera et que le résultat sous-jacent du T3 est d'environ 195 500 €.
7. Isole les 12 000 € d'avocat comme une charge observée et ponctuelle, distincte de la tendance.
8. Calcule le coût de transport unitaire (7 € contre 6 €, soit +9 000 € par rapport au budget flexible) et le présente comme non expliqué, avec des hypothèses marquées comme telles (tarif ou surcharge du transporteur, livraisons plus petites ou plus nombreuses) et la vérification à faire (factures transporteur, nombre d'expéditions).
9. Relève que le personnel augmente de 18 000 € alors que le volume baisse de 10 %, et propose des hypothèses à vérifier (intérim, heures supplémentaires, remplacement d'absences), sans en présenter aucune comme un fait.
10. Formule le lien entre la hausse de prix au 1er juillet et la baisse de 10 % du volume comme une hypothèse à tester (volumes par client et par mois, clients perdus), pas comme une cause établie, et sépare dans toute la sortie ce qui est observé, ce qui est une hypothèse chiffrée et ce qui reste à vérifier.

## Forme attendue

1. En tête, avant tout tableau, une synthèse de trois à cinq lignes pour le comité donne l'écart de résultat en euros et ses deux ou trois causes principales chiffrées.
2. Un tableau des écarts ligne par ligne avec les colonnes : budget, réel, écart en euros, écart en %, favorable / défavorable, puis budget flexible et écart réel / flexible ; il inclut les lignes de total des charges et de résultat, et indique la période et l'unité (€ HT).
3. Un pont du résultat (tableau ou cascade) part du résultat budgété, liste chaque effet avec son signe et son montant, et arrive exactement au résultat réel ; la somme des effets égale l'écart total affiché.
4. Chaque explication porte une étiquette visible de statut (observé, hypothèse, à vérifier), en colonne ou en marqueur, et chaque hypothèse est suivie de la donnée ou du document qui la confirmerait.
5. Les éléments non récurrents (report du salon, honoraires d'avocat) sont regroupés dans un bloc à part, avec un résultat retraité présenté à côté du résultat réel, sans le remplacer.
6. Les actions et vérifications forment une liste distincte du diagnostic, chacune avec la fonction qui la porte et l'échéance (avant le comité, clôture du T4).

## Une mauvaise sortie

- Conclut que les charges sont maîtrisées (−6 000 €) et que l'écart vient « du chiffre d'affaires », sans budget flexible ni décomposition volume/prix.
- Compte les 18 000 € de marketing comme une économie, ou affirme sans réserve que la hausse de prix a fait fuir les clients.
- Commente seulement les écarts en pourcentage, ligne par ligne, sans pont jusqu'au résultat.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 10) | Note |
|---|---|---|---|---|
| 2026-10-16 | 1.1.0 | Sonnet 5.5 | 5.7 (5–6) | banc 3 passages, moyenne (min–max) ; erreurs relevées 0.3 (0–1) |
| 2026-10-16 | 1.2.0 | Sonnet 5.5 | **6.7 (6–7)** | banc 3 passages ; erreurs 1.3 (0–4) |
| 2026-10-16 | 1.1.0 | Haiku 5.5 | 4.0 (3–5) | banc 3 passages, moyenne (min–max) ; erreurs relevées 7.7 (7–8) |
| 2026-10-16 | 1.2.0 | Haiku 5.5 | **5.0 (4–6)** | banc 3 passages ; erreurs 9.0 (7–12) |
| 2026-10-16 | sans skill | Sonnet 5.5, effort medium | 4.2 (2.5–5.5) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 0.8 (0.5–1.0) /6 ; coût moyen 0.037 $ |
| 2026-10-16 | 1.1.0 | Sonnet 5.5, effort medium | 6.2 (6.0–6.5) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 2.2 (1.5–3.0) /6 ; coût moyen 0.069 $ |
| 2026-10-16 | 1.2.0 | Sonnet 5.5, effort medium | 6.5 (6.5–6.5) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 1.5 (1.0–2.0) /6 ; coût moyen 0.092 $ |
| 2026-10-16 | sans skill | Sonnet 5.5, effort high | 5.2 (4.5–6.0) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 2.3 (1.5–3.0) /6 ; coût moyen 0.047 $ |
| 2026-10-16 | 1.1.0 | Sonnet 5.5, effort high | 6.3 (6.0–6.5) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 2.2 (1.0–3.0) /6 ; coût moyen 0.085 $ |
| 2026-10-16 | 1.2.0 | Sonnet 5.5, effort high | 6.7 (6.5–7.0) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 1.7 (1.0–2.0) /6 ; coût moyen 0.116 $ |
| 2026-10-16 | sans skill | Opus 5.5 | 5.5 (5.0–6.0) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 2.5 (2.0–3.0) /6 ; coût moyen 0.113 $ |
| 2026-10-16 | 1.1.0 | Opus 5.5 | 6.5 (5.0–7.5) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 2.8 (2.5–3.0) /6 ; coût moyen 0.162 $ |
| 2026-10-16 | 1.2.0 | Opus 5.5 | 7.2 (6.0–8.0) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 2.5 (2.0–3.0) /6 ; coût moyen 0.219 $ |
