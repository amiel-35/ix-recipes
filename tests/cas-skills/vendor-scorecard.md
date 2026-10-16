---
skill: vendor-scorecard
famille: commercial-achats
ecrit: 2026-10-16
---

# Cas 1 — grille pour remplacer un logiciel de paie

## Demande

> On lance une consultation pour remplacer notre logiciel de paie (SaaS, 250 salariés, données RH sensibles). La DAF veut que le prix compte pour 40 %. Construis la grille avant qu'on envoie le cahier des charges. Pour qu'on voie comment se comporte la note prix, simule-la sur trois prix fictifs sur 3 ans : 100 k€, 110 k€ et 150 k€.

## Valeurs de référence

Notes sur 10 ; entre parenthèses, points sur 4 avec un prix à 40 %.

| Formule | 100 k€ | 110 k€ | 150 k€ |
|---|---|---|---|
| Proportionnelle `10 × Pmin/P` | 10 (4,00) | 9,09 (3,64) | 6,67 (2,67) |
| Linéaire min–max `10 × (Pmax−P)/(Pmax−Pmin)` | 10 (4,00) | 8,00 (3,20) | 0 (0) |
| Écart relatif, k = 1 | 10 (4,00) | 9,00 (3,60) | 5,00 (2,00) |

## Une bonne sortie contient

(« * » : échouerait probablement avec la version 1.1.0)

1. \* Des éliminatoires « oui / non » séparés de la notation : production de la DSN, contrat RGPD art. 28. La raison est donnée (un poids compenserait).
2. Des dimensions propres à un logiciel de paie : couverture fonctionnelle et conventions collectives, mises à jour réglementaires incluses, intégration (SIRH, comptabilité), sécurité, réversibilité des historiques, reprise et déploiement, support, solidité de l'éditeur.
3. Le prix à 40 %, avec ce que ce poids implique, et des poids qui totalisent 100.
4. \* Une formule de prix choisie et justifiée, et les valeurs simulées exactes (tableau ci-dessus) pour la ou les formules présentées.
5. \* L'effet de la formule linéaire min–max (150 k€ obtient 0 quel que soit l'écart) et la dépendance de la proportionnelle au moins-disant.
6. \* La règle des pondérations figées avant l'envoi, avec sa raison ; tout changement après réception présenté comme une sensibilité.
7. \* Une échelle ancrée (descripteur par niveau) pour au moins un critère.
8. Le prix noté sur le coût complet à 3 ans, pas sur l'abonnement seul.
9. Les critères qui demandent une définition interne avant usage, signalés.
10. Aucun « bon poids » présenté comme une norme sans source ; le repère de poids du prix donné comme un défaut non sourcé.

## Une mauvaise sortie

- Les exigences légales (DSN, contrat art. 28) traitées comme des critères pondérés.
- Une note prix simulée avec des valeurs fausses, ou une seule formule sans ses effets.
- Des critères sans échelle, ou « bon / moyen / faible » sans descripteur.
- Un article de loi inventé ou faux.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 10) | Note |
|---|---|---|---|---|
