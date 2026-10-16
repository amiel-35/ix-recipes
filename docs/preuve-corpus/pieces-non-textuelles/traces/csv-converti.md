# Essai csv-converti

Pièces : budget-t3.T3.csv, budget-t3.Commentaires.csv  
Code de sortie : 0 ; coût : 0.0208 $

## Consigne

Le dossier courant contient la ou les pièces d'un dossier : budget-t3.T3.csv, budget-t3.Commentaires.csv. Lis-les avec l'outil Read. Si une lecture échoue, dis exactement ce que l'outil a répondu et n'invente rien. Réponds : (a) l'écart marketing ; (b) le total des charges, budget et réel ; (c) la date d'arrêté ; (d) la cause de l'écart marketing. Cite chaque valeur par fichier:ligne.

## Lectures (flux stream-json)

- `Read {"file_path": "/private/var/folders/fz/l9h9d2bx1kq0j9mt0fv9plfr0000gn/T/corpus-essai-30xstad2/budget-t3.T3.csv"}` → ok : "1\tSuivi budgétaire T3 2026 - k€ HT\n2\tPoste,Budget T3,Réel T3,Écart\n3\tChiffre d'affaires,2400,2310,-90\n4\tAchats matières,960,1010,50\n5\tMasse salariale,720,705,-15\n6\tMarketing,120,138,18\n7\tDéplacements,30,41,11\n8\tLoyers et charges,90,90,0\n9\tTotal charges,1920,1984,64\n10\t\n11\tArrêté au,2026-09-30\n12\t"
- `Read {"file_path": "/private/var/folders/fz/l9h9d2bx1kq0j9mt0fv9plfr0000gn/T/corpus-essai-30xstad2/budget-t3.Commentaires.csv"}` → ok : '1\tPoste,Cause\n2\tMarketing,"Salon Maison&Objet de septembre, décidé en juin, hors budget."\n3\tAchats matières,Prix du chêne +6 % depuis juillet.\n4\t'

## Réponse

Les deux fichiers se sont lus sans erreur.

**(a) Écart marketing :** +18 k€ HT. Le budget est de 120 et le réel de 138 (budget-t3.T3.csv:6).

**(b) Total des charges :**
- Budget : 1 920 k€ HT (budget-t3.T3.csv:9).
- Réel : 1 984 k€ HT (budget-t3.T3.csv:9).
- L'écart est de +64 k€ (budget-t3.T3.csv:9).

**(c) Date d'arrêté :** 2026-09-30 (budget-t3.T3.csv:11).

**(d) Cause de l'écart marketing :** « Salon Maison&Objet de septembre, décidé en juin, hors budget. » (budget-t3.Commentaires.csv:2)

Le total des charges (1 920 budget, 1 984 réel) ne correspond pas à la somme des lignes de charges. Les cinq lignes (achats matières, masse salariale, marketing, déplacements, loyers et charges) donnent 1 900 en budget (960+720+120+30+90) et 1 984 en réel (1010+705+138+41+90). Le réel s'additionne bien. Le budget du fichier est supérieur de 20 à la somme des lignes (budget-t3.T3.csv:4-9). Je n'ai pas d'explication de cet écart dans les pièces. Il faut donc vérifier le total budgétaire avant de s'en servir.
