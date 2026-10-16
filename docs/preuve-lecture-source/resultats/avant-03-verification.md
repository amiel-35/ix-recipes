# Fact-check: Commentaire des écarts, T3 2026

## Synthèse / Summary
15 affirmations : 9 confirmées, 0 contredite, 3 absentes de la source, 3 non vérifiables.

Les plus risquées sont trois ajouts qu'un lecteur prendrait pour établis :
- le « ralentissement durable de la demande » (A3) ;
- la « tolérance de 10 % » sur les dépenses commerciales (A10), qui sert à conclure que l'écart marketing est acceptable (A11) ;
- les « déplacements » (A15), poste que la source ne nomme pas.

## Affirmations contredites / Contradicted
Aucune.

## Ajoutées, absentes de la source / Not in the source
- A3 — Le recul du chiffre d'affaires traduit un ralentissement durable de la demande. La source donne l'écart du chiffre d'affaires sans cause. Recherché : « demande », « ralentissement », « durable », « cause » dans la ligne Chiffre d'affaires et dans toute la source.
- A10 — Une tolérance de 10 % est fixée pour les dépenses commerciales. Recherché : « tolérance », « 10 % », « seuil », « dépenses commerciales » dans toute la source. Seul le pourcentage d'écart du marketing (+6,7 %) y figure.
- A15 — Les déplacements font partie des autres postes. La source ne cite aucun poste « déplacements ». Recherché : « déplacements », « frais ». Elle dit seulement « Autres postes : proches du budget. »

## Confirmées / Confirmed
- A1 — Le chiffre d'affaires du trimestre s'établit à 2 310 k€ — source : « réel 2 310 k€, budget 2 400 k€, écart −90 k€ (−3,75 %) »
- A2 — Il est en retrait de 90 k€ sur le budget (−3,75 %) — source : « écart −90 k€ (−3,75 %) »
- A5 — Les achats matières dépassent le budget de 50 k€ — source : « Achats matières : réel 1 010 k€, budget 960 k€, écart +50 k€ (+5,2 %) ; cause : prix du chêne. »
- A6 — Ce dépassement vient de la hausse du prix du chêne — source : « cause : prix du chêne ». C'est une reformulation fidèle. La source ne dit pas « hausse », mais le sens de l'écart (+50 k€) l'implique.
- A7 — Le marketing dépasse son budget de 8 k€ (+6,7 %) — source : « Marketing : réel 128 k€, budget 120 k€, écart +8 k€ (+6,7 %) »
- A8 — Ce dépassement vient du salon Maison&Objet — source : « cause : salon Maison&Objet. »
- A12 — La masse salariale est inférieure de 15 k€ au budget — source : « Masse salariale : réel 705 k€, budget 720 k€, écart −15 k€ (−2,1 %). »
- A13 — Les autres postes sont conformes au budget — source : « Autres postes : proches du budget. » Nuance : « conformes » est plus fort que « proches », mais je le tiens pour une reformulation acceptable.
- A14 — Le commentaire ne contredit aucun chiffre repris de l'analyse. Cette entrée regroupe la vérification croisée des montants : 2 310, 90, 50, 8 et 15 k€, ainsi que −3,75 % et +6,7 %. Le détail est dans A1, A2, A5, A7 et A12.

## Non vérifiables / Not checkable
- A4 — Il faudra intégrer ce recul dans la révision du budget 2027 (recommandation).
- A9 — L'écart marketing « reste dans la tolérance » (A11 ci-dessous). Une telle conclusion repose sur A10 et n'est pas contrôlable sans cette règle.
- A11 — L'écart marketing reste dans la tolérance de 10 %. Le calcul +6,7 % < 10 % est exact, mais la tolérance n'est pas dans la source (voir A10). C'est un jugement dérivé d'un fait absent.

## Limites / Limits
La source tient en cinq lignes d'analyse, sans en-têtes. Elle paraît complète, mais elle est brève : les verdicts d'absence valent pour ce seul texte. Le mode est `closed`. Aucun budget 2027, aucune règle de tolérance ni aucune donnée de demande n'y figurent.

## HANDOFF
### verdicts
```json
{"mode": "closed", "verdicts": [
{"id": "A1", "claim": "CA du trimestre = 2 310 k€", "verdict": "confirmed", "quote": "réel 2 310 k€, budget 2 400 k€, écart −90 k€ (−3,75 %)"},
{"id": "A2", "claim": "CA en retrait de 90 k€ sur budget (−3,75 %)", "verdict": "confirmed", "quote": "écart −90 k€ (−3,75 %)"},
{"id": "A3", "claim": "Le recul traduit un ralentissement durable de la demande", "verdict": "not_in_source", "quote": ""},
{"id": "A4", "claim": "À intégrer dans la révision du budget 2027", "verdict": "not_checkable", "quote": ""},
{"id": "A5", "claim": "Achats matières dépassent le budget de 50 k€", "verdict": "confirmed", "quote": "Achats matières : réel 1 010 k€, budget 960 k€, écart +50 k€ (+5,2 %) ; cause : prix du chêne."},
{"id": "A6", "claim": "Dépassement dû à la hausse du prix du chêne", "verdict": "confirmed", "quote": "cause : prix du chêne"},
{"id": "A7", "claim": "Marketing dépasse son budget de 8 k€ (+6,7 %)", "verdict": "confirmed", "quote": "Marketing : réel 128 k€, budget 120 k€, écart +8 k€ (+6,7 %)"},
{"id": "A8", "claim": "Dépassement marketing dû au salon Maison&Objet", "verdict": "confirmed", "quote": "cause : salon Maison&Objet."},
{"id": "A9", "claim": "L'écart marketing reste dans la tolérance (jugement)", "verdict": "not_checkable", "quote": ""},
{"id": "A10", "claim": "Tolérance de 10 % fixée pour les dépenses commerciales", "verdict": "not_in_source", "quote": ""},
{"id": "A11", "claim": "Écart marketing dans la tolérance de 10 %", "verdict": "not_checkable", "quote": ""},
{"id": "A12", "claim": "Masse salariale inférieure de 15 k€ au budget", "verdict": "confirmed", "quote": "Masse salariale : réel 705 k€, budget 720 k€, écart −15 k€ (−2,1 %)."},
{"id": "A13", "claim": "Les autres postes sont conformes au budget", "verdict": "confirmed", "quote": "Autres postes : proches du budget."},
{"id": "A14", "claim": "Les montants et pourcentages repris sont exacts", "verdict": "confirmed", "quote": "réel 2 310 k€, budget 2 400 k€, écart −90 k€ (−3,75 %)"},
{"id": "A15", "claim": "Les déplacements font partie des autres postes", "verdict": "not_in_source", "quote": ""}
]}
```

## SUMMARY
15 affirmations vérifiées en mode fermé : 9 confirmées, 0 contredite, 3 absentes de la source, 3 non vérifiables.
Ajouts à risque : « ralentissement durable de la demande » (A3), « tolérance de 10 % » (A10) et « déplacements » (A15).
La conclusion « dans la tolérance » (A9, A11) repose sur la règle de 10 %, absente de la source.
Tous les chiffres repris sont exacts. « Conformes » (A13) dit un peu plus que « proches du budget ».