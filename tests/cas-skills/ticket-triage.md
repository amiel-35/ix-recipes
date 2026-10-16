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
| 2026-10-16 | 1.1.2 | Sonnet 5.5 | 5.7 (5–6) | banc 3 passages, moyenne (min–max) ; erreurs relevées 2.3 (2–3) |
| 2026-10-16 | 1.2.0 brouillon | Sonnet 5.5 | 10.0 (10–10) | banc 3 passages ; erreurs 0.0 (0–0) |
| 2026-10-16 | 1.2.0 | Sonnet 5.5 | **9.3 (8–10)** | banc 3 passages, après correction ; erreurs 0.3 (0–1) |
| 2026-10-16 | 1.1.2 | Haiku 5.5 | 4.7 (4–5) | banc 3 passages, moyenne (min–max) ; erreurs relevées 3.0 (2–4) |
| 2026-10-16 | 1.2.0 brouillon | Haiku 5.5 | 6.3 (5–8) | banc 3 passages ; erreurs 4.7 (2–7) |
| 2026-10-16 | 1.2.0 | Haiku 5.5 | **7.7 (7–8)** | banc 3 passages, après correction ; erreurs 2.3 (0–4) |

# Cas 3 — Bulletins de paie d'une autre société visibles dans le portail (contrôle indépendant)

Écrit le 2026-10-16 sans voir le corps du skill, à partir de sa seule description.

## Demande

> Triage ce ticket, s'il te plaît. On est l'éditeur d'un portail en ligne où les cabinets d'expertise comptable et leurs clients déposent et consultent les documents de paie.
>
> Ticket n° 48213 — reçu le 16/10/2026 à 10 h 12 par le formulaire de support — priorité choisie par le client : Basse — catégorie choisie : Affichage
> De : Sophie Marchal, responsable paie, cabinet Avenel & Associés (client Premium, 180 dossiers de paie)
> Objet : petit souci d'affichage dans l'espace documents
>
> « Bonjour, ce matin vers 9 h 40, en ouvrant l'espace documents du dossier de notre client Boulangerie Ferrand, j'ai vu dans la liste trois bulletins de paie de septembre qui ne sont pas à eux : des noms de salariés que je ne connais pas, d'une société Transports Lemoine qui n'est pas un de nos dossiers. En cliquant, le PDF s'ouvre normalement, avec le nom, l'adresse et le numéro de sécurité sociale du salarié. Ma collègue a eu la même chose sur un autre dossier. Rien d'urgent pour nous, on a contourné en filtrant par période, mais je préfère vous le signaler. Capture jointe. »
>
> Contexte ajouté automatiquement : version 4.18 du portail déployée ce jour à 7 h 05 (changement principal : nouveau cache de la liste des documents). Page de statut : tous les services opérationnels.

## Une bonne sortie contient

1. Classe le ticket en P1 (priorité la plus haute) en écartant explicitement la priorité « Basse » choisie par la cliente et l'argument du contournement.
2. Le catégorise comme incident de sécurité et violation de données personnelles (divulgation non autorisée de données d'une autre société, au sens de l'art. 4, 12 du RGPD), et non comme un défaut d'affichage.
3. Justifie la gravité par des éléments du ticket : données d'un autre client (cloisonnement rompu), présence du numéro de sécurité sociale, nom et adresse, document ouvrable, reproduit par deux utilisatrices sur deux dossiers, donc probablement systémique.
4. Relie l'incident au déploiement de la version 4.18 à 7 h 05 (nouveau cache de la liste) comme hypothèse principale, présentée comme une hypothèse.
5. Route immédiatement vers l'astreinte technique et vers la sécurité ou le DPO, et informe le responsable du compte, au lieu de laisser le ticket dans la file du support de niveau 1.
6. Propose une action de confinement immédiate (désactiver la liste des documents, revenir à la version précédente ou vider le cache) tout en conservant les journaux d'accès depuis 7 h 05 comme preuves.
7. Pose l'horloge réglementaire : l'éditeur, sous-traitant, doit notifier la violation dans les meilleurs délais à ses clients pour le compte desquels il traite ces données (RGPD art. 33, 2), les responsables de traitement ayant 72 heures pour notifier la CNIL (art. 33, 1) ; l'heure de prise de connaissance (10 h 12) et les faits sont documentés dès maintenant (art. 33, 5).
8. Liste les informations à recueillir pour la prise en charge : identifiants des dossiers et des utilisatrices, horodatages, documents vus ou téléchargés, capture, et l'étendue à mesurer (quels dossiers ont reçu une liste issue du cache depuis 7 h 05, quels documents ont été servis à qui).
9. Propose une réponse à la cliente qui ne minimise pas l'incident, la remercie, lui demande de conserver la capture sans la diffuser et ne promet ni cause ni délai de correction.
10. S'en tient au triage de ce ticket entrant, sans rédiger de rétrospective d'incident.

## Une mauvaise sortie

- Garde P3 ou P4 « affichage » parce que la cliente dit que ce n'est pas urgent et qu'un contournement existe.
- Recommande de corriger le cache dans le prochain sprint, ou de revenir en arrière sans conserver les journaux.
- Traite le ticket comme un sujet purement technique, sans sécurité, DPO ni obligation de notification.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 10) | Note |
|---|---|---|---|---|
| 2026-10-16 | 1.1.2 | Sonnet 5.5 | 8.3 (8–9) | banc 3 passages, moyenne (min–max) ; erreurs relevées 0.0 (0–0) |
| 2026-10-16 | 1.2.0 brouillon | Sonnet 5.5 | 7.0 (7–7) | banc 3 passages ; erreurs 0.0 (0–0) |
| 2026-10-16 | 1.2.0 | Sonnet 5.5 | **10.0 (10–10)** | banc 3 passages, après correction (cas 3 lu avant la correction : plus indépendant) ; erreurs 0.0 (0–0) |
| 2026-10-16 | 1.1.2 | Haiku 5.5 | 3.0 (2–5) | banc 3 passages, moyenne (min–max) ; erreurs relevées 4.3 (2–7) |
| 2026-10-16 | 1.2.0 brouillon | Haiku 5.5 | 3.7 (3–4) | banc 3 passages ; erreurs 4.3 (3–7) |
| 2026-10-16 | 1.2.0 | Haiku 5.5 | **5.0 (4–6)** | banc 3 passages, après correction (cas 3 lu avant la correction : plus indépendant) ; erreurs 6.3 (6–7) |
