---
status: draft
skill: ix-skills:deliver
format: readme
recipient: dev (profil imposé : le mainteneur d'ix-recipes et l'auteur de recettes ; spécifications techniques, contraintes, exemples)
---

# Le format 4 d'une recette-workflow

Le **format 4** (2026-10-18) est le format **minimal** des recettes qui ont besoin de trois choses que les formats 1 à 3 n'ont pas : des **boucles bornées**, un **champ caché** et un **arrêt avant une étape jouée à part**. Il ajoute des clés d'étape à `format-recette.md` (formats 1 à 3, qui restent décrits et inchangés) et se joue par `scripts/parcours.py` ; la page de suivi ne le joue pas. Le harnais de la procédure « traiter un sujet de bout en bout » (`docs/harnais/`) est son premier usage : `skills/amont-sujet.md`.

## 1. Pourquoi c'est un format

Le critère de `format-recette.md` §2bis : une recette écrite selon les nouvelles règles serait-elle **mal jouée sans le dire** par un lecteur qui ne les connaît pas ? Oui. Un exécuteur du format 3 ignore les clés qu'il ne connaît pas : il jouerait une boucle une seule fois, donnerait à toutes les étapes le champ qui devait rester caché, et jouerait l'étape qui devait s'arrêter. Le format 4 fait refuser la recette par tout lecteur qui ne le connaît pas (« mettez la page à jour », « mettez à jour build.py »), au lieu de la jouer à moitié.

## 2. Ce que le format 4 est, et n'est pas

**Il a** : des boucles bornées par un plafond des réglages, un champ caché, un arrêt avant une étape externe.

**Il n'a pas** (et `build.py` et l'exécuteur le refusent, en nommant la cause) :

| Refusé | Clé ou valeur | Pourquoi |
|---|---|---|
| une étape parallèle | `parallel: true` | l'isolation de l'exécuteur joue les étapes l'une après l'autre ; le parallèle serait le format complet |
| une étape qui écrit ou lance des commandes | `writes: true` | la plus contraire à l'isolation (`--tools Read`) |
| le modèle `fable` | `model: fable` | Fable ne s'appelle qu'après accord, à part, jamais dans un enchaînement automatisé |
| des boucles imbriquées | deux `loop` dont les étendues se recouvrent | le format minimal n'en a pas besoin |

Les formats 1 à 3 ne changent pas, y compris pour ce que l'exécuteur accepte aujourd'hui : l'acceptation de `model: fable` par l'exécuteur pour ces formats n'est pas corrigée ici (seul `build.py` la refuse) ; elle est notée pour le bilan.

## 3. Les clés d'étape

En plus de celles des formats 1 à 3. **Quatre sont réservées au format 4** : `verdict_field`, `loop`, `hidden` et `external` (la constante `FORMAT4_STEP_KEYS`, dans `scripts/parcours.py` et `build.py`) ; une recette de format 3 ou moins qui en porte une est refusée, avec « format: 4 » demandé en tête du bloc `workflow`. Les deux autres, `stage` et `role`, **ne sont pas réservées** : le code les lit sur toute recette, et une recette de format 3 qui les porte passe sans erreur. Elles ne sont contrôlées qu'en format 4 (`stage` : texte non vide ; `role` : voir le tableau).

| Clé | Sens | Règle |
|---|---|---|
| `stage` | l'étape de la procédure (`1a`, `2B`, `3`…) que la ligne de trace porte | texte non vide |
| `role` | la clé de `modeles` des réglages (A4) dont le modèle s'applique à l'appel | en format 4, obligatoire sauf sur une étape externe, et doit nommer une clé de `modeles` ; `build.py` vérifie que `model` en est la valeur ; l'exécuteur applique la valeur des réglages lue à la **création** du parcours |
| `verdict_field` | le champ de `transmits` où une étape qui vérifie rend son verdict | la première ligne non vide du champ commence par `OK` ou `REPRENDRE` : le premier mot est lu sans tenir compte de la casse ni des accents, une décoration Markdown devant lui (`#`, `*`, `>`, `-`, `` ` ``, `_`) est ignorée, et la suite de la ligne n'est pas lue. Si ce premier mot n'est ni l'un ni l'autre, l'étape échoue (« verdict illisible ») |
| `loop` | `{to: <étape>, ceiling: <plafond>}` : sur `REPRENDRE`, renvoyer à l'étape `to` | `to` est une étape antérieure ; l'étape a un `verdict_field` ; `ceiling` est une clé de `plafonds` des réglages |
| `hidden` | des champs de `transmits` que l'exécuteur ne laisse pas dans le dossier | voir §5 ; aucun n'est `output_field` ; aucune étape ne les reçoit, sauf une étape `external` |
| `external` | l'exécuteur s'arrête avant l'étape | voir §6 ; ni `pause`, ni `model`, ni `optional`, ni `produces_context_sheet` |

Une étape qui a un `verdict_field` sans `loop` et qui rend `REPRENDRE` n'est ni suivie ni levée comme une pause : le parcours attend (`pending.type` vaut `verdict`) ; `rerun` d'une étape antérieure le relance, `validate --stop` l'arrête.

## 4. Les boucles bornées

À chaque passage d'une étape qui a un `verdict_field`, l'exécuteur compte une passe, lit le verdict et :

- `OK` : le parcours continue ;
- `REPRENDRE` avec une passe disponible : il remet en file l'étape `to` et celles qui la suivent (leurs sorties sont gardées en `.vN`), et donne le verdict à l'étape `to` comme entrée supplémentaire (`<étape>.<champ>`) ;
- `REPRENDRE` au plafond : il s'arrête (`pending.type` vaut `ceiling`), écrit le constat (dernier résultat, ce qui reste en échec, ce qui est livré) et n'offre que les suites que les réglages donnent à ce plafond. **Il ne choisit jamais.** `parcours.py next` ne rejoue rien tant que le pilote n'a pas choisi.

Le plafond n'est écrit nulle part dans la recette : `ceiling` nomme une clé des réglages, et la valeur est copiée dans l'état du parcours à sa création. La suite se consigne par `parcours.py suite <slug> --suite relancer --n N` (le pilote fixe N), `--suite livrer_avec_reserve --text "…"` ou `--suite abandonner`. « contourner » n'est offerte que si les réglages l'offrent à ce plafond.

## 5. Le champ caché

Un champ déclaré `hidden` est sorti du HANDOFF dès qu'il est produit : l'exécuteur le range dans le **scellé** et ne laisse dans le dossier du parcours qu'une marque (`[champ caché : scellé]`) et son empreinte, dans la sortie de l'étape, dans l'état et dans la trace du message de relance. Aucune étape jouée par l'exécuteur ne le reçoit ; une étape `external` le reçoit, et son message est écrit au scellé.

Le scellé est le dossier donné par la variable d'environnement **`IX_SCELLE_DIR`**, à l'exécution. L'exécuteur le refuse si la variable manque, si le dossier est dans un dépôt git, ou s'il contient, ou s'il est sous, le dossier du sujet, le dossier du livrable (`$L`) ou ix-recipes. Aucune valeur par défaut, aucun chemin déduit, aucun chemin écrit dans un fichier.

L'instruction à l'étape qui produit le champ est dans sa mission : la part cachée va dans ce champ **et nulle part ailleurs**.

## 6. L'étape externe

Une étape `external: true` n'est pas jouée par l'exécuteur. Quand le parcours l'atteint, il construit son message (le texte du skill, la mission, les entrées déclarées, le contrôle d'isolation compris), l'écrit en `NN-<étape>.in.md` (au scellé si une entrée est cachée), puis s'arrête : `pending.type` vaut `external` et `pending.step` nomme l'étape. Le pilote appelle le modèle de son choix, après son accord, et rend la sortie complète :

```bash
python3 scripts/parcours.py supply <slug> <étape> --file sortie.md [--model fable] [--cost-usd 1.25]
```

La sortie est lue comme celle de toute étape (HANDOFF, verdict) ; si l'étape a un `verdict_field` et un `loop`, sa passe compte dans le plafond comme les autres. La recette de l'amont l'utilise pour la contre-vérification des critères : la recette n'appelle jamais Fable.

## 7. Les réglages

L'exécuteur lit le fichier de réglages `docs/harnais/A4-reglages.yaml` (ou le fichier que désigne `IX_REGLAGES`) avec la bibliothèque standard seule. Il en prend : les plafonds, les suites offertes à chaque plafond, le modèle de chaque rôle. `build.py` fait les mêmes vérifications (plafond et suites existent ; le `model` écrit est celui du `role`).

## 8. Qui lit le format 4

| Lecteur | Format 4 |
|---|---|
| `build.py` (recettes du dépôt) | accepté ; les règles ci-dessus ; les messages nomment la cause |
| l'exécuteur (`parcours.py`) | joué ; `formats --json` annonce `[1, 2, 3, 4]` et `loop_format: 4` |
| la page de suivi | **refusé** : elle annonce et accepte 1 à 3 ; créer un parcours sur une recette au format 4 répond 422 `recipe_refused` ; `PAGE_FORMATS` le fixe |
| un exécuteur ou une page plus anciens | refusé (« mettez la page à jour ») |

## 9. Écrire une recette de format 4

1. `format: 4` en tête du bloc `workflow` ; `role` sur chaque étape jouée par l'exécuteur, avec `model` égal à la valeur de ce rôle dans les réglages.
2. Pour chaque boucle : un `verdict_field` (la mission dit la première ligne : `OK` ou `REPRENDRE`) et un `loop`.
3. Pour une part cachée : `hidden` sur l'étape qui la produit, et rien de la part cachée dans les autres champs ni dans le document de l'étape.
4. `python3 build.py <id> --validate`, puis les tests : `tests/test_format4.py` rejoue les règles ci-dessus sur la recette du dépôt.

## 10. Ce qui est laissé au pilote

La version du plugin, la version de la page de suivi et le CHANGELOG ne sont pas touchés par l'introduction du format 4 : ils sont laissés au pilote, qui les fait avec le commit, à la livraison. Ce document ne mentionne aucune entrée de CHANGELOG. La copie de `build.py` d'ix-skills n'est pas mise à jour non plus (`format-recette.md` §2bis l'exigerait pour un nouveau format ; elle reste en l'état tant qu'ix-skills n'est pas fusionné).

---
delivery_notes:
- mode de rendu retenu / rendering mode : readme technique, pour le mainteneur d'ix-recipes et l'auteur de recettes
- signaux du brief appliqués / brief signals applied : profil de lecteur imposé ; description placée à côté des formats 1 à 3 (`format-recette.md` §2quinquies y renvoie) ; aucune entrée de CHANGELOG, la version du plugin, celle de la page et le CHANGELOG sont dits laissés au pilote
- arbitrages / arbitrations : un seul document pour le format, `executeur.md` §8 ne reprend que ce que l'exécuteur fait de plus ; les valeurs de réglage ne sont pas recopiées
