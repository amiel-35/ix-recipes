---
skill: strategie-prix
famille: finance
ecrit: 2026-10-16
---

# Cas 1 — hausse de 49 à 59 € et métrique « par utilisateur »

Ce cas est écrit pour la version enrichie (question 10 de la revue : enrichir ou retirer le skill). La version 1.1.1 ne reformule que les consignes et définit `modele_prix` et `inclure_tests` ; les critères marqués « (Q10) » ne sont pas attendus d'elle et servent de référence tant que la question n'est pas tranchée.

## Demande

> On vend notre outil à 49 €/mois par utilisateur, marge brute 80 %, 1 200 utilisateurs payants (PME françaises, contrats mensuels). On pense passer à 59 €. Combien d'utilisateurs on peut perdre avant d'y perdre ? Et est-ce que le « par utilisateur » est le bon modèle, nos clients se plaignent de payer pour des gens qui se connectent une fois par mois ?

## Valeurs de référence (calculées à la main, 2026-10-16)

| Élément | Valeur |
|---|---|
| Variation de prix Δp | 10 / 49 = 20,4 % |
| Coût variable par utilisateur | 49 × 20 % = 9,80 € |
| Contribution mensuelle actuelle | 1 200 × 39,20 = **47 040 €** |
| Utilisateurs pour la même contribution à 59 € | 47 040 / 49,20 = **956** |
| Perte tolérée | **244 utilisateurs, soit 20,3 %** = 0,204 / (0,80 + 0,204) |

## Une bonne sortie contient

1. La perte tolérée ≈ 20 % (≈ 244 utilisateurs), formule et entrées montrées. (Q10)
2. Le raisonnement sur la marge sur coût variable, pas sur le chiffre d'affaires. (Q10)
3. Le niveau de prix (49 → 59) séparé de la question du modèle (par siège ou autre).
4. Au moins deux métriques de valeur de rechange (utilisateurs actifs, volume traité, palier par compte), jugées sur des critères. (Q10)
5. La plainte des clients reliée à une métrique de valeur qui ne suit pas la valeur reçue.
6. Une méthode pour mesurer le consentement à payer ou un test proposé (nouvelle cohorte à 59 €, par exemple), sans prix « optimal » affirmé sans données.
7. Le traitement des clients existants (préavis, maintien temporaire de l'ancien prix) mentionné.
8. Une recommandation avec ce qu'elle sacrifie et les hypothèses qui la feraient changer.
9. Aucune règle de droit de la consommation plaquée sur une vente B2B (la règle d'annonce de réduction ne concerne que les consommateurs).

## Une mauvaise sortie

- Un prix « optimal » affirmé sans donnée de consentement à payer.
- Un raisonnement de break-even sur le chiffre d'affaires (perdre 17 % d'utilisateurs) au lieu de la marge.
- Une liste de modèles sans recommandation.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 9) | Note |
|---|---|---|---|---|
