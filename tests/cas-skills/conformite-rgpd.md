---
skill: conformite-rgpd
famille: juridique
ecrit: 2026-10-16
---

# Cas 1 — Application de coaching sportif avec plan généré par IA et appels commerciaux

## Demande

> Check RGPD de notre nouvelle version avant mise en prod le 1er novembre 2026. Appli B2C de coaching sportif (SAS, 25 salariés, France). Inscription dès 13 ans. On collecte : e-mail, téléphone, date de naissance, poids, fréquence cardiaque et sommeil via la montre connectée de l'utilisateur. Nouveauté : un plan d'entraînement généré par IA à partir de ces données. Hébergement AWS (région Francfort), support client sur Zendesk (société américaine), Google Analytics sur le site et dans l'appli. Le marketing veut appeler à partir du 1er novembre les anciens abonnés qui ont résilié pour leur proposer -50 % ; les numéros viennent du formulaire d'inscription, sans case de consentement à la prospection.

## Une bonne sortie contient

1. Qualifie le poids, la fréquence cardiaque et le sommeil en données de santé (art. 9) et exige une exception de l'art. 9(2), vraisemblablement le consentement explicite.
2. Registre des traitements requis malgré moins de 250 salariés (art. 30(5) : données de l'art. 9, traitement non occasionnel).
3. AIPD à mener ou à justifier (art. 35, liste CNIL), présentée comme « à confirmer », avec la raison.
4. Utilisateurs de 13-14 ans : art. 8 du RGPD et art. 45 de la loi de 1978 (âge de 15 ans), consentement conjoint avec le titulaire de l'autorité parentale.
5. Appels aux anciens abonnés : depuis le 11 août 2026, un consentement préalable est obligatoire (C. conso. L223-1) ; l'exception du contrat en cours ne joue pas pour des abonnés qui ont résilié ; le projet n'est pas conforme en l'état ; c'est un point séparé, comme les cookies.
6. N'invoque pas l'opposition (liste d'opposition au démarchage) comme régime applicable aux appels vers des consommateurs.
7. Google Analytics : point séparé relevant de l'art. 82 de la loi de 1978 et de la CNIL.
8. Zendesk : transfert hors EEE (certification DPF à vérifier à la date de l'analyse, sinon clauses contractuelles types et analyse d'impact du transfert) ; AWS Francfort : contrat de sous-traitance art. 28 ; chaque sous-traitant est nommé.
9. Procédure de violation de données : notification à la CNIL sous 72 heures (art. 33).
10. Date de référence ; chaque point cite son article ; statut en place / à faire / à confirmer.
11. Une seule mention de la limite juridique.

## Une mauvaise sortie

- Traite les appels aux anciens abonnés comme un simple droit d'opposition, ou comme couverts par l'exception du contrat en cours.
- Dit que le registre n'est pas obligatoire parce que l'entreprise a moins de 250 salariés.
- Présente le projet européen « omnibus » comme déjà en vigueur.
- Répète trois ou quatre fois que le document ne remplace pas un DPO.
- Cite des articles qui n'existent pas.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 11) | Note |
|---|---|---|---|---|

# Cas 2 — Éditeur de paie agissant comme sous-traitant (cas de contrôle)

## Demande

> On est un éditeur de logiciel de paie (SAS, 40 salariés). Nos clients, des employeurs, nous confient les données de leurs salariés ; on les héberge et on génère les bulletins. Nouveau module : envoi des bulletins par e-mail via un prestataire d'emailing américain. On veut la checklist RGPD avant la sortie du module.

## Une bonne sortie contient

1. Qualifie notre rôle en sous-traitant pour les données des salariés des clients, et le prestataire d'emailing en sous-traitant ultérieur.
2. Place base légale, information des personnes, AIPD et notification à l'autorité dans la colonne du responsable de traitement (les clients), et non dans la liste du sous-traitant.
3. Liste les obligations propres du sous-traitant : contrat art. 28, registre des catégories d'activités de traitement (art. 30(2)), sécurité (art. 32), alerte du responsable sans délai en cas de violation (art. 33(2)).
4. Sous-traitant ultérieur : autorisation écrite préalable du client, spécifique ou générale (avec information des changements et droit d'opposition), mêmes obligations en cascade (art. 28(2) et (4)).
5. Transfert vers les États-Unis : adéquation limitée aux destinataires certifiés DPF, à vérifier à la date de l'analyse, sinon garanties de l'art. 46.
6. Ne dit pas que le registre est facultatif en raison de l'effectif.
7. Date de référence, article cité pour chaque point, statut défini ; une seule mention de la limite juridique.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 7) | Note |
|---|---|---|---|---|
