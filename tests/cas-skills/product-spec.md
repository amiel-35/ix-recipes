---
skill: product-spec
famille: produit
ecrit: 2026-10-16
---

# Cas 1 — un écran de liste avec des cas de volume et de droits

## Demande

> Écris la spec de l'écran « Mes factures » de notre espace client B2B : liste des factures, filtre par période, téléchargement du PDF, statut payé / en attente / en retard. Certains clients ont plus de 2 000 factures. Seuls les utilisateurs avec le rôle « Facturation » voient les montants.

## Une bonne sortie contient

1. Une `spec` principale lisible seule, qui annonce ses annexes (s'il y en a) et la raison de chacune.
2. Les états de la liste : chargement, vide, erreur, sans droit sur les montants.
3. Deux cas « vide » distincts : aucune facture (premier usage) et filtre sans résultat, avec un message et une action différents.
4. Les 2 000 factures traitées : pagination ou chargement progressif, avec un nombre par page.
5. La règle de calcul de « en retard » (échéance dépassée et non payée), avec la date de référence et le fuseau.
6. Le comportement pour le rôle sans « Facturation » (montants masqués ou écran refusé), posé en question ouverte si ce n'est pas tranché.
7. Un modèle de données de la facture : identifiant, numéro, dates, montant, statut et ses transitions, qui la voit.
8. Le cas de l'échec du téléchargement du PDF (erreur récupérable, action proposée).
9. Chaque règle porte une étiquette (décidé / hypothèse / ouvert).
10. Aucune annexe produite sans raison ; aucune mention de `spec_plan`.

## Une mauvaise sortie

- Une liste d'écrans sans états ni cas limites.
- « En retard » affiché sans règle de calcul.
- Une annexe pour chaque type possible, y compris ceux sans contenu.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 10) | Note |
|---|---|---|---|---|
