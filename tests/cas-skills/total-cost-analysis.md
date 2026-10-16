---
skill: total-cost-analysis
famille: commercial-achats
ecrit: 2026-10-16
---

# Cas 1 — deux offres SaaS pour un outil de ticketing

## Demande

> Deux offres pour notre outil de ticketing support (40 agents), horizon 3 ans, montants HT.
> Offre A (SaaS) : 55 €/agent/mois, mise en service 8 000 €, connecteur CRM inclus, révision annuelle des prix selon l'indice Syntec, plafonnée à 4 %.
> Offre B (SaaS) : 45 €/agent/mois, prix fermes et engagement ferme sur 3 ans, mise en service 20 000 €, connecteur CRM en option à 300 €/mois, reprise de l'historique « sur devis ».
> On passera de 40 à 50 agents au début de la 2e année. Le connecteur CRM nous semble nécessaire, à confirmer avec l'équipe. Notre outil actuel coûte 2 400 €/mois et il faudra le garder 2 mois de plus pendant la bascule. Compare le coût total.

## Valeurs de référence

| Poste | A | B |
|---|---|---|
| Mise en service | 8 000 | 20 000 |
| Année 1 (40 agents) | 26 400 | 21 600 |
| Année 2 (50 agents) | 33 000 sans révision ; 34 320 à +4 % | 27 000 |
| Année 3 | 33 000 ; 35 692,80 à +4 %/an | 27 000 |
| Connecteur CRM | inclus | 10 800 (300 × 36) |
| **Total** | **100 400 à 104 412,80** | **106 400 + reprise non chiffrée** |
| B sans connecteur | — | 95 600 |
| Double run (commun) | 4 800 | 4 800 |

Seuil de bascule : sans connecteur, B est moins cher que A de 4 800 € (A sans révision) à 8 812,80 € (A au plafond), tant que la reprise d'historique coûte moins que cet écart. La première révision est comptée à l'anniversaire, soit au début de l'année 2.

## Une bonne sortie contient

(« * » : échouerait probablement avec la version 1.1.0)

1. \* Le total de A en fourchette, de 100 400 à 104 412,80 € HT, avec la révision chiffrée au plafond à partir de l'année 2.
2. Le total de B : 106 400 € HT plus la reprise d'historique, marquée non chiffrée.
3. Le passage à 50 agents appliqué aux deux offres dès l'année 2.
4. \* Le connecteur CRM nommé comme l'hypothèse qui inverse le classement (B à 95 600 € sans lui).
5. \* Le seuil de bascule sur la reprise d'historique (4 800 à 8 813 €).
6. Le double run de 4 800 € compté, et dit neutre pour la comparaison.
7. L'engagement ferme de 3 ans de B signalé comme coût de sortie si l'effectif baisse.
8. La base HT dite, avec la condition (TVA récupérée).
9. Les coûts internes (administration, formation) listés, chiffrés ou marqués non chiffrés.
10. Le piège du prix affiché relevé : B est 18 % moins cher par agent mais plus cher au total avec le connecteur.
11. Pas de recommandation : le skill compare, c'est `offer-comparison` ou `decision` qui tranche.

## Une mauvaise sortie

- Un total de A sans la révision, ou avec une révision inventée à un taux autre que le plafond et 0 %.
- Un coût de reprise d'historique inventé.
- Des totaux faux (erreur d'addition) ou le passage à 50 agents appliqué à une seule offre.
- Un article de loi inventé ou faux.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 11) | Note |
|---|---|---|---|---|
