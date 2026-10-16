---
skill: mockup
famille: produit
ecrit: 2026-10-16
---

# Cas 1 — une maquette de discussion avec trois états

Cas à jouer seulement si la question 12 de la revue garde le skill. Les critères ci-dessous ne portent que sur ce que la version 1.2.0 écrit ; le socle d'accessibilité, la charte et le format français sont en attente de cette décision.

## Demande

> Maquette HTML de la page « Mes factures » de notre espace client, pour la réunion de jeudi. Montre la liste normale (une dizaine de factures), le cas « aucune facture » et le cas « erreur de chargement ». Je ne t'ai pas dit comment filtrer par période : propose quelque chose.

## Une bonne sortie contient

1. Un seul fichier HTML, CSS en ligne, lisible sans réseau (police système en repli, pas de CDN).
2. Les trois états visibles et accessibles sans modifier le code (sections empilées ou sélecteur).
3. Le filtre par période, que la demande n'a pas défini, marqué visiblement à l'écran comme proposé (contour en pointillés et mention « à confirmer »).
4. Une légende en haut de page qui explique la marque.
5. Des factures avec de vrais libellés et des données plausibles (pas de lorem ipsum).
6. Des boutons nommés par leur action (« Télécharger le PDF »), pas « Valider » ou « Submit ».
7. Une mise en page lisible à 375 px de large comme à 1 280 px.
8. Ce que la demande énonce (liste, trois états) montré sans la marque « à confirmer ».

## Une mauvaise sortie

- Seule la liste normale, les deux autres états laissés en commentaire.
- Un filtre présenté comme acquis, sans marque.
- Une police ou une feuille de style chargée depuis un CDN.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 8) | Note |
|---|---|---|---|---|
