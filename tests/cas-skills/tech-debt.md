---
skill: tech-debt
famille: tech
ecrit: 2026-10-16
---

# Cas 1 — Audit pour le planning, avec des notes déjà posées (effort 1 = facile)

## Demande

> Audit de dette pour le prochain planning. L'équipe a déjà noté chaque item (Impact, Risque, Effort de 1 à 5, Effort 1 = facile, 5 = très lourd) :
> 1. Module facturation sans tests automatisés, 2 régressions en prod ce trimestre — I4 R4 E2.
> 2. Déploiement manuel, 2 h chaque mardi, une erreur de configuration en juin — I3 R3 E1.
> 3. Django 3.2, plus maintenu depuis avril 2024 — I2 R5 E3.
> 4. README d'installation obsolète, il faut 3 jours pour installer le poste d'un nouveau développeur — I2 R1 E1.
> 5. Découper le monolithe en microservices — I3 R2 E5.
> 6. Logs non structurés — I2 R2 E2.

## Valeurs de référence

Formule (Impact + Risque) × (6 − Effort), l'effort étant noté brut :

| Item | Score | Horizon |
|---|---|---|
| 1 | 8 × 4 = **32** | sprint |
| 2 | 6 × 5 = **30** | sprint |
| 3 | 7 × 3 = **21** | trimestre |
| 4 | 3 × 5 = **15** | trimestre (pile sur le seuil) |
| 5 | 5 × 1 = **5** | backlog |
| 6 | 4 × 4 = **16** | trimestre |

Avec la double inversion de l'effort (version 1.2.1), l'item 2 tombait à 6 (backlog) et l'item 5 montait à 25 (trimestre).

## Une bonne sortie contient

1. Les 6 scores ci-dessus, avec leurs horizons.
2. L'item 2 au prochain sprint, avec 30 (l'effort n'est pas inversé deux fois).
3. L'item 5 au backlog, avec 5 ; la réécriture en microservices n'est pas recommandée sans comparaison chiffrée du coût de maintien et du coût de remplacement.
4. Une justification métier pour chaque item retenu, étiquetée observée, probable ou hypothèse (par exemple 2 h par semaine, soit une centaine d'heures par an, pour l'item 2 ; les régressions de facturation exposent le chiffre d'affaires).
5. Un plan entrelacé avec les fonctionnalités : une part de capacité par sprint, donnée comme défaut à remplacer, sans gel des fonctionnalités.
6. Pas de « RAS », puisque des items dépassent 15.
7. Les notes fragiles signalées : l'item 4 est pile sur 15, et son impact dépend du rythme des recrutements, non fourni. *(échoue probablement avec 1.2.1)*
8. L'effort-5 traité comme un item à découper (l'item 5 ne peut jamais dépasser 10 points) avant d'être noté de nouveau. *(échoue probablement avec 1.2.1)*
9. Les sorties nommées `tech_debt_audit`, `plan_remediation` et `questions_ouvertes`.

## Une mauvaise sortie

- Scores recalculés avec l'effort inversé deux fois (item 2 à 6, item 5 à 25).
- Une liste exhaustive non classée, ou un plan qui gèle les fonctionnalités.
- Une justification purement technique (« code plus propre ») sans conséquence métier.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 9) | Note |
|---|---|---|---|---|

# Cas 2 — Aucun item n'atteint le seuil (cas de contrôle du « RAS »)

## Demande

> Fais l'audit de dette de notre site vitrine (WordPress, 12 pages, mis à jour chaque mois par l'agence). Les seules choses que l'équipe a notées : un plugin de galerie remplaçable en une demi-journée (I1 R1 E1) et deux captures d'écran périmées dans la doc interne (I1 R1 E1).

## Valeurs de référence

(1 + 1) × (6 − 1) = **10** pour chaque item, soit sous 15.

## Une bonne sortie contient

1. Une ouverture par « RAS — » suivie de la raison (aucun item n'atteint le seuil du trimestre), et rien d'autre de substantiel.
2. Les deux scores de 10, vérifiables.
3. Les deux items rangés dans une ligne de backlog unique, sans plan de remédiation.
4. La mention que l'audit repose sur la liste fournie (périmètre non lu : le code, les extensions en place).

## Une mauvaise sortie

- Un plan de remédiation trimestriel inventé pour remplir le livrable.
- Des items ajoutés de mémoire sur WordPress en général.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 4) | Note |
|---|---|---|---|---|
