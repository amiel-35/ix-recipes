# Format d'une recette-workflow

Spécification v1 du 2026-10-14 : c'est le **format 1** des recettes (§2bis, champ `format` ajouté le 2026-10-16). Le **format 2** (2026-10-16) y ajoute une seule chose : une étape qui vérifie peut relire la source (§1.10, §2ter). Une **recette-workflow** est un skill d'ix-recipes qui enchaîne plusieurs skills (atomes d'ix-skills ou autres recettes) pour un travail récurrent. Elle reprend ce qu'ix-memory avait éprouvé (chaîne courte, mission locale par étape, handoff borné, pauses humaines) et corrige ce qui n'avait jamais marché (le brief de départ qui pollue les étapes aval, `handoff.fields` jamais appliqué).

Une recette qui n'enchaîne rien reste un skill ordinaire : c'est le cas par défaut.

## 1. Principes

1. **Isolation.** Chaque étape tourne dans un contexte neuf — un sous-agent quand la plateforme en a (Claude Code), un appel neuf quand un script exécute (`claude -p`, `codex exec`, `agy -p`, `vibe -p`). Elle ne reçoit **que** ce que sa ligne « reçoit » liste. Les consignes (« ignore ce qui précède ») ne sont qu'un repli là où rien ne permet d'isoler.
2. **Le brief brut ne va qu'à l'étape 1.** Jamais au-delà, pas même à la dernière — à une exception près, réservée aux étapes qui vérifient (§1.10, format 2).
3. **La fiche de contexte remplace le brief pour la suite.** L'étape 1 la produit, l'humain la valide, toutes les étapes la reçoivent. Elle contient des faits (entités, objectif, contraintes, destinataire, format, échéances, solutions déjà nommées), jamais de demande d'action.
4. **Handoff nommé et borné.** Chaque étape termine sa sortie par un bloc `## HANDOFF` contenant une sous-section `### <champ>` par champ que la recette lui demande de transmettre (1 à 5), puis un bloc `## SUMMARY` de cinq lignes au plus. Un champ peut faire plusieurs paragraphes : c'est pour cela qu'on découpe par titres, pas par lignes ni en JSON. L'étape suivante reçoit ces champs, pas la sortie complète — sauf pour une étape dont le livrable est un document (une offre, un brief) : elle déclare `output_field`, et sa sortie complète devient ce champ, au lieu d'être recopiée (un modèle qui recopie un document long dans un champ le résume). La fiche de contexte, courte, est rendue en JSON (bloc `## CONTEXT SHEET` suivi d'un bloc de code `json`).
5. **Extraction mot pour mot, quand la source l'impose.** Certaines listes doivent passer à l'identique (objectifs, exercices, pièces à remettre d'un cahier des charges) : l'étape 1 les recopie dans un champ déclaré `verbatim`. Ce champ est une **liste** : chaque ligne est contrôlée séparément (un élément de liste passe, un paragraphe recopié est bloqué), et l'ensemble ne peut pas couvrir plus de 85 % de la source — au-delà, c'est la source elle-même qui passerait. Ce qu'un champ `verbatim` a cité est ensuite admis : les étapes suivantes peuvent le reprendre tel quel (une offre qui reprend les éléments imposés), le reste de la source reste contrôlé.
6. **Une étape = un rôle.** Elle ne refait pas le travail d'une autre et ne requalifie pas un champ reçu sans le signaler (`requalifié : <raison>`).
7. **L'orchestrateur ne tranche jamais sur le fond.** Il enchaîne, s'arrête aux pauses, s'arrête si une étape signale un blocage, et fait choisir l'humain quand la recette prévoit un embranchement.
8. **Orchestrateur léger.** Le sous-agent écrit sa sortie complète dans le fichier de trace et ne renvoie à l'orchestrateur que son bloc `## HANDOFF` et un résumé de cinq lignes. L'orchestrateur n'accumule pas les sorties ; un modèle léger (Sonnet) lui suffit, et chaque étape indique le sien (`model`). Règle par défaut : **Opus pour l'étape 1**, seule à lire la source brute, car ce qu'elle rate est perdu pour toute la suite ; **Sonnet pour les autres**, y compris les décisions, que l'humain valide juste après ; Opus en option sur une étape à fort enjeu.
9. **Chaîne courte et linéaire.** Pas de boucle, pas de parallèle. Une étape optionnelle n'est lancée que si l'humain le décide à la pause qui la précède.
10. **Une étape qui vérifie peut relire la source** (format 2, décidé le 2026-10-16). La règle 2 vient d'ix-memory, où les étapes profondes qui relisaient le brief le réinterprétaient et dérivaient : elle vaut pour les étapes qui **produisent**. Une étape qui **vérifie** a le besoin inverse : contrôler ce que la chaîne a fait de la demande. Avec la fiche et les champs de l'amont seulement, elle ne contrôle que la cohérence de la chaîne avec elle-même : un chiffre mal recopié à l'étape 1 et repris ensuite sort « confirmé », ce que la fiche a laissé de côté ne peut être qu'« absent » (cas rejoué : [preuve](preuve-lecture-source/README.md)). Les champs `verbatim` (règle 5) ne couvrent que ce que l'étape 1 a prévu de recopier.
    - La recette le déclare sur l'étape : `reads_source: true`. Rien n'est implicite : le circuit des données se lit dans la recette, jamais dans le skill (on a écarté l'option où le skill déciderait lui-même de faire passer ce qu'il reçoit).
    - **Réservé aux skills qui vérifient**, une liste fermée : `ix-skills:fact-check`, `ix-skills:quality-check`, `ix-skills:controle-qualite` (`VERIFICATION_SKILLS` dans `scripts/parcours.py` et `build.py`). Pourquoi une liste et pas un rôle déclaré (`role: verify`) : un rôle déclaré par la recette serait sa propre garantie, et c'est justement la recette qu'on contrôle. Pourquoi pas la `category` des skills : dans ix-skills, `category: critique` couvre aussi `red-team`, `contrarian`, `dixieme-homme`, qui produisent. Un nouveau skill de vérification s'ajoute à la liste, dans les deux fichiers, avec un test.
    - Jamais à l'étape 1 (elle lit déjà la demande), jamais sur une étape qui produit : `build.py`, l'exécuteur et la page refusent en le disant (« reads_source est réservé aux étapes qui vérifient… ; pour lui faire passer des éléments précis de la demande, déclarez-les verbatim à l'étape 1 »).
    - Les champs `verbatim` restent le défaut ; `reads_source` sert quand le contrôle porte sur la demande elle-même (chiffres d'un tableau, éléments imposés, mots du demandeur), pas seulement sur ce que l'amont a transmis.
    - Ce qu'elle transmet reste contrôlé : un verdict qui recopie un passage long de la source (40 mots d'affilée) est refusé comme toute fuite, puisque ses champs peuvent aller à une étape qui produit (une offre refaite avec les verdicts).
    - La vérification **de calcul** (recalculer un écart, un ratio, un total à partir des valeurs de la source) est un geste à part de `fact-check`, qui vérifie seulement qu'un chiffre est dans la source. Son atome, `ix-skills:calc-check`, est spécifié dans [`atome-verification-calcul.md`](atome-verification-calcul.md) et figure dans la liste fermée depuis le 2026-10-16 (décision 8) ; il reste à le créer dans ix-skills. Tant qu'il n'existe pas, `requires` le refuse et le concepteur de la page ne l'annonce pas.

## 2. Frontmatter

En plus du frontmatter canonique (CLAUDE.md §3), une recette-workflow déclare :

```yaml
category: workflow
requires: [ix-skills:cadrage, ix-skills:questioning, ix-skills:brief]
workflow:
  format: 1                       # le format de la recette (§2bis) ; en tête du bloc
  context_sheet: [entities, objective, constraints, recipient, format, deadlines, named_solutions]
  context_labels:                 # facultatif : nom de chaque rubrique pour l'utilisateur, en français
    entities: "Acteurs"
    named_solutions: "Solutions déjà nommées"
  steps:
    - id: cadrage                 # identifiant unique de l'étape
      label: "Cadrage de la demande"   # nom affiché à l'utilisateur, en français (facultatif ; l'id sinon)
      skill: ix-skills:cadrage    # skill exécuté, avec son espace de noms ; doit figurer dans requires
      mission: Clarify the need…  # mission locale, en une ou deux phrases
      receives: [brief]           # brief (étape 1 seulement), context_sheet, answers, ou <étape>.<champ>
      transmits: [need, constraints, hypotheses, open_points]
      produces_context_sheet: true   # étape 1 seulement
      verbatim: [imposed_items]      # étape 1 seulement : champs recopiés mot pour mot exprès (listes imposées par la source)
      output_field: offer            # quand le livrable de l'étape est un document : sa sortie complète devient ce champ
      reads_source: true             # format 2, étape qui vérifie seulement (§1.10) : elle relit aussi la demande brute
      pause: validate             # none | validate | answers | choose
      model: opus                 # opus | sonnet | haiku — indication pour Claude Code et l'exécuteur (voir §1.7)
    - id: explorer
      skill: ix-skills:explorer
      optional: true              # lancée seulement si l'humain le décide à la pause précédente
      …
```

`build.py` vérifie mécaniquement :

- `format` est présent et vaut un format connu (1 ou 2) — sinon il s'arrête là : les règles qui suivent sont celles des formats 1 et 2 ;
- chaque `skill` figure dans `requires`, et chaque id de `requires` existe (dans ix-recipes, ou dans `../ix-skills/skills/` quand le dépôt voisin est présent) ;
- les ids d'étape sont uniques ;
- seule la première étape reçoit `brief`, et c'est elle qui porte `produces_context_sheet` ; sa pause vaut `validate` ou `answers` ;
- `verbatim` n'est déclaré que sur la première étape et ne nomme que des champs de ses `transmits` ;
- `output_field`, s'il est donné, fait partie des `transmits` ;
- `label`, s'il est donné, est une chaîne non vide ;
- `context_labels` n'associe que des clés de `context_sheet` à des libellés non vides ; `summary_fr` (frontmatter, une phrase lisible affichée par la page de suivi à la création d'un dossier) est une chaîne non vide.
- chaque `<étape>.<champ>` reçu existe dans les `transmits` d'une étape **antérieure** ;
- `answers` n'est reçu qu'après une étape dont la pause vaut `answers` ;
- chaque `skill` est cité dans le corps du SKILL.md (le corps et le frontmatter ne divergent pas) ;
- `model`, s'il est donné, vaut `sonnet`, `opus` ou `haiku` ;
- `reads_source`, s'il est donné, vaut `true` ou `false` ; `true` seulement hors de l'étape 1, sur un skill de `VERIFICATION_SKILLS`, et dans une recette au format 2 au moins.

Le frontmatter est la version lisible par machine : c'est elle que l'exécuteur du lot 2 lira.

## 2bis. Le format (`workflow.format`)

**Ce que c'est.** Un nombre entier, en tête du bloc `workflow`, qui dit selon quelles règles lire ce bloc. Le **format 1** est ce document hors §1.10 et §2ter ; le **format 2** est le format 1 plus `reads_source`. Il ne se confond ni avec `version` (la version de la recette elle-même, en x.y.z, qui change à chaque retouche), ni avec la version du plugin, ni avec celle de la page de suivi ([interface.md](interface.md) §4).

**Qui le lit, et ce qu'il fait d'un format qu'il ne connaît pas.**

| Lecteur | Format connu | Format plus récent, ou inconnu | Pas de champ `format` |
|---|---|---|---|
| `build.py` (recettes du dépôt) | accepté (1, 2) | erreur, seule (le reste n'est pas vérifié) : « mettez à jour build.py et la page de suivi » | erreur : « ajoutez « format: 1 » » |
| l'exécuteur (`parcours.py`) | accepté | refus : `new`, `next`, `plan` échouent ; `status` reste lisible et dit pourquoi dans `recipe_error` ; `recipes` écarte la recette (une recette personnelle va dans `personal_problems`) | lu comme format 1, avec un avertissement (`new`, `recipes` ; `warnings` dans `recipes --json`) |
| la page de suivi | acceptée | la même chose, par l'exécuteur ; « Mes recettes » dit de mettre la page à jour plutôt que de modifier la recette ; créer un dossier répond 422 `recipe_refused` | lue comme format 1 ; la proposition au dépôt demande d'ajouter le champ |

Un format plus récent donne « cette recette est au format N, plus récent que ce que la page de suivi sait lire (format 1) : mettez la page à jour (installez la dernière version du plugin ix-recipes) ». Toute autre valeur (un texte, un décimal comme `1.0`, `0`, un booléen, `"1"` entre guillemets) est un format inconnu, avec le même conseil. Les formats acceptés sont annoncés par `parcours.py formats [--json]` et `GET /api/version` (`recipe_formats`) ; `state.json` garde le format de la recette à la création d'un dossier (`recipe_format`).

**Une recette sans champ `format` est lue comme format 1** (tranché le 2026-10-16). Raisons : toute recette écrite avant ce champ l'a été selon les règles du format 1, le seul qui existait — il n'y a donc aucune ambiguïté sur ce qu'elle veut dire ; la refuser casserait les recettes personnelles et les dossiers déjà créés sans rien protéger ; et la règle est figée : l'absence de champ voudra dire « format 1 » pour toujours, même quand le format 2 existera — une recette au format 2 devra le déclarer. L'avertissement suffit à le faire ajouter. Le dépôt, lui, exige le champ (`build.py`) : une recette publiée dit son format explicitement.

**À la création.** Toute recette créée depuis la page déclare son format, le plus bas qui l'exprime : `format: 1`, ou `format: 2` dès qu'une étape relit la source (`needed_format`). C'est vrai du modèle, de la recette écrite à partir des blocs, de la copie d'une recette fournie, du fichier écrit par le concepteur (ajouté en tête du bloc `workflow` s'il l'a omis, relevé de 1 à 2 s'il a écrit 1 avec `reads_source`). Une recette qui n'utilise rien du format 2 reste au format 1 : une page plus ancienne sait encore la jouer. Une recette déjà rangée dans le recueil n'est jamais réécrite d'office.

**Quand changer de format.** On passe au format suivant quand une recette écrite selon les nouvelles règles serait **mal jouée sans le dire** par l'exécuteur actuel, ou une recette actuelle par le nouvel exécuteur :

- un champ existant change de sens (`receives` qui accepterait autre chose qu'un champ nommé, `pause` dont une valeur ferait autre chose) ;
- un champ nouveau que l'exécuteur ne peut pas ignorer sans trahir la recette : imbrication de recettes, étapes en parallèle, boucle, embranchement conditionnel, une nouvelle valeur de `pause` ;
- un champ est retiré ou rendu obligatoire.

On reste au format 1 pour un champ facultatif qu'un exécuteur plus ancien peut ignorer sans danger (un libellé, une indication d'affichage : c'est ainsi que `label`, `context_labels` et `summary_fr` sont arrivés), pour un contrôle de plus dans `build.py`, ou pour un changement du corps du SKILL.md. Un tel ajout se documente dans ce document, daté.

**Passer au format 2.** Dans l'ordre :

1. écrire ce que change le format 2 dans ce document (une section par format, le format 1 restant décrit) ;
2. l'exécuteur apprend à jouer les deux (`RECIPE_FORMATS = (1, 2)`) : une recette au format 1 continue de tourner telle quelle, sans migration forcée ;
3. `build.py` accepte 2 — dans les deux copies, ix-recipes et ix-skills (CLAUDE.md §7) ;
4. la page relève sa version (mineure : elle lit un format de plus) ; `RECIPE_FORMAT`, le format écrit à la création, passe à 2 quand le modèle, les blocs et `concepteur-recette` savent l'écrire ;
5. une recette du dépôt passe au format 2 seulement si elle utilise ce qu'il apporte ;
6. le CHANGELOG le dit (section « Page » et notes du plugin).

Cesser de lire le format 1 serait un changement majeur de la page, annoncé à l'avance et accompagné d'une conversion des recettes.

## 2ter. Le format 2 (2026-10-16) : une étape qui vérifie relit la source

**Ce qu'il ajoute.** Le champ d'étape `reads_source` (§1.10) ; rien d'autre ne change. Une recette au format 2 qui ne s'en sert pas se joue exactement comme au format 1.

**Pourquoi c'est un format et pas un champ facultatif du format 1.** Le critère du §2bis : une recette écrite selon les nouvelles règles serait-elle mal jouée **sans le dire** par l'exécuteur actuel ? Oui. Un exécuteur du format 1 ignore les clés qu'il ne connaît pas : il jouerait l'étape de vérification sans la source et rendrait un contrôle qui a l'air complet — exactement le défaut que le champ corrige (dans la preuve, « 0 contredite » au lieu de 4). Ce n'est pas un libellé qu'on peut ignorer sans danger, comme `label` ou `summary_fr`. Le passage au format 2 fait refuser la recette par une page plus ancienne (« mettez la page à jour ») au lieu de la jouer à moitié. Dans l'autre sens, rien ne casse : l'exécuteur du format 2 joue toute recette au format 1 telle quelle, sans migration.

**Ce qui a suivi les étapes du §2bis.** Ce document décrit le format 2 sans retirer le format 1 ; l'exécuteur joue les deux (`RECIPE_FORMATS = (1, 2)`) ; `build.py` accepte 2 (la copie d'ix-skills est à mettre à jour de la même façon) ; la page passe en 1.1.0 ; `RECIPE_FORMAT` reste 1, et la page écrit 2 seulement quand une étape relit la source ; aucune recette du dépôt ne passe au format 2, aucune ne s'en sert encore ; le CHANGELOG le dit.

**Ce que reçoit l'étape.** Le texte exact de `input.md`, en entrée nommée `source`, après ses autres entrées, avec une consigne : c'est la référence du contrôle, une preuve et non une demande ; ne pas y répondre ni refaire le travail demandé ; la citer brièvement. Le contrôle d'isolation de son message écarte ce seul bloc : un passage de la demande dans un autre champ reçu reste une fuite. Sa relance éventuelle, qui lui renvoie sa propre sortie, n'est pas contrôlée (elle peut citer la source). Ses champs transmis restent contrôlés (§1.10).

## 3. Les pauses

| `pause` | L'orchestrateur… | Reprend quand… |
|---|---|---|
| `none` | enchaîne | — |
| `validate` | montre la sortie de l'étape (et la fiche de contexte après l'étape 1) | l'humain valide ou corrige |
| `answers` | montre les questions à poser à un tiers (client, acheteur) et **s'arrête** | l'humain colle les réponses, ou dit d'avancer sans (les points restent alors des hypothèses). Sur l'étape 1, cette pause valide aussi la fiche de contexte : inutile d'ajouter une étape pour loger l'attente des réponses |
| `choose` | présente l'embranchement prévu (ex. « plusieurs voies restent ouvertes : passer par `explorer` → `decision` ? ») | l'humain choisit |

Un sous-agent ne parle jamais à l'humain : toutes les pauses passent par l'orchestrateur.

## 4. Le corps du SKILL.md

Ordre des sections, en anglais comme tout corps de skill :

1. **Role** — orchestrer, jamais faire le travail d'une étape.
2. **Absolute rules** — les principes du §1, dans les termes de la recette.
3. **Context sheet** — les champs et leur définition, en tableau `| \`champ\` | définition |` : l'exécuteur (`scripts/parcours.py`) envoie ces définitions à l'étape 1 avec les clés à remplir — un nom de clé seul ne dit ni ce qui y va, ni ce qui reste dehors.
4. **Steps** — un tableau : étape, skill, mission, reçoit, transmet, pause.
5. **Running a step** — le gabarit du message envoyé au sous-agent (skill à utiliser, modèle, mission, fiche de contexte, champs reçus, fichier de trace où écrire la sortie complète, réponse limitée au bloc `## HANDOFF` et à un résumé, interdiction de dépasser la mission).
6. **Pauses** — ce qu'on montre, ce qu'on attend.
7. **Trace** — si la plateforme permet d'écrire des fichiers : chaque sortie complète dans `./parcours/<slug>/NN-<étape>.md` et la fiche de contexte dans `00-context.md`, pour relire, auditer ou reprendre.
8. **Without sub-agents** — le repli : enchaîner dans la conversation en ouvrant chaque étape par un bloc qui ne contient que ses entrées, et dire en tête de sortie que l'isolation n'a pas été possible.
9. **Output** — la sortie de la dernière étape, plus une trace courte (étapes jouées, pauses, ce qui est resté hypothèse).
10. **Definition of done**.

## 5. Réutiliser une chaîne

v1 : une recette ne lance pas une autre recette-workflow. Elle **réutilise ses étapes** en les recopiant dans sa propre liste (ex. la réponse à appel d'offres reprend les étapes `questioning` → `brief` de `brief-client`). Une imbrication réelle (un parcours qui en lance un autre avec ses propres pauses) attendra l'exécuteur du lot 2.

## 6. Portabilité

| Plateforme | Isolation | Remarque |
|---|---|---|
| Claude Code | sous-agent par étape | cas nominal |
| Codex, agy (plugins installés) | non testée en conversation | nommer la recette dans la demande ; l'exécuteur du lot 2 donnera une isolation réelle via `codex exec` / `agy -p` |
| Cowork, interfaces de chat | repli (§4.8) | la recette le dit en tête de sortie |

## 7. Ce qui n'est pas dans la v1

Sortie JSON des étapes (lot 2), état persistant et reprise automatique (lot 2), interface de suivi et serveur MCP (lot 3), imbrication de recettes, exécution parallèle, boucles. La vérification de calcul est spécifiée ([`atome-verification-calcul.md`](atome-verification-calcul.md)) et admise à relire la source, mais son atome n'existe pas encore dans ix-skills.
