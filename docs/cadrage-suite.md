# Cadrage — la suite d'ix-recipes

État au 2026-10-14, après la séparation ix-skills / ix-recipes, la récupération des références métier et la revue des 46 recettes.

## 1. Intention

Faire d'ix-recipes un vrai livre de recettes : des skills métier qui marchent seuls dans Claude, et des enchaînements d'atomes ix-skills qu'on peut suivre pas à pas — à la main dans une conversation, par script, ou depuis une petite interface — sans reconstruire le moteur lourd d'ix-memory (base, runs, composer, catalogue).

Le problème de fond à ne pas reproduire : dans ix-memory, chaque étape relisait le brief de départ, la livraison défaisait la décision et la décision corrigeait au lieu de trancher. `handoff.fields` devait l'empêcher et n'a jamais été appliqué.

## 2. Acquis (contraintes)

- **ix-recipes dépend d'ix-skills, jamais l'inverse.** Ids uniques entre les deux repos.
- **Le skill unique reste la règle.** Revue des 46 recettes : 39 restent des skills, 5 deviennent des workflows, 2 sont à fusionner. L'ancien composer avait choisi « skill unique » 14 fois sur 14.
- **Les annexes se lisent à la demande** (`partials/` → `references/`), éprouvé sur les recettes RH et sur `prioritize`.
- **Règles de chaîne héritées d'ix-memory** : chaîne la plus courte défendable, linéaire, une mission locale par étape, brief brut à l'étape 1 seulement, une étape ne refait pas le travail d'une autre, l'orchestrateur ne tranche jamais sur le fond, pas de requalification d'un champ reçu sans le signaler.
- **Clés JSON en anglais** (décision du 2026-10-06).
- **Repos publics, sources créditées** (`THIRD_PARTY.md`).

## 3. Chantiers

| # | Chantier | Dépend de | Taille |
|---|---|---|---|
| A | **Format de recette** : spec du SKILL.md de workflow | — | moyenne |
| B | **Prototype `brief-client`** : `cadrage` → `questioning` → réponses du client → [`explorer` → `decision`] → `brief`, plus un `mode: handoff` sur `cadrage`, `questioning`, `brief` | A | moyenne |
| C | **Sortie machine (JSON)** : schéma par skill (`skills/<id>.schema.json`), `output: json` remplace le Markdown, ids conservés, champ `nature` observé / déduit | A pour les clés de handoff | grande |
| D | **État d'un parcours** : un fichier JSON qui décrit les étapes, leur statut, leurs sorties, les questions en attente — indépendant de l'interface | C | moyenne |
| E | **Exécution et suivi** : script (`claude -p` par étape, ne transmet que les champs de handoff), puis interface | D | grande |
| F | **Les 5 workflows** : note-strategique, offer-comparison, business-case-draft, strategie-prix (à enrichir, sinon fusion), persona | A, B | moyenne |
| G | **Parcours métier documentés** : recrutement, achats (`vendor-scorecard` → `rfp-draft` → offres → `total-cost-analysis` → `decision`), réponse à appel d'offres, produit | A | petite par parcours |
| H | **Fusions** : `feature-spec` → `product-spec` ; `contrat-fournisseur` → `cgv-checker` (à discuter) | — | petite |
| I | **Recettes minces** : 13 signalées ; `feature-spec` et `ticket-triage` peuvent retrouver le savoir de leur source Anthropic | — | moyenne |

## 4. Options pour le suivi des parcours (chantier E)

| | Script local | Interface locale | Page claude.ai (Artifact) |
|---|---|---|---|
| Ce que c'est | `claude -p` par étape, état en JSON sur disque | une page servie depuis le Mac, qui lit l'état et lance le script | une page hébergée, état partagé dans sa base |
| Qui exécute les étapes | le script | le script, déclenché depuis la page | Claude, dans la conversation ou via la page (capacité « demander à Claude » à vérifier) |
| Isolation entre étapes | **réelle** : le script choisit ce qu'il transmet | réelle | dépend de l'exécution |
| Partage | non | non | **oui** (lien privé, partageable) |
| Installation | aucune | un petit serveur | aucune |
| Pour qui | toi | toi | toi et d'autres (client, collègue) |

**Recommandation :** construire d'abord l'état (D) et le script (E, colonne 1) sur un seul parcours, puisque c'est là que l'isolation est réelle et que le JSON sert vraiment. L'interface se pose ensuite sur le même état ; le choix entre interface locale et page claude.ai dépend de la question 3 ci-dessous.

## 5. Hypothèses à valider

1. Sous Claude Code, un SKILL.md de workflow peut faire tourner chaque étape dans un sous-agent qui ne reçoit que le handoff ; le comportement sous Cowork n'est pas connu.
2. Une page claude.ai peut faire exécuter une étape par Claude depuis la page elle-même (à vérifier dans les capacités des Artifacts).
3. Cowork accepte les sources `git-subdir` du catalogue `amiel-35/plugins` (à tester avec « Ajouter depuis un dépôt »).
4. Un `mode: handoff` en Markdown compact suffit quand un modèle lit l'étape suivante ; le JSON n'est nécessaire que quand un script filtre.

## 6. Questions ouvertes (à trancher par Amiel)

1. **Isolation** : sous-agent par étape sous Claude Code (consignes en repli ailleurs), ou consignes partout pour un comportement identique sur toutes les plateformes ?
2. **Brief brut à la dernière étape** : le redonner pour le destinataire et le format, ou jamais après l'étape 1 ?
3. **Pour qui sont les parcours suivis** : toi seul (script + interface locale suffisent), ou aussi des clients ou collègues (page claude.ai partageable) ?
4. **Premier parcours outillé** : recrutement (le plus riche, références métier prêtes) ou réponse à appel d'offres (le plus fréquent en conseil) ?
5. **Fusion `contrat-fournisseur` / `cgv-checker`** : on fusionne, ou on garde les deux ?

## 7. Ordre proposé

1. **Lot 1** — A + B : spec du format, prototype `brief-client`, testé sur un vrai brief client.
2. **Lot 2** — C + D + E (script) : sortie JSON des skills d'un parcours, état du parcours, runner en script.
3. **Lot 3** — E (interface) sur ce même parcours.
4. **Lot 4** — F, G, H, I au fil de l'eau, chaque recette convertie selon le format validé au lot 1.

## 8. Prochain pas

Écrire la spec du format (A) en partant de la synthèse des workflows d'ix-memory, puis le prototype `brief-client` (B), dès que les questions 1 et 2 sont tranchées.
