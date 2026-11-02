---
status: draft
skill: ix-skills:deliver
format: report
recipient: client (profil imposé : un lecteur sans Claude Code, qui lit la trace d'un sujet ; bénéfices concrets, peu de jargon)
---

# Lire une trace

Ce texte se lit seul. Il ne demande ni Claude Code, ni programme, ni autre document.

## À quoi sert une trace

Une trace est le journal d'un sujet : elle dit, étape par étape, **ce qui est entré, ce qui en est sorti, quel modèle d'intelligence artificielle a fait le travail, combien de temps cela a pris et combien cela a coûté, avec la façon dont ce coût a été connu**. Elle dit aussi quelles décisions ont été prises, quelles limites ont été atteintes, et ce qui a été figé ou tenu secret pendant le travail.

Vous lisez la trace de **votre** sujet, et seulement la sienne. Elle ne contient aucune pièce d'un autre sujet.

## Comment l'ouvrir

La trace est un fichier de texte (Markdown, extension `.md`), nommé `trace.md`, à la racine du dossier de votre sujet. Ouvrez-le avec n'importe quel éditeur de texte ou avec un navigateur. Elle est faite de **tableaux** : chaque colonne a un nom en première ligne, et chaque ligne décrit une chose (une étape, un skill, une décision…). Elle est écrite par des outils, pas à la main : elle ne contient jamais de case vide, une valeur absente est dite comme telle.

Les tableaux portent des titres numérotés :

| Titre | Ce qu'il contient |
|---|---|
| T1. Sujet | l'identité du sujet : titre, type, qui le pilote, date de début |
| T2. Plafonds appliqués | les limites fixées avant de commencer (nombre de tentatives, de tours) |
| **T3. Étapes** | **le cœur : une ligne par étape, avec entrée, sortie, modèle, durée, jetons, coût** |
| T4. Skills | les méthodes utilisées à chaque étape, avec leur version |
| T5. Sous-agents | les assistants lancés pendant une étape, avec leur modèle |
| T6. Pauses et décisions | les décisions prises par une personne |
| T7. Plafonds atteints et suites | les fois où une limite a été atteinte, et ce qui a été choisi ensuite |
| T8. Sujets enfants | les sujets lancés à part à partir de celui-ci |
| T9. Gel et scellés | ce qui a été figé, et ce qui a été tenu secret jusqu'à la fin du jugement |
| T10. Lancements du script de recette | chaque contrôle automatique lancé pendant la production |
| T11. Points à confirmer et écarts | les décisions prises au plus étroit faute de réponse, les chemins qui n'ont pas été ouverts, les écarts au cadrage |

## Trouver une étape dans T3

La table T3 a une ligne par étape, dans l'ordre. La **première ligne est toujours l'étape 0** : la demande, séparée des pièces. Pour trouver une étape, regardez deux colonnes :

- `étape` : son numéro (`0`, `1a`, `1b`, `1c`, `1d`, `1e`, `2A`, `2B`, `3`, `4`, `5`, `6`, `7`) ;
- `occurrence` : ce qui distingue plusieurs lignes d'une même étape (`passe 1`, `passe 2`, `tour 3`…). Le couple `étape` + `occurrence` ne désigne qu'une seule ligne.

Par exemple, la deuxième tentative de l'évaluation du cadrage est la ligne dont `étape` vaut `1d` et `occurrence` vaut `passe 2`.

Les valeurs d'`occurrence` que vous rencontrerez :

| `occurrence` | Ce que c'est |
|---|---|
| `unique` | l'étape n'a qu'une ligne |
| `rédaction 2` | l'étape qui écrit a été refaite après un défaut relevé par l'étape qui vérifie |
| `passe 1`, `passe 2` | une tentative d'une étape qui **vérifie** (l'évaluation du cadrage, la vérification du goal, la contre-vérification) ; le nombre de passes est borné par une limite fixée avant de commencer |
| `gel`, `regel 1` | le moment où les contrôles ont été figés, puis refigés après une dérogation |
| `tour 3` | un tour de la session de production (étape `4`) ou de correction (étape `6`) |
| `gel du livrable 1` | le livrable a été enregistré et étiqueté avant d'être jugé |
| `appel du juge 1` | un appel du juge (étape `5`) |

## Lire une ligne de T3

| Colonne | Ce qu'elle vous dit |
|---|---|
| `entrée` | les documents que l'étape a reçus (chemins de fichiers du dossier du sujet) |
| `sortie` | les documents que l'étape a produits |
| `agent` | qui a travaillé : un assistant (avec son contexte, « neuf » ou « repris »), ou `humain` |
| `modèle` | le modèle d'intelligence artificielle utilisé (par exemple « Opus 5.5 ») ; `humain` si c'est une personne |
| `durée` | le temps écoulé à l'horloge |
| `jetons` | la quantité de texte traitée, en « jetons » (des morceaux de mots) ; plus c'est grand, plus l'étape a traité de matière |
| `portée_jetons` | ce que compte ce nombre : un seul appel, le cumul d'un assistant qui a travaillé plusieurs fois, ou une session entière |
| `coût` | le coût en dollars, équivalent au prix public de l'API |
| `source_coût` | **comment ce coût est connu** : `mesuré`, `estimé` ou `n.c.` |
| `méthode_coût` | la méthode de l'estimation, ou la raison pour laquelle le coût n'est pas connu |
| `inclus_dans` | quand le nombre de jetons ou le coût est `inclus dans la session` : le numéro de la ligne qui porte la mesure (ou `n.c.` si cette mesure n'a pas de ligne dans la trace) ; `sans objet` sinon |
| `cumule_de` | quand les jetons et le coût sont un cumul : le numéro de la ligne précédente que ce cumul inclut ; `sans objet` si la ligne part de zéro |
| `note` | un commentaire qui aide à lire la ligne |

## Lire le coût, et sa source

Le coût n'est jamais donné seul : sa colonne `source_coût` dit s'il faut le croire à la lettre.

- **`mesuré`** : l'outil qui a fait le travail a rendu lui-même le montant. C'est une mesure.
- **`estimé`** : on l'a calculé à partir du nombre de jetons et du prix public. C'est une estimation, et la colonne `méthode_coût` dit comment on l'a faite et ce qu'elle ignore (par exemple la part du travail déjà en mémoire, que l'outil ne détaille pas). Elle peut s'écarter du coût réel.
- **`n.c.`** : non communiqué. L'outil n'a pas donné le coût ; la colonne `méthode_coût` en donne la raison (par exemple : un essai à blanc où aucun assistant réel n'a été appelé, ou un travail fait par abonnement). Il n'y a pas de montant, et on n'en a pas inventé.

## Les marques de valeur absente

Une cellule n'est jamais vide. Quand une valeur manque, on trouve :

- `n.c.` : l'outil ne la donne pas ;
- `inclus dans la session` : le travail n'a pas de mesure propre, il est compris dans la mesure d'une autre ligne, en général celle d'une session plus large ; la colonne `inclus_dans` donne le numéro de cette ligne, ou `n.c.` quand elle n'est pas dans la trace ;
- `sans objet` : la valeur n'existe pas pour cette ligne (par exemple, des jetons pour une étape faite par une personne).

## Les trois niveaux de détail

Toutes les étapes ne sont pas mesurées au même niveau. La colonne `granularité` le dit :

- `appel` (étapes 0 à 3) : une ligne par appel à un assistant, avec son propre temps et son coût ; les jetons ne sont pas toujours relevés par l'outil, et la ligne le dit (`n.c.` et la raison dans `note`) ;
- `session` (production et correction, étapes 4 et 6) : une ligne pour toute la session de travail, avec le temps et les jetons relevés, un coût **estimé**, et les assistants lancés listés à part dans T5, avec leur modèle et **sans coût individuel** ;
- `étape` (jugement, étape 5) : une ligne pour le jugement pris comme un tout, ses assistants listés de même dans T5.

## Le coût d'une étape qui a plusieurs lignes

Certaines étapes ont plusieurs lignes (deux passes, plusieurs relevés d'une longue session). Pour en connaître le coût :

1. Prenez toutes les lignes de T3 dont `étape` est l'étape cherchée.
2. Pour chaque ligne, retenez sa **mesure propre**. Si la cellule est `inclus dans la session`, la ligne n'en a pas : sa mesure est dans la ligne que nomme `inclus_dans`. Sinon, si `cumule_de` vaut `sans objet`, c'est la valeur de la cellule. Sinon, c'est la valeur de la cellule moins celle de la ligne que nomme `cumule_de` (un relevé cumulé inclut le précédent : l'additionner tel quel le compterait deux fois). Faites la même chose pour les jetons.
3. Additionnez les mesures propres qui sont des nombres. Les lignes qui n'en ont pas (`inclus dans la session`, `n.c.`) restent hors du compte : le total est alors partiel, et la trace doit le dire.
4. Le total est aussi fiable que sa ligne la moins fiable : `estimé` si une des lignes l'est, `mesuré` sinon.

Les assistants que lance un assistant (T5) n'ont jamais de ligne propre en T3 ni de coût propre : leur coût est dans la ligne qui les a lancés.

## Retrouver ce qui a été décidé, limité ou tenu secret

- **T6** : pour chaque question tranchée par une personne : la décision, qui l'a prise, et d'où elle vient. `réponse` veut dire que la personne a répondu ; `défaut accepté` que la réponse proposée par défaut a été gardée sans remarque (la colonne `à rappeler` vaut alors `oui`, pour que la personne puisse la corriger).
- **T10** : les lancements du script de contrôle pendant la production. Le harnais n'assiste pas à ces lancements, qui se font dans la session de production : sa table dit « aucun lancement du script de recette consigné » ; les tours, eux, sont comptés en T3 (étapes `4` et `6`).
- **T7** : quand une limite a été atteinte, ce qui restait en échec, les suites proposées et celle choisie : relancer (quelques tours de plus, nombre fixé par le pilote), contourner (revoir un critère, avec la raison), livrer avec une réserve (écrite dans la colonne `réserve`), ou abandonner. S'il n'y en a pas, la trace écrit « aucun plafond atteint ».
- **T9** : ce qui a été figé avant la production (les contrôles et leur référence), et ce qui a été tenu secret jusqu'à la fin du jugement : la part cachée du contrôle et la trace du juge. Tant qu'un élément est `scellé`, seule son empreinte (une signature numérique, sha256) est écrite : elle prouvera plus tard qu'il n'a pas changé. Une fois `ouvert`, son emplacement est donné et il fait partie de la trace.
- **T8** : s'il y a eu des sujets lancés à part, leur dossier est nommé. Leurs documents ne sont pas cités.
- **T4** : pour chaque ligne de T3, les méthodes (skills) utilisées, avec leur `version` et leur `empreinte_sha256`, pour savoir exactement quel texte a été appliqué.

## Un exemple de lecture

Question : « Quel modèle a fait la deuxième passe de l'évaluation, qu'a-t-elle reçu et produit, et combien a-t-elle coûté ? »

1. Ouvrir T3 et chercher la ligne où `étape` vaut `1d` et `occurrence` vaut `passe 2`.
2. Lire `entrée` et `sortie` : les fichiers reçus et produits.
3. Lire `modèle` : le modèle utilisé. Lire `jetons`, puis `portée_jetons` pour savoir ce que le nombre compte.
4. Lire `coût`, puis `source_coût`. Si c'est `n.c.`, lire `méthode_coût` : la raison pour laquelle aucun montant n'est donné. Si c'est `estimé`, lire la méthode avant de se fier au chiffre.
