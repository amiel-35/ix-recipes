---
skill: business-case-draft
famille: finance
ecrit: 2026-10-16
---

# Cas 1 — « le ROI » d'une automatisation

## Demande

> Mon DG veut un business case pour automatiser la saisie des commandes. Il me demande « le ROI ». Voilà ce que j'ai :
> - Investissement : 120 000 € la première année (licences + intégration)
> - Coût de fonctionnement : 10 000 €/an
> - Gains attendus par an : 18 000 € d'intérim qu'on arrête au service commandes, 12 000 € de pénalités de retard évitées, et environ 0,4 ETP libéré (≈ 20 000 €/an), mais personne ne part
> - Horizon 5 ans, taux d'actualisation 8 % (donné par le DAF), on raisonne avant impôt pour l'instant.

## Valeurs de référence (calculées à la main, 2026-10-16)

Investissement à t = 0, flux en fin d'année, facteur d'annuité à 8 % sur 5 ans = 3,9927.

| Cas | Flux net annuel | VAN à 8 % | TRI | Payback |
|---|---|---|---|---|
| Tous gains (encaissés + temps libéré) | 40 000 € | **+39 708 €** | **19,9 %** | 3 ans simple ; ≈ 3,6 ans actualisé |
| Gains encaissés seuls | 20 000 € | **−40 146 €** | ≈ −5,8 % | jamais sur 5 ans (100 000 € cumulés < 120 000 €) |
| Point mort | **30 055 €/an** de flux net | 0 | 8 % | il faut qu'environ 10 055 € des 20 000 € de temps libéré deviennent un gain encaissé |
| « ROI » naïf sans coût de fonctionnement | — | (5 × 50 000 − 120 000) / 120 000 = 108 % | — | à refuser |
| ROI sur 5 ans, coût de fonctionnement déduit | — | (5 × 40 000 − 120 000) / 120 000 = 66,7 % (non actualisé) | — | — |

Les scénarios bas et haut sont libres ; les critères portent sur leur présence et leur cohérence.

## Une bonne sortie contient

1. Le coût de fonctionnement de 10 000 €/an déduit de chaque année ; aucun ROI à 108 %.
2. La distinction entre gains encaissés (30 000 €) et temps libéré (20 000 €), avec la VAN dans les deux cas (+39,7 k€ et −40,1 k€).
3. Une VAN à 8 % de ≈ +39 700 € sur l'ensemble des gains, et un TRI ≈ 19,9 %.
4. Le payback simple de 3 ans, avec le payback actualisé (≈ 3,6 ans) ou la limite du payback dite.
5. Le point mort calculé (≈ 30 000 €/an de flux net, soit la moitié environ du temps libéré à convertir en gain encaissé).
6. Au moins trois scénarios, chacun nommant l'hypothèse qui bouge.
7. Le « ROI » demandé défini par sa formule.
8. La comparaison au statu quo explicite (l'intérim et les pénalités continuent si on ne fait rien).
9. Une recommandation qui dépend de la condition clé (que fait-on des 0,4 ETP ?), pas un oui sans condition.
10. Le calcul dit avant impôt, conformément à la demande, sans taux d'IS appliqué.

## Une mauvaise sortie

- Un ROI unique présenté comme « le » résultat, sans scénarios ni point mort.
- Les 50 000 € de gains comptés comme de la trésorerie.
- Aucun calcul de VAN, ou une VAN sans taux ni horizon.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 10) | Note |
|---|---|---|---|---|
