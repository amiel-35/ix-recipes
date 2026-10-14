# Format d'une recette-workflow

Spécification v1 du 2026-10-14. Une **recette-workflow** est un skill d'ix-recipes qui enchaîne plusieurs skills (atomes d'ix-skills ou autres recettes) pour un travail récurrent. Elle reprend ce qu'ix-memory avait éprouvé (chaîne courte, mission locale par étape, handoff borné, pauses humaines) et corrige ce qui n'avait jamais marché (le brief de départ qui pollue les étapes aval, `handoff.fields` jamais appliqué).

Une recette qui n'enchaîne rien reste un skill ordinaire : c'est le cas par défaut.

## 1. Principes

1. **Isolation.** Chaque étape tourne dans un contexte neuf — un sous-agent quand la plateforme en a (Claude Code), un appel neuf quand un script exécute (`claude -p`, `codex exec`, `agy -p`, `vibe -p`). Elle ne reçoit **que** ce que sa ligne « reçoit » liste. Les consignes (« ignore ce qui précède ») ne sont qu'un repli là où rien ne permet d'isoler.
2. **Le brief brut ne va qu'à l'étape 1.** Jamais au-delà, pas même à la dernière.
3. **La fiche de contexte remplace le brief pour la suite.** L'étape 1 la produit, l'humain la valide, toutes les étapes la reçoivent. Elle contient des faits (entités, objectif, contraintes, destinataire, format, échéances, solutions déjà nommées), jamais de demande d'action.
4. **Handoff nommé et borné.** Chaque étape termine sa sortie par un bloc `## HANDOFF` avec les seuls champs que la recette lui demande de transmettre (1 à 5). L'étape suivante reçoit ces champs, pas la sortie complète.
5. **Une étape = un rôle.** Elle ne refait pas le travail d'une autre et ne requalifie pas un champ reçu sans le signaler (`requalifié : <raison>`).
6. **L'orchestrateur ne tranche jamais sur le fond.** Il enchaîne, s'arrête aux pauses, s'arrête si une étape signale un blocage, et fait choisir l'humain quand la recette prévoit un embranchement.
7. **Orchestrateur léger.** Le sous-agent écrit sa sortie complète dans le fichier de trace et ne renvoie à l'orchestrateur que son bloc `## HANDOFF` et un résumé de cinq lignes. L'orchestrateur n'accumule pas les sorties ; un modèle léger (Sonnet) lui suffit, et chaque étape indique le sien (`model`). Règle par défaut : **Opus pour l'étape 1**, seule à lire la source brute, car ce qu'elle rate est perdu pour toute la suite ; **Sonnet pour les autres**, y compris les décisions, que l'humain valide juste après ; Opus en option sur une étape à fort enjeu.
8. **Chaîne courte et linéaire.** Pas de boucle, pas de parallèle. Une étape optionnelle n'est lancée que si l'humain le décide à la pause qui la précède.

## 2. Frontmatter

En plus du frontmatter canonique (CLAUDE.md §3), une recette-workflow déclare :

```yaml
category: workflow
requires: [ix-skills:cadrage, ix-skills:questioning, ix-skills:brief]
workflow:
  context_sheet: [entities, objective, constraints, recipient, format, deadlines, named_solutions]
  steps:
    - id: cadrage                 # identifiant unique de l'étape
      skill: ix-skills:cadrage    # skill exécuté, avec son espace de noms ; doit figurer dans requires
      mission: Clarify the need…  # mission locale, en une ou deux phrases
      receives: [brief]           # brief (étape 1 seulement), context_sheet, answers, ou <étape>.<champ>
      transmits: [need, constraints, hypotheses, open_points]
      produces_context_sheet: true   # étape 1 seulement
      pause: validate             # none | validate | answers | choose
      model: opus                 # opus | sonnet | haiku — indication pour Claude Code et l'exécuteur (voir §1.7)
    - id: explorer
      skill: ix-skills:explorer
      optional: true              # lancée seulement si l'humain le décide à la pause précédente
      …
```

`build.py` vérifie mécaniquement :

- chaque `skill` figure dans `requires`, et chaque id de `requires` existe (dans ix-recipes, ou dans `../ix-skills/skills/` quand le dépôt voisin est présent) ;
- les ids d'étape sont uniques ;
- seule la première étape reçoit `brief`, et c'est elle qui porte `produces_context_sheet` ;
- chaque `<étape>.<champ>` reçu existe dans les `transmits` d'une étape **antérieure** ;
- `answers` n'est reçu qu'après une étape dont la pause vaut `answers` ;
- chaque `skill` est cité dans le corps du SKILL.md (le corps et le frontmatter ne divergent pas) ;
- `model`, s'il est donné, vaut `sonnet`, `opus` ou `haiku`.

Le frontmatter est la version lisible par machine : c'est elle que l'exécuteur du lot 2 lira.

## 3. Les pauses

| `pause` | L'orchestrateur… | Reprend quand… |
|---|---|---|
| `none` | enchaîne | — |
| `validate` | montre la sortie de l'étape (et la fiche de contexte après l'étape 1) | l'humain valide ou corrige |
| `answers` | montre les questions à poser à un tiers (client, acheteur) et **s'arrête** | l'humain colle les réponses, ou dit d'avancer sans (les points restent alors des hypothèses) |
| `choose` | présente l'embranchement prévu (ex. « plusieurs voies restent ouvertes : passer par `explorer` → `decision` ? ») | l'humain choisit |

Un sous-agent ne parle jamais à l'humain : toutes les pauses passent par l'orchestrateur.

## 4. Le corps du SKILL.md

Ordre des sections, en anglais comme tout corps de skill :

1. **Role** — orchestrer, jamais faire le travail d'une étape.
2. **Absolute rules** — les principes du §1, dans les termes de la recette.
3. **Context sheet** — les champs et leur définition.
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

Sortie JSON des étapes (lot 2), état persistant et reprise automatique (lot 2), interface de suivi et serveur MCP (lot 3), imbrication de recettes, exécution parallèle.
