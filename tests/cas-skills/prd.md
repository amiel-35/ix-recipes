---
skill: prd
famille: produit
ecrit: 2026-10-16
---

# Cas 1 — une demande de sponsor qui contient déjà une solution

## Demande

> Notre directeur des opérations veut « une appli mobile en React Native avec Firebase pour que les techniciens saisissent leurs rapports d'intervention, avec mode hors ligne ». Contexte : 120 techniciens, les rapports sont faits sur papier et ressaisis au bureau en moyenne 2 jours plus tard ; 8 % des factures d'intervention sont contestées par les clients parce que le rapport est illisible ou incomplet. Les rapports contiennent le nom du client, son adresse, et parfois une signature. Objectif de la direction : lancer avant l'été. Fais-moi le PRD.

## Une bonne sortie contient

1. Un problème qui chiffre ce que coûte le statu quo (délai de 2 jours, 8 % de factures contestées).
2. Des objectifs en résultats, chacun avec un seuil de succès, une cible haute, une méthode de mesure (outil, fenêtre) et une date d'évaluation ; la valeur de départ de 8 % est reprise, les cibles ne sont pas présentées comme validées.
3. React Native et Firebase absents des exigences : rangés en contrainte (si quelqu'un la justifie) ou en hypothèse, avec la question « qui l'impose et pourquoi ? ».
4. Le mode hors ligne écrit comme un besoin (saisir un rapport sans réseau), pas comme une technologie.
5. Des non-objectifs (3 à 5), chacun avec sa raison.
6. Une exigence sur les données personnelles : données collectées (nom, adresse, signature), finalité, durée de conservation, accès (RGPD art. 25 ou 5, ou la règle sans numéro marquée « à vérifier »).
7. Chaque exigence porte une étiquette « validé (source) » ou « hypothèse (comment la tester) » ; par exemple « chaque technicien a un smartphone professionnel » est une hypothèse.
8. Des priorités P0 / P1 / P2 justifiées par le test du P0, avec au moins un élément en P2 écrit comme assurance d'architecture (par exemple une autre plateforme ou une intégration à la facturation).
9. Des questions ouvertes marquées bloquantes ou non, avec qui répond.
10. « Avant l'été » traité comme une échéance, avec ce qui en dépend, et non comme une date de livraison acquise.
11. Aucune user story, aucun backlog ; `feature-spec` nommé comme étape suivante.

## Une mauvaise sortie

- « L'application sera développée en React Native avec Firebase » dans les exigences.
- Une cible chiffrée (« moins de 2 % de factures contestées ») sans base ni méthode de mesure ni date.
- Aucune mention des données personnelles, ou un article RGPD au numéro inventé.
- Une liste de user stories à la place des exigences.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 11) | Note |
|---|---|---|---|---|
