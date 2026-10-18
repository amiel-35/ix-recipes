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
| Outils de l'aval, hook, trace A3 | `harnais/harnais.py`, `harnais/hook.py`, `harnais/trace_a3.py`, `harnais/commun.py` | ix-recipes |
| Manifeste, déclaration du hook, modèle de verdict | `harnais/points-d-entree.env`, `harnais/hooks.json`, `harnais/modele-verdict.md` | ix-recipes |
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
| le modèle d'un rôle | une clé de `modeles` | passer le goal de `sonnet` à `opus` : éditer `modeles.redaction_goal`. Chaque appel d'agent de l'amont prend le modèle de son rôle (`role` dans la recette), lu à la **création** du parcours |
| un skill de format | `types_de_sujet.<type>.skills_de_format` | éditer la clé voulue |

Limites à connaître :

- **Un parcours déjà créé garde ce qu'il a lu.** Ses plafonds, ses suites et ses modèles sont copiés dans son état à la création ; changer A4 vaut pour les parcours suivants. De même, un goal déjà rédigé garde le plafond de tours qu'il porte.
- **Le gel prime.** Pendant la production et jusqu'à la fin du jugement, le script de recette, la grille et leurs fixtures sont figés. Un critère à revoir passe par la suite « contourner » (retour en 2B, dérogation tracée, `regeler`).
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

**Le hook.** `harnais/hooks.json` déclare une commande qui cite `$R`. `geler` la copie mot pour mot dans `.claude/settings.json` du sujet. La session de production doit avoir `R` dans son environnement, sinon le hook échoue et chaque appel d'outil est refusé. Le hook ne connaît le scellé que si `IX_SCELLE_DIR` est dans cet environnement. Ce que le hook ne voit pas est dit dans `architecture-harnais.md` §8 ; ne pas le promettre plus fort.

**Ce que l'exécuteur de la base accepte encore** : `model: fable` sur une étape d'une recette de format 1 à 3 (seul `build.py` la refuse). Il n'est pas corrigé ici (hors de B) ; à noter au bilan.

## 5. Ce qui reste à faire

| Quoi | Qui |
|---|---|
| committer la branche, poser l'étiquette `b-a-livrable` | le pilote |
| relever la version du plugin et celle de la page, écrire l'entrée du CHANGELOG | le pilote, à la livraison |
| fusionner les branches d'ix-skills (A1, A2, `criteres-reussite`), puis mettre à jour la copie de `build.py` d'ix-skills et simplifier `preparer-skills.sh` | le pilote |
| éprouver le lancement réel du juge (`claude -p --allowedTools …`) sur un sujet réel | le pilote, à B-b |
| relever les jetons des appels de l'exécuteur (aujourd'hui `n.c.` en T3) | à décider |
| traduire A3 et A4 vers une forme propre au harnais | **non nécessaire** : le harnais lit A4 et écrit A3 tels quels |

## 6. Renvoi depuis le README d'ix-pilote

Le `README.md` d'ix-pilote cite chaque chemin du manifeste (`harnais/points-d-entree.env`), relatif à la racine d'ix-recipes. Si un fichier change de nom, mettre le manifeste et ce README à jour dans le même geste.

---
delivery_notes:
- mode de rendu retenu / rendering mode : readme technique, pour un mainteneur
- signaux du brief appliqués / brief signals applied : profil de lecteur imposé (mainteneur) ; contenu demandé : où vit chaque pièce après la migration, changer un réglage, entretenir le format 4 et les outils de l'aval
- arbitrages / arbitrations : aucune valeur de réglage n'est recopiée ; la section « ce qui reste à faire » reprend ce que le goal laisse au pilote (version du plugin, version de la page, CHANGELOG, commit) sans en faire
