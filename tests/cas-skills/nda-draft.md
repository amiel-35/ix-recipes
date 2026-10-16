---
skill: nda-draft
famille: juridique
ecrit: 2026-10-16
---

# Cas 1 — NDA avant un audit d'acquisition par un groupe coté

## Demande

> On est une PME française (SAS, éditeur de logiciel, 45 salariés). Un groupe coté à Paris nous approche pour un éventuel rachat. Avant l'audit, ils veulent accéder à nos contrats clients, à notre fichier clients et à notre code source. Ils ne nous ont pas envoyé de NDA, c'est à nous de le proposer. Rédige-le.

## Une bonne sortie contient

1. Un choix explicite unilatéral / mutuel, motivé (ici, le groupe partagera aussi des informations sur son offre et ses intentions : le mutuel se défend ; l'unilatéral protège mieux la cible).
2. Une définition de l'information confidentielle qui couvre l'existence même des discussions, avec les exclusions usuelles : domaine public, déjà connue, développée indépendamment, reçue licitement d'un tiers, et la divulgation exigée par la loi ou une autorité.
3. La limitation de l'usage à l'évaluation de l'opération, et l'accès limité à ceux qui en ont besoin (salariés, conseils), le destinataire répondant d'eux.
4. Une durée des obligations bornée (et pas « perpétuelle », art. 1210 C. civ.), avec la survie après la fin des discussions.
5. La restitution ou la destruction à la fin, avec l'exception des sauvegardes et des obligations légales de conservation.
6. Une clause de non-sollicitation des salariés (et éventuellement des clients) proposée comme option propre au rachat.
7. Le point « groupe coté » : l'opération peut constituer une information privilégiée (règlement MAR n° 596/2014) ; signaler la question, le standstill éventuel et la liste d'initiés côté acheteur, sans les inventer.
8. Le point « fichier clients » : des données personnelles ; le NDA ne suffit pas (RGPD : minimisation, base légale, éventuellement anonymisation ou data room) ; conseiller de ne pas transmettre le fichier brut au stade de l'audit.
9. Le point « code source » : modalités d'accès restreintes (data room, consultation sans copie, auditeur tiers).
10. Pas de licence, pas d'obligation de conclure, pas de garantie sur l'exactitude des informations.
11. Le droit applicable et la juridiction, à confirmer.
12. Les sanctions : réparation ou clause pénale, en signalant que le juge peut la modérer (art. 1231-5 C. civ.).
13. Les champs inconnus laissés en blanc (noms, SIREN, signataires), jamais inventés.
14. La liste des points à valider et le rappel qu'un avocat relit avant signature.

## Une mauvaise sortie

- Un NDA générique « prestataire » sans rien de propre au rachat (non-sollicitation, MAR, données personnelles, code source).
- Une durée perpétuelle, ou une durée sans dire ce qui survit.
- Des noms ou des numéros d'immatriculation inventés.

## Résultats

Notation à l'aveugle par un juge Opus (sorties anonymisées et mélangées), banc `claude -p` avec le seul skill en invite système, outil Lecture seulement. « 1.2.0 brouillon » est la première réécriture ; ses défauts (articles inventés par Haiku, durée ouverte pour les secrets d'affaires) ont conduit aux corrections de la 1.2.0.

| Date | Version | Modèle | Critères tenus (sur 14) | Note |
|---|---|---|---|---|
| 2026-10-16 | 1.1.0 | Sonnet 5.5 | 13 | Obligations sur le code source « sans limite de durée » (art. 1210). 1 erreur. |
| 2026-10-16 | 1.2.0 brouillon | Sonnet 5.5 | **14** | 0 erreur ; MAR, RGPD, art. 1210 et 1231-5 justes. |
| 2026-10-16 | 1.1.0 | Haiku 5.5 | 6 | NDA générique : ni MAR, ni non-sollicitation discutée, fichier clients brut dans l'objet, durée perpétuelle. 2 erreurs. |
| 2026-10-16 | 1.2.0 brouillon | Haiku 5.5 | 12 | Contenu propre au rachat présent, mais 4 erreurs : deux articles inventés ou abrogés, art. 7 MAR pour l'art. 10, DPA déclaré obligatoire pour l'acquéreur. |
| 2026-10-16 | 1.2.0 | Sonnet 5.5 | **14** | Second tour de notation (les versions 1.1.0 y obtiennent les mêmes notes) ; 0 erreur. |
| 2026-10-16 | 1.2.0 | Haiku 5.5 | 12 | Plus d'article inventé, durée bornée ; mais choix unilatéral / mutuel absent, standstill imposé alors que la cible n'est pas cotée, « dommages-intérêts punitifs » ; 4 erreurs. |

# Cas 2 — un « NDA » qui est en fait une non-concurrence (cas de contrôle)

## Demande

> Un de nos développeurs part dans un mois chez un concurrent. Je veux lui faire signer un accord de confidentialité qui l'empêche de travailler sur un produit concurrent pendant 2 ans. Tu peux me le rédiger ?

## Une bonne sortie contient

1. Le constat que l'interdiction de travailler sur un produit concurrent est une clause de non-concurrence, pas de confidentialité.
2. Les quatre conditions cumulatives de la non-concurrence (intérêt légitime, limitation dans le temps et l'espace, spécificités de l'emploi, contrepartie financière), avec la jurisprudence citée.
3. Le conseil de vérifier d'abord le contrat de travail et la convention collective (une clause existe peut-être déjà).
4. Le fait que le salarié n'est pas tenu de signer une nouvelle obligation au départ, et qu'il faut une contrepartie.
5. Un accord de confidentialité post-contrat limité aux informations confidentielles, proposé comme alternative.
6. Une exception pour les signalements protégés (lanceur d'alerte) et les divulgations exigées par la loi.
7. Pas de clause attributive de juridiction avec un salarié (ou bien signalée comme inopérante).
8. Le rappel de la relecture par un avocat.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 8) | Note |
|---|---|---|---|---|
| 2026-10-16 | 1.1.0 | Sonnet 5.5 | 7 | Conditions justes mais sans l'arrêt cité. 0 erreur. |
| 2026-10-16 | 1.2.0 brouillon | Sonnet 5.5 | **8** | 0 erreur ; arrêt du 10 juillet 2002 cité, confidentialité séparée de la non-concurrence. |
| 2026-10-16 | 1.1.0 | Haiku 5.5 | 2 | Rédige la non-concurrence demandée, clause de juridiction avec un salarié ; 2 erreurs. |
| 2026-10-16 | 1.2.0 brouillon | Haiku 5.5 | 3 | Repère la non-concurrence et ses 4 conditions, puis pose des questions au lieu de rédiger ; 0 erreur. |
| 2026-10-16 | 1.2.0 | Sonnet 5.5 | **8** | 0 erreur. |
| 2026-10-16 | 1.2.0 | Haiku 5.5 | 2 | Pose des questions au lieu de rédiger ; 2 erreurs (non-concurrence « au contrat d'embauche » seulement, contrepartie payée pendant le préavis). |
