# A3 : format de trace

Ce document décrit comment on tient la **trace d'un sujet** traité avec la procédure « traiter un sujet de bout en bout ». Une trace dit, pour chaque étape, ce qui y est entré, ce qui en est sorti, quel modèle l'a faite, combien elle a duré et coûté, et avec quels skills et quels réglages. Elle permet de rejouer le même déroulé et de l'auditer.

**Pour qui.** Amiel, qui audite ; un client, qui lit la trace de son seul sujet ; le constructeur d'un harnais, qui doit pouvoir écrire et lire cette trace par programme. Le lecteur n'a besoin ni de Claude Code ni d'un programme : la trace est du Markdown, qui s'ouvre dans un éditeur de texte ou un navigateur.

**Forme.** Des tableaux Markdown. Chaque tableau a un titre fixe (« T1 » à « T11 »), des colonnes nommées, et **un champ par colonne**. Les noms de colonnes ci-dessous sont le contrat : un programme les lit tels quels, sans deviner. L'ordre des colonnes est libre ; les noms ne changent pas. Les réglages cités (plafonds, modèles, suites) sont ceux de `partie-a/A4-reglages.yaml` : leurs valeurs ne sont écrites que là, la trace en consigne la version et, pour les plafonds, la valeur appliquée au moment du passage.

## 1. Confinement

Trois règles, qui valent pour toutes les traces :

1. **Une trace par sujet, dans le dossier du sujet.** Elle tient en un fichier, ou en plusieurs extraits (un par phase) qui suivent les mêmes titres et les mêmes colonnes ; ensemble, ils forment la trace. Pour la lire, on réunit les lignes de chaque table dans tous les extraits : les identifiants `ligne` sont uniques dans cet ensemble.
2. **Aucune copie hors de ce dossier.** La trace désigne les pièces par un chemin relatif au dossier du sujet et n'en recopie pas le contenu dans un autre sujet. Une pièce d'un client ne sort pas de son dossier.
3. **Aucun renvoi à une pièce d'un autre sujet.** Seul le renvoi aux sujets enfants est permis (table T8) : il nomme le dossier de l'enfant, il ne cite aucune de ses pièces.

## 2. Valeurs absentes

On n'invente aucune valeur. Quand une valeur manque, on l'écrit ainsi, jamais par une cellule vide :

| Marque | Sens | Où la raison s'écrit |
|---|---|---|
| `n.c.` | non communiqué : l'outil qui a fait l'appel ne l'expose pas | dans la colonne `note` (pour un coût, dans `méthode_coût`) |
| `inclus dans la session` | l'appel n'a pas de mesure propre : elle est comprise dans la mesure d'une autre ligne, en général une ligne de granularité `session` | la colonne `inclus_dans` de T3 : l'identifiant de cette ligne, ou `n.c.` quand cette mesure n'est pas une ligne de la trace (la session de pilotage n'a pas de ligne) ; la raison d'un `n.c.` s'écrit dans `note` |
| `sans objet` | la valeur n'existe pas pour cette ligne (par exemple les jetons d'une étape faite par une personne) | — |

## 3. Les trois granularités de l'audit

La colonne `granularité` de la table T3 prend trois valeurs. Elles viennent de la décision d'audit du cadrage clos (D6 et LR3).

| Granularité | Étapes | Ce que la ligne mesure | Les sous-agents |
|---|---|---|---|
| `appel` | 0 à 3 | un appel d'agent : entrée, sortie, modèle, durée, jetons, coût | l'appel est la ligne ; ses sous-agents éventuels sont listés en T5 |
| `session` | 4 et 6 | la session entière : durée et jetons relevés, coût **estimé** et marqué comme tel | listés en T5 avec leur modèle, **sans coût individuel** |
| `étape` | 5 | le jugement : une ligne par appel du juge lancé par le pilote (durée, jetons, coût) ; s'il y a plusieurs appels, `occurrence` les distingue | listés en T5 avec leur modèle, sans coût individuel |

**Qui lance l'appel.** Cette règle vaut à toutes les étapes, sans exception. Une ligne de T3 est un appel, une session ou un jugement **lancé par le pilote** (ou par la session de pilotage). Un appel lancé **par un agent**, pendant la ligne de cet agent, est un sous-agent : il n'a de ligne qu'en T5, sans coût individuel, et sa mesure est comprise dans la ligne qui l'a lancé. L'étape 6 a ses propres lignes (`étape` vaut `6`) ; elles ne sont jamais comprises dans une ligne de l'étape 4.

## 4. Les tables

### T1. Sujet

Une seule ligne. Elle ouvre la trace.

| Colonne | Contenu |
|---|---|
| `sujet` | identifiant du sujet (le nom de son dossier) |
| `titre` | titre court |
| `type_de_sujet` | une clé de `types_de_sujet` dans les réglages (par exemple `code`) |
| `pilote` | la personne qui pilote le sujet |
| `début` | date et heure de début, ISO 8601 |
| `version_réglages` | valeur de la clé `version` des réglages (A4) au lancement |
| `empreinte_réglages` | sha256 du fichier de réglages au lancement |
| `sujet_parent` | dossier du sujet parent, ou `sans objet` (renvoi, voir T8) |

### T2. Plafonds appliqués

Une ligne par plafond du fichier de réglages (clés sous `plafonds`) et par limite numérique de la production (par exemple les limites de sous-agents). La valeur est celle lue dans les réglages au lancement : la copier ici fixe ce qui a été appliqué, même si les réglages changent ensuite.

| Colonne | Contenu |
|---|---|
| `plafond` | nom de la clé sous `plafonds` dans les réglages |
| `valeur_appliquée` | la valeur lue dans les réglages au lancement |
| `atteint` | `oui` ou `non` ; `oui` renvoie à une ligne de T7 |

### T3. Étapes

Une ligne par appel, session ou jugement, **dans l'ordre**. **La première ligne est l'étape 0** (voir la règle ci-dessous). C'est la table que l'on lit pour savoir qui a fait quoi, quand et à quel coût.

| Colonne | Contenu |
|---|---|
| `ligne` | identifiant de la ligne, unique dans la trace (`L01`, `L02`…), cité par les autres tables |
| `étape` | numéro de l'étape de la procédure : `0`, `1a`, `1b`, `1c`, `1d`, `1e`, `2A`, `2B`, `3`, `4`, `5`, `6`, `7`, ou `pause 1` / `pause 2` pour une pause |
| `occurrence` | ce qui distingue plusieurs lignes d'une même étape : `passe 1`, `passe 2`, `tour 3`, `relevé après le tour 5`, `appel du juge 2`, `gel` (le gel de l'étape 3), `relecture de la grille` ; `unique` quand l'étape n'a qu'une ligne. Le couple (`étape`, `occurrence`) est **unique** dans la trace : il désigne une seule ligne |
| `granularité` | `appel`, `session` ou `étape` (section 3). Une ligne faite par une personne (étapes 0 et 7, pauses, gel) prend `appel` : une action = une ligne |
| `entrée` | les pièces reçues : chemins relatifs au dossier du sujet, séparés par `;` |
| `sortie` | les pièces produites : chemins relatifs, séparés par `;` |
| `agent` | le type d'agent et son contexte (`contexte neuf` ou `contexte repris`) ; `humain` pour une étape faite par une personne |
| `modèle` | le modèle qui a fait la ligne, avec sa version quand on la connaît (`Opus 5.5`) ; `humain` pour une personne |
| `réglages` | `version_réglages` en vigueur pour cette ligne |
| `durée` | durée à l'horloge (`2 min 28 s`) |
| `jetons` | le nombre rapporté par l'outil, écrit en chiffres seulement (les espaces entre les milliers ne comptent pas ; pas de suffixe comme « k »), ou une marque d'absence (section 2) |
| `portée_jetons` | `appel`, `cumul de l'agent` (un agent repris compte tout depuis son premier appel) ou `session` (tout depuis le début de la session). Cette portée vaut pour `jetons` **et** pour `coût` |
| `coût` | un montant en dollars équivalent API, écrit avec une virgule décimale et suivi de ` $` (`9,40 $`), ou une marque d'absence (section 2). Même portée que `jetons` |
| `source_coût` | `mesuré` (rendu par l'outil qui a fait l'appel), `estimé`, `n.c.`, ou `sans objet` (ligne faite par une personne) |
| `méthode_coût` | pour `estimé` : la méthode (jetons relevés × tarif public, avec la date du tarif et ce qu'on ignore, comme la part servie par le cache) ; pour `n.c.` : la raison ; pour `mesuré` : l'outil qui l'a rendu |
| `inclus_dans` | quand `jetons` ou `coût` vaut `inclus dans la session` : la `ligne` qui porte la mesure, ou `n.c.` quand cette mesure n'est pas une ligne de la trace ; `sans objet` sinon |
| `cumule_de` | quand les `jetons` et le `coût` de la ligne sont cumulés (portée `cumul de l'agent`, ou `session` pour un relevé qui en suit un autre) : la `ligne` précédente que ce cumul inclut, ou `n.c.` quand le cumul part d'un appel qui n'est pas une ligne de la trace (la raison s'écrit dans `note`) ; `sans objet` pour une ligne qui part de zéro (portée `appel`, premier relevé d'une session, premier appel d'un agent) |
| `note` | ce qui aide à lire la ligne : constats, écarts à la procédure, motif d'une valeur absente |

**Règle de l'étape 0.** La première ligne de T3 est l'étape 0, le brief : la demande, séparée des pièces. Sa `entrée` liste la demande puis les pièces, chacune par son chemin ; sa `sortie` dit où la demande et les pièces sont rangées, séparément. Si l'étape 0 est faite par une personne, `agent` et `modèle` valent `humain`, `jetons` vaut `sans objet`.

**Coût.** Il porte toujours sa source. `mesuré` : l'outil l'a rendu. `estimé` : on l'a calculé à partir des jetons et du tarif public ; la `méthode_coût` est obligatoire et dit ce qu'elle ignore. `n.c.` : l'outil ne l'expose pas ; la `méthode_coût` en donne la raison. Une estimation ne se présente jamais comme une mesure.

**Exemple fictif**, sur un sujet imaginaire, pour montrer la forme (les valeurs ne sont pas des mesures) :

| ligne | étape | occurrence | granularité | entrée | sortie | agent | modèle | réglages | durée | jetons | portée_jetons | coût | source_coût | méthode_coût | inclus_dans | cumule_de | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L01 | 0 | unique | appel | `demande.md` ; `pieces/` | `demande.md` ; `pieces/` | humain | humain | 1.0.0 | sans objet | sans objet | sans objet | sans objet | sans objet | personne : aucun appel d'outil | sans objet | sans objet | demande séparée des pièces |
| L02 | 1a | unique | appel | `demande.md` | `cadrage.md` | agent généraliste, contexte neuf | Opus 5.5 | 1.0.0 | 5 min 18 s | 188 191 | appel | n.c. | n.c. | l'outil de pilotage ne rend pas les dollars | sans objet | sans objet | exemple fictif |
| L03 | 1c | unique | appel | `cadrage.md` | `fusion.md` | session de pilotage | Opus 5.5 | 1.0.0 | 2 min | inclus dans la session | session | n.c. | n.c. | l'outil de pilotage ne rend pas les dollars | n.c. | sans objet | la session de pilotage n'a pas de ligne dans cette trace ; exemple fictif |
| L04 | 4 | relevé après le tour 3 | session | `goal.md` | `livrable/` | agent de production, contexte repris | Sonnet | 1.0.0 | 1 h 12 min | 2 400 000 | session | 9,40 $ | estimé | jetons × tarif public du 2026-10-17 ; part du cache inconnue | sans objet | sans objet | exemple fictif |
| L05 | 4 | relevé après le tour 5 | session | `goal.md` | `livrable/` | agent de production, contexte repris | Sonnet | 1.0.0 | 1 h 50 min | 3 650 000 | session | 14,10 $ | estimé | jetons × tarif public du 2026-10-17 ; part du cache inconnue | sans objet | L04 | cumul depuis le début de la session : la mesure propre de L05 est 3 650 000 − 2 400 000 jetons et 14,10 $ − 9,40 $ ; exemple fictif |

Dans cet exemple, le coût de l'étape 4 se lit ainsi : mesures propres L04 = 9,40 $ et L05 = 14,10 $ − 9,40 $ = 4,70 $, total 14,10 $, `estimé`. L'étape 1c n'a pas de total propre (voir la section 6).

### T4. Skills

Une ligne par skill utilisé par une ligne de T3. Les sous-agents de T5 qui appliquent un skill y ont leur ligne aussi (renvoyer à la ligne de T3 qui les a lancés).

| Colonne | Contenu |
|---|---|
| `ligne` | la ligne de T3 qui a utilisé le skill |
| `skill` | l'identifiant complet (`ix-skills:cadrage`) |
| `version` | la version du skill, lue dans son en-tête |
| `empreinte_sha256` | le sha256 du texte du skill tel que lu au moment de l'appel |
| `fichier` | le chemin du texte lu, ou `n.c.` si le skill est chargé par la plateforme |
| `note` | motif d'une valeur absente, ou usage particulier (par exemple un mode choisi par le message) |

Un skill dont on ne connaît ni la version ni l'empreinte garde sa ligne, avec `n.c.` dans les deux colonnes et la raison dans `note`.

### T5. Sous-agents

Une ligne par sous-agent, **avec son modèle et sans coût individuel**. Un sous-agent est un appel lancé par un agent, et non par le pilote (section 3) : à toutes les étapes, il n'a de ligne qu'ici. Son coût est compris dans la ligne de T3 qui l'a lancé : un appel d'agent aux étapes 0 à 3, la session aux étapes 4 et 6, l'appel du juge à l'étape 5. Un appel lancé par le pilote, à n'importe quelle étape, est une ligne de T3 et n'est pas listé ici.

| Colonne | Contenu |
|---|---|
| `ligne` | la ligne de T3 (appel, session ou jugement) qui a lancé le sous-agent |
| `rôle` | ce que le sous-agent a fait : lire, expertiser, relire, juger un thème, jouer le test du nouveau venu |
| `modèle` | le `model` explicite de l'appel |
| `objet` | l'objet de l'appel, en une phrase |
| `résultat` | le chemin de ce qu'il a rendu, ou son résumé en une phrase |

### T6. Pauses et décisions

Une ligne par question tranchée à une pause.

| Colonne | Contenu |
|---|---|
| `pause` | `1`, `2`… |
| `question` | l'identifiant et l'énoncé de la question |
| `décision` | ce qui a été décidé |
| `source` | `réponse` (le décideur a répondu, ses mots cités), `défaut accepté` (la réponse par défaut proposée, sans remarque du décideur), ou `confirmé en bloc` |
| `décideur` | la personne qui a tranché |
| `date` | date ISO |
| `à rappeler` | `oui` pour une décision venue d'un silence, que le pilote rappelle à la clôture ; `non` sinon |

### T7. Plafonds atteints et suites

Une ligne par plafond atteint. S'il n'y en a aucun, la section porte la phrase « aucun plafond atteint » et pas de tableau.

| Colonne | Contenu |
|---|---|
| `ligne` | la ligne de T3 où le plafond est atteint |
| `plafond` | la clé du plafond dans les réglages |
| `constat` | dernier résultat, ce qui reste en échec, ce qui est livré |
| `suites_proposées` | les suites offertes à ce plafond, lues dans les réglages |
| `suite_choisie` | `relancer`, `contourner`, `livrer_avec_reserve` ou `abandonner` (les noms des suites dans les réglages) |
| `tours_ajoutés` | pour `relancer`, le nombre de tours supplémentaires fixé par le pilote à ce moment ; `sans objet` sinon |
| `dérogation` | pour `contourner`, le critère revu et la raison (retour en 2B) ; `sans objet` sinon |
| `réserve` | pour `livrer_avec_reserve`, le texte de la réserve ; `sans objet` sinon |
| `décideur` | la personne qui a choisi |
| `date` | date ISO |

### T8. Sujets enfants

Une ligne par sujet enfant lancé à partir de ce sujet. Il n'y en a pas de gérés par la procédure dans sa première version (réglage `sujets_enfants`) : la table sert quand le pilote lance une partie découpée comme un sujet distinct. S'il n'y en a aucun, la section porte la phrase « aucun sujet enfant » et pas de tableau.

| Colonne | Contenu |
|---|---|
| `enfant` | identifiant du sujet enfant |
| `dossier` | le dossier du sujet enfant, relatif au dossier de ce sujet ou à son parent commun |
| `ligne` | la ligne de T3 où la découpe a été décidée |
| `motif` | le test de découpage qui l'a justifiée |

Aucune pièce de l'enfant n'est citée ici (règle 3 de la section 1).

### T9. Gel et scellés

Une ligne par élément figé ou scellé. C'est ici que vivent la **part cachée** et la **trace du juge**.

| Colonne | Contenu |
|---|---|
| `élément` | `script de recette`, `grille visible`, `fixtures`, `part cachée`, `trace du juge`, ou un autre élément figé |
| `état` | `figé` (lisible, mais interdit de modification), `scellé` (hors de portée du producteur) ou `ouvert` |
| `empreinte_sha256` | le sha256 relevé au gel ou au scellement |
| `emplacement` | le chemin de l'élément tant qu'il est `figé` ou `ouvert` ; pour un élément `scellé`, **`non écrit`** |
| `ligne` | la ligne de T3 où il a été figé ou scellé |
| `ouvert_à` | pour un élément `scellé`, la ligne de T3 ou la date de son ouverture ; `à venir` tant qu'il est scellé |

Règles du scellé :

- La part cachée et la trace du juge sont tenues **hors de ce que lit le producteur** jusqu'à la **fin du jugement**. Leur chemin n'est pas écrit dans la trace tant qu'elles sont `scellées` : la trace que le producteur lit ne doit pas le lui apprendre. Seule l'empreinte sha256 y figure, pour prouver plus tard qu'elles n'ont pas changé.
- À la fin du jugement, le pilote passe la ligne à `ouvert`, écrit l'`emplacement` et verse la pièce dans le dossier du sujet. Elles entrent alors dans la trace complète que le client lit.
- Les appels du juge sont des lignes de T3 comme les autres (étape 5, granularité `étape`). Leur contenu, qui montrerait la part cachée, est tenu à la place scellée : la ligne de T3 porte `scellé, voir T9` dans `sortie`.

### T10. Lancements du script de recette

Une ligne par lancement du script de recette pendant la production (étape 4) ou la correction (étape 6).

| Colonne | Contenu |
|---|---|
| `ligne` | la ligne de T3 (session) qui contient le lancement |
| `tour` | numéro du tour de la boucle au moment du lancement, ou le nombre de fois où l'agent a rendu la main si le numéro est inconnu |
| `commande` | la commande exacte du lancement |
| `code_sortie` | le code de sortie du script |
| `vérifications` | le nombre de vérifications exécutées (il ne baisse jamais d'un lancement à l'autre) |
| `échecs` | le nombre d'échecs |
| `durée_relevée` | la durée de la session relevée à ce moment |
| `jetons_relevés` | les jetons de la session relevés à ce moment |

### T11. Points à confirmer et écarts

Une ligne par point que la production ou une étape a dû marquer à part : une décision prise au plus étroit faute de réponse (« à confirmer »), un chemin hors du périmètre autorisé qui s'est présenté et n'a pas été ouvert, un écart au cadrage avec sa raison. S'il n'y en a aucun, la section porte la phrase « aucun point à confirmer ».

| Colonne | Contenu |
|---|---|
| `ligne` | la ligne de T3 pendant laquelle le point est apparu |
| `nature` | `à confirmer`, `chemin hors périmètre` ou `écart au cadrage` |
| `description` | le point, en une ou deux phrases |
| `raison` | pourquoi : la décision prise au plus étroit, ou la règle du cadrage mise en cause |
| `confirmé_par` | la personne qui a tranché ensuite et la date, ou `à venir` |

## 5. Rejouer le même déroulé

La reproductibilité vise le **même déroulé**, pas le même livrable. Pour rejouer un sujet, on relit dans la trace : les entrées de chaque étape (T3, `entrée`), le modèle de chaque appel (T3, `modèle`), chaque skill avec sa version et son empreinte (T4), la version des réglages (T1, T3 `réglages`) et les plafonds appliqués (T2). Si une empreinte d'un skill ou des réglages a changé depuis, le rejeu n'est plus identique ; la trace le montre.

## 6. Lire la trace par un programme

Un programme n'a besoin d'aucune heuristique.

**Une ligne.**

1. Trouver le titre de niveau 3 qui commence par « T3. », prendre le tableau qui le suit (dans tous les extraits, section 1).
2. Lire la ligne d'en-tête : ses cellules sont les noms de colonnes.
3. Choisir la ligne par `ligne`, ou par `étape` et `occurrence` (par exemple `étape` = `1d` et `occurrence` = `passe 2`) : ce couple désigne une seule ligne.
4. Le **modèle** est la cellule de la colonne `modèle`. Le **coût** est la cellule de la colonne `coût` quand `cumule_de` vaut `sans objet` ; sinon la cellule est un cumul, et le coût propre de la ligne se calcule comme à l'alinéa suivant (point 2). Sa fiabilité se lit dans `source_coût` (`mesuré`, `estimé` ou `n.c.`) et `méthode_coût`.
5. Pour les skills d'une ligne, filtrer T4 sur `ligne` ; pour ses sous-agents, filtrer T5 sur `ligne`.

**Une étape** (le coût, les jetons, les modèles d'une étape). Cette procédure vaut pour toute étape, même à une seule ligne.

1. Réunir les lignes de T3 dont `étape` vaut l'étape demandée.
2. Pour chaque ligne et pour chacune des deux grandeurs, `jetons` et `coût`, lire la **mesure propre** :
   - si la cellule vaut `inclus dans la session` : la ligne n'a pas de mesure propre ; la mesure est dans la ligne que nomme `inclus_dans` (ou hors trace si `inclus_dans` vaut `n.c.`) ;
   - sinon, si `cumule_de` vaut `sans objet` : la valeur de la cellule ;
   - sinon : la valeur de la cellule moins la valeur de la même colonne dans la ligne que nomme `cumule_de` (si l'une des deux est une marque d'absence, ou si `cumule_de` vaut `n.c.`, la mesure propre est `n.c.`).
3. Le **total** de l'étape est la somme des mesures propres numériques. Les lignes dont la mesure propre n'est pas un nombre (`inclus dans la session`, `n.c.`, `sans objet`) sont nommées à côté du total, qui est alors un total partiel, sauf deux cas où rien ne manque au compte : une ligne `inclus dans la session` dont `inclus_dans` nomme une ligne de la même étape, déjà comptée, et une ligne `sans objet` faite par une personne ; une étape dont aucune ligne n'a de mesure propre numérique n'a pas de total propre. Un total n'est jamais présenté comme complet quand une ligne reste hors du compte.
4. La fiabilité du coût total est la plus faible des `source_coût` des lignes comptées, et, pour une ligne cumulée, de celle de la ligne que nomme `cumule_de` (`mesuré`, puis `estimé`).
5. Les **modèles** de l'étape sont les valeurs de `modèle` de ses lignes, une par ligne ; il n'y a pas de modèle unique quand elles diffèrent. Ses sous-agents sont les lignes de T5 dont `ligne` est l'une de ses lignes : leur mesure est déjà dans ces lignes.

Une cellule vaut une marque d'absence (section 2) quand la valeur manque ; elle n'est jamais vide.
