---
skill: tam-sam-som
famille: finance
ecrit: 2026-10-16
---

# Cas 1 — ordre de grandeur en mode flash pour un pitch

## Demande

> Mode flash, j'ai besoin d'un ordre de grandeur pour le pitch de vendredi. On vend un logiciel de gestion des plannings pour cabinets dentaires en France, 150 €/mois par cabinet. Mes données : environ 38 000 chirurgiens-dentistes libéraux, 1,6 praticien par cabinet en moyenne ; à peu près 40 % des cabinets ont un logiciel de gestion avec agenda intégré et ne changeront pas. Un rapport dit que le marché européen des logiciels dentaires pèse 1,2 Md€. Côté équipe : 3 commerciaux, environ 8 signatures par mois chacun. Horizon 3 ans.

## Valeurs de référence (calculées à la main, 2026-10-16 ; données fictives fournies par l'utilisateur)

| Élément | Valeur |
|---|---|
| Cabinets | 38 000 / 1,6 = **23 750** |
| TAM (bottom-up) | 23 750 × 150 × 12 = **42,75 M€/an** |
| SAM (60 % non équipés) | **25,65 M€/an** |
| SOM à 3 ans (capacité, sans attrition) | 3 × 8 × 36 = 864 cabinets × 1 800 € = **1,56 M€ d'ARR** ≈ 6 % du SAM |
| Top-down naïf | 1,2 Md€ × part France (≈ 15 % si supposée) ≈ 180 M€ : **tous logiciels dentaires**, pas les plannings seuls |

## Une bonne sortie contient

1. TAM ≈ 42,75 M€/an, calculé bottom-up, facteurs et unités (€/an) visibles.
2. SAM ≈ 25,65 M€/an avec le filtre des 40 % justifié.
3. SOM tiré de la capacité commerciale (≈ 864 cabinets, ≈ 1,56 M€ d'ARR à 3 ans), pas d'un pourcentage du marché.
4. Le chiffre de 1,2 Md€ jamais retenu comme TAM : son périmètre (Europe, toutes catégories de logiciels) est dit plus large, et l'écart au bottom-up expliqué.
5. Toute part France supposée (≈ 15 % par exemple) marquée comme hypothèse.
6. SOM ≤ SAM ≤ TAM respecté.
7. L'attrition et le temps de montée en charge des commerciaux signalés comme facteurs qui réduisent le SOM.
8. Avertissement « mode flash » limité aux chiffres de mémoire ; les données de l'utilisateur ne sont pas présentées comme « potentiellement périmées ».
9. Une fourchette ou les facteurs les plus sensibles nommés (praticiens par cabinet, taux d'équipement).
10. Les données à vérifier avant le pitch, avec une source publique proposée pour chacune.

## Une mauvaise sortie

- Le rapport à 1,2 Md€ retenu comme TAM, ou un TAM moyenné entre bottom-up et top-down.
- Un SOM de « 1 % du marché » sans raisonnement.
- Un TAM exprimé en cumul sur trois ans au lieu de €/an.

## Résultats

| Date | Version | Modèle | Critères tenus (sur 10) | Note |
|---|---|---|---|---|
