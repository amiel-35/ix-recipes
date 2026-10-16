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
| 2026-10-16 | 1.1.0 | Sonnet 5.5 | 6.3 (6–7) | banc 3 passages, moyenne (min–max) ; erreurs relevées 0.3 (0–1) |
| 2026-10-16 | 1.2.0 | Sonnet 5.5 | **7.7 (6–9)** | banc 3 passages ; erreurs 0.0 (0–0) |
| 2026-10-16 | 1.1.0 | Haiku 5.5 | 3.0 (2–4) | banc 3 passages, moyenne (min–max) ; erreurs relevées 4.3 (2–6) |
| 2026-10-16 | 1.2.0 | Haiku 5.5 | **4.7 (4–5)** | banc 3 passages ; erreurs 8.7 (5–12) |

# Cas 3 — Grille pour trois offres d'infogérance (contrôle indépendant)

Écrit le 2026-10-16 sans voir le corps du skill, à partir de sa seule description.

## Demande

> On est une ETI de 220 salariés sur trois sites (Lyon, Grenoble, Annecy). On a consulté pour l'infogérance de notre parc : support aux utilisateurs, supervision des serveurs, gestion des postes. On a reçu trois offres. On veut s'engager sur 3 ans maximum. Volume actuel : 55 tickets par mois en moyenne sur les 12 derniers mois. Le comité de sélection (DSI, DAF, RSSI, une responsable de site) se réunit le 3 novembre : construis la grille de notation pour scorer ces offres.
>
> - Offre A : 4 200 € HT par mois, engagement 36 mois, frais de mise en place 9 000 € HT, 60 tickets par mois inclus, délai d'intervention garanti de 4 h ouvrées, support de 8 h à 18 h, équipe en France. Société de 140 salariés.
> - Offre B : 3 600 € HT par mois, engagement 48 mois, frais de mise en place 18 000 € HT, 40 tickets par mois inclus puis 45 € HT par ticket supplémentaire, délai d'intervention garanti de 2 h ouvrées, support de 8 h à 19 h, centre de support de niveau 1 situé à Casablanca. Société de 600 salariés.
> - Offre C : 4 900 € HT par mois tout compris, tickets illimités, engagement 24 mois, pas de frais de mise en place, délai d'intervention garanti de 1 h, 24 h/24 et 7 j/7. Société de 9 salariés créée en 2023.
>
> Le DAF penche pour B, « la moins chère ».

## Valeurs de référence

Coût total sur l'horizon commun de 36 mois, au volume actuel de 55 tickets par mois (B paie 15 tickets supplémentaires par mois, soit 675 € HT) :

| Offre | Mensuel facturé | Coût sur 36 mois | Coût sur l'engagement exigé |
|---|---|---|---|
| A | 4 200 | 4 200 × 36 + 9 000 = 160 200 | 160 200 (36 mois) |
| B | 3 600 + 675 = 4 275 | 4 275 × 36 + 18 000 = 171 900 | 223 200 (48 mois) |
| C | 4 900 | 4 900 × 36 = 176 400 | 117 600 (24 mois), reconduction à prix inconnu |

- Classement au prix d'abonnement affiché : B < A < C. Classement au coût sur 36 mois : A < B < C.
- Note prix avec la formule proportionnelle (prix le plus bas / prix de l'offre × 10), sur le coût à 36 mois : A 10 ; B 9,32 ; C 9,08. Sur le seul mensuel affiché (à ne pas faire) : B 10 ; A 8,57 ; C 7,35.

Textes vérifiés le 2026-10-16 : C. trav. L8222-1, R8222-1 (vérifications obligatoires dès 5 000 € HT), D8222-5 (attestation de vigilance à la conclusion puis tous les six mois), L8222-2 (solidarité financière ; nouvelle rédaction au 26 déc. 2026 qui conserve le principe) ; RGPD art. 28 et 44.

## Une bonne sortie contient

1. Sépare les critères éliminatoires (conformes / non conformes) des critères pondérés, avec au moins : engagement compatible avec les 3 ans maximum, attestation de vigilance URSSAF remise à la signature puis tous les six mois (obligatoire au-delà de 5 000 € HT, sous peine de solidarité financière en cas de travail dissimulé du prestataire), accord de sous-traitance des données personnelles conforme à l'art. 28 du RGPD.
2. Donne des pondérations qui totalisent 100 %, fixées avant la notation et accompagnées de la consigne de ne pas les modifier après avoir vu les notes.
3. Définit une échelle de notation dont chaque niveau est décrit par un constat observable (ce qui vaut 1, 3, 5…), au moins pour les critères qualitatifs.
4. Fait noter le prix sur le coût total au même horizon de 36 mois, frais de mise en place et tickets hors forfait au volume réel compris, et non sur l'abonnement affiché ; en tire que A (160 200 €) est moins chère que B (171 900 €), contrairement à l'intuition du DAF.
5. Traite l'engagement de 48 mois de B : élimination au regard de la limite de 3 ans, ou condition à négocier avant notation ; s'il est conservé, son coût sur la durée exigée (223 200 €) apparaît.
6. Écrit la formule de notation du prix et en montre l'effet sur les trois offres (par exemple A 10, B 9,32, C 9,08 en formule proportionnelle), en signalant qu'elle resserre les écarts et que la pondération du prix doit en tenir compte.
7. Transforme la qualité de service en critères mesurables : délai d'intervention et de rétablissement, plages couvertes, pénalités en cas de non-respect, rapports d'activité.
8. Inclut un critère de solidité et de continuité du prestataire (taille, ancienneté, comptes, plan de continuité), pertinent pour l'offre C (9 salariés, créée en 2023).
9. Inclut un critère sur la localisation des données et des accès et l'encadrement des transferts hors UE (RGPD, chapitre V), pertinent pour le support de niveau 1 de B à Casablanca, et un critère de réversibilité en fin de contrat.
10. Prévoit une notation individuelle par chaque membre du comité avant consolidation, une case de justification par note, et ne désigne pas de lauréat : la grille est l'outil, la décision revient au comité.

## Forme attendue

1. Les critères éliminatoires forment un bloc placé avant la grille pondérée, sous forme de liste conforme / non conforme par offre, avec pour chacun la pièce justificative attendue.
2. La grille pondérée est un tableau réutilisable avec les colonnes : critère, pondération en %, mode de mesure, note par offre (A, B, C), note pondérée, justification ; une ligne de total pondéré la ferme.
3. Les critères pondérés sont regroupés par famille (coût, qualité de service, solidité du prestataire, sécurité et données, réversibilité) avec un sous-total de pondération par famille, le total faisant 100 %.
4. L'échelle de notation est présentée en tableau à part (niveau, descripteur observable), par critère qualitatif ou en échelle commune à laquelle chaque critère renvoie.
5. Les données des offres (coût sur 36 mois, engagement, délais garantis, plages, tickets inclus) sont reprises dans un tableau comparatif séparé de la grille, avec l'horizon et le volume de calcul (55 tickets par mois) écrits en tête.
6. Le mode d'emploi pour le comité est séparé de la grille : étapes dans l'ordre (contrôle éliminatoire, notation individuelle, consolidation, discussion des écarts de notes), et une fiche de notation individuelle vierge à remplir par chaque membre.

## Une mauvaise sortie

- Note le prix sur l'abonnement mensuel affiché et donne la meilleure note prix à B.
- Produit une liste de critères pondérés sans échelle décrite, sans critères éliminatoires ni attestation de vigilance.
- Remplit la grille et annonce l'offre gagnante à la place du comité.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 10) | Note |
|---|---|---|---|---|
| 2026-10-16 | 1.1.0 | Sonnet 5.5 | 6.0 (5–7) | banc 3 passages, moyenne (min–max) ; erreurs relevées 0.7 (0–1) |
| 2026-10-16 | 1.2.0 | Sonnet 5.5 | **8.7 (8–9)** | banc 3 passages ; erreurs 0.7 (0–1) |
| 2026-10-16 | 1.1.0 | Haiku 5.5 | 1.3 (1–2) | banc 3 passages, moyenne (min–max) ; erreurs relevées 8.7 (7–10) |
| 2026-10-16 | 1.2.0 | Haiku 5.5 | **4.3 (4–5)** | banc 3 passages ; erreurs 11.7 (10–13) |
| 2026-10-16 | sans skill | Sonnet 5.5, effort medium | 4.8 (4.5–5.5) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 0.3 (0.0–1.0) /6 ; coût moyen 0.067 $ |
| 2026-10-16 | 1.1.0 | Sonnet 5.5, effort medium | 6.5 (6.0–7.0) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 2.0 (1.5–2.5) /6 ; coût moyen 0.065 $ |
| 2026-10-16 | 1.2.0 | Sonnet 5.5, effort medium | 8.2 (7.5–9.0) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 0.0 (0.0–0.0) /6 ; coût moyen 0.107 $ |
| 2026-10-16 | sans skill | Sonnet 5.5, effort high | 5.8 (5.0–6.5) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 0.7 (0.0–1.0) /6 ; coût moyen 0.121 $ |
| 2026-10-16 | 1.1.0 | Sonnet 5.5, effort high | 6.8 (6.5–7.0) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 2.2 (1.5–3.0) /6 ; coût moyen 0.109 $ |
| 2026-10-16 | 1.2.0 | Sonnet 5.5, effort high | 7.8 (7.5–8.0) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 0.3 (0.0–1.0) /6 ; coût moyen 0.173 $ |
| 2026-10-16 | sans skill | Opus 5.5 | 6.5 (6.5–6.5) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 0.0 (0.0–0.0) /6 ; coût moyen 0.145 $ |
| 2026-10-16 | 1.1.0 | Opus 5.5 | 7.3 (7.0–8.0) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 2.7 (2.0–3.0) /6 ; coût moyen 0.177 $ |
| 2026-10-16 | 1.2.0 | Opus 5.5 | 8.0 (7.0–9.0) | banc « valeur », 3 passages, juges Opus et Sonnet ; forme 0.7 (0.0–1.0) /6 ; coût moyen 0.311 $ |
