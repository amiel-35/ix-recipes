---
status: draft
skill: ix-skills:deliver
format: report
recipient: un humain qui ne connaît pas la procédure (profil imposé : bénéfices concrets, peu de jargon)
---

# A7 : guide d'usage du harnais

Ce guide explique comment mener un **sujet de code** avec le harnais, de la demande à la livraison, et comment répondre aux pauses et choisir une suite quand une limite est atteinte. Vous n'avez pas besoin de connaître la procédure avant de le lire. Pour lire la trace d'un sujet, un texte à part se lit seul : `docs/harnais/A7-lire-une-trace.md`.

## 1. L'idée en deux phrases

Un sujet passe par des étapes, dans le même ordre à chaque fois, avec les mêmes garde-fous, et ces garde-fous **tiennent sans que vous ayez à y penser** : ce que le harnais compte, il le compte à votre place, ce qu'il fige, il le refuse à celui qui produit. Chaque étape laisse une ligne dans une trace, que n'importe qui peut relire pour savoir ce qui a été fait, par quel modèle, et à quel coût.

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
export IX_SCELLE_DIR=~/.ix-scelles            # le scellé : hors de tout dépôt git, loin du dossier du sujet (VOTRE terminal seulement)
```

Le scellé est un dossier que **vous** choisissez. Le harnais refuse de travailler s'il manque, s'il est dans un dépôt git ou s'il est sous le dossier du sujet ou celui du livrable. Il n'est écrit nulle part.

**Gardez-le hors de la session de production.** Elle ne doit pas savoir où est la part cachée. N'exportez donc jamais `IX_SCELLE_DIR` dans le terminal d'où vous lancez cette session : le harnais ne vérifie pas que vous l'avez fait, et s'il y est, la session peut le lire. Les trois commandes qu'elle lance (`tour`, `tour-correction`, `fin-production`) n'en ont pas besoin. Vous lancez la session par `env -u IX_SCELLE_DIR claude …` si vous n'êtes pas sûr du terminal, et vous vérifiez avant : `env | grep -c IX_SCELLE_DIR` doit afficher `0` dans ce terminal.

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
| **Gel** | vous | `python3 "$R/harnais/harnais.py" geler livrable grille.md acceptation.sh fixtures/exemples.txt` : le premier mot est le dossier du livrable, les suivants sont les fichiers à figer. Le harnais relève leurs empreintes, scelle la part cachée et déclare le hook de gel dans `.claude/settings.json` du sujet. |
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

La production tourne dans une session `/goal`, **depuis le dossier du sujet**, avec la variable `R` exportée (sans elle, le hook de gel échoue et la session ne peut plus utiliser aucun outil) et **sans `IX_SCELLE_DIR`** (section 2).

1. Remplissez les emplacements du goal avant de le lancer. Un goal qui contient encore un emplacement réservé non rempli est refusé au premier tour, avec le nom de l'emplacement.
2. Ajoutez au goal que, **au début de chaque tour**, la session lance `python3 "$R/harnais/harnais.py" tour` (et `tour-correction` pendant la correction). Cette commande vérifie les empreintes des fichiers figés, compte le tour, et refuse au plafond. Un appel refusé ne compte pas.
3. **Ce que le harnais ne peut pas faire à votre place : forcer la session à lancer `tour`.** Le plafond de tours ne vaut que si elle le lance. Rien ne l'y oblige ; le goal le lui demande, c'est tout. Il vous revient donc de vérifier, **à chaque fois que la main vous revient**, que le nombre de tours comptés (dans la trace, table T3, lignes `tour 1`, `tour 2`…) est celui des tours que la session déclare dans son journal ou que vous voyez passer. Un écart veut dire qu'un tour n'a pas été compté : le plafond n'est pas tenu, et c'est à vous de décider quoi faire (section 6).
4. La session ne peut pas modifier le script, la grille, leurs fixtures, l'état du harnais ni les réglages de hooks : le hook refuse les formes d'écriture qu'il reconnaît. Une écriture qu'il ne reconnaît pas est repérée plus tard : par `tour` au prochain tour, et dans tous les cas par `python3 "$R/harnais/harnais.py" empreintes` et par `juge`, que vous lancez avec `IX_SCELLE_DIR`. Lancez `empreintes` quand la main vous revient, avant `fin-production`.
5. Elle ne peut pas non plus choisir une suite, ni demander où est le scellé : ces commandes (`suite`, `sceau`, `geler`, `regeler`, `juge`, `ouvrir`, `contre-verif`, `empreintes`) refusent tout appelant qui n'a pas `IX_SCELLE_DIR` ou dont le dossier n'est pas le scellé de ce sujet, quelle que soit la façon de les appeler.

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
