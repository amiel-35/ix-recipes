---
skill: ticket-triage
famille: tech
ecrit: 2026-10-16
---

# Cas 1 — Des factures d'une autre société visibles après une mise à jour

## Demande

> Triage ce ticket, reçu vendredi à 17 h 40 : "Bonjour, depuis la mise à jour de ce matin, quand je me connecte à notre espace client, je vois les factures d'une autre société (raison sociale, adresse, nom du contact, IBAN partiel). Deux collègues voient la même chose. Nous sommes client Premium. Merci de régler ça vite. — Julie, DAF."

## Valeurs de référence

72 heures à compter d'une prise de connaissance le vendredi à 17 h 40 : le lundi à 17 h 40, week-end compris (l'article 33 compte des heures, pas des jours ouvrés). Seule la qualification (responsable du traitement ou sous-traitant, début de la prise de connaissance) revient au DPO.

## Une bonne sortie contient

1. Priorité P1, justifiée (données exposées à un tiers, plusieurs utilisateurs, depuis une mise à jour).
2. Catégorie sécurité en principal, bug (régression probable) en secondaire, la cause étant étiquetée hypothèse.
3. Un routage vers la sécurité et l'ingénierie, plus le DPO ou le juridique.
4. La possible violation de données personnelles signalée (nom du contact), l'heure de réception notée, le délai de 72 heures (art. 33) rappelé, week-end compris, et la qualification renvoyée au DPO (responsable ou sous-traitant). *(échoue probablement avec 1.1.2)*
5. Le délai de première réponse P1 (1 heure) donné comme défaut à remplacer par celui de l'organisation ou du contrat Premium. *(échoue probablement avec 1.1.2)*
6. Doublon : la mention « doublon non vérifiable — aucune base fournie », jamais « pas de doublon » ; la remarque que d'autres clients sont probablement touchés depuis la mise à jour, ce qui déclenche une montée. *(échoue probablement avec 1.1.2)*
7. Une réponse au client qui accuse réception, annonce l'escalade et un délai de retour, sans hypothèse sur la cause, sans admission de responsabilité et sans qualifier l'événement de violation.
8. Aucune demande de captures d'écran des factures de l'autre société, qui propageraient la fuite ; au besoin, la demande de ne pas diffuser ni télécharger ces documents.
9. Une note interne qui propose d'envisager un retour arrière de la mise à jour.
10. Les sorties nommées `triage` et `questions_ouvertes`.

## Une mauvaise sortie

- Une priorité P2 parce que « le client peut encore travailler ».
- Un article du RGPD cité avec un mauvais numéro, ou la notification à la CNIL présentée comme décidée par le support.
- Une réponse qui dit « nous avons un problème de sécurité » ou qui explique la cause probable.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 10) | Note |
|---|---|---|---|---|
