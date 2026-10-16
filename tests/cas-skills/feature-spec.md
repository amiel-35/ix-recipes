---
skill: feature-spec
famille: produit
ecrit: 2026-10-16
---

# Cas 1 — un PO qui veut que tout soit Must

## Demande

> Spec fonctionnelle : export CSV des factures depuis l'espace client, pour nos clients PME qui l'envoient à leur expert-comptable. Sur 1 200 tickets « facturation » par trimestre, 30 % demandent un export. Il faut livrer avant le 15 janvier (clôtures annuelles). L'équipe voudrait aussi l'export PDF groupé et une API, et le PO considère que tout est Must.

## Valeurs de référence

- 30 % × 1 200 = **360 tickets d'export par trimestre** (base de la métrique de succès).

## Une bonne sortie contient

1. Le problème en 2 ou 3 phrases, avec la base de 360 tickets d'export par trimestre.
2. Une métrique de succès avec un seuil et une cible haute sous cette base, une méthode de mesure (catégorie de ticket, fenêtre) et une date d'évaluation.
3. Le « tout est Must » contesté : CSV en Must par le test du P0 (sans lui, le problème n'est pas résolu) ; export PDF groupé et API classés en Should, Could ou Won't, chacun avec sa raison.
4. L'API en « Won't (cette fois) » avec une ligne d'assurance d'architecture, ou en non-objectif avec sa raison.
5. Des user stories avec un utilisateur précis (gérant de PME, comptable) et une capacité sans élément d'interface.
6. Des critères Given/When/Then, dont un cas négatif (période sans facture, utilisateur sans droit).
7. Aucun mot vague sans chiffre (par exemple « export rapide » sans durée maximale).
8. Le format du fichier (séparateur, encodage, format des montants) posé en exigence ou en question bloquante.
9. Des questions ouvertes marquées bloquantes ou non, avec qui répond ; l'échéance du 15 janvier reprise avec ce qui en dépend.
10. Les choix non validés par l'équipe étiquetés (par exemple « Must (proposé, à confirmer) »).

## Une mauvaise sortie

- CSV, PDF et API tous en Must, sans test.
- « L'export doit être rapide » comme critère.
- Des critères qui ne couvrent que le chemin nominal.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 10) | Note |
|---|---|---|---|---|
| 2026-10-16 | 1.1.1 | Sonnet 5.5 | 7.0 (6–8) | banc 3 passages, moyenne (min–max) ; erreurs relevées 0.7 (0–1) |
| 2026-10-16 | 1.2.0 brouillon | Sonnet 5.5 | 9.0 (9–9) | banc 3 passages ; erreurs 0.3 (0–1) |
| 2026-10-16 | 1.2.0 | Sonnet 5.5 | **9.3 (9–10)** | banc 3 passages, après correction ; erreurs 1.0 (0–3) |
| 2026-10-16 | 1.1.1 | Haiku 5.5 | 4.0 (3–5) | banc 3 passages, moyenne (min–max) ; erreurs relevées 9.0 (6–11) |
| 2026-10-16 | 1.2.0 brouillon | Haiku 5.5 | 6.7 (6–7) | banc 3 passages ; erreurs 9.3 (9–10) |
| 2026-10-16 | 1.2.0 | Haiku 5.5 | **6.0 (5–7)** | banc 3 passages, après correction ; erreurs 7.7 (6–9) |

# Cas 3 — Relances automatiques des factures impayées (contrôle indépendant)

Écrit le 2026-10-16 sans voir le corps du skill, à partir de sa seule description.

## Demande

> Je suis PM chez un éditeur de logiciel de facturation en ligne pour TPE et PME (12 000 entreprises clientes, surtout des artisans et des sociétés de services). Il me faut la spec fonctionnelle de la feature « relances automatiques des impayés », avec user stories, MoSCoW, critères d'acceptation et métriques.
>
> Données : 38 % des factures émises par nos clients sont adressées à des particuliers, 62 % à des professionnels. 23 % des factures sont payées après l'échéance ; délai moyen de paiement constaté : 41 jours. 31 % de nos clients exportent leurs factures dans Excel pour relancer à la main ; « comment relancer » est le 2e motif de contact au support. Le rapprochement bancaire existe déjà : on sait quand une facture est payée, y compris partiellement. Le numéro SIREN du client final est un champ facultatif. Sur les factures, la mention des pénalités de retard est un texte libre que nos clients peuvent modifier ou supprimer.
>
> Ce que l'équipe et les clients demandent, en vrac :
> - relance par e-mail avant l'échéance (J−3) puis après (J+7, J+21) ;
> - ajouter automatiquement les pénalités de retard et l'indemnité de 40 € sur les relances ;
> - générer une mise en demeure en PDF à J+30 ;
> - relance par SMS ;
> - arrêter les relances dès que la facture est payée ;
> - modèles de relance personnalisables ;
> - un tableau de bord des encours ;
> - le CEO veut « pouvoir envoyer directement au contentieux, injonction de payer en ligne ».

## Valeurs de référence

- Taux de l'intérêt légal du second semestre 2026 (arrêté du 26 juin 2026) : 2,75 % lorsque le créancier n'est pas une personne physique agissant hors de ses besoins professionnels, 6,84 % sinon. Le créancier étant ici l'entreprise cliente, c'est 2,75 % qui s'applique, même quand le débiteur est un particulier.
- Plancher des pénalités de retard stipulées entre professionnels : 3 × 2,75 % = 8,25 % (C. com. L441-10, II). Taux par défaut sans stipulation : taux de refinancement de la BCE majoré de 10 points, celui du 1er janvier pour le premier semestre et du 1er juillet pour le second.
- Indemnité forfaitaire pour frais de recouvrement : 40 € (C. com. D441-5), due par un débiteur professionnel.

Textes vérifiés le 2026-10-16 : C. com. L441-9 et L441-10 (versions en vigueur depuis le 1er sept. 2026), D441-5 ; C. civ. 1231-6 ; C. mon. fin. L313-2 (deux taux légaux, fixés par arrêté, calculés chaque semestre).

## Une bonne sortie contient

1. Écrit des user stories au format « en tant que… je veux… afin de… », qui couvrent au moins l'entreprise qui relance et son client final destinataire de la relance.
2. Classe toutes les demandes en MoSCoW avec une justification, et place au moins l'envoi au contentieux ou l'injonction de payer en ligne en « Won't (pour cette version) » ou équivalent, avec la raison.
3. Rédige des critères d'acceptation Given/When/Then testables, avec des valeurs concrètes (date d'échéance, jour de relance, montant).
4. Distingue les débiteurs professionnels des particuliers et en tire la règle produit : l'indemnité de 40 € et les pénalités du code de commerce seulement pour un débiteur professionnel ; pour un particulier, à défaut de stipulation, des intérêts au taux légal à compter de la mise en demeure (C. civ. 1231-6) ; exige donc un champ qui qualifie le débiteur, le SIREN étant facultatif.
5. Fait calculer les pénalités sur le taux indiqué sur la facture (mention obligatoire entre professionnels, L441-9), à compter du lendemain de l'échéance, sans exiger de rappel préalable (L441-10) ; traite le cas où la mention a été supprimée ou est sous le plancher de 3 fois le taux légal (8,25 % au second semestre 2026).
6. Interdit de coder les taux en dur : taux légal et taux BCE sont des paramètres mis à jour chaque semestre.
7. Spécifie l'arrêt des relances et ses cas limites : paiement total (arrêt), paiement partiel (relance du solde seulement), avoir, facture contestée ou litige (suspension manuelle), plusieurs factures en retard pour un même client (regroupement ou non).
8. Donne des métriques de succès avec valeur de départ, cible et délai : par exemple part des factures payées en retard (23 % au départ), délai moyen de paiement (41 jours au départ), part des clients qui exportent vers Excel pour relancer (31 % au départ), contacts au support sur la relance ; plus au moins un garde-fou (taux de désactivation de la feature, plaintes ou désabonnements des destinataires).
9. Précise que la mise en demeure en PDF est générée par l'outil mais envoyée ou validée par l'utilisateur, et indique pour le particulier qu'elle fait courir les intérêts au taux légal.
10. Liste les exigences non fonctionnelles et les questions ouvertes (délivrabilité des e-mails, horaires d'envoi des SMS, journal des relances envoyées pour servir de preuve, validation juridique des modèles).

## Une mauvaise sortie

- Ajoute 40 € et des pénalités à toutes les relances, y compris celles adressées à des particuliers.
- Fixe le taux des pénalités en dur (« 3 fois le taux légal ») sans lire la mention de la facture ni prévoir de mise à jour semestrielle.
- Livre des critères d'acceptation vagues (« la relance part au bon moment ») et des métriques sans valeur de départ ni cible.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 10) | Note |
|---|---|---|---|---|
| 2026-10-16 | 1.1.1 | Sonnet 5.5 | 5.0 (4–6) | banc 3 passages, moyenne (min–max) ; erreurs relevées 0.0 (0–0) |
| 2026-10-16 | 1.2.0 brouillon | Sonnet 5.5 | 4.0 (3–5) | banc 3 passages ; erreurs 0.3 (0–1) |
| 2026-10-16 | 1.2.0 | Sonnet 5.5 | **4.3 (3–5)** | banc 3 passages, après correction (cas 3 lu avant la correction : plus indépendant) ; erreurs 0.7 (0–2) |
| 2026-10-16 | 1.1.1 | Haiku 5.5 | 2.0 (1–3) | banc 3 passages, moyenne (min–max) ; erreurs relevées 10.3 (8–12) |
| 2026-10-16 | 1.2.0 brouillon | Haiku 5.5 | 3.0 (1–4) | banc 3 passages ; erreurs 7.0 (6–9) |
| 2026-10-16 | 1.2.0 | Haiku 5.5 | **2.3 (2–3)** | banc 3 passages, après correction (cas 3 lu avant la correction : plus indépendant) ; erreurs 8.3 (6–12) |

# Cas 4 — spec d'écran avec ses états

Écrit le 2026-10-16 pour la fusion de `product-spec` dans `feature-spec` (version 2.0.0), à partir de la seule demande d'un écran, sans lire le corps du skill. Il vérifie que `feature-spec` couvre ce que faisait `product-spec` : les états d'une vue, les cas limites de contenu et la règle de calcul d'un statut dérivé.

## Demande

> Écris la spec de l'écran « Demandes de congés à valider », que verra chaque manager dans notre outil RH. Contexte : un manager voit la liste des demandes de congés en attente de son équipe, avec le nom du collaborateur, les dates, le nombre de jours, la date de la demande ; il peut accepter ou refuser (avec un motif) depuis la liste. Une demande en attente depuis plus de 5 jours ouvrés doit apparaître « à relancer ». Une équipe compte de 3 à 120 personnes. Les collaborateurs qui ne sont pas managers ne doivent pas voir cet écran. L'écran sera livré dans deux semaines à l'équipe de développement et à la designer.

## Valeurs de référence

- Seuil de relance : 5 jours ouvrés après la date de la demande (donnée de la demande).
- Taille d'équipe : de 3 à 120 personnes (donnée de la demande) : la liste peut dépasser une page.

## Une bonne sortie contient

1. Le même document couvre la feature (problème, périmètre, exigences, critères d'acceptation) et l'écran (états, données) ; il ne renvoie pas vers un autre skill pour l'écran.
2. Les états de la vue sont décrits un par un, avec ce que voit l'utilisateur et ce qu'il peut faire : chargement, erreur récupérable, absence d'accès, partiel ou désactivé.
3. Deux états vides distincts avec deux messages et deux actions : aucune demande en attente (rien à faire, état normal) et filtre ou recherche sans résultat.
4. L'absence de droits est un état : un collaborateur non manager n'accède pas à l'écran (message ou redirection, à préciser), et la donnée n'est pas non plus servie par l'interface de programmation.
5. Les cas limites de contenu sont réglés avec un chiffre quand il existe : nom très long, nombre de demandes (pagination ou chargement progressif, avec le nombre par page), plusieurs demandes d'un même collaborateur, dates qui se chevauchent, demande déjà traitée par un autre manager pendant que l'écran est ouvert.
6. Le statut « à relancer » est calculé par une règle écrite : comparaison (strictement plus de 5 jours ouvrés), date de départ (date de la demande), calendrier des jours ouvrés (jours fériés ?), date et fuseau horaire de référence. Les points qu'on ne peut pas trancher sont des questions ouvertes.
7. Le cycle de vie de la demande est donné : états (en attente, acceptée, refusée, annulée par le collaborateur), ce qui déclenche chaque transition, qui voit quoi, ce qui se passe quand le collaborateur annule une demande en attente.
8. Des critères d'acceptation Given/When/Then avec des valeurs concrètes, dont au moins un cas négatif (refus sans motif impossible, ou non-manager refusé), et une exigence de refus avec motif obligatoire ou non, posée comme question si l'énoncé ne tranche pas.
9. Chaque règle et chaque comportement porte une étiquette (décidé, hypothèse, proposé) ; les questions ouvertes sont classées bloquantes ou non, avec qui répond.
10. Pas de solution imposée à la designer (pas de description de composant), pas de métrique inventée sans valeur de départ (« à mesurer »).

## Une mauvaise sortie

- Décrit seulement le parcours nominal (la liste avec des demandes) et oublie les états vide, erreur et sans accès.
- Écrit « à relancer » sans règle de calcul, ou compte des jours calendaires sans le dire.
- Confond liste vide parce que rien à valider et liste vide parce qu'un filtre est actif.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 10) | Note |
|---|---|---|---|---|
| | | | | à jouer sur 2.0.0 avec `tests/cas-skills/banc.py` ; écrit avant la fusion, donc contrôle pour elle |
