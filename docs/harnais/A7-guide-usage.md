---
status: draft
skill: ix-skills:deliver
format: report
recipient: un humain qui ne connaît pas la procédure (profil imposé : bénéfices concrets, peu de jargon)
---

# A7 : guide d'usage du harnais

Ce guide explique comment mener un **sujet de code** avec le harnais, de la demande à la livraison, et comment répondre aux pauses et choisir une suite quand une limite est atteinte. Vous n'avez pas besoin de connaître la procédure avant de le lire. Pour lire la trace d'un sujet, un texte à part se lit seul : `docs/harnais/A7-lire-une-trace.md`.

## 1. L'idée en deux phrases

Un sujet passe par des étapes, dans le même ordre à chaque fois, avec les mêmes garde-fous, et ces garde-fous sont **interdits et détectés** : ce que le harnais compte, il le compte à votre place, ce qu'il fige, il le refuse à celui qui produit sous les formes qu'il reconnaît, et ce que ce refus laisse passer a un détecteur dont le moment est écrit (section 5, point 7). Le harnais n'*empêche* pas un processus du même compte système ; il le refuse et cherche à le voir. Chaque étape laisse une ligne dans une trace, que n'importe qui peut relire pour savoir ce qui a été fait, par quel modèle, et à quel coût.

**Mots à connaître.**

| Mot | Sens |
|---|---|
| sujet | ce qu'on veut obtenir, avec son dossier |
| demande | ce que vous voulez obtenir ; elle est séparée des pièces |
| pièces | le matériau fourni (cahier des charges, notes, données…) |
| pilote | la personne qui mène le sujet et tranche aux pauses : vous |
| cadrage | le document qui clarifie la demande avant de produire |
| goal | la mission écrite pour l'agent qui produit seul |
| critères, grille | ce qui dit si le travail est réussi ; une partie est visible, une partie est cachée |
| script de recette | le contrôle automatique des critères visibles |
| juge | l'agent distinct du producteur qui vérifie le travail |
| plafond | une limite (passes, tours) après laquelle on s'arrête |
| gel | le moment où le script, la grille et leurs fichiers ne peuvent plus être modifiés par celui qui produit |
| scellé | l'endroit, hors du dossier du sujet, où vit la part cachée jusqu'à la fin du jugement |
| trace | le journal du sujet |

## 2. Ce dont vous avez besoin

- Claude Code, Python 3 et git sur votre Mac.
- Le dépôt ix-recipes sur la branche du harnais. Dans ce guide, `$R` est son dossier.
- Un dossier **par sujet**, où vivra sa trace.
- Trois variables. Les deux premières vont dans le terminal où vous travaillez **et** dans celui où vous lancez la session de production ; la troisième, **dans le premier seulement** :

```bash
export R=~/Projets/ix-recipes                 # la racine d'ix-recipes (les deux terminaux)
export IX_SKILLS_PATH=~/.ix-skills/dist/skills  # les skills de l'amont, voir ci-dessous (votre terminal)
export IX_SCELLE_DIR=/chemin/que/vous/avez/choisi   # le scellé (VOTRE terminal seulement) : voir ci-dessous
```

Le scellé est un dossier que **vous** choisissez, **une fois**. Le harnais n'en propose aucun et n'en a aucun par défaut : un emplacement prévisible se trouve par une simple recherche. Prenez un nom tiré au hasard, hors de tout dépôt git et hors du dossier du sujet et du livrable, par exemple `mktemp -d "$HOME/.XXXXXXXXXXXXXXXX"` (il crée le dossier, en 0700, et écrit son chemin), puis gardez ce chemin dans votre profil de shell. **Ne l'écrivez dans aucun fichier du sujet, du livrable ou d'ix-recipes**, ni dans le goal. Le harnais refuse de travailler s'il manque, s'il est dans un dépôt git ou s'il est sous le dossier du sujet ou celui du livrable. Il y range, pour chaque sujet, un sous-dossier dont le nom est tiré au hasard (il ne se calcule pas depuis le chemin du sujet) et le tient dans un index à la racine du scellé.

**Gardez-le hors de la session de production.** Elle ne doit pas savoir où est la part cachée. N'exportez donc jamais `IX_SCELLE_DIR` dans le terminal d'où vous lancez cette session. Elle ne lance d'ailleurs aucune commande du harnais qui l'exige : ses tours sont comptés par des hooks (section 5). Au gel, le harnais écrit l'emplacement du scellé, en hexadécimal, dans `.claude/settings.json` du sujet, pour que ces hooks le trouvent ; le hook de la session refuse à celle-ci de lire ce fichier et de lire, lister ou chercher dans le scellé (`Read`, `Glob`, `Grep`, `find`, `grep -r`, `ls`, `cat`…). Ce refus lit des chemins et des mots de commande ; il ne voit pas une commande qui construit son chemin dans un interpréteur : c'est le résidu, dit dans `architecture-harnais.md` §8 et `spec-harnais.md` §6.2, avec, pour chaque geste, ce qui le détecte et quand (section 5, point 7). Vous lancez la session par `env -u IX_SCELLE_DIR claude …` si vous n'êtes pas sûr du terminal, et vous vérifiez avant : `env | grep -c IX_SCELLE_DIR` doit afficher `0` dans ce terminal.

Les skills de l'amont qui ne sont pas encore fusionnés dans ix-skills se lisent sur leur branche, sans rien écrire dans ix-skills :

```bash
"$R/harnais/preparer-skills.sh" ~/.ix-skills   # un dossier neuf
```

À chaque étape, vous lancez une commande, vous lisez ce que le harnais rend, et la trace se met à jour toute seule.

## 3. Mener un sujet de code, étape par étape

Le plafond de chaque boucle, le modèle de chaque rôle et chaque suite sont dans `docs/harnais/A4-reglages.yaml` : ne les cherchez pas ailleurs, et ne les retenez pas.

| Étape | Qui | Ce que vous faites |
|---|---|---|
| **0. Brief** | vous | Créez le dossier du sujet et posez-y `demande.md` (la demande, sans les pièces). Lancez `python3 "$R/harnais/harnais.py" lancer code` depuis ce dossier. Le harnais refuse un type qui n'existe pas ou qui n'est pas encore prêt, sans rien créer. |
| **1a à 1d** | des agents, l'un après l'autre | `python3 "$R/scripts/parcours.py" next amont` joue jusqu'à la prochaine pause. À la fin de 1a, validez la fiche de contexte (`validate amont`). L'évaluation du cadrage (1d) renvoie à la fusion (1c) si elle trouve un défaut, jusqu'au plafond de passes. |
| **Pause 1** | **vous** | Voir la section 4. |
| **1e, vérification de forme, 2A, 2B** | des agents | `next amont` joue la clôture du cadrage, la vérification de la liste « livrable vers skill de format », le goal et sa vérification, puis les critères. Le goal est écrit sans voir les critères, les critères sans voir le goal. La part cachée des critères quitte aussitôt le dossier du sujet. |
| **Contre-vérification** | **vous**, puis un autre modèle | La recette **s'arrête** avant : elle n'appelle jamais ce modèle. Demandez-vous si vous donnez votre accord ; si oui, appelez le modèle de contre-vérification avec le message que `parcours/amont/` annonce (il est dans le scellé : `python3 "$R/harnais/harnais.py" sceau` donne le dossier). Rendez sa sortie : `python3 "$R/harnais/harnais.py" contre-verif sortie.md`. Chaque sortie rendue compte une passe. |
| **3. Réconciliation** | un agent | `next amont` vérifie que la condition d'arrêt du goal renvoie au script et que chaque critère renvoie au cadrage. |
| **Pause 2** | **vous** | Voir la section 4. Puis écrivez le script de recette et la grille à partir de la grille visible. |
| **Gel** | vous | `python3 "$R/harnais/harnais.py" geler livrable grille.md acceptation.sh fixtures/exemples.txt` : le premier mot est le dossier du livrable, les suivants sont les fichiers à figer. Le harnais relève leurs empreintes, scelle la part cachée, ouvre la garde (le compteur de tours, au scellé) et déclare ses hooks (`PreToolUse`, `Stop`, `UserPromptSubmit`) dans `.claude/settings.json` du sujet. |
| **4. Production** | la session de production | Section 5. |
| **Fin de production** | vous (ou la session) | `python3 "$R/harnais/harnais.py" empreintes`, puis `python3 "$R/harnais/harnais.py" fin-production` : le livrable est commité et étiqueté. Rien ne le modifie plus avant le jugement. |
| **5. Jugement** | le juge | `python3 "$R/harnais/harnais.py" juge`. Le juge relance le script, répartit la relecture, joue le test du nouveau venu, et rend un verdict. Il est refusé si le livrable a bougé depuis son étiquette. |
| **6. Correction** | la session de production | Seuls les échecs reviennent, dans le fichier `constat-juge.md` : l'exigence de chaque ligne cachée en échec y est nommée, **sans son contenu**. |
| **Fin du jugement** | vous | `python3 "$R/harnais/harnais.py" ouvrir` : la part cachée et la trace du juge sont versées dans `jugement/`. Refusé tant que les tours de correction ne sont pas terminés. |
| **7. Livraison, terrain** | vous | Notez les défauts constatés à l'usage : ils servent à améliorer les grilles. |

## 4. Répondre aux pauses

Une pause est le moment où **vous** décidez : un agent peut vérifier qu'une question est posée, pas y répondre.

### Pause 1, après l'évaluation du cadrage

Vous recevez un cadrage avec des **questions bloquantes**, chacune accompagnée d'une réponse proposée par défaut (elles sont dans `parcours/amont/04-evaluation.md`). Pour chacune :

- répondez « oui » pour garder la réponse par défaut ; ou
- donnez votre réponse, avec vos mots : elle prime sur le défaut ;
- si vous ne dites rien, le défaut est gardé et marqué « défaut accepté ». Il vous sera **rappelé à la clôture**, car un silence n'est pas un « oui » : vous pouvez alors le corriger.

Écrivez vos réponses dans un fichier et donnez-le : `python3 "$R/scripts/parcours.py" answer amont --file reponses.md`, ou `answer amont --none` si vous n'avez rien à dire. Pour une à trois questions difficiles, vous pouvez demander l'avis d'un conseil de plusieurs voix, en option.

### Pause 2, courte, après la réconciliation

Vous répondez aux questions ouvertes que la grille soulève, vous parcourez la part cachée si vous en avez le droit (elle est dans le scellé), puis vous validez : `python3 "$R/scripts/parcours.py" validate amont`. Votre feu vert précède le gel.

### L'accord pour la contre-vérification

Avant d'appeler le modèle de contre-vérification, **votre accord** est demandé. Sans accord, la recette reste arrêtée : vous pouvez rendre la sortie d'un autre modèle, celui que les réglages donnent « ailleurs ».

## 5. La session de production

La production tourne dans une session `/goal`, **depuis le dossier du sujet**, avec la variable `R` exportée (sans elle, le hook de gel échoue et la session ne peut plus utiliser aucun outil) et **sans `IX_SCELLE_DIR`** (section 2). Les hooks du sujet ne se chargent que si le dossier est approuvé dans Claude Code (boîte de confiance du dossier) et si `disableAllHooks` n'est pas vrai : lancez la session, ouvrez `/hooks` et vérifiez que `PreToolUse`, `Stop` et `UserPromptSubmit` y figurent.

1. Remplissez les emplacements du goal avant de le lancer. Un goal qui contient encore un emplacement réservé non rempli est refusé au début du tour, avec le nom de l'emplacement.
2. **Rien à ajouter au goal pour les tours.** Les hooks du sujet comptent un tour à **chaque fin de tour** de la session, que la boucle `/goal` la relance ou non, sans que la session lance quoi que ce soit. Au plafond (`plafonds.tours_goal_max`, ou `tours_correction_max` pendant la correction) la boucle s'arrête, le début du tour suivant est refusé et aucun outil n'est permis : la main vous revient. La session n'a pas le droit de lire ni d'écrire le compteur, qui est au scellé : le hook le refuse sous les formes qu'il reconnaît, et une remise à zéro d'une moitié de la garde (le compteur ou son témoin) arrête la session avant son outil suivant. Une remise à zéro des deux moitiés d'un même geste, par un processus que le hook ne reconnaît pas, n'est vue par rien dans le harnais : c'est le point 7. Pour savoir où en est le compte, lancez `python3 "$R/harnais/harnais.py" trace` : la table T3 montre les lignes `tour 1`, `tour 2`…
3. **Après avoir consigné une suite qui ajoute des tours** (`suite … relancer N`), la boucle est en pause : relancez-la par un message à la session (`/goal` à nouveau si elle l'a effacé). Un message envoyé alors que le plafond est atteint est refusé, avec la cause.
4. **Si la session ne compte rien** (la trace ne montre aucun `tour 1` après qu'elle a travaillé), les hooks n'étaient pas chargés : dossier non approuvé, `disableAllHooks`, session lancée hors du dossier du sujet. Dans ce cas rien n'arrête la session ; arrêtez-la, corrigez, relancez. `python3 "$R/harnais/harnais.py" empreintes` vous le dit aussi pour les réglages : il refuse si les hooks déclarés ne désignent pas le scellé de ce sujet.
5. Le hook refuse à la session d'écrire le script, la grille, leurs fixtures, l'état du harnais et les réglages de hooks, sous les formes d'écriture qu'il reconnaît. Une écriture qu'il ne reconnaît pas change l'empreinte d'un fichier figé : les hooks la voient avant l'outil suivant (comparaison avec la copie des empreintes gardée au scellé), arrêtent la boucle et ferment tous les outils jusqu'à ce que vous ayez réglé l'écart. `empreintes` et `juge`, que vous lancez avec `IX_SCELLE_DIR`, font la même comparaison. Lancez `empreintes` quand la main vous revient, avant `fin-production`.
6. La session n'a pas non plus à choisir une suite ni à demander où est le scellé, et le harnais le lui refuse : ces commandes (`suite`, `sceau`, `geler`, `regeler`, `juge`, `ouvrir`, `contre-verif`, `empreintes`) refusent tout appelant qui n'a pas `IX_SCELLE_DIR` ou dont le dossier n'est pas le scellé de ce sujet, quelle que soit la façon de les appeler ; et ce qu'elles changent est dans le scellé, pas dans un fichier que la session écrit. `tour` et `tour-correction` existent aussi : ce sont vos commandes (elles font le même compte que les hooks, avec `IX_SCELLE_DIR`) ; la session n'a pas à les lancer.
7. **Ce que vous contrôlez vous-même, à chaque retour de la main** (un plafond atteint, une session arrêtée), et au plus tard avant `fin-production`, avant `juge` et avant `ouvrir`. Le harnais ne le fait pas à votre place et ne vous le rappelle pas ; **ces trois contrôles n'ont jamais été éprouvés** : (a) comptez les lignes `tour n` de T3 et les événements `Stop` de la transcription de la session de production : plus d'événements que de lignes, c'est un compteur remis à zéro ; (b) cherchez dans cette transcription les noms du scellé et un marqueur de la part cachée : un résultat, c'est une lecture du scellé ; (c) relisez T7 et comparez-la aux suites que vous avez consignées vous-même : une suite que vous ne reconnaissez pas, c'est une commande lancée avec le vrai scellé. Un fichier figé récrit avec ses deux copies d'empreintes, ou modifié puis restauré entre deux contrôles, n'est vu par rien : `spec-harnais.md` §6.2 le dit.

## 6. Choisir une suite quand une limite est atteinte

Quand un plafond est atteint, on s'arrête, on **n'essaie plus rien**, et on trace l'échec : le dernier résultat, ce qui reste en échec, ce qui est livré. La main revient à vous. Vous choisissez une suite, et votre choix est tracé. Les valeurs des plafonds et la liste des suites offertes à chacun sont dans `docs/harnais/A4-reglages.yaml` (clés `plafonds` et `suites_au_plafond`). Trois plafonds existent :

| Plafond atteint | Suites offertes |
|---|---|
| les passes de vérification (cadrage, goal, critères) | relancer ; livrer avec une réserve ; abandonner. **Pas « contourner »** : il n'y a pas encore de critère en échec à revoir. |
| les tours de correction (après le jugement) | relancer ; contourner ; livrer avec une réserve ; abandonner |
| les tours de la production | relancer ; contourner ; livrer avec une réserve ; abandonner |

**Ce que veut dire chaque suite, et la commande qui la consigne** (le premier mot après `suite` est le plafond atteint) :

| Suite | Ce qui se passe | Commande |
|---|---|---|
| **Relancer** | quelques tours ou passes de plus : **vous** fixez le nombre, et il est tracé | `python3 "$R/harnais/harnais.py" suite tours_goal_max relancer 3` |
| **Contourner** | revoir le critère qui échoue : retour en 2B, avec une dérogation tracée (quel critère, pourquoi) ; puis nouveau gel | `… suite tours_correction_max contourner "critère 3 revu : ambigu"`, puis `… regeler` |
| **Livrer avec une réserve** | on livre l'état courant, la réserve est écrite dans la trace | `… suite tours_goal_max livrer_avec_reserve "reste un défaut mineur"` |
| **Abandonner** | on arrête le sujet ; la trace garde l'échec et ce qui est livré | `… suite tours_goal_max abandonner` |

Pour les passes de vérification de l'amont, c'est la même commande avec `passes_verification_max`.

**Comment choisir.** Si le travail avance mais n'a pas fini : relancer. Si le même critère échoue à chaque tour et que vous soupçonnez le critère plutôt que le travail : contourner. Si le livrable sert déjà et que le reste est mineur : livrer avec une réserve. Si le sujet n'a plus de raison d'être : abandonner. Dans tous les cas, ne modifiez ni le script, ni la grille : seul « contourner » les rouvre, par `regeler`, et `regeler` n'est accepté qu'après un « contourner » consigné.

Les tours de correction sont comptés à part des tours de production.

## 7. Lire une trace

Voir le texte à part : `docs/harnais/A7-lire-une-trace.md`. Il se lit seul, sans ce guide ni Claude Code. La trace du sujet est le fichier `trace.md`, à la racine de son dossier ; `python3 "$R/harnais/harnais.py" trace` la met à jour.

---
delivery_notes:
- mode de rendu retenu / rendering mode : rapport guidé, par étapes, pour un lecteur sans connaissance de la procédure ; une commande par geste
- signaux du brief appliqués / brief signals applied : profil de lecteur imposé (un humain qui ne connaît pas la procédure) ; quatre contenus demandés (mener un sujet de code avec le harnais, répondre aux pauses, choisir une suite, lire une trace) ; « lire une trace » séparé dans son propre fichier pour se lire seul
- arbitrages / arbitrations : aucune valeur de réglage n'est recopiée, le guide renvoie à A4 par le nom des clés ; les arguments des commandes (3, « critère 3 revu ») sont des exemples ; l'étape 7 reste faite par le pilote
