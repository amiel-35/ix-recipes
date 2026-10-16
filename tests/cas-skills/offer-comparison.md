---
skill: offer-comparison
famille: commercial-achats
ecrit: 2026-10-16
---

# Cas 1 — trois offres pour un logiciel de notes de frais, avec une repondération demandée par le DG

## Demande

> Trois offres normalisées pour notre logiciel de notes de frais (coût total sur 3 ans, HT, même périmètre sauf mention). Grille validée avant l'envoi du cahier des charges : prix 40 %, couverture fonctionnelle 35 %, support 15 %, sécurité et réversibilité 10 %. Note prix = 10 × prix le plus bas / prix de l'offre. Notes qualité (sur 10) de l'équipe projet :
> A : 180 k€ ; fonctionnel 8 ; support 7 ; sécurité 8.
> B : 210 k€ ; fonctionnel 9 ; support 9 ; sécurité 7.
> C : 150 k€ ; fonctionnel 6 ; support 5 ; sécurité 4. Reprise des données historiques non chiffrée (« sur devis »).
> Notre DG trouve que le support de B est un vrai plus et propose de passer le support à 25 %, en prenant 10 points au prix. Lequel on prend ?

## Valeurs de référence

| | Note prix | Score, grille validée | Score, grille du DG (30/35/25/10) | Score si C = 180 k€ |
|---|---|---|---|---|
| A | 8,33 | **7,98** | 7,85 | **8,65** (note prix 10) |
| B | 7,14 | **8,06** | 8,24 | **8,63** (note prix 8,57) |
| C | 10 | **7,25** | 6,75 | 7,25 (note prix 10) |

Écart B − A avec la grille validée : 0,07. Effet d'un point de support : 0,15. Effet d'un point de fonctionnel : 0,35.

## Une bonne sortie contient

(« * » : échouerait probablement avec la version 1.1.0)

1. Les notes prix et les scores de la grille validée (A 7,98, B 8,06, C 7,25) avec la méthode.
2. \* La pondération du DG non appliquée comme grille, présentée en sensibilité étiquetée « après ouverture » (A 7,85, B 8,24, C 6,75), avec la raison.
3. C déclarée non comparable sur le prix tant que la reprise n'est pas chiffrée ; prix ferme demandé.
4. \* L'effet de la formule : si la reprise porte C à 180 k€, A passe devant B (8,65 contre 8,63) sans qu'A ni B n'aient changé.
5. \* Un classement A / B jugé fragile : 0,07 d'écart, moins que l'effet d'un point de note sur un critère qualitatif (support 0,15, fonctionnel 0,35) ; confiance faible.
6. Une recommandation nette malgré tout, avec sa condition (par exemple : B, sous réserve du chiffre de C et d'une négociation ; ou un départage nommé).
7. La note sécurité de C (4/10) signalée comme point de vigilance, voire seuil à poser.
8. La distinction entre données fournies, calculs, hypothèses et recommandation.

## Une mauvaise sortie

- La grille du DG appliquée comme grille officielle, sans la sensibilité étiquetée.
- C notée à 10 sur le prix sans questionner la reprise « sur devis ».
- Un classement présenté comme net malgré 0,07 d'écart, ou une conclusion neutre (« à vous de choisir »).
- Des scores faux (erreur d'addition ou de pondération).

## Résultats

| Date | Version | Modèle | Critères tenus (sur 8) | Note |
|---|---|---|---|---|
