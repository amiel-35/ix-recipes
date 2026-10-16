---
skill: reformulation-us
famille: produit
ecrit: 2026-10-16
---

# Cas 1 — cinq user stories de natures différentes

## Demande

> Reformule ces US de notre backlog congés :
> 1. En tant qu'utilisateur, je veux que l'appli soit plus rapide.
> 2. En tant qu'admin, je veux un menu déroulant pour choisir le rôle d'un membre.
> 3. En tant que développeur, je veux migrer la base vers Postgres 16.
> 4. En tant que manager, je veux voir les congés de l'équipe, les valider et exporter le planning.
> 5. En tant que salarié, je veux poser une demi-journée de congé afin de ne pas consommer une journée entière.

## Une bonne sortie contient

1. L'US 1 placée dans `us_problematiques` (trop vague), avec la question qui la débloquerait (quel écran, quelle durée, mesurée comment), sans capacité inventée.
2. L'US 2 réécrite sur la capacité (« attribuer un rôle à un membre »), le menu déroulant gardé en note « solution suggérée ».
3. L'US 3 classée comme tâche technique, sans faux utilisateur ni faux bénéfice.
4. L'US 4 découpée en trois (consulter, valider, exporter), chacune avec ses critères.
5. L'US 5 gardée telle quelle (ou presque), avec seulement ses critères ajoutés.
6. Pour l'US 5, au moins un cas négatif dans les critères (solde insuffisant, demi-journée déjà posée).
7. L'erreur corrigée nommée pour chaque US réécrite ou écartée.
8. Aucun critère avec un mot vague (« rapide ») sans seuil ou sans question.

## Une mauvaise sortie

- Une capacité inventée pour l'US 1 (« charger la liste en moins de 2 s ») sans l'avoir demandée.
- Un utilisateur fictif pour la migration de base.
- L'US 5 réécrite de fond en comble.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 8) | Note |
|---|---|---|---|---|
