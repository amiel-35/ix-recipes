---
status: draft
skill: ix-skills:deliver
format: readme
recipient: dev (profil imposé : le mainteneur — Amiel ; spécifications techniques, contraintes, exemples ; peu de vernis métier)
---

# A8 : note de maintenance

Pour Amiel, qui maintient le harnais et les pièces de la procédure. La note dit où vit chaque pièce après la migration, comment changer une valeur sans rien casser, comment entretenir le format 4 et les outils de l'aval, et ce que la partie B laisse à faire.

## 1. Où vit chaque pièce

Le code et les pièces de la procédure vivent maintenant dans **ix-recipes**, sur la branche du harnais. ix-pilote garde le cadrage, la décision et la trace du passage manuel, et sert d'archive : son `README.md` renvoie ici.

| Pièce | Fichier | Dépôt |
|---|---|---|
| Recette de l'amont (format 4) | `skills/amont-sujet.md` (+ `skills/amont-sujet.mystaffy.json`, `dist/skills/amont-sujet/`) | ix-recipes |
| Exécuteur, format 4 | `scripts/parcours.py` | ix-recipes |
| Contrôle de build, format 4 | `build.py` | ix-recipes |
| Page de suivi (inchangée : formats 1 à 3) | `scripts/interface.py` | ix-recipes |
| Outils de l'aval, hooks, garde, trace A3 | `harnais/harnais.py`, `harnais/hook.py`, `harnais/garde.py`, `harnais/trace_a3.py`, `harnais/commun.py` | ix-recipes |
| Manifeste, déclaration des hooks, modèle de verdict | `harnais/points-d-entree.env`, `harnais/hooks.json`, `harnais/modele-verdict.md` | ix-recipes |
| Préparation des skills de l'amont | `harnais/preparer-skills.sh` | ix-recipes |
| A3, format de trace | `docs/harnais/A3-format-trace.md` | ix-recipes (migré sans changement de sens) |
| A4, réglages | `docs/harnais/A4-reglages.yaml` | ix-recipes (migré sans changement) |
| A5, grille fixe du cadrage | `docs/harnais/A5-grille-cadrage.md` | ix-recipes (migrée sans changement) |
| A6, spec et architecture des pièces sans harnais | `docs/harnais/A6-spec.md`, `docs/harnais/A6-architecture.md` | ix-recipes (migrées sans changement) |
| Spec et architecture du harnais | `docs/harnais/spec-harnais.md`, `docs/harnais/architecture-harnais.md` | ix-recipes |
| A7, guide d'usage et « lire une trace » | `docs/harnais/A7-guide-usage.md`, `docs/harnais/A7-lire-une-trace.md` | ix-recipes (mis à jour pour le harnais) |
| A8, cette note | `docs/harnais/A8-maintenance.md` | ix-recipes (mise à jour) |
| Description du format 4 | `docs/format-4.md`, avec `docs/format-recette.md` §2quinquies et `docs/executeur.md` §8 | ix-recipes |
| A1 et A2, skills (`cadrage` mode `close`, `goal-writing`) | `skills/cadrage.md`, `skills/goal-writing.md` | **ix-skills**, branche `claude/pieces-sans-harnais-partie-a` (commit `645a599`), **non fusionnée** : la fusion est à ta main |
| `criteres-reussite` | `skills/criteres-reussite.md` | **ix-skills**, branche `claude/skill-cahier-de-recette-30edc2`, non fusionnée |
| Cadrage, décision, trace du passage de B | `trace/partie-b/` | ix-pilote |

Les originaux de A3 à A8 restent en place dans `partie-a/` d'ix-pilote : la migration est une copie.

**Rien n'est fait ici de ce qui revient au pilote à la livraison** : le commit et l'étiquette `b-a-livrable`, la version du plugin (`dist/.claude-plugin/plugin.json`), la version de la page de suivi, l'entrée du `CHANGELOG.md`, la fusion de la branche et la publication, la fusion des branches d'ix-skills et la copie de `build.py` d'ix-skills, qui reste en l'état.

## 2. Changer un réglage

**Une seule règle : une valeur de réglage s'écrit dans `docs/harnais/A4-reglages.yaml` et nulle part ailleurs.** Le code n'en porte aucune : l'exécuteur lit les plafonds, les suites et les modèles dans ce fichier, les outils de l'aval aussi.

1. Ouvrir `docs/harnais/A4-reglages.yaml`.
2. Modifier la valeur de la clé voulue, et mettre à jour son commentaire si la raison a changé.
3. Monter `version` en tête du fichier (correctif si seule une valeur change, mineure si une clé est ajoutée, majeure si une clé change de sens ou disparaît).
4. Lancer les tests (section 4). C'est tout : les sujets suivants consignent la nouvelle version (A3, table T1).

| Je veux changer | Clé dans A4 | Exemple |
|---|---|---|
| un plafond | `plafonds.passes_verification_max`, `plafonds.tours_correction_max`, `plafonds.tours_goal_max` | abaisser le plafond des passes : éditer `passes_verification_max` ; les trois boucles de l'amont le suivent, sans autre édition |
| le modèle d'un rôle | une clé de `modeles` | changer le modèle de la rédaction du goal : éditer `modeles.redaction_goal`. Chaque appel d'agent de l'amont prend le modèle de son rôle (`role` dans la recette), lu à la **création** du parcours |
| un skill de format | `types_de_sujet.<type>.skills_de_format` | éditer la clé voulue |

Limites à connaître :

- **Un parcours déjà créé garde ce qu'il a lu.** Ses plafonds, ses suites et ses modèles sont copiés dans son état à la création ; changer A4 vaut pour les parcours suivants. De même, un goal déjà rédigé garde le plafond de tours qu'il porte.
- **Le gel prime.** Le script de recette, la grille et leurs fixtures sont figés dans les limites que disent `gel.script_et_grille_figes` et `gel.gele_jusqu_a` (A4). Un critère à revoir passe par la suite `contourner` (sa définition est `definition_des_suites.contourner`, A4), puis par `regeler`.
- Le fichier `build.py` vérifie que le modèle écrit dans la recette (`model`) est celui du rôle (`role`) dans A4 : après avoir changé un modèle d'A4, mettre le `model` des étapes de ce rôle à la même valeur, sinon `build.py` refuse la recette. L'exécuteur, lui, applique la valeur d'A4.

## 3. Changer un skill de format

Un skill de format est un skill d'un autre dépôt. On ne le modifie pas depuis ici : remplacer son identifiant dans `types_de_sujet.<type>.skills_de_format`, monter `version`, et vérifier qu'`A6` (migré, non modifié) n'en cite pas l'ancien identifiant comme valeur.

## 4. Entretenir le format 4 et les outils de l'aval

**Les trois lieux.**

| Brique | Où | Ce qui s'entretient |
|---|---|---|
| Format 4 | `scripts/parcours.py` et `build.py`, qui portent la **même** règle écrite deux fois (`format4_errors`, `reglages_errors`) ; `docs/format-4.md` | une règle de plus se met aux deux endroits, avec un test dans `tests/test_format4.py` et une variante dans `tests/test_recettes.py` |
| Outils de l'aval | `harnais/` | une commande de plus : la fonction, son entrée dans `construire_parseur`, une clé `CMD_*` dans le manifeste si le pilote ou un test la lance, son test dans `tests/test_harnais.py` |
| Trace | `harnais/trace_a3.py` | une colonne ou une table de plus suit A3 ; `controler` en vérifie ce que le code sait vérifier |

**Les tests.** Depuis la racine d'ix-recipes, avec un Python qui a `pyyaml` et `jsonschema` (`pip install -r requirements.txt`), et un dossier `ix-skills/dist/skills` pour `IX_SKILLS_PATH` (voir le guide) :

```bash
python3 -m unittest discover -s tests
```

`tests/test_format4.py` joue le format 4 sur le moteur `fake` ; `tests/test_harnais.py` joue les outils de l'aval avec un faux `claude` ; aucun test n'appelle un modèle.

**Régénérer `dist/` quand les scripts ou les recettes changent** : `python3 build.py --target agentskills`. Le test `test_the_plugin_bundles_the_current_scripts` exige que `dist/skills/suivi-parcours/scripts/` soit identique à `scripts/`. `build.py` cherche `../ix-skills/skills` pour vérifier `requires` : tant que `goal-writing` et `criteres-reussite` ne sont pas fusionnés dans ix-skills, construire dans un dossier jetable où un `ix-skills/` voisin est extrait des deux références (voir `harnais/preparer-skills.sh`, qui prépare le `dist/skills` ; ajouter aussi `skills/`).

**La page de suivi.** `PAGE_FORMATS` (dans `scripts/parcours.py`) fixe les formats qu'elle annonce et accepte : 1 à 3. Elle refuse de créer un parcours au format 4 (`recipe_refused`). Ne pas y toucher tant que B n'a pas de front.

**Les hooks.** `harnais/hooks.json` déclare trois hooks qui citent `$R` ; `geler` les copie dans `.claude/settings.json` du sujet : `PreToolUse` mot pour mot, `Stop` et `UserPromptSubmit` avec `{GARDE}` remplacé par le scellé du sujet, en hexadécimal (`--garde`). `Stop` compte chaque fin de tour dans la garde (`harnais/garde.py`, `garde.json` au scellé) et arrête la boucle au plafond ; `UserPromptSubmit` et `PreToolUse` refusent la suite ; le témoin `.harnais/temoin.json` fait voir une garde récrite seule. Toute commande du pilote qui change le compteur, la limite ou la phase passe par `garde.modifier`. La session de production doit avoir `R` dans son environnement, sinon le hook échoue et chaque appel d'outil est refusé. Elle ne doit **pas** avoir `IX_SCELLE_DIR` : le hook n'en a plus besoin pour fermer le scellé (il le connaît par le pointeur des réglages), mais ce serait un emplacement de plus à lire. Les commandes du pilote ne reposent pas sur le hook : elles refusent tout appelant qui ne tient pas le scellé du sujet (le jeton, `commun.exiger_pilote`), et ce qu'elles changent vit au scellé. Une commande de plus réservée au pilote s'y branche par `exiger_pilote`, **et** par `POUR_LE_PILOTE` dans `hook.py` pour le message en clair ; sans le premier, elle serait libre à toute forme d'appel que le second ne reconnaît pas. Une règle de plus sur le scellé se met dans `hook.py` (`refuser_scelle_shell`, `decider`) **avec** un cas refusé et un cas légitime dans `tests/test_harnais.py` (`SealClosedTests`). Ce que le hook ne voit pas (le résidu), son détecteur et son moment pour chaque geste, le niveau réel de chaque protection (« interdit et détecté » pour O5, O10 et O11) et ce qui n'est pas éprouvé en session réelle sont dits dans `architecture-harnais.md` §8 et `spec-harnais.md` §6 ; ne pas le promettre plus fort, et ne pas écrire « impossible » ni « mécanisme qui empêche » pour ces protections.

**Ce que l'exécuteur de la base accepte encore** : `model: fable` sur une étape d'une recette de format 1 à 3 (seul `build.py` la refuse). Il n'est pas corrigé ici (hors de B) ; à noter au bilan.

## 5. Installer le harnais sur une autre machine

Rien du harnais n'est installé dans la configuration de la machine : le code est dans le dépôt, et le hook est déclaré au gel de chaque sujet, dans le dossier de ce sujet. Installer, c'est donc réunir les prérequis, le dépôt, les skills de l'amont et deux variables.

1. **Prérequis.** Python 3, git, et Claude Code (`claude` trouvé par le `PATH`, connecté à un compte qui donne accès aux modèles que nomment les clés de `modeles` d'A4 : le harnais les lit, il n'en choisit aucun). Vérifier : `claude --version`, `python3 --version`, `git --version`.
2. **Le dépôt.** Cloner ix-recipes et extraire la branche du harnais. Installer les dépendances de `build.py` et des tests : `pip install -r requirements.txt`, de préférence dans un environnement virtuel. Les réglages (`docs/harnais/A4-reglages.yaml`) et le manifeste (`harnais/points-d-entree.env`) viennent avec le dépôt : on ne les recopie pas, et on ne retape aucune de leurs valeurs ; la valeur d'un plafond, d'un modèle ou d'une suite se lit à sa clé d'A4 (section 2).
3. **Les skills de l'amont.** Tant que `cadrage` (mode `close`), `goal-writing` et `criteres-reussite` ne sont pas fusionnés dans ix-skills, cloner ix-skills à côté (ou donner son dossier par `IXS`) et lancer `harnais/preparer-skills.sh DOSSIER_NEUF` : il extrait les références que `IX_SKILLS_REFS` désigne par défaut, sans rien écrire dans ix-skills. Une fois fusionnés, `IX_SKILLS_PATH` désigne `dist/skills` d'ix-skills et ce script ne sert plus.
4. **Les variables**, dans le terminal du pilote : `R` (la racine d'ix-recipes), `IX_SKILLS_PATH` (le `dist/skills` de l'étape 3), `IX_SCELLE_DIR` (un dossier neuf **au nom tiré au hasard**, hors de tout dépôt git, hors du dossier du sujet et du livrable, lisible de vous seul ; `mktemp -d "$HOME/.XXXXXXXXXXXXXXXX"` le crée en 0700 ; son chemin n'est écrit que dans votre profil de shell). Facultatives : `IX_PILOTE` (le nom écrit en T1, sinon l'utilisateur git), `IX_MODELE_EXTERNE` (le modèle de l'étape externe, sinon `n.c.` en trace), `IX_REGLAGES` (un autre fichier de réglages), `IX_JUGE_DELAI` (le délai du juge, en secondes). **Dans le terminal où l'on lance la session de production : `R`, et pas `IX_SCELLE_DIR`.**
5. **Vérifier sans modèle.** Depuis la racine d'ix-recipes : `python3 -m unittest discover -s tests` (section 4). Aucun test n'appelle de modèle. Si `dist/` doit être régénéré (`python3 build.py --target agentskills`), construire dans un dossier jetable qui a un `ix-skills/` voisin (section 4).
6. **Ce qui ne se vérifie qu'avec un modèle.** Le lancement réel du juge (`claude -p …`) et un passage de l'amont sur le moteur réel ne sont éprouvés par aucun test : le premier passage sur la nouvelle machine est un passage de terrain (section 6).

Une machine neuve ne partage pas l'état d'un sujet commencé ailleurs : le scellé, les empreintes et l'état du harnais sont dans le dossier du sujet et dans `IX_SCELLE_DIR`, et le nom du sous-dossier scellé de chaque sujet est tiré au hasard et gardé dans `index.json`, à la racine de `IX_SCELLE_DIR`. Reprendre un sujet sur une autre machine n'est pas prévu (un pilote, un sujet, une machine).

## 6. Ce qui reste à faire

| Quoi | Qui |
|---|---|
| committer la branche, poser l'étiquette `b-a-livrable` | le pilote |
| relever la version du plugin et celle de la page, écrire l'entrée du CHANGELOG | le pilote, à la livraison |
| fusionner les branches d'ix-skills (A1, A2, `criteres-reussite`), puis mettre à jour la copie de `build.py` d'ix-skills et simplifier `preparer-skills.sh` | le pilote |
| éprouver le lancement réel du juge (`claude -p --allowedTools …`) sur un sujet réel | le pilote, à B-b |
| relever les jetons des appels de l'exécuteur (aujourd'hui `n.c.` en T3) | à décider |
| traduire A3 et A4 vers une forme propre au harnais | **non nécessaire** : le harnais lit A4 et écrit A3 tels quels |

## 7. Renvoi depuis le README d'ix-pilote

Le `README.md` d'ix-pilote cite chaque chemin du manifeste (`harnais/points-d-entree.env`), relatif à la racine d'ix-recipes. Si un fichier change de nom, mettre le manifeste et ce README à jour dans le même geste.

---
delivery_notes:
- mode de rendu retenu / rendering mode : readme technique, pour un mainteneur
- signaux du brief appliqués / brief signals applied : profil de lecteur imposé (mainteneur) ; contenu demandé : où vit chaque pièce après la migration, changer un réglage, entretenir le format 4 et les outils de l'aval, installer le harnais sur une autre machine
- arbitrages / arbitrations : aucune valeur de réglage n'est recopiée ; la section « ce qui reste à faire » reprend ce que le goal laisse au pilote (version du plugin, version de la page, CHANGELOG, commit) sans en faire
