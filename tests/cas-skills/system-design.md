---
skill: system-design
famille: tech
ecrit: 2026-10-16
---

# Cas 1 — Prise de rendez-vous pour un réseau de cabinets de kinésithérapie

## Demande

> Conçois l'architecture d'un service de prise de rendez-vous en ligne pour un réseau de 40 cabinets de kinésithérapie (600 praticiens, en moyenne 20 rendez-vous par praticien et par jour ouvré, 21 jours ouvrés par mois, 60 % des rendez-vous pris en ligne, réservations ouvertes de 8 h à 20 h). Rappel SMS la veille pour chaque rendez-vous ; notre fournisseur SMS facture 0,045 € HT le SMS. Équipe : 3 développeurs Python. Budget d'hébergement : 500 € par mois. Lancement dans 4 mois.

## Valeurs de référence

- 600 × 20 = **12 000 rendez-vous par jour** ; × 21 = **252 000 par mois**.
- Réservations en ligne : 12 000 × 0,6 = **7 200 par jour** ; sur 12 h (43 200 s) = **0,17 écriture par seconde** en moyenne, environ **0,8 par seconde** avec un pic × 5.
- SMS : 252 000 × 0,045 € = **11 340 € HT par mois**.

## Une bonne sortie contient

1. Une estimation de charge chiffrée et écrite, cohérente avec les valeurs ci-dessus, avec le facteur de pic dit et justifié.
2. Une conclusion tirée de cette charge : un monolithe et une base relationnelle suffisent, sans microservices. *(échoue probablement avec 1.1.1)*
3. Le coût des SMS (environ 11 340 € HT par mois) relevé comme sans commune mesure avec le budget d'hébergement de 500 €, avec une question bloquante (qui paie, quels rappels). *(échoue probablement avec 1.1.1)*
4. La double réservation d'un même créneau empêchée par une contrainte en base ou une transaction, avec le compromis choisi.
5. Des rappels SMS envoyés en lot, avec reprise sur erreur et sans double envoi (idempotence).
6. La question des données de santé et de l'hébergement certifié (RGPD art. 9, CSP L1111-8) posée comme contrainte à qualifier avant de choisir l'hébergeur, sans trancher à la place du DPO ; l'hébergement et la sauvegarde hors UE examinés (art. 44). *(échoue probablement avec 1.1.1)*
7. Pour chaque décision structurante : ce qui devient plus facile, plus difficile, et ce qu'on revoit avec la croissance. *(échoue probablement avec 1.1.1)*
8. Des choix techniques adaptés à 3 développeurs Python, dits dans les compromis.
9. Des questions ouvertes bloquantes listées avec qui répond (qui paie les SMS, fuseau horaire, annulations).
10. Les sorties nommées `system_design`, `modele_donnees`, `api_contracts` et `questions_ouvertes`, sans `trade_offs` ni `data_model` à part.

## Une mauvaise sortie

- Des microservices, une file de messages distribuée et Kubernetes pour 0,8 écriture par seconde au pic.
- Aucun chiffre de charge, ou une charge sans lien avec le choix d'architecture.
- Un article du RGPD ou du code de la santé publique cité de mémoire avec un mauvais numéro.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 10) | Note |
|---|---|---|---|---|
