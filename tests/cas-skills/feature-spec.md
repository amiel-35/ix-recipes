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
