---
skill: interview-loop-planner
famille: rh
ecrit: 2026-10-16
---

# Cas 1 — boucle pour un développeur backend senior, recrutement pressé

## Demande

> On recrute un Senior Backend Engineer (Python, API, Postgres) dans notre scale-up de 80 personnes. Fiche de poste : « Tu rejoindras l'équipe Plateforme (6 devs). Missions : concevoir et faire évoluer nos API, améliorer la fiabilité, mentorer les juniors. Profil : 5 ans d'expérience Python minimum, bon communicant, team player, dynamique, à l'aise avec les bases de données. » On veut une offre signée en 3 semaines. Conçois le process d'entretien.

## Une bonne sortie contient

1. Famille tech, niveau senior, et des compétences tirées du référentiel tech (conception et code, résolution de problèmes, architecture ; leadership technique, collaboration).
2. Un nombre de tours justifié par le niveau (4 ou 5), ou une compression assumée à cause du délai, avec ce qu'elle coûte.
3. Un tableau de couverture compétence × tour, où chaque compétence cœur est évaluée au moins une fois.
4. Les termes flous de la fiche relevés (« bon communicant », « team player », « dynamique ») avec une reformulation observable.
5. Pas deux tours qui évaluent les mêmes compétences.
6. Un planning qui tient les 3 semaines, sans plus de 3 h d'entretien par jour pour le candidat.
7. Une scorecard pondérée avec seuils de décision, et un veto sur une compétence cœur trop basse.
8. Un `round_brief` par tour, au format attendu par `interview-guide-recruteur`.
9. Un débrief où chacun note seul avant la réunion, et un protocole quand les notes divergent de plus de 1,5 point.
10. La vigilance anti-biais citée dans la préparation des intervieweurs.
11. Aucune question d'entretien rédigée (c'est le rôle du guide).
12. Le cadre du recrutement : candidat informé à l'avance des méthodes (art. L1221-8 C. trav.), informations demandées en lien direct avec l'emploi (art. L1221-6), un exercice à la maison proportionné.
13. Un tour « culture / fit » non structuré évité, ou signalé comme risque de biais.

## Une mauvaise sortie

- Six tours pour un senior avec offre en 3 semaines, sans arbitrage.
- Des questions d'entretien rédigées.
- « team player » repris comme compétence évaluée telle quelle.

## Résultats

Notation à l'aveugle par un juge Opus (sorties anonymisées et mélangées), banc `claude -p` avec le seul skill en invite système, outil Lecture seulement. « 1.3.0 brouillon » est la première réécriture (pour le cas 2, après la consigne « version de travail puis conception » qui empêchait Haiku de s'arrêter) ; ses erreurs d'addition ont conduit à l'étape « vérifier les totaux » de la 1.3.0.

| Date | Version | Modèle | Critères tenus (sur 13) | Note |
|---|---|---|---|---|
| 2026-10-16 | 1.2.0 | Sonnet 5.5 | 12 | Aucun cadre légal (L1221-6, L1221-8). 0 erreur. |
| 2026-10-16 | 1.3.0 brouillon | Sonnet 5.5 | 12 | L1221-8 et -9 cités, L1221-6 omis ; fin de sortie dupliquée, durée totale incohérente (1 erreur). |
| 2026-10-16 | 1.2.0 | Haiku 5.5 | 9 | Questions rédigées, tour « culture fit » libre, deux tours redondants ; 4 erreurs de calcul. |
| 2026-10-16 | 1.3.0 brouillon | Haiku 5.5 | 8 | Nombre de tours non rattaché au niveau, 3 h 30 un même jour, questions rédigées, « fit » libre ; 5 erreurs (durées, coefficients). |
| 2026-10-16 | 1.3.0 | Sonnet 5.5 | 12 | Second tour de notation (1.2.0 Sonnet : 12, 1 erreur ; 1.2.0 Haiku : 9, 6 erreurs). L1221-8 et -9 cités, L1221-6 omis ; totaux justes ; 1 erreur héritée de l'annexe débrief (durée), corrigée depuis. |
| 2026-10-16 | 1.3.0 | Haiku 5.5 | 8 | « team player » non reformulé, deux tours redondants, questions rédigées, tour de « fit » ; 6 erreurs. |

# Cas 2 — premier commercial d'une startup, sans fiche de poste (cas de contrôle)

## Demande

> On est une startup de 15 personnes, on veut recruter un SDR junior, c'est notre premier commercial. On n'a pas de fiche de poste. Les entretiens seront faits par les deux fondateurs. Fais-nous le process.

## Une bonne sortie contient

1. Le manque de fiche de poste signalé, avec une version de travail à valider avant de concevoir les tours.
2. La famille commerciale et le niveau junior identifiés.
3. Deux ou trois tours, pas plus, avec la raison (niveau junior, petite équipe).
4. Un format de mise en situation (jeu de rôle d'appel ou de prospection) plutôt qu'un entretien libre.
5. Une scorecard pondérée fixée avant les entretiens.
6. Un débrief adapté à deux intervieweurs : chacun note seul avant d'en parler.
7. Le candidat informé à l'avance des méthodes, dont la mise en situation.
8. Aucune question d'entretien rédigée.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 8) | Note |
|---|---|---|---|---|
| 2026-10-16 | 1.2.0 | Sonnet 5.5 | 7 | Seuils « à ajuster après le premier candidat » (grille non fixée avant) ; 1 erreur de durée. |
| 2026-10-16 | 1.3.0 brouillon | Sonnet 5.5 | **8** | Fiche de travail à valider, 3 tours justifiés, mise en situation annoncée ; 1 erreur (maximum de la grille). |
| 2026-10-16 | 1.2.0 | Haiku 5.5 | 5 | Tours justifiés par le « culture fit », grille incohérente, questions rédigées, candidat inventé dans le modèle ; 5 erreurs. |
| 2026-10-16 | 1.3.0 brouillon | Haiku 5.5 | 7 | Questions rédigées dans une option ; 4 erreurs d'addition (maximum, bandes, durée). |
| 2026-10-16 | 1.3.0 | Sonnet 5.5 | **8** | Second tour (1.2.0 Sonnet : 7, 1 erreur ; 1.2.0 Haiku : 5, 10 erreurs). Totaux justes ; 1 erreur héritée de l'annexe débrief. |
| 2026-10-16 | 1.3.0 | Haiku 5.5 | 7 | Questions rédigées ; 3 erreurs de durée. |
