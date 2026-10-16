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

# Cas 2 — passer d'un prix par utilisateur à un prix à l'usage

## Demande

> On édite un outil de signature électronique pour PME : 29 € par utilisateur et par mois, 400 clients, 2 000 sièges, environ 30 000 signatures par mois au total. Nos clients se plaignent de payer des sièges qui signent rarement. On pense passer à 2 € par signature, sans abonnement. Coût variable : environ 0,15 € par signature (horodatage, SMS). Voilà la répartition des clients :
>
> - 250 clients : 3 sièges, 40 signatures par mois chacun
> - 100 clients : 6 sièges, 100 signatures par mois
> - 40 clients : 10 sièges, 150 signatures par mois
> - 10 clients : 25 sièges, 400 signatures par mois
>
> Qu'est-ce que ça change pour notre chiffre d'affaires et pour chaque type de client ? Est-ce la bonne façon de facturer ?

## Valeurs de référence (calculées à la main, 2026-10-16)

| Élément | Valeur |
|---|---|
| CA mensuel actuel | 2 000 × 29 = **58 000 €** |
| Prix neutre pour le CA | 58 000 / 30 000 = **1,93 € par signature** |
| CA à 2 € | 30 000 × 2 = **60 000 €** (+3,4 %) |
| Contribution mensuelle (coût variable 4 500 €) | **53 500 €** avant, **55 500 €** après si personne ne bouge |
| Facture par client, avant → après | 3 sièges : 87 → 80 € (−8,1 %) ; 6 sièges : 174 → 200 € (+14,9 %) ; 10 sièges : 290 → 300 € (+3,4 %) ; 25 sièges : 725 → 800 € (+10,3 %) |
| Perte de clients tolérée par segment qui paie plus (contribution par client : 159 → 185 € ; 267,5 → 277,5 € ; 665 → 740 €) | 6 sièges : **14,1 %** ; 10 sièges : **3,6 %** ; 25 sièges : **10,1 %** |
| Gain de clients nécessaire pour le segment qui paie moins (contribution 81 → 74 €) | 3 sièges : **+9,5 %** |

## Une bonne sortie contient

1. Le CA avant et après (58 000 → 60 000 €), et le prix neutre (≈ 1,93 €) comme repère.
2. La facture de chaque type de client avant et après : le petit client gagne (−8 %), les trois autres paient plus.
3. Le volume d'équilibre calculé sur la marge par client, par segment, avec la formule et les entrées (≈ 14 %, 3,6 %, 10 %), pas sur le chiffre d'affaires.
4. Le constat que le CA global masque des gagnants et des perdants : le segment à 10 sièges n'a presque aucune marge de perte (3,6 %).
5. La signature jugée sur les critères d'une bonne métrique (suit la valeur, comprise, mesurable, croît avec le compte), et au moins une autre piste (documents envoyés, paliers de volume, socle plus signatures incluses).
6. Le risque d'une facture imprévisible ou saisonnière nommé, avec une parade (socle ou engagement minimal, paliers).
7. Le traitement de la base installée : clause de révision du contrat, préavis, maintien temporaire de l'ancien prix pour ceux qui paient plus.
8. La question du modèle séparée de celle du niveau de prix (2 € est un niveau, « à la signature » est une métrique).
9. Une méthode ou un test pour mesurer le consentement à payer (nouvelle cohorte facturée à la signature), sans prix « optimal » affirmé.
10. Une pente (« option qui paraît la mieux étayée ») étiquetée comme telle, avec ce qui la renverserait et les critères prêts pour `decision`, sans verdict définitif.
11. Aucune règle de droit de la consommation plaquée sur cette vente entre professionnels.

## Une mauvaise sortie

Elle conclut que « le CA augmente de 3 % donc c'est bon », sans regarder qui paie plus ; calcule le volume d'équilibre sur le chiffre d'affaires ; déclare l'usage « le meilleur modèle » sans critère ni test ; applique la règle de la réduction de prix du Code de la consommation ou invente un article.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 11) | Note |
|---|---|---|---|---|
